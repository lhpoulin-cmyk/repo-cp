"""Local creation and failure boundaries; synthetic roots only, no network."""
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from repocp import cli, create
from repocp.safety import Denied
from repocp.scaffold import CONTRACT_COMMIT, scaffold


class CreateTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.parent = Path(temp.name)
        self.target = self.parent / 'example-cp'

    def make(self, **kwargs):
        return create.create_repository(str(self.target), purpose='Synthetic test repository', **kwargs)

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.target), *args], capture_output=True, text=True)

    def test_creates_real_git_repository_and_both_instructions(self):
        result = self.make()
        self.assertEqual(result['status'], 'CREATED')
        self.assertEqual(self.git('symbolic-ref', 'HEAD').stdout.strip(), 'refs/heads/main')
        self.assertEqual(self.git('remote').stdout, '')
        self.assertNotEqual(self.git('rev-parse', '--verify', 'HEAD').returncode, 0)
        self.assertFalse((self.target / '.git/hooks').exists())
        for name in ('AGENTS.md', 'OPENAI_PROJECT_INSTRUCTIONS.md'):
            body = (self.target / name).read_text()
            self.assertIn(CONTRACT_COMMIT, body)
            self.assertIn('Synthetic test repository', body)
            self.assertIn('HELIX_AGENT_EXECUTION_DOCTRINE_V1', body)
            self.assertNotIn('1.1.0-rc', body)
            self.assertLess(len(body.encode()), 8000)
        for path in self.target.iterdir():
            if path.is_file():
                self.assertEqual(path.stat().st_nlink, 1)
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(create.inspect_repository(str(self.target))['content'], 'VERIFIED')
        self.assertEqual(list(self.parent.iterdir()), [self.target])

    def test_dry_run_is_deterministic_and_writes_nothing(self):
        first = self.make(dry_run=True)
        self.assertEqual(first, self.make(dry_run=True))
        self.assertEqual(first['contents'], {k: v.decode() for k, v in scaffold(
            'example-cp', 'Synthetic test repository', 'Louis').items()})
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_existing_targets_never_changed_including_empty_and_symlink(self):
        other = self.parent / 'other'
        other.mkdir()
        for kind in ('empty', 'file', 'symlink', 'dangling'):
            with self.subTest(kind=kind):
                if kind == 'empty':
                    self.target.mkdir()
                elif kind == 'file':
                    self.target.write_text('preserve me')
                else:
                    self.target.symlink_to(other if kind == 'symlink' else self.parent / 'absent')
                with self.assertRaisesRegex(Denied, 'CREATE_DESTINATION_EXISTS'):
                    self.make()
                if kind == 'empty':
                    self.assertEqual(list(self.target.iterdir()), [])
                    self.target.rmdir()
                else:
                    if kind == 'file':
                        self.assertEqual(self.target.read_text(), 'preserve me')
                    self.target.unlink()
                self.assertEqual(list(other.iterdir()), [])

    def test_bad_input_rejected_before_writes(self):
        for destination in ('relative', str(self.parent) + '/../escape', str(self.parent / '.git'),
                            str(self.parent / '-option'), str(self.parent) + '//bad'):
            with self.subTest(destination=destination), self.assertRaises(Denied):
                create.create_repository(destination, purpose='test')
        for text in ('', ' ', 'multiline\ntext', 'x' * 401, 'tok' + 'en=' + 'SYNTHETIC' * 3):
            with self.subTest(text=text[:10]), self.assertRaises(Denied):
                create.create_repository(str(self.target), purpose=text)
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_symlinked_parent_and_world_writable_parent_refused(self):
        real = self.parent / 'real'
        real.mkdir()
        link = self.parent / 'linked'
        link.symlink_to(real)
        with self.assertRaises((Denied, OSError)):
            create.create_repository(str(link / 'example'), purpose='test')
        real.chmod(0o777)
        with self.assertRaisesRegex(Denied, 'DESTINATION_DIRECTORY_POLICY'):
            create.create_repository(str(real / 'example'), purpose='test')
        self.assertEqual(list(real.iterdir()), [])

    def test_privilege_refused_before_contract_or_io(self):
        with patch.object(os, 'geteuid', return_value=0), patch.object(create, 'verify_agent_contract') as verify:
            with self.assertRaisesRegex(Denied, 'UNPRIVILEGED_REFERENCE_ONLY'):
                self.make()
            verify.assert_not_called()
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_contract_tamper_refused_before_creation(self):
        copied = self.parent / 'source'
        shutil.copytree(ROOT, copied, ignore=shutil.ignore_patterns('.git'))
        (copied / 'docs/AGENT_WORK_CONTRACT.md').write_text('tampered')
        with self.assertRaisesRegex(Denied, 'AGENT_CONTRACT_MISMATCH'):
            self.make(source=copied)
        self.assertFalse(self.target.exists())
        self.assertEqual(list(self.parent.iterdir()), [copied])

    def test_ambient_git_environment_and_templates_are_not_used(self):
        alien = self.parent / 'alien'
        alien.mkdir()
        config = self.parent / 'bad-config'
        config.write_text('this is invalid Git configuration')
        template = self.parent / 'template'
        (template / 'hooks').mkdir(parents=True)
        (template / 'hooks/post-checkout').write_text('must never be copied')
        with patch.dict(os.environ, {'GIT_DIR': str(alien), 'GIT_WORK_TREE': str(alien),
                                     'GIT_CONFIG_GLOBAL': str(config), 'GIT_TEMPLATE_DIR': str(template),
                                     'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'init.defaultBranch',
                                     'GIT_CONFIG_VALUE_0': 'wrong'}):
            self.make()
        self.assertEqual(list(alien.iterdir()), [])
        self.assertFalse((self.target / '.git/hooks').exists())
        self.assertEqual(self.git('symbolic-ref', 'HEAD').stdout.strip(), 'refs/heads/main')

    def test_failed_git_preserves_staging_and_inspection_reports_incomplete(self):
        with patch.object(create, 'git_init', side_effect=OSError('SENSITIVE_MARKER')):
            with self.assertRaisesRegex(Denied, '^CREATE_PREPARATION_FAILED$'):
                self.make()
        self.assertFalse(self.target.exists())
        stage, = self.parent.iterdir()
        self.assertEqual(create.inspect_repository(str(stage))['content'], 'INCOMPLETE_OR_CHANGED')

    def test_rename_race_preserves_other_creators_directory(self):
        rename = create.rename_exclusive
        def race(parent, source, target):
            self.target.mkdir()
            (self.target / 'keep').write_text('other creator')
            rename(parent, source, target)
        with patch.object(create, 'rename_exclusive', side_effect=race):
            with self.assertRaisesRegex(Denied, '^CREATE_RECOVERY_REQUIRED$'):
                self.make()
        self.assertEqual((self.target / 'keep').read_text(), 'other creator')
        self.assertEqual(len(list(self.parent.iterdir())), 2)

    def test_error_after_successful_rename_never_claims_no_mutation(self):
        rename = create.rename_exclusive
        def uncertain(parent, source, target):
            rename(parent, source, target)
            raise OSError('lost acknowledgement')
        with patch.object(create, 'rename_exclusive', side_effect=uncertain):
            with self.assertRaisesRegex(Denied, '^CREATE_RECOVERY_REQUIRED$'):
                self.make()
        evidence = create.inspect_repository(str(self.target))
        self.assertEqual((evidence['location'], evidence['content'], evidence['status']),
                         ('TARGET', 'VERIFIED', 'RECOVERY_REQUIRED'))
        before = (self.target / 'AGENTS.md').read_bytes()
        with self.assertRaisesRegex(Denied, 'CREATE_DESTINATION_EXISTS'):
            self.make()
        self.assertEqual((self.target / 'AGENTS.md').read_bytes(), before)

    def test_parent_verification_failure_after_publish_requires_recovery(self):
        original = create.locked_directory
        @contextlib.contextmanager
        def fail_on_exit(*args):
            with original(*args) as directory:
                yield directory
                raise OSError('parent changed after publish')
        with patch.object(create, 'locked_directory', fail_on_exit):
            with self.assertRaisesRegex(Denied, '^CREATE_RECOVERY_REQUIRED$'):
                self.make()
        self.assertEqual(create.inspect_repository(str(self.target))['content'], 'VERIFIED')

    def test_parent_lock_conflict_has_no_writes(self):
        import fcntl
        fd = os.open(self.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(Denied, '^CONCURRENCY_CONFLICT$'):
                self.make()
        finally:
            os.close(fd)
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_fsync_failure_is_recoverable_not_success(self):
        with patch.object(create.os, 'fsync', side_effect=OSError('storage error')):
            with self.assertRaisesRegex(Denied, '^CREATE_PREPARATION_FAILED$'):
                self.make()
        self.assertFalse(self.target.exists())
        self.assertEqual(len(list(self.parent.iterdir())), 1)

    def test_interrupt_preserves_staging(self):
        with patch.object(create, 'git_init', side_effect=KeyboardInterrupt):
            with self.assertRaisesRegex(Denied, '^CREATE_INTERRUPTED$'):
                self.make()
        self.assertFalse(self.target.exists())
        self.assertEqual(len(list(self.parent.iterdir())), 1)

    def test_inspection_detects_changed_guidance_without_modifying_it(self):
        self.make()
        path = self.target / 'AGENTS.md'
        path.write_text('changed')
        self.assertEqual(create.inspect_repository(str(self.target))['content'], 'INCOMPLETE_OR_CHANGED')
        self.assertEqual(path.read_text(), 'changed')

    def test_cli_success_and_error_output(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/repo-cp'),
                                 'create', str(self.target), '--purpose', 'CLI example'], capture_output=True)
        self.assertEqual((result.returncode, result.stderr), (0, b''))
        self.assertEqual(json.loads(result.stdout)['status'], 'CREATED')
        for args in ([str(self.target), '--purpose', 'test'],
                     [str(self.parent / 'unused'), '--purpose', 'test', '--pur', 'bad'],
                     [str(self.parent / 'unused')]):
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                self.assertEqual(create.main(args), 2)
            self.assertEqual(stdout.getvalue(), '')
            self.assertTrue(stderr.getvalue().startswith('BLOCKER=REPOSITORY_CREATION_FAILED\n'))

    def test_existing_read_only_command_does_not_import_creation(self):
        code = '''import sys
sys.path.insert(0, sys.argv[1])
from repocp import cli
sys.argv = ['repo-cp', 'validate']
assert cli.main() == 0
assert 'repocp.create' not in sys.modules
assert 'repocp.publication' not in sys.modules
'''
        result = subprocess.run([sys.executable, '-B', '-c', code, str(ROOT / 'src')], capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
