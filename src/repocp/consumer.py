"""Consume verified Foundation V1 bytes. Never authorize or execute actions."""
import hashlib
import json
from pathlib import Path
import types

from .safety import Denied, has_indicator, load, read_public

ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_REVISION = '999fcf6a4bf181bdba201e9ca0c2f2bc4e7e2af5'
DOCTRINE_REVISION = 'd2fe6c6291ea1eaffadb15ded6c0240fed0e96ca'
SOURCE = {'repository_revision': REPOSITORY_REVISION, 'doctrine_revision': DOCTRINE_REVISION}
ARTIFACTS = {
    'AGENTS.md', 'README.md', 'OWNERSHIP.md', 'PROVENANCE.md', 'VERSION',
    'docs/ACTIVE_DOCTRINE.md', 'registries/active-doctrine.json',
    'contracts/HELIX_OPERATOR_ACTION_CONTRACT_V1.md', 'docs/OPERATOR_ACTION_VALIDATION.md',
    'registries/operator-action.json', 'schemas/operator-action-v1.schema.json',
    'src/operator_action.py', 'tools/render_operator_action.py', 'tests/test_operator_action.py',
    *{'tests/fixtures/operator_action/' + n for n in
      ('ready.json', 'blocked.json', 'invalid-blocked-command.json', 'ready.txt', 'blocked.txt')},
}


def verify(root=ROOT):
    try:
        repo = load(read_public(root, 'pins/foundation-repository.json'))
        doctrine = load(read_public(root, 'pins/foundation-doctrine.json'))
        if (set(repo) != {'schema_version', 'authority', 'remote', 'branch', 'revision',
                         'contract_id', 'contract_version', 'artifacts'}
                or set(doctrine) != {'schema_version', 'authority', 'revision', 'version', 'artifacts'}
                or type(repo['schema_version']) is not int or repo['schema_version'] != 1
                or type(doctrine['schema_version']) is not int or doctrine['schema_version'] != 1
                or repo['revision'] != REPOSITORY_REVISION or doctrine['revision'] != DOCTRINE_REVISION
                or repo['remote'] != 'git@github.com:lhpoulin-cmyk/foundation-cp.git'
                or repo['branch'] != 'main' or repo['authority'] != 'foundation-cp'
                or doctrine['authority'] != 'foundation-cp' or doctrine['version'] != '1.0.0'
                or repo['contract_id'] != 'HELIX_OPERATOR_ACTION_CONTRACT_V1'
                or repo['contract_version'] != '1.0.0' or set(repo['artifacts']) != ARTIFACTS
                or set(doctrine['artifacts']) != {'docs/ACTIVE_DOCTRINE.md', 'registries/active-doctrine.json', 'VERSION'}):
            raise Denied('FOUNDATION_PIN_INVALID')
        artifacts = {}
        for name in sorted(ARTIFACTS):
            raw = read_public(root, 'vendor/foundation/' + name)
            digest = hashlib.sha256(raw).hexdigest()
            if digest != repo['artifacts'][name] or (name in doctrine['artifacts'] and digest != doctrine['artifacts'][name]):
                raise Denied('FOUNDATION_ARTIFACT_MISMATCH')
            artifacts[name] = raw
        registry = load(artifacts['registries/operator-action.json'])
        if registry['contract_id'] != repo['contract_id'] or registry['contract_version'] != repo['contract_version']:
            raise Denied('FOUNDATION_REGISTRY_MISMATCH')
        return artifacts
    except (KeyError, TypeError):
        raise Denied('FOUNDATION_PIN_INVALID') from None


def reference(root=ROOT):
    artifacts = verify(root)
    name = str(Path(root).absolute() / 'vendor/foundation/src/operator_action.py')
    module = types.ModuleType('verified_foundation_operator_action')
    module.__file__ = name
    # Execute only the reviewed, verified implementation bytes, never action text.
    exec(compile(artifacts['src/operator_action.py'], name, 'exec'), module.__dict__)
    if module.SCHEMA != load(artifacts['schemas/operator-action-v1.schema.json']):
        raise Denied('FOUNDATION_ARTIFACT_MISMATCH')
    return module


def render(raw, root=ROOT):
    module = reference(root)
    try:
        action = module.load_action(raw)
        # Producer-side heuristic only; this is not an extension of V1 doctrine.
        if has_indicator(raw) or has_indicator(json.dumps(action, ensure_ascii=True).encode()):
            raise Denied('SECRET_INDICATOR')
        return module.render_action(action, expected_source=SOURCE)
    except module.OperatorActionError:
        raise Denied('OPERATOR_ACTION_NONCONFORMANCE') from None
