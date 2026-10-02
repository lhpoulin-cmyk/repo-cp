# Work Entry 010 — DERP delivery record

Name: DERP — Deterministic Engine for Policy and Routing

Status: `COMPLETE` — implementation published and synthetically validated;
one Claude hosted test was sent but did not produce an accepted artifact

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

## Hosted testing slice

The earlier GPT-only authorization was evaluated but **NOT SENT** because its
production qualification, matching Work Entry 005 evidence and approved API
credential/account path were absent. Canonical helix-offload
`475bf31765395e3e4d6a233fd2f774301894463d` preserves that historical gate.

Louis then authorized a Claude-first hosted slice and required separate Claude
API/subscription and OpenAI API/subscription accounting. Canonical helix-offload
`6e02f1128a990dfc62e28da6adcc90143a2731cf` now contains:

- bounded Claude Messages API and Claude Code subscription adapters while
  preserving the OpenAI Responses adapter;
- billing-source and attempt identities in receipt V2;
- an exact `TEST_ONLY` qualification/admission path limited to the 38-byte
  Ada/Basic/`REF-42` extraction, live quality `UNPROVEN`, and no production or
  general routing eligibility;
- a content-bound LIVE grant and durable attempt evidence;
- a four-path support matrix, Claude-first packet and cuda-compute follow-up; and
- 42 passing tests plus a successful exact synthetic lifecycle.

One Claude Code invocation was **SENT** through the existing first-party
Claude.ai Pro login. The client returned an envelope, but the adapter rejected
it as `HOSTED_RESPONSE_INVALID`; no artifact reached postflight. Actual provider
model, usage, cost and underlying provider request count are `UNKNOWN`. The
caller made no resend. Human disposition remains `PENDING`. OpenAI was **NOT
SENT** because API credentials were absent and the subscription client could not
meet this slice's no-tools/no-retry boundary.

Post-call review found that Claude Code puts schema-constrained output in
`structured_output`; the adapter had read only `result`. It also found that the
consumed invocation's structured-output retry variable allowed one retry rather
than one total attempt, so an internal retry cannot be excluded. Both defects are
fixed and synthetically covered in the published revision. The fix is not
retroactive acceptance and grants no retry authority. Sanitized live evidence is
in helix-offload `docs/evidence/WORK_ENTRY_010_CLAUDE_LIVE_RESULT.md` and
`docs/evidence/work-entry-010-claude-live-20261001/`.
repo-cp's disposition is
[WORK_ENTRY_010_HOSTED_SLICE_20261001.md](WORK_ENTRY_010_HOSTED_SLICE_20261001.md).

## Recovery and corrected live call

The original attempt's client envelope was not recoverable from durable evidence
or safely available Claude Code session/output locations. Louis authorized one
corrected call. `work-entry-010-claude-live-002` was **SENT** once with a fresh
content-bound LIVE grant and zero configured retries, but its returned envelope
also failed `HOSTED_RESPONSE_INVALID`; again no artifact reached postflight.
Actual provider model, usage, cost and the precise rejected field remain
`UNKNOWN`, and human disposition remains `PENDING`. No resend or other provider
call occurred.

The full disposition is
[WORK_ENTRY_010_CLAUDE_RECOVERY_20261001.md](WORK_ENTRY_010_CLAUDE_RECOVERY_20261001.md).
Sanitized helix-offload evidence is committed at
`9ec732046ba6481be70018277b91ff04534baa8d` and published on review branch
`codex/work-entry-010-recovery`; canonical helix-offload main is still
`6e02f1128a990dfc62e28da6adcc90143a2731cf`, so that evidence is not claimed
merged or canonical.

## Acceptance boundary and next action

Delivery stage: **IMPLEMENTATION PUBLISHED / SYNTHETICALLY VALIDATED**.

Operational stage: **TWO LIVE REQUESTS SENT / ACCEPTANCE NOT ESTABLISHED**. DERP is not
operationally proven, and the 20% target has not been achieved. The Claude
authorizations were consumed and do not authorize another retry or cohort.

Exact next action is to make failed-envelope evidence bounded and recoverable,
then, only under a new explicit authority, run one diagnostic acceptance call.
The bounded cuda-compute packet is prepared but remains next only after the
hosted path produces an artifact suitable for human disposition.

Live effects: two separately authorized Claude Code invocations disclosed the
same synthetic Ada/Basic/`REF-42` input through Louis's existing Claude.ai Pro
allowance; both client envelopes were rejected locally. No artifact, accepted
output, OpenAI call, API-billed charge, manual retry, cohort, GPU workload,
generated-text publication, deployment, installation, credential/account change
or runtime configuration mutation occurred. The original hosted-slice review
branch and canonical helix-offload main were published non-forced at
`6e02f1128a990dfc62e28da6adcc90143a2731cf`; the follow-up sanitized evidence is
published only on review branch `codex/work-entry-010-recovery` at
`9ec732046ba6481be70018277b91ff04534baa8d`.
