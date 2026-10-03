# helix-offload Claude integration failure analysis

- Research date: 2026-10-03
- Retrieval date for changing web sources: 2026-10-03
- repo-cp baseline: `27d18a00c269b8c8652ca251bb2119dea6b5bafc`
- helix-offload baseline: `d6c7f708fa5bee2845fbd11b67a946161898dfe1`
- Installed client inspected without inference: Claude Code `2.1.283`, executable
  SHA-256 `1859583ce32920595c61ef868bee52e1b1594f7486db209935e01f1e5e804ae2`
- Delivery stage: research and recommendation only

## Concise explanation

The evidence does not support one recurring Claude defect. It records **four
sent Claude Code client runs**, not three model invocations, and they fall into
three failure classes:

1. Two 2026-10-01 field-extraction runs returned client JSON but the adapter
   discarded the envelopes after strict parsing failed. Attempt 001 exposed one
   real parser defect: schema output belongs in `structured_output`, not only
   `result`. Attempt 002 failed after that correction, but its discarded
   envelope makes the exact reason unknowable.
2. A 2026-10-03 change-summary run failed inside Claude Code's own
   `--json-schema` validation. The client reported missing `risks` and
   `review_notes` plus a 650-character summary above the 480-character limit,
   then returned `error_max_structured_output_retries` without the rejected
   candidate.
3. The repaired stream run completed generation and finally made the transport
   observable. DERP then correctly refused it because Claude Code reported
   5,202 input and 5,574 total tokens against 4,000/4,600 workflow limits. A
   separate offline diagnostic found the unchanged text was not the requested
   JSON. The text explicitly treated a historical packet field,
   `NOT_AUTHORIZED_FRESH_ONE_INVOCATION_GRANT_REQUIRED`, as current authority
   and asked for permission.

The count of “three unsuccessful attempts” can therefore be reconciled as
three failure classes or three remembered milestones. The immutable attempt
records establish four caller-launched client runs. They do **not** establish
four provider requests: underlying request and retry counts are `UNKNOWN` for
every run. Offline recovery and reprocessing are not additional model calls.

The latest failure was not another envelope-parser failure. The stream adapter
captured a complete result, model, stop reason, usage and timing. The next repair
should change the **model-visible projection** of the change-summary packet:
keep current execution authority exclusively in host-enforced admission/grant
state; keep historical authority and other deterministic metadata available to
deterministic assembly; send the model only the bounded narrative evidence,
short source IDs and an explicit instruction/data boundary. Do not change the
stream parser, model, output contract or limits at the same time.

## Evidence method and limits

This analysis used:

- public, Git-owned helix-offload attempt records and code at the revisions
  identified below;
- repo-cp frontier-connector research at
  `a48a802132f1db64304a032bcc4b207d7f26ea71`;
- the installed executable's `--version` and `--help` output only; and
- current first-party documentation plus narrowly relevant upstream issues.

No credential store, secret-bearing environment, provider account, dashboard,
session transcript outside published evidence, or private raw capture was read.
No authentication command, model/API/GPU invocation, installation, update or
configuration change occurred. A recognized flag or passing fixture is not
treated as live proof.

The first two attempt records do not bind an exact executable hash or execution
tree. Their evidence commits and ancestry are durable, but the exact in-memory
code that launched attempt 001 is especially uncertain because its report says
the `structured_output` correction was made after the consumed call while the
first durable implementation commit already contains that correction. The
ledger labels this gap rather than choosing a convenient revision.

## Attempt ledger

