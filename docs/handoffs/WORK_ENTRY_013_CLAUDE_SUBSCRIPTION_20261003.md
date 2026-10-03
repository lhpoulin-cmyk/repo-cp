# Work Entry 013 — Claude subscription comparison attempt

Status: `PARKED / ONE CLIENT RUN FAILED / NO ARTIFACT`

On 2026-10-03 Louis authorized one bounded Claude Code client run through the
existing subscription authentication. The run used the repaired Work Entry 015
`change-summary-v1` input and source registry, requested
`claude-haiku-4-5-20251001`, allowed no tools or fallback, and was bounded to
120 seconds and 600 generated tokens.

Before execution, helix-offload corrected future receipt-V4 accounting so an
HTTP/client response proves communication but does not alone prove inference.
`execution_occurred` is true only for a parsed model completion, refusal or
incomplete result; it is false for proven `NOT_SENT` and null when inference is
not established. Synthetic 401, 429, 500, malformed-response, timeout and
launch-failure cases cover the distinction. Historical receipts were not
rewritten.

The single Claude Code run returned a captured client envelope with
`error_max_structured_output_retries`: required compact fields were missing and
the summary exceeded its 480-character field limit. The client did not return
the rejected prose itself, so DERP received no artifact and postflight did not
run. No acceptance rule was relaxed and no second call was made.

Observed evidence:

- client-run submission: `RESPONSE_RECEIVED`;
- terminal state: `CLIENT_ERROR` / `ADAPTER_CLIENT_FAILED`;
- inference: `UNKNOWN`;
- requested model: `claude-haiku-4-5-20251001`; observed model: `UNKNOWN`;
- connector elapsed: 8,415 ms; client-reported duration: 8,172 ms;
- normalized tokens, cost, provider requests and provider retries: `UNKNOWN`;
- human disposition: `PENDING`; no artifact exists to accept.

Canonical helix-offload `8421ac36e9563120c670a2d803295faf22969c18`
contains the accounting correction, exact TEST_ONLY packet and grant, sanitized
attempt evidence and result record. Raw bounded client recovery evidence remains
local and mode 0600 at
`/home/louis/helix-arpa/repo-cp/.agent-checkouts/codex/work-entry-013-private-evidence/result/`.

Work Entry 013 is parked because the one-call authority is consumed and no
Claude comparison artifact was produced. Work Entry 014 remains parked behind a
usable Claude comparison. A future action requires a new bounded decision; this
record grants none.

Live effects: one Claude Code subscription-backed client run; publication of
the helix-offload review branch and a non-forced fast-forward of canonical
helix-offload main. No paid API use, retry, fallback, account or credential
change, installation, deployment or generated-text application occurred.

