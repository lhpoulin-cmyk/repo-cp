# helix-offload frontier connector repair research

- Date: 2026-10-03
- Retrieval date for changing web sources: 2026-10-03
- Repository observations: `lhpoulin-cmyk/helix-offload` at
  `8bb94065b3948ae625a372ab70cfd6e23900e707`; `lhpoulin-cmyk/repo-cp` at
  `20674f38a8efc568c0b77b94b8de0201efe45e30`
- Delivery stage: research and implementation plan only
- Live effects from this research: none on model providers, GPUs, credentials,
  accounts, subscriptions, or canonical repository branches

## Executive recommendation

The smallest reliable repair is not another Claude-specific parser patch. It is
one provider-independent, evidence-first connector boundary used by the existing
Anthropic Messages and OpenAI Responses adapters:

1. Persist a bounded original response envelope and allowlisted transport
   metadata before strict parsing.
2. Return a typed connector outcome for completed, refused, incomplete,
   provider-error, client-error, parse-failed, and submission-uncertain states.
3. Record submission state separately from generation success and from DERP
   postflight.
4. Extract the documented provider payload; then validate the workload schema;
   then assemble deterministic facts; then require human acceptance.

Use direct provider APIs as the primary frontier transport. Start with the
existing Anthropic Messages adapter for Work Entry 013 and apply the same
boundary to the existing OpenAI Responses adapter before Work Entry 014. These
interfaces are inference-oriented, support native structured output, expose
model, usage, completion, error, and request identifiers, and can use a client
with automatic retries disabled. API billing is separate from Claude, ChatGPT,
or Codex subscriptions.

Use a repaired Claude Code subscription adapter only as a practical fallback
when Louis deliberately prefers subscription allowance and accepts its weaker
attempt semantics. Claude Code's documented headless interface supports JSON or
JSONL output, schema-constrained `structured_output`, disabled tools, restricted
mode, and client metadata. It is nevertheless an agent client. It has a default
system prompt and agent loop, subscription-authenticated calls cannot use the
new reproducible `--bare` mode, and the current documentation describes internal
API retry events rather than a supported hard switch proving one provider
submission. A grant for this route must therefore authorize one **client run**,
not claim one provider request, and preserve retry events or `UNKNOWN`.

Do not use Codex CLI as an inference-only OpenAI subscription adapter. The
supported ChatGPT-plan route with the closest API semantics is Sign in with
ChatGPT (SIWC) to Responses, optionally through Codex app-server. It currently
adds OAuth registration, token lifecycle, eligibility, and client integration.
The repository is private and has no license grant, so open-source SIWC
eligibility is not established. Keep SIWC as the OpenAI subscription fallback,
not the minimum repair. Do not use browser sessions, cookies, compatibility
proxies, or undocumented tokens.

This ordering retains the owned OpenClaw/Ollama path as the default measured
baseline, uses frontier calls only for explicitly continued work, and avoids a
new orchestration framework.

## Evidence classes and limits

- **Repository observation** means a file or Git fact at the two exact revisions
  above.
- **Documentation claim** means a current first-party provider document retrieved
  on 2026-10-03. Most living documentation pages show no publication date; the
  source manifest records that as `null` rather than inventing one.
- **Calculation** means arithmetic from a published price and an explicit token
  bound. It is not an observed charge or a provider-enforced per-call cap.
- **Inference** means a reasoned implementation conclusion. It is labeled.
- Private accounts, current credentials, current model entitlements, provider
  dashboards, and billing balances were not inspected. Historical evidence of
  a successful Claude Code login is not proof that access is currently ready.
- No endpoint, model, GPU, client, or benchmark was invoked for this research.

## What “frontier connector” means here

The current repository already separates most policy responsibilities. The
remaining connector work should preserve that separation.

| Layer | Current owner | Responsibility | Is it the historic Claude defect? |
| --- | --- | --- | --- |
| Provider/client transport | Adapter | Submit one authorized request or one authorized client run; enforce local deadline and request bounds | Partly. Claude Code returned an envelope, so transport was reached. |
| Response-envelope capture | Adapter/transport boundary | Preserve bounded bytes, identifiers, headers/events, and submission observations before parsing | Yes. Both Claude envelopes were discarded. |
| Provider-envelope extraction | Provider-specific parser | Interpret Messages, Responses, Claude Code JSON, or JSONL according to its documented wrapper | Plausibly. The first parser used `result` instead of `structured_output`; attempt 002 remains unknowable. |
| Workload structured-output validation | Provider-neutral connector/workflow | Validate the extracted payload against the job schema and explicit permitted normalizations | Not proved. No historic Claude payload survived to test. |
| Admission and execution grant | DERP and Work Entry 005 | Decide eligibility and bind one explicitly authorized attempt/client run | Existing and distinct; a parser fix grants no authority. |
| Postflight and deterministic assembly | DERP | Check references/content and attach host-known facts without asking the model to repeat them | Existing and demonstrated by Work Entry 015; semantic quality still requires review. |
| Frontier continuation | DERP/human workflow | Package the bounded unresolved task after a local result; attribute the new work separately | Not an adapter retry and not retroactive local success. |

The minimum repair belongs at the first four layers plus receipt accounting. It
does not require changes to recommendation policy, candidate admission,
execution-grant issuance, deterministic Git packing, or human authority.