| Client run | Date; durable revisions | Route, client and model | Input, prompt and contract | Submission, capture and first failing layer | Follow-up and live verification |
| --- | --- | --- | --- | --- | --- |
| `work-entry-010-claude-live-001` | 2026-10-01; implementation/evidence ancestry `ffcbf284d78bcd0486056c4e5b0a4c6d8419c480` -> `6e02f1128a990dfc62e28da6adcc90143a2731cf`; exact execution tree not recorded | Existing `claude.ai` Pro subscription; `claude-code.subscription.v1`; requested `claude-haiku-4-5-20251001`; observed model `UNKNOWN`; contemporaneous path matrix says Claude Code 2.1.283, but the attempt did not bind its executable | 38-byte Ada/Basic/`REF-42` field extraction; JSON output plus `--json-schema`; instructions were supplied through `--system-prompt` and duplicated in stdin before input; one turn; 30 s; 4,000 input, 600 output, 4,600 total; general API retries 0; structured-output attempts configured as 1 after a mistaken interpretation | One client run `SENT`; no timeout/disconnect/manual retry; provider requests/retries `UNKNOWN`; raw envelope absent. Adapter returned `HOSTED_RESPONSE_INVALID`; no artifact/postflight. Demonstrated code defect: parser did not read documented `structured_output`. The precise returned envelope is missing. | Parser changed to prefer `structured_output`; synthetic fixture passed. Attempt 002 later showed this repair was insufficient. |
| `work-entry-010-claude-live-002` | 2026-10-01; prepared after `6e02f112...`; evidence commit `9ec732046ba6481be70018277b91ff04534baa8d`; runtime code SHA not embedded | Same Pro subscription adapter and requested model; observed model and exact bound client version `UNKNOWN` | Same 38-byte packet and schema path; same duplicated instructions; 30 s; 600 output; general and structured-output retry settings 0 | One client run `SENT`; no timeout/disconnect/manual retry; provider requests/retries `UNKNOWN`; raw envelope again absent. Parser handled `structured_output` but still returned `HOSTED_RESPONSE_INVALID`. Exact predicate, payload, usage and model are unknowable. | Established that field-name repair alone did not solve the route. Led to the evidence-first connector boundary; no live result can verify a more specific diagnosis. |
| `work-entry-013-claude-change-summary-live-001` | 2026-10-03; execution base by ancestry `a93eb46dd40b120f298bcde2681bd21679ca08a5`; evidence commit `8421ac36e9563120c670a2d803295faf22969c18`; attempt record does not hash code | Claude Code 2.1.283, binary SHA above; existing Pro subscription; requested Haiku 4.5; observed model `UNKNOWN` | Work Entry 015 packet SHA-256 `f5bb1cd016bd36f847d9129efd2057b6a36ddc9d67bbddce56e6384e07966f41`; commit range `9ec7320...ca999875...`; `change-summary-v1`; JSON output plus `--json-schema`; instructions duplicated in system prompt and stdin; v1 generated contract (480-char summary); 120 s; 600 output; 4,000/4,600 input/total; tools/MCP/session/fallback disabled; configured general and structured retries 0 | One client run `SENT`, response received; captured sanitized envelope. Client terminal `error_max_structured_output_retries`; diagnostic: missing `risks` and `review_notes`, summary 650 > 480. Rejected candidate not exposed. `num_turns=2`, empty model usage and 0 ms API duration do not prove no provider work. First failing layer: Claude Code client structured-output validation, before DERP parsing/postflight. | Connector-outcome/v1 and receipt v4 made submission and inference uncertainty explicit. Removing `--json-schema`, using stream JSON and parsing at DERP was live-verified by the next run. Contract tightening was only partially tested because the next output was prose, not JSON. |
| `work-entry-013-claude-change-summary-live-002-attempt-001` | 2026-10-03; repaired base `15b86e6c09a5602bc40125fe6bee2a45727c787a`; evidence commit `f24cdc317c364aa01c72eac162fb1281fcafa2f5`; attempt record does not hash code | Claude Code 2.1.283, binary SHA above; existing Pro subscription; requested and observed `claude-haiku-4-5-20251001` | Same packet SHA and repository range; stream-json/verbose/partial messages; no `--json-schema`; v2 compact contract (240-char summary, <=2 risks, <=1 review note); instructions once through `--system-prompt`; stdin contained serialized task data; 120 s; 600 output; 4,000/4,600 input/total; tools/MCP/session/fallback disabled | One client run `SENT`; 188 events, one assistant event, one terminal success, `end_turn`, not truncated, no observable `api_retry` or tool event. Provider request count `UNKNOWN`. Complete capture available. Reported 5,202 input / 372 output / 5,574 total, 5,550 ms and $0.012261 list-cost estimate. First authoritative failure: DERP `USAGE_LIMIT_EXCEEDED`, so parsing/postflight/assembly did not run. Offline only: text was malformed JSON and treated historical authority as current. | Proved stream capture/extraction and accounting worked. Did **not** prove the compact contract, semantic quality, preventive input capping or single-provider-request behavior. |

