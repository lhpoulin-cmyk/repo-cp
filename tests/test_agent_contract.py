"""Agent work contract integrity; synthetic temporary roots only, never peers."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from repocp import agent_contract as contract
from repocp.consumer import verify
from repocp.safety import Denied

PINS = (contract.RELEASE_PIN, contract.CANDIDATE_PIN)
COVERED = sorted(contract.COVERED)

# Records every open(2) path the verifier requests. The hook is installed after
# imports, so recorded names come only from verification. Descriptor-relative
# opens report the final component, so sentinels use unique basenames.
PROBE = '''import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
from repocp import agent_contract
from repocp.agent_contract import verify_agent_contract
from repocp.safety import Denied
agent_contract.PIN_SHA256.update(json.loads(sys.argv[3]))
opened = []
sys.addaudithook(lambda event, args: opened.append(str(args[0])) if event == 'open' else None)
try:
    verify_agent_contract(sys.argv[2]); code = 'PASS'
except Denied as error:
    code = str(error)
sys.stdout.write(json.dumps({'code': code, 'opened': opened}))
'''


class ContractRoot(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.root = self.base / 'repo-cp'
        for relative in (*PINS, *COVERED):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)  # Independent copies, never links.

    def pin(self, relative):
        return json.loads((self.root / relative).read_bytes())

    def write_pin(self, relative, data):
        (self.root / relative).write_text(json.dumps(data, indent=2) + '\n')

    def denied(self, code):
        with self.assertRaises(Denied) as caught:
            contract.verify_agent_contract(self.root)
        self.assertEqual(str(caught.exception), code)

    def reanchored(self, pin):
        # Simulate a careless anchor update that accepts the malformed bytes, so
        # the structural layer is tested independently of the byte anchor.
        digest = hashlib.sha256((self.root / pin).read_bytes()).hexdigest()
        return patch.dict(contract.PIN_SHA256, {pin: digest})

    def assert_both_layers(self, pin, *, structural=True):
        self.denied('AGENT_CONTRACT_PIN_INVALID')
        if structural:
            with self.reanchored(pin):
                self.denied('AGENT_CONTRACT_PIN_INVALID')

    def probe(self, reanchor=None):
        anchors = {} if reanchor is None else {
            reanchor: hashlib.sha256((self.root / reanchor).read_bytes()).hexdigest()}
        result = subprocess.run([sys.executable, '-B', '-c', PROBE, str(ROOT / 'src'), str(self.root),
                                 json.dumps(anchors)], capture_output=True, check=True)
        data = json.loads(result.stdout)
        return data['code'], {os.path.basename(name) for name in data['opened']}


class PublishedTreeTests(unittest.TestCase):
    def test_published_contract_pins_and_bytes_verify(self):
        self.assertEqual(contract.verify_agent_contract(), COVERED)
        self.assertEqual(len(COVERED), 4)

    def test_released_bytes_and_foundation_artifacts_preserved(self):
        released = hashlib.sha256((ROOT / 'docs/AGENT_WORK_CONTRACT.md').read_bytes()).hexdigest()
        self.assertEqual(released, 'a4838c4bfd8e1d27ed794c48ca1d475d76929309fabc212368234c4073df7674')
        self.assertEqual(len(verify()), 19)


class TamperTests(ContractRoot):
    def test_every_covered_artifact_rejects_tampering(self):
        for relative in COVERED:
            path = self.root / relative
            original = path.read_bytes()
            flipped = bytes([original[0] ^ 1]) + original[1:]
            for variant in (flipped, original + b'\n', original[:-1], b''):
                with self.subTest(path=relative, size=len(variant)):
                    path.write_bytes(variant)
                    self.denied('AGENT_CONTRACT_MISMATCH')
            path.write_bytes(original)
        self.assertEqual(contract.verify_agent_contract(self.root), COVERED)

    def test_consistent_pin_and_artifact_edit_still_rejected(self):
        # A declaration cannot re-anchor trust: pins must equal reviewed anchors.
        cases = [(contract.RELEASE_PIN, contract.RELEASE['path'], None),
                 (contract.CANDIDATE_PIN, contract.CANDIDATE['path'], None),
                 *[(contract.CANDIDATE_PIN, name, name) for name in sorted(contract.COMPANIONS)]]
        for pin, relative, companion in cases:
            with self.subTest(path=relative):
                self.setUp()
                path = self.root / relative
                path.write_bytes(path.read_bytes() + b'\nUnreviewed addition.\n')
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                data = self.pin(pin)
                if companion:
                    data['companions'][companion] = digest
                else:
                    data['sha256'] = digest
                self.write_pin(pin, data)
                self.assert_both_layers(pin)

    def test_missing_artifacts_and_pins_rejected(self):
        for relative in (*PINS, *COVERED):
            with self.subTest(path=relative):
                self.setUp()
                (self.root / relative).unlink()
                self.denied('PUBLIC_FILE_UNAVAILABLE')


class PinMetadataTests(ContractRoot):
    def mutate(self, pin, change):
        data = self.pin(pin)
        change(data)
        self.write_pin(pin, data)

    def test_reformatted_pin_rejected_by_byte_anchor(self):
        for pin in PINS:
            with self.subTest(pin=pin):
                self.setUp()
                data = self.pin(pin)
                (self.root / pin).write_text(json.dumps(data, indent=4) + '\n')
                self.assertEqual(self.pin(pin), data)  # Same values, different bytes.
                self.denied('AGENT_CONTRACT_PIN_INVALID')
                with self.reanchored(pin):
                    self.assertEqual(contract.verify_agent_contract(self.root), COVERED)

    def test_malformed_pin_metadata_rejected(self):
        for pin in PINS:
            text = contract.RELEASE_TEXT if pin == contract.RELEASE_PIN else contract.CANDIDATE_TEXT
            for key in self.pin(pin):
                for label, change in [
                        ('missing', lambda d, k=key: d.pop(k)),
                        ('none', lambda d, k=key: d.__setitem__(k, None)),
                        ('integer', lambda d, k=key: d.__setitem__(k, 1)),
                        ('boolean', lambda d, k=key: d.__setitem__(k, True)),
                        ('list', lambda d, k=key: d.__setitem__(k, [d[k]])),
                        ('empty', lambda d, k=key: d.__setitem__(k, '')),
                        ('blank', lambda d, k=key: d.__setitem__(k, '   ')),
                        ('changed', lambda d, k=key: d.__setitem__(k, 'x' + json.dumps(d[k])))]:
                    with self.subTest(pin=pin, key=key, change=label):
                        self.setUp()
                        self.mutate(pin, change)
                        # Free text may legitimately change once re-anchored in review.
                        self.assert_both_layers(pin, structural=not (key in text and label == 'changed'))
            for label, raw in [('extra key', None), ('array', b'[]\n'), ('scalar', b'"1.0.0"\n'),
                               ('invalid json', b'{"release": \n'), ('nan', b'{"release": NaN}\n'),
                               ('uppercase digest', None), ('empty file', b'')]:
                with self.subTest(pin=pin, change=label):
                    self.setUp()
                    if label == 'extra key':
                        self.mutate(pin, lambda d: d.__setitem__('signature', 'unreviewed'))
                    elif label == 'uppercase digest':
                        self.mutate(pin, lambda d: d.__setitem__('sha256', d['sha256'].upper()))
                    else:
                        (self.root / pin).write_bytes(raw)
                    self.assert_both_layers(pin)

    def test_duplicate_keys_rejected_even_when_last_value_is_correct(self):
        for pin in PINS:
            for first in ('0' * 64, None):
                with self.subTest(pin=pin, first=first):
                    self.setUp()
                    data = self.pin(pin)
                    value = data['sha256'] if first is None else first
                    body = json.dumps(data)
                    # Last-wins parsers would accept this; repo-cp must not.
                    (self.root / pin).write_text('{"sha256": ' + json.dumps(value) + ', ' + body[1:])
                    self.assert_both_layers(pin)


class NominationTests(ContractRoot):
    def sentinel(self, name, source=contract.RELEASE['path']):
        # Identical bytes: if a nominated file were read and hashed, it would match.
        path = self.root / 'docs' / name
        shutil.copyfile(ROOT / source, path)
        return path

    def assert_rejected_unread(self, pin, *names):
        for reanchor in (None, pin):  # Byte anchor, then the structural layer alone.
            result, opened = self.probe(reanchor)
            self.assertEqual(result, 'AGENT_CONTRACT_PIN_INVALID')
            self.assertIn(os.path.basename(pin), opened)  # Positive control: hook records.
            for name in names:
                self.assertNotIn(name, opened)
            # Pins are validated before any covered artifact is opened.
            self.assertFalse(opened & {os.path.basename(p) for p in COVERED})

    def test_manifest_cannot_nominate_another_file(self):
        outside = self.base / 'OUTSIDE_SENTINEL.md'
        shutil.copyfile(ROOT / contract.RELEASE['path'], outside)
        for path in ('docs/NOMINATED_SENTINEL.md', '../OUTSIDE_SENTINEL.md', str(outside),
                     'docs/../docs/NOMINATED_SENTINEL.md', 'docs//NOMINATED_SENTINEL.md'):
            for pin in PINS:
                with self.subTest(pin=pin, path=path):
                    self.setUp()
                    shutil.copyfile(ROOT / contract.RELEASE['path'], self.base / 'OUTSIDE_SENTINEL.md')
                    self.sentinel('NOMINATED_SENTINEL.md')
                    data = self.pin(pin); data['path'] = path; self.write_pin(pin, data)
                    self.assert_rejected_unread(pin, 'NOMINATED_SENTINEL.md', 'OUTSIDE_SENTINEL.md')

    def test_companion_changes_cannot_reduce_or_redirect_coverage(self):
        names = sorted(contract.COMPANIONS)
        digest = contract.COMPANIONS[names[0]]
        cases = {
            'remove one': lambda c: c.pop(names[0]),
            'remove all': lambda c: c.clear(),
            'add nominated': lambda c: c.__setitem__('docs/NOMINATED_SENTINEL.md', digest),
            'replace one': lambda c: c.__setitem__('docs/NOMINATED_SENTINEL.md', c.pop(names[0])),
            'unsafe path': lambda c: c.__setitem__('../OUTSIDE_SENTINEL.md', c.pop(names[0])),
        }
        for label, change in cases.items():
            with self.subTest(change=label):
                self.setUp()
                self.sentinel('NOMINATED_SENTINEL.md', names[0])
                data = self.pin(contract.CANDIDATE_PIN)
                change(data['companions'])
                self.write_pin(contract.CANDIDATE_PIN, data)
                self.assert_rejected_unread(contract.CANDIDATE_PIN, 'NOMINATED_SENTINEL.md',
                                            'OUTSIDE_SENTINEL.md')
        with self.subTest(change='companions not an object'):
            self.setUp()
            data = self.pin(contract.CANDIDATE_PIN)
            data['companions'] = sorted(data['companions'].items())
            self.write_pin(contract.CANDIDATE_PIN, data)
            self.assert_both_layers(contract.CANDIDATE_PIN)

    def test_deleting_a_companion_file_is_not_reduced_coverage(self):
        for name in sorted(contract.COMPANIONS):
            with self.subTest(path=name):
                self.setUp()
                (self.root / name).unlink()
                self.denied('PUBLIC_FILE_UNAVAILABLE')


class LinkTests(ContractRoot):
    def test_symlinked_artifacts_and_pins_refused_without_following(self):
        for relative in (*PINS, *COVERED):
            with self.subTest(path=relative):
                self.setUp()
                path = self.root / relative
                target = self.base / 'SYMLINK_TARGET_SENTINEL'
                shutil.copyfile(path, target)  # Identical bytes behind the link.
                path.unlink()
                path.symlink_to(target)
                code, opened = self.probe()
                self.assertEqual(code, 'PUBLIC_FILE_UNAVAILABLE')
                self.assertIn(path.name, opened)  # The link itself was attempted...
                self.assertNotIn('SYMLINK_TARGET_SENTINEL', opened)  # ...never its target.

    def test_symlinked_directory_component_refused(self):
        docs = self.root / 'docs'
        real = self.base / 'SYMLINK_DIRECTORY_SENTINEL'
        docs.rename(real)
        docs.symlink_to(real, target_is_directory=True)
        code, opened = self.probe()
        self.assertEqual(code, 'PUBLIC_FILE_UNAVAILABLE')
        self.assertIn('docs', opened)
        self.assertNotIn('SYMLINK_DIRECTORY_SENTINEL', opened)

    def test_hardlinked_artifacts_and_pins_refused_before_bytes_are_read(self):
        # Bounded negative rejection test: the link lives only in this temporary
        # root and is never reused as a fixture (HELIX_NO_HARDLINKS_V1 exception).
        real_fdopen = os.fdopen
        for relative in (*PINS, *COVERED):
            with self.subTest(path=relative):
                self.setUp()
                path = self.root / relative
                os.link(path, self.base / 'HARDLINK_ALIAS_SENTINEL')
                linked = path.stat().st_ino
                reads = []

                class Recorder:
                    def __init__(self, stream):
                        self.stream = stream
                    def __enter__(self):
                        return self
                    def __exit__(self, *details):
                        return self.stream.__exit__(*details)
                    def fileno(self):
                        return self.stream.fileno()
                    def read(self, *args):
                        reads.append(os.fstat(self.stream.fileno()).st_ino)
                        return self.stream.read(*args)

                recorded = patch('repocp.safety.os.fdopen', lambda fd, mode: Recorder(real_fdopen(fd, mode)))
                with recorded:
                    self.denied('SINGLE_LINK_REGULAR_REQUIRED')
                self.assertNotIn(linked, reads)
                # Positive control: once single-link, the recorder sees this inode read.
                (self.base / 'HARDLINK_ALIAS_SENTINEL').unlink()
                with recorded:
                    self.assertEqual(contract.verify_agent_contract(self.root), COVERED)
                self.assertIn(linked, reads)


if __name__ == '__main__':
    unittest.main()
