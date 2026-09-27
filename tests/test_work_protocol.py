"""Schema and relationship tests for repository work contracts."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from repocp.safety import Denied
from repocp.work_protocol import schemas, validate

FIXTURES = ROOT / 'tests/fixtures/work-protocol'


def fixture(kind):
    return json.loads((FIXTURES / (kind + '.json')).read_bytes())


def encoded(document):
    return json.dumps(document).encode()


def cli(kind, document):
    return subprocess.run(
        [sys.executable, '-B', str(ROOT / 'tools/repo-cp'), 'check-work-' + kind],
        input=encoded(document), capture_output=True, check=False)


class WorkProtocolTests(unittest.TestCase):
    def test_schemas_and_fixtures(self):
        self.assertEqual(set(schemas()), {'entry', 'result'})
        for kind in ('entry', 'result'):
            document = fixture(kind)
            receipt = validate(kind, encoded(document))
            self.assertEqual(receipt['status'], 'PASS')
            self.assertEqual(receipt['invariant_id'], 'HELIX_CLEAN_EXECUTION_BASELINE_V1')
            self.assertFalse(receipt['automatic_execution'])
            result = cli(kind, document)
            self.assertEqual((result.returncode, result.stderr), (0, b''))
            self.assertEqual(json.loads(result.stdout), receipt)
        repository_receipt = subprocess.run(
            [sys.executable, '-B', str(ROOT / 'tools/repo-cp'), 'validate'],
            capture_output=True, check=False)
        self.assertEqual(repository_receipt.returncode, 0)
        self.assertEqual(json.loads(repository_receipt.stdout)['clean_execution_invariant_id'],
                         'HELIX_CLEAN_EXECUTION_BASELINE_V1')

    def test_entry_authority_scope_dependencies_and_dirty_state(self):
        cases = []
        document = fixture('entry')
        document['authority']['explicitly_not_granted'] = list(document['authority']['granted'])
        cases.append(document)
        document = fixture('entry')
        document['mutation_scope']['prohibited'] = list(document['mutation_scope']['allowed'])
        cases.append(document)
        document = fixture('entry')
        document['dependencies'].append(copy.deepcopy(document['dependencies'][0]))
        cases.append(document)
        document = fixture('entry')
        document['source_workspace']['dirty_state']['state'] = 'CLEAN'
        cases.append(document)
        for candidate in cases:
            with self.assertRaises(Denied):
                validate('entry', encoded(candidate))

    def test_clean_execution_baseline_mutation_gate(self):
        entry = fixture('entry')
        self.assertEqual(validate('entry', encoded(entry))['mutation_gate'], 'OPEN')

        closed = fixture('entry')
        closed['isolation'] = {'used': False, 'mechanism': 'NONE',
                               'reason': 'Mutation is prohibited pending source resolution.'}
        closed['execution_workspace'] = copy.deepcopy(closed['source_workspace'])
        closed['execution_workspace']['mutation_gate'] = 'CLOSED'
        receipt = validate('entry', encoded(closed))
        self.assertEqual(receipt['mutation_gate'], 'CLOSED')
        closed_cli = cli('entry', closed)
        self.assertEqual(closed_cli.returncode, 1)
        self.assertEqual(json.loads(closed_cli.stdout)['mutation_gate'], 'CLOSED')

        cases = []
        unsafe = copy.deepcopy(closed)
        unsafe['execution_workspace']['mutation_gate'] = 'OPEN'
        cases.append(unsafe)
        same_identity = fixture('entry')
        same_identity['execution_workspace']['identity'] = same_identity['source_workspace']['identity']
        cases.append(same_identity)
        wrong_baseline = fixture('entry')
        wrong_baseline['execution_workspace']['head'] = '2' * 40
        cases.append(wrong_baseline)
        dirty_start = fixture('entry')
        dirty_start['execution_workspace']['dirty_state'] = {
            'state': 'DIRTY', 'staged': [], 'unstaged': ['task-change'], 'untracked': []}
        dirty_start['execution_workspace']['dirtiness_attribution'] = 'CURRENT_WORK_ENTRY'
        cases.append(dirty_start)
        for candidate in cases:
            with self.assertRaises(Denied):
                validate('entry', encoded(candidate))

        continuation = fixture('entry')
        continuation['work_entry_phase'] = 'CONTINUE'
        continuation['execution_workspace']['dirty_state'] = {
            'state': 'DIRTY', 'staged': [], 'unstaged': ['task-change'], 'untracked': []}
        continuation['execution_workspace']['dirtiness_attribution'] = 'CURRENT_WORK_ENTRY'
        self.assertEqual(validate('entry', encoded(continuation))['mutation_gate'], 'OPEN')

    def test_result_node_and_relationship_invariants(self):
        cases = []
        document = fixture('result')
        document['status_topology']['nodes'][0]['blocking'] = True
        cases.append(document)
        document = fixture('result')
        document['status_topology']['nodes'].append(copy.deepcopy(document['status_topology']['nodes'][0]))
        cases.append(document)
        document = fixture('result')
        document['status_topology']['relationships'][0]['object'] = 'missing.node'
        cases.append(document)
        document = fixture('result')
        document['status_topology']['relationships'][0]['predicate'] = 'BLOCKED_BY'
        cases.append(document)
        document = fixture('result')
        document['status_topology']['nodes'][2]['status'] = 'PENDING'
        cases.append(document)
        for candidate in cases:
            with self.assertRaises(Denied):
                validate('result', encoded(candidate))

    def test_result_attributes_all_ending_dirtiness(self):
        result = fixture('result')
        self.assertTrue(validate('result', encoded(result))['ending_dirtiness_accounted'])
        cases = []
        missing = fixture('result')
        missing['ending_dirtiness_attribution']['current_work_entry']['unstaged'] = []
        cases.append(missing)
        duplicate = fixture('result')
        duplicate['ending_dirtiness_attribution']['pre_existing']['unstaged'] = ['README.md']
        cases.append(duplicate)
        same_workspace = fixture('result')
        same_workspace['workspace_evidence']['execution_workspace_identity'] = \
            same_workspace['workspace_evidence']['source_workspace_identity']
        cases.append(same_workspace)
        wrong_baseline = fixture('result')
        wrong_baseline['starting_head'] = '2' * 40
        cases.append(wrong_baseline)
        for candidate in cases:
            with self.assertRaises(Denied):
                validate('result', encoded(candidate))

    def test_complete_status_topology_vocabulary(self):
        document = fixture('result')
        statuses = [
            ('completed', 'WORK', 'COMPLETED', False),
            ('active', 'WORK', 'ACTIVE', False),
            ('pending', 'DEPENDENCY', 'PENDING', False),
            ('blocked', 'DEPENDENCY', 'BLOCKED', True),
            ('incomplete', 'WORK', 'NON_BLOCKING_INCOMPLETE', False),
            ('unknown', 'EXTERNAL_DEPENDENCY', 'UNKNOWN', False),
            ('drift', 'EXTERNAL_DEPENDENCY', 'DRIFT', False),
            ('approval', 'AUTHORIZATION', 'AUTHORIZATION_REQUIRED', False),
            ('handoff', 'CROSS_CONTROL_PLANE_REQUEST', 'PENDING', False),
        ]
        document['status_topology']['nodes'] = [
            {'id': node_id, 'kind': kind, 'status': status,
             'summary': 'Synthetic ' + node_id, 'owner': 'synthetic-owner', 'blocking': blocking}
            for node_id, kind, status, blocking in statuses
        ]
        document['status_topology']['relationships'] = [
            {'subject': 'blocked', 'predicate': 'BLOCKED_BY', 'object': 'pending'},
            {'subject': 'active', 'predicate': 'DEPENDS_ON', 'object': 'pending'},
            {'subject': 'incomplete', 'predicate': 'NON_BLOCKING_FOR', 'object': 'active'},
            {'subject': 'approval', 'predicate': 'REQUIRES_AUTHORIZATION_FROM', 'object': 'active'},
            {'subject': 'pending', 'predicate': 'OWNED_BY', 'object': 'active'},
            {'subject': 'handoff', 'predicate': 'HANDOFF_TO', 'object': 'unknown'},
            {'subject': 'completed', 'predicate': 'SUPERSEDES', 'object': 'drift'},
        ]
        self.assertEqual(validate('result', encoded(document))['status'], 'PASS')

    def test_invalid_input_is_atomic_and_never_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / 'never-created'
            document = fixture('entry')
            document['objective'] = 'touch ' + str(sentinel)
            result = cli('entry', document)
            self.assertEqual(result.returncode, 0)
            self.assertFalse(sentinel.exists())
        document = fixture('entry')
        document['objective'] = 'token=' + 'SYNTHETIC' * 5
        result = cli('entry', document)
        self.assertEqual((result.returncode, result.stdout), (2, b''))
        self.assertEqual(result.stderr, b'BLOCKER=REPO_CP_NONCONFORMANCE\n')
        self.assertNotIn(b'SYNTHETIC', result.stderr)


if __name__ == '__main__':
    unittest.main()
