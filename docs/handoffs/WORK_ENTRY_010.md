# Work Entry 010 — DERP delivery record

Name: DERP — Deterministic Engine for Policy and Routing

Status: `COMPLETE` — implementation published and synthetically validated;
the authorized hosted live-acceptance call was not sent

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

- helix-offload owns the portable DERP evaluator, bounded execution integration,
  artifact/receipt contracts and cohort calculations;
- repo-cp retains Louis's portfolio policy decisions, priorities, authority,
  work governance and evidence review; independent consumers supply their own
  policy and candidate evidence through portable interfaces;
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

DERP is helix-offload's governor: it applies explicit supplied policy through
preflight, recommendation, execution-limit checks, postflight and outcome
accounting. Adapters perform only separately granted execution. Louis grants
authority, accepts results and resolves exceptions. This purpose does not imply
a daemon, automatic dispatch, retry loop or additional control plane.

## Delivery

Canonical helix-offload `main` was independently queried after implementation
publication and resolved to `28c2dab305e05e18e053321f6a70df9de1b85485`. That revision contains:

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

The resumed slice adds the first usable portable path:

`prepare → preview → explicit grant → one adapter call → postflight → untrusted
artifact plus receipt → human disposition`.

`change-summary-v1` keeps lane `PORTFOLIO_REPOSITORY`, operation `DOCUMENT` and
job family separate. Its deterministic Git packer collects bounded revision/path
facts, normalized supplied validation receipts and allowlisted document excerpts.
Exact SHAs, statuses, authority values, paths and evidence references are checked
after generation; semantic adequacy remains human review. Cohort V2 records
eligible opportunities not routed as well as actual usage/cost,
preparation/review effort and observed versus estimated frontier displacement.

The machine-readable result is
[WORK_ENTRY_010_RESULT.json](WORK_ENTRY_010_RESULT.json). Detailed validation and
the live packet are in helix-offload at the published revision under
`docs/evidence/WORK_ENTRY_010_SYNTHETIC_VALIDATION.md` and
`docs/evidence/WORK_ENTRY_010_HOSTED_LIVE_ACCEPTANCE.md`. The resumed validation
is `docs/evidence/WORK_ENTRY_010_HOSTED_PATH_SYNTHETIC_VALIDATION.md`.

Externally supplied feature research is preserved at
`research-notes/2026-10-01-helix-offload-feature-research.md` with its source
manifest and a separate disposition record. Outcome forecasting/calibration is separately recorded at
`research-notes/2026-10-01-helix-offload-outcome-forecasting.md` as deferred
roadmap work; it was not implemented and cannot control routing.

The earlier externally supplied practical-workflow research report's full source
text was not available in this active session. It was not reconstructed from a
handoff and is not claimed as durably saved; only the complete feature-research
artifact identified by local commit `f9575a0fc7e9c8eab1c3e10f8073166cbf3be6e6`
was available, verified and published.

## Authorized live-acceptance gate

Louis subsequently authorized exactly one call from the published hosted packet,
including disclosure of its synthetic input and the bounded charge. The packet
matched that authority, but the call was **NOT SENT**. Production qualification
for the exact model/profile and matching Work Entry 005 `ADMITTED` evidence were
absent, and no approved credential descriptor or authenticated account/model/
billing path was available. Synthetic fixtures were not promoted to live
evidence, and no workflow, LIVE grant, result directory, artifact or receipt was
created.

Canonical helix-offload `475bf31765395e3e4d6a233fd2f774301894463d`
preserves the sanitized gate evidence. repo-cp's review is
[WORK_ENTRY_010_LIVE_ACCEPTANCE_GATE_20261001.md](WORK_ENTRY_010_LIVE_ACCEPTANCE_GATE_20261001.md).

## Acceptance boundary and next action

Delivery stage: **IMPLEMENTATION PUBLISHED / SYNTHETICALLY VALIDATED**.

Operational stage: **LIVE ACCEPTANCE NOT SENT**. DERP is not operationally proven,
and the 20% target has not been achieved. Under the exact one-call authority
already supplied, execution may proceed only after the packet's candidate,
access, price, admission, execution-grant, usage, deadline, and stop conditions
are freshly verified.

Exact call authority and synthetic-input disclosure approval were supplied, and
fresh official pricing remained within the local ceiling. The unresolved gates
are verified OpenAI project billing/access/rate limit for the named snapshot, an
approved credential injector that opens descriptor 3, an exact owner-accepted
qualified candidate and matching 005 admission identity. Only after those pass
may a matching LIVE grant and new result directory be created.

Live effects: normal non-forced publication of the feature-research branch and
records to repo-cp, plus the hosted-path review branch and ordinary fast-forward
to canonical helix-offload `main`, and publication of the sanitized NOT SENT gate
record at `475bf31765395e3e4d6a233fd2f774301894463d`; no model call, API charge,
GPU workload, generated-text publication, deployment, installation,
credential/account change, or runtime configuration mutation.
