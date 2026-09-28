"""Validate bounded work contracts; never execute, authorize, discover or write."""
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from .consumer import ROOT
from .safety import Denied, has_indicator, load, read_public

PROTOCOLS = {
    'entry': ('HELIX_WORK_ENTRY_V1', 'schemas/work-entry-v1.schema.json'),
    'result': ('HELIX_WORK_RESULT_V1', 'schemas/work-result-v1.schema.json'),
}
SCHEMA_PATHS = {
    **{kind: path for kind, (_, path) in PROTOCOLS.items()},
    'topology': 'schemas/work-topology-v1.schema.json',
}
CLEAN_EXECUTION_BASELINE = 'HELIX_CLEAN_EXECUTION_BASELINE_V1'
WORKFLOW = 'HELIX_LOUIS_WORKFLOW_V1'
WORK_TOPOLOGY = 'HELIX_WORK_TOPOLOGY_V1'
TOPOLOGY_PATH = 'registries/work-topology.json'


def schemas(root=ROOT):
    result = {}
    for kind, path in SCHEMA_PATHS.items():
        schema = load(read_public(root, path))
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError:
            raise Denied('WORK_PROTOCOL_SCHEMA_INVALID') from None
        result[kind] = schema
    return result


def topology(root=ROOT):
    document = load(read_public(root, TOPOLOGY_PATH))
    schema = schemas(root)['topology']
    if not isinstance(document, dict) or not Draft202012Validator(schema).is_valid(document):
        raise Denied('WORK_TOPOLOGY_NONCONFORMANCE') from None
    identifiers = [entry['id'] for entry in document['entries']]
    if len(identifiers) != len(set(identifiers)):
        raise Denied('WORK_TOPOLOGY_NONCONFORMANCE') from None
    candidate_identifiers = [candidate['id'] for candidate in document['future_work_candidates']]
    member_identifiers = [member['id'] for candidate in document['future_work_candidates']
                          for member in candidate['members']]
    if len(candidate_identifiers) != len(set(candidate_identifiers)) \
            or len(member_identifiers) != len(set(member_identifiers)) \
            or set(candidate_identifiers) & set(identifiers):
        raise Denied('WORK_TOPOLOGY_NONCONFORMANCE') from None
    by_id = {entry['id']: entry for entry in document['entries']}
    for entry in document['entries']:
        if any(identifier not in by_id for identifier in entry['dependencies']):
            raise Denied('WORK_TOPOLOGY_NONCONFORMANCE') from None
        unsatisfied = [identifier for identifier in entry['dependencies']
                       if by_id[identifier]['state'] != 'COMPLETE']
        if entry['state'] == 'ACTIVE':
            expected = 'ELIGIBLE'
            if unsatisfied:
                raise Denied('WORK_TOPOLOGY_NONCONFORMANCE') from None
        elif entry['state'] == 'BLOCKED':
            expected = 'INELIGIBLE_DEPENDENCY'
            if not unsatisfied:
                raise Denied('WORK_TOPOLOGY_NONCONFORMANCE') from None
        else:
            expected = 'INELIGIBLE_STATE'
        if entry['scheduling_eligibility'] != expected:
            raise Denied('WORK_TOPOLOGY_NONCONFORMANCE') from None
    return document


