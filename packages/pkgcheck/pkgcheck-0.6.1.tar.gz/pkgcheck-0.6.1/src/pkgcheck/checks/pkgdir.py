from collections import defaultdict
import os
import stat

from pkgcore.ebuild.atom import MalformedAtom, atom as atom_cls
from snakeoil.chksum import get_chksums
from snakeoil.osutils import listdir, pjoin, sizeof_fmt
from snakeoil.strings import pluralism as _pl

from .. import base, sources


allowed_filename_chars = "a-zA-Z0-9._-+:"
allowed_filename_chars_set = set()
allowed_filename_chars_set.update(chr(x) for x in range(ord('a'), ord('z')+1))
allowed_filename_chars_set.update(chr(x) for x in range(ord('A'), ord('Z')+1))
allowed_filename_chars_set.update(chr(x) for x in range(ord('0'), ord('9')+1))
allowed_filename_chars_set.update([".", "-", "_", "+", ":"])


class MismatchedPN(base.PackageResult, base.Error):
    """Ebuilds that have different names than their parent directory."""

    def __init__(self, pkg, ebuilds):
        super().__init__(pkg)
        self.ebuilds = tuple(sorted(ebuilds))

    @property
    def short_desc(self):
        return "mismatched package name%s: [ %s ]" % (
            _pl(self.ebuilds), ', '.join(self.ebuilds))


class InvalidPN(base.PackageResult, base.Error):
    """Ebuilds that have invalid package names."""

    def __init__(self, pkg, ebuilds):
        super().__init__(pkg)
        self.ebuilds = tuple(sorted(ebuilds))

    @property
    def short_desc(self):
        return "invalid package name%s: [ %s ]" % (
            _pl(self.ebuilds), ', '.join(self.ebuilds))


class EqualVersions(base.PackageResult, base.Error):
    """Ebuilds that have equal versions.

    For example, cat/pn-1.0.2, cat/pn-1.0.2-r0, cat/pn-1.0.2-r00 and
    cat/pn-1.000.2 all have equal versions according to PMS and therefore
    shouldn't exist in the same repository.
    """

    def __init__(self, pkg, versions):
        super().__init__(pkg)
        self.versions = tuple(sorted(versions))

    @property
    def short_desc(self):
        return f"equal package versions: [ {', '.join(self.versions)} ]"


class DuplicateFiles(base.PackageResult, base.Warning):
    """Two or more identical files in FILESDIR."""

    def __init__(self, pkg, files):
        super().__init__(pkg)
        self.files = tuple(sorted(files))

    @property
    def short_desc(self):
        return 'duplicate identical files in FILESDIR: %s' % (
            ', '.join(map(repr, self.files)))


class EmptyFile(base.PackageResult, base.Warning):
    """File in FILESDIR is empty."""

    def __init__(self, pkg, filename):
        super().__init__(pkg)
        self.filename = filename

    @property
    def short_desc(self):
        return f'empty file in FILESDIR: {self.filename!r}'


class ExecutableFile(base.PackageResult, base.Warning):
    """File has executable bit, but doesn't need it."""

    def __init__(self, pkg, filename):
        super().__init__(pkg)
        self.filename = filename

    @property
    def short_desc(self):
        return f'unnecessary executable bit: {self.filename!r}'


class SizeViolation(base.PackageResult, base.Warning):
    """File in $FILESDIR is too large (current limit is 20k)."""

    def __init__(self, pkg, filename, size):
        super().__init__(pkg)
        self.filename = filename
        self.size = size

    @property
    def short_desc(self):
        return f'{self.filename!r} exceeds 20k in size; {sizeof_fmt(self.size)} total'


class Glep31Violation(base.PackageResult, base.Error):
    """File doesn't abide by glep31 requirements."""

    def __init__(self, pkg, filename):
        super().__init__(pkg)
        self.filename = filename

    @property
    def short_desc(self):
        return "filename contains char outside the allowed ranges defined " \
               f"by glep31: {self.filename!r}"


class InvalidUTF8(base.PackageResult, base.Error):
    """File isn't UTF-8 compliant."""

    def __init__(self, pkg, filename, err):
        super().__init__(pkg)
        self.filename = filename
        self.err = err

    @property
    def short_desc(self):
        return f"invalid UTF-8: {self.err}: {self.filename!r}"


