"""Bounded supplied-public-data attribution pilot; no runtime Git or discovery."""
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator
from .safety import has_indicator

MAX_INPUT = 16 * 1024 * 1024
MAX_MESSAGE = 128 * 1024
VERSION = 'attribution-pilot/1'
ERROR = 'BLOCKER=REPO_CP_NONCONFORMANCE\n'
# Only installed schema bytes are read. No input can nominate a path or URL.
SCHEMA_BYTES = (Path(__file__).resolve().parents[2] /
                'schemas/contribution-attribution-v1.schema.json').read_bytes()
SCHEMA = json.loads(SCHEMA_BYTES)
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA)
DEFINITIONS = {k: Draft202012Validator({'$defs': SCHEMA['$defs'], '$ref': '#/$defs/' + k})
               for k in ('actor', 'model', 'claim', 'work')}
BIDI = set(range(0x202a, 0x202f)) | set(range(0x2066, 0x206a)) | {0x061c, 0x200e, 0x200f}
TRAILER = re.compile(r'([A-Za-z0-9-]+): (.*)\Z')
MARKER = re.compile(r'^[ \t]*attribution-', re.I | re.M)


class Invalid(ValueError):
    """Constant, non-disclosing reason only."""


def fail(code='INVALID_METADATA'):
    raise Invalid(code)


def dumps(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False)


def pairs(items):
    out = {}
    for key, value in items:
        if key in out:
            fail()
        out[key] = value
    return out


def integer(token):
    if len(token.lstrip('-')) > 19:
        fail()
    value = int(token)
    if not -(2 ** 63) <= value < 2 ** 63:
        fail()
    return value


def no_number(_):
    fail()


def strings(value, depth=0, message=False):
    if depth > 12:
        fail()
    if isinstance(value, str):
        if len(value) > (MAX_MESSAGE if message else 2048):
            fail()
        for c in value:
            n = ord(c)
            if 0xd800 <= n <= 0xdfff or n in BIDI or n == 127 or (n < 32 and not (message and c == '\n')):
                fail()
        if has_indicator(value.encode('utf-8')):
            fail()
    elif isinstance(value, dict):
        for k, v in value.items():
            strings(k, depth + 1)
            strings(v, depth + 1, k == 'message')
    elif isinstance(value, list):
        for v in value:
            strings(v, depth + 1)


def load(raw, limit=MAX_INPUT):
    if type(raw) is not bytes or len(raw) > limit:
        fail()
    try:
        text = raw.decode('utf-8')
        # Bound container depth before handing the input to the JSON decoder.
        depth, quoted, escape = 0, False, False
        for c in text:
            if quoted:
                if escape:
                    escape = False
                elif c == '\\':
                    escape = True
                elif c == '"':
                    quoted = False
            elif c == '"':
                quoted = True
            elif c in '[{':
                depth += 1
                if depth > 12:
                    fail()
            elif c in ']}':
                depth -= 1
        result = json.loads(text, object_pairs_hook=pairs, parse_int=integer,
                            parse_float=no_number, parse_constant=no_number)
        strings(result)
        return result
    except (ValueError, UnicodeError, RecursionError, OverflowError):
        fail()


def valid(kind, data):
    validator = VALIDATOR if kind == 'input' else DEFINITIONS[kind]
    if next(validator.iter_errors(data), None) is not None:
        fail()


def index(items):
    out = {}
    for item in items:
        if item['id'] in out:
            fail('DUPLICATE_ID')
        out[item['id']] = item
    return out


def scope_key(scope, commit):
    if scope['kind'] == 'work':
        t = scope['target']
        return ('work', t['repository']['id'], t['id'], t['revision'])
    t = scope['target']
    return ('commit', commit['repository_id'], commit['oid']) if t == 'self' else (
        'commit', t['repository']['id'], t['oid'])


def unknown_claim(c):
    p, v = c['predicate'], c['value']
    if p == 'participation':
        return v['present'] is None
    if p == 'coverage':
        return v == 'unknown'
    if p in ('responsibility', 'identity-binding', 'descriptor-field'):
        return v is None if p != 'descriptor-field' else v['expected'] is None
    if p == 'authorization':
        return v['decision'] is None
    if p == 'provenance':
        return v['source'] is None
    if p == 'signature':
        return v['valid'] is None
    if p == 'commit-execution':
        return all(v[k] is None for k in ('executor', 'mechanism', 'acting_principal'))
    return False


