# Checkout cleanup — 2026-10-01

## Scope and remote baseline

This record completes checkout cleanup only. It does not implement DERP.

Before mutation, direct remote queries and fresh fetches resolved repo-cp
canonical `main` to `83c07506cd23f6fc6e1aed2be46cb45a075ab301` and
helix-offload canonical `main` to
`3073fd4e4c552a692d506489597faaf3f5e1038a`. No Git lock or other active
writer was found in the inventoried checkouts. Applicable repository guidance,
the pinned Agent Work Contract, and the prior Work Entry 007 and efficiency
reconciliation records were read before mutation.

## Checkout and branch disposition

| Repository / checkout or branch | State found | Disposition |
| --- | --- | --- |
| repo-cp primary `/home/louis/helix-arpa/repo-cp` | local `main` `25be360`, 0 ahead/25 behind fresh `origin/main`, 4 tracked modifications and 12 untracked files | Exact bytes and hashes published on recovery branch `codex/recovery-pre-cleanup-primary-20261001` at `018efb16f9273aea072bc2286a3a53d807a54cef`; primary then fast-forwarded cleanly to canonical main. |
| repo-cp `.agent-checkouts/codex/agent-contract-publication` | `b9e528d`, 0 ahead/23 behind `origin/main`; 3 modified and 1 untracked file | Retired. All four dirty files were byte-identical to files in recovery commit `018efb16`; the base commit is an ancestor of main. |
| repo-cp `.agent-checkouts/codex/efficiency-priority-reconciliation` | clean `83c0750`, review upstream at the same commit | Checkout retired and merged/main-equivalent remote review branch deleted. |
| repo-cp `.agent-checkouts/codex/reconcile-preserved-work` | clean local `main` `d46ac50`, 4 behind `origin/main` | Retired after the primary checkout was clean and synchronized. Its HEAD is an ancestor of main. |
| repo-cp `.agent-checkouts/codex/work-entry-006` | `c2a3e12`, 0 ahead/12 behind `origin/main`; one untracked `observation.json` | Observation preserved byte-for-byte in the private recovery bundle below; checkout retired after comparison and hash verification. |
| repo-cp `.agent-checkouts/codex/work-entry-009-gpu-pilot-prep` | clean `37a8462`, review upstream at the same commit, 2 behind main | Checkout retired and merged remote review branch deleted; `37a8462` is an ancestor of main. No GPU workload was run. |
| repo-cp earlier Work Entry 007 registration/implementation, hardlink-policy-release, work-entry-003-review, work-entry-005, and work-entry-standard-002 checkouts | Already retired by the preceding reconciliation after duplicate/ancestry proof | Remain retired; canonical commits and the attribution shutdown handoff remain. See `docs/handoffs/WORK_ENTRY_007.md`. |
| repo-cp `.agent-checkouts/codex/attribution-pilot-shutdown-20261001T1532Z` | non-Git durable handoff | Retained unchanged as historical recovery evidence. |
| repo-cp `.agent-checkouts/codex/checkout-cleanup-recovery-20261001` | private recovery bundle created by this cleanup | Retained; contains the Work Entry 006 observation plus provenance and restoration instructions. |
| repo-cp `.agent-checkouts/codex/contract-rollout-20260922.md` | non-Git historical record | Retained unchanged. |
| repo-cp `.agent-checkouts/codex/repo-voice/BASE_REPO_VOICE.md` | non-Git historical source record | Retained unchanged. |
| repo-cp `policy/work-entry-and-status-topology` | remote `2d172c5`, 1 unique commit and 17 behind the starting main | Preserved as unrelated unpublished policy work; no checkout retained. |
| repo-cp `codex/recovery-pre-cleanup-primary-20261001` | `018efb16`, published review/recovery branch | Retained explicitly for the unfinished `1.1.0-rc.4` candidate and other primary-checkout bytes. It is preservation, not an instruction to merge wholesale. |
| repo-cp `release/repository-creation` | remote branch whose tip was an ancestor of main | Deleted as merged and redundant. |
| helix-offload primary `/home/louis/helix-arpa/helix-offload` | clean `adr/0002-repo-cp-local-lane` at unique `da96e7a`, no upstream; 1 ahead/1 behind main | ADR branch published and verified at `da96e7a3e068b543921049d0b31ea39a6bad46f4`; primary switched to `main` and fast-forwarded cleanly to `3073fd4`. |
| helix-offload `adr/0002-repo-cp-local-lane` | unrelated unique ADR commit | Retained locally and remotely with explicit upstream; 1 ahead/1 behind main. It was not merged by this cleanup. |
| helix-offload `codex/005-execution-admission-v1` checkout/branch | Already published to main and retired by the preceding reconciliation | Remains retired; canonical main is `3073fd4`, which contains the feature commit. |

## Recovery integrity

The primary recovery commit includes
`docs/handoffs/CHECKOUT_RECOVERY_PRIMARY_20261001.md`, which records the source
checkout, all 16 preserved file hashes, classification, and restoration steps.
Direct `ls-remote` verification resolved the recovery branch to `018efb16`.

The private observation bundle is
`.agent-checkouts/codex/checkout-cleanup-recovery-20261001/`:

- `MANIFEST.md`: SHA-256
  `b5f6850c81e95c8fa2212b441970782af50faccd944ec26373071daddb89cb83`
- `work-entry-006-observation.json`: SHA-256
  `8f863553f3549d070cbf6053bc5be71e613960951a23f0fa1179ef593f5731a2`

The observation copy passed byte-for-byte comparison with the source before the
source checkout was retired. Its manifest includes exact provenance and
restoration instructions.

Retained historical evidence hashes were also rechecked:

- contract rollout record:
  `e47cbff5369ae65f5858a371385b3fe55c3ee7350d3524f3df1a8fb3536621a1`
- repository voice source:
  `1d84708396418f5ffd977162140a73f2d8d6c49b6fde44544450ff8e81f291be`
- attribution shutdown bundle files, in filename order shown by `sha256sum`:
  `efc8612d…`, `ffc675b5…`, `0ebbfea1…`, `993492dd…`, `cd67a2a5…`

## Validation and effects

- repo-cp `tools/validate`: PASS; metadata/syntax/schema checks passed,
  Foundation suite 13/13 passed, repository suite 211/211 passed,
  `AUTOMATIC_EXECUTION=DISABLED`, `LIVE_MUTATION=NONE`.
- helix-offload `python3 -m pytest -q -p no:cacheprovider`: 16/16 passed.
- Recovery snapshot: `git diff --check` passed and all preserved file hashes
  matched the pre-commit inventory.
- No credentials, accounts, runtime configuration, live systems, model jobs or
  GPU workloads were touched. Live effects were limited to Git branch/main
  synchronization, preservation pushes, review-branch retirement, and checkout
  removal after uniqueness proof.

The reliable next-session environment is the repo-cp primary checkout on clean
canonical `main`. DERP remains a separate, unstarted task.
