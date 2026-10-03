# Work Entry 013 — Claude implementation and local-baseline comparison

Status: `PARKED`

Priority: `GREEN` (normal attention)

Scheduling eligibility: `INELIGIBLE_STATE`

## Objective and sequence

Implement and evaluate Claude only after Work Entry 010 has produced an
artifact-bearing local OpenClaw baseline. Compare Claude against the same
Ada/Basic/`REF-42` workload, acceptance criteria, attempt accounting and
measurement definitions. The local baseline is evidence for comparison, not
authority for a hosted call.

Keep Claude API billing separate from Claude subscription-backed allowance.
Use only documented provider interfaces and existing approved authentication;
never reuse subscription credentials on API endpoints or infer that one billing
path consumes the other. The eventual implementation must preserve exact model,
client, account/allowance source and observable usage in its receipt.

## Preserved failed attempts and required repair

Work Entry 010 attempts `work-entry-010-claude-live-001` and
`work-entry-010-claude-live-002` remain historical evidence. Both were sent and
both failed local envelope validation before an artifact reached postflight.
The second attempt also failed to retain the response envelope despite the
previous recovery instruction. Model, usage, cost, provider retry behavior and
the rejected field therefore remain `UNKNOWN`.

Before any future live request, the Claude implementation must durably capture a
bounded, sanitized original response envelope before strict parsing. Recovery,
parsing, postflight and human disposition must link to the immutable attempt.
No live request, retry, account/credential change or subscription/API purchase is
authorized by this parked registration.

Dependency: Work Entry 010 local OpenClaw acceptance baseline.

Dependency update: Louis accepted the Work Entry 010 local artifact with 0 ms
preparation effort and 120,000 ms review effort. The comparison baseline is now
available. This satisfies the evidence dependency only; Work Entry 013 remains
`PARKED` and no implementation or hosted invocation is authorized.

## Offline connector-repair update — 2026-10-03

Louis separately resumed Work Entry 013 for the repair only. Canonical
helix-offload commit `6b88dea4066d1711ead5de5914bd7f5992abcf87`
implements a provider-neutral connector outcome, bounded mode-0600 raw capture,
a key-redacted review envelope before strict parsing, receipt V4 and truthful
nullable execution accounting for Claude API and Claude Code. Offline synthetic
validation passed 51/51 under both unittest and pytest. No model invocation,
credential access, account/billing change or runtime mutation occurred.

The implementation used the externally researched report at repo-cp branch
`codex/frontier-connector-research`, commit
`a48a802132f1db64304a032bcc4b207d7f26ea71`. The report remains research
evidence rather than implementation proof. The implementation's separate tests
and published source are the verification evidence.

This closes the required offline repair, not the entry's live Claude comparison.
Work Entry 013 returns to `PARKED`; a later task must choose one exact supported
Claude execution path and independently authorize its model invocation. Work
Entry 014 remains parked behind that comparison.

Live effects: canonical helix-offload and review branch publication only. No
model invocation, credential access, account/billing change, installation,
deployment or runtime mutation occurred.

## Claude subscription comparison attempt — 2026-10-03

Louis subsequently authorized one Claude Code subscription-backed client run
using the repaired Work Entry 015 change-summary packet. Canonical helix-offload
`8421ac36e9563120c670a2d803295faf22969c18` preserves the exact grant, the
compatible HTTP/inference-accounting correction and sanitized result evidence.

The client run returned a structured-output client error and no artifact. One
client run is observed; provider submission, provider retries, inference, model
identity, normalized token usage and cost remain `UNKNOWN`. No postflight could
run and human disposition remains `PENDING`. No retry or fallback occurred.

The detailed result is
[`WORK_ENTRY_013_CLAUDE_SUBSCRIPTION_20261003.md`](WORK_ENTRY_013_CLAUDE_SUBSCRIPTION_20261003.md).
The one-run authority is consumed. Work Entry 013 is parked without a usable
Claude comparison artifact, and Work Entry 014 remains parked.

## Offline subscription stream repair — 2026-10-03