## Evidence-backed diagnosis

### Confirmed repository facts

1. `src/helix_offload/adapters.py:117-233` uses a direct, synchronous OpenAI
   Responses request. It requests strict `text.format` JSON schema, disables
   tools and storage, and requires a completed response. Its transport at
   `adapters.py:704-749` reads JSON into memory and discards raw response bytes,
   response headers, request IDs, and error bodies.
2. `adapters.py:236-329` uses a direct Anthropic Messages request with
   `output_config.format`, no tools, and a standard-only service tier. Its
   transport at `adapters.py:752-798` likewise discards the raw body, headers,
   request ID, and HTTP error body before DERP can preserve them.
3. `adapters.py:332-461` invokes the first-party `claude` executable in print
   mode. The command requests JSON, a JSON schema, one agent turn, no built-in
   tools, no MCP servers, safe/restricted modes, no session persistence, no
   Chrome, and no fallback models. Subscription authentication therefore means
   Claude Code, not claude.ai browser automation and not the Anthropic API.
4. The Claude Code adapter captures stdout and stderr only in process memory,
   parses stdout after process exit, uses an automatically deleted temporary
   directory, and accepts no envelope destination. A nonzero exit discards both
   streams. A zero exit followed by any strict field rejection also discards the
   envelope.
5. The current Claude Code parser correctly looks first at
   `structured_output`. It still requires the exact top-level success shape, one
   turn, a valid session ID, and `set(modelUsage) == {requested_model}`. That
   exact-key equality is brittle when a client reports an observed model rather
   than the requested alias, adds a model, or evolves optional fields.
6. The local OpenClaw adapter already demonstrates the useful pattern: the CLI
   passes `result/response-envelope.json`; the adapter writes a bounded envelope
   before strict parsing; `workflow.py:455-490` binds its hash into the result
   manifest.
7. The hosted CLI paths in `cli.py:264-370` reserve a result directory and write
   attempt intent, but do not pass an envelope destination to the OpenAI,
   Anthropic, or Claude Code adapters. This is the precise asymmetry to remove.
8. `derp.py:306-315` turns every `AdapterFailure` into
   `execution_occurred: false`. The historic receipts therefore say execution
   did not occur even though both reports say a Claude client request was sent
   and an envelope returned. `adapter_invoked: true` does not repair that
   ambiguity.
9. Current hosted synthetic tests in `tests/test_derp.py:333-458` inject one
   ideal Python mapping or subprocess result. They do not use versioned sanitized
   provider envelopes, JSONL streams, HTTP error bodies, unknown optional fields,
   partial output, or phase-specific timeout fixtures.

### Historic Claude attempts

The following is confirmed at the observed revision:

- Attempts `work-entry-010-claude-live-001` and `...-002` were separately
  authorized and each reached the Claude Code client path.
- Both were rejected locally as `HOSTED_RESPONSE_INVALID` before postflight.
- Attempt 001 led to the documented correction from `result` to
  `structured_output`.
- Attempt 002 failed after that correction.
- Neither result directory contains a response envelope. Their manifests have
  no envelope identity, and their receipts contain no actual model, usage,
  response/session identifier, elapsed time, or rejected-field diagnostic.
- No valid artifact can be reconstructed from expected output or synthetic
  fixtures.

The precise second failure is unknowable. Plausible causes include a changed or
unexpected envelope field, the exact `modelUsage` key-set check, a different
success subtype, an absent/invalid session ID, usage shape variation, or a
payload type difference. Those are hypotheses, not findings.

### Client and provider semantics that matter

- Claude Code documents `result` for text output and `structured_output` for a
  schema-constrained run. `json` is one object; `stream-json` is JSONL whose last
  line is a result event. It documents `system/api_retry` events and their
  attempt counts. The repository's `CLAUDE_CODE_MAX_RETRIES=0` and
  `MAX_STRUCTURED_OUTPUT_RETRIES=0` controls are not found in the current public
  settings/headless documentation, so they must not be treated as a provider
  guarantee.
- Claude Code's new `--bare` mode is recommended for reproducible scripts, but
  it deliberately does not read subscription OAuth credentials. Therefore a
  subscription adapter must use safe/restricted settings rather than claim bare
  reproducibility.
- Anthropic's official SDKs retry transient failures twice by default unless
  configured otherwise. The current stdlib HTTP transport has no retry loop,
  which is useful for DERP's strict one-submission path.
- OpenAI's official SDKs also retry eligible errors subject to settings. The
  current stdlib HTTP transport has no retry loop, but its OpenAI timeout is
  mislabeled merely `ADAPTER_TIMEOUT`; after bytes may have been sent, the
  correct state is submission uncertain.
- OpenAI supports a caller-supplied `X-Client-Request-Id`, which can help support
  determine whether a request arrived. It is not documented as an idempotency
  key. Anthropic exposes a server request ID on responses/errors. Neither
  provider document examined establishes an idempotency guarantee for the
  synchronous create operation.
- A process exit code proves only client termination status. Generation success
  still requires the documented envelope status, payload, stop/completion state,
  and absence of refusal/error.

## Supported-interface comparison

The detailed, machine-readable table is preserved beside this report as
`2026-10-03-helix-offload-frontier-interface-comparison.csv`.

