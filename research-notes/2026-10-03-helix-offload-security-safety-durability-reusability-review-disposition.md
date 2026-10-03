# Disposition — helix-offload security, safety, durability and reusability review

Date: 2026-10-03

Research provenance: branch `codex/helix-offload-security-research-20261003`,
commit `4eae1b63e85cdfe42ff64a4ab149e2661ab86150`.

The externally researched report
[`2026-10-03-helix-offload-security-safety-durability-reusability-review.md`](2026-10-03-helix-offload-security-safety-durability-reusability-review.md)
and its source manifest are preserved unchanged. Verified SHA-256:

- report: `cb8605eaa5b44230edb61e5a11e526b996302bcc53248e3ff16a51af58a97974`;
- source manifest: `09953b5db41f66934f4d5370bf25a6e0054961a8430fe1dbafa2217c7a9f8d10`.

The research is a security/design review, not implementation, operational or
live-acceptance evidence. Its source manifest records retrieval date,
methodology and limitations. Canonical integration retains the research commit
as an ancestor rather than recreating its files.

## Adopted now

The top-ranked direct authority defect was grant replay: result-directory
exclusivity did not prevent reuse of the same one-use execution grant with a
new result directory or attempt ID. Canonical helix-offload
`d6c7f708fa5bee2845fbd11b67a946161898dfe1` implements the bounded remedy:
an immutable filesystem reservation keyed by canonical grant digest, exclusive
creation plus file/directory fsync, one common supported CLI boundary, and no
automatic release. Its synthetic race/crash suite passed 69/69 repository tests.

That implementation is independent verification evidence for the adopted slice;
this research report alone is not.

## Preserved follow-up sequence

These are candidates, not numbered Work Entries and not execution authority.
Their ordering reflects the reviewed dependency sequence, not an estimate of
effort or automatic scheduling:

1. durable submission/capture phases and crash reconciliation, building on the
   reservation key;
2. private recovery storage outside disposable checkout trees, with retention,
   backup and restore evidence;
3. allowlisted public evidence derivatives from protected originals;
4. one connector-accounting model applied consistently to OpenAI and OpenClaw;
5. protected OpenClaw prompt transport rather than process arguments;
6. preventive resource controls distinguished from retrospective usage checks;
7. prompt/data separation for historical authority facts and current host
   authority, plus evidence-based input-token accounting;
8. licensing, packaging, versioning, release verification and standalone
   adoption before external distribution.

The topology preserves these as one non-executing
`FUTURE_WORK_CANDIDATE_GROUP`; no entry numbers were allocated or inferred.

## Explicitly deferred

Distributed coordination, grant signatures, automatic retry/fallback, semantic
model judges, a daemon, queue, cache, MCP integration and broad orchestration
remain deferred. Their likely overhead and unresolved requirements exceed the
evidence for this first hardening slice.

Live effects: integration of the already-pushed research commit into the
authorized repo-cp publication containing this disposition. No model/API/GPU
call, credential access, installation, deployment or runtime mutation.
