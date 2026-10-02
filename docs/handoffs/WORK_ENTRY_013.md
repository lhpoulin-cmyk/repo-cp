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

Live effects: NONE.
