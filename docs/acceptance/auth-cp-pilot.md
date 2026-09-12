# Current auth-cp repository-only pilot

Refreshed 2026-09-12 after completed RC008 owner review.
AUTH_CP_PILOT=REPOSITORY_ONLY; ENROLLMENT=PILOT; ENROLLED_REPOSITORIES=NONE.
AUTOMATIC_EXECUTION=DISABLED; LIVE_MUTATION=NONE.

## Source and owner disposition

Canonical auth-cp main: `57815b15533ace72ee3ab2aef82fe3b764925652`. Previous reviewed source:
`f84b7292659d6c4b14a4a1f767367343105a0cfa`. Nested policy: `c36ec1e23fcd8ec11818a054374de3a6f64e1d4b`.
Canonical remote was fetched; local HEAD and origin/main already matched the
verified direct remote HEAD/main. An ancestry check passed; no merge or peer
worktree update was needed. No reset, stash or history rewrite was used.

The exact upstream commit changes only registries/b70-revision-handoff.json,
replacing foundation.revision with
`999fcf6a4bf181bdba201e9ca0c2f2bc4e7e2af5`. All other handoff values remain equal:
doctrine
`d2fe6c6291ea1eaffadb15ded6c0240fed0e96ca`, version 1.0.0; B70 identity,
policy and closed credential/adoption/APPLY gates unchanged. No target-facet
authority was supplied or inferred. Disposition COMPATIBLE is recorded in the
upstream commit message and [owner-review receipt](rc008-owner-review.json).

Only the pilot source revision and handoff SHA-256 changed in the inventory.
The other six public digests, states, scope and null enrollment approval are
unchanged. The [current proposal](../proposals/auth-cp-enrollment.md) lists all
seven exact filenames and digests. Original pilot reports and proposals at
repo-cp 904a5fd08b26465dd33ea3dea2e5859c04c789c6 are superseded historical
snapshots retained in Git. The original bootstrap DELIVERY.md and synthetic
action fixtures describe that historical bootstrap, not current audit findings.

## Audit evidence

[JSON](auth-cp-audit.json), [human report](auth-cp-audit.txt), and
[review artifacts](auth-cp-proposals.json) were regenerated.
RC001, RC002, RC003, RC007 and RC008: one PASS each.
RC004, RC005 and RC006: seven PASS each. RC009: one UNKNOWN.
Overall UNKNOWN: 27 findings, 26 PASS, 0 DRIFT, 0 BLOCKED, 1 UNKNOWN,
0 NOT_APPLICABLE. RC008=PASS / HANDOFF_PINS_MATCH.

Two consecutive audits returned identical data and unchanged peer HEAD/status
and unrelated public-document digests. Audit JSON SHA-256:
`6ae6c01efae0829e60df0b843119dd1b54d28a47e363e60c1aca88c0443d4b8a`. Offline RC009 remains UNKNOWN even though this separate
operator-authorized refresh verified direct remote parity. No audit network
capability or new freshness policy was introduced.

Existing tests cover negative conformance, deterministic no-change audits,
and isolated enrollment patch apply/repeat-denial/reversal. Full suite: 43 tests
(13 Foundation, 30 consumer/audit); focused AuditTests: 17 tests. Syntax/data,
schema, indicator and diff checks passed: 11 Python files, 17 JSON files,
2 schemas, 1 YAML file and 57 files scanned with zero indicators. No runtime code,
Foundation pins or vendor artifacts changed.

## Pending decision and effects

Only Louis's approval of the [new exact proposal](../proposals/auth-cp-enrollment.md)
remains; no approval is recorded and the patch is unapplied. Repository state is
PILOT. No peer validators, operational actions, credentials or target operations
were invoked. Unrelated auth-cp observation documents and Foundation/ansible-cp
work remain untouched. Peer worktree mutations, enrollment, live observation,
live mutation, secret access, issuance/adoption and infrastructure effects: NONE.
