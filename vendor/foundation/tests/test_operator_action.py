"""Public synthetic declarations; no operational commands are executed."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from operator_action import (MAX_INPUT_BYTES, OperatorActionError, load_action,
                             render_action, validate_action)
FIXTURES = ROOT / 'tests/fixtures/operator_action'
PINS = {'repository_revision': '1' * 40, 'doctrine_revision': '2' * 40}


def fixture(name='ready'):
    return load_action((FIXTURES / (name + '.json')).read_bytes())


class OperatorActionTests(unittest.TestCase):
    def deny(self, action):
        with self.assertRaises(OperatorActionError):
            render_action(action, expected_source=PINS)

    def cli(self, raw, *args):
        return subprocess.run([sys.executable, '-B', str(ROOT / 'tools/render_operator_action.py'),
                               '--foundation-revision', PINS['repository_revision'],
                               '--doctrine-revision', PINS['doctrine_revision'], *args],
                              input=raw, capture_output=True, check=False)

    def test_positive_golden_and_immutable(self):
        for name in ('ready', 'blocked'):
            with self.subTest(name=name):
                action = fixture(name)
                before = copy.deepcopy(action)
                expected = (FIXTURES / (name + '.txt')).read_text()
                self.assertEqual(render_action(action, expected_source=PINS), expected)
                self.assertEqual(render_action(action, expected_source=PINS), expected)
                self.assertEqual(action, before)
                self.assertEqual(validate_action(action, expected_source=PINS), {
                    'status': 'DECLARATION_CONFORMANT', 'execution_occurred': False,
                    'mutation_authorized': False, 'live_acceptance': False})
                result = self.cli(json.dumps(action).encode())
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout.decode(), expected)
                self.assertEqual(result.stderr, b'')

    def test_missing_and_unknown_fields(self):
        for key in fixture():
            action = fixture()
            del action[key]
            with self.subTest(key=key):
                self.deny(action)
        for where in (None, 'source', 'command'):
            action = fixture()
            (action if where is None else action[where])['extra'] = 'unrecognized'
            self.deny(action)

    def test_status_command_reason_consistency(self):
        self.deny(fixture('invalid-blocked-command'))
        for key, value in [('command', None), ('stop_reason', 'Not ready'),
                           ('status', 'AUTHORIZED'), ('phase', 'EXECUTION')]:
            action = fixture(); action[key] = value
            self.deny(action)
        action = fixture('blocked'); action['stop_reason'] = None
        self.deny(action)

    def test_versions_and_boolean_types(self):
        for key, value in [('schema_version', True), ('schema_version', 1.0),
                           ('schema_version', 2), ('contract_version', '2.0.0'),
                           ('authority', 'repo-cp'), ('contract_id', 'replacement'),
                           ('execution_occurred', True), ('execution_occurred', 0),
                           ('mutation_authorized', True), ('mutation_authorized', 'false')]:
            action = fixture(); action[key] = value
            with self.subTest(key=key, value=value): self.deny(action)

    def test_expected_pins_required_and_independent(self):
        for pins in (None, {}, fixture()['source'] | {'extra': 'x'},
                     PINS | {'doctrine_revision': '3' * 40},
                     PINS | {'repository_revision': '3' * 40},
                     PINS | {'repository_revision': '1' * 40 + '\n'}):
            with self.subTest(pins=pins), self.assertRaises(OperatorActionError):
                render_action(fixture(), expected_source=pins)

    def test_terminal_injection_rejected_every_text_location(self):
        for bad in ('\x1b[2J', 'safe\nMUTATION_AUTHORIZED: YES', 'safe\rspoof',
                    'trailing\n', '\t', '\x00', '\x7f', '\u202e', '\u200b', '', '   '):
            for place in ('repository', 'evidence', 'command'):
                action = fixture()
                if place == 'evidence': action[place] = [bad]
                elif place == 'command': action[place]['text'] = bad
                else: action[place] = bad
                with self.subTest(bad=repr(bad), place=place): self.deny(action)

    def test_malformed_and_duplicate_json(self):
        samples = [b'{', b'\xff', b'{"a":1,"a":2}', b'{"nested":{"a":1,"a":2}}',
                   b'NaN', b'Infinity', b'-Infinity', b'[' * 2000, b'9' * 10000,
                   b' ' * (MAX_INPUT_BYTES + 1)]
        for raw in samples:
            with self.subTest(raw=raw[:40]), self.assertRaises(OperatorActionError):
                load_action(raw)

    def test_nonobject_and_incomplete_collections(self):
        for value in (None, True, 1, [], 'action'):
            self.deny(value)
        for key in ('scope', 'return_output', 'preconditions', 'risks'):
            action = fixture(); action[key] = []
            self.deny(action)
        action = fixture(); action['evidence'] = []
        self.assertIn('EVIDENCE:\n  - NONE\n', render_action(action, expected_source=PINS))

    def test_size_and_shell_constraints(self):
        for key, value in [('shell', 'unknown'), ('working_directory', ''), ('text', 'x' * 4097)]:
            action = fixture(); action['command'][key] = value
            self.deny(action)
        action = fixture(); action['evidence'] = ['x'] * 65
        self.deny(action)

    def test_exact_copyable_commands_for_both_shells(self):
        for shell, command in [('bash', "printf '%s' '$HOME; `literal`'"),
                               ('powershell', "Write-Output '$env:HOME; literal'")]:
            action = fixture(); action['command'].update(shell=shell, text=command)
            rendered = render_action(action, expected_source=PINS)
            self.assertIn('\n' + command + '\nEXECUTION_OCCURRED: NO\n', rendered)

    def test_cli_failure_is_atomic_and_does_not_echo_payload(self):
        action = fixture(); action['extra'] = 'sensitive-sentinel-do-not-echo'
        for raw in (json.dumps(action).encode(), b'{"secret-sentinel":', b'9' * 10000,
                    (FIXTURES / 'invalid-blocked-command.json').read_bytes()):
            result = self.cli(raw)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, b'')
            self.assertIn(b'BLOCKER=OPERATOR_ACTION_NONCONFORMANCE', result.stderr)
            self.assertNotIn(b'sentinel', result.stderr)
            self.assertNotIn(b'forbidden-blocked-command', result.stderr)

    def test_rendering_never_executes_command(self):
        import tempfile
        with tempfile.TemporaryDirectory(prefix='helix-action-') as directory:
            sentinel = Path(directory) / 'must-not-exist'
            action = fixture(); action['command']['text'] = 'touch ' + str(sentinel)
            result = self.cli(json.dumps(action).encode())
            self.assertEqual(result.returncode, 0)
            self.assertFalse(sentinel.exists())

    def test_registry_paths_and_boundaries(self):
        registry = json.loads((ROOT / 'registries/operator-action.json').read_text())
        for key in ('contract', 'schema', 'implementation', 'cli', 'tests', 'fixtures'):
            self.assertTrue((ROOT / registry[key]).exists())
        for key in ('contract_id', 'contract_version', 'authority'):
            self.assertEqual(registry[key], fixture()[key])
        self.assertEqual(registry['status'], 'REPOSITORY_CONTRACT_ONLY')
        self.assertEqual(registry['fleet_conformance'], 'unverified')
        self.assertFalse(registry['runtime_activation'])
        self.assertFalse(registry['mutation_authorized'])


if __name__ == '__main__':
    unittest.main()
