# auth-cp repository-only pilot

AUTH_CP_PILOT=REPOSITORY_ONLY
ENROLLED_REPOSITORIES=NONE
AUTOMATIC_EXECUTION=DISABLED
LIVE_MUTATION=NONE

Observed auth-cp main HEAD f84b7292659d6c4b14a4a1f767367343105a0cfa.
Canonical remote recorded from preflight:
git@github.com:lhpoulin-cmyk/auth-cp.git. Seven committed public metadata files
match reviewed digests in registries/repositories.json. No peer validator,
operational command, account, credential, host or custody operation was invoked.
The unrelated untracked contracts/ws-wowzer-win-observation.md was preserved.

[Machine report](auth-cp-audit.json), [human report](auth-cp-audit.txt), and
[review proposals](auth-cp-proposals.json) are captured repository observations.
Result: 27 check results, 25 PASS,
1 DRIFT, 0 BLOCKED, 1 UNKNOWN,
0 NOT_APPLICABLE. Overall DRIFT.
The RC008 finding identifies the auth-cp B70 handoff's earlier Foundation
repository pin fb129f747c5c9eabaadb8b7c09e433f5b071af4b, while the doctrine pin
still matches d2fe6c6291ea1eaffadb15ded6c0240fed0e96ca. This requires owner
compatibility review, not automatic pin replacement or altered admission.
RC009 is UNKNOWN because the runtime audit does not query remotes.

Two consecutive audits produced identical results and unchanged peer Git status.
Audit JSON SHA-256: 95ebd4427ac785cd6e73c24beaaa3afc2d9770f7546d25a8e1072fda5c5fd15e.
Synthetic tests independently hash all temporary checkout files before and after
two audits and prove zero changes, including no command execution.

The two tests/fixtures/auth-cp JSON declarations and their golden text outputs
are synthetic presentation fixtures, not live observations or approvals.
BLOCKED has no command; READY_FOR_REVIEW proposes a bounded public revision
inspection, never executed by rendering. Both use real accepted Foundation pins.
Negative tests cover invalid parsing, pins, versions, text, sizes, integrity and
non-disclosing atomic denial. Foundation's 13 reference cases and repo-cp's 30
consumer/audit cases pass (43 distinct tests).

Next exact approval decision: Louis approves or declines enrollment of auth-cp
alone for the seven listed public metadata files at the reviewed source revision,
after its owner reviews RC008. The [exact proposed registry diff](../proposals/auth-cp-enrollment.patch) and
[approval gate](../proposals/auth-cp-enrollment.md) are prepared for separate
review. They remain unapplied; this pilot is not enrollment approval.
No live command, APPLY, credential issuance/adoption or operational gate is open.
