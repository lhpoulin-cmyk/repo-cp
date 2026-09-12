"""Public synthetic inputs; test runners never execute declared action commands."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from repocp.consumer import SOURCE, render, verify
from repocp.safety import Denied, MAX_BYTES, has_indicator, read_public
from repocp.audit import audit, head, proposals, registry

FIXTURES = ROOT / 'tests/fixtures/auth-cp'


def raw(name='ready'):
    return (FIXTURES / (name + '.json')).read_bytes()


def cli(payload, *args):
    return subprocess.run([sys.executable, '-B', str(ROOT / 'tools/repo-cp'), *args],
                          input=payload, capture_output=True, check=False)


def snapshot(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in Path(root).rglob('*') if p.is_file() and not p.is_symlink()}


class ConsumerTests(unittest.TestCase):
    def test_accepted_artifacts(self):
        self.assertEqual(len(verify()), 19)

    def test_golden_both_statuses(self):
        for name in ('ready', 'blocked'):
            expected = (FIXTURES / (name + '.txt')).read_text()
            self.assertEqual(render(raw(name)), expected)
            result = cli(raw(name), 'render')
            self.assertEqual((result.returncode, result.stdout.decode(), result.stderr), (0, expected, b''))

    def test_reference_golden_compatibility(self):
        for name in ('ready', 'blocked'):
            fixture = ROOT / 'vendor/foundation/tests/fixtures/operator_action'
            action = json.loads((fixture / (name + '.json')).read_bytes())
            action['source'] = SOURCE
            expected = (fixture / (name + '.txt')).read_text().replace('1' * 40, SOURCE['repository_revision']).replace('2' * 40, SOURCE['doctrine_revision'])
            self.assertEqual(render(json.dumps(action).encode()), expected)

    def test_invalid_input_atomic(self):
        action = json.loads(raw()); action['extra'] = 'do-not-echo-marker'
        inputs = [b'{', b'\xff', b'NaN', b'Infinity', b'{"x":1,"x":2}',
                  b'{"nested":{"x":1,"x":2}}', b'[' * 2000, b'9' * 10000,
                  b'x' * (MAX_BYTES + 1), json.dumps(action).encode()]
        for payload in inputs:
            result = cli(payload, 'render')
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b'')
            self.assertEqual(result.stderr, b'BLOCKER=REPO_CP_NONCONFORMANCE\n')

    def test_pins_independent(self):
        for key in SOURCE:
            for value in ('main', '0' * 40, None):
                action = json.loads(raw()); action['source'][key] = value
                with self.assertRaises(Denied): render(json.dumps(action).encode())
        action = json.loads(raw()); del action['source']
        with self.assertRaises(Denied): render(json.dumps(action).encode())

    def test_all_missing_fields(self):
        for key in json.loads(raw()):
            action = json.loads(raw()); del action[key]
            with self.assertRaises(Denied): render(json.dumps(action).encode())

    def test_controls_and_size(self):
        for value in ('\n', '\r', '\t', '\x1b[2J', '\u202e', '\x00', 'x' * 4097):
            for location in ('repository', 'command', 'evidence'):
                action = json.loads(raw())
                if location == 'command': action[location]['text'] = value
                elif location == 'evidence': action[location] = [value]
                else: action[location] = value
                result = cli(json.dumps(action).encode(), 'render')
                self.assertEqual((result.returncode, result.stdout), (2, b''))

    def test_status_and_unknown_extensions(self):
        for key, value in [('execution_occurred', True), ('mutation_authorized', True),
                           ('status', 'AUTHORIZED'), ('schema_version', 1.0),
                           ('contract_version', '2.0.0'), ('gate_id', 'invented'),
                           ('expires_at', 'tomorrow')]:
            action = json.loads(raw()); action[key] = value
            with self.assertRaises(Denied): render(json.dumps(action).encode())
        action = json.loads(raw('blocked')); action['command'] = json.loads(raw())['command']
        with self.assertRaises(Denied): render(json.dumps(action).encode())

    def test_no_execution_and_repeat(self):
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / 'never-created'
            action = json.loads(raw()); action['command']['text'] = 'touch ' + str(sentinel)
            payload = json.dumps(action).encode()
            first = cli(payload, 'render'); second = cli(payload, 'render')
            self.assertEqual(first.returncode, 0)
            self.assertEqual(first.stdout, second.stdout)
            self.assertFalse(sentinel.exists())

    def test_secret_indicator_no_echo(self):
        action = json.loads(raw()); action['command']['text'] = 'token=' + 'SYNTHETIC' * 5
        result = cli(json.dumps(action).encode(), 'render')
        self.assertEqual((result.returncode, result.stdout), (2, b''))
        self.assertNotIn(b'SYNTHETIC', result.stderr)
        self.assertTrue(has_indicator(('-----BEGIN ' + 'PRIVATE KEY-----').encode()))
        encoded = json.dumps(action).replace('token=', '\\u0074oken=').encode()
        self.assertEqual(cli(encoded, 'render').returncode, 2)

    def test_invalid_cli_no_echo(self):
        result = cli(b'', 'payload-marker-not-a-command')
        self.assertEqual((result.returncode, result.stdout, result.stderr),
                         (2, b'', b'BLOCKER=REPO_CP_NONCONFORMANCE\n'))

    def test_tampered_or_missing_source_denied(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            shutil.copytree(ROOT / 'vendor', target / 'vendor')
            shutil.copytree(ROOT / 'pins', target / 'pins')
            impl = target / 'vendor/foundation/src/operator_action.py'
            impl.write_bytes(impl.read_bytes() + b'\nraise RuntimeError("must not load")\n')
            with self.assertRaises(Denied): render(raw(), target)
            impl.unlink()
            with self.assertRaises(Denied): render(raw(), target)

    def test_tampered_manifest_pin_denied(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            shutil.copytree(ROOT / 'pins', target / 'pins')
            pin = target / 'pins/foundation-repository.json'
            data = json.loads(pin.read_bytes()); data['revision'] = 'main'
            pin.write_text(json.dumps(data))
            with self.assertRaises(Denied): verify(target)
            data['revision'] = SOURCE['repository_revision']; data['schema_version'] = True
            pin.write_text(json.dumps(data))
            with self.assertRaises(Denied): verify(target)


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'repo-cp'
        for name in ('pins', 'vendor', 'registries', 'schemas'):
            shutil.copytree(ROOT / name, self.root / name)
        self.peer = self.base / 'auth-cp'
        self.peer.mkdir()
        self.data = registry(self.root)
        self.entry = next(r for r in self.data['repositories'] if r['repository'] == 'auth-cp')
        for filename in self.entry['files']:
            path = self.peer / filename; path.parent.mkdir(parents=True, exist_ok=True)
            if filename == 'VERSION': content = b'1.0.0\n'
            elif filename.endswith('.json'):
                content = json.dumps({'foundation': {'revision': SOURCE['repository_revision'],
                                                    'doctrine_revision': SOURCE['doctrine_revision']}}).encode()
            else: content = b'Synthetic public repository metadata\n'
            path.write_bytes(content)
            self.entry['files'][filename] = hashlib.sha256(content).hexdigest()
        (self.peer / '.git/refs/heads').mkdir(parents=True)
        (self.peer / '.git/HEAD').write_text('ref: refs/heads/main\n')
        (self.peer / '.git/refs/heads/main').write_text(self.entry['source_revision'] + '\n')
        self.save()

    def save(self):
        (self.root / 'registries/repositories.json').write_text(json.dumps(self.data))

    def run_audit(self):
        return audit(self.base, pilot=True, root=self.root)

    def test_default_does_not_enroll_or_read_pilot(self):
        report = audit(self.base, root=self.root)
        self.assertEqual(report['repositories_audited'], [])
        self.assertEqual(report['results'][-1]['status'], 'NOT_APPLICABLE')

    def test_pilot_success_and_no_change_second_audit(self):
        before = snapshot(self.base)
        first = self.run_audit(); second = self.run_audit()
        self.assertEqual(first, second)
        self.assertEqual(before, snapshot(self.base))
        self.assertEqual(first['status'], 'UNKNOWN')  # Offline remote freshness.
        self.assertEqual([r for r in first['results'] if r['status'] == 'DRIFT'], [])
        self.assertFalse(first['automatic_execution'])

    def test_stale_head(self):
        (self.peer / '.git/refs/heads/main').write_text('0' * 40)
        self.assertIn('BRANCH_OR_REVISION_CHANGED', str(self.run_audit()))

    def test_missing_authority_metadata(self):
        (self.peer / 'OWNERSHIP.md').unlink()
        self.assertEqual(self.run_audit()['status'], 'BLOCKED')

    def test_modified_metadata_is_drift(self):
        (self.peer / 'README.md').write_text('Changed public content')
        self.assertEqual(self.run_audit()['status'], 'DRIFT')

    def test_stale_handoff_pin(self):
        path = self.peer / 'registries/b70-revision-handoff.json'
        content = json.dumps({'foundation': {'revision': '0' * 40, 'doctrine_revision': SOURCE['doctrine_revision']}}).encode()
        path.write_bytes(content)
        self.entry['files']['registries/b70-revision-handoff.json'] = hashlib.sha256(content).hexdigest(); self.save()
        self.assertIn('HANDOFF_PIN_REVIEW_REQUIRED', str(self.run_audit()))

    def test_secret_indicator_not_in_report(self):
        (self.peer / 'README.md').write_text('token=' + 'SYNTHETIC' * 5)
        report = self.run_audit()
        self.assertEqual(report['status'], 'BLOCKED')
        self.assertNotIn('SYNTHETIC', json.dumps(report))

    def test_symlink_refused(self):
        (self.peer / 'README.md').unlink()
        (self.peer / 'README.md').symlink_to(self.peer / 'VERSION')
        self.assertEqual(self.run_audit()['status'], 'BLOCKED')
        with self.assertRaises(Denied): read_public(self.peer, '../repo-cp/README.md')

    def test_absent_repository_unknown_and_blocked(self):
        shutil.rmtree(self.peer)
        report = self.run_audit()
        self.assertEqual(report['status'], 'BLOCKED')
        self.assertIn('CHECKOUT_OR_REVISION_UNAVAILABLE', str(report))

    def test_unsupported_git_layout(self):
        shutil.rmtree(self.peer / '.git'); (self.peer / '.git').write_text('gitdir: /untrusted')
        self.assertIn('CHECKOUT_OR_REVISION_UNAVAILABLE', str(self.run_audit()))

    def test_packed_ref(self):
        (self.peer / '.git/refs/heads/main').unlink()
        (self.peer / '.git/packed-refs').write_text(self.entry['source_revision'] + ' refs/heads/main\n')
        self.assertEqual(head(self.peer), ('main', self.entry['source_revision']))

    def test_duplicate_repositories(self):
        self.data['repositories'].append(copy.deepcopy(self.entry)); self.save()
        with self.assertRaises(Denied): self.run_audit()

    def test_enrollment_requires_explicit_record(self):
        self.entry['state'] = 'ENROLLED'; self.save()
        with self.assertRaises(Denied): self.run_audit()
        self.entry['enrollment_authorization'] = 'Synthetic Louis-reviewed enrollment record'; self.save()
        self.assertEqual(audit(self.base, root=self.root)['repositories_audited'], ['auth-cp'])

    def test_mutable_pin_and_identity_conflict(self):
        self.entry['source_revision'] = 'main'; self.save()
        with self.assertRaises(Denied): self.run_audit()
        self.entry['source_revision'] = '0' * 40
        self.entry['canonical_remote'] = 'git@github.com:lhpoulin-cmyk/other-cp.git'; self.save()
        with self.assertRaises(Denied): self.run_audit()

    def test_unapproved_file_and_controls(self):
        self.entry['files']['credentials.json'] = '0' * 64; self.save()
        with self.assertRaises(Denied): self.run_audit()
        del self.entry['files']['credentials.json']
        self.entry['repository'] = 'auth-cp\n'; self.save()
        with self.assertRaises(Denied): self.run_audit()

    def test_proposals_never_write_or_authorize(self):
        before = snapshot(self.base)
        report = self.run_audit()
        first = proposals(report)
        self.assertEqual(first, proposals(report))
        self.assertIsNone(first['patch'])
        self.assertFalse(first['automatic_execution'])
        self.assertEqual(before, snapshot(self.base))

    def test_enrollment_review_patch_and_reversal(self):
        # Apply only inside an isolated synthetic checkout, never repo-cp or peers.
        shutil.copyfile(ROOT / 'registries/repositories.json', self.root / 'registries/repositories.json')
        patch = (ROOT / 'docs/proposals/auth-cp-enrollment.patch').read_bytes()
        before = snapshot(self.root)
        def apply(*options):
            return subprocess.run(['git', 'apply', *options, '-'], cwd=self.root,
                                  input=patch, capture_output=True, check=False)
        self.assertEqual(apply('--check').returncode, 0)
        self.assertEqual(apply().returncode, 0)
        after = snapshot(self.root)
        data = registry(self.root)
        self.assertEqual([r['repository'] for r in data['repositories'] if r['state'] == 'ENROLLED'], ['auth-cp'])
        self.assertNotEqual(apply().returncode, 0)
        self.assertEqual(after, snapshot(self.root))
        self.assertEqual(apply('--reverse').returncode, 0)
        self.assertEqual(before, snapshot(self.root))


if __name__ == '__main__':
    unittest.main()
