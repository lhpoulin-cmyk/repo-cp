"""Bounded public reads and non-disclosing indicator checks. No secret discovery."""
import json
import os
from pathlib import Path
import re
import stat

MAX_BYTES = 131072


class Denied(ValueError):
    """Only constant public reason codes may be supplied."""


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise Denied('DUPLICATE_FIELD')
        result[key] = value
    return result


def constant(_):
    raise Denied('INVALID_JSON')


def load(raw):
    if not isinstance(raw, bytes) or len(raw) > MAX_BYTES:
        raise Denied('INPUT_SIZE')
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=constant)
    except (ValueError, RecursionError):
        raise Denied('INVALID_JSON') from None


def open_directory(path):
    """Open every directory component without symlink traversal (Linux)."""
    absolute = Path(path).absolute()
    if '..' in absolute.parts:
        raise Denied('UNSAFE_PATH')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in absolute.parts[1:]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        return fd
    except BaseException:
        os.close(fd)
        raise


def open_parent(root, relative):
    if not isinstance(relative, str) or not relative or relative.startswith('/'):
        raise Denied('UNSAFE_PATH')
    parts = relative.split('/')
    if any(p in ('', '.', '..') for p in parts):
        raise Denied('UNSAFE_PATH')
    fd = open_directory(root)
    try:
        for part in parts[:-1]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        return fd, parts[-1]
    except BaseException:
        os.close(fd)
        raise


def require_single_regular(info):
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise Denied('SINGLE_LINK_REGULAR_REQUIRED')


def read_public(root, relative, limit=MAX_BYTES, *, git_internal=False):
    """Only caller-allowlisted relative regular files; refuse symlinks and devices."""
    if git_internal and not relative.startswith('.git/'):
        raise Denied('INVALID_GIT_EXCLUSION')
    fd = None
    try:
        fd, name = open_parent(root, relative)
        source = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_NOATIME, dir_fd=fd)
        with os.fdopen(source, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not git_internal:
                require_single_regular(info)
            if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
                raise Denied('UNSAFE_FILE_OR_SIZE')
            raw = stream.read(limit + 1)
            after = os.fstat(stream.fileno())
            if not git_internal:
                require_single_regular(after)
            if (info.st_size, info.st_mtime_ns, info.st_ctime_ns) != (
                    after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise Denied('PUBLIC_FILE_CHANGED')
            if len(raw) > limit:
                raise Denied('UNSAFE_FILE_OR_SIZE')
            return raw
    except OSError:
        raise Denied('PUBLIC_FILE_UNAVAILABLE') from None
    finally:
        if fd is not None:
            os.close(fd)


def has_indicator(raw):
    # Values are never included in exceptions, reports, or logs. This is a
    # bounded heuristic, not a proof that arbitrary content contains no secrets.
    patterns = [rb'-----BEGIN ' + rb'(?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY',
                rb'AGE-SECRET-' + rb'KEY-', rb'gh[pousr]_' + rb'[A-Za-z0-9]{20,}',
                rb'github_pat_' + rb'[A-Za-z0-9_]{20,}',
                rb'(?i)(?:password|passwd|token|secret|private_key)\s*[=:]\s*["\x27]?[A-Za-z0-9+/=_-]{12,}']
    return any(re.search(pattern, raw) for pattern in patterns)