def parse_record(commit):
    message = commit['message']
    if len(message.encode('utf-8')) > MAX_MESSAGE:
        fail()
    if not MARKER.search(message):
        return None
    text = message[:-1] if message.endswith('\n') else message
    if '\n\n' not in text:
        fail()
    body, block = text.rsplit('\n\n', 1)
    if MARKER.search(body):
        fail()
    groups = defaultdict(list)
    occurrences = defaultdict(list)
    for position, line in enumerate(block.split('\n'), 1):
        match = TRAILER.fullmatch(line)
        if not match:
            fail()
        key, value = match.groups()
        key = key.lower()
        if not key.startswith('attribution-'):
            continue
        if len(line.encode('utf-8')) > 8192:
            fail()
        if key not in ('attribution-version', 'attribution-work', 'attribution-actor',
                       'attribution-model', 'attribution-claim'):
            fail()
        groups[key].append((position, value))
    if len(groups['attribution-version']) != 1 or len(groups['attribution-work']) > 1:
        fail()
    if groups['attribution-version'][0][1] != '1':
        fail('UNSUPPORTED_VERSION')
    parsed = {}
    for kind, maximum in [('actor', 32), ('model', 32), ('claim', 128), ('work', 1)]:
        entries = groups['attribution-' + kind]
        if len(entries) > maximum:
            fail()
        result = {}
        for pos, value in entries:
            data = load(value.encode('utf-8'), 8192)
            if kind == 'claim' and isinstance(data, dict):
                evidence = data.get('evidence', [])
                if isinstance(evidence, list) and any(isinstance(e, dict) and e.get('state') in
                                                      ('observed', 'verified') for e in evidence):
                    fail('UNSUPPORTED_EVIDENCE_STATE')
            valid(kind, data)
            key = data.get('id', 'work')
            if key in result and result[key] != data:
                fail('CONFLICTING_ID')
            result[key] = data
            occurrences[kind + ':' + key].append(pos)
        parsed[kind] = result
    actors, models, claims = parsed['actor'], parsed['model'], parsed['claim']
    if set(actors) & set(models) or 'record' in actors or 'record' in models:
        fail('CONFLICTING_ID')
    for actor in actors.values():
        if actor['kind'] == 'human' and (actor['tool'] is not None or actor['models']):
            fail()
        if any(m not in models for m in actor['models']):
            fail()
    for model in models.values():
        fields = ('provider', 'model_id', 'tag', 'resolved_digest', 'revision', 'quantization')
        if set(model['unavailable']) != {k for k in fields if model[k] is None}:
            fail()
    executors = []
    for c in claims.values():
        p, v, subject = c['predicate'], c['value'], c['subject']
        if p in ('participation', 'responsibility', 'identity-binding', 'authorization'):
            if subject not in actors:
                fail()
        elif p == 'descriptor-field':
            descriptor = actors.get(subject, models.get(subject))
            field = v['pointer'][1:]
            if descriptor is None or field not in descriptor or not isinstance(descriptor[field], (str, type(None))):
                fail()
            if descriptor[field] != v['expected']:
                fail('CLAIM_CONFLICT')
        elif subject != 'record':
            fail()
        if p in ('git-header', 'signature', 'commit-execution') and c['scope']['kind'] != 'commit':
            fail()
        if p == 'authorization' and c['scope']['target'] == 'self':
            fail()
        if p == 'commit-execution':
            executors.append(c)
            if c['scope']['target'] != 'self' or (v['executor'] is not None and v['executor'] not in actors):
                fail()
            if set(v['unknown']) != {k for k in ('executor', 'mechanism', 'acting_principal') if v[k] is None}:
                fail()
        for e in c['evidence']:
            if e['claim'] != c['id'] or (e['state'] == 'declared' and e['by'] not in actors):
                fail()
            if (e['state'] == 'unknown') != unknown_claim(c):
                fail()
    if len(executors) != 1:
        fail('EXECUTOR_REQUIRED')
    return {'actors': list(actors.values()), 'models': list(models.values()),
            'claims': list(claims.values()), 'work': next(iter(parsed['work'].values()), None),
            'occurrences': dict(occurrences), 'executor': executors[0]['value']}


