"""Verify published agent work contract bytes. Fixed reviewed paths only.

The pins are published records, not trust inputs: each must equal the reviewed
anchors below before any contract artifact is read. A pin therefore cannot
nominate, add or remove a covered path, and consistent pin/artifact edits still
fail until this reviewed code changes. Reads use the anchors, never pin values.
"""
import hashlib

from .consumer import ROOT
from .safety import Denied, load, read_public

CONTRACT_ID = 'HELIX_AGENT_WORK_CONTRACT_V1'
RELEASE_PIN = 'pins/agent-work-contract.json'
CANDIDATE_PIN = 'pins/agent-work-contract-candidate.json'
RELEASE = {
    'release': '1.0.0',
    'path': 'docs/AGENT_WORK_CONTRACT.md',
    'sha256': 'a4838c4bfd8e1d27ed794c48ca1d475d76929309fabc212368234c4073df7674',
}
CANDIDATE = {
    'release': '1.1.0-rc.3',
    'base_release': '1.0.0',
    'base_commit': '4ede9b73501b38a2b0ba5a50c9c32875a2d0eb19',
    'path': 'docs/AGENT_WORK_CONTRACT_CANDIDATE.md',
    'sha256': 'ecf323a58e1943fed778054d954cd7defd00794f54f3d6eb314e76f1405c6e3c',
}
COMPANIONS = {
    'docs/HELIX_CONTROL_PLANE.md': '874499b04a7671d05a51a1a25e079f28a6f3ef0b1901d908a3abc2076477d96f',
    'docs/REPOSITORY_VOICE.md': 'c61dfbe8fb7d1ca660e7c9ff371b68f0200d175400d778a2c934a022792925ba',
}
# Exact published record bytes, including free-text fields. The structural
# checks below remain an independent layer if an anchor is ever updated.
PIN_SHA256 = {
    RELEASE_PIN: 'dfd31869a7de7453ca7ce9d5cd9fbe4b62bc8aa91220e63dbaa91ddc264cc061',
    CANDIDATE_PIN: '0f6d40463298a25a8cd086481845cb2c46693e4779434fc52d292984cdc2414b',
}
RELEASE_TEXT = ('authority', 'publication_custodian', 'approved_date', 'changes')
CANDIDATE_TEXT = ('status', 'requested_date', 'changes')
COVERED = {RELEASE['path']: RELEASE['sha256'], CANDIDATE['path']: CANDIDATE['sha256'], **COMPANIONS}


def pin(root, relative, anchors, text):
    raw = read_public(root, relative)
    if hashlib.sha256(raw).hexdigest() != PIN_SHA256[relative]:
        raise Denied('AGENT_CONTRACT_PIN_INVALID')
    try:
        data = load(raw)
    except Denied:
        # Malformed JSON, duplicate keys and oversize input are pin defects.
        raise Denied('AGENT_CONTRACT_PIN_INVALID') from None
    expected = {'contract_id': CONTRACT_ID, **anchors}
    if (type(data) is not dict or set(data) != set(expected) | set(text)
            or any(type(data[key]) is not str or not data[key].strip() for key in text)
            or any(type(data[key]) is not type(value) or data[key] != value
                   for key, value in expected.items())):
        raise Denied('AGENT_CONTRACT_PIN_INVALID')


def verify_agent_contract(root=ROOT):
    """Return the covered paths after both pins and all artifact digests match."""
    # Complete all metadata checks before reading any covered artifact bytes.
    pin(root, RELEASE_PIN, RELEASE, RELEASE_TEXT)
    pin(root, CANDIDATE_PIN, {**CANDIDATE, 'companions': COMPANIONS}, CANDIDATE_TEXT)
    for relative in sorted(COVERED):
        if hashlib.sha256(read_public(root, relative)).hexdigest() != COVERED[relative]:
            raise Denied('AGENT_CONTRACT_MISMATCH')
    return sorted(COVERED)