All four runs used one caller-launched process and no manual relaunch. None
supports a claim of exactly one underlying provider request. Attempts 001 and
002 have no response bytes. Attempt 003 has the terminal client diagnostic but
not the rejected candidate. Attempt 004 has complete bounded private capture
and an allowlisted public derivative.

## Installed Claude Code capability and uncertainty matrix

Official documentation and upstream pages in this section were retrieved on
2026-10-03.

| Control or behavior | Officially documented | Verified for installed 2.1.283 without inference | Demonstrated by retained live evidence | Remaining limit |
| --- | --- | --- | --- | --- |
| Headless execution and stdin | `claude -p`; piped stdin supported and capped at 10 MB | `--help` recognizes `-p`, `--input-format text|stream-json` | All four client runs used print mode; latest packet reached generation | Passing stdin does not reveal the complete provider request or hidden client scaffolding. |
| System prompt | `--system-prompt` fully replaces the default; `--append-system-prompt` preserves it | Both flags recognized | Latest run used replacement and supplied instructions once | Claude Code's system prompt is unpublished; replacement does not prove absence of all client/provider scaffolding. |
| JSON result | `--output-format json`; schema value in `structured_output` | `json` and `--json-schema` recognized | First two runs returned JSON; third returned a structured-output terminal error | First two envelopes were discarded; exact shapes are absent. |
| Stream JSON | JSONL; `--verbose --include-partial-messages`; last line is terminal result | All flags recognized | Latest run produced 188 parseable events and a matching terminal result | Stream events expose what the client emits, not hidden candidates or provider request count. |
| Client structured output | `--json-schema` validates after the agent workflow; current docs describe first attempt plus corrective attempts | Flag recognized; schema fixture tests are offline only | Third run hit `error_max_structured_output_retries` | Upstream issues show similar symptoms in other versions/modes, but do not prove this run's root cause. |
| Tool restriction | `--tools ""` disables built-ins; deny patterns supported | Flags recognized and command construction tested | Latest stream had zero tool events | Absence of tool events is not a proof of every effective ambient policy. |
| MCP restriction | `--strict-mcp-config` plus empty `--mcp-config` ignores other MCP config | Flags recognized and command construction tested | Latest stream had zero MCP/tool events | No effective-policy dump was obtained; managed policy can still apply. |
| Safe/restricted modes | Safe mode disables customizations but not managed policy; restricted mode removes command/code tools and ignores user/project/local settings while managed settings and explicit settings remain | Flags recognized | Requested for all runs; no tool events in latest run | Installed help and docs explicitly preserve managed-policy influence. Current managed config was not inspected. |
| Hooks/plugins/ambient configuration | Safe mode and restricted mode narrow discovery; managed settings have highest precedence | Flags recognized | No hook/plugin/tool events observed in latest capture | “Disabled” is a requested client configuration, not a proof that no managed instruction affected the request. |
| Maximum turns | `--max-turns` limits agentic turns, not provider requests | Flag recognized | Latest run reported one turn; structured-output run reported two turns despite one-turn configuration | Turn count is not request count and schema correction may add client behavior. |
| Output tokens | `CLAUDE_CODE_MAX_OUTPUT_TOKENS` limits output for “most requests”; model caps also apply | Environment variable is documented; adapter sets 600; not exposed by `--help` | Latest output was 372 tokens | One under-limit result does not prove the cap; docs do not promise every request uses it. |
| Input/total tokens | No Claude Code flag inspected supplies a preventive per-run input or total-token cap | None | DERP compared reported usage only after response | The 4,000/4,600 gates were retrospective. They prevented acceptance, not consumption. |
| Deadline | No native per-run deadline flag was found; adapter uses `API_TIMEOUT_MS` and a 120 s subprocess timeout | Wrapper code and offline tests verified | Runs returned within deadline | Killing a client after timeout cannot prove the provider did not execute. |
| API retries | `CLAUDE_CODE_MAX_RETRIES` controls failed API retries; default 10; retry watchdog can alter defaults/caps if enabled | Env variable documented; adapter sets 0 in a stripped environment | Latest stream had zero observable `system/api_retry` events | No documented guarantee says all provider activity is observable as retry events. Provider request count remains `UNKNOWN`. |
| Structured-output retries | `MAX_STRUCTURED_OUTPUT_RETRIES` is total attempts, default 5 (first plus four retries) | Documented; current stream route does not set it because it removed `--json-schema` | Third client said failure after 0 attempts; attempt 001 used 1 based on a mistaken older interpretation | Version wording and terminal diagnostics are awkward; do not infer actual provider calls from the integer. |
| Session persistence | `--no-session-persistence` disables saving/resume for print mode | Flag recognized | Requested for all runs; the first recovery found no session | Lack of a saved session is consistent with the control, not proof of provider-side deletion. |
| Model selection | Full ID via `--model`; fallback chains are separately configurable | `--model` and `--fallback-model` recognized | Latest requested/observed model matched exactly | Earlier observed model is missing. Empty fallback setting plus no fallback event is not a universal provider guarantee. |
| Usage and cost | JSON/stream terminal metadata includes usage and client-side list-price estimates; subscription session cost is not billing truth | Output modes recognized | Latest returned token counts and $0.012261 list cost | Marginal Pro-subscription charge is `UNKNOWN`; cache/category breakdown is incomplete in public evidence. |
| Subscription versus API auth | Claude.ai OAuth can use subscription allowance; `ANTHROPIC_API_KEY` overrides it in `-p`; `--bare` does not read OAuth/keychain | Installed help documents `--bare` auth restriction; no auth-status command was run | Retained evidence identifies Pro subscription route; current allowance is unavailable per task context | Current authentication readiness was deliberately not queried. Console/API credits do not automatically fund the subscription route. |