def _semantic_entry(document):
    state_present = 'work_state' in document
    if state_present != ('priority' in document):
        raise Denied('WORK_ENTRY_LIFECYCLE_CONFLICT')
    if state_present != ('scheduling_eligibility' in document):
        raise Denied('WORK_ENTRY_LIFECYCLE_CONFLICT')
    authority = document['authority']
    if set(authority['granted']) & set(authority['explicitly_not_granted']):
        raise Denied('WORK_ENTRY_AUTHORITY_CONFLICT')
    scope = document['mutation_scope']
    if set(scope['allowed']) & set(scope['prohibited']):
        raise Denied('WORK_ENTRY_SCOPE_CONFLICT')
    identifiers = [item['id'] for item in document['dependencies']]
    if len(identifiers) != len(set(identifiers)):
        raise Denied('WORK_ENTRY_DUPLICATE_DEPENDENCY')
    unsatisfied = [item for item in document['dependencies']
                   if item.get('blocking', True) and item['status'] != 'COMPLETED']
    if state_present:
        state = document['work_state']
        if state == 'ACTIVE':
            expected_eligibility = 'ELIGIBLE'
            if unsatisfied:
                raise Denied('WORK_ENTRY_DEPENDENCY_CONFLICT')
        elif state == 'BLOCKED':
            expected_eligibility = 'INELIGIBLE_DEPENDENCY'
            if not unsatisfied:
                raise Denied('WORK_ENTRY_DEPENDENCY_CONFLICT')
        else:
            expected_eligibility = 'INELIGIBLE_STATE'
        if 'scheduling_eligibility' in document \
                and document['scheduling_eligibility'] != expected_eligibility:
            raise Denied('WORK_ENTRY_DEPENDENCY_CONFLICT')
    source = document['source_workspace']
    execution = document['execution_workspace']
    _semantic_workspace_state(source)
    _semantic_workspace_state(execution)
    gate = execution['mutation_gate']
    if state_present and document['work_state'] in ('PARKED', 'PAUSED', 'BLOCKED', 'COMPLETE') \
            and gate != 'CLOSED':
        raise Denied('WORK_ENTRY_LIFECYCLE_CONFLICT')
    phase = document['work_entry_phase']
    safe_to_open = ((phase == 'START' and execution['dirty_state']['state'] == 'CLEAN'
                     and execution['dirtiness_attribution'] == 'NONE')
                    or (phase in ('CONTINUE', 'RESUME')
                        and ((execution['dirty_state']['state'] == 'CLEAN'
                              and execution['dirtiness_attribution'] == 'NONE')
                             or (execution['dirty_state']['state'] == 'DIRTY'
                                 and execution['dirtiness_attribution'] == 'CURRENT_WORK_ENTRY'))))
    if gate == 'OPEN' and (not safe_to_open
            or execution['head'] != document['canonical_baseline']['resolved_head']):
        raise Denied('WORK_ENTRY_MUTATION_GATE_CONFLICT')
    if execution['dirtiness_attribution'] in ('PRE_EXISTING', 'UNRELATED', 'MIXED', 'UNKNOWN') \
            and gate != 'CLOSED':
        raise Denied('WORK_ENTRY_MUTATION_GATE_CONFLICT')
    isolation = document['isolation']
    if isolation['used']:
        if (isolation['mechanism'] == 'NONE' or source['identity'] == execution['identity']
                or (phase == 'START' and (execution['dirty_state']['state'] != 'CLEAN'
                    or execution['dirtiness_attribution'] != 'NONE'))):
            raise Denied('WORK_ENTRY_ISOLATION_CONFLICT')
    elif isolation['mechanism'] != 'NONE' or source['identity'] != execution['identity']:
        raise Denied('WORK_ENTRY_ISOLATION_CONFLICT')
    continuation = document.get('continuation')
    if phase == 'RESUME' or (state_present and document['work_state'] == 'PAUSED'):
        if continuation is None:
            raise Denied('WORK_ENTRY_CONTINUATION_CONFLICT')
    elif continuation is not None:
        raise Denied('WORK_ENTRY_CONTINUATION_CONFLICT')
    if continuation is not None:
        _semantic_continuation(continuation)
        if continuation['work_entry_id'] != document['work_entry_id'] \
                or continuation['mutation_gate_at_handoff'] != 'CLOSED':
            raise Denied('WORK_ENTRY_CONTINUATION_CONFLICT')
        if phase == 'RESUME':
            if not state_present or document['work_state'] != 'ACTIVE' \
                    or continuation['revalidation_status'] != 'COMPLETED':
                raise Denied('WORK_ENTRY_CONTINUATION_CONFLICT')
        elif continuation['revalidation_status'] != 'PENDING':
            raise Denied('WORK_ENTRY_CONTINUATION_CONFLICT')


