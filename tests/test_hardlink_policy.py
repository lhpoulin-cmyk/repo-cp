"""Synthetic file-integrity qualification; one bounded real hardlink rejection test."""
from dataclasses import asdict, replace
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from jsonschema import Draft202012Validator
from repocp import publication as pub
from repocp.file_integrity import invariant, inspect_link, governed_paths, local_audit
from repocp.safety import Denied, read_public

PAYLOAD = b'Public synthetic artifact\n' * 5
REVISION = '1' * 40


class ChangedStat:
    def __init__(self, source, **changes):
        self.source, self.changes = source, changes
    def __getattr__(self, name):
        return self.changes.get(name, getattr(self.source, name))


class SyntheticRoot(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix='repo-cp-integrity-'))
        self.root_identity = (self.root.stat().st_dev, self.root.stat().st_ino)
        self.addCleanup(self.cleanup_root)
        self.policy = invariant(ROOT)

    def cleanup_root(self):
        actual = self.root.lstat()
        self.assertTrue(stat.S_ISDIR(actual.st_mode))
        self.assertEqual((actual.st_dev, actual.st_ino), self.root_identity)
        shutil.rmtree(self.root)

    def file(self, name, content=PAYLOAD):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path


class HardlinkAuditTests(SyntheticRoot):
    def inspect(self, name, protected=True):
        return inspect_link(self.root, name, protected=protected, policy=self.policy)

    def test_single_link_protected_and_workflow(self):
        self.file('pins/public.json')
        self.file('tests/fixtures/normal.txt')
        self.assertEqual(self.inspect('pins/public.json'), ('PASS', 'SINGLE_LINK_REGULAR'))
        self.assertEqual(self.inspect('tests/fixtures/normal.txt', False), ('PASS', 'SINGLE_LINK_REGULAR'))

    def test_hardlinked_protected_metadata_model(self):
        self.file('pins/public.json')
        original = os.fstat
        with patch('os.fstat', side_effect=lambda fd: ChangedStat(original(fd), st_nlink=2)):
            self.assertEqual(self.inspect('pins/public.json'), ('BLOCKED', 'HARDLINK_FORBIDDEN'))

    def test_hardlinked_normal_fixture_metadata_model(self):
        self.file('tests/fixtures/normal.txt')
        original = os.fstat
        with patch('os.fstat', side_effect=lambda fd: ChangedStat(original(fd), st_nlink=2)):
            self.assertEqual(self.inspect('tests/fixtures/normal.txt', False), ('DRIFT', 'HARDLINK_FORBIDDEN'))

    def test_bounded_real_hardlink_rejection_only(self):
        # The sole link creation in the suite; both names remain inside this root.
        protected = self.file('pins/protected.txt')
        fixture = self.root / 'tests/fixtures/rejected.txt'
        fixture.parent.mkdir(parents=True)
        os.link(protected, fixture)
        original = protected.stat()
        self.assertEqual(original.st_nlink, 2)
        self.assertEqual(self.inspect('pins/protected.txt'), ('BLOCKED', 'HARDLINK_FORBIDDEN'))
        self.assertEqual(self.inspect('tests/fixtures/rejected.txt', False), ('DRIFT', 'HARDLINK_FORBIDDEN'))
        with self.assertRaises(Denied):
            read_public(self.root, 'pins/protected.txt')
        expected = expectation(protected)
        destination = self.root / 'never-published.txt'
        with self.assertRaises(pub.PublicationFailure):
            pub.copy_and_publish(protected, destination, source_expected=expected,
                                 destination_expected=expected, operation='a' * 32, reviewed_revision=REVISION)
        self.assertFalse(destination.exists())
        self.assertEqual(protected.stat().st_ino, original.st_ino)
        self.assertEqual(protected.stat().st_nlink, 2)
        self.assertEqual(fixture.read_bytes(), PAYLOAD)

    def test_symlink_file_never_read_or_called_hardlink(self):
        target = self.file('outside/value.txt')
        self.root.joinpath('link.txt').symlink_to(target)
        with patch('os.read', side_effect=AssertionError('Audit must not read contents')):
            self.assertEqual(self.inspect('link.txt'), ('BLOCKED', 'SYMLINK_REFUSED'))
        self.assertEqual(target.read_bytes(), PAYLOAD)

    def test_symlink_ancestor_and_root_refused(self):
        self.file('actual/value.txt')
        (self.root / 'alias').symlink_to(self.root / 'actual', target_is_directory=True)
        self.assertEqual(self.inspect('alias/value.txt'), ('BLOCKED', 'UNSAFE_PATH'))
        status, reason = inspect_link(self.root / 'alias', 'value.txt', protected=True, policy=self.policy)
        self.assertEqual(status, 'BLOCKED')

    def test_fifo_refused_without_opening_for_read(self):
        os.mkfifo(self.root / 'fifo')
        self.assertEqual(self.inspect('fifo'), ('BLOCKED', 'NONREGULAR_REFUSED'))

    def test_missing_file_unknown(self):
        self.assertEqual(self.inspect('missing'), ('UNKNOWN', 'METADATA_UNAVAILABLE'))

    def test_permission_denied_unknown(self):
        with patch('repocp.file_integrity.open_parent', side_effect=PermissionError()):
            self.assertEqual(self.inspect('missing'), ('UNKNOWN', 'METADATA_UNAVAILABLE'))

    def test_exclusions_pruned_before_stat_or_scandir(self):
        excluded = self.policy['audit']['excluded_components']
        for name in excluded:
            self.file(name + '/not-scanned.txt')
        self.file('governed.txt')
        original = os.stat
        def guarded(name, *args, **kwargs):
            self.assertNotIn(name, excluded)
            return original(name, *args, **kwargs)
        with patch('os.stat', side_effect=guarded):
            self.assertEqual(list(governed_paths(self.root, self.policy)), ['governed.txt'])
        for name in excluded:
            with patch('repocp.file_integrity.open_parent', side_effect=AssertionError('Excluded path opened')):
                self.assertEqual(self.inspect(name + '/not-scanned.txt'), ('NOT_APPLICABLE', 'EXCLUDED_SCOPE'))

    def test_declared_repository_exclusion_pruned(self):
        self.policy['audit']['repository_excluded_paths'] = ['application-state']
        self.file('application-state/never-read')
        self.file('ordinary.txt')
        self.assertEqual(list(governed_paths(self.root, self.policy)), ['ordinary.txt'])

    def test_same_device_mount_pruned(self):
        self.file('mounted/not-scanned')
        self.file('ordinary.txt')
        with patch('repocp.file_integrity.mountpoints', return_value={str(self.root / 'mounted')}):
            self.assertEqual(list(governed_paths(self.root, self.policy)), ['ordinary.txt'])

    def test_different_device_mount_pruned(self):
        self.file('foreign/not-scanned')
        self.file('ordinary.txt')
        original = os.stat
        def changed(name, *args, **kwargs):
            result = original(name, *args, **kwargs)
            return ChangedStat(result, st_dev=result.st_dev + 1) if name == 'foreign' else result
        with patch('os.stat', side_effect=changed):
            self.assertEqual(list(governed_paths(self.root, self.policy)), ['ordinary.txt'])

    def test_explicit_peer_path_mount_excluded_before_open(self):
        self.file('mounted/public.txt')
        with patch('repocp.file_integrity.mountpoints', return_value={str(self.root / 'mounted')}), \
                patch('repocp.file_integrity.open_parent', side_effect=AssertionError('Mounted file opened')):
            self.assertEqual(self.inspect('mounted/public.txt'), ('NOT_APPLICABLE', 'EXCLUDED_MOUNT'))

    def test_symlink_directory_not_traversed(self):
        other = self.root / 'other'
        other.mkdir()
        (self.root / 'alias').symlink_to(other, target_is_directory=True)
        self.assertEqual(list(governed_paths(self.root, self.policy)), ['alias'])
        self.assertEqual(local_audit(self.root, self.policy)['status'], 'BLOCKED')

    def test_deterministic_classification_and_no_mutation(self):
        self.file('normal.txt')
        before = self.root.joinpath('normal.txt').stat()
        first = local_audit(self.root, self.policy)
        self.assertEqual(first, local_audit(self.root, self.policy))
        self.assertEqual(first['status'], 'PASS')
        self.assertFalse(first['automatic_execution'])
        self.assertEqual(self.root.joinpath('normal.txt').stat().st_atime_ns, before.st_atime_ns)
        self.assertEqual(first['live_mutation'], 'NONE')

    def test_unknown_incomplete_scan_not_pass(self):
        with patch('repocp.file_integrity.mountpoints', side_effect=OSError()):
            self.assertEqual(local_audit(self.root, self.policy)['status'], 'UNKNOWN')

    def test_schema_rejects_weakening_and_unknown_fields(self):
        schema = json.loads((ROOT / 'schemas/file-integrity-v1.schema.json').read_text())
        validator = Draft202012Validator(schema)
        self.assertTrue(validator.is_valid(self.policy))
        for key, value in [('protected_regular_file_nlink', 2), ('automatic_execution', True),
                           ('invariant_id', 'OTHER'), ('schema_version', 2), ('unexpected', True)]:
            data = dict(self.policy, **{key: value})
            self.assertFalse(validator.is_valid(data))

    def test_nonobject_and_boolean_version_rejected(self):
        shutil.copytree(ROOT / 'registries', self.root / 'registries')
        shutil.copytree(ROOT / 'schemas', self.root / 'schemas')
        for data in ([], None, dict(self.policy, schema_version=True)):
            (self.root / 'registries/file-integrity.json').write_text(json.dumps(data))
            with self.assertRaises(Denied):
                invariant(self.root)

    def test_reader_preserves_atime(self):
        path = self.file('public.txt')
        os.utime(path, ns=(1_000_000_000, 2_000_000_000))
        before = path.stat()
        self.assertEqual(read_public(self.root, 'public.txt'), PAYLOAD)
        self.assertEqual(path.stat().st_atime_ns, before.st_atime_ns)

    def test_existing_audit_rc011_and_rejection_no_content_read(self):
        # Reuse the established public enrollment fixture, never a live peer.
        from test_consumer import AuditTests
        from repocp import audit as audit_module
        fixture = AuditTests('test_pilot_success_and_no_change_second_audit')
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        first = fixture.run_audit()
        checks = [r for r in first['results'] if r['check_id'] == 'RC011']
        self.assertEqual(len(checks), len(fixture.entry['files']))
        self.assertTrue(all(r['status'] == 'PASS' for r in checks))
        inspect = audit_module.inspect_link
        reader = audit_module.read_public
        def rejected(root, relative, **kwargs):
            if root == fixture.peer and relative == 'README.md':
                return 'BLOCKED', 'HARDLINK_FORBIDDEN'
            return inspect(root, relative, **kwargs)
        def guarded(root, relative, *args, **kwargs):
            self.assertFalse(root == fixture.peer and relative == 'README.md')
            return reader(root, relative, *args, **kwargs)
        with patch('repocp.audit.inspect_link', side_effect=rejected), \
                patch('repocp.audit.read_public', side_effect=guarded):
            report = fixture.run_audit()
        self.assertEqual(report['status'], 'BLOCKED')
        proposal = audit_module.proposals(report)
        self.assertIsNone(proposal['patch'])
        self.assertFalse(proposal['automatic_execution'])


