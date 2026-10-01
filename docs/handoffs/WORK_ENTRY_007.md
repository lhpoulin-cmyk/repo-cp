# Work Entry 007 recovery and publication result

Status: COMPLETE

Capture date: 2026-10-01

Scope: recover and reconcile preserved repo-cp Work Entry 007 work, publish the
validated helix-offload Work Entry 005 candidate, correct the repo-cp agent
review-branch delivery gap, and preserve unrelated work.

## Sources and recovery

The durable private shutdown record remains at
`.agent-checkouts/codex/attribution-pilot-shutdown-20261001T1532Z/`. Its
`HANDOFF.md`, manifest, patch, validation log and checkout inventory were read
before mutation. The manifest bound 13 implementation paths to baseline
`4f47ec6cc4744eaf2a158009c57553a223432cdd`; their hashes still matched.

The implementation checkout supplied the authoritative reporter, schema,
proposal, fixtures and tests. The earlier checkout supplied two complementary
registration paths, `registries/work-topology.json` and
`tests/test_work_protocol.py`. Its other attribution paths were an older duplicate
and were not adopted. The registration and implementation were first preserved
as local commits `71c976a` and `7f13d83`, then replayed onto freshly verified
canonical repo-cp main as `da63458` and `2620089` in an isolated checkout.

The repo-cp primary checkout and the agent-contract candidate checkout contain
pre-existing work outside this publication. They were not staged, rewritten or
discarded. Work Entry 006's untracked `observation.json` also remains preserved.

## Published results

- helix-offload `3073fd4e4c552a692d506489597faaf3f5e1038a` implements Execution
  Admission V1. Canonical main advanced normally from
  `88b236aa16dd6e9db578e1ef9f52b0302cb7f835` to that commit.
- repo-cp implementation commit `2620089` preserves Stage 1 contribution
  reporting and explicit commit-executor attribution and Stage 2 supplied
  Git/account profile checks. Publication tip `88d2f71` also reconciles the
  delivery authority and requires evidence-backed isolated review-branch
  delivery without inferring canonical-main authority.
- The 19 accepted Foundation artifacts, repository/doctrine pins and enrollment
  remain unchanged. auth-cp and ansible-cp remain ENROLLED; foundation-cp remains
  DISCOVERED.

The earlier assertion defect was corrected by testing exact evidence states
instead of treating `verified` as a substring; raw regular-expression fixtures
remove invalid Python escape warnings. Tests were not weakened. Portfolio voice
and optional personal reflections remain separate from attribution records.

## Validation

repo-cp exact published candidate `88d2f71`:

- `tools/validate`: PASS; 13 Foundation tests and 211 repository tests.
- Focused attribution tests: 33 PASS.
- Focused Git identity tests: 7 PASS.
- Focused agent-rule tests: 3 PASS.
- JSON/schema, Python syntax, secret-indicator, `git diff --check` and complete
  diff review: PASS.

helix-offload exact published commit `3073fd4`:

- `PYTHONPATH=src python3 -B -m unittest discover -s tests -v`: 16 PASS.
- JSON parsing and Draft 2020-12 schema metaschema checks: PASS.
- Governance/source pin digests and relative Markdown links: PASS.
- Compilation with bytecode cache isolated under `/tmp`: PASS.
- Selected-profile identity membership, wrong identity/digest refusal,
  malformed Unicode and oversized-integer failure, supplied-result invariants,
  deterministic rendering and absence of process/network/runtime adapter paths:
  PASS.
- `git diff --check` and complete commit review: PASS.

The pinned helix-offload governance copy still links to upstream
`AGENT_WORK_ADOPTION.md`, which is absent from the local copied governance
directory. The exact pinned bytes were preserved; helix-offload instructions
explicitly retain upstream-relative link meaning, and the canonical repo-cp
release contains that file. This is not an Execution Admission V1 defect.

## Boundaries and effects

No runtime execution, model invocation, deployment, enrollment, account,
credential, identity, workstation or peer-repository configuration change
occurred. Git effects were limited to the authorized review-branch and ordinary
fast-forward canonical-main publications. No force push, history rewrite,
protection bypass or self-approval occurred.

Live effects: pushed repo-cp review branch `codex/reconcile-preserved-work`
through `702c3fc`; fast-forwarded repo-cp canonical main through `702c3fc`;
fast-forwarded helix-offload canonical main to `3073fd4`; deleted both merged
review branches after directly verifying their exact tips on canonical main.

## Final branch and checkout disposition

| Repository / branch or checkout | Disposition | Evidence and reason |
| --- | --- | --- |
| helix-offload `codex/005-execution-admission-v1` | Published, branch retired, checkout removed | Review branch and canonical main both resolved to `3073fd4` before retirement. |
| repo-cp `codex/reconcile-preserved-work` | Published, branch retired; checkout retained on clean `main` | Review branch and canonical main both resolved to `702c3fc` before retirement; retained checkout is the clean synchronized starting point. |
| repo-cp attribution registration / implementation checkouts | Recovered duplicates retired and removed | Patch IDs for `71c976a`/`da63458` and `7f13d83`/`2620089` matched exactly; canonical main contains the replayed commits and the private shutdown handoff remains. |
| repo-cp hardlink-policy-release, work-entry-003-review, work-entry-005 and work-entry-standard-002 checkouts | Merged duplicates retired and removed | Each checkout was clean and its HEAD was an ancestor of canonical main. |
| repo-cp primary checkout | Preserved | Dirty state predates this recovery. Some paths now match canonical bytes; other agent-contract candidate and guidance paths remain distinct and require their own scoped review before synchronization. |
| repo-cp agent-contract-publication checkout | Preserved | Dirty 1.1.0-rc.4 candidate/audit material is outside Work Entry 007. Its four dirty files are byte-identical to copies preserved in the primary checkout. |
| repo-cp work-entry-006 checkout | Preserved | Untracked `observation.json` is unrelated work. |
| repo-cp work-entry-009-gpu-pilot-prep checkout | Preserved | Dirty Work Entry 009/010 preparation appeared during final inventory and is unrelated concurrent work. |
| helix-offload `adr/0002-repo-cp-local-lane` primary checkout | Preserved | Local `da96e7a` is unrelated to Execution Admission V1 and is not on canonical main; its former remote branch is absent. |

The removed checkouts are recoverable from the cited canonical commits and the
preserved private handoff. No dirty unrelated checkout was deleted. Remote review
branches were removed only after direct evidence showed their exact tips on
canonical main.