Primary documentation:

- https://code.claude.com/docs/en/cli-reference
- https://code.claude.com/docs/en/headless
- https://code.claude.com/docs/en/env-vars
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/authentication
- https://code.claude.com/docs/en/model-config
- https://code.claude.com/docs/en/costs

## Latest completed-generation failure

### Where the apparent authority conflict came from

The host packed a Work Entry 015 change-summary request into
`job.input.content`. The unchanged packet included this source-data array:

```json
[
  {"name":"execution","value":"NOT_AUTHORIZED_FRESH_ONE_INVOCATION_GRANT_REQUIRED"},
  {"name":"generated_output","value":"UNACCEPTED_HUMAN_REVIEW_REQUIRED"},
  {"name":"change_scope","value":"EXPLICIT_ALLOWLIST_5_OF_38_CHANGED_PATHS"}
]
```

That array described the **prepared packet's historical authority state**. The
current one-use execution grant was enforced by the host and was not sent to the
model. The model-facing instruction said repository excerpts and receipt text
were untrusted data and told the model not to copy authority, but it did not say
plainly that packet authority values were historical facts with no power over
the current run. The serialized task also retained
`authority_reference: work-entry-013:claude-stream-json:next-live-grant-required`
outside the packed content.

The generated text quoted the packet's authority meaning and asked whether it
should proceed. This confirms **interpretation of task data as live authority**.
It does not prove a Claude model defect or a Claude Code defect. The strongest
explanation is a prompt/data-boundary defect: stale preparation state and live
host authority were represented in different places, while only the stale
state was model-visible. The explicit instruction not to copy authority was
insufficient to make that distinction operationally clear.

Competing explanations:

- **Confirmed contributor:** model-visible preparation-state text directly
  contradicted the fact that a host grant had already been issued.
- **Probable contributor:** Claude Code/client scaffolding emphasizes safety and
  authorization, increasing the salience of the uppercase authority value. The
  exact scaffolding is unpublished, so this cannot be quantified.