| Route | Billing/authentication | Controls and observability | Maintenance | Fit and disposition |
| --- | --- | --- | --- | --- |
| Anthropic Messages API over current direct HTTP | Anthropic API workspace; API billing separate from Claude subscription | Exact request body; no tools; native schema; returned ID/model/stop/usage; server request ID and error body available; caller can make zero retries | Low after shared capture boundary | **Primary Claude route. Build.** Best strict one-submission semantics. |
| Official `ant` CLI to Messages API | Same Anthropic API billing/key | Official typed CLI, JSON/JSONL/raw output; client/SDK retry defaults must be explicitly disabled or avoided | Low-to-medium | **Diagnostic fallback, not a second production adapter.** Reuse if direct HTTP portability becomes a problem. |
| Claude Code print mode with subscription login | Eligible Claude subscription allowance; not API credit | Supported headless JSON/JSONL, structured output, tool restrictions, safe/restricted modes, session/usage/client estimates; internal retry events; cannot use subscription auth in `--bare` | Medium; client versions and agent semantics evolve | **Conditional fallback. Repair capture, then use only under one-client-run authority.** |
| Claude Code Routines API | Claude subscription allowance; routine-scoped bearer token | Starts managed agent sessions; no idempotency key; every successful retry starts another session; experimental and not SDK-supported | High relative to this need | **Reject for DERP inference.** Agentic and weaker duplicate control. |
| OpenAI Responses API over current direct HTTP | OpenAI API project; API billing separate from ChatGPT | Exact request; no tools; strict schema; response ID/status/model/output/usage; incomplete/refusal fields; server and caller request IDs | Low after shared capture boundary | **Primary OpenAI route. Build after Claude boundary is proven.** |
| Official OpenAI CLI to Responses API | Same OpenAI API billing/key | Official JSON/JSONL/raw and error output; not subscription-backed | Low | **Diagnostic fallback, not a separate DERP abstraction.** |
| SIWC direct Responses or Codex app-server | Eligible ChatGPT plan permission via OAuth; plan allowance, not API key billing | Supported Responses stream; app-server has NDJSON lifecycle and completed/failed/interrupted turn status; requires OAuth registration, refresh, secure token storage, and eligibility | Medium-to-high initially | **OpenAI subscription fallback. Defer.** Current private/no-license repo does not establish OSS eligibility. |
| Codex CLI authenticated with ChatGPT | ChatGPT/Codex subscription allowance | JSONL and output schema exist, but the product is a coding agent with context, sandbox, and possible tool activity rather than a one-response inference client | High mismatch | **Reject for this connector.** Use Codex for coding sessions, not DERP inference. |
| Existing OpenClaw → Ollama local route | Owned hardware; no hosted API bill | Exact model digest, tool-free local call, bounded envelope capture; token and energy fields remain interface-dependent | Already implemented | **Retain as baseline.** Not a frontier connector. |

### Account eligibility and billing findings

- Repository evidence establishes only that a Claude.ai Pro-backed Claude Code
  login worked on 2026-10-01. Current allowance and model entitlement are
  `UNKNOWN`.
- Anthropic states that Claude subscriptions and Console API billing are
  separate. No API credential or billing readiness is established by this
  research.
- OpenAI states that ordinary API work uses API credentials and API billing.
  SIWC is a separate supported path by which eligible local/open-source apps can
  obtain user-approved ChatGPT-plan Responses access. It does not expose ChatGPT
  conversations.
- helix-offload's current README says the repository is private and no license
  grant is configured. Whether Louis wants to make it eligible for an open-source
  SIWC path is a separate product/legal decision. Do not change licensing merely
  to obtain subscription access.

## Proposed provider-independent connector result

Keep workflow definitions portable. Provider-specific bytes and transport facts
belong in an execution-evidence object, not in the job packet, admission result,
or policy rules.

### `connector-attempt/v1`

Write this immutable intent before any network/client operation:

- `attempt_id`, `job_id`, workflow/preview/grant hashes;
- adapter ID and version, interface kind, billing source;
- requested provider and exact requested model string;
- input, instructions, output-schema, limits, and executable/config hashes;
- granted submission unit: `PROVIDER_REQUEST` or `CLIENT_RUN`;
- local start time and monotonic deadline;
- expected retry/fallback/tool policy;
- raw and sanitized capture destinations.

The existing `attempt.json` supplies much of this. Version it rather than create
a parallel ledger.

### `connector-outcome/v1`

Return this from every adapter, including failures:

```text
attempt_id
submission_state: NOT_SENT | SENT | RESPONSE_RECEIVED | SUBMISSION_UNCERTAIN
terminal_state: COMPLETED | REFUSED | INCOMPLETE | PROVIDER_ERROR |
                CLIENT_ERROR | PARSE_FAILED | POLICY_REFUSED
requested_model_id
observed_model_id: string | null
provider_response_id: string | null
provider_request_id: string | null
client_request_id: string | null
client_identity: {name, version} | null
provider_identity: {name, api_version} | null
payload: {text, structured} | null
usage: {
  input_tokens, output_tokens, total_tokens,
  reasoning_tokens, cache_read_tokens, cache_write_tokens,
  provider_dimensions, basis
}
completion: {reason, truncated, basis}
timing: {wall_ms, provider_ms, basis}
billing: {source, observed_cost_microusd, estimated_cost_microusd,
          estimate_basis}
attempt_observation: {client_runs, provider_requests, basis}
error: {class, code, sanitized_message} | null
envelope: {raw_sha256, sanitized_sha256, bytes, overflow, format,
           published}
```

