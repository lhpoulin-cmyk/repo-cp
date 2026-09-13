"""Read declared public metadata only. No subprocess, network, discovery or writes."""
import hashlib
from pathlib import Path
import re

from jsonschema import Draft202012Validator

from .consumer import ROOT, SOURCE, verify
from .safety import Denied, has_indicator, load, read_public
from .file_integrity import invariant, inspect_link

STATES = ('PASS', 'DRIFT', 'BLOCKED', 'NOT_APPLICABLE', 'UNKNOWN')
CHECKS = {
    'RC001': 'Foundation consumer integrity',
    'RC002': 'Explicit enrollment or bounded pilot selection',
    'RC003': 'Local checkout branch and immutable revision',
    'RC004': 'Declared public metadata presence',
    'RC005': 'Public metadata digest drift',
    'RC006': 'Public metadata secret indicators',
    'RC007': 'Repository version declaration',
    'RC008': 'B70 handoff separate Foundation pins',
    'RC009': 'Remote publication freshness',
    'RC010': 'Derived auth policy and containing handoff pins',
    'RC011': 'Governed artifact single-link integrity',
}


def registry(root=ROOT):
    invariant(root)
    raw = read_public(root, 'registries/repositories.json')
    data = load(raw)
    def safe(value):
        if isinstance(value, str):
            return re.fullmatch('[ -~]+', value) is not None and bool(value.strip())
        if isinstance(value, dict):
            return all(safe(k) and safe(v) for k, v in value.items())
        if isinstance(value, list):
            return all(safe(v) for v in value)
        return True
    if has_indicator(raw) or not safe(data):
        raise Denied('UNSAFE_REGISTRY')
    schema = load(read_public(root, 'schemas/repository-enrollment-v1.schema.json'))
    if not Draft202012Validator(schema).is_valid(data) or type(data['schema_version']) is not int:
        raise Denied('ENROLLMENT_NONCONFORMANCE')
    names = [r['repository'] for r in data['repositories']]
    if len(names) != len(set(names)):
        raise Denied('DUPLICATE_REPOSITORY')
    for entry in data['repositories']:
        if entry['canonical_remote'] != 'git@github.com:lhpoulin-cmyk/' + entry['repository'] + '.git':
            raise Denied('REPOSITORY_IDENTITY_CONFLICT')
        if entry['state'] != 'ENROLLED' and entry['enrollment_authorization'] is not None:
            raise Denied('ENROLLMENT_AUTHORITY_CONFLICT')
    return data


def head(checkout):
    raw = read_public(checkout, '.git/HEAD', 4096, git_internal=True).decode('ascii').strip()
    if re.fullmatch('[0-9a-f]{40}', raw):
        return None, raw
    if not re.fullmatch(r'ref: refs/heads/[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_-]+)*', raw):
        raise Denied('UNSUPPORTED_GIT_LAYOUT')
    ref = raw[5:]
    try:
        revision = read_public(checkout, '.git/' + ref, 4096, git_internal=True).decode('ascii').strip()
    except Denied:
        packed = read_public(checkout, '.git/packed-refs', git_internal=True).decode('ascii')
        matches = [line.split(' ')[0] for line in packed.splitlines() if line.endswith(' ' + ref)]
        if len(matches) != 1:
            raise Denied('PUBLIC_REVISION_UNAVAILABLE') from None
        revision = matches[0]
    if not re.fullmatch('[0-9a-f]{40}', revision):
        raise Denied('PUBLIC_REVISION_INVALID')
    return ref[len('refs/heads/'):], revision


def result(repository, check, status, reason):
    return {'repository': repository, 'check_id': check, 'status': status, 'reason': reason}


