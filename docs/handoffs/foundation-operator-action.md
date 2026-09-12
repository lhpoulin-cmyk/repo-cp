# Foundation handoff: missing operator-action authority

PLAY: repo-cp fleet governance bootstrap
CHECKPOINT: mandatory authority discovery before implementation
STATUS: BLOCKED
RESULT: evidence and handoff only; bootstrap acceptance is not achieved

## Exact stop

```text
BLOCKER=FOUNDATION_OPERATOR_ACTION_CONTRACT_MISSING
operation=consume HELIX_OPERATOR_ACTION_CONTRACT_V1 for repo-cp terminal renderer
observed=contract absent from Foundation committed tree and inspected checkout
expected=published Foundation contract with authoritative consumer semantics
authority=Louis bootstrap instruction 8; Foundation owns shared contracts
why_not_ordinary_debugging=creating replacement semantics in repo-cp would invent competing doctrine
```

This is a handoff request, not a proposed replacement contract. Foundation
changes require a separate authorized Foundation task. No peer file is changed.

## Verified repository evidence

Preflight observed host `ws-hadrian`, user `louis`, path
`/home/louis/helix-arpa/repo-cp`, branch `main`, clean worktree, upstream
`origin/main`, and initial HEAD `2f309d732d34344930cd895ba0584bb154a6c6da`.
Canonical fetch/push origin is
`https://github.com/lhpoulin-cmyk/repo-cp.git`. Direct `git ls-remote origin
HEAD refs/heads/main` returned that same hash for both refs. The initial
sandbox DNS failure was resolved by an approved network-capable read; it is
not the blocker.

Foundation canonical origin is
`git@github.com:lhpoulin-cmyk/foundation-cp.git`. Direct remote HEAD and
`refs/heads/main` both matched its checkout HEAD:
`fb129f747c5c9eabaadb8b7c09e433f5b071af4b`.
The active doctrine content last changed at
`d2fe6c6291ea1eaffadb15ded6c0240fed0e96ca`; the diff of
`docs/ACTIVE_DOCTRINE.md` and `registries/active-doctrine.json` between those
revisions is empty. Neither supplied revision has advanced in its respective
role. The repository revision adds execution profiles; it does not replace
the consolidated doctrine content revision. See the separate
[repository pin](foundation-repository-pin.json) and
[doctrine pin](foundation-doctrine-pin.json).

Read the parent AGENTS.md, portfolio execution doctrine, Foundation AGENTS.md,
README, OWNERSHIP, PROVENANCE, VERSION, active doctrine and registry, active
doctrine schema, execution-profile documentation/schema/implementation, and
tools/validate. Sibling guidance and related gates were inspected read-only.

The exact committed-tree search was:

```sh
git -C /home/louis/helix-arpa/foundation-cp grep -n -i \
  -e HELIX_OPERATOR_ACTION_CONTRACT_V1 -e 'operator.action' \
  fb129f747c5c9eabaadb8b7c09e433f5b071af4b --
```

It returned no matches (exit 1). A checkout search across Foundation,
auth-cp, ansible-cp and arpa-docs found no named contract. Foundation's
committed contracts are `b70-encode-matrix-observer-custody-v1.md` and
`foundation-signer-request.md`; its schemas cover active doctrine, custody
manifests and execution profiles. No universal operator-action renderer was
located in the inspected Foundation source, auth tools or ansible scripts.

Related existing mechanisms are not substitutes:

* Foundation `src/execution_profiles.py` validates public session declarations
  and emits structured conformance blockers; it grants no execution authority.
* auth-cp `schemas/account-mutation-gate-v1.schema.json` describes account
  changes with commands, authorization, rollback, lockout and idempotence
  evidence. `tools/principal_model.py` emits JSON with mutation authorization
  false. These are account-domain mechanisms, not the missing universal contract.
* ansible-cp `roles/apply-acknowledgement/tasks/main.yml` asserts the exact
  `APPLY <operation> <target>` acknowledgement. It is an Ansible guard, not a
  universal clean terminal renderer.

Peer observations: auth-cp HEAD
`f84b7292659d6c4b14a4a1f767367343105a0cfa`; ansible-cp HEAD
`4c40a0ef8aaf820dfec4b8562d4f5b39bd89eb86`.
Unrelated dirty state was preserved: Foundation untracked
`docs/WINDOWS_BACKUP_CUSTODY.md`; auth-cp untracked
`contracts/ws-wowzer-win-observation.md`; ansible-cp modified
`docs/SEMAPHORE_RECOVERY.md` and `docs/WS_WOWZER_WIN_ADMISSION.md`.
No peer validation or operational action was executed.

## Requested Foundation delivery

In a separately authorized Foundation task, locate and publish the real
`HELIX_OPERATOR_ACTION_CONTRACT_V1`, or establish it there under Louis's
authority, with its versioned schema, validator, compatibility guidance,
authoritative renderer/reference behavior and deterministic positive and
fail-closed fixtures. Return exact canonical repository and doctrine content
revisions separately, paths, validation results and direct publication parity.

The consumer requirements below come from Louis's bootstrap request and are
acceptance inputs for that handoff, not locally invented Foundation semantics:
repository/target identity; phase/status; stop reason; collected evidence;
exact copyable command; scope/effects/risks/downtime/removals; preconditions;
success/failure evidence; recovery/rollback; exact output Louis should return;
and explicit confirmation that execution has not occurred.

No operational command is proposed while this authority is missing. There
are no execution preconditions to satisfy by running a live action. Execution
has not occurred. Effects, downtime and removals: NONE. The next work is
repository-only Foundation contract preparation, not an operator live ceremony.

## Resume, pilot and recovery

After the Foundation handoff, recheck current HEAD, status, history, canonical
remote parity and both distinct pins; review any advances for compatibility.
Do not treat a matching contract name alone as validated authority. Then
implement the originally requested policy/model, inventory/enrollment schema,
stable checks/results, report-only validator, contract consumer/renderer,
fixtures/tests, secret-safe checks, CI and operating documentation. Complete
the full suite, focused tests, syntax and secret checks, diff review, cohesive
commits and authorized publication with direct parity evidence.

Pilot candidate: `auth-cp`, **PROPOSED / NOT ENROLLED**. Its observed maturity
includes ownership/provenance/version, repository-native validation, versioned
schemas, explicit Foundation pin consumption, account conformance blockers and
revision-handoff discipline. Selection is provisional; no conformance pass or
live readiness is claimed. Begin with explicitly bounded read-only committed
metadata checks after Foundation compatibility is established. Discovery never
enrolls a repository. All other repositories remain unenrolled.

Louis retains exception, approval and merge authority. No exception bypass of
the missing contract is inferred. Later remediation proposals must identify
the owning authority and Foundation source, exact patch and scope, test and
idempotence evidence, reversal plan and review path; they must never self-merge.

This documentation-only handoff can be superseded by a reviewed follow-up
commit. No runtime rollback is required and history rewriting is unnecessary.
Remaining unknowns are the actual contract/schema/renderer paths and semantics,
their version compatibility, and fleet conformance. No bootstrap validator or
test suite exists yet; a documentation check cannot establish bootstrap success.

Live observations: NONE. Live mutations: NONE. Secret access: NONE.
Infrastructure effects: NONE. Peer repository mutations: NONE.
Repository mutations are limited to this handoff, its two observation pins,
README status, and their authorized commit/publication.