- **Not supported as a root cause:** a provider safety refusal. The terminal
  stop was `end_turn`, not a provider refusal, and the response was ordinary
  prose.
- **Not supported as a root cause:** stream extraction. Terminal text matched
  the last assistant text, and capture/extraction completed.

### What the 5,202 input tokens do and do not mean

Reconstructable facts:

- packed `input.content`: 8,541 UTF-8 bytes;
- generated system instruction: 817 UTF-8 bytes;
- serialized stdin prompt: 9,321 UTF-8 bytes;
- Claude Code reported input usage: 5,202 tokens;
- output: 372 tokens; total: 5,574 tokens.

The 9,321-byte stdin value wraps the already JSON-serialized packet as a JSON
string plus objective/workload/lane/job-family fields. It does not include the
separate system instruction. Bytes are not tokens. The public terminal metadata
does not partition usage among visible packet text, the system prompt, Claude
Code/client scaffolding, provider transformations, cache reads/writes or other
categories. Anthropic's Messages API documentation likewise warns that API
transformations mean usage does not map one-to-one to visible request text.

Controls:

- the 600 output-token environment setting was intended as a preventive client
  bound and the observed output stayed below it, but one observation does not
  prove enforcement;
- the 120-second subprocess/API timeouts were preventive local bounds;
- the 4,000 input and 4,600 total-token limits were **retrospective DERP
  acceptance checks**. They detected excess only after the client had consumed
  usage; and
- the public Claude Code route exposes no verified preventive input/total-token
  cap. Direct Anthropic API token counting is a separate endpoint and therefore
  a separate request, not a free inference inside the subscription client.

## Reassessment of earlier diagnoses

| Earlier diagnosis or repair | Evidence assessment | What it actually established |
| --- | --- | --- |
| Read `structured_output` instead of only `result` | **Confirmed defect and correct repair.** Official headless docs specify the field. | Fixed one parser mistake. Attempt 002 proved it was not the whole problem. |
| Treat attempt 002 as another field-name failure | **Unsupported.** No envelope survived. | Nothing beyond `HOSTED_RESPONSE_INVALID` can be attributed. |
| Relax exact `modelUsage` parsing | **Plausible robustness repair, not historical diagnosis.** Attempt 002 might have failed there, but no bytes exist. | Prevents one brittle future rejection; it does not explain the old run. |
| Add bounded envelope capture and connector outcome/receipt v4 | **Confirmed necessary and live-verified.** | Attempt 003 retained its client error; attempt 004 retained complete generation and truthful submission/generation state. |
| Remove `--json-schema`; parse final stream output in DERP | **Directly addressed demonstrated client schema-layer loss; live-verified.** | Attempt 004 exposed the complete text, model, usage, stop reason and timing. It did not make the content valid. |
| Remove duplicated instructions from stdin | **Confirmed implementation cleanup; causal benefit unresolved.** | Latest run received instructions once and completed. It still ignored the requested JSON shape. |
| Tighten output to v2 and include a tiny valid example | **Reasonable output-budget experiment; live efficacy unresolved.** | Latest output was below 600 tokens but prose, so v2 conformance was never tested. |
| Attribute attempt 003 to a known upstream bug | **Not established.** | GitHub issues show structured-output failures in other versions, platforms, Workflow/subagent modes or schemas. Similar symptoms are corroboration, not identity of cause. |
| Treat 600 output tokens as the reason for attempt 003 | **Not established.** | The client reported a 650-character summary, not a token truncation or `max_tokens` stop. Missing sibling fields were also reported. |
| Treat 5,202 input tokens as packet bytes converted to tokens | **Incorrect.** | Only aggregate client usage and visible byte counts are known. |

Relevant upstream reports, used only as secondary evidence:

- Claude Code 2.1.81 `--json-schema`/StructuredOutput conflict:
  https://github.com/anthropics/claude-code/issues/37904
- Claude Code 2.1.30/2.1.31 first-run structured-output failure:
  https://github.com/anthropics/claude-code/issues/23265
- Workflow/subagent invalid-escape retry failure on 2.1.215:
  https://github.com/anthropics/claude-code/issues/79019