def audit(fleet_root, *, pilot=False, repository=None, root=ROOT):
    verify(root)
    entries = registry(root)['repositories']
    policy = invariant(root)
    selected = [r for r in entries if r['state'] == 'ENROLLED' or
                (pilot and r['state'] == 'PILOT')]
    if repository is not None:
        selected = [r for r in selected if r['repository'] == repository]
        if not selected:
            raise Denied('REPOSITORY_NOT_SELECTED')
    results = [result('repo-cp', 'RC001', 'PASS', 'ACCEPTED_ARTIFACTS_VERIFIED')]
    if not selected:
        results.append(result('repo-cp', 'RC002', 'NOT_APPLICABLE', 'NO_ENROLLED_REPOSITORIES'))
    for entry in selected:
        name = entry['repository']
        checkout = Path(fleet_root) / name
        results.append(result(name, 'RC002', 'PASS', 'PILOT_ONLY' if entry['state'] == 'PILOT' else 'ENROLLED'))
        try:
            branch, revision = head(checkout)
            matched = branch == entry['branch'] and revision == entry['source_revision']
            results.append(result(name, 'RC003', 'PASS' if matched else 'DRIFT',
                                  'REVISION_MATCH' if matched else 'BRANCH_OR_REVISION_CHANGED'))
        except (Denied, UnicodeError):
            results.append(result(name, 'RC003', 'UNKNOWN', 'CHECKOUT_OR_REVISION_UNAVAILABLE'))
        public = {}
        for filename in sorted(entry['files']):
            # Filename never comes from arbitrary target input: schema allowlist.
            status, reason = inspect_link(checkout, filename, protected=True, policy=policy)
            results.append(result(name, 'RC011', status, reason + ':' + filename))
            if status != 'PASS':
                # Never read unsafe input after a metadata-only rejection.
                absent = entry['files'][filename] is None
                results.append(result(name, 'RC004', 'UNKNOWN' if absent else 'BLOCKED',
                                      'PUBLIC_FILE_UNAVAILABLE:' + filename))
                continue
            try:
                raw = read_public(checkout, filename)
            except Denied:
                absent = entry['files'][filename] is None
                results.append(result(name, 'RC004', 'UNKNOWN' if absent else 'BLOCKED',
                                      ('UNPINNED_METADATA_UNAVAILABLE:' if absent else 'PUBLIC_FILE_UNAVAILABLE:') + filename))
                continue
            results.append(result(name, 'RC004', 'PASS', 'PUBLIC_FILE_PRESENT:' + filename))
            if has_indicator(raw):
                results.append(result(name, 'RC006', 'BLOCKED', 'SECRET_INDICATOR'))
                continue
            results.append(result(name, 'RC006', 'PASS', 'NO_INDICATOR:' + filename))
            digest = hashlib.sha256(raw).hexdigest()
            same = digest == entry['files'][filename]
            results.append(result(name, 'RC005', 'PASS' if same else 'DRIFT',
                                  ('DIGEST_MATCH:' if same else 'CONTENT_CHANGED:') + filename))
            # Changed content is never interpreted as accepted public authority.
            if same:
                public[filename] = raw
        version = public.get('VERSION', b'')
        valid = re.fullmatch(rb'[0-9]+\.[0-9]+\.[0-9]+\n?', version) is not None
        results.append(result(name, 'RC007', 'PASS' if valid else 'UNKNOWN',
                              'VERSION_DECLARED' if valid else 'ACCEPTED_VERSION_UNAVAILABLE'))
        if name == 'auth-cp':
            try:
                handoff = load(public['registries/b70-revision-handoff.json'])['foundation']
                same = (handoff['revision'] == SOURCE['repository_revision'] and
                        handoff['doctrine_revision'] == SOURCE['doctrine_revision'])
                results.append(result(name, 'RC008', 'PASS' if same else 'DRIFT',
                                      'HANDOFF_PINS_MATCH' if same else 'HANDOFF_PIN_REVIEW_REQUIRED'))
            except (KeyError, TypeError, Denied):
                results.append(result(name, 'RC008', 'UNKNOWN', 'ACCEPTED_HANDOFF_UNAVAILABLE'))
        elif name == 'ansible-cp':
            results.extend(derived_handoff_checks(public, entries, root))
        else:
            results.append(result(name, 'RC008', 'NOT_APPLICABLE', 'NO_B70_HANDOFF_CHECK'))
        results.append(result(name, 'RC009', 'UNKNOWN', 'OFFLINE_AUDIT_NO_REMOTE_QUERY'))
    return report(results, [r['repository'] for r in selected])


