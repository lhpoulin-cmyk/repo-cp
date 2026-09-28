"""Synthetic evidence for the bounded, non-dispatching usage adviser."""
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from repocp.usage_advice import (UsageInputError, evaluate_advice, human_report,
                                 parse_observation, proposed_ledger)
from repocp.work_protocol import topology


NOW = datetime(2026, 9, 27, 12, tzinfo=timezone.utc)


def raw_window(*, semantic='REMAINING', percentage=72, observed_at='2026-09-27T08:00:00Z',
               reset_at='2026-09-29T12:00:00Z', reset_timezone=None,
               display_resolution=1, provider='openai', resource_pool='codex-plan',
               window_id='weekly'):
    window = {
        'provider': provider,
        'resource_pool': resource_pool,
        'window_id': window_id,
        'semantic': semantic,
        'percentage': percentage,
        'observed_at': observed_at,
        'reset_at': reset_at,
        'display_resolution': display_resolution,
        'source': 'PROVIDER_UI_MANUAL',
    }
    if reset_timezone is not None:
        window['reset_timezone'] = reset_timezone
    return window


def encoded(*windows):
    return json.dumps({'schema_version': 1, 'protocol': 'HELIX_USAGE_OBSERVATION_V1',
                       'windows': list(windows)}).encode()


def active_topology():
    document = copy.deepcopy(topology())
    entry = next(item for item in document['entries'] if item['id'] == '006')
    entry['state'] = 'ACTIVE'
    entry['scheduling_eligibility'] = 'ELIGIBLE'
    return document


def advice(windows, **kwargs):
    return evaluate_advice(active_topology(), windows, '006', now=NOW, **kwargs)