def safe_work(commit):
    """Recover only a structurally valid work link; never echo rejected trailers."""
    message = commit['message'].removesuffix('\n')
    if '\n\n' not in message:
        return None
    body, block = message.rsplit('\n\n', 1)
    if MARKER.search(body):
        return None
    values = []
    for line in block.split('\n'):
        match = TRAILER.fullmatch(line)
        if match and match[1].lower() == 'attribution-work':
            values.append(match[2])
    if len(values) != 1:
        return None
    try:
        work = load(values[0].encode('utf-8'), 8192)
        valid('work', work)
        return work
    except Invalid:
        return None


def check_profile(check):
    fields = {}
    for key, expected in check['expected'].items():
        observed = check['observed'][key]
        if expected is None or observed is None:
            fields[key] = 'UNKNOWN'
        else:
            if key.endswith('_destinations'):
                expected, observed = sorted(set(expected)), sorted(set(observed))
            fields[key] = 'MATCH' if expected == observed else 'MISMATCH'
    status = 'MISMATCH' if 'MISMATCH' in fields.values() else 'UNKNOWN' if 'UNKNOWN' in fields.values() else 'MATCH'
    return {'id': check['id'], 'repository_id': check['repository_id'], 'status': status,
            'fields': fields, 'findings': ['PROFILE_MISMATCH'] if status == 'MISMATCH' else [],
            'authority_effect': 'NONE'}


def binding_map(parsed, commit, registry):
    principals = {p['id']: p for p in registry['principals']}
    bindings = {b['id']: b for b in registry['git_identity_bindings']}
    mapping, findings = {}, []
    for actor in parsed['actors']:
        mapping[actor['id']] = 'actor:' + dumps([commit['repository_id'], commit['oid'], actor['id']])
        requests = [c for c in parsed['claims'] if c['predicate'] == 'identity-binding' and c['subject'] == actor['id']]
        resolved = set()
        actor_unresolved = False
        for c in requests:
            v = c['value']
            b = bindings.get(v['binding_id']) if v else None
            if (not b or v['registry_revision'] != registry['source_revision'] or
                    commit['repository_id'] not in b['repository_ids'] or
                    actor['principal'] not in (None, b['principal_id']) or
                    principals[b['principal_id']]['kind'] != actor['kind']):
                findings.append('IDENTITY_UNRESOLVED')
                actor_unresolved = True
                continue
            matches = [x for x in bindings.values() if x['name'] == b['name'] and x['email'] == b['email']
                       and commit['repository_id'] in x['repository_ids']]
            if len(matches) != 1:
                actor_unresolved = True
                findings.append('IDENTITY_UNRESOLVED')
            else:
                resolved.add(b['principal_id'])
        if len(resolved) == 1 and len(requests) > 0 and not actor_unresolved:
            mapping[actor['id']] = 'principal:' + next(iter(resolved))
        elif len(resolved) > 1:
            findings.append('IDENTITY_UNRESOLVED')
    return mapping, findings


def known_value(c):
    v = c['value']
    if unknown_claim(c):
        return None
    if isinstance(v, dict):
        return {k: x for k, x in v.items() if x is not None and k != 'unknown'}
    return v


def conflicts(entries):
    seen = defaultdict(dict)
    for entry in entries:
        c = entry['claim']
        if c['predicate'] == 'provenance':
            continue
        v = known_value(c)
        if v is None:
            continue
        discriminator = ''
        if isinstance(c['value'], dict):
            field = {'participation': 'role', 'descriptor-field': 'pointer',
                     'git-header': 'field', 'authorization': 'action',
                     'identity-binding': 'binding_id', 'signature': 'signer_reference'}.get(c['predicate'])
            if field:
                discriminator = c['value'].get(field)
        key = (entry['actor'], c['predicate'], discriminator)
        fields = v if isinstance(v, dict) else {'value': v}
        for field, value in fields.items():
            if field in seen[key] and seen[key][field] != value:
                return True
            seen[key][field] = value
    return False


