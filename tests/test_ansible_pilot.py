"""Synthetic public metadata only; no Ansible, peer programs or target operations."""
import hashlib
import json
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch

import test_consumer as support
from test_consumer import ROOT, snapshot
from repocp.audit import audit, registry, proposals
from repocp.consumer import SOURCE
from repocp.safety import Denied


class AnsiblePilotTests(unittest.TestCase):
    save = support.AuditTests.save

    def setUp(self):
        support.AuditTests.setUp(self)
        self.ans = next(e for e in self.data['repositories'] if e['repository'] == 'ansible-cp')
        self.ans.clear()
        self.ans.update(json.loads((ROOT / 'tests/fixtures/enrollment/ansible-pilot-before.json').read_bytes()))
        receipt = self.root / 'docs/acceptance/rc008-owner-review.json'
        receipt.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / 'docs/acceptance/rc008-owner-review.json', receipt)
        self.owner = json.loads(receipt.read_bytes())
        self.checkout = self.base / 'ansible-cp'
        (self.checkout / '.git/refs/heads').mkdir(parents=True)
        (self.checkout / '.git/HEAD').write_text('ref: refs/heads/main\n')
        (self.checkout / '.git/refs/heads/main').write_text(self.ans['source_revision'])
        for name, digest in self.ans['files'].items():
            if digest is None:
                continue
            if name.endswith('b70-revision-handoff.json'):
                value = {'foundation': {'revision': SOURCE['repository_revision'],
                                       'doctrine_revision': SOURCE['doctrine_revision']},
                         'auth_cp': {'revision': self.owner['policy_revision']}}
            elif name.endswith('b70-doctrine-reconciliation.json'):
                value = {'foundation_current_revision': SOURCE['repository_revision'],
                         'foundation_active_doctrine_revision': SOURCE['doctrine_revision'],
                         'auth_policy_revision': self.owner['policy_revision'],
                         'observed_auth_published_revision': self.owner['source_revision']}
            else:
                value = None
            self.put(name, json.dumps(value).encode() if value else b'Synthetic reviewed metadata\n')
        self.save()

    def put(self, name, raw):
        path = self.checkout / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        self.ans['files'][name] = hashlib.sha256(raw).hexdigest()

    def report(self):
        return audit(self.base, root=self.root, pilot=True, repository='ansible-cp')

    def test_explicit_selection_and_authorization(self):
        with self.assertRaises(Denied): audit(self.base, root=self.root, repository='ansible-cp')
        self.assertEqual(self.report()['repositories_audited'], ['ansible-cp'])
        self.ans['pilot_authorization'] = self.entry['pilot_authorization']; self.save()
        with self.assertRaises(Denied): self.report()

    def test_missing_metadata_visible_without_invention(self):
        findings = self.report()['results']
        missing = [r for r in findings if r['check_id'] == 'RC004' and r['status'] == 'UNKNOWN']
        self.assertEqual(len(missing), 3)
        self.assertEqual([r['status'] for r in findings if r['check_id'] == 'RC007'], ['UNKNOWN'])
        self.assertFalse((self.checkout / 'VERSION').exists())

    def test_absence_cannot_weaken_enrollment(self):
        self.ans.update(state='ENROLLED', enrollment_authorization='synthetic approval')
        self.save()
        with self.assertRaises(Denied): registry(self.root)

    def test_policy_and_containing_commits_not_interchangeable(self):
        name = 'contracts/linux-guest-admission/b70-revision-handoff.json'
        data = json.loads((self.checkout / name).read_bytes())
        data['auth_cp']['revision'] = self.owner['source_revision']
        self.put(name, json.dumps(data).encode()); self.save()
        self.assertTrue(any(r['check_id'] == 'RC010' and r['status'] == 'DRIFT' for r in self.report()['results']))

    def test_stale_foundation_and_unavailable_owner(self):
        name = 'contracts/linux-guest-admission/b70-revision-handoff.json'
        data = json.loads((self.checkout / name).read_bytes()); data['foundation']['revision'] = '0' * 40
        self.put(name, json.dumps(data).encode()); self.save()
        (self.root / 'docs/acceptance/rc008-owner-review.json').unlink()
        rows = self.report()['results']
        self.assertTrue(any(r['check_id'] == 'RC008' and r['status'] == 'DRIFT' for r in rows))
        self.assertTrue(all(r['status'] == 'UNKNOWN' for r in rows if r['check_id'] == 'RC010'))

    def test_missing_pinned_file_blocks(self):
        (self.checkout / 'scripts/validate').unlink()
        self.assertEqual(self.report()['status'], 'BLOCKED')

    def test_new_unpinned_metadata_is_drift(self):
        (self.checkout / 'VERSION').write_text('1.0.0\n')
        self.assertEqual(self.report()['status'], 'DRIFT')
        self.assertIsNone(self.ans['files']['VERSION'])

    def test_malformed_handoff_denied_without_echo(self):
        name = 'contracts/linux-guest-admission/b70-revision-handoff.json'
        self.put(name, b'{"rejected-payload-marker":'); self.save()
        report = self.report()
        self.assertIn('ACCEPTED_HANDOFF_UNAVAILABLE', str(report))
        self.assertNotIn('rejected-payload-marker', str(report))

    def test_audit_and_proposal_never_execute_or_write(self):
        before = snapshot(self.base)
        with patch('subprocess.run', side_effect=AssertionError('no subprocess permitted')):
            first = self.report(); second = self.report()
            self.assertEqual(first, second)
            self.assertIsNone(proposals(first)['patch'])
        self.assertEqual(before, snapshot(self.base))
        self.assertEqual([r['status'] for r in first['results'] if r['check_id'] == 'RC009'], ['UNKNOWN'])


if __name__ == '__main__':
    unittest.main()
