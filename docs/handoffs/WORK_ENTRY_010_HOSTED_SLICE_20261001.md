# Work Entry 010 — hosted-slice disposition

Date: 2026-10-01. Owner boundary: helix-offload owns adapters/evaluation;
repo-cp records authority and reviews evidence.

Canonical helix-offload main was independently resolved to
`6e02f1128a990dfc62e28da6adcc90143a2731cf`. That revision publishes Claude API,
Claude subscription and preserved OpenAI API adapters; provider-neutral
billing/attempt receipts; exact TEST_ONLY admission; synthetic validation; the
Claude attempt evidence; and a non-executing cuda-compute follow-up packet.

Disposition:

- Claude subscription: `SENT` once through the existing Claude.ai Pro client.
  The envelope failed local `HOSTED_RESPONSE_INVALID`; no artifact or postflight
  exists. Human disposition is `PENDING` and semantic acceptance is `UNKNOWN`.
- Claude API: `NOT SENT`; no approved API-key source.
- OpenAI API: `NOT SENT`; no approved API-key source.
- OpenAI subscription: `NOT SENT`; the supported Codex client could not meet the
  exact no-tools/no-retry boundary for this slice.
- The consumed Claude call's underlying request count is `UNKNOWN` because the
  structured-output retry variable allowed one retry. The canonical repair sets
  both retry controls to zero and parses documented `structured_output`, with
  synthetic tests. It is not retroactive evidence.
- No result counts toward accepted offload or the 20% target. No cohort began.

The authorization is consumed. Any Claude retry, cuda-compute execution or other
model call requires new explicit authority. Detailed sanitized evidence remains
in helix-offload; repo-cp does not duplicate provider artifacts.

Live effects: one bounded synthetic extraction input was disclosed to Anthropic;
no artifact, OpenAI call, API-billed charge, manual retry, GPU execution,
credential/account change, purchase, deployment or automatic publication
occurred. The hosted-slice branch and canonical helix-offload main were published
non-forced.
