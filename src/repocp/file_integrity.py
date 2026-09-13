"""Metadata-only hardlink detection for explicitly governed public paths."""
import errno
import os
from pathlib import Path
import stat

from jsonschema import Draft202012Validator

from .safety import Denied, has_indicator, load, open_directory, open_parent, read_public

INVARIANT = 'HELIX_NO_HARDLINKS_V1'


def invariant(root):
    raw = read_public(root, 'registries/file-integrity.json')
    data = load(raw)
    schema = load(read_public(root, 'schemas/file-integrity-v1.schema.json'))
    if (not isinstance(data, dict) or has_indicator(raw) or type(data.get('schema_version')) is not int
            or not Draft202012Validator(schema).is_valid(data)):
        raise Denied('FILE_INTEGRITY_NONCONFORMANCE')
    for path in data['audit']['repository_excluded_paths']:
        if any(part in ('.', '..') for part in path.split('/')):
            raise Denied('UNSAFE_EXCLUSION')
    return data


def excluded(relative, policy):
    rules = policy['audit']
    return (any(p in rules['excluded_components'] for p in relative.split('/'))
            or any(relative == p or relative.startswith(p + '/')
                   for p in rules['repository_excluded_paths']))


def inspect_link(root, relative, *, protected, policy):
    """No content read, inode numbers or private values in the finding."""
    if excluded(relative, policy):
        return 'NOT_APPLICABLE', 'EXCLUDED_SCOPE'
    parent = source = None
    try:
        base = Path(root).absolute()
        mounts = mountpoints()
        parts = relative.split('/')
        if any(str(base.joinpath(*parts[:i])) in mounts for i in range(1, len(parts) + 1)):
            return 'NOT_APPLICABLE', 'EXCLUDED_MOUNT'
        parent, name = open_parent(root, relative)
        root_fd = open_directory(root)
        try:
            device = os.fstat(root_fd).st_dev
        finally:
            os.close(root_fd)
        if os.fstat(parent).st_dev != device:
            return 'NOT_APPLICABLE', 'EXCLUDED_MOUNT'
        source = os.open(name, os.O_PATH | os.O_NOFOLLOW, dir_fd=parent)
        info = os.fstat(source)
        if info.st_dev != device:
            return 'NOT_APPLICABLE', 'EXCLUDED_MOUNT'
        if stat.S_ISLNK(info.st_mode):
            return 'BLOCKED', 'SYMLINK_REFUSED'
        if not stat.S_ISREG(info.st_mode):
            return 'BLOCKED', 'NONREGULAR_REFUSED'
        if info.st_nlink > 1:
            return ('BLOCKED' if protected else 'DRIFT'), 'HARDLINK_FORBIDDEN'
        if info.st_nlink != 1:
            return 'BLOCKED', 'SINGLE_LINK_REQUIRED'
        return 'PASS', 'SINGLE_LINK_REGULAR'
    except Denied:
        return 'BLOCKED', 'UNSAFE_PATH'
    except OSError as error:
        if error.errno in (errno.ELOOP, errno.ENOTDIR):
            return 'BLOCKED', 'UNSAFE_PATH'
        return 'UNKNOWN', 'METADATA_UNAVAILABLE'
    finally:
        if source is not None:
            os.close(source)
        if parent is not None:
            os.close(parent)


def mountpoints():
    with open('/proc/self/mountinfo', encoding='utf-8') as stream:
        return {line.split(' ')[4].replace('\\040', ' ').replace('\\011', '\t')
                .replace('\\012', '\n').replace('\\134', '\\') for line in stream}


def governed_paths(root, policy):
    """Local development audit only; never used to discover files in peers.

    Descriptor-relative traversal prunes exclusions and different-device mounts
    before descent. Same-device mountpoints are checked against Linux mountinfo.
    Only filesystem mountpoint names are consumed, never artifact contents.
    """
    mounts = mountpoints()
    base = Path(root).absolute()
    parent = open_directory(base)
    try:
        fd = os.open('.', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NOATIME, dir_fd=parent)
    finally:
        os.close(parent)
    try:
        device = os.fstat(fd).st_dev
        def walk(current, prefix):
            with os.scandir(current) as entries:
                names = sorted(entry.name for entry in entries)
            for name in names:
                relative = prefix + name
                if excluded(relative, policy):
                    continue
                info = os.stat(name, dir_fd=current, follow_symlinks=False)
                if info.st_dev != device or str(base / relative) in mounts:
                    continue
                if stat.S_ISDIR(info.st_mode):
                    child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NOATIME,
                                    dir_fd=current)
                    try:
                        opened = os.fstat(child)
                        if (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
                            raise Denied('AUDIT_DIRECTORY_CHANGED')
                        yield from walk(child, relative + '/')
                    finally:
                        os.close(child)
                else:
                    yield relative
        yield from walk(fd, '')
    finally:
        os.close(fd)


def local_audit(root, policy):
    # Import here to reuse the existing report conventions without a cycle.
    from .audit import result, report
    results = []
    try:
        for relative in sorted(governed_paths(root, policy)):
            protected = any(relative == p or relative.startswith(p + '/')
                            for p in policy['audit']['protected_prefixes'])
            status, reason = inspect_link(root, relative, protected=protected, policy=policy)
            # Do not echo arbitrary discovered names: stable ordinal labels only.
            results.append(result('repo-cp', 'RC011', status,
                                  reason + ':LOCAL_FILE_' + str(len(results) + 1).zfill(6)))
    except (Denied, OSError, ValueError):
        results.append(result('repo-cp', 'RC011', 'UNKNOWN', 'AUDIT_COVERAGE_UNAVAILABLE'))
    if not results:
        results.append(result('repo-cp', 'RC011', 'UNKNOWN', 'NO_GOVERNED_FILES'))
    return report(results, ['repo-cp'])
