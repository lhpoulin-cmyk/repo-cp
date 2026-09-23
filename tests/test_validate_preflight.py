"""tools/validate privilege preflight, exercised with simulated IDs; needs no privilege."""
import contextlib
import io
import itertools
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / 'tools/validate'
REJECTION = (b'BLOCKER=REPOSITORY_VALIDATION_FAILED\n'
             b'REASON=UNPRIVILEGED_ENVIRONMENT_REQUIRED\n'
             b'Run tools/validate as an ordinary user without root, set-user-ID '
             b'or set-group-ID; the suite does not run privileged.\n')

# Fresh interpreter: simulate IDs, then record every open, process creation and
# newly imported module while tools/validate runs as __main__. Repository and
# third-party imports are recorded and refused, so a validator that got past its
# preflight stops there instead of running the suite recursively.
PROBE = '''import json, os, runpy, sys
script, ids, report = sys.argv[1], json.loads(sys.argv[2]), sys.argv[3]
os.getuid, os.geteuid = (lambda: ids['uid']), (lambda: ids['euid'])
os.getgid, os.getegid = (lambda: ids['gid']), (lambda: ids['egid'])
events = {'opened': [], 'spawned': [], 'refused_imports': []}
class Refuse:
    def find_spec(self, name, path=None, target=None):
        if name.split('.')[0] in ('repocp', 'jsonschema', 'yaml'):
            events['refused_imports'].append(name)
            raise ImportError('PREFLIGHT_PROBE_REFUSED')
        return None
sys.meta_path.insert(0, Refuse())
# Warm runpy's own lazy imports on an empty script so only the validator's
# activity is recorded below.
empty = os.path.join(os.path.dirname(report), 'empty.py')
open(empty, 'w').close()
runpy.run_path(empty, run_name='warm_up')
before = set(sys.modules)
def hook(event, args):
    if event == 'open':
        events['opened'].append(str(args[0]))
    elif event in ('subprocess.Popen', 'os.posix_spawn', 'os.exec', 'os.system', 'os.fork', 'os.spawn'):
        events['spawned'].append(event)
sys.addaudithook(hook)
sys.argv = [script]
try:
    runpy.run_path(script, run_name='__main__')
    code = None
except SystemExit as stop:
    code = stop.code
except ImportError:
    code = 'REFUSED_IMPORT'
events['code'] = code
events['new_modules'] = sorted(set(sys.modules) - before)
data = json.dumps(events)
with open(report, 'w') as stream:
    stream.write(data)
'''
IDS = ('uid', 'euid', 'gid', 'egid')
USER = dict(uid=1000, euid=1000, gid=1000, egid=1000)
PRIVILEGED = {
    'root': dict(uid=0, euid=0, gid=0, egid=0),
    'effective root': dict(USER, euid=0),
    'set-user-ID': dict(USER, euid=1001),
    'real root, dropped effective': dict(USER, uid=0),
    'set-group-ID': dict(USER, egid=1001),
}
# Group 0 without set-ID is accepted by the publication reference policy too;
# the parity test covers it. Changing that is a policy decision, not this fix.


def probe(ids):
    with tempfile.TemporaryDirectory() as directory:
        report = Path(directory) / 'report.json'
        result = subprocess.run([sys.executable, '-B', '-c', PROBE, str(VALIDATE), json.dumps(ids), str(report)],
                                capture_output=True, check=False)
        return result, json.loads(report.read_text())


class PreflightTests(unittest.TestCase):
    def test_privileged_ids_rejected_before_any_validation_work(self):
        for label, ids in PRIVILEGED.items():
            with self.subTest(label):
                result, events = probe(ids)
                self.assertEqual(events['code'], 2)
                self.assertEqual((result.returncode, result.stdout, result.stderr), (0, b'', REJECTION))
                # No repository/third-party import attempt, process creation or
                # file open beyond the script itself; no stdlib validation modules.
                self.assertEqual(events['refused_imports'], [])
                self.assertEqual(events['spawned'], [])
                self.assertEqual(set(events['opened']), {str(VALIDATE)})
                self.assertFalse({'ast', 'subprocess', 'pathlib'} & set(events['new_modules']))

    def test_ordinary_ids_pass_preflight_positive_control(self):
        result, events = probe(USER)
        # The probe itself works: past preflight, the validator opens more files
        # and attempts the repository imports the probe refuses.
        self.assertEqual(events['code'], 'REFUSED_IMPORT')
        self.assertEqual(events['refused_imports'][:1], ['repocp'])
        self.assertIn('subprocess', events['new_modules'])
        self.assertNotIn(b'UNPRIVILEGED_ENVIRONMENT_REQUIRED', result.stderr)

    def test_preflight_matches_publication_reference_policy(self):
        sys.path.insert(0, str(ROOT / 'src'))
        from repocp import publication
        from repocp.safety import Denied

        for values in itertools.product((0, 1000, 1001), repeat=4):
            ids = dict(zip(IDS, values))
            with self.subTest(**ids):
                with contextlib.ExitStack() as stack:
                    for name in IDS:
                        stack.enter_context(patch.object(os, 'get' + name, lambda v=ids[name]: v))
                    try:
                        publication.require_unprivileged()
                        refused = False
                    except Denied:
                        refused = True
                    stderr = io.StringIO()
                    # Not __main__: module-level preflight runs, main() does not.
                    with patch.object(sys, 'path', list(sys.path)), contextlib.redirect_stderr(stderr):
                        try:
                            runpy.run_path(str(VALIDATE), run_name='preflight_parity')
                            rejected = False
                        except SystemExit as stop:
                            self.assertEqual(stop.code, 2)
                            rejected = True
                self.assertEqual(rejected, refused)
                self.assertEqual(stderr.getvalue().encode(), REJECTION if rejected else b'')


if __name__ == '__main__':
    unittest.main()
