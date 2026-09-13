"""Unprivileged public/synthetic artifact publication reference, never a CLI lane.

Callers supply reviewed expectations and authorization outside this library.
No credential handling, replacement, remediation, privilege acquisition or DB
transaction is implemented. Directory flock coordinates cooperating writers;
owner-controlled directories and atomic no-replace publication prevent clobber.
Recovery uses durable intent plus independently checked inode/content identity.
"""
from contextlib import contextmanager
import ctypes
from dataclasses import dataclass
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import signal
import stat

from .safety import Denied, open_directory, require_single_regular
from .file_integrity import INVARIANT

TOOL_VERSION = '0.1.0'
__all__ = ('Expectation', 'Outcome', 'PublicationFailure', 'copy_and_publish', 'resolve_publication')


def close_fd(fd):
    try:
        os.close(fd)
    except OSError:
        pass  # All durable writes were fsynced; cleanup cannot replace an outcome.


def require_unprivileged():
    if os.geteuid() == 0 or os.getuid() != os.geteuid() or os.getgid() != os.getegid():
        raise Denied('UNPRIVILEGED_REFERENCE_ONLY')


def check_directory_path(path, directory):
    other = open_directory(path)
    try:
        a, b = os.fstat(directory), os.fstat(other)
        if (a.st_dev, a.st_ino, a.st_uid, a.st_gid, a.st_mode) != (
                b.st_dev, b.st_ino, b.st_uid, b.st_gid, b.st_mode):
            raise Denied('DIRECTORY_PATH_CHANGED')
    finally:
        close_fd(other)


@dataclass(frozen=True)
class Expectation:
    uid: int
    gid: int
    mode: int
    device: int
    size: int
    sha256: str


@dataclass(frozen=True)
class Outcome:
    status: str
    phase: str
    cause: str


class PublicationFailure(Denied):
    def __init__(self, outcome):
        self.outcome = outcome
        super().__init__(outcome.cause)


class Interrupted(Exception):
    pass


@contextmanager
def termination_control():
    """Call on the main thread; restore handlers, including after interruption."""
    previous = {}
    def interrupted(number, frame):
        raise Interrupted('CANCELLED')
    try:
        for number in (signal.SIGINT, signal.SIGHUP, signal.SIGTERM):
            previous[number] = signal.signal(number, interrupted)
        yield
    finally:
        for number, handler in previous.items():
            signal.signal(number, handler)


def absolute_file(path):
    raw = os.fspath(path)
    if (not isinstance(raw, str) or not raw.startswith('/') or raw.startswith('//')
            or any(p in ('', '.', '..') for p in raw[1:].split('/'))
            or any(ord(c) < 32 or ord(c) > 126 for c in raw)):
        raise Denied('ABSOLUTE_UNAMBIGUOUS_PATH_REQUIRED')
    return Path(raw)


def identity(info):
    return (info.st_dev, info.st_ino, info.st_uid, info.st_gid, info.st_mode,
            info.st_size, info.st_nlink, info.st_mtime_ns, info.st_ctime_ns)


def check_metadata(fd, expected):
    info = os.fstat(fd)
    require_single_regular(info)
    if (info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode), info.st_dev,
            info.st_size) != (expected.uid, expected.gid, expected.mode,
                              expected.device, expected.size):
        raise Denied('METADATA_MISMATCH')
    return info


def digest_fd(fd, limit):
    os.lseek(fd, 0, os.SEEK_SET)
    digest = hashlib.sha256()
    count = 0
    while True:
        block = os.read(fd, min(65536, limit - count + 1))
        if not block:
            return count, digest.hexdigest()
        count += len(block)
        if count > limit:
            raise Denied('BYTE_COUNT_MISMATCH')
        digest.update(block)


def verify_fd(fd, expected):
    before = check_metadata(fd, expected)
    if digest_fd(fd, expected.size) != (expected.size, expected.sha256):
        raise Denied('HASH_OR_BYTE_COUNT_MISMATCH')
    if identity(before) != identity(check_metadata(fd, expected)):
        raise Denied('FILE_CHANGED_DURING_VERIFICATION')
    return before


