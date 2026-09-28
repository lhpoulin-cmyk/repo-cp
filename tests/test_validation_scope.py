"""Private development trees must never become parent-validator input."""
import os
from pathlib import Path
import runpy
import tempfile
import unittest
from unittest.mock import patch


PUBLIC_FILES = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'tools/validate'))['public_files']


class ValidationScopeTests(unittest.TestCase):
    def test_private_checkout_is_pruned_before_traversal(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            private = root / '.agent-checkouts'
            (private / 'codex' / 'task').mkdir(parents=True)
            (private / 'codex' / 'task' / 'invalid.json').write_text('{')
            public = root / 'docs' / 'public.md'
            public.parent.mkdir()
            public.write_text('Public guidance\n')
            scandir = os.scandir

            def guarded_scandir(path):
                self.assertNotIn('.agent-checkouts', Path(path).parts)
                return scandir(path)

            with patch('os.scandir', side_effect=guarded_scandir):
                self.assertEqual(list(PUBLIC_FILES(root)), [public])

    def test_normal_source_and_metadata_remain_selected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            names = ['.gitignore', 'AGENTS.md', 'src/example.py', 'pins/example.json']
            for name in names:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('synthetic\n')
            self.assertEqual({p.relative_to(root).as_posix() for p in PUBLIC_FILES(root)}, set(names))


if __name__ == '__main__':
    unittest.main()
