# Work Entry 015 — first useful local change-summary-v1

Status: `COMPLETE`

Priority: `GREEN` (normal attention)

Scheduling eligibility: `INELIGIBLE_STATE`

## Objective

Use helix-offload/DERP to produce one bounded, evidence-grounded review summary
of the published local OpenClaw integration and accepted disposition. The exact
source range is
`9ec732046ba6481be70018277b91ff04534baa8d..ca9998755a463980bf9f618338d4e9303cd1f7bc`,
which contains only the local integration and accepted-disposition commits after
the hosted recovery baseline.

Lane is `PORTFOLIO_REPOSITORY`, operation is `DOCUMENT`, and job family is
`change-summary-v1`. The local execution target is OpenClaw on `ws-hadrian`, the
existing approved loopback transport, Ollama in `cuda-compute-katra`, exact
`phi4-mini:latest` digest
`78fad5d182a7c33065e153a5f8ba210754207ba9d91973f57dffa7f487363753`,
and the passed-through RTX 5070 Ti.

## Authority and boundaries

Louis authorizes one local inference request, one attempt, no retry or fallback,
at most 120 seconds and 600 generated tokens. Preparing and previewing the job
must not invoke a model. The output is untrusted, cannot be applied or published
as authoritative prose, and remains `PENDING` until Louis records a human
disposition.

Work Entries 013 and 014 remain parked. This entry grants no hosted call,
cohort, additional benchmark, download, upgrade, installation, credential or
account change, network exposure, resource reallocation or service mutation.

Live effects before execution: NONE.

## Result

Canonical helix-offload
`cb2cc72d799f2828188b5060d1e64c4a242f6016` preserves the bounded packet,
original response envelope, unaccepted artifact, receipt, measurements and
human-disposition record. The packet identity is
`change-summary-packet:39d71e272bc23e39333fb6f0`; its full SHA-256 is
`39d71e272bc23e39333fb6f0cd2c703fa4b35f4c7c8d2579d641a1624aa64304`.

Exactly one request, attempt
`work-entry-015-local-change-summary-live-001`, was `SENT`. It completed in
10,560 ms through the verified local path but reached the 600-token output
ceiling mid-JSON. Deterministic postflight therefore returned
`REFUSED / MALFORMED_OUTPUT` at `OUTPUT_JSON`; no retry, fallback, hosted call,
second benchmark or automatic application occurred. Human disposition remains
`PENDING`.

The response did expose the exact local model/runtime identity but not token
usage. Input, output and total tokens, operating cost, preparation time and
review time remain `UNKNOWN`. Frontier preparation occurred, so this job cannot
be counted as accepted completion without frontier intervention even if Louis
later accepts its semantic content. One refused job proves neither throughput,
general quality nor the 20 percent target.

Published evidence:

- `helix-offload/docs/evidence/WORK_ENTRY_015_LOCAL_CHANGE_SUMMARY_RESULT.md`
- `helix-offload/docs/evidence/work-entry-015-local-change-summary-20261001/`
- `docs/handoffs/WORK_ENTRY_015_RESULT.json`

Exact next action: Louis records `REJECTED` or `FRONTIER_CONTINUATION` for the
preserved malformed output (or otherwise supplies an explicit disposition).
No further inference request is authorized by this entry. Work Entries 013 and
014 remain `PARKED`.

Live effects: one bounded local inference request was sent; scoped sanitized
evidence and the packer repair were published to the helix-offload review
branch and canonical main. No hosted request, retry, fallback, installation,
account or credential change, service mutation, generated-text application or
cohort execution occurred.

## Follow-on format repair

Canonical helix-offload
`11a2cba48540e5501a3b67699ecd20a52ca7fbec` publishes a compatible repair that
keeps the final artifact shape but asks the model only for bounded `summary`,
`risks` and `review_notes` claims using short source IDs. Repository, revision,
validation, authority, execution and receipt facts are now assembled and checked
deterministically. Receipt v3 preserves exposed usage and stop metadata; absent
measurements remain `UNKNOWN`.

Attempt 001 remains byte-identical, `REFUSED / MALFORMED_OUTPUT`, and `PENDING`.
The next packet SHA-256 is
`f5bb1cd016bd36f847d9129efd2057b6a36ddc9d67bbddce56e6384e07966f41`;
its proposed grant is `UNISSUED` and submission is `NOT_SENT`. See
`WORK_ENTRY_015_FORMAT_REPAIR_20261001.md` and
`WORK_ENTRY_015_FORMAT_REPAIR_RESULT_20261001.json`. No inference occurred in
the repair.

## Repaired local attempt 002

Louis authorized exactly one invocation from packet
`f5bb1cd016bd36f847d9129efd2057b6a36ddc9d67bbddce56e6384e07966f41`.
Attempt `work-entry-015-local-change-summary-live-002` was sent once through the
verified local OpenClaw/Ollama/phi4-mini path and completed in 8,306 ms. There
was no retry, fallback or hosted call.

The original strict result remains `REFUSED / MALFORMED_OUTPUT`: the complete
response used a `json` fence and singleton risk/review objects. Louis then
directed postflight repair. Bounded offline reprocessing invoked no model,
preserved the raw response, explicitly recorded each compatibility
normalization, resolved source IDs and assembled deterministic metadata. Its
disposition is `CANDIDATE_OUTPUT_REVIEW_REQUIRED`; human disposition remains
`PENDING`. Tokens, cost, stop reason and truncation remain `UNKNOWN`.

Canonical helix-offload
`5b1c53025b29b858650b2a62fe0f4cfcf7361862` preserves both results. See
`WORK_ENTRY_015_ATTEMPT_002_20261002.md` and
`WORK_ENTRY_015_ATTEMPT_002_RESULT_20261002.json`. No further inference is
authorized; Work Entries 013 and 014 remain parked.