def write_all(fd, block):
    while block:
        written = os.write(fd, block)
        if written <= 0:
            raise Denied('SHORT_WRITE')
        block = block[written:]


def copy_bytes(source, target, size):
    os.lseek(source, 0, os.SEEK_SET)
    count = 0
    while True:
        block = os.read(source, min(65536, size - count + 1))
        if not block:
            break
        count += len(block)
        if count > size:
            raise Denied('BYTE_COUNT_MISMATCH')
        write_all(target, block)
    if count != size:
        raise Denied('BYTE_COUNT_MISMATCH')


def rename_exclusive(directory, source, target):
    """Linux renameat2; never emulate no-replace with a hardlink or check/rename."""
    libc = ctypes.CDLL(None, use_errno=True)
    try:
        rename = libc.renameat2
    except AttributeError:
        raise Denied('ATOMIC_NOREPLACE_UNAVAILABLE') from None
    rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int,
                       ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(directory, os.fsencode(source), directory, os.fsencode(target), 1) != 0:
        number = ctypes.get_errno()
        raise OSError(number, 'ATOMIC_PUBLICATION_UNAVAILABLE')


def create_temp(directory):
    # Directory is locked and owner-controlled; O_EXCL still enforces identity.
    name = '.repo-cp-' + secrets.token_hex(16) + '.tmp'
    fd = os.open(name, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                 0o600, dir_fd=directory)
    try:
        require_single_regular(os.fstat(fd))
    except BaseException:
        close_fd(fd)
        raise
    return name, fd


def remove_own_temp(directory, name, fd):
    """Only remove our still-single-link temporary inode; preserve violations."""
    current = os.stat(name, dir_fd=directory, follow_symlinks=False)
    opened = os.fstat(fd)
    require_single_regular(current)
    require_single_regular(opened)
    if (current.st_dev, current.st_ino, current.st_uid) != (
            opened.st_dev, opened.st_ino, os.geteuid()):
        raise Denied('TEMP_IDENTITY_CHANGED')
    os.unlink(name, dir_fd=directory)
    os.fsync(directory)


def record(directory, name, data):
    """A durable immutable public/synthetic journal record, never a credential receipt."""
    raw = (json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n').encode()
    temporary, fd = create_temp(directory)
    published = False
    try:
        write_all(fd, raw)
        expected = Expectation(os.geteuid(), os.getegid(), 0o600,
                               os.fstat(directory).st_dev, len(raw), hashlib.sha256(raw).hexdigest())
        os.fchown(fd, expected.uid, expected.gid)
        os.fchmod(fd, expected.mode)
        verify_fd(fd, expected)
        os.fsync(fd)
        rename_exclusive(directory, temporary, name)
        published = True
        os.fsync(directory)
        check = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_NOATIME, dir_fd=directory)
        try:
            actual = verify_fd(check, expected)
            if (actual.st_dev, actual.st_ino) != (os.fstat(fd).st_dev, os.fstat(fd).st_ino):
                raise Denied('RECORD_IDENTITY_CHANGED')
        finally:
            close_fd(check)
    finally:
        if not published:
            try:
                remove_own_temp(directory, temporary, fd)
            except (Denied, OSError):
                pass  # Preserve original failure; stale artifact requires review.
        close_fd(fd)


def validate_expectation(expected):
    if (not isinstance(expected, Expectation)
            or any(type(v) is not int or v < 0 for v in
                   (expected.uid, expected.gid, expected.mode, expected.device, expected.size))
            or expected.mode > 0o777 or not isinstance(expected.sha256, str)
            or re.fullmatch('[0-9a-f]{64}', expected.sha256) is None):
        raise Denied('INVALID_EXPECTATION')


def names(operation):
    if not isinstance(operation, str) or re.fullmatch('[0-9a-f]{32}', operation) is None:
        raise Denied('INVALID_OPERATION_ID')
    return '.repo-cp-' + operation + '.intent.json', '.repo-cp-' + operation + '.receipt.json'