Null means unknown. Do not manufacture a common number from unlike provider
dimensions. For example, preserve Anthropic base/cache input fields and OpenAI
reasoning/cached-token details under `provider_dimensions`; populate the common
totals only where the interface defines them.

### Receipt compatibility

Add `helix-offload.derp-receipt/v4` rather than silently reinterpret v3:

- embed or hash-bind the connector outcome;
- replace ambiguous failure accounting with `submission_state` and
  `generation_state`;
- keep `adapter_invoked` for historical readability;
- retain `execution_occurred` only as a deprecated derived field when it is
  definitely true or false, or omit it in v4. It cannot represent
  `SUBMISSION_UNCERTAIN` honestly;
- preserve v1-v3 schemas and readers unchanged;
- an offline reprocessor may create a new linked v4 receipt but must not mutate
  or relabel the original receipt.

This is a visible schema migration. It corrects a material accounting defect;
it is not optional telemetry churn.

## Response capture and handling flow

1. Reserve a consumer-selected result directory with mode `0700`.
2. Write and fsync attempt intent before invoking a client or opening an HTTP
   request.
3. Submit at most the granted unit. Update submission phase conservatively.
4. Capture the original response stream/body to a new file before JSON parsing.
   For a subprocess, capture stdout and stderr separately. For HTTP, capture the
   bounded body plus an allowlist of status, request ID, processing time,
   content type, and rate-limit headers.
5. Enforce a default 1 MiB raw-envelope limit. Read at most limit + 1 byte. If
   overflow occurs, preserve the prefix and `overflow: true`, record the known
   lower-bound size, refuse parsing, and never pretend the prefix is complete.
6. Fsync, hash, and close the raw capture. Then create a sanitized derivative.
7. Parse the documented outer envelope. Unknown optional fields are preserved
   in the raw capture and ignored by the typed extractor. Unknown required
   discriminators fail visibly.
8. Extract exactly one generated payload or a documented refusal/error. For
   JSONL, accept only a valid terminal result after a well-formed event stream;
   preserve partial lines and error/retry events on failure.
9. Validate the extracted payload against the workload schema and explicit
   content limits.
10. Run DERP postflight and deterministic assembly only after payload validity.
11. Write the connector outcome, receipt, optional untrusted artifact, and a
    manifest binding every hash. Write `complete: true` last.

### Capture lifecycle and publication

- Keep raw capture under the caller-supplied result directory, not a source-tree
  path or global workstation path hard-coded into helix-offload.
- Default raw capture to private/local evidence. Retain it at least until human
  disposition and any failure diagnosis are complete. The consumer owns later
  retention/deletion policy.
- A sanitizer should allowlist documented response fields, redact headers except
  safe identifiers/limits/timing, and omit credentials, cookies, filesystem
  paths, account/workspace identifiers, request URLs with query data, and raw
  debug logs.
- Publish only the sanitized derivative and hashes unless explicit disclosure
  authority covers the raw content. A hash does not make sensitive content safe.
- Invalid JSON, partial output, and provider errors are evidence. Preserve their
  bounded raw bytes and a sanitized diagnostic; never discard them merely
  because no artifact can be built.

### Hash chain

Bind these identities explicitly:

```text
attempt intent
  -> raw envelope SHA-256
  -> sanitized envelope SHA-256
  -> extracted payload SHA-256
  -> normalized payload SHA-256 (only when a versioned policy permits it)
  -> assembled artifact SHA-256
  -> receipt and manifest SHA-256
```

The original and each derivative remain separate files. A recovery receipt
links them and names every transformation.

## Syntax extraction versus acceptance policy

The connector should make four operations visibly different.

| Operation | Example | Policy |
| --- | --- | --- |
| Documented envelope extraction | Claude Code `structured_output`; Responses `output[].content[].output_text`; Messages text block | Required provider parser behavior. Not “repair.” |
| Complete presentation-wrapper removal | One complete fenced JSON document | Permit only in an explicit workload normalization policy; retain original and record action. Native strict structured output should normally refuse a fence. |
| Permitted representation normalization | Wrap a singleton claim object into a one-item array | Only when the contract version explicitly accepts both representations or a versioned recovery policy says so. |
| Acceptance-policy change | Increase claim limit from 180 to 320 characters | Contract/policy version change, not normalization. Original result remains evaluated under original limits. |
| Claim editing | Reword, add, or delete a generated factual claim | Never automatic. Requires a new model/human artifact and attribution. |

Work Entry 015 handled historical recovery correctly in one important respect:
it preserved the original strict refusal and created a separately linked offline
reprocessing result. The new connector should make that pattern routine without
making loose output the default.

Provider-native schemas reduce syntax failures but do not establish semantic
adequacy. OpenAI Structured Outputs and Anthropic structured outputs support
subsets of JSON Schema and have refusal/incomplete paths that can violate the
expected success schema. Keep local validation authoritative for the portable
contract and test only the intersection actually used by helix-offload:
objects, required properties, strings, arrays, item objects, enums, length/item
limits enforced locally, and `additionalProperties: false`. Do not rely on
unsupported conditionals or provider-specific annotations.

