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


def read_public(root, relative, limit=MAX_BYTES):
    """Only caller-allowlisted relative regular files; refuse symlinks and devices."""
    parts = Path(relative).parts
    if not parts or Path(relative).is_absolute() or any(p in ('.', '..') for p in parts):
        raise Denied('UNSAFE_PATH')
    fd = None
    try:
        # Open each ancestor without following links, including the root path.
        absolute = Path(root).absolute()
        fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
        for part in absolute.parts[1:] + parts[:-1]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        source = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        with os.fdopen(source, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
                raise Denied('UNSAFE_FILE_OR_SIZE')
            raw = stream.read(limit + 1)
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