def expectation(path):
    info = path.stat()
    return pub.Expectation(info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode), info.st_dev,
                           info.st_size, hashlib.sha256(PAYLOAD).hexdigest())


class PublicationTests(SyntheticRoot):
    def setUp(self):
        super().setUp()
        self.source = self.file('source/public.txt')
        self.destination_dir = self.root / 'destination'
        self.destination_dir.mkdir(mode=0o700)
        self.destination = self.destination_dir / 'published.txt'
        self.source_expected = expectation(self.source)
        self.target_expected = replace(self.source_expected, mode=0o640)
        self.operation = 'a' * 32

    def publish(self):
        return pub.copy_and_publish(self.source, self.destination, source_expected=self.source_expected,
                                    destination_expected=self.target_expected, operation=self.operation,
                                    reviewed_revision=REVISION)

    def resolve(self, finalize=False):
        return pub.resolve_publication(self.destination, destination_expected=self.target_expected,
                                       operation=self.operation, reviewed_revision=REVISION, finalize=finalize)

    def test_verified_copy_publication_and_idempotent_finalization(self):
        outcome = self.publish()
        self.assertEqual(outcome.status, 'COMPLETED')
        self.assertEqual(self.destination.read_bytes(), PAYLOAD)
        info = self.destination.stat()
        self.assertEqual(info.st_nlink, 1)
        self.assertNotEqual(info.st_ino, self.source.stat().st_ino)
        self.assertEqual(stat.S_IMODE(info.st_mode), 0o640)
        self.assertEqual(self.resolve().cause, 'DURABILITY_REQUIRES_FINALIZATION')
        self.assertEqual(outcome, self.resolve(True))
        schema = json.loads((ROOT / 'schemas/file-integrity-v1.schema.json').read_text())['$defs']['publicationOutcome']
        self.assertTrue(Draft202012Validator(schema).is_valid(asdict(outcome)))
        receipt = json.loads(next(self.destination_dir.glob('*.receipt.json')).read_text())
        self.assertEqual(receipt['reviewed_revision'], REVISION)
        self.assertEqual(receipt['tool_version'], pub.TOOL_VERSION)
        self.assertIn('intent_sha256', receipt)

    def test_existing_destination_preserved(self):
        self.destination.write_bytes(b'Existing valid public state')
        before = self.destination.stat()
        with self.assertRaises(pub.PublicationFailure) as caught:
            self.publish()
        self.assertEqual(caught.exception.outcome.cause, 'EXISTING_STATE_REQUIRES_RESOLUTION')
        self.assertEqual(self.destination.read_bytes(), b'Existing valid public state')
        self.assertEqual(self.destination.stat().st_ino, before.st_ino)

    def test_existing_symlink_destination_preserved(self):
        self.destination.symlink_to(self.source)
        with self.assertRaises(pub.PublicationFailure):
            self.publish()
        self.assertTrue(self.destination.is_symlink())
        self.assertEqual(self.source.read_bytes(), PAYLOAD)

    def test_rejects_relative_traversal_and_ambiguous_paths(self):
        for value in ('', 'relative', '/a/../b', '/a/./b', '//a/b', '/a//b', '/a/b\n'):
            with self.subTest(path=value), self.assertRaises(Denied):
                pub.absolute_file(value)

    def test_source_symlink_rejected(self):
        alias = self.source.parent / 'alias'
        alias.symlink_to(self.source)
        self.source = alias
        with self.assertRaises(pub.PublicationFailure):
            self.publish()
        self.assertFalse(self.destination.exists())

    def test_owner_group_mode_device_size_hash_expectations_enforced(self):
        original = self.source_expected
        for key, value in [('uid', original.uid + 1), ('gid', original.gid + 1), ('mode', 0o777),
                           ('device', original.device + 1), ('size', original.size + 1), ('sha256', '0' * 64)]:
            with self.subTest(field=key):
                self.source_expected = replace(original, **{key: value})
                with self.assertRaises(pub.PublicationFailure):
                    self.publish()
                self.assertFalse(self.destination.exists())
        self.source_expected = original

    def test_root_execution_rejected_before_io(self):
        with patch('os.geteuid', return_value=0), patch('repocp.publication.open_directory', side_effect=AssertionError('Unexpected IO')):
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
        self.assertEqual(caught.exception.outcome.status, 'FAILED')

    def test_partial_writes_are_completed(self):
        original = os.write
        with patch('os.write', side_effect=lambda fd, data: original(fd, data[:3])):
            self.assertEqual(self.publish().status, 'COMPLETED')
        self.assertEqual(self.destination.read_bytes(), PAYLOAD)

    def test_corrupt_copy_hash_rejected_before_publication(self):
        def corrupt(source, target, size):
            pub.write_all(target, b'X' * size)
        with patch('repocp.publication.copy_bytes', side_effect=corrupt):
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
        self.assertEqual(caught.exception.outcome.status, 'FAILED')
        self.assertFalse(self.destination.exists())
        self.assertEqual(self.source.read_bytes(), PAYLOAD)

    def test_fsync_faults_at_each_durability_boundary(self):
        # intent file/dir, copied file, primary dir, receipt file/dir.
        for boundary in range(1, 7):
            with self.subTest(boundary=boundary):
                self.operation = format(boundary, '032x')
                self.destination = self.destination_dir / ('artifact-' + str(boundary))
                original = os.fsync
                calls = 0
                def fail(fd):
                    nonlocal calls
                    calls += 1
                    if calls == boundary:
                        raise OSError(errno.ENOSPC, 'SYNTHETIC_IO_FAILURE')
                    return original(fd)
                with patch('os.fsync', side_effect=fail):
                    with self.assertRaises(pub.PublicationFailure) as caught:
                        self.publish()
                expected = 'FAILED' if boundary <= 3 else 'RECOVERY_REQUIRED'
                self.assertEqual(caught.exception.outcome.status, expected)
                self.assertEqual(self.destination.exists(), boundary >= 4)
                self.assertEqual(self.source.read_bytes(), PAYLOAD)
                if boundary >= 4:
                    self.assertEqual(self.resolve(True).status, 'COMPLETED')

    def test_intent_write_failure_preserves_source(self):
        with patch('os.write', side_effect=OSError(errno.ENOSPC, 'SYNTHETIC_FULL_FILESYSTEM')):
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
        self.assertEqual(caught.exception.outcome.status, 'FAILED')
        self.assertFalse(self.destination.exists())
        self.assertEqual(self.source.read_bytes(), PAYLOAD)

    def test_copy_permission_denial_preserves_state(self):
        with patch('repocp.publication.copy_bytes', side_effect=PermissionError()):
            with self.assertRaises(pub.PublicationFailure):
                self.publish()
        self.assertFalse(self.destination.exists())
        self.assertEqual(self.resolve().cause, 'PRIMARY_STATE_UNCHANGED')

    def test_atomic_rename_failure_is_recovery_required(self):
        original = pub.rename_exclusive
        def fail(directory, source, target):
            if target == self.destination.name:
                raise OSError(errno.EXDEV, 'SYNTHETIC_RENAME_FAILURE')
            return original(directory, source, target)
        with patch('repocp.publication.rename_exclusive', side_effect=fail):
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
        self.assertEqual(caught.exception.outcome.status, 'RECOVERY_REQUIRED')
        self.assertEqual(self.resolve().cause, 'PRIMARY_STATE_UNCHANGED')

    def test_rename_committed_then_error_resolves_committed_side(self):
        original = pub.rename_exclusive
        def ambiguous(directory, source, target):
            original(directory, source, target)
            if target == self.destination.name:
                raise OSError(errno.EIO, 'SYNTHETIC_POST_COMMIT_FAILURE')
        with patch('repocp.publication.rename_exclusive', side_effect=ambiguous):
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
        self.assertEqual(caught.exception.outcome.status, 'RECOVERY_REQUIRED')
        self.assertEqual(self.resolve().cause, 'PRIMARY_STATE_COMMITTED')
        self.assertEqual(self.resolve(True).status, 'COMPLETED')
        self.assertEqual(self.resolve(True).status, 'COMPLETED')

    def test_receipt_failure_preserves_published_primary(self):
        original = pub.record
        def fail(directory, name, data):
            if name.endswith('.receipt.json'):
                raise OSError(errno.EIO, 'SYNTHETIC_RECEIPT_FAILURE')
            return original(directory, name, data)
        with patch('repocp.publication.record', side_effect=fail):
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
        self.assertEqual(caught.exception.outcome.phase, 'RECEIPT_PENDING')
        self.assertEqual(self.resolve().phase, 'RECEIPT_PENDING')
        self.assertEqual(self.resolve(True).status, 'COMPLETED')

    def test_concurrent_writer_fails_without_mutation(self):
        directory = os.open(self.destination_dir, os.O_RDONLY | os.O_DIRECTORY)
        try:
            fcntl.flock(directory, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
            self.assertEqual(caught.exception.outcome.cause, 'CONCURRENCY_CONFLICT')
            self.assertEqual(list(self.destination_dir.iterdir()), [])
        finally:
            os.close(directory)

    def test_existing_receipt_finalization_repeats_fsync(self):
        self.publish()
        with patch('os.fsync', wraps=os.fsync) as sync:
            self.assertEqual(self.resolve(True).status, 'COMPLETED')
        self.assertEqual(sync.call_count, 3)

    def test_readonly_resolution_writes_no_records_or_atime(self):
        self.publish()
        before = {p.name: (p.stat().st_atime_ns, p.stat().st_mtime_ns) for p in self.destination_dir.iterdir()}
        with patch('os.write', side_effect=AssertionError('Read-only resolver wrote data')), \
                patch('os.fsync', side_effect=AssertionError('Read-only resolver changed durability')):
            self.assertEqual(self.resolve().status, 'RECOVERY_REQUIRED')
        after = {p.name: (p.stat().st_atime_ns, p.stat().st_mtime_ns) for p in self.destination_dir.iterdir()}
        self.assertEqual(before, after)

    def test_interruption_records_categorical_outcome(self):
        with patch('repocp.publication.copy_bytes', side_effect=pub.Interrupted('CANCELLED')):
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
        self.assertEqual(caught.exception.outcome.status, 'INTERRUPTED')
        data = json.loads(next(self.destination_dir.glob('*.outcome.json')).read_text())
        self.assertEqual(data['cause'], 'CANCELLED')
        self.assertEqual(data['reviewed_revision'], REVISION)
        self.assertIn('intent_sha256', data)
        self.assertNotIn(PAYLOAD.decode(), json.dumps(data))

    def test_stale_kernel_lock_released_after_process_exit(self):
        script = 'import os,fcntl,sys; fd=os.open(sys.argv[1],os.O_RDONLY|os.O_DIRECTORY); fcntl.flock(fd,fcntl.LOCK_EX); os._exit(0)'
        result = subprocess.run([sys.executable, '-B', '-c', script, str(self.destination_dir)],
                                capture_output=True, timeout=10, check=False)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.publish().status, 'COMPLETED')

    def test_destination_directory_substitution_never_completed(self):
        original = pub.copy_bytes
        def substitute(source, target, size):
            original(source, target, size)
            self.destination_dir.rename(self.root / 'displaced')
            self.destination_dir.mkdir(mode=0o700)
        with patch('repocp.publication.copy_bytes', side_effect=substitute):
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
        self.assertNotEqual(caught.exception.outcome.status, 'COMPLETED')
        self.assertFalse(self.destination.exists())

    def test_source_path_substitution_rejected(self):
        original = pub.copy_bytes
        def substitute(source, target, size):
            original(source, target, size)
            self.source.rename(self.source.parent / 'original')
            self.source.write_bytes(PAYLOAD)
        with patch('repocp.publication.copy_bytes', side_effect=substitute):
            with self.assertRaises(pub.PublicationFailure):
                self.publish()
        self.assertFalse(self.destination.exists())

    def test_source_metadata_drift_rejected(self):
        original = pub.copy_bytes
        def drift(source, target, size):
            original(source, target, size)
            self.source.chmod(0o600)
        with patch('repocp.publication.copy_bytes', side_effect=drift):
            with self.assertRaises(pub.PublicationFailure):
                self.publish()
        self.assertFalse(self.destination.exists())

    def test_recovery_rejects_changed_primary(self):
        self.publish()
        self.destination.write_bytes(b'Changed public artifact')
        before = self.destination.read_bytes()
        self.assertEqual(self.resolve(True).phase, 'OPERATOR_ADJUDICATION')
        self.assertEqual(self.destination.read_bytes(), before)

    def test_recovery_missing_intent_is_not_success(self):
        self.assertEqual(self.resolve().cause, 'INTENT_UNAVAILABLE')

    def test_no_replace_racing_writer_preserved(self):
        original = pub.rename_exclusive
        def race(directory, source, target):
            if target == self.destination.name:
                self.destination.write_bytes(b'Concurrent public state')
            return original(directory, source, target)
        with patch('repocp.publication.rename_exclusive', side_effect=race):
            with self.assertRaises(pub.PublicationFailure):
                self.publish()
        self.assertEqual(self.destination.read_bytes(), b'Concurrent public state')
        self.assertEqual(self.resolve().phase, 'OPERATOR_ADJUDICATION')

    def test_atomic_primitive_unavailable_has_no_link_fallback(self):
        with patch('repocp.publication.ctypes.CDLL', return_value=object()):
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
        self.assertEqual(caught.exception.outcome.status, 'FAILED')
        self.assertFalse(self.destination.exists())

    def test_cleanup_failure_preserves_original_cause(self):
        with patch('repocp.publication.copy_bytes', side_effect=pub.Interrupted('CANCELLED')), \
                patch('repocp.publication.remove_own_temp', side_effect=PermissionError()):
            with self.assertRaises(pub.PublicationFailure) as caught:
                self.publish()
        self.assertEqual(caught.exception.outcome.cause, 'CANCELLED')
        self.assertFalse(self.destination.exists())
        self.assertTrue(any(self.destination_dir.glob('*.tmp')))

    def test_real_cross_filesystem_copy(self):
        # Both roots are synthetic and inside allowed writable locations.
        other = Path(tempfile.mkdtemp(prefix='.hardlink-test-', dir=ROOT))
        info = other.lstat()
        try:
            if info.st_dev == self.root.stat().st_dev:
                self.skipTest('NOT_RUN: QUALIFICATION_ENVIRONMENT lacks two writable filesystems')
            self.destination_dir = other
            self.destination = other / 'published.txt'
            self.target_expected = replace(self.target_expected, device=info.st_dev)
            self.assertEqual(self.publish().status, 'COMPLETED')
            self.assertEqual(self.destination.stat().st_dev, info.st_dev)
            self.assertEqual(self.destination.read_bytes(), PAYLOAD)
        finally:
            current = other.lstat()
            self.assertEqual((current.st_dev, current.st_ino), (info.st_dev, info.st_ino))
            shutil.rmtree(other)

    def test_sigint_sighup_sigterm_controlled_in_subprocess(self):
        script = '''import hashlib,os,signal,stat,sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from repocp import publication as p
source=Path(sys.argv[2]); destination=Path(sys.argv[3]); info=source.stat()
e=p.Expectation(info.st_uid,info.st_gid,stat.S_IMODE(info.st_mode),info.st_dev,info.st_size,hashlib.sha256(source.read_bytes()).hexdigest())
p.copy_bytes=lambda *args: os.kill(os.getpid(), int(sys.argv[4]))
try:
 p.copy_and_publish(source,destination,source_expected=e,destination_expected=e,operation='b'*32,reviewed_revision='1'*40)
except p.PublicationFailure as failure:
 print(failure.outcome.status)
'''
        for number in (signal.SIGINT, signal.SIGHUP, signal.SIGTERM):
            directory = self.destination_dir / str(number)
            directory.mkdir(mode=0o700)
            result = subprocess.run([sys.executable, '-B', '-c', script, str(ROOT / 'src'),
                                     str(self.source), str(directory / 'published'), str(number)],
                                    capture_output=True, timeout=10, check=False)
            self.assertEqual((result.returncode, result.stdout), (0, b'INTERRUPTED\n'))
            self.assertFalse((directory / 'published').exists())


if __name__ == '__main__':
    unittest.main()