- `format: uri` behavior on 2.1.136:
  https://github.com/anthropics/claude-code/issues/57757

None matches all of installed version 2.1.283, print mode, Pro subscription,
the exact change-summary schema and the retained attempt configuration. The
historical schema has no `format: uri`, and the Workflow/subagent reports use a
different interface.

## Root-cause findings

### Confirmed

1. Four client runs were sent; offline recovery/processing added no model calls.
2. Attempts 001 and 002 lost the evidence needed for exact diagnosis.
3. Attempt 001 exposed a documented envelope-field parser defect.
4. Attempt 003 failed in Claude Code's schema-validation layer before DERP.
5. Attempt 004 completed client-visible generation and was first refused by a
   retrospective usage policy, not by transport or envelope extraction.
6. The attempt 004 packet exposed historical “not authorized” state to the
   model while the actual issued grant remained host-only.
7. The response interpreted that historical state as a reason to stop.
8. Attempt 004's unchanged output was malformed for the v2 JSON contract.
9. No run proves a single underlying provider request; missing evidence is not
   evidence of zero requests or retries.

### Probable

1. The model-visible authority/preparation state was the principal cause of the
   permission-seeking prose in attempt 004.
2. Claude Code/client overhead contributed to reported input usage beyond what
   visible packet byte counts alone suggest.
3. Attempt 003's large summary plus omitted siblings reflects contract/prompt
   pressure at the client structured-output boundary, but the missing candidate
   prevents separating model serialization, client validation and retry
   feedback behavior.

### Unresolved

1. Exact envelopes, observed models, usage and first rejected predicates for
   attempts 001 and 002.
2. Exact Claude Code binary and code tree used for each 2026-10-01 invocation.
3. Underlying provider request/retry/inference behavior for attempts 001-003,
   and provider request count for attempt 004.
4. Exact decomposition of 5,202 input tokens.
5. Whether a clean model-view projection is sufficient for valid JSON on the
   installed subscription route.
6. Current subscription allowance, usage-credit status, Console/API credit
   balance and model entitlement; none was inspected.

## Interface and billing options

| Approach | Benefit | Burden and uncertainty | Disposition |
| --- | --- | --- | --- |
| Existing Claude Code subscription stream route | Already captures complete stream evidence; latest run proved requested/observed model, usage and completion metadata; reuses subscription authentication | Agent-client overhead; provider request count unknown; no verified preventive input cap; managed policy remains ambient; allowance currently unavailable | **Continue only for one decisive diagnostic after the model-view boundary is fixed.** It is now diagnosable, not yet accepted. |
| Same route with simplified model-visible packet | Removes the demonstrated authority ambiguity and reduces visible input while keeping the comparison task, model, route and contract stable | Still cannot guarantee provider request count or pre-send input tokens | **Recommended smallest repair.** Implement offline, then run once only under new authority and available subscription/usage-credit allowance. |
| Direct Anthropic Messages API | Explicit request body; direct model/usage/stop/request IDs; `max_tokens`; no Claude Code agent loop; separate token-count endpoint available | Separate Console/API credential and billing; token counting would be an additional API request; changes transport and billing; no current live acceptance | **Preferred eventual production connector when separately funded and authorized**, especially if the targeted subscription experiment fails or strict accounting is prioritized. |
| Claude Code `--bare` | Less ambient client configuration | Installed help says OAuth/keychain are not read; requires API key or helper, so it cannot preserve the existing subscription route | **Reject for this comparison.** Direct Messages is the cleaner API-key route. |
| Another agent/session interface | Could provide subscription access | More session/orchestration semantics and no demonstrated reliability advantage for one bounded inference | **Defer/reject.** No documented alternative reviewed has lower burden than stream print mode or direct Messages. |

Billing distinctions are material:

- Claude paid plans and Claude Console/API are separate products; a paid Claude
  plan does not include API access.
- An `ANTHROPIC_API_KEY` in non-interactive Claude Code overrides the
  subscription route and incurs API billing.