def _semantic_dirty_state(state):
    paths = state['staged'] + state['unstaged'] + state['untracked']
    if (state['state'] == 'CLEAN' and paths) or (state['state'] == 'DIRTY' and not paths):
        raise Denied('WORK_PROTOCOL_DIRTY_STATE_CONFLICT')


def _semantic_workspace_state(workspace):
    state = workspace['dirty_state']['state']
    attribution = workspace['dirtiness_attribution']
    _semantic_dirty_state(workspace['dirty_state'])
    if ((state == 'CLEAN') != (attribution == 'NONE')
            or (state == 'UNKNOWN') != (attribution == 'UNKNOWN')):
        raise Denied('WORK_PROTOCOL_ATTRIBUTION_CONFLICT')


def _semantic_continuation(continuation):
    invocation = continuation['in_flight_invocation']
    if (invocation['disposition'] == 'NONE') != (invocation['attribution'] == 'NONE'):
        raise Denied('WORK_PROTOCOL_CONTINUATION_CONFLICT')


def _semantic_result(document):
    state_present = 'work_state' in document
    if state_present != ('priority' in document):
        raise Denied('WORK_RESULT_PRIORITY_CONFLICT')
    _semantic_dirty_state(document['starting_dirty_state'])
    _semantic_dirty_state(document['ending_dirty_state'])
    workspaces = document['workspace_evidence']
    if workspaces['isolated_execution'] == (
            workspaces['source_workspace_identity'] == workspaces['execution_workspace_identity']):
        raise Denied('WORK_RESULT_WORKSPACE_CONFLICT')
    if document['starting_head'] != document['canonical_baseline']['resolved_head']:
        raise Denied('WORK_RESULT_WORKSPACE_CONFLICT')
    continuation = document.get('continuation')
    if state_present and document['work_state'] == 'PAUSED':
        if continuation is None:
            raise Denied('WORK_RESULT_CONTINUATION_CONFLICT')
    elif continuation is not None:
        raise Denied('WORK_RESULT_CONTINUATION_CONFLICT')
    if continuation is not None:
        _semantic_continuation(continuation)
        if continuation['work_entry_id'] != document['work_entry_id'] \
                or continuation['mutation_gate_at_handoff'] != 'CLOSED' \
                or continuation['revalidation_status'] != 'PENDING':
            raise Denied('WORK_RESULT_CONTINUATION_CONFLICT')
    discovery = document.get('discovery_coverage')
    if discovery is not None:
        if discovery['recheck_status'] == 'COMPLETED' and not discovery['recheck_evidence']:
            raise Denied('WORK_RESULT_DISCOVERY_CONFLICT')
        if discovery['recheck_status'] != 'COMPLETED' and discovery['recheck_evidence']:
            raise Denied('WORK_RESULT_DISCOVERY_CONFLICT')
        if state_present and document['work_state'] == 'COMPLETE' \
                and (discovery['actionable_findings_remaining']
                     or discovery['recheck_status'] == 'PENDING'):
            raise Denied('WORK_RESULT_DISCOVERY_CONFLICT')
    attribution = document['ending_dirtiness_attribution']
    for bucket in ('staged', 'unstaged', 'untracked'):
        classified = [path for category in attribution.values() for path in category[bucket]]
        if len(classified) != len(set(classified)) \
                or set(classified) != set(document['ending_dirty_state'][bucket]):
            raise Denied('WORK_RESULT_DIRTINESS_ACCOUNTING_CONFLICT')
    nodes = document['status_topology']['nodes']
    identifiers = [node['id'] for node in nodes]
    if len(identifiers) != len(set(identifiers)):
        raise Denied('WORK_RESULT_DUPLICATE_NODE')
    by_id = {node['id']: node for node in nodes}
    priorities = ['priority' in node for node in nodes]
    if any(priorities) and not all(priorities):
        raise Denied('WORK_RESULT_PRIORITY_CONFLICT')
    for node in nodes:
        if node['status'] in ('COMPLETED', 'PAUSED', 'PARKED', 'NON_BLOCKING_INCOMPLETE') \
                and node['blocking']:
            raise Denied('WORK_RESULT_BLOCKING_CONFLICT')
        if node['status'] == 'BLOCKED' and not node['blocking']:
            raise Denied('WORK_RESULT_BLOCKING_CONFLICT')
        if node['kind'] == 'AUTHORIZATION' and node['status'] != 'AUTHORIZATION_REQUIRED':
            raise Denied('WORK_RESULT_AUTHORITY_CONFLICT')
    for relation in document['status_topology']['relationships']:
        if relation['subject'] not in by_id or relation['object'] not in by_id:
            raise Denied('WORK_RESULT_RELATION_UNKNOWN_NODE')
        subject = by_id[relation['subject']]
        if relation['predicate'] == 'BLOCKED_BY' and subject['status'] != 'BLOCKED':
            raise Denied('WORK_RESULT_RELATION_CONFLICT')
        if relation['predicate'] == 'NON_BLOCKING_FOR' and subject['status'] != 'NON_BLOCKING_INCOMPLETE':
            raise Denied('WORK_RESULT_RELATION_CONFLICT')
        if relation['predicate'] == 'REQUIRES_AUTHORIZATION_FROM' and subject['status'] != 'AUTHORIZATION_REQUIRED':
            raise Denied('WORK_RESULT_RELATION_CONFLICT')
        if relation['predicate'] == 'MAY_BE_RESOLVED_BY' and subject['status'] != 'UNKNOWN':
            raise Denied('WORK_RESULT_RELATION_CONFLICT')
        if relation['predicate'] == 'HANDOFF_TO' and subject['kind'] != 'CROSS_CONTROL_PLANE_REQUEST':
            raise Denied('WORK_RESULT_RELATION_CONFLICT')
        if relation['predicate'] == 'PROMOTED_TO':
            target = by_id[relation['object']]
            if subject['kind'] != 'FINDING' or target['kind'] != 'FUTURE_WORK' \
                    or target['status'] != 'PARKED':
                raise Denied('WORK_RESULT_RELATION_CONFLICT')