def classify(entries):
    if conflicts(entries):
        return {'classification': 'unclassifiable', 'findings': ['CLAIM_CONFLICT'],
                'participation': [], 'exclusive': 'unknown', 'roles': [], 'non_additive': True}
    positive, unresolved, negative = {}, set(), set()
    complete = any(e['claim']['predicate'] == 'coverage' and e['claim']['value'] == 'complete' for e in entries)
    for e in entries:
        c = e['claim']
        if c['predicate'] != 'participation':
            continue
        key = (e['actor'], c['value']['role'])
        if c['value']['present'] is True:
            if key in positive:
                positive[key]['models'] = sorted(set(positive[key]['models']) | set(e['models']))
            else:
                positive[key] = dict(e)
        elif c['value']['present'] is None:
            unresolved.add(key)
        else:
            negative.add(key)
    unresolved -= positive.keys() | negative
    kinds = {e['kind'] for e in positive.values()}
    classification = 'undetermined'
    if {'human', 'agent'} <= kinds:
        classification = 'mixed'
    elif complete and not unresolved and kinds in ({'human'}, {'agent'}):
        classification = 'human-only' if kinds == {'human'} else 'agent-only'
    people = {key[0] for key in positive}
    exclusive = 'shared' if len(people) > 1 else 'exclusive' if complete and len(people) == 1 and not unresolved else 'unknown'
    roles = []
    for role in sorted({key[1] for key in positive}):
        actors = sorted({key[0] for key in positive if key[1] == role})
        status = ('shared' if len(actors) > 1 else 'exclusive'
                  if complete and not any(k[1] == role for k in unresolved) else 'unknown')
        roles.append({'role': role, 'actors': actors, 'participation': status})
    return {'classification': classification, 'findings': [], 'exclusive': exclusive,
            'coverage': 'declared-complete' if complete else 'incomplete', 'roles': roles,
            'participation': [{'actor': a, 'role': r, 'kind': e['kind'], 'models': e['models']}
                              for (a, r), e in sorted(positive.items())], 'non_additive': True}


def observation(claim, method, reference, timestamp, value):
    return {'claim': claim, 'state': 'observed', 'by': VERSION, 'method': method,
            'ref': reference, 'at': timestamp, 'value': value}


def totals(rows):
    counts = Counter(row['classification'] for row in rows)
    return {key: counts[key] for key in ('human-only', 'agent-only', 'mixed', 'undetermined', 'unclassifiable')}


def participation_views(rows):
    """Each actor/model/role/kind counts at most once per scope, never add views."""
    views = {k: Counter() for k in ('actors', 'models', 'roles', 'kinds')}
    for row in rows:
        entries = row['participation']
        views['actors'].update({e['actor'] for e in entries})
        views['models'].update({m for e in entries for m in e['models']})
        views['roles'].update({e['role'] for e in entries})
        views['kinds'].update({e['kind'] for e in entries})
    return {**{k: dict(sorted(v.items())) for k, v in views.items()}, 'non_additive': True}