## One-attempt semantics and recovery

### Strict direct-API path

- Grant one `PROVIDER_REQUEST`.
- Use the current direct HTTP approach or an SDK explicitly configured with zero
  retries. Do not layer an SDK, CLI, proxy, and application retry loop.
- Do not configure provider fallback models.
- Bind deadline and output-token maximum in intent and request.
- Send no tools.
- On a timeout/disconnect after request transmission may have begun, record
  `SUBMISSION_UNCERTAIN`; do not resend under the same grant.
- Record `X-Client-Request-Id: <attempt_id>` for OpenAI. Preserve Anthropic and
  OpenAI server request IDs when returned. These aid diagnosis; they are not
  deduplication guarantees.
- If a provider response ID is available and the interface supports retrieval,
  offline recovery may retrieve that same response only under explicit
  read/recovery authority. It must not create a second generation.

### Subscription-client path

- Grant one `CLIENT_RUN`, not a fictitious single provider request.
- Capture JSONL if the supported client can emit retry and initialization events
  together with the terminal result; otherwise provider request count is
  `UNKNOWN`.
- Pin and record client version and every effective boundary flag.
- Claude Code fallback should use an empty built-in tool set, deny all MCP tools,
  strict empty MCP configuration, safe and restricted modes, no session
  persistence, no Chrome, no fallback model, one turn, and an isolated empty
  working directory. Verify current flags at implementation time.
- A client timeout is submission uncertain. Killing the local process does not
  prove the provider did not execute or complete a request.
- If a client cannot satisfy the grant's retry/tool/fallback boundary, refuse
  before invocation. Do not silently weaken the grant.

### Attempt ledger

Use an append-only state progression:

```text
INTENT_RECORDED -> CLIENT_STARTED -> REQUEST_MAY_HAVE_BEEN_SENT ->
RESPONSE_BYTES_RECEIVED -> ENVELOPE_CAPTURED -> PAYLOAD_EXTRACTED ->
POSTFLIGHT_COMPLETE -> HUMAN_DISPOSITION_RECORDED
```

Each state records time, prior-record hash, and evidence basis. Terminal failure
may occur at any state. Recovery reads the ledger first and never submits if it
shows `REQUEST_MAY_HAVE_BEEN_SENT` without a resolved outcome. Local deduplication
prevents the helix caller from resending; it does not make a provider operation
idempotent.

## Making frontier continuation useful: Work Entry 015

At the observed revisions, Louis recorded `FRONTIER_CONTINUATION` for the
reprocessed local artifact. Semantic acceptance remains `UNKNOWN`; this is the
appropriate trigger for a separately authorized frontier job.

The frontier packet should contain only:

1. The original bounded objective: summarize the exact helix-offload commit
   range for review using `summary`, `risks`, and `review_notes` claims.
2. The existing deterministic v2 source registry and bounded excerpts.
3. Exact local raw output SHA-256
   `9c83c1457fb246c38fcb82a86e7fe98434fced8b389a5edab6440092c3f4b78c`.
4. The immutable original refusal and linked offline-reprocessed receipt.
5. Deterministic postflight facts: syntax normalization succeeded; source IDs
   resolved; entailment and semantic completeness were not proved.
6. Louis's `FRONTIER_CONTINUATION` disposition and the specific remaining task:
   produce a grounded account of the actual code changes and limitations,
   without exaggerating implications from a synthetic workload.
7. The same compact output contract and source-ID registry. The model still does
   not copy SHAs, paths, authority, measurements, or status fields.

A suitable continuation instruction is:

> Using only the supplied source registry, excerpts, local output, and postflight
> findings, return compact `summary`, `risks`, and `review_notes` claims. Explain
> the implemented adapter/receipt/format changes and the demonstrated local
> outcome. Do not infer throughput, general quality, token/cost savings, or the
> 20% target. Cite each factual claim with supplied source IDs. Address why the
> local prose was not semantically accepted; do not merely reformat it.

The host then validates the frontier payload and deterministically assembles
repository facts exactly as it did locally.

Accounting remains separate:

- local preparation and execution effort;
- local output and postflight disposition;
- human review and continuation decision;
- frontier-packet preparation effort;
- frontier tokens/cost/latency;
- frontier output/postflight;
- final human review and any repair.

A successful frontier completion does not make the local result accepted or the
local candidate qualified. It records a continuation outcome with its own
candidate, grant, receipt, and disposition.

## Minimal implementation plan

### Phase 1 — shared evidence boundary; no live call

1. Add `src/helix_offload/response_boundary.py` containing immutable
   `ConnectorAttempt`, `EnvelopeIdentity`, `ConnectorOutcome`, and bounded
   capture/sanitization helpers. Use the standard library; add no orchestration
   dependency.
2. Add `schemas/connector-outcome-v1.schema.json` and
   `schemas/derp-receipt-v4.schema.json`. Preserve all old schemas byte-for-byte.
3. Update `src/helix_offload/workflow.py` so every live adapter receives the
   reserved result directory/capture sink, and finalization writes an outcome
   and manifest even when extraction or postflight fails.
