# ansible-cp repository-only pilot

Louis authorized PILOT preparation, not enrollment. Evidence label:
`Louis:repo-cp-ansible-cp-repository-only-pilot`.
Source: `4c40a0ef8aaf820dfec4b8562d4f5b39bd89eb86` on canonical main.
The preflight verified local/upstream/direct canonical remote parity before mutation.
All six accepted public files match committed source bytes. No peer tool ran.

## Reviewed scope

| File | SHA-256 or observed absence |
| --- | --- |
| AGENTS.md | 9cd4a451f53c408f88e77d7b07253d4fcdc61af159b79cc9cd3613c17c0506cc |
| OWNERSHIP.md | ABSENT; UNKNOWN, no accepted digest |
| PROVENANCE.md | ABSENT; UNKNOWN, no accepted digest |
| README.md | 885a5ba507b3a0599a4f845ef9e2effb8e7f10f7e8cdabb09a8c93d1139983b8 |
| VERSION | ABSENT; UNKNOWN, no accepted digest |
| contracts/linux-guest-admission/b70-doctrine-reconciliation.json | 6b67c6b2a7d9d6111aee0adeb3dae221d381da32432712388c2f46ffad599e26 |
| contracts/linux-guest-admission/b70-revision-handoff.json | 4bd6566b72af51bdb1953dab0f6e419761b6d318005b7aaedf8dfdbeb9888d0b |
| docs/AUTHORITY.md | a6d31c3299d2954eaf75ad5741e385d31dde405fca642f1e9ef74d39690ea064 |
| scripts/validate | d0ba8178dc4269932ad5d4ce611491cbd2fae3e2f5716803d903faf1e1664055 |

AGENTS.md and README.md establish mission and working boundaries; docs/AUTHORITY.md
establishes realization-only authority. scripts/validate records the validation
entry point as public evidence: it is never executed by this audit. The two B70
JSON records supply existing machine-readable Foundation/auth revision evidence.
The three absent root metadata files are not invented or silently substituted.
Their absence is UNKNOWN under local readiness checks, not a claim that Foundation
universally requires those filenames. VERSION consequently remains UNKNOWN.

## Findings

| Check | Results |
| --- | --- |
| RC001 | 1 PASS |
| RC002 | 1 PASS |
| RC003 | 1 PASS |
| RC004 | 6 PASS, 3 UNKNOWN |
| RC005 | 6 PASS |
| RC006 | 6 PASS |
| RC007 | 1 UNKNOWN |
| RC008 | 2 DRIFT |
| RC009 | 1 UNKNOWN |
| RC010 | 2 DRIFT |

Overall: DRIFT. Counts: {"BLOCKED": 0, "DRIFT": 4, "NOT_APPLICABLE": 0, "PASS": 21, "UNKNOWN": 5}.
RC008 preserves two Foundation repository-pin differences: the handoff and
reconciliation each reference `57aaa67489040e65afc267eb2daeaa9af262dbf4`,
versus accepted `999fcf6a4bf181bdba201e9ca0c2f2bc4e7e2af5`.
Both doctrine pins already match `d2fe6c6291ea1eaffadb15ded6c0240fed0e96ca`.
RC010 preserves two auth revision findings: both derived policy references are
`92556f2f0b269e7dda91155a54cf471d3db668ad`, versus separately reviewed policy
`c36ec1e23fcd8ec11818a054374de3a6f64e1d4b`. The reconciliation's observed
published source is `85546a420c8c4b8b5f9841c05f0984c2aa0340b4`, versus containing
handoff `57815b15533ace72ee3ab2aef82fe3b764925652`.
These findings require owner review; a containing commit is not a policy commit.
RC009 stays UNKNOWN: direct operator preflight is not incorporated into offline
runtime freshness semantics. No target-facet authority is supplied or inferred.

## Determinism and effects

Two consecutive `tools/repo-cp audit --pilot --repository ansible-cp` runs returned
exit 1 (DRIFT) and byte-identical JSON with SHA-256
`6a3ce78c2aade7590cdbb1c8996c9feabdca4752d230dadce873ca1bffaaf689`.
[Machine receipt](ansible-cp-pilot.json) records unchanged peer HEAD/status and
preserved hashes of the two unrelated dirty ansible documents. auth-cp's untracked
observation document and Foundation's untracked custody document remain untouched.
[Machine audit](ansible-cp-audit.json) and [human audit](ansible-cp-audit.txt)
retain every finding; [machine proposals](ansible-cp-proposals.json) authorize no
mutation and contain no patch.

Inventory: auth-cp alone ENROLLED; ansible-cp PILOT; Foundation DISCOVERED provider.
No enrollment proposal is justified while four DRIFT results remain unresolved.
See [owner review proposals](../proposals/ansible-cp-remediation.md).
Enrollment, peer mutation, live observation, live mutation, credential operations,
secret access and infrastructure effects: NONE. Automatic execution: DISABLED.
B70 remains not admitted; no desired-state, execution or APPLY gate changed.

Reversal is a reviewed repo-cp follow-up restoring DISCOVERED and removing the
pilot scope while preserving these historical reports; no runtime rollback exists.

## Validation

`tools/validate`: PASS, 52 tests (13 accepted Foundation tests and 39 repo-cp
consumer/audit tests). Metadata checks: 69 files scanned for secret indicators,
12 Python syntax checks, 23 strict JSON parses, 2 schemas and 1 YAML parse.
Focused `test_ansible_pilot.AnsiblePilotTests` and `test_consumer.AuditTests`:
26 tests PASS. The nine new synthetic pilot tests cover authorization, absent
metadata, enrollment denial, distinct revision roles, stale/unavailable evidence,
missing pinned files, unaccepted new content, malformed input and no execution or
writes. The default auth-cp audit is byte-identical to its enrolled acceptance
report (26 PASS, 1 UNKNOWN). `git diff --check` and complete diff review passed.
