"""Deterministic capacity advice from explicit observations; never dispatches or writes."""
import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .consumer import verify
from .safety import MAX_BYTES, has_indicator, load
from .work_protocol import topology


PROTOCOL = 'HELIX_USAGE_OBSERVATION_V1'
RESULT_PROTOCOL = 'HELIX_USAGE_ADVICE_V1'
LEDGER_PROTOCOL = 'HELIX_USAGE_LEDGER_PROPOSAL_V1'
STALE_AFTER_HOURS = 12
SOURCES = frozenset({'PROVIDER_UI_MANUAL'})
SEMANTICS = frozenset({'REMAINING', 'USED'})
SIZES = ('S', 'M', 'L')
WINDOW_KEYS = frozenset({
    'provider', 'resource_pool', 'window_id', 'semantic', 'percentage',
    'observed_at', 'reset_at', 'reset_timezone', 'display_resolution', 'source',
})
IDENTIFIER = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,199}$')


class UsageInputError(ValueError):
    """An observation or option is structurally unsafe or ambiguous."""


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise UsageInputError('CLI_ARGUMENTS')


def _number(value, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise UsageInputError('INVALID_NUMBER')
    result = float(value)
    if not math.isfinite(result) or (positive and result <= 0):
        raise UsageInputError('INVALID_NUMBER')
    return result


def _identifier(value):
    if not isinstance(value, str) or IDENTIFIER.fullmatch(value) is None:
        raise UsageInputError('INVALID_IDENTIFIER')
    return value


def _display_number(value):
    value = round(float(value), 10)
    return int(value) if value.is_integer() else value


def _timestamp(value, *, reset_timezone=None):
    if not isinstance(value, str) or not value:
        raise UsageInputError('INVALID_TIMESTAMP')
    candidate = value[:-1] + '+00:00' if value.endswith('Z') else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        raise UsageInputError('INVALID_TIMESTAMP') from None
    if parsed.tzinfo is None:
        if reset_timezone is None:
            raise UsageInputError('TIMEZONE_REQUIRED')
        try:
            parsed = parsed.replace(tzinfo=ZoneInfo(reset_timezone))
        except ZoneInfoNotFoundError:
            raise UsageInputError('INVALID_TIMEZONE') from None
    return parsed.astimezone(timezone.utc)


def _iso(value):
    return value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def read_explicit(path):
    """Read only the explicitly named regular file, without following its final symlink."""
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    if hasattr(os, 'O_NOATIME'):
        flags |= os.O_NOATIME
    try:
        descriptor = os.open(Path(path), flags)
        with os.fdopen(descriptor, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size > MAX_BYTES:
                raise UsageInputError('UNSAFE_INPUT_FILE')
            raw = stream.read(MAX_BYTES + 1)
            after = os.fstat(stream.fileno())
            if (info.st_size, info.st_mtime_ns, info.st_ctime_ns) != (
                    after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise UsageInputError('INPUT_FILE_CHANGED')
    except OSError:
        raise UsageInputError('INPUT_FILE_UNAVAILABLE') from None
    if len(raw) > MAX_BYTES:
        raise UsageInputError('INPUT_SIZE')
    return raw


def parse_observation(raw):
    """Validate and normalize one explicit observation document."""
    if raw in (b'', None):
        return []
    if not isinstance(raw, bytes) or has_indicator(raw):
        raise UsageInputError('OBSERVATION_NONCONFORMANCE')
    try:
        document = load(raw)
    except ValueError:
        raise UsageInputError('OBSERVATION_NONCONFORMANCE') from None
    if not isinstance(document, dict) or set(document) != {'schema_version', 'protocol', 'windows'} \
            or document['schema_version'] != 1 or document['protocol'] != PROTOCOL \
            or not isinstance(document['windows'], list):
        raise UsageInputError('OBSERVATION_NONCONFORMANCE')
    result = []
    identities = set()
    for source in document['windows']:
        required = WINDOW_KEYS - {'reset_timezone', 'display_resolution'}
        if not isinstance(source, dict) or set(source) - WINDOW_KEYS \
                or not required <= set(source):
            raise UsageInputError('OBSERVATION_NONCONFORMANCE')
        for key in ('provider', 'resource_pool', 'window_id'):
            _identifier(source[key])
        if source['semantic'] not in SEMANTICS or source['source'] not in SOURCES:
            raise UsageInputError('OBSERVATION_NONCONFORMANCE')
        percentage = _number(source['percentage'])
        if percentage < 0 or percentage > 100:
            raise UsageInputError('PERCENTAGE_RANGE')
        resolution = source.get('display_resolution')
        if resolution is not None:
            resolution = _number(resolution, positive=True)
            if resolution > 100:
                raise UsageInputError('DISPLAY_RESOLUTION_RANGE')
        zone = source.get('reset_timezone')
        if zone is not None:
            if not isinstance(zone, str) or not zone:
                raise UsageInputError('INVALID_TIMEZONE')
            try:
                ZoneInfo(zone)
            except ZoneInfoNotFoundError:
                raise UsageInputError('INVALID_TIMEZONE') from None
        observed = _timestamp(source['observed_at'])
        reset = _timestamp(source['reset_at'], reset_timezone=zone)
        identity = (source['provider'], source['resource_pool'], source['window_id'])
        if identity in identities:
            raise UsageInputError('DUPLICATE_WINDOW')
        identities.add(identity)
        remaining = percentage if source['semantic'] == 'REMAINING' else 100 - percentage
        result.append({
            'provider': source['provider'],
            'resource_pool': source['resource_pool'],
            'window_id': source['window_id'],
            'source': source['source'],
            'original_semantic': source['semantic'],
            'observed_percentage': source['percentage'],
            'normalized_remaining_percentage': _display_number(remaining),
            'observed_at': _iso(observed),
            'reset_at': _iso(reset),
            'reset_timezone': zone,
            'display_resolution': source.get('display_resolution'),
            '_observed': observed,
            '_reset': reset,
        })
    return result


def _public_window(window, now):
    age = (now - window['_observed']).total_seconds() / 3600
    if age < 0:
        raise UsageInputError('FUTURE_OBSERVATION')
    until_reset = (window['_reset'] - now).total_seconds() / 3600
    if window['_reset'] <= now:
        freshness = 'RESET_PASSED'
        pace = None
    elif age > STALE_AFTER_HOURS:
        freshness = 'STALE'
        pace = None
    else:
        freshness = 'FRESH'
        pace = window['normalized_remaining_percentage'] / (until_reset / 24)
    return {
        key: value for key, value in window.items() if not key.startswith('_')
    } | {
        'observation_age_hours': _display_number(age),
        'hours_until_reset': _display_number(until_reset),
        'freshness': freshness,
        'pacing_heuristic_percentage_points_per_day': (
            None if pace is None else _display_number(pace)),
    }


def _unevaluated_window(window):
    return {
        key: value for key, value in window.items() if not key.startswith('_')
    } | {
        'observation_age_hours': None,
        'hours_until_reset': None,
        'freshness': 'NOT_EVALUATED',
        'pacing_heuristic_percentage_points_per_day': None,
    }


def _topology_context(document, work_entry_id):
    by_id = {item['id']: item for item in document['entries']}
    entry = next((item for item in document['entries'] if item['id'] == work_entry_id), None)
    if entry is None:
        return ({'found': False, 'state': None, 'priority': None,
                 'scheduling_eligibility': None, 'dependencies': [],
                 'dependency_status': []}, False,
                'WORK_ENTRY_NOT_IN_CANONICAL_TOPOLOGY')
    context = {
        'found': True,
        'state': entry['state'],
        'priority': entry['priority'],
        'scheduling_eligibility': entry['scheduling_eligibility'],
        'dependencies': list(entry['dependencies']),
        'dependency_status': [
            {'id': identifier, 'state': by_id[identifier]['state'],
             'satisfied': by_id[identifier]['state'] == 'COMPLETE'}
            for identifier in entry['dependencies']
        ],
    }
    eligible = entry['state'] == 'ACTIVE' and entry['scheduling_eligibility'] == 'ELIGIBLE'
    if entry['scheduling_eligibility'] == 'INELIGIBLE_DEPENDENCY':
        reason = 'WORK_ENTRY_DEPENDENCY_BLOCKED'
    elif not eligible:
        reason = 'WORK_ENTRY_LIFECYCLE_INELIGIBLE'
    else:
        reason = None
    return context, eligible, reason


def evaluate_advice(topology_document, windows, work_entry_id, *, size=None, expected=None,
                    resource_pool=None, capacity_window=None, now=None):
    now = (now or datetime.now(timezone.utc))
    if now.tzinfo is None:
        raise UsageInputError('TIMEZONE_REQUIRED')
    now = now.astimezone(timezone.utc)
    _identifier(work_entry_id)
    if resource_pool is not None:
        _identifier(resource_pool)
    if capacity_window is not None:
        _identifier(capacity_window)
    if (size is None) == (expected is None):
        raise UsageInputError('WORK_SIZE_REQUIRED')
    if size is not None and size not in SIZES:
        raise UsageInputError('INVALID_SIZE')
    if expected is not None:
        expected = _number(expected, positive=True)
        if expected > 100:
            raise UsageInputError('PERCENTAGE_RANGE')

    topology_context, eligible, topology_reason = _topology_context(topology_document, work_entry_id)
    reasons = []
    limitations = [
        'Capacity advice is heuristic, not provider billing, token, cost, or future-availability truth.',
        'Capacity advice does not grant execution authority or change Work Entry lifecycle state.',
    ]
    work = {
        'work_entry_id': work_entry_id,
        'ordinal_size': size,
        'expected_consumption_percentage_points': (
            None if expected is None else _display_number(expected)),
        'resource_pool': resource_pool,
        'capacity_window_id': capacity_window,
    }
    result = {
        'protocol': RESULT_PROTOCOL,
        'evaluation_order': ['TOPOLOGY', 'CAPACITY'],
        'evaluated_at': _iso(now),
        'stale_after_hours': STALE_AFTER_HOURS,
        'work': work,
        'topology': topology_context,
        'windows': [],
        'selected_window': None,
        'capacity_assessment': 'UNKNOWN',
        'advice': 'REVIEW',
        'reasons': reasons,
        'evidence_limitations': limitations,
        'authority_effect': 'NONE',
    }
    if not eligible:
        result['windows'] = [_unevaluated_window(window) for window in windows]
        reasons.append(topology_reason)
        reasons.append('CAPACITY_NOT_EVALUATED_TOPOLOGY_INELIGIBLE')
        result['advice'] = 'DEFER' if topology_context['found'] else 'REVIEW'
        return result
    public_windows = [_public_window(window, now) for window in windows]
    result['windows'] = public_windows
    if not windows:
        reasons.append('CAPACITY_OBSERVATION_MISSING')
        return result

    pools = sorted({window['resource_pool'] for window in windows})
    if resource_pool is None:
        if len(pools) != 1:
            reasons.append('RESOURCE_POOL_SELECTION_REQUIRED')
            return result
        resource_pool = pools[0]
        work['resource_pool'] = resource_pool
    selected_pool = [window for window in windows if window['resource_pool'] == resource_pool]
    if not selected_pool:
        reasons.append('RESOURCE_POOL_NOT_OBSERVED')
        return result
    if capacity_window is None:
        if len(selected_pool) != 1:
            reasons.append('CAPACITY_WINDOW_SELECTION_REQUIRED')
            reasons.append('INDEPENDENT_WINDOWS_NOT_COMBINED')
            return result
        selected = selected_pool[0]
        work['capacity_window_id'] = selected['window_id']
    else:
        matches = [window for window in selected_pool if window['window_id'] == capacity_window]
        if len(matches) != 1:
            reasons.append('CAPACITY_WINDOW_NOT_OBSERVED')
            return result
        selected = matches[0]
    public_selected = next(window for window in public_windows
                           if (window['provider'], window['resource_pool'], window['window_id']) ==
                           (selected['provider'], selected['resource_pool'], selected['window_id']))
    result['selected_window'] = {
        'provider': selected['provider'], 'resource_pool': selected['resource_pool'],
        'window_id': selected['window_id'],
    }
    if public_selected['freshness'] == 'STALE':
        result['capacity_assessment'] = 'STALE'
        reasons.append('CAPACITY_OBSERVATION_STALE')
        return result
    if public_selected['freshness'] == 'RESET_PASSED':
        reasons.append('CAPACITY_WINDOW_RESET_PASSED')
        return result
    if size is not None:
        reasons.append('ORDINAL_SIZE_HAS_NO_PERCENTAGE_MAPPING')
        limitations.append('S, M, and L are ordinal only; no percentage-point mapping is inferred.')
        return result

    remaining = float(selected['normalized_remaining_percentage'])
    allowance = float(public_selected['pacing_heuristic_percentage_points_per_day'])
    if expected <= remaining and expected <= allowance:
        result['capacity_assessment'] = 'ADEQUATE'
        result['advice'] = 'FIT'
        reasons.append('EXPECTED_CONSUMPTION_WITHIN_CURRENT_PACING_HEURISTIC')
    else:
        result['capacity_assessment'] = 'CONSTRAINED'
        result['advice'] = 'DEFER'
        if expected > remaining:
            reasons.append('EXPECTED_CONSUMPTION_EXCEEDS_REMAINING_CAPACITY')
        if expected > allowance:
            reasons.append('EXPECTED_CONSUMPTION_EXCEEDS_CURRENT_PACING_HEURISTIC')
    return result


def proposed_ledger(work_entry_id, before, after, *, attribution_context='UNKNOWN'):
    """Build a stdout-only proposal; never persists or claims ambiguous attribution."""
    _identifier(work_entry_id)
    if attribution_context not in ('UNKNOWN', 'EXCLUSIVE', 'CONCURRENT'):
        raise UsageInputError('INVALID_ATTRIBUTION_CONTEXT')
    after_by_id = {(item['provider'], item['resource_pool'], item['window_id']): item
                   for item in after}
    records = []
    for first in before:
        identity = (first['provider'], first['resource_pool'], first['window_id'])
        second = after_by_id.get(identity)
        record = {
            'provider': first['provider'],
            'resource_pool': first['resource_pool'],
            'window_id': first['window_id'],
            'before': {key: value for key, value in first.items() if not key.startswith('_')},
            'after': (None if second is None else
                      {key: value for key, value in second.items() if not key.startswith('_')}),
            'attribution': 'UNKNOWN',
            'observed_consumption_percentage_points': None,
            'attribution_reason': None,
        }
        if second is None:
            record['attribution_reason'] = 'AFTER_OBSERVATION_MISSING'
        elif attribution_context != 'EXCLUSIVE':
            record['attribution_reason'] = ('CONCURRENT_ACTIVITY_DECLARED'
                                             if attribution_context == 'CONCURRENT'
                                             else 'EXCLUSIVITY_NOT_ESTABLISHED')
        elif second['_observed'] <= first['_observed']:
            record['attribution_reason'] = 'OBSERVATION_ORDER_INVALID'
        elif second['_reset'] != first['_reset'] or first['_reset'] <= second['_observed']:
            record['attribution_reason'] = 'RESET_CONTAMINATED_INTERVAL'
        else:
            delta = (float(first['normalized_remaining_percentage'])
                     - float(second['normalized_remaining_percentage']))
            if delta < 0:
                record['attribution_reason'] = 'CAPACITY_INCREASE_UNEXPLAINED'
            else:
                record['attribution'] = 'WORK_ENTRY'
                record['observed_consumption_percentage_points'] = _display_number(delta)
                record['attribution_reason'] = 'OPERATOR_DECLARED_EXCLUSIVE_INTERVAL'
        records.append(record)
    return {
        'protocol': LEDGER_PROTOCOL,
        'persistence': 'STDOUT_ONLY',
        'work_entry_id': work_entry_id,
        'attribution_context': attribution_context,
        'records': records,
        'authority_effect': 'NONE',
    }


def human_report(result):
    topology_context = result['topology']
    dependencies = topology_context['dependency_status']
    work = result['work']
    sizing = ('ordinal ' + work['ordinal_size'] if work['ordinal_size'] is not None else
              '%s expected percentage points' % work['expected_consumption_percentage_points'])
    lines = [
        'Work Entry: ' + work['work_entry_id'],
        'Topology: ' + (('%s / %s / %s' % (
            topology_context['state'], topology_context['priority'],
            topology_context['scheduling_eligibility'])) if topology_context['found'] else 'NOT FOUND'),
        'Dependencies: ' + (', '.join('%s=%s (%s)' % (
            item['id'], item['state'], 'satisfied' if item['satisfied'] else 'unsatisfied')
            for item in dependencies) if dependencies else 'none'),
        'Work sizing: ' + sizing,
        'Capacity: ' + result['capacity_assessment'],
        'Advice: ' + result['advice'],
        'Authority effect: NONE',
    ]
    for window in result['windows']:
        age = ('not evaluated' if window['observation_age_hours'] is None else
               '%s hours' % window['observation_age_hours'])
        lines.append('Window: %s/%s/%s; observed %s%% %s; %s%% remaining' % (
            window['provider'], window['resource_pool'], window['window_id'],
            window['observed_percentage'], window['original_semantic'],
            window['normalized_remaining_percentage']))
        lines.append('  Evidence: %s; observed %s; age %s; resolution %s; freshness %s' % (
            window['source'], window['observed_at'], age,
            window['display_resolution'] if window['display_resolution'] is not None else 'unknown',
            window['freshness']))
        lines.append('  Reset: %s; reset timezone %s' % (
            window['reset_at'], window['reset_timezone'] or 'encoded in timestamp'))
        if window['pacing_heuristic_percentage_points_per_day'] is not None:
            lines.append('  Pacing heuristic: %s percentage points/day' %
                         window['pacing_heuristic_percentage_points_per_day'])
    lines.extend('Reason: ' + reason for reason in result['reasons'])
    lines.extend('Limitation: ' + limitation for limitation in result['evidence_limitations'])
    if 'proposed_ledger_record' in result:
        lines.append('Proposed ledger record (stdout only):')
        lines.append(json.dumps(result['proposed_ledger_record'], sort_keys=True))
    return '\n'.join(lines) + '\n'


def main(argv=None):
    parser = Parser(description=__doc__)
    parser.add_argument('--work-entry', required=True)
    sizing = parser.add_mutually_exclusive_group(required=True)
    sizing.add_argument('--size', choices=SIZES)
    sizing.add_argument('--expected-percentage-points', type=float)
    parser.add_argument('--input', type=Path, help='Explicit observation JSON path; default: stdin')
    parser.add_argument('--resource-pool')
    parser.add_argument('--capacity-window')
    parser.add_argument('--now', help='Timezone-aware evaluation timestamp (test/replay seam)')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--propose-ledger', action='store_true')
    parser.add_argument('--after-input', type=Path)
    parser.add_argument('--attribution-context', choices=('UNKNOWN', 'EXCLUSIVE', 'CONCURRENT'),
                        default='UNKNOWN')
    args = parser.parse_args(argv)
    if args.after_input is not None and not args.propose_ledger:
        raise UsageInputError('LEDGER_OPTION_CONFLICT')
    raw = read_explicit(args.input) if args.input is not None else sys.stdin.buffer.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise UsageInputError('INPUT_SIZE')
    windows = parse_observation(raw)
    now = _timestamp(args.now) if args.now else datetime.now(timezone.utc)
    verify()
    topology_document = topology()
    result = evaluate_advice(
        topology_document, windows, args.work_entry, size=args.size,
        expected=args.expected_percentage_points, resource_pool=args.resource_pool,
        capacity_window=args.capacity_window, now=now)
    if args.propose_ledger:
        after = [] if args.after_input is None else parse_observation(read_explicit(args.after_input))
        result['proposed_ledger_record'] = proposed_ledger(
            args.work_entry, windows, after, attribution_context=args.attribution_context)
    sys.stdout.write((json.dumps(result, indent=2, sort_keys=True) + '\n')
                     if args.json else human_report(result))
    return 0