def validate(kind, raw, root=ROOT):
    if kind not in PROTOCOLS or has_indicator(raw):
        raise Denied('WORK_PROTOCOL_NONCONFORMANCE')
    document = load(raw)
    schema = schemas(root)[kind]
    if not isinstance(document, dict) or not Draft202012Validator(schema).is_valid(document):
        raise Denied('WORK_PROTOCOL_NONCONFORMANCE')
    if kind == 'entry':
        _semantic_entry(document)
    else:
        _semantic_result(document)
    expected, _ = PROTOCOLS[kind]
    if document['protocol'] != expected:
        raise Denied('WORK_PROTOCOL_NONCONFORMANCE')
    return {
        'schema_version': 1,
        'protocol': expected,
        'invariant_id': CLEAN_EXECUTION_BASELINE,
        'work_entry_id': document['work_entry_id'],
        'status': 'PASS',
        'automatic_execution': False,
        'mutation_authorized': False,
        'live_mutation': 'NONE',
        **({'work_state': document['work_state'], 'priority': document['priority']}
           if 'work_state' in document else {}),
        **({'scheduling_eligibility': document['scheduling_eligibility']}
           if 'scheduling_eligibility' in document else {}),
        **({'continuation_ready': True} if document.get('continuation') else {}),
        **({'mutation_gate': document['execution_workspace']['mutation_gate']}
           if kind == 'entry' else {'ending_dirtiness_accounted': True}),
    }
