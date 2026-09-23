"""Entry-point stderr end to end; independent of new modules so baseline behavior is observable."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EntryPointTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.copy = Path(temp.name) / 'repo-cp'

        def ignore(folder, names):
            # Omit repo-cp test modules so a baseline validator cannot recurse.
            if Path(folder) == ROOT / 'tests':
                return [n for n in names if n.endswith('.py')]
            return [n for n in names if n in ('.git', '__pycache__')]

        shutil.copytree(ROOT, self.copy, ignore=ignore)

    def run_tool(self, name, *args, payload=b''):
        return subprocess.run([sys.executable, '-B', str(self.copy / 'tools' / name), *args],
                              input=payload, capture_output=True, check=False, cwd=self.copy)

    def append(self, relative):
        path = self.copy / relative
        path.write_bytes(path.read_bytes() + b'\nUnreviewed addition.\n')

    def assert_blocked(self, result, stderr):
        self.assertEqual((result.returncode, result.stdout, result.stderr), (2, b'', stderr))

    def test_cli_reports_public_foundation_reason(self):
        self.append('vendor/foundation/VERSION')
        for command in ('validate', 'inventory', 'audit'):
            with self.subTest(command):
                self.assert_blocked(self.run_tool('repo-cp', command),
                                    b'BLOCKER=REPO_CP_NONCONFORMANCE\nREASON=FOUNDATION_ARTIFACT_MISMATCH\n')

    def test_validate_reports_public_contract_reason(self):
        self.append('docs/AGENT_WORK_CONTRACT.md')
        self.assert_blocked(self.run_tool('validate'),
                            b'BLOCKER=REPOSITORY_VALIDATION_FAILED\nREASON=AGENT_CONTRACT_MISMATCH\n')

    def test_audit_hardlinks_reports_public_registry_reason(self):
        path = self.copy / 'registries/file-integrity.json'
        data = json.loads(path.read_bytes())
        data['schema_version'] = 2
        path.write_text(json.dumps(data))
        self.assert_blocked(self.run_tool('audit-hardlinks'),
                            b'BLOCKER=FILE_INTEGRITY_AUDIT_UNAVAILABLE\nREASON=FILE_INTEGRITY_NONCONFORMANCE\n')

    def test_internal_codes_keep_exact_generic_stderr(self):
        generic = b'BLOCKER=REPO_CP_NONCONFORMANCE\n'
        for label, args, payload in [('duplicate field', ('render',), b'{"x":1,"x":2}'),
                                     ('invalid json', ('render',), b'{'),
                                     ('secret indicator', ('render',), b'{"a": "tok' + b'en=' + b'SYNTHETIC' * 3 + b'"}'),
                                     ('argument error', ('not-a-command',), b'')]:
            with self.subTest(label):
                self.assert_blocked(self.run_tool('repo-cp', *args, payload=payload), generic)
        self.assert_blocked(self.run_tool('audit-hardlinks', 'extra'),
                            b'BLOCKER=FILE_INTEGRITY_AUDIT_UNAVAILABLE\n')


if __name__ == '__main__':
    unittest.main()
