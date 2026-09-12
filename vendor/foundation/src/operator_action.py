"""Pure operator-action validation and deterministic terminal rendering; never execution."""
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MAX_INPUT_BYTES = 131072
SCHEMA = json.loads((ROOT / 'schemas/operator-action-v1.schema.json').read_text())
VALIDATOR = Draft202012Validator(SCHEMA)


class OperatorActionError(ValueError):
    """Public reason codes never contain rejected input."""


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise OperatorActionError('DUPLICATE_FIELD')
        result[key] = value
    return result


def _constant(_value):
    raise OperatorActionError('INVALID_JSON')


def load_action(raw):
    """Load bounded UTF-8 JSON, rejecting duplicate keys and nonfinite numbers."""
    if not isinstance(raw, bytes) or len(raw) > MAX_INPUT_BYTES:
        raise OperatorActionError('INPUT_SIZE_OR_TYPE')
    try:
        return json.loads(raw.decode('utf-8'), object_pairs_hook=_pairs,
                          parse_constant=_constant)
    except OperatorActionError:
        raise
    except (ValueError, RecursionError):
        raise OperatorActionError('INVALID_JSON') from None


def _safe_values(value):
    # Fullmatch also rejects trailing LF (JSON Schema's $ may match before LF).
    if isinstance(value, str):
        if re.fullmatch(r'[ -~]+', value) is None or not value.strip():
            raise OperatorActionError('UNSAFE_TEXT')
    elif isinstance(value, dict):
        for key, item in value.items():
            _safe_values(key)
            _safe_values(item)
    elif isinstance(value, list):
        for item in value:
            _safe_values(item)


def validate_action(action, *, expected_source):
    """Compare caller-supplied independent pins; this does not authenticate them."""
    try:
        _safe_values(action)
        if not VALIDATOR.is_valid(action):
            raise OperatorActionError('SCHEMA_NONCONFORMANCE')
        if type(action['schema_version']) is not int:
            raise OperatorActionError('SCHEMA_NONCONFORMANCE')
        if (not isinstance(expected_source, dict)
                or set(expected_source) != {'repository_revision', 'doctrine_revision'}
                or any(not isinstance(v, str) or re.fullmatch(r'[0-9a-f]{40}', v) is None
                       for v in expected_source.values())):
            raise OperatorActionError('SOURCE_PIN_REQUIRED')
        if action['source'] != expected_source:
            raise OperatorActionError('SOURCE_PIN_MISMATCH')
    except RecursionError:
        raise OperatorActionError('INVALID_STRUCTURE') from None
    return {'status': 'DECLARATION_CONFORMANT', 'execution_occurred': False,
            'mutation_authorized': False, 'live_acceptance': False}


def render_action(action, *, expected_source):
    """Validate everything before returning any output. Input remains unchanged."""
    validate_action(action, expected_source=expected_source)
    lines = ['HELIX_OPERATOR_ACTION_CONTRACT_V1 1.0.0',
             'DECLARATION ONLY: independent review and authorization required.']
    for key in ('repository', 'target', 'operation', 'phase', 'status'):
        lines.append(key.upper() + ': ' + action[key])
    for key in ('repository_revision', 'doctrine_revision'):
        lines.append('FOUNDATION_' + key.upper() + ': ' + action['source'][key])
    lines.append('STOP_REASON: ' + (action['stop_reason'] or 'NONE'))
    for key in ('evidence', 'scope', 'effects', 'risks', 'downtime', 'removals',
                'preconditions', 'success_evidence', 'failure_evidence', 'recovery',
                'rollback', 'return_output'):
        lines.append(key.upper() + ':')
        lines.extend('  - ' + item for item in (action[key] or ['NONE']))
    command = action['command']
    if command is None:
        lines.append('COMMAND: NONE')
    else:
        lines.extend(['COMMAND_SHELL: ' + command['shell'],
                      'COMMAND_WORKING_DIRECTORY: ' + command['working_directory'],
                      'COMMAND (copy only the next line; review before execution):',
                      command['text']])
    lines.extend(['EXECUTION_OCCURRED: NO', 'MUTATION_AUTHORIZED: NO'])
    return '\n'.join(lines) + '\n'
