# Work Entry 010 — DERP delivery record

Name: DERP — Deterministic Engine for Policy and Routing

Status: `COMPLETE` — implementation published and synthetically validated;
live acceptance not run

Priority: `GREEN` (normal attention)

Operator health: `BLUE` — preserved as historical operator context. It is not a
priority, readiness, or live-acceptance result.

## Recovery provenance

Louis's 2026-10-01 recovery instruction established that Work Entry 010 belongs
to DERP. The first recovery pass found no implementation artifact and therefore
recorded only the supplied name and health. The machine-readable
[WORK_ENTRY_010.json](WORK_ENTRY_010.json) remains the historical recovery input;
its absent-authority and unknown-owner statements describe that capture time,
not the later implementation authority.

The capacity assessment that briefly used 010 was renumbered to 011 without
rewriting its immutable history. The mapping remains in
[WORK_ENTRY_010_011_RENUMBER.md](WORK_ENTRY_010_011_RENUMBER.md).

## Accepted scope and ownership

Louis's later Work Entry 010 instruction supplied the previously missing scope,
ownership, and authority:

- helix-offload owns the DERP evaluator and bounded execution integration;
- repo-cp retains policy decisions, authority, work governance, and evidence
  review;
- DERP recommends among supplied, already-admissible candidates and cannot grant
  admission or execution authority;
- hosted execution is adapter-isolated and requires an exact admission result
  plus a separate execution grant;
- local-model and GPU execution, deployments, account or credential changes,
  automatic retries, frontier calls, dispatch, and publication are outside the
  implementation's runtime behavior.

The accepted implementation refines the earlier
[smallest-useful-slice proposal](../proposals/derp-smallest-useful-slice.md)
without creating a competing admission, attribution, telemetry, or orchestration
system. It reuses Work Entry 005 candidate identities and explicit admission,
keeps Work Entry 006 as advice rather than authority, and carries Work Entry 007
attribution fields into receipts where applicable.

## Delivery

Canonical helix-offload `main` was independently queried after publication and
resolved to `c1a1c89f4d54d695adf6675e97c045a31267f29d`. That revision contains:

- versioned schemas for workflows, recommendations, receipts, and measurements;
- deterministic preflight and recommendation with precise `UNKNOWN` and
  `REFUSED` outcomes;
- separate fake and bounded OpenAI Responses adapters;
- document, inference, and isolated light-coding postflight checks;
- attributable receipts with hashes, admission references, usage, cost, attempt
  history, evidence gaps, and frontier-review recommendations;
- a measurement ledger that separates completion, observed displaced frontier
  usage, total usage/cost, elapsed time, retries, intervention, review effort,
  and estimates; and
- one concrete hosted live-acceptance packet that was prepared but not run.

The machine-readable result is
[WORK_ENTRY_010_RESULT.json](WORK_ENTRY_010_RESULT.json). Detailed validation and
the live packet are in helix-offload at the published revision under
`docs/evidence/WORK_ENTRY_010_SYNTHETIC_VALIDATION.md` and
`docs/evidence/WORK_ENTRY_010_HOSTED_LIVE_ACCEPTANCE.md`.

## Acceptance boundary and next action

Delivery stage: **IMPLEMENTATION PUBLISHED / SYNTHETICALLY VALIDATED**.

Operational stage: **LIVE ACCEPTANCE NOT RUN**. DERP is not operationally proven,
and the 20% target has not been achieved. The next action is a separately
authorized execution of the exact hosted acceptance packet after its candidate,
access, disclosure, price, admission, execution-grant, usage, deadline, and stop
conditions are freshly verified.

Live effects: Git review-branch publication and ordinary non-forced publication
to canonical helix-offload `main`; no model call, GPU workload, deployment,
installation, credential/account change, or runtime configuration mutation.