def report(results, repositories):
    results.sort(key=lambda r: (r['repository'], r['check_id'], r['reason']))
    overall = next((s for s in ('BLOCKED', 'DRIFT', 'UNKNOWN') if any(r['status'] == s for r in results)), 'PASS')
    return {'schema_version': 1, 'status': overall, 'scope': 'REPOSITORY_ONLY',
            'automatic_execution': False, 'live_mutation': 'NONE',
            'repositories_audited': repositories, 'results': results}


def derived_handoff_checks(public, entries, root):
    """Compare reviewed evidence, keeping auth policy and containing revisions distinct."""
    results = []
    try:
        owner = load(read_public(root, 'docs/acceptance/rc008-owner-review.json'))
        auth = next(e for e in entries if e['repository'] == 'auth-cp')
        if (owner['source_revision'] != auth['source_revision'] or owner['disposition'] != 'COMPATIBLE'
                or owner['foundation'] != SOURCE
                or re.fullmatch('[0-9a-f]{40}', owner['policy_revision']) is None):
            raise Denied('AUTH_REVIEW_UNAVAILABLE')
    except (Denied, KeyError, TypeError, StopIteration):
        owner = None
    for filename in ('contracts/linux-guest-admission/b70-revision-handoff.json',
                     'contracts/linux-guest-admission/b70-doctrine-reconciliation.json'):
        try:
            record = load(public[filename])
            if filename.endswith('b70-revision-handoff.json'):
                foundation = record['foundation']['revision']
                doctrine = record['foundation']['doctrine_revision']
                auth_policy = record['auth_cp']['revision']
                containing = None
            else:
                foundation = record['foundation_current_revision']
                doctrine = record['foundation_active_doctrine_revision']
                auth_policy = record['auth_policy_revision']
                containing = record['observed_auth_published_revision']
            if any(not isinstance(v, str) or re.fullmatch('[0-9a-f]{40}', v) is None
                   for v in (foundation, doctrine, auth_policy)) or (
                       containing is not None and (not isinstance(containing, str)
                       or re.fullmatch('[0-9a-f]{40}', containing) is None)):
                raise Denied('INVALID_HANDOFF_PIN')
            same = foundation == SOURCE['repository_revision'] and doctrine == SOURCE['doctrine_revision']
            results.append(result('ansible-cp', 'RC008', 'PASS' if same else 'DRIFT',
                                  ('HANDOFF_PINS_MATCH:' if same else 'HANDOFF_PIN_REVIEW_REQUIRED:') + filename))
            if owner is None:
                results.append(result('ansible-cp', 'RC010', 'UNKNOWN', 'AUTH_REVIEW_UNAVAILABLE:' + filename))
            else:
                same = auth_policy == owner['policy_revision'] and (
                    containing is None or containing == owner['source_revision'])
                results.append(result('ansible-cp', 'RC010', 'PASS' if same else 'DRIFT',
                                      ('AUTH_PINS_MATCH:' if same else 'AUTH_PIN_REVIEW_REQUIRED:') + filename))
        except (Denied, KeyError, TypeError):
            for check in ('RC008', 'RC010'):
                results.append(result('ansible-cp', check, 'UNKNOWN', 'ACCEPTED_HANDOFF_UNAVAILABLE:' + filename))
    return results


def proposals(report):
    """Deterministic stdout-only review artifact; no invented patch or action."""
    findings = [r for r in report['results'] if r['status'] in ('DRIFT', 'BLOCKED', 'UNKNOWN')]
    return {'schema_version': 1, 'status': 'REVIEW_REQUIRED' if findings else 'NO_CHANGE',
            'source': SOURCE, 'automatic_execution': False, 'patch': None,
            'proposals': [{'repository': r['repository'], 'check_id': r['check_id'],
                           'reason': r['reason'], 'next_step': 'OWNER_REVIEW_REQUIRED',
                           'mutation_authorized': False} for r in findings]}


def text_report(report):
    lines = ['REPO-CP REPOSITORY AUDIT', 'STATUS: ' + report['status']]
    lines += [r['repository'] + ' ' + r['check_id'] + ' ' + r['status'] + ' ' + r['reason']
              for r in report['results']]
    return '\n'.join(lines + ['AUTOMATIC_EXECUTION: DISABLED', 'LIVE_MUTATION: NONE']) + '\n'