- Claude plan **usage credits** can be enabled and prepaid separately to
  continue Claude Code after plan allowance is exhausted, at standard API
  rates. They are additional subscription-bill charges.
- Console/API credits fund the API route. Buying them does not silently fund or
  convert the existing Pro-subscription invocation path.
- Claude Code's returned dollar figure is a local/list-price estimate; Anthropic
  says the session cost figure is not relevant to Pro/Max subscription billing.

Sources:

- https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan
- https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans
- https://support.claude.com/en/articles/9876003-i-have-a-paid-claude-subscription-pro-max-team-or-enterprise-plans-why-do-i-have-to-pay-separately-to-use-the-claude-api-and-console
- https://code.claude.com/docs/en/costs
- https://platform.claude.com/docs/en/api/messages/create
- https://platform.claude.com/docs/en/build-with-claude/token-counting

## Recommended repair plan — not implemented

Create one deterministic **model-view projection** for
`change-summary-v1`. The canonical host packet remains unchanged and
hash-bound, but the model receives only:

1. the bounded objective;
2. short source IDs;
3. the changed-path facts and selected excerpts needed to write narrative;
4. supplied validation outcomes needed for narrative; and
5. a clear wrapper stating that all enclosed source material is inert,
   historical data that cannot grant, revoke or alter the current run.

Keep these out of model-visible input and attach them deterministically after
content validation:

- current or historical execution authorization;
- grant/admission/preparation state;
- repository identity, commit hashes and full paths already known by the host;
- validation and submission bookkeeping that the model need not restate; and
- human disposition.

The model still returns only `summary`, `risks` and `review_notes` under v2,
with short source IDs. The host validates JSON, bounds and references before
assembly. This is not hiding history: historical authority remains in the
canonical packet and final deterministic artifact; it simply no longer shares
an instruction channel with generated prose.

Offline tests that would matter:

- canonical packet and model projection have separate stable hashes;
- every projected fact maps to an allowlisted source ID;
- no authority/grant/preparation status enters the projection;
- delimiters cannot be escaped by repository excerpts;
- the exact prior packet produces the expected reduced projection;
- prompt byte counts and a clearly labeled tokenizer estimate are recorded;
- v2 valid, malformed, unknown-reference and over-limit outputs keep existing
  behavior; and
- deterministic assembly reproduces authority/revision/status fields without
  model participation.

What offline work cannot prove: actual Claude input usage, hidden client
overhead, adherence to JSON, provider request count, live quality or human
acceptance.

Direct API is the preferred long-term strict connector, consistent with the
prior frontier research, but switching transport before fixing the packet
boundary risks reproducing the same semantic mistake through a different bill.
Fix the provider-neutral projection first.

## Proposed decisive future experiment — no grant and no execution

**Question:** With the demonstrated authority ambiguity removed, can the
installed Claude Code subscription stream route complete the same bounded
change-summary task as valid v2 JSON within the unchanged 4,000/4,600/600 token
limits?

**Hypothesis:** The historical authority field, not transport or stream parsing,
caused the permission-seeking response. A deterministic narrative-only
projection will yield contract-valid JSON and materially lower reported input
usage.

**Frozen inputs:**

- canonical source packet SHA-256
  `f5bb1cd016bd36f847d9129efd2057b6a36ddc9d67bbddce56e6384e07966f41`;
- repository range
  `9ec732046ba6481be70018277b91ff04534baa8d..ca9998755a463980bf9f618338d4e9303cd1f7bc`;
- lane/operation/job family
  `PORTFOLIO_REPOSITORY` / `DOCUMENT` / `change-summary-v1`;
- generated-content contract v2 and its existing limits;
- requested model `claude-haiku-4-5-20251001`; and
- Claude Code stream-json route, one client run, no tools/MCP/fallback/session,
  120 seconds, 600 output tokens, zero controllable API retries.

**Only changed architectural variable:** replace the serialized full packet in
stdin with the deterministic model-view projection described above and add the
explicit inert-data boundary. This necessarily changes both visible content and
its byte length; both are consequences of one boundary correction, not
independent tuning.

**Required evidence before launch:**