4. Update `src/helix_offload/derp.py` to consume a connector outcome rather than
   flatten every adapter failure into `execution_occurred: false`. Admission,
   recommendation, grant validation, postflight, and artifact assembly remain
   unchanged.
5. Add a migration document under `docs/contracts/` explaining receipt v4,
   legacy receipt interpretation, and no retroactive rewriting.

Acceptance: every synthetic terminal path leaves an immutable attempt, bounded
envelope when bytes exist, connector outcome, receipt, and complete manifest;
no test creates a second submission.

### Phase 2 — primary direct APIs; no live call

1. Modify `OpenAIResponsesHTTPTransport` and
   `AnthropicMessagesHTTPTransport` in `adapters.py` to write body and allowlisted
   headers before parsing, include phase-aware submission state, and preserve
   sanitized HTTP errors.
2. Add the OpenAI caller request ID. Classify `incomplete_details`, refusal,
   provider error, model mismatch, and truncation explicitly. Tolerate additive
   unknown response fields.
3. Classify Anthropic `end_turn`, `refusal`, `max_tokens`, and other documented
   stop reasons explicitly. Preserve request ID and cache token dimensions.
4. Keep zero application retries and no tools. Do not replace the working
   stdlib transport with an SDK unless portability evidence justifies the added
   dependency; if an SDK is later used, set and test zero retries.
5. Update `cli.py` so credential descriptors remain caller-opened and never
   enter arguments, captures, or reports.

Acceptance: sanitized, documented API fixtures produce correct outcomes and
receipts; malformed/partial/error fixtures remain diagnosable offline.

### Phase 3 — Claude Code subscription fallback; no live call

1. Add the same envelope sink to `ClaudeCodeSubscriptionAdapter`; persist stdout
   and bounded stderr before checking exit status or parsing.
2. Prefer documented `stream-json` only if an offline current-client fixture
   proves structured output and terminal event extraction. Otherwise retain
   documented `json` and record provider attempt count `UNKNOWN`.
3. Remove exact `set(modelUsage) == {requested_model}` parsing. Extract and
   preserve all observed model entries, compare the documented selected/actual
   model conservatively, and fail on conflicting multi-model execution without
   deleting evidence.
4. Treat undocumented retry environment variables as best-effort client
   configuration, not a guarantee. Preserve documented retry events when
   available.
5. Record the exact Claude Code version and effective boundary flags. Refuse
   unsupported versions before a live run.

Acceptance: historical-shape fixtures, current documented JSON, JSONL retry,
and error fixtures are recoverable and never overstate one provider request.

### Phase 4 — bounded acceptance, separately authorized

Run one Anthropic API acceptance packet below. If it passes transport, envelope,
postflight, and human review, Work Entry 013 can then compare the same task with
the local baseline. Do not start Work Entry 014 until its registered dependency
is met or Louis explicitly changes the sequence.

### Migration and rollback

- New code reads v1-v4 receipts; old receipts are immutable.
- New live adapters emit v4. Synthetic/fake adapter tests may continue to emit
  older versions only where compatibility is the subject of the test.
- Gate v4 execution behind an explicit CLI subcommand/version until offline
  fixtures pass.
- Rollback is selecting the previous adapter/receipt path for synthetic work;
  never delete v4 evidence. A live attempt under v4 remains governed by its
  original grant even if code is rolled back.
- No database or daemon migration is required.

### Code to avoid

- no general agent framework;
- no retry service or automatic fallback;
- no browser automation or auth extraction;
- no universal provider-schema superset in portable jobs;
- no second deterministic assembly engine;
- no automatic semantic “repair” model;
- no abstraction over every possible provider before Claude and OpenAI fixtures
  prove the two needed shapes.

## Offline verification matrix

All fixtures must be synthetic or authorized sanitized captures and carry a
small provenance sidecar: interface, source, original/synthetic status, capture
date, sanitization actions, and raw/sanitized hashes.

| Case | Expected connector result | Required assertion |
| --- | --- | --- |
| Anthropic valid text + schema payload | COMPLETED | ID/model/stop/usage/request ID and payload preserved |
| OpenAI valid Responses structured text | COMPLETED | Status/model/output/usage and request IDs preserved |
| Claude Code documented JSON with `structured_output` | COMPLETED | Wrapper metadata separated from payload |
| Claude Code JSONL init/retry/result | COMPLETED or policy-refused | Retry count and actual model evidence preserved; no hidden flattening |
| API refusal | REFUSED | No schema-repair attempt; provider reason preserved |
| Provider HTTP error JSON | PROVIDER_ERROR | Body/request ID/status captured and sanitized |
| Client nonzero exit with stdout result | CLIENT_ERROR or documented terminal state | Both streams captured before classification |
| Empty body/stdout | PARSE_FAILED | Empty length/hash recorded |
| Malformed JSON | PARSE_FAILED | Exact bounded bytes retained |
| Oversized envelope | POLICY_REFUSED | Prefix + overflow marker retained; no partial parse |
| Incomplete/truncated response | INCOMPLETE | Stop/incomplete details and truncation recorded |
| Missing usage | COMPLETED with UNKNOWN usage | No zero or estimate mislabeled observed |
| Missing model identity | outcome per route policy | Requested model never mislabeled observed |
| Additive unknown fields/events | otherwise unchanged | Parser tolerates documented schema evolution |
| Tool-call output when tools forbidden | POLICY_REFUSED | No tool execution; payload not accepted |
| Timeout before socket/client start | NOT_SENT | Safe fresh authority may be possible after review |
| Timeout after possible send | SUBMISSION_UNCERTAIN | No resend under same grant |
| Disconnect after response ID | SUBMISSION_UNCERTAIN/recoverable | Ledger permits retrieval, not generation resend |
| Offline reprocessing | linked new receipt | Original envelope/receipt unchanged; actions and policy versions explicit |
| Code fence and singleton claim | strict refusal, optional versioned recovery | Extraction, normalization, and policy change remain distinct |

