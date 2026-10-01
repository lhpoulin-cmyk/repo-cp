# Primary-checkout recovery snapshot — 2026-10-01

This branch preserves the exact dirty state found in the primary `repo-cp`
checkout before checkout cleanup. The source checkout was
`/home/louis/helix-arpa/repo-cp`, on local `main` at
`25be360064f87d5cef52e5304da332861a9980e9`. Freshly fetched canonical
`origin/main` was `83c07506cd23f6fc6e1aed2be46cb45a075ab301`; the source was 25 commits
behind and had no commits ahead.

The files include superseded copies of already-published documents and an
unfinished `1.1.0-rc.4` contract-candidate/audit-preparation set. This is a
preservation snapshot, not acceptance or publication of that candidate.

## Preserved files

| Path | SHA-256 |
| --- | --- |
| `AGENTS.md` | `7c39301f18b0a4c9ef78736197cec8e6397a84dd494dbc462bded875b8faaea0` |
| `OWNERSHIP.md` | `3b2b7e11a462c33943568c3a8dce4b1e4b638c38d62a3fdab795ae968ec82c83` |
| `PROVENANCE.md` | `7d1cefc35ae98eda6d9946409ee6cbbabf1b056c6e19c36152886d82f854da1a` |
| `README.md` | `099827b8b080cc345a013d4406be92ab561985ab9743478da7d6f97c78ecc31d` |
| `.gitignore` | `8a4f65fb30e7b42498b44102291307af164bbb9c0d60135f11cff93e638d4a85` |
| `CLAUDE.md` | `a73acc92c018c1eefcab10277695da824c07413d2b7908b6d6b7f2e32c662afb` |
| `docs/AGENT_CHECKOUT_RULES.md` | `1754c2769672d14072971e762ccfaaa14db2f6f0b49a75881f2a71919fc5a0c9` |
| `docs/AGENT_WORK_ADOPTION.md` | `1cefb59ca5ddd556a9f365088c5d615a9dcba4bc23974e7bdef1aec7ebcf15ef` |
| `docs/AGENT_WORK_CONTRACT.md` | `a4838c4bfd8e1d27ed794c48ca1d475d76929309fabc212368234c4073df7674` |
| `docs/AGENT_WORK_CONTRACT_CANDIDATE.md` | `ffa68e0701562fa05a14b54637515ec4f8e8d5df33d8e78f7d1834ad46821f2d` |
| `docs/HELIX_CONTROL_PLANE.md` | `874499b04a7671d05a51a1a25e079f28a6f3ef0b1901d908a3abc2076477d96f` |
| `docs/REPOSITORY_VOICE.md` | `7b7b5c04b4a07fd8ca0300c0144138eb475cb56e2924a34bc86c728c1ef95ddb` |
| `docs/handoffs/repo-cp-audit-remediation-20260923.md` | `56b1fba53bfd6d0b136928af6e5e15d1770a9c0d5cfe66970e509318b064a72b` |
| `pins/agent-work-contract-candidate.json` | `84678e2865c6250a1f4d280e0fa479ae2716d502bbee7f2c16dc4794d625b37b` |
| `pins/agent-work-contract.json` | `dfd31869a7de7453ca7ce9d5cd9fbe4b62bc8aa91220e63dbaa91ddc264cc061` |
| `tests/test_validation_scope.py` | `070feb91710912e42f14a4114a2f6277ebfaf7524ca228b7c9ae70ec532d41b4` |

## Provenance and duplication

The four dirty files in the separate
`.agent-checkouts/codex/agent-contract-publication` checkout were byte-identical
to the corresponding files here: the contract candidate, repository voice,
candidate pin, and audit-remediation handoff. The other source files were found
only in the primary dirty checkout or matched older/published history.

## Restoration

Fetch the repository and switch to the published preservation branch
`codex/recovery-pre-cleanup-primary-20261001`. Verify the file hashes above
before selecting any content for a new review branch. Do not merge this snapshot
wholesale: compare individual files with then-current canonical `main` and apply
the normal contract-review and validation process.