def report(raw):
    data = load(raw)
    valid('input', data)
    # jsonschema considers 1.0 an integer; the parser rejects all floats first.
    datetime.strptime(data['captured_at'], '%Y-%m-%dT%H:%M:%SZ')
    registry = data['registry']
    principals = index(registry['principals'])
    index(registry['git_identity_bindings'])
    index(data['profile_checks'])
    if any(b['principal_id'] not in principals for b in registry['git_identity_bindings']):
        fail()
    grouped = defaultdict(list)
    for n, commit in enumerate(data['commits']):
        grouped[(commit['repository_id'], commit['oid'])].append((n, commit))
    rows, aggregates, exclusions = [], defaultdict(list), Counter()
    work_keys, entry_sources = set(), defaultdict(set)
    unresolved = False
    for key, sources in sorted(grouped.items()):
        n, commit = sources[0]
        row = {'repository_id': key[0], 'oid': key[1], 'input_occurrences': [x[0] for x in sources],
               'integration': len(commit['parents']) >= 2, 'status': 'valid', 'findings': [],
               'work': None, 'actors': [], 'models': [], 'claims': [], 'observations': [],
               'executor': None, 'occurrences': {}}
        row['work'] = safe_work(commit)
        if row['work']:
            w = row['work']
            work_keys.add(('work', w['repository']['id'], w['id'], w['revision']))
        try:
            if any(c != commit for _, c in sources):
                fail('OBJECT_CONFLICT')
            parsed = parse_record(commit)
            if parsed is None:
                row['status'] = 'missing'
                row['findings'] = ['ATTRIBUTION_MISSING']
                unresolved = True
            else:
                row.update({k: parsed[k] for k in ('work', 'executor', 'occurrences')})
                if parsed['work']:
                    w = parsed['work']
                    work_keys.add(('work', w['repository']['id'], w['id'], w['revision']))
                mapping, findings = binding_map(parsed, commit, registry)
                row['findings'].extend(findings)
                actor_table = {a['id']: a for a in parsed['actors']}
                local = defaultdict(list)
                for c in parsed['claims']:
                    actor = actor_table.get(c['subject'])
                    entry = {'claim': c, 'actor': mapping[c['subject']] if actor else c['subject'],
                             'kind': actor['kind'] if actor else None,
                             'models': sorted({'model:' + dumps([key[0], key[1], m]) for m in actor['models']}) if actor else [],
                             'source': [key[0], key[1], c['id']]}
                    sk = scope_key(c['scope'], commit)
                    local[sk].append(entry)
                    if sk[0] == 'work':
                        work_keys.add(sk)
                if any(conflicts(items) for items in local.values()):
                    fail('CLAIM_CONFLICT')
                for sk, entries in local.items():
                    aggregates[sk].extend(entries)
                    entry_sources[sk].add(key)
                for k in ('actors', 'models', 'claims'):
                    row[k] = sorted(parsed[k], key=lambda x: x['id'])
                unresolved |= bool(findings) or any(unknown_claim(c) for c in parsed['claims']) or bool(parsed['executor']['unknown'])
                unresolved |= any(a['kind'] == 'unknown' or (a['kind'] == 'agent' and not a['models']) for a in parsed['actors'])
                unresolved |= any(bool(m['unavailable']) for m in parsed['models'])
            for field in ('author', 'committer'):
                matches = [b for b in registry['git_identity_bindings'] if
                           b['name'] == commit[field]['name'] and b['email'] == commit[field]['email'] and
                           key[0] in b['repository_ids']]
                value = {'binding_id': None, 'principal_id': None, 'status': 'UNKNOWN'}
                if len(matches) == 1:
                    b = matches[0]
                    value = {'binding_id': b['id'], 'principal_id': b['principal_id'],
                             'status': 'DECLARED_MATCH', 'binding_source_status': b['source_status'],
                             'principal_source_status': principals[b['principal_id']]['source_status']}
                else:
                    unresolved = True
                row['observations'].append(observation(field, 'match-supplied-git-identity-v1',
                    'input:commits/' + str(n) + '/' + field, data['captured_at'], value))
        except Invalid as error:
            code = str(error)
            row['status'] = 'unsupported' if code in ('UNSUPPORTED_VERSION', 'UNSUPPORTED_EVIDENCE_STATE') else 'invalid'
            row['findings'] = [code]
            # Do not expose any rejected metadata; retain only an already validated work link.
            for k in ('actors', 'models', 'claims', 'observations'):
                row[k] = []
            row['executor'], row['occurrences'] = None, {}
            if row['work']:
                w = row['work']
                exclusions[('work', w['repository']['id'], w['id'], w['revision'])] += 1
            else:
                exclusions[('unlinked',)] += 1
        rows.append(row)
    conflicted_commits = {sk for sk, entries in aggregates.items()
                          if sk[0] == 'commit' and conflicts(entries)}
    rejected_sources = set()
    for sk in conflicted_commits:
        rejected_sources.update(tuple(e['source'][:2]) for e in aggregates[sk])
    for row in rows:
        key = (row['repository_id'], row['oid'])
        if key in rejected_sources:
            row['status'] = 'invalid'
            row['findings'] = sorted(set(row['findings'] + ['CLAIM_CONFLICT']))
            row['claims'], row['actors'], row['models'], row['observations'] = [], [], [], []
            row['executor'], row['occurrences'] = None, {}
            if row['work']:
                w = row['work']
                exclusions[('work', w['repository']['id'], w['id'], w['revision'])] += 1
            else:
                exclusions[('unlinked',)] += 1
    if rejected_sources:
        for sk in aggregates:
            aggregates[sk] = [e for e in aggregates[sk] if tuple(e['source'][:2]) not in rejected_sources]
            entry_sources[sk] -= rejected_sources
    for row in rows:
        sk = ('commit', row['repository_id'], row['oid'])
        summary = classify(aggregates[sk])
        if row['status'] in ('invalid', 'unsupported'):
            summary = classify([])
            summary['classification'] = 'unclassifiable'
        if sk in conflicted_commits:
            summary['classification'] = 'unclassifiable'
            summary['findings'] = ['CLAIM_CONFLICT']
        if summary['findings']:
            row['status'] = 'invalid'
        row['findings'] = sorted(set(row['findings'] + summary.pop('findings')))
        row.update(summary)
    works = []
    for sk in sorted(work_keys):
        summary = classify(aggregates[sk])
        # A known excluded source prevents an exclusive/completeness conclusion.
        if exclusions[sk]:
            summary['coverage'] = 'incomplete-excluded-sources'
            if summary['classification'] in ('human-only', 'agent-only'):
                summary['classification'] = 'undetermined'
            if summary['exclusive'] == 'exclusive':
                summary['exclusive'] = 'unknown'
            for role in summary['roles']:
                if role['participation'] == 'exclusive':
                    role['participation'] = 'unknown'
        works.append({'repository_id': sk[1], 'work_id': sk[2], 'revision': sk[3],
                      'sources': [list(k) for k in sorted(entry_sources[sk])],
                      'excluded_sources': exclusions[sk],
                      'claims': sorted(aggregates[sk], key=lambda e: e['source']), **summary})
    profiles = sorted((check_profile(c) for c in data['profile_checks']), key=lambda c: c['id'])
    invalid = any(r['status'] in ('invalid', 'unsupported') for r in rows) or any(w['findings'] for w in works) or any(p['status'] == 'MISMATCH' for p in profiles)
    uncertain = unresolved or any(r['classification'] == 'undetermined' for r in rows + works) or any(p['status'] == 'UNKNOWN' for p in profiles)
    status = 2 if invalid else 1 if uncertain else 0
    result = {'schema_version': 1, 'reporter': VERSION, 'schema_sha256': hashlib.sha256(SCHEMA_BYTES).hexdigest(),
              'input_sha256': hashlib.sha256(raw).hexdigest(), 'captured_at': data['captured_at'],
              'registry': {'source_repository_id': registry['source_repository_id'],
                           'source_revision': registry['source_revision'], 'principals': registry['principals']},
              'commits': rows, 'works': works, 'profile_checks': profiles,
              'totals': {'commits': totals(rows), 'works': totals(works),
                         'commit_participation_views': participation_views(rows),
                         'work_participation_views': participation_views(works),
                         'record_status': dict(sorted(Counter(r['status'] for r in rows).items())),
                         'unique_objects': len({r['oid'] for r in rows}), 'repository_occurrences': len(rows),
                         'integration_commits': sum(r['integration'] for r in rows),
                         'work_entries': len({k[1:3] for k in work_keys}), 'work_scopes': len(work_keys),
                         'unlinked_commits': sum(r['work'] is None for r in rows),
                         'unlinked_invalid_sources': exclusions[('unlinked',)],
                         'executor': dict(sorted(Counter('unknown' if r['executor'] is None or r['executor']['executor'] is None else
                             next(a['kind'] for a in r['actors'] if a['id'] == r['executor']['executor']) for r in rows).items()))},
              'non_additive_participation': True, 'authority_effect': 'NONE', 'exit_status': status}
    return dumps(result) + '\n', status


def main(args, stdin, stdout, stderr):
    try:
        if args:
            fail()
        output, status = report(stdin.read(MAX_INPUT + 1))
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError, OverflowError, OSError):
        stderr.write(ERROR)
        return 2
    stdout.write(output)
    return status