Suggested fixture layout:

```text
tests/fixtures/connectors/
  anthropic-messages/
  claude-code-json/
  claude-code-jsonl/
  openai-responses/
  shared-errors/
```

Create `tests/test_response_boundary.py` for capture/outcome invariants and keep
provider extraction tests in `tests/test_adapters.py`. Retain DERP policy and
assembly tests separately. This prevents a transport fixture from silently
testing a policy decision.

## Proposed bounded live acceptance packet — not authorized or executed

This is an engineering acceptance call, not the Work Entry 015 continuation and
not a cohort.

| Field | Proposed value |
| --- | --- |
| Work Entry | Resume 013 only after separate implementation and live authority |
| Route | Direct Anthropic Messages API |
| Model | Requested `claude-sonnet-5-5`; record returned model exactly; verify current availability through the Models API/account before grant |
| Billing source | `CLAUDE_API`; never Claude subscription allowance |
| Workload | Existing 38-byte synthetic field extraction: Ada, Basic, preserve `REF-42` |
| Input/output | At most 4,000 input tokens and 600 output tokens |
| Deadline | 30 seconds outer deadline |
| Attempts | One provider request, zero application/SDK/CLI retries, no fallback |
| Tools | None |
| Estimated maximum | $0.014 at documented standard Sonnet 5.5 rates: 4,000 × $2/M + 600 × $10/M; estimate only |
| Required credential | Existing approved Anthropic API credential through caller-opened descriptor; no credential in arguments/logs/capture |
| Admission | Exact TEST_ONLY profile and matching Work Entry 005 admission limited to this packet |
| Grant | Fresh content-bound LIVE grant covering model, adapter, hashes, deadline, output, cost estimate, and one provider request |
| Capture | Attempt intent first; raw body + allowlisted headers before parse; sanitized envelope; outcome/receipt/manifest |
| Deterministic success | Completed envelope; requested/observed identity recorded; valid required fields; `REF-42` preserved; no tool/fallback/retry evidence; bounds respected |
| Human success | Louis records ACCEPTED after seeing full untrusted artifact and receipt |
| Refusal | Preserve provider refusal/error/incomplete evidence; no resend |
| Uncertainty | Mark SUBMISSION_UNCERTAIN; stop; use request identifiers for diagnosis; no resend |
| Stop conditions | Packet/hash drift, credential/billing/model unavailable, capture not armed, retry cannot be disabled, bounds mismatch, uncertain prior attempt, or response overflow |

Sonnet 5.5 is chosen for this proposed packet because it is current, its bounded
worst-case standard token estimate fits the historical $0.02 ceiling, and Haiku
4.5 is close to its documented not-before retirement date of 2026-10-15. This is
a research recommendation, not account-access evidence. If current access or
pricing differs at execution time, regenerate preview/admission/grant rather
than silently substitute a model.

After transport acceptance, a separately authorized useful test may run the
Work Entry 015 continuation packet. Do not count that as a direct model-vs-model
quality comparison because the frontier receives the local attempt and review
findings. A fair comparative evaluation requires a separately declared arm that
receives the same original source packet and contract as the local arm.

## Cost and maintenance comparison

### Documented pricing calculations

At 4,000 maximum input and 600 maximum output tokens, standard short-context
list-price ceilings are:

| Candidate | Published rates per 1M input/output | Arithmetic ceiling | Interpretation |
| --- | --- | --- | --- |
| Claude Sonnet 5.5 | $2 / $10 | $0.008 + $0.006 = **$0.014** | Estimated API token charge; account/service-tier specifics still apply |
| Claude Haiku 4.5 | $1 / $5 | $0.004 + $0.003 = **$0.007** | Cheaper, but retirement risk is immediate at this research date |
| OpenAI GPT-6.1 Sol | $2 / $10 | $0.008 + $0.006 = **$0.014** | Estimated standard API token charge |
| OpenAI GPT-6 Luna | $0.10 / $0.50 | $0.0004 + $0.0003 = **$0.0007** | Very cheap; quality for this workload is an evaluation question |
| Claude Code / ChatGPT-plan route | Subscription allowance | **UNKNOWN incremental monetary cost** | Uses constrained allowance/credits and has opportunity cost; not zero |
| Existing local GPU route | Owned hardware | **UNKNOWN** | No hosted charge; energy, maintenance, and review cost not measured |

These calculations exclude taxes, regional/fast tiers, long-context uplifts,
explicit cache-write charges, extra tools, and retries. The live preview must
select a model and tier and include every applicable billing dimension.
`max_output_tokens` and bounded input make a conservative local estimate
possible; they do not create a provider-enforced per-call dollar cap. Provider
organization/project spend limits are aggregate controls. Claude Code's
`--max-budget-usd` is documented as a client control and its reported costs are
client-side estimates, not a general subscription invoice measurement.

