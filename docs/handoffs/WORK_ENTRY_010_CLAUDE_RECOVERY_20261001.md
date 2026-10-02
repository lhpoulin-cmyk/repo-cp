# Work Entry 010 — Claude recovery and corrected-call disposition

Date: 2026-10-01. Owner boundary: helix-offload owns adapter execution and
evidence; repo-cp records authority and disposition.

Fresh direct remote verification resolved canonical repo-cp main to
`36476ed1298d2f903f4dd4da219fccee77fe1375` and canonical helix-offload main to
`6e02f1128a990dfc62e28da6adcc90143a2731cf` before this work.

The original response envelope for `work-entry-010-claude-live-001` was not
recoverable offline. Its committed evidence remained byte-identical. A targeted
search found no matching repository copy, retained Claude Code session/history,
cache/state artifact, temporary directory, or unreachable Git object. Recovery
made no model call, session resume, or resend.

Louis then authorized one corrected live acceptance call. Attempt
`work-entry-010-claude-live-002` reused the exact test-only 38-byte
Ada/Basic/`REF-42` packet, requested `claude-haiku-4-5-20251001` through the
existing Claude.ai Pro-backed `claude-code.subscription.v1` path, used a fresh
content-bound LIVE grant, a 30-second deadline, 600-token/8-KiB output limit, and
zero configured API or structured-output retries.

The invocation was **SENT** once and returned without timeout or disconnect. The
corrected adapter again returned `EXECUTION_FAILED / HOSTED_RESPONSE_INVALID`.
No artifact reached postflight; actual model, usage and subscription monetary
cost remain `UNKNOWN`; human disposition remains `PENDING`. No retry, fallback,
OpenAI call, or continuation occurred. The exact rejected field is also UNKNOWN
because the client envelope was not durably retained.

Sanitized evidence commit
`9ec732046ba6481be70018277b91ff04534baa8d` is published on helix-offload review
branch `codex/work-entry-010-recovery`. Canonical helix-offload main remains
`6e02f1128a990dfc62e28da6adcc90143a2731cf`: the execution environment rejected
the ordinary fast-forward because it could not establish repository identity for
the isolated checkout, despite a clean diff and verified remote. The review
commit therefore is not claimed merged or canonical.

The corrected-call authority is consumed. Another live call would require new
explicit authority. Before any such call, helix-offload should preserve a
bounded sanitized response envelope before strict parsing so a failure remains
recoverable and diagnosable; that is a proposed repair, not a completed or
authorized acceptance result.

Live effects: one additional disclosure of the same synthetic `REF-42` input to
Anthropic through the existing Claude.ai Pro allowance, plus non-forced
publication of sanitized evidence branch `codex/work-entry-010-recovery` at
`9ec732046ba6481be70018277b91ff04534baa8d`. No artifact, postflight, acceptance,
retry, OpenAI/API-billed call, credential/account change, purchase, deployment,
GPU execution, cohort, or canonical-main publication occurred.