Louis then authorized implementation and publication of an offline-only repair,
with no model invocation. Canonical helix-offload commit
`15b86e6c09a5602bc40125fe6bee2a45727c787a` removes `--json-schema` from the
Claude Code subscription route, captures bounded `stream-json` evidence before
DERP parsing, refuses ambiguous/incomplete/tool/retry events, and retains
submission and inference uncertainty when later processing fails.

The failed attempt remains unchanged. Its supported conclusion remains: Claude
Code reported a 650-character summary with missing required fields and ended in
structured-output retry exhaustion; a reported upstream defect is only a
possible explanation. Provider execution, actual model and usage remain
`UNKNOWN`.

A fresh TEST_ONLY packet for the same Work Entry 015 evidence is published at
source packet SHA-256
`f5bb1cd016bd36f847d9129efd2057b6a36ddc9d67bbddce56e6384e07966f41`.
Its generated-content contract is explicitly v2, its proposed grant is
`UNISSUED`, and its submission state is `NOT_SENT`. Offline validation passed
62/62 under unittest and pytest; 147/147 repository JSON files parsed. Work Entry 013 remains `PARKED`; a live run
requires fresh exact authority and issuance of a real grant. Work Entry 014
remains parked.

## Repaired subscription stream attempt — 2026-10-03

Louis then authorized exactly one Claude Code subscription-backed client run
bound to the published repaired packet. Canonical helix-offload
`f24cdc317c364aa01c72eac162fb1281fcafa2f5` preserves attempt
`work-entry-013-claude-change-summary-live-002-attempt-001` and its sanitized
evidence.

The requested and observed model was `claude-haiku-4-5-20251001`. One client
run completed with `end_turn`; no client retry or tool/MCP event was observed,
while underlying provider request/retry behavior remains `UNKNOWN`. Claude Code
reported 5,202 input, 372 output and 5,574 total tokens. DERP refused the result
as `USAGE_LIMIT_EXCEEDED` against the packet's 4,000-input/4,600-total limits
before postflight. The returned prose was not the required JSON, no artifact was
assembled and human disposition remains `PENDING`.

The detailed result is
[`WORK_ENTRY_013_CLAUDE_STREAM_LIVE_002_20261003.md`](WORK_ENTRY_013_CLAUDE_STREAM_LIVE_002_20261003.md).
The one-run authority is consumed. Work Entry 013 remains parked without a
usable Claude comparison artifact; Work Entry 014 remains parked.

## Security review and one-use grant reservation — 2026-10-03

Louis then authorized preservation of the security review and Claude result
together plus one bounded offline hardening slice. The research commit
`4eae1b63e85cdfe42ff64a4ab149e2661ab86150` is integrated with its exact report
and source-manifest hashes; it remains research evidence rather than
implementation proof.

Canonical helix-offload `d6c7f708fa5bee2845fbd11b67a946161898dfe1`
implements an immutable filesystem reservation keyed by canonical grant digest.
Every supported explicit executor now records intent and durably reserves the
grant in one configured shared private local store before adapter construction
or invocation. Different attempt IDs, crashes and restarts do not release or
reuse it. The boundary provides local at-most-once admission, not exactly-once
provider execution or coordination across independent stores.

Offline validation passed 69/69 tests including a two-process race with exactly
one fake-adapter invocation, changed-attempt reuse refusal, immediate
post-reservation crash/restart refusal and storage-failure prevention. No model,
provider API or GPU call occurred.

The preserved Claude result remains refused with no artifact and human
disposition `PENDING`. Its packet made historical authority facts model-visible,
and its input/total limits detected excess usage only after consumption. Prompt-
authority separation and preventive token accounting are prepared follow-ups,
not retroactive acceptance or a proven provider defect.

The detailed continuation is
[`WORK_ENTRY_013_SECURITY_REVIEW_AND_GRANT_RESERVATION_20261003.md`](WORK_ENTRY_013_SECURITY_REVIEW_AND_GRANT_RESERVATION_20261003.md).
The remaining ranked hardening findings are one non-executing future-work
candidate group; no new Work Entry numbers were allocated. Work Entry 014
remains parked.