### Observed evidence versus estimates

- Local extraction: 9,432 ms; accepted; two minutes human review; tokens and
  operating cost unknown.
- First local change summary: 10,560 ms; output hit the 600-token bound and was
  malformed.
- Repaired local attempt: 8,306 ms; complete raw response; original strict
  refusal; offline reprocessing reached review-required; tokens, stop reason,
  cost, preparation time, and review time unknown; Louis ultimately requested
  frontier continuation.
- Claude historic attempts: client returned in the second report at about 2.160
  seconds, but actual model, usage, payload, and provider request count are
  unknown. They cannot support quality or cost comparison.
- All API prices above are estimates from current documentation, not observed
  account charges.

### Maintenance judgment

Direct APIs have the lowest long-term boundary maintenance because their response
contracts, errors, request IDs, structured outputs, and billing are provider
products intended for applications. The repository already has both transports.
The repair is mainly capture, classification, and accounting.

Claude Code subscription reuses an existing subscription but adds client-version,
settings, agent-loop, retry, and envelope-shape maintenance. SIWC can provide
supported ChatGPT-plan Responses access but adds OAuth/client registration and
license/eligibility work. These paths can be economically useful when allowance
is otherwise unused, but their engineering and opportunity cost must be measured,
not assumed away.

The owned local path has the lowest external dependency and no API invoice. Its
observed semantic/review burden is material: one useful summary did not reach
human acceptance. The right frontier connector reduces that burden only if
accepted frontier completions save more review/repair effort than their packet,
call, and review costs.

## Decisions requiring Louis's judgment

1. **API billing versus subscription allowance:** approve an existing Anthropic
   API credential/billing path for the reliable primary route, or explicitly
   accept one-client-run/unknown-provider-retry semantics for Claude Code.
2. **Open-source/SIWC direction:** decide whether helix-offload will ever receive
   an open-source license and SIWC client integration. Do not couple that product
   decision to the connector repair.
3. **First live task:** use the tiny extraction packet for transport acceptance,
   then separately authorize the Work Entry 015 continuation; or accept the
   higher diagnostic risk of making the continuation the first API call.
4. **Receipt v4 migration:** approve replacing the misleading failure boolean
   with explicit submission/generation states while preserving old receipts.
5. **Raw evidence retention:** choose a consumer retention period and whether
   encrypted/private raw envelopes may be kept beyond disposition. Publication
   should remain sanitized by default.
6. **Comparison objective:** decide whether the next metric is accepted artifact
   quality, reduced human review time, avoided frontier continuation, latency,
   or monetary cost. One call cannot optimize all five.

## Explicit unknowns

- Exact contents and exact rejected field of both historic Claude envelopes.
- Current Claude subscription allowance/model entitlement.
- Current Anthropic API credential, balance, workspace, and model entitlement.
- Current OpenAI API credential/billing readiness.
- Louis's current SIWC eligibility or desire to license the private repository.
- Whether the current Claude Code version emits schema-constrained output in
  `stream-json` with all retry/model evidence needed by this adapter. Verify
  offline against a no-network help/version capture or an authorized sanitized
  fixture before a model call.
- Whether provider-side generation completed after any historic ambiguous event.
- Local energy cost, local token counts, and review effort for Work Entry 015.
- Comparative semantic quality of Sonnet 5.5, GPT-6.1 Sol/Luna, and phi4-mini on
  the exact same source packet.

## Exact recommended next engineering action

Resume Work Entry 013 for an **offline-only connector-boundary implementation**:
add bounded envelope capture and `connector-outcome/v1`, emit receipt v4 with
explicit submission state, route the existing Anthropic Messages adapter through
it, and pass the fixture matrix without invoking any provider. Review that diff
before requesting a fresh one-call Anthropic API acceptance grant. Leave the
Claude Code subscription path as a captured conditional fallback and Work Entry
014 parked until the Claude comparison dependency is resolved.

## Source index

The complete source list, dates, repository file hashes, claim mapping, and
limitations are in
`2026-10-03-helix-offload-frontier-connector-repair.sources.json`. Key changing
technical sources include:

- Anthropic headless client and structured output:
  https://code.claude.com/docs/en/headless
- Anthropic Claude Code CLI controls:
  https://code.claude.com/docs/en/cli-reference
- Anthropic Messages API and errors:
  https://platform.claude.com/docs/en/api/messages/create and
  https://platform.claude.com/docs/en/api/errors
- Anthropic current models and pricing:
  https://platform.claude.com/docs/en/models/overview
- OpenAI API overview/request IDs:
  https://developers.openai.com/api/reference/overview
- OpenAI Structured Outputs and Responses:
  https://developers.openai.com/api/docs/guides/structured-outputs and
  https://developers.openai.com/api/reference/cli/resources/responses/methods/create
- OpenAI current models and pricing:
  https://developers.openai.com/api/docs/models and
  https://developers.openai.com/api/docs/pricing
- OpenAI Sign in with ChatGPT and Codex app-server:
  https://developers.openai.com/siwc/token-sharing-open-source and
  https://developers.openai.com/siwc/token-sharing-open-source/codex-app-server