@contextmanager
def locked_directory(path, device):
    directory = open_directory(path)
    try:
        info = os.fstat(directory)
        if info.st_uid != os.geteuid() or info.st_mode & 0o022 or info.st_dev != device:
            raise Denied('DESTINATION_DIRECTORY_POLICY')
        try:
            fcntl.flock(directory, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Denied('CONCURRENCY_CONFLICT') from None
        yield directory
        check_directory_path(path, directory)
        after = os.fstat(directory)
        if (info.st_dev, info.st_ino, info.st_uid, info.st_gid, info.st_mode) != (
                after.st_dev, after.st_ino, after.st_uid, after.st_gid, after.st_mode):
            raise Denied('DESTINATION_DIRECTORY_CHANGED')
    finally:
        close_fd(directory)  # Kernel releases flock even after process death.


def exists(directory, name):
    try:
        os.stat(name, dir_fd=directory, follow_symlinks=False)
        return True
    except FileNotFoundError:
        return False


def failure_outcome(error, phase, primary_possible):
    if primary_possible:
        return Outcome('RECOVERY_REQUIRED', phase, 'PRIMARY_STATE_MAY_BE_COMMITTED')
    if isinstance(error, (Interrupted, KeyboardInterrupt)):
        return Outcome('INTERRUPTED', phase, 'CANCELLED')
    causes = {'CONCURRENCY_CONFLICT', 'EXISTING_STATE_REQUIRES_RESOLUTION'}
    cause = str(error) if isinstance(error, Denied) and str(error) in causes else (
        'INTEGRITY_OR_POLICY_REJECTION' if isinstance(error, Denied) else
        'CAPABILITY_OR_IO_FAILURE' if isinstance(error, OSError) else 'INTERNAL_FAILURE')
    return Outcome('FAILED', phase, cause)


def copy_and_publish(source, destination, *, source_expected, destination_expected, operation,
                     reviewed_revision):
    """Create a NEW public/synthetic artifact. Existing destinations are never changed.

    An exact reviewed plan and owner authorization are caller preconditions.
    Source and destination expectations include device, uid, gid, mode, size,
    SHA-256. Cross-filesystem sources are supported; only temporary-to-final
    rename is same-filesystem. All errors are value-free typed outcomes.
    """
    phase = 'MUTATION_NOT_STARTED'
    primary_possible = False
    source_fd = parent = target_fd = None
    temporary = None
    try:
        require_unprivileged()
        if not isinstance(reviewed_revision, str) or re.fullmatch('[0-9a-f]{40}', reviewed_revision) is None:
            raise Denied('REVIEWED_REVISION_REQUIRED')
        validate_expectation(source_expected)
        validate_expectation(destination_expected)
        if (source_expected.size, source_expected.sha256) != (
                destination_expected.size, destination_expected.sha256):
            raise Denied('COPY_EXPECTATIONS_DIFFER')
        source = absolute_file(source)
        destination = absolute_file(destination)
        intent_name, receipt_name = names(operation)
        with termination_control(), locked_directory(destination.parent, destination_expected.device) as directory:
            if any(exists(directory, name) for name in (destination.name, intent_name, receipt_name)):
                raise Denied('EXISTING_STATE_REQUIRES_RESOLUTION')
            parent = open_directory(source.parent)
            source_fd = os.open(source.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_NOATIME,
                                dir_fd=parent)
            source_before = verify_fd(source_fd, source_expected)
            temporary, target_fd = create_temp(directory)
            target_info = os.fstat(target_fd)
            intent = {'schema_version': 1, 'invariant_id': INVARIANT,
                      'policy_version': '1.0.0', 'tool_version': TOOL_VERSION,
                      'reviewed_revision': reviewed_revision,
                      'operation': operation, 'status': 'STARTED', 'phase': 'MUTATION_PREPARED',
                      'target': destination.name, 'temporary': temporary,
                      'inode': target_info.st_ino, 'expected': destination_expected.__dict__}
            try:
                record(directory, intent_name, intent)
                phase = 'MUTATION_PREPARED'
                copy_bytes(source_fd, target_fd, source_expected.size)
                os.fchown(target_fd, destination_expected.uid, destination_expected.gid)
                os.fchmod(target_fd, destination_expected.mode)
                verify_fd(target_fd, destination_expected)
                if identity(source_before) != identity(verify_fd(source_fd, source_expected)):
                    raise Denied('SOURCE_CHANGED')
                check_directory_path(source.parent, parent)
                current_source = os.stat(source.name, dir_fd=parent, follow_symlinks=False)
                if identity(current_source) != identity(source_before):
                    raise Denied('SOURCE_PATH_CHANGED')
                os.fsync(target_fd)
                check_directory_path(destination.parent, directory)
                # Once publication is attempted, never assert the primary is unchanged.
                primary_possible = True
                phase = 'PRIMARY_STATE_COMMIT_ATTEMPTED'
                rename_exclusive(directory, temporary, destination.name)
                phase = 'RECEIPT_PENDING'
                os.fsync(directory)
                verify_published(directory, intent, destination_expected)
                record(directory, receipt_name, completed_record(intent))
                verify_published(directory, intent, destination_expected)
                return Outcome('COMPLETED', 'OPERATION_COMPLETED', 'POSTCONDITIONS_VERIFIED')
            except (Exception, KeyboardInterrupt) as error:
                # Best-effort durable categorical outcome; original error wins if
                # storage or cancellation also prevents writing this record.
                try:
                    if exists(directory, intent_name):
                        outcome = failure_outcome(error, phase, primary_possible)
                        record(directory, '.repo-cp-' + operation + '.outcome.json',
                               {**completed_record(intent), **outcome.__dict__})
                except (Exception, KeyboardInterrupt):
                    pass  # Durable intent remains the recovery authority.
                raise
            finally:
                if not primary_possible:
                    try:
                        remove_own_temp(directory, temporary, target_fd)
                    except (Denied, OSError):
                        pass  # No last-known-good file or existing violation is deleted.
    except (Exception, KeyboardInterrupt) as error:
        raise PublicationFailure(failure_outcome(error, phase, primary_possible)) from None
    finally:
        for fd in (target_fd, source_fd, parent):
            if fd is not None:
                close_fd(fd)


def completed_record(intent):
    return {'schema_version': 1, 'invariant_id': INVARIANT,
            'policy_version': '1.0.0', 'tool_version': TOOL_VERSION,
            'reviewed_revision': intent['reviewed_revision'],
            'operation': intent['operation'],
            'intent_sha256': hashlib.sha256(json.dumps(intent, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            'status': 'COMPLETED', 'phase': 'OPERATION_COMPLETED',
            'cause': 'POSTCONDITIONS_VERIFIED'}


def read_record(directory, name):
    from .safety import load
    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_NOATIME, dir_fd=directory)
    try:
        info = os.fstat(fd)
        require_single_regular(info)
        if (info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode)) != (os.geteuid(), os.getegid(), 0o600):
            raise Denied('RECORD_METADATA_MISMATCH')
        if info.st_size > 16384:
            raise Denied('RECORD_SIZE')
        raw = os.read(fd, 16385)
        if len(raw) != info.st_size or identity(info) != identity(os.fstat(fd)):
            raise Denied('RECORD_CHANGED')
        return load(raw)
    finally:
        os.close(fd)


def verify_published(directory, intent, expected):
    fd = os.open(intent['target'], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_NOATIME,
                 dir_fd=directory)
    try:
        info = verify_fd(fd, expected)
        if info.st_ino != intent['inode']:
            raise Denied('PUBLISHED_IDENTITY_CHANGED')
    finally:
        os.close(fd)


def resolve_publication(destination, *, destination_expected, operation, reviewed_revision, finalize=False):
    """Inspect stale intent; explicit finalize only durably acknowledges verified state.

    No automatic resume, rollback, destination rewrite or stale-file deletion.
    Absent primary state and already-committed primary state remain distinct.
    A caller can prepare a new operation after separate authorized cleanup of a
    failed preparation. Repeated finalization independently verifies the target.
    """
    try:
        require_unprivileged()
        if type(finalize) is not bool or not isinstance(reviewed_revision, str) or re.fullmatch('[0-9a-f]{40}', reviewed_revision) is None:
            raise Denied('INVALID_RECOVERY_PLAN')
        validate_expectation(destination_expected)
        destination = absolute_file(destination)
        intent_name, receipt_name = names(operation)
        with termination_control(), locked_directory(destination.parent, destination_expected.device) as directory:
            if not exists(directory, intent_name):
                return Outcome('RECOVERY_REQUIRED', 'OPERATOR_ADJUDICATION', 'INTENT_UNAVAILABLE')
            intent = read_record(directory, intent_name)
            if (set(intent) != {'schema_version', 'invariant_id', 'operation', 'status', 'phase',
                                'policy_version', 'tool_version', 'reviewed_revision',
                                'target', 'temporary', 'inode', 'expected'}
                    or type(intent['schema_version']) is not int or intent['schema_version'] != 1
                    or intent['invariant_id'] != INVARIANT
                    or intent['policy_version'] != '1.0.0' or intent['tool_version'] != TOOL_VERSION
                    or intent['reviewed_revision'] != reviewed_revision
                    or intent['operation'] != operation or intent['status'] != 'STARTED'
                    or intent['phase'] != 'MUTATION_PREPARED'
                    or intent['target'] != destination.name
                    or intent['expected'] != destination_expected.__dict__
                    or type(intent['inode']) is not int or intent['inode'] <= 0
                    or not isinstance(intent['temporary'], str)
                    or re.fullmatch(r'\.repo-cp-[0-9a-f]{32}\.tmp', intent['temporary']) is None):
                raise Denied('INTENT_MISMATCH')
            if not exists(directory, destination.name):
                if exists(directory, receipt_name):
                    return Outcome('RECOVERY_REQUIRED', 'OPERATOR_ADJUDICATION', 'COMPLETED_PRIMARY_MISSING')
                return Outcome('RECOVERY_REQUIRED', 'ROLLBACK_REQUIRED', 'PRIMARY_STATE_UNCHANGED')
            verify_published(directory, intent, destination_expected)
            if exists(directory, receipt_name):
                if read_record(directory, receipt_name) != completed_record(intent):
                    raise Denied('RECEIPT_MISMATCH')
                if not finalize:
                    return Outcome('RECOVERY_REQUIRED', 'RECEIPT_PENDING', 'DURABILITY_REQUIRES_FINALIZATION')
                # A cached directory entry does not prove that a previous fsync
                # succeeded. Explicit finalization reestablishes durability.
                for name in (destination.name, receipt_name):
                    fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_NOATIME,
                                 dir_fd=directory)
                    try:
                        require_single_regular(os.fstat(fd))
                        os.fsync(fd)
                    finally:
                        close_fd(fd)
                os.fsync(directory)
                verify_published(directory, intent, destination_expected)
                if read_record(directory, receipt_name) != completed_record(intent):
                    raise Denied('RECEIPT_CHANGED')
                return Outcome('COMPLETED', 'OPERATION_COMPLETED', 'POSTCONDITIONS_VERIFIED')
            if not finalize:
                return Outcome('RECOVERY_REQUIRED', 'RECEIPT_PENDING', 'PRIMARY_STATE_COMMITTED')
            os.fsync(directory)
            check_directory_path(destination.parent, directory)
            record(directory, receipt_name, completed_record(intent))
            verify_published(directory, intent, destination_expected)
            return Outcome('COMPLETED', 'OPERATION_COMPLETED', 'POSTCONDITIONS_VERIFIED')
    except (Exception, KeyboardInterrupt):
        # Recovery never claims rollback or absence of a possibly committed file.
        return Outcome('RECOVERY_REQUIRED', 'OPERATOR_ADJUDICATION', 'RECOVERY_INTEGRITY_OR_CAPABILITY_FAILURE')
