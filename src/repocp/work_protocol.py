"""Validate bounded work contracts; never execute, authorize, discover or write."""
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from .consumer import ROOT
from .safety import Denied, has_indicator, load, read_public

PROTOCOLS = {
    'entry': ('HELIX_WORK_ENTRY_V1', 'schemas/work-entry-v1.schema.json'),
    'result': ('HELIX_WORK_RESULT_V1', 'schemas/work-result-v1.schema.json'),
}
CLEAN_EXECUTION_BASELINE = 'HELIX_CLEAN_EXECUTION_BASELINE_V1'


def schemas(root=ROOT):
    result = {}
    for kind, (_, path) in PROTOCOLS.items():
        schema = load(read_public(root, path))
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError:
            raise Denied('WORK_PROTOCOL_SCHEMA_INVALID') from None
        result[kind] = schema
    return result


def _semantic_entry(document):
    authority = document['authority']
    if set(authority['granted']) & set(authority['explicitly_not_granted']):
        raise Denied('WORK_ENTRY_AUTHORITY_CONFLICT')
    scope = document['mutation_scope']
    if set(scope['allowed']) & set(scope['prohibited']):
        raise Denied('WORK_ENTRY_SCOPE_CONFLICT')
    identifiers = [item['id'] for item in document['dependencies']]
    if len(identifiers) != len(set(identifiers)):
        raise Denied('WORK_ENTRY_DUPLICATE_DEPENDENCY')
    source = document['source_workspace']
    execution = document['execution_workspace']
    _semantic_workspace_state(source)
    _semantic_workspace_state(execution)
    gate = execution['mutation_gate']
    phase = document['work_entry_phase']
    safe_to_open = ((phase == 'START' and execution['dirty_state']['state'] == 'CLEAN'
                     and execution['dirtiness_attribution'] == 'NONE')
                    or (phase == 'CONTINUE'
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


def _semantic_result(document):
    _semantic_dirty_state(document['starting_dirty_state'])
    _semantic_dirty_state(document['ending_dirty_state'])
    workspaces = document['workspace_evidence']
    if workspaces['isolated_execution'] == (
            workspaces['source_workspace_identity'] == workspaces['execution_workspace_identity']):
        raise Denied('WORK_RESULT_WORKSPACE_CONFLICT')
    if document['starting_head'] != document['canonical_baseline']['resolved_head']:
        raise Denied('WORK_RESULT_WORKSPACE_CONFLICT')
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
    for node in nodes:
        if node['status'] in ('COMPLETED', 'NON_BLOCKING_INCOMPLETE') and node['blocking']:
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
        if relation['predicate'] == 'HANDOFF_TO' and subject['kind'] != 'CROSS_CONTROL_PLANE_REQUEST':
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
        **({'mutation_gate': document['execution_workspace']['mutation_gate']}
           if kind == 'entry' else {'ending_dirtiness_accounted': True}),
    }
