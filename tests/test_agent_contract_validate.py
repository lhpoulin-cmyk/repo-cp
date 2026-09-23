"""tools/validate end to end; independent of new modules so baseline behavior is observable."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ValidateIntegrationTests(unittest.TestCase):
    def test_validate_rejects_tampered_contract_before_any_output(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'repo-cp'

            def ignore(folder, names):
                # Omit repo-cp test modules so a baseline validator cannot recurse.
                if Path(folder) == ROOT / 'tests':
                    return [n for n in names if n.endswith('.py')]
                return [n for n in names if n in ('.git', '__pycache__')]

            shutil.copytree(ROOT, copy, ignore=ignore)
            target = copy / 'docs/AGENT_WORK_CONTRACT.md'
            target.write_bytes(target.read_bytes() + b'\nUnreviewed addition.\n')
            result = subprocess.run([sys.executable, '-B', str(copy / 'tools/validate')],
                                    capture_output=True, check=False, cwd=copy)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b'')
            self.assertTrue(result.stderr.startswith(b'BLOCKER=REPOSITORY_VALIDATION_FAILED\n'))


if __name__ == '__main__':
    unittest.main()