class PkgDirCheck(base.Check):
    """Actual ebuild directory scans; file size, glep31 rule enforcement."""

    feed_type = base.raw_package_feed
    source = sources.RawRepoSource

    ignore_dirs = frozenset(["cvs", ".svn", ".bzr"])
    known_results = (
        DuplicateFiles, EmptyFile, ExecutableFile, SizeViolation,
        Glep31Violation, InvalidUTF8, MismatchedPN, InvalidPN,
    )

    # TODO: put some 'preferred algorithms by purpose' into snakeoil?
    digest_algo = 'sha256'

    def feed(self, pkgset):
        pkg = pkgset[0]
        pkg_path = pjoin(self.options.target_repo.location, pkg.category, pkg.package)
        ebuild_ext = '.ebuild'
        mismatched = []
        invalid = []
        # note we don't use os.walk, we need size info also
        for filename in listdir(pkg_path):
            # while this may seem odd, written this way such that the
            # filtering happens all in the genexp.  if the result was being
            # handed to any, it's a frame switch each
            # char, which adds up.

            if any(True for x in filename if x not in allowed_filename_chars_set):
                yield Glep31Violation(pkg, filename)

            if (filename.endswith(ebuild_ext) or filename in
                    ("Manifest", "metadata.xml")):
                if os.stat(pjoin(pkg_path, filename)).st_mode & 0o111:
                    yield ExecutableFile(pkg, filename)

            if filename.endswith(ebuild_ext):
                try:
                    with open(pjoin(pkg_path, filename), mode='rb') as f:
                        f.read(8192).decode()
                except UnicodeDecodeError as e:
                    yield InvalidUTF8(pkg, filename, str(e))

                pkg_name = os.path.basename(filename[:-len(ebuild_ext)])
                try:
                    pkg_atom = atom_cls(f'={pkg.category}/{pkg_name}')
                    if pkg_atom.package != os.path.basename(pkg_path):
                        mismatched.append(pkg_name)
                except MalformedAtom:
                    invalid.append(pkg_name)

        if mismatched:
            yield MismatchedPN(pkg, mismatched)
        if invalid:
            yield InvalidPN(pkg, invalid)

        files_by_size = defaultdict(list)
        pkg_path_len = len(pkg_path) + 1
        for root, dirs, files in os.walk(pjoin(pkg_path, 'files')):
            # don't visit any ignored directories
            for d in self.ignore_dirs.intersection(dirs):
                dirs.remove(d)
            base_dir = root[pkg_path_len:]
            for file_name in files:
                file_stat = os.lstat(pjoin(root, file_name))
                if stat.S_ISREG(file_stat.st_mode):
                    if file_stat.st_mode & 0o111:
                        yield ExecutableFile(pkg, pjoin(base_dir, file_name))
                    if file_stat.st_size == 0:
                        yield EmptyFile(pkg, pjoin(base_dir, file_name))
                    else:
                        files_by_size[file_stat.st_size].append(pjoin(base_dir, file_name))
                        if file_stat.st_size > 20480:
                            yield SizeViolation(pkg, pjoin(base_dir, file_name), file_stat.st_size)
                    if any(True for char in file_name if char not in allowed_filename_chars_set):
                        yield Glep31Violation(pkg, pjoin(base_dir, file_name))

        files_by_digest = defaultdict(list)
        for size, files in files_by_size.items():
            if len(files) > 1:
                for f in files:
                    digest = get_chksums(pjoin(pkg_path, f), self.digest_algo)[0]
                    files_by_digest[digest].append(f)

        for digest, files in files_by_digest.items():
            if len(files) > 1:
                yield DuplicateFiles(pkg, files)


class EqualVersionsCheck(base.Check):
    """Scan package ebuilds for semantically equal versions."""

    feed_type = base.package_feed
    known_results = (EqualVersions,)

    def feed(self, pkgset):
        equal_versions = defaultdict(set)
        sorted_pkgset = sorted(pkgset)
        for i, pkg_a in enumerate(sorted_pkgset):
            try:
                pkg_b = sorted_pkgset[i + 1]
            except IndexError:
                break
            if pkg_a.versioned_atom == pkg_b.versioned_atom:
                equal_versions[pkg_a.versioned_atom].update([pkg_a.fullver, pkg_b.fullver])
        for atom, versions in equal_versions.items():
            yield EqualVersions(atom, versions)