class UsageAdviceTests(unittest.TestCase):
    def test_remaining_and_used_are_explicit_and_normalized(self):
        remaining = parse_observation(encoded(raw_window()))[0]
        used = parse_observation(encoded(raw_window(semantic='USED', percentage=28)))[0]
        self.assertEqual(remaining['normalized_remaining_percentage'], 72)
        self.assertEqual(used['normalized_remaining_percentage'], 72)
        self.assertEqual((remaining['original_semantic'], used['original_semantic']),
                         ('REMAINING', 'USED'))

    def test_ambiguous_and_out_of_range_percentages_are_rejected(self):
        ambiguous = raw_window()
        del ambiguous['semantic']
        with self.assertRaises(UsageInputError):
            parse_observation(encoded(ambiguous))
        for value in (-1, 101):
            with self.subTest(value=value), self.assertRaises(UsageInputError):
                parse_observation(encoded(raw_window(percentage=value)))

    def test_missing_observation_returns_unknown_review(self):
        result = advice(parse_observation(b''), expected=5)
        self.assertEqual((result['capacity_assessment'], result['advice']), ('UNKNOWN', 'REVIEW'))
        self.assertIn('CAPACITY_OBSERVATION_MISSING', result['reasons'])

    def test_stale_observation_returns_stale_review(self):
        windows = parse_observation(encoded(raw_window(observed_at='2026-09-26T22:59:59Z')))
        result = advice(windows, expected=5)
        self.assertEqual((result['capacity_assessment'], result['advice']), ('STALE', 'REVIEW'))

    def test_reset_already_passed_returns_unknown_review(self):
        windows = parse_observation(encoded(raw_window(reset_at='2026-09-27T11:59:59Z')))
        result = advice(windows, expected=5)
        self.assertEqual((result['capacity_assessment'], result['advice']), ('UNKNOWN', 'REVIEW'))
        self.assertIn('CAPACITY_WINDOW_RESET_PASSED', result['reasons'])

    def test_naive_reset_requires_and_uses_named_timezone(self):
        with self.assertRaises(UsageInputError):
            parse_observation(encoded(raw_window(reset_at='2026-09-29T08:00:00')))
        windows = parse_observation(encoded(raw_window(
            reset_at='2026-09-29T08:00:00', reset_timezone='America/Detroit')))
        self.assertEqual(windows[0]['reset_at'], '2026-09-29T12:00:00Z')
        with self.assertRaises(UsageInputError):
            parse_observation(encoded(raw_window(observed_at='not-a-timestamp')))

    def test_independent_windows_are_reported_but_never_combined(self):
        windows = parse_observation(encoded(
            raw_window(percentage=20, window_id='short'),
            raw_window(percentage=30, window_id='long')))
        result = advice(windows, expected=40)
        self.assertEqual((result['capacity_assessment'], result['advice']), ('UNKNOWN', 'REVIEW'))
        self.assertIn('INDEPENDENT_WINDOWS_NOT_COMBINED', result['reasons'])
        self.assertEqual([item['normalized_remaining_percentage'] for item in result['windows']],
                         [20, 30])
        self.assertNotIn(50, [item['normalized_remaining_percentage'] for item in result['windows']])

    def test_multiple_resource_pools_require_explicit_selection(self):
        windows = parse_observation(encoded(
            raw_window(resource_pool='codex-plan'),
            raw_window(provider='anthropic', resource_pool='claude-plan')))
        result = advice(windows, expected=5)
        self.assertEqual(result['advice'], 'REVIEW')
        self.assertIn('RESOURCE_POOL_SELECTION_REQUIRED', result['reasons'])

    def test_display_rounding_is_preserved(self):
        windows = parse_observation(encoded(raw_window(percentage=72.5, display_resolution=0.5)))
        result = advice(windows, expected=5)
        self.assertEqual(result['windows'][0]['observed_percentage'], 72.5)
        self.assertEqual(result['windows'][0]['display_resolution'], 0.5)

    def test_ordinal_sizes_remain_ordinal_and_review(self):
        windows = parse_observation(encoded(raw_window()))
        for size in ('S', 'M', 'L'):
            with self.subTest(size=size):
                result = advice(windows, size=size)
                self.assertEqual((result['capacity_assessment'], result['advice']),
                                 ('UNKNOWN', 'REVIEW'))
                self.assertIsNone(result['work']['expected_consumption_percentage_points'])
                self.assertIn('ORDINAL_SIZE_HAS_NO_PERCENTAGE_MAPPING', result['reasons'])

    def test_explicit_consumption_supports_fit_and_defer(self):
        windows = parse_observation(encoded(raw_window()))
        fit = advice(windows, expected=10)
        defer = advice(windows, expected=40)
        self.assertEqual((fit['capacity_assessment'], fit['advice']), ('ADEQUATE', 'FIT'))
        self.assertEqual((defer['capacity_assessment'], defer['advice']),
                         ('CONSTRAINED', 'DEFER'))
        self.assertEqual(fit['authority_effect'], 'NONE')
        self.assertIn('EXPECTED_CONSUMPTION_EXCEEDS_CURRENT_PACING_HEURISTIC',
                      defer['reasons'])
        report = human_report(fit)
        self.assertIn('Work sizing: 10 expected percentage points', report)
        self.assertIn('observed 72% REMAINING; 72% remaining', report)
        self.assertIn('Authority effect: NONE', report)

    def test_topology_ineligible_short_circuits_capacity(self):
        windows = parse_observation(encoded(raw_window()))
        result = evaluate_advice(topology(), windows, '006', expected=1, now=NOW)
        self.assertEqual(result['advice'], 'DEFER')
        self.assertEqual(result['capacity_assessment'], 'UNKNOWN')
        self.assertEqual(result['reasons'][0], 'WORK_ENTRY_LIFECYCLE_INELIGIBLE')
        self.assertIn('CAPACITY_NOT_EVALUATED_TOPOLOGY_INELIGIBLE', result['reasons'])
        self.assertEqual(result['windows'][0]['freshness'], 'NOT_EVALUATED')
        self.assertIsNone(result['windows'][0]['pacing_heuristic_percentage_points_per_day'])

    def test_dependency_blocked_short_circuits_capacity(self):
        document = active_topology()
        entry = next(item for item in document['entries'] if item['id'] == '006')
        entry['state'] = 'BLOCKED'
        entry['scheduling_eligibility'] = 'INELIGIBLE_DEPENDENCY'
        result = evaluate_advice(document, parse_observation(encoded(raw_window())), '006',
                                 expected=1, now=NOW)
        self.assertEqual(result['advice'], 'DEFER')
        self.assertEqual(result['reasons'][0], 'WORK_ENTRY_DEPENDENCY_BLOCKED')

    def test_ledger_preserves_evidence_and_fails_closed_on_attribution(self):
        before = parse_observation(encoded(raw_window(percentage=72)))
        after = parse_observation(encoded(raw_window(
            percentage=68, observed_at='2026-09-27T10:00:00Z')))
        exclusive = proposed_ledger('006', before, after, attribution_context='EXCLUSIVE')
        self.assertEqual(exclusive['persistence'], 'STDOUT_ONLY')
        self.assertEqual(exclusive['records'][0]['attribution'], 'WORK_ENTRY')
        self.assertEqual(exclusive['records'][0]['observed_consumption_percentage_points'], 4)
        self.assertEqual(exclusive['records'][0]['before']['original_semantic'], 'REMAINING')
        self.assertEqual(exclusive['records'][0]['before']['display_resolution'], 1)

        concurrent = proposed_ledger('006', before, after, attribution_context='CONCURRENT')
        self.assertEqual(concurrent['records'][0]['attribution'], 'UNKNOWN')
        self.assertEqual(concurrent['records'][0]['attribution_reason'],
                         'CONCURRENT_ACTIVITY_DECLARED')

        reset_after = parse_observation(encoded(raw_window(
            percentage=100, observed_at='2026-09-30T10:00:00Z',
            reset_at='2026-10-06T12:00:00Z')))
        contaminated = proposed_ledger('006', before, reset_after,
                                       attribution_context='EXCLUSIVE')
        self.assertEqual(contaminated['records'][0]['attribution'], 'UNKNOWN')
        self.assertEqual(contaminated['records'][0]['attribution_reason'],
                         'RESET_CONTAMINATED_INTERVAL')

    def test_cli_json_and_ledger_are_stdout_only(self):
        result = subprocess.run(
            [sys.executable, '-B', str(ROOT / 'tools/repo-cp'), 'usage-advice',
             '--work-entry', '006', '--expected-percentage-points', '5', '--json',
             '--propose-ledger', '--now', '2026-09-27T12:00:00Z'],
            cwd=ROOT, input=encoded(raw_window()), capture_output=True, check=False)
        self.assertEqual((result.returncode, result.stderr), (0, b''))
        output = json.loads(result.stdout)
        self.assertEqual(output['authority_effect'], 'NONE')
        self.assertEqual(output['advice'], 'DEFER')
        self.assertEqual(output['proposed_ledger_record']['persistence'], 'STDOUT_ONLY')
        self.assertEqual(output['proposed_ledger_record']['records'][0]['attribution'], 'UNKNOWN')

    def test_cli_accepts_only_the_explicitly_supplied_observation_file(self):
        with tempfile.TemporaryDirectory() as directory:
            observation = Path(directory) / 'observation.json'
            observation.write_bytes(encoded(raw_window()))
            result = subprocess.run(
                [sys.executable, '-B', str(ROOT / 'tools/repo-cp'), 'usage-advice',
                 '--work-entry', '006', '--size', 'S', '--input', str(observation), '--json',
                 '--now', '2026-09-27T12:00:00Z'],
                cwd=ROOT, input=b'', capture_output=True, check=False)
            self.assertEqual((result.returncode, result.stderr), (0, b''))
            self.assertEqual(json.loads(result.stdout)['authority_effect'], 'NONE')


if __name__ == '__main__':
    unittest.main()