- new projection, instruction, workflow, preview, admission and proposed-grant
  hashes;
- exact client version and executable hash;
- exact command controls and stripped environment-variable names/values that
  are safe to publish;
- visible packet/projection/instruction/prompt byte counts;
- fresh one-client-run authority and available subscription allowance or
  separately authorized usage credits; and
- proof that no prior attempt has consumed the grant.

**Capture:** bounded private stdout/stderr before parsing; sanitized public
derivative; all stream event types; observed model, retry/tool events,
completion, usage/cache dimensions, client list cost and elapsed time; connector
outcome, receipt, parse/reference/postflight result and human disposition.

**Enforceable controls:** one caller-launched process; reservation; 120-second
process/API timeout; 600-token client output setting for requests to which the
client applies it; empty tools/MCP; no configured fallback; no session
persistence; application retry setting zero; no manual relaunch.

**Observational limits:** underlying provider requests, every internal retry,
hidden scaffolding and pre-send input/total-token consumption remain unproved.
The 4,000/4,600 gates remain retrospective. If strict preventive input counting
is required, use a separately authorized direct-API experiment with Anthropic's
token-count endpoint and count that endpoint as its own request.

**Outcomes:**

- **Success:** terminal `end_turn`; requested/observed model match; reported
  usage within 4,000 input and 4,600 total; valid v2 JSON; every source ID
  resolves; DERP postflight/assembly complete; artifact presented with human
  disposition `PENDING`.
- **Failure:** completed client run but repeated permission-seeking, malformed or
  out-of-contract JSON, invalid references, tool/retry evidence, or usage-limit
  refusal. Preserve and stop; do not repair or relaunch.
- **Inconclusive:** allowance/auth/rate/client startup failure, model mismatch,
  timeout/submission uncertainty, capture failure or ambiguous terminal output.
  It says nothing decisive about the projection hypothesis.

**Stop conditions:** any hash drift, unavailable subscription/usage-credit
route, inability to preserve capture, unexpected tool/MCP/fallback control,
prior submission uncertainty, or changed model/contract/limits.

**Next-step rule:** success permits human review and a bounded comparison with
the local Work Entry 015 result. A clean semantic/contract failure justifies
moving the same projection to the direct Anthropic Messages adapter when API
billing is separately authorized. An inconclusive infrastructure/account result
does not justify another model call.

## Reviewed revisions and explicit gaps

Reviewed helix-offload evidence commits:

- `6e02f1128a990dfc62e28da6adcc90143a2731cf`
- `9ec732046ba6481be70018277b91ff04534baa8d`
- `8421ac36e9563120c670a2d803295faf22969c18`
- `15b86e6c09a5602bc40125fe6bee2a45727c787a`
- `f24cdc317c364aa01c72eac162fb1281fcafa2f5`
- current main `d6c7f708fa5bee2845fbd11b67a946161898dfe1`

Reviewed prior research:

- repo-cp branch commit
  `a48a802132f1db64304a032bcc4b207d7f26ea71`
- report SHA-256
  `c21aababb63c5ae6b9b0cbc2da1565091a2921a15a62b9c85aeae8cada63423d`
- source-manifest SHA-256
  `1e8acd6a17a8164d0b43421c64efe580eba1e14d2ff4deedcb4c7c9988181331`

The companion source manifest records exact local file hashes, URLs and claim
scope. Its limitations include absent raw envelopes for attempts 001/002,
uninspected account/auth state, missing provider request counts, incomplete
token-category data and no live verification of the recommended projection.

## Exact recommended next action

After the active durability work is complete, authorize an **offline-only
change-summary model-view projection repair** in helix-offload. Keep the current
stream adapter, model, v2 contract and bounds unchanged; add the projection and
tests above; publish it; then review one fresh subscription-backed experiment
packet. Do not buy or spend credits, issue a grant or run the experiment as part
of that offline repair.

Live effects: Git research artifact creation and, after validation, a non-forced
push of the isolated research branch only. No model/API/GPU call, authentication
flow, credential/account/billing change, installation, runtime mutation,
canonical-main change or active durability-work mutation.
