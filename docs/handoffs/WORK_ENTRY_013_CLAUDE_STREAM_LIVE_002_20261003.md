# Work Entry 013 — repaired Claude subscription live result

Status: `PARKED / ONE CLIENT RUN CONSUMED / DERP REFUSED / HUMAN PENDING`

On 2026-10-03 Louis authorized one exact Claude Code subscription-backed run
bound to the already published repaired stream packet. Canonical helix-offload
`f24cdc317c364aa01c72eac162fb1281fcafa2f5` preserves the issued grant,
pre-send attempt intent, sanitized connector evidence, complete generated text,
receipt and pending human-disposition record.

The attempt was
`work-entry-013-claude-change-summary-live-002-attempt-001`. Claude Code
`2.1.283` used the existing first-party claude.ai Pro authentication. Requested
and observed model identity both equal `claude-haiku-4-5-20251001`. One client
run and one completed result are observed. The client exposed no `api_retry`
event and no tool/MCP use. Underlying provider request count and unobservable
provider retry behavior remain `UNKNOWN`.

The result completed with `end_turn` and was not truncated. Observed usage was
5,202 input, 372 output and 5,574 total tokens, with 5,550 ms adapter elapsed
time. The configured 600-output-token limit held, but input and total usage
exceeded the workflow's 4,000/4,600 limits. DERP therefore returned
`REFUSED / USAGE_LIMIT_EXCEEDED` before parsing or postflight. The generated
text asked for clarification instead of returning the required compact JSON.
There is no assembled artifact and no authoritative postflight result. An
explicitly diagnostic-only offline parse confirmed `MALFORMED_OUTPUT` without
changing the receipt or fabricating an artifact.

The client exposed `$0.012261` as list-cost metadata. Actual marginal
subscription charge remains `UNKNOWN`; the observation is not API billing or a
cash-savings claim. Human preparation/review effort and semantic disposition
remain `UNKNOWN` / `PENDING`.

Public sanitized evidence:
`helix-offload/docs/evidence/work-entry-013-claude-stream-live-002-20261003/`.
The complete result narrative is
`helix-offload/docs/evidence/WORK_ENTRY_013_CLAUDE_STREAM_LIVE_002_RESULT.md`.

The bounded original stream, stderr, envelope, grant and receipt remain local,
owner-only at
`/home/louis/helix-arpa/repo-cp/.agent-checkouts/codex/work-entry-013-claude-live-002-private/`.
Its manifest-linked raw stdout SHA-256 is
`e068be86bb5e913aace8db00334b53bf10dd428c8f0d674c749e859a1245cdca`.

The one-run authority is consumed. Work Entry 013 remains parked without a
usable Claude comparison artifact. Work Entry 014 remains parked. The exact
next action is Louis's human disposition on this result; another Claude run
would require a new bounded packet and separate authority.

Live effects: one Claude Code subscription-backed client run; publication of
helix-offload review branch `codex/work-entry-013-claude-live-002`; ordinary
non-forced canonical helix-offload publication to
`f24cdc317c364aa01c72eac162fb1281fcafa2f5`; publication of the repo-cp review
branch and the canonical repo-cp commit containing this record. No retry,
relaunch, paid API call,
fallback, tool/MCP action, installation, account/credential change, runtime
mutation or generated-text application occurred.
