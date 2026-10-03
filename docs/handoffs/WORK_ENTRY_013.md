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
