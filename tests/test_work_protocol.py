"""Schema and relationship tests for repository work contracts."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from repocp.safety import Denied
from repocp.work_protocol import WORKFLOW, schemas, topology, validate

FIXTURES = ROOT / 'tests/fixtures/work-protocol'


def fixture(kind):
    return json.loads((FIXTURES / (kind + '.json')).read_bytes())


def encoded(document):
    return json.dumps(document).encode()


def continuation(revalidation_status):
    return {
        'handoff_id': 'synthetic.pause.001',
        'work_entry_id': 'synthetic.repo-cp.001',
        'workspace_state_preserved': True,
        'mutation_gate_at_handoff': 'CLOSED',
        'in_flight_invocation': {
            'identity': 'synthetic-invocation',
            'disposition': 'INTERRUPTED',
            'attribution': 'CURRENT_WORK_ENTRY',
        },
        'session_binding': 'synthetic-session',
        'session_disposition': 'RELEASED',
        'continuation_point': 'Resume at the synthetic validation boundary.',
        'revalidation_requirements': [
            'Recheck HEAD, workspace dirtiness and the mutation gate',
        ],
        'revalidation_status': revalidation_status,
    }


def cli(kind, document):
    return subprocess.run(
        [sys.executable, '-B', str(ROOT / 'tools/repo-cp'), 'check-work-' + kind],
        input=encoded(document), capture_output=True, check=False)


class WorkProtocolTests(unittest.TestCase):
    def test_schemas_and_fixtures(self):
        self.assertEqual(set(schemas()), {'entry', 'result', 'topology'})
        for kind in ('entry', 'result'):
            document = fixture(kind)
            receipt = validate(kind, encoded(document))
            self.assertEqual(receipt['status'], 'PASS')
            self.assertEqual(receipt['invariant_id'], 'HELIX_CLEAN_EXECUTION_BASELINE_V1')
            self.assertFalse(receipt['automatic_execution'])
            self.assertEqual((receipt['work_state'], receipt['priority']), ('ACTIVE', 'GREEN'))
            result = cli(kind, document)
            self.assertEqual((result.returncode, result.stderr), (0, b''))
            self.assertEqual(json.loads(result.stdout), receipt)
        repository_receipt = subprocess.run(
            [sys.executable, '-B', str(ROOT / 'tools/repo-cp'), 'validate'],
            capture_output=True, check=False)
        self.assertEqual(repository_receipt.returncode, 0)
        self.assertEqual(json.loads(repository_receipt.stdout)['clean_execution_invariant_id'],
                         'HELIX_CLEAN_EXECUTION_BASELINE_V1')
        self.assertEqual(json.loads(repository_receipt.stdout)['workflow'], WORKFLOW)
        self.assertEqual(json.loads(repository_receipt.stdout)['work_topology'], 'PASS')

    def test_current_work_topology_keeps_state_priority_and_authority_independent(self):
        document = topology()
        self.assertEqual(document['authority'], 'NONE')
        self.assertFalse(document['automatic_preemption'])
        surfaces = document['surface_model']
        self.assertEqual(surfaces['portfolio_control_plane'], 'repo-cp')
        self.assertEqual(surfaces['primary_work_surface'], 'repo-cp')
        self.assertEqual(surfaces['authority_source'], 'EXPLICIT_WORK_ENTRY')
        self.assertEqual(surfaces['evidence_return'], 'repo-cp')
        self.assertFalse(surfaces['supporting_projects_are_control_planes'])
        self.assertEqual(set(surfaces['supporting_projects']), {
            'helix-offload', 'helix-repo-manager-bot', 'ws-code-agent', 'ws-doc-writer'})
        candidates = {
            candidate['id']: [member['id'] for member in candidate['members']]
            for candidate in document['future_work_candidates']
        }
        self.assertEqual(candidates, {
            'remediation.hardening-correctness': ['R4', 'R5'],
            'remediation.diagnostics-state-fidelity': ['R6', 'R9'],
            'remediation.evidence-trust-architecture': ['R7', 'R8'],
        })
        self.assertTrue(all(not candidate['execution_authorized']
                            for candidate in document['future_work_candidates']))
        r5 = next(member for candidate in document['future_work_candidates']
                  for member in candidate['members'] if member['id'] == 'R5')
        self.assertIn('valid dotted Git branch names are rejected', r5['summary'])
        current = {
            item['id']: (item['state'], item['priority'], item['scheduling_eligibility'],
                         item['dependencies'])
            for item in document['entries']
        }
        self.assertEqual(current, {
            '001': ('COMPLETE', 'GREEN', 'INELIGIBLE_STATE', []),
            '002': ('COMPLETE', 'GREEN', 'INELIGIBLE_STATE', []),
            '003': ('COMPLETE', 'GREEN', 'INELIGIBLE_STATE', []),
            '004': ('PARKED', 'YELLOW', 'INELIGIBLE_STATE', []),
            '005': ('COMPLETE', 'GREEN', 'INELIGIBLE_STATE', []),
            '006': ('COMPLETE', 'GREEN', 'INELIGIBLE_STATE', ['003']),
            '007': ('COMPLETE', 'GREEN', 'INELIGIBLE_STATE', []),
            '008': ('PARKED', 'RED', 'INELIGIBLE_STATE', []),
            '009': ('COMPLETE', 'GREEN', 'INELIGIBLE_STATE', []),
            '010': ('COMPLETE', 'GREEN', 'INELIGIBLE_STATE', ['005']),
            '011': ('COMPLETE', 'GREEN', 'INELIGIBLE_STATE', []),
            '012': ('PARKED', 'GREEN', 'INELIGIBLE_STATE', ['007']),
        })
        entries = {item['id']: item for item in document['entries']}
        for entry_id in ('008',):
            provenance = ' '.join(entries[entry_id]['provenance'])
            self.assertIn('DOUBLE RED', provenance)
            self.assertIn('research authority NONE', provenance)
            self.assertIn('implementation authority NONE', provenance)
        self.assertIn('Execution Admission V1', entries['005']['summary'])
        self.assertIn('deterministic admission boundary', entries['005']['summary'])
        self.assertIn('helix-offload', entries['005']['summary'])
        self.assertIn('5070 Ti remains candidate compute only',
                      ' '.join(entries['005']['provenance']))
        self.assertIn('helix-repo-manager-bot repository intelligence/evidence plane',
                      ' '.join(entries['008']['provenance']))
        self.assertIn('relationship is intentionally unresolved',
                      ' '.join(entries['008']['provenance']))
        self.assertIn('Logical ownership, execution placement and physical hosting',
                      ' '.join(entries['008']['provenance']))
        for entry_id in ('009', '010', '011'):
            provenance = ' '.join(entries[entry_id]['provenance'])
            self.assertIn('health BLUE', provenance)
            self.assertIn('normal priority GREEN', provenance)
        self.assertIn('live run was not performed', entries['009']['summary'])
        self.assertIn('Deterministic Engine for Policy and Routing', entries['010']['summary'])
        self.assertIn('synthetically validated', entries['010']['summary'])
        self.assertIn('hosted live acceptance remains unperformed', entries['010']['summary'])
        self.assertIn('c1a1c89f4d54d695adf6675e97c045a31267f29d',
                      ' '.join(entries['010']['provenance']))
        self.assertIn('coordinated Work Entry 009 run', entries['011']['summary'])
        self.assertIn('renumbered this assessment from 010 to 011',
                      ' '.join(entries['011']['provenance']))
        self.assertIn('GitHub-hosted account or repository identity', entries['012']['summary'])
        self.assertIn('live account, credential', ' '.join(entries['012']['provenance']))
        self.assertEqual(document['updated_by_work_entry'], '010')

        derp_result = json.loads(
            (ROOT / 'docs/handoffs/WORK_ENTRY_010_RESULT.json').read_bytes())
        self.assertEqual(validate('result', encoded(derp_result))['status'], 'PASS')
        self.assertEqual(derp_result['ending_head'],
                         'c1a1c89f4d54d695adf6675e97c045a31267f29d')
        self.assertEqual(derp_result['delivery_stage'], 'PUBLISHED')

        current_state = (ROOT / 'docs/CURRENT_STATE.md').read_text()
        self.assertIn('| 004 |', current_state)
        self.assertIn('| 008 |', current_state)
        self.assertIn('| 010 |', current_state)
        self.assertIn('| 012 |', current_state)
        self.assertIn('GPU workload UNPERFORMED', current_state)
        self.assertIn('measurement UNPERFORMED', current_state)
        schema = schemas()['topology']
        automatic = copy.deepcopy(document)
        automatic['automatic_preemption'] = True
        self.assertFalse(Draft202012Validator(schema).is_valid(automatic))
        invented_priority = copy.deepcopy(document)
        invented_priority['entries'][0]['priority'] = 'BLUE'
        self.assertFalse(Draft202012Validator(schema).is_valid(invented_priority))

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
        document = fixture('entry')
        del document['priority']
        cases.append(document)
        document = fixture('entry')
        del document['scheduling_eligibility']
        cases.append(document)
        document = fixture('entry')
        document['work_state'] = 'PARKED'
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

    def test_scheduling_eligibility_is_independent_of_priority(self):
        blocked = fixture('entry')
        blocked['work_state'] = 'BLOCKED'
        blocked['priority'] = 'RED'
        blocked['scheduling_eligibility'] = 'INELIGIBLE_DEPENDENCY'
        blocked['dependencies'][0]['status'] = 'PENDING'
        blocked['execution_workspace']['mutation_gate'] = 'CLOSED'
        receipt = validate('entry', encoded(blocked))
        self.assertEqual(receipt['scheduling_eligibility'], 'INELIGIBLE_DEPENDENCY')

        active = copy.deepcopy(blocked)
        active['work_state'] = 'ACTIVE'
        active['scheduling_eligibility'] = 'ELIGIBLE'
        active['execution_workspace']['mutation_gate'] = 'OPEN'
        with self.assertRaises(Denied):
            validate('entry', encoded(active))

        green = copy.deepcopy(blocked)
        green['priority'] = 'GREEN'
        self.assertEqual(validate('entry', encoded(green))['scheduling_eligibility'],
                         'INELIGIBLE_DEPENDENCY')

    def test_pause_and_resume_preserve_continuation_evidence(self):
        paused = fixture('result')
        paused['work_state'] = 'PAUSED'
        paused['continuation'] = continuation('PENDING')
        self.assertTrue(validate('result', encoded(paused))['continuation_ready'])

        missing = copy.deepcopy(paused)
        del missing['continuation']
        with self.assertRaises(Denied):
            validate('result', encoded(missing))

        resume = fixture('entry')
        resume['work_entry_phase'] = 'RESUME'
        resume['continuation'] = continuation('COMPLETED')
        self.assertTrue(validate('entry', encoded(resume))['continuation_ready'])

        not_revalidated = copy.deepcopy(resume)
        not_revalidated['continuation']['revalidation_status'] = 'PENDING'
        with self.assertRaises(Denied):
            validate('entry', encoded(not_revalidated))

        wrong_work = copy.deepcopy(resume)
        wrong_work['continuation']['work_entry_id'] = 'synthetic.repo-cp.other'
        with self.assertRaises(Denied):
            validate('entry', encoded(wrong_work))

        wrong_attribution = copy.deepcopy(resume)
        wrong_attribution['continuation']['in_flight_invocation']['disposition'] = 'NONE'
        with self.assertRaises(Denied):
            validate('entry', encoded(wrong_attribution))

    def test_discovery_closure_requires_recheck_evidence(self):
        no_evidence = fixture('result')
        no_evidence['discovery_coverage']['recheck_evidence'] = []
        with self.assertRaises(Denied):
            validate('result', encoded(no_evidence))

        unresolved = fixture('result')
        unresolved['work_state'] = 'COMPLETE'
        unresolved['discovery_coverage']['actionable_findings_remaining'] = ['finding.open']
        with self.assertRaises(Denied):
            validate('result', encoded(unresolved))

        bounded_unknown = fixture('result')
        bounded_unknown['work_state'] = 'COMPLETE'
        bounded_unknown['discovery_coverage']['remaining_unknowns'] = ['Unavailable peer evidence']
        self.assertEqual(validate('result', encoded(bounded_unknown))['status'], 'PASS')

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
        document = fixture('result')
        del document['status_topology']['nodes'][0]['priority']
        cases.append(document)
        document = fixture('result')
        del document['priority']
        cases.append(document)
        document = fixture('result')
        document['status_topology']['nodes'][0]['status'] = 'PARKED'
        document['status_topology']['nodes'][0]['blocking'] = True
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
            ('paused', 'WORK', 'PAUSED', False),
            ('parked', 'FUTURE_WORK', 'PARKED', False),
            ('finding', 'FINDING', 'ACTIVE', False),
            ('pending', 'DEPENDENCY', 'PENDING', False),
            ('blocked', 'DEPENDENCY', 'BLOCKED', True),
            ('incomplete', 'WORK', 'NON_BLOCKING_INCOMPLETE', False),
            ('unknown', 'EXTERNAL_DEPENDENCY', 'UNKNOWN', False),
            ('drift', 'EXTERNAL_DEPENDENCY', 'DRIFT', False),
            ('approval', 'AUTHORIZATION', 'AUTHORIZATION_REQUIRED', False),
            ('handoff', 'CROSS_CONTROL_PLANE_REQUEST', 'PENDING', False),
        ]
        document['status_topology']['nodes'] = [
            {'id': node_id, 'kind': kind, 'status': status, 'priority': 'GREEN',
             'summary': 'Synthetic ' + node_id, 'owner': 'synthetic-owner', 'blocking': blocking}
            for node_id, kind, status, blocking in statuses
        ]
        document['status_topology']['relationships'] = [
            {'subject': 'blocked', 'predicate': 'BLOCKED_BY', 'object': 'pending'},
            {'subject': 'active', 'predicate': 'DEPENDS_ON', 'object': 'pending'},
            {'subject': 'incomplete', 'predicate': 'NON_BLOCKING_FOR', 'object': 'active'},
            {'subject': 'approval', 'predicate': 'REQUIRES_AUTHORIZATION_FROM', 'object': 'active'},
            {'subject': 'unknown', 'predicate': 'MAY_BE_RESOLVED_BY', 'object': 'active'},
            {'subject': 'pending', 'predicate': 'OWNED_BY', 'object': 'active'},
            {'subject': 'handoff', 'predicate': 'HANDOFF_TO', 'object': 'unknown'},
            {'subject': 'completed', 'predicate': 'SUPERSEDES', 'object': 'drift'},
            {'subject': 'finding', 'predicate': 'PROMOTED_TO', 'object': 'parked'},
        ]
        self.assertEqual(validate('result', encoded(document))['status'], 'PASS')

        parked = next(node for node in document['status_topology']['nodes']
                      if node['id'] == 'parked')
        parked['priority'] = 'RED'
        self.assertEqual(validate('result', encoded(document))['status'], 'PASS')
        self.assertEqual(document['status_topology']['nodes'][1]['status'], 'ACTIVE')

        parked['status'] = 'ACTIVE'
        with self.assertRaises(Denied):
            validate('result', encoded(document))

        bad_resolution = fixture('result')
        bad_resolution['status_topology']['relationships'].append({
            'subject': 'work.optional-review',
            'predicate': 'MAY_BE_RESOLVED_BY',
            'object': 'owner.operator',
        })
        with self.assertRaises(Denied):
            validate('result', encoded(bad_resolution))

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
