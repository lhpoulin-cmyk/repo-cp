# Additional features for helix-offload

Research date: 2026-10-01

Evidence cutoff: 2026-10-01

Research status: recommendation only; no feature implementation or live execution

Local baselines inspected: repo-cp `9cd6d51b9e11a84a7bd1e4adcfa415438355879c` and helix-offload `c1a1c89f4d54d695adf6675e97c045a31267f29d`

Canonical baseline verification: direct remote `HEAD` and `refs/heads/main` queries matched both revisions on 2026-10-01.

## Executive recommendation

Finish the in-progress explicit CLI and `change-summary-v1`, run one authorized
hosted acceptance call, and collect the first comparable cohort before broadening
the product. Those steps are ahead of every feature proposed here.

After that evidence exists, the next three worthwhile features are:

1. **Portable qualification packs and repeatable candidate evaluation.** A
   candidate should enter DERP only through a versioned, workload-specific pack
   with frozen cases, deterministic scorers, human rubric results, exact model and
   adapter identities, and an explicitly accepted qualification result. This is
   the best protection against cheap-but-unsuitable routing and repeated manual
   trials.
2. **A portable release bundle with model manifests and adapter conformance.**
   Produce an installable wheel/source distribution, test it outside the source
   tree, load schemas through package resources, accept only explicit consumer
   configuration, and run an offline `doctor`/adapter conformance suite. Include
   model lifecycle and pricing evidence as supplied, time-stamped facts rather
   than built-in truth. This is what turns a private portfolio component into an
   independently usable toolkit without importing repo-cp.
3. **Acceptance-gated exact-result reuse.** Add a small content-addressed cache
   only if the first cohort shows recurring identical jobs. Reuse only an exact
   key over all material inputs and versions, and only after a human-accepted
   disposition. Do not begin with semantic similarity.

These are intentionally not a general agent framework. They improve evidence,
portability, and removal of duplicate calls while preserving the current
one-attempt adapter boundary and explicit authority.

One non-feature gate precedes external export: helix-offload currently has no
repository `LICENSE`, and its README states that no license grant has been
configured. The owner must choose and document a license before distributing the
toolkit for third-party reuse. This research does not recommend a particular
license and does not treat public source visibility as a grant.

## Evidence boundary

### Verified local implementation evidence

At helix-offload commit `c1a1c89f4d54d695adf6675e97c045a31267f29d`,
the inspected source and contracts establish:

- Execution Admission V1, strict qualified-profile matching, and a DERP V1
  recommendation/evaluation boundary;
- exact binding of an execution grant to a job, candidate, adapter, authority
  reference, and `SYNTHETIC` or `LIVE` mode;
- a fake adapter and a bounded OpenAI Responses adapter;
- one adapter attempt, with no automatic retry, fallback, dispatch, frontier
  call, or publication;
- deterministic document, inference, and narrow pure-Python postflight checks;
- returned receipts and a logical-job measurement summary; and
- synthetic validation only, with live acceptance explicitly not run.

The current adapter is a library integration. The current CLI exposes admission,
side-effect-free DERP recommendation, and fake execution; it does not expose a
live hosted command. The explicit CLI lifecycle and `change-summary-v1` are a
separate task in progress and are not counted here as established capabilities.

The repository contains consumer-neutral JSON interfaces, but some documentation
still describes repo-cp ownership and historical workstation/local-worker plans.
Those statements can remain provenance; an exported runtime must not require
repo-cp, a portfolio registry, or a Louis-specific path.

### External research evidence

External technical, project-maintenance, model, and pricing claims below were
checked against the primary URLs in the source register at the end of this note.
They are research inputs, not proof that helix-offload implements or qualifies
the described capability. Prices, model availability, API fields, project status,
and specifications can change after the stated retrieval date.

## Proposed sequence

| Order | Gate or feature | Why now | Proceed when | Stop or defer when |
| --- | --- | --- | --- | --- |
| 0 | Complete current CLI and `change-summary-v1` | Creates the first real entry and return path | Synthetic lifecycle passes and diff is reviewed | It expands into a daemon, dispatcher, or general repository agent |
| 1 | One bounded hosted acceptance call | Establishes that the destination, credential injection, grant, output, and receipt work together | Separate live authority and all packet prerequisites are satisfied | Access, disclosure, model, price, or authority is unknown |
| 2 | Comparable first cohort | Reveals quality, review effort, repeats, and failure causes | Logical jobs include eligible-but-not-routed opportunities | Routed requests are counted as successful offload |
| 3 | Qualification Pack V1 | Makes candidate evidence repeatable and portable | The first cohort supplies realistic fixtures and rubric defects | There is still no accepted live output to anchor the pack |
| 4 | Portable release/conformance bundle | Removes source-tree and portfolio assumptions | License decision exists and installed-wheel tests pass | Distribution rights or consumer contract remain ambiguous |
| 5 | Exact accepted-result cache | Avoids demonstrably duplicated work | Repetition is observed and privacy/retention policy is explicit | Identical accepted jobs are rare or review dominates total effort |
| Later | Second hosted provider or local adapter | Adds resilience or lowers measured marginal cost | A qualified workload and adapter conformance pack exist | It is driven only by theoretical price or owned hardware |

The sequence is evidence-driven, not strictly serial engineering. For example,
an offline wheel-install test can be prepared while the cohort runs, but external
release still waits for the license decision.

## Feature comparison

| Candidate | Product layer | Net-benefit outlook | Disposition | Reason |
| --- | --- | --- | --- | --- |
| Versioned context packers and job templates | Core | High | **Finish current work** | The first useful job depends on it; do not create a second template system |
| Qualification packs and repeatable evaluation | Core evidence interface; DERP consumes result | High | **Build next** | Prevents unsuitable routing and makes model changes reviewable |
| Portable wheel, explicit config, installed-package self-test | Core | High | **Build next** | Necessary for consumers without the source tree or repo-cp |
| Adapter/model manifest and conformance suite | Core contract plus adapter tests | High | **Build with portable release** | Contains provider drift without a gateway |
| Exact accepted-result cache | Core storage; DERP policy gates reuse | Potentially high but workload-dependent | **Build conditionally** | Directly removes calls only if exact repetition exists |
| Usage, cost, and human-effort accounting | Core receipt/measurement | Already substantial | **Extend narrowly** | Add missing dimensions discovered by the cohort; avoid telemetry platform scope |
| Safe artifact return and human disposition | Core CLI/artifact handling | High | **Finish current work** | Required before cache or autonomous reuse; semantic acceptance remains human |
| Explicit fallback/escalation recommendation | DERP | Moderate | **Defer** | A recommendation can be useful after multiple candidates qualify; no automatic call |
| Second hosted-provider adapter | Adapter | Moderate | **Defer** | Add only for a qualified candidate, availability need, or measured cost case |
| Local-model adapter | Adapter plus deployment policy | Unknown | **Defer** | Owned hardware is not evidence of quality, throughput, or lower total cost |
| MCP/editor/Codex wrapper | Optional integration | Moderate convenience | **Defer** | Wrap the stable CLI later; do not put policy or credentials in the wrapper |
| LiteLLM gateway | Optional integration | Low initially | **Integrate only at scale** | Useful across many providers, but adds a fast-moving gateway and price-map authority risk |
| Inspect AI runtime dependency | Optional evaluation integration | Mixed | **Export/import, do not require** | Strong eval/logging facilities; too broad for the runtime dependency surface |
| OpenTelemetry GenAI export | Optional integration | Low initially | **Defer** | Conventions are still marked Development and content fields can be sensitive |
| Semantic response cache | Separate experimental system | Unfavorable initially | **Reject** | Similarity adds false-hit, embedding, privacy, and invalidation burdens |
| Learned router/model cascade | Separate research system | Unfavorable now | **Reject for current scope** | Conflicts with explicit deterministic policy and needs much larger labeled evidence |
| Automatic retry/fallback/escalation | DERP/execution | Unfavorable now | **Reject** | Multiplies spend and weakens the one-grant/one-attempt authority model |
| Background daemon, queue, or general agent framework | Deployment/orchestration | Unfavorable | **Reject** | Operating overhead and authority complexity can consume the savings |

## Recommended feature 1: Qualification Pack V1

### User problem and example

A profile can currently carry supplied quality evidence, but an independent
consumer needs a repeatable way to establish that evidence. Example: before
admitting a low-cost hosted model for `change-summary-v1`, run it on frozen
repository-change packets containing status wording, SHAs, path names, failed
checks, and scope constraints. Score literal-field preservation and reference
validity deterministically; have a human score semantic adequacy and material
omissions on a held-out set.

Without this feature, every consumer either trusts an assertion or rebuilds an
ad hoc evaluation. Both produce more review and failed-call waste.

### Expected efficiency benefit and measurement

The expected benefit is fewer unsuitable live attempts, fewer frontier
continuations caused by predictable quality defects, and less repeated manual
model comparison. Measure it with:

- qualification runs reused across later admissions;
- held-out pass/fail by criterion, not one blended score;
- live postflight failure, human rejection, correction, and frontier-continuation
  rates before and after qualification;
- evaluation cost and reviewer time amortized across accepted live jobs; and
- drift failures when a model, adapter, template, or checker changes.

No numerical saving is asserted. A small portfolio may spend more on evaluation
than it saves; record that cost in a separate evaluation cohort.

### Minimal implementation slice

Add two portable JSON contracts and one offline runner:

- `qualification-pack/v1`: workload/job-family identity, immutable cases,
  input and expected-evidence hashes, template/checker versions, deterministic
  criteria, human rubric, disclosure class, and train/development/held-out split;
- `qualification-result/v1`: pack digest, exact candidate/model/adapter identity,
  run configuration, per-case outputs and scores, usage/cost/time, human rubric
  decisions, evidence gaps, and final `QUALIFIED`, `NOT_QUALIFIED`, or `UNKNOWN`;
- `helix-offload qualify-replay`: score supplied recorded outputs without a model
  call. A separately authorized command may generate outputs later through an
  existing adapter, but generation is not part of the first implementation.

Do not add model-graded acceptance. Inspect AI permits generation and scoring to
be separated, which is useful, but helix-offload can keep its initial runner
small and export/import cases and results rather than taking Inspect as a runtime
dependency.

### Inputs, outputs, ownership, and interactions

- **Inputs:** portable pack, exact candidate/profile, recorded outputs, and human
  rubric decisions. Deployment policy supplies thresholds.
- **Outputs:** content-addressed qualification result that Execution Admission V1
  can reference. It grants neither execution nor general competence.
- **Ownership:** helix-offload owns schemas, replay, and result integrity; DERP
  consumes the result; the consumer owns thresholds, candidate approval, source
  disclosure, and final qualification.
- **Dependencies:** existing JSON Schema and canonical hashing; optional Inspect
  conversion at the edge. No repo-cp dependency.

### Portability, verification, burden, and failure modes

The pack must use logical IDs and hashes, never workstation paths. Fixtures must
be distributable or supplied by the consumer. Verification requires schema and
digest checks, split-integrity tests, deterministic replay, tamper cases, scorer
unit tests, an installed-package run, and evidence that human fields cannot be
forged by model output.

Main burdens are corpus maintenance, reviewer calibration, data rights, and model
drift. Main failures are leakage from development into held-out cases, overfitting
one template, incomparable model settings, and treating a narrow qualification as
general capability. **Disposition: BUILD NEXT. Evidence strength: strong for the
need and reuse pattern; actual efficiency benefit remains a cohort hypothesis.**

## Recommended feature 2: Portable release and adapter conformance bundle

### User problem and example

An external consumer should be able to install helix-offload into a clean Python
environment, provide a local policy/profile/job file, run synthetic rehearsal, and
obtain the same schemas and receipts without `/home/louis`, repo-cp, a portfolio
registry, or a source checkout. Today the project uses standard `pyproject.toml`
metadata and installs schema data, but this has not been demonstrated as a clean
external install and no license grant is present.

Providers also change model aliases, parameters, tokenization, pricing, and
retirement dates. OpenAI recommends pinned model versions and evaluations;
Anthropic publishes explicit active/deprecated/retired states; Google distinguishes
stable, preview, latest, and experimental identifiers. A portable consumer needs
these as visible, dated evidence—not hard-coded assumptions inside DERP.

### Expected efficiency benefit and measurement

The feature reduces setup debugging, provider-specific conditionals, and repeated
manual verification. Measure:

- clean-environment install and `doctor` success rate;
- time from install to successful fake workflow;
- adapter conformance failures detected before live calls;
- model-manifest expiry/deprecation findings before invocation;
- number of provider-specific branches outside adapters; and
- support incidents caused by missing schemas, implicit paths, or stale prices.

### Minimal implementation slice

1. Build wheel and source distribution from the existing `pyproject.toml`.
2. In a fresh temporary virtual environment, install the wheel with dependencies
   resolved from an explicit lock/test constraints file; run CLI help, schema
   loading, admission, DERP recommendation, and fake execution outside the source
   tree.
3. Load packaged schemas through `importlib.resources`, with a deliberate source-
   tree fallback only for development.
4. Add `helix-offload doctor --offline` that reports package version, schema
   availability/digests, supported contract versions, adapter plugins explicitly
   installed, and no credential/model availability claims.
5. Add a portable `model-manifest/v1` containing provider, exact model ID or alias
   policy, capabilities, checked-at time, deprecation state, token limits, price
   dimensions, source URLs, and evidence basis. It is caller-supplied and expires
   by policy.
6. Add an adapter conformance suite over recorded request/response fixtures:
   request shape, structured-output translation, one-attempt behavior, deadline,
   response-size bound, sanitized errors, usage mapping, and model identity.

The release may expose a Python adapter protocol or explicit entry-point group,
but should not dynamically discover arbitrary plugins by default. Consumers select
an adapter by explicit configuration.

### Inputs, outputs, ownership, and interactions

- **Inputs:** explicit local configuration, model manifest, candidate evidence,
  and consumer-selected adapter.
- **Outputs:** installed self-test report and adapter conformance result; no live
  request from `doctor`.
- **Ownership:** helix-offload owns packaging, interfaces, schemas, and conformance;
  adapter packages own transport mapping; consumers own credentials, price facts,
  data residency, retention, and allowlists. DERP consumes only validated facts.
- **Dependencies:** PyPA wheel/source-distribution standards, existing JSON Schema,
  and provider-native documentation. No gateway is required.

### Portability, verification, burden, and failure modes

Portability is the feature's purpose. Test Linux and at least one additional
consumer environment only when real users require it; avoid promising every OS.
Verify that artifacts contain schemas and license metadata, have hashes, install
without the Git checkout, and never reference repo-cp or absolute workstation
paths. A release smoke test must use fake fixtures and no network.

Failure modes include alias drift, stale prices, provider response changes,
plugin dependency conflicts, and a self-test that accidentally reads credentials
or calls a network. Model manifests therefore need `retrieved_at`, source URL,
exact/alias distinction, and an expiry outcome of `UNKNOWN`, not silent refresh.

LiteLLM is actively maintained and covers many providers, but it is a fast-moving
gateway with mixed licensing boundaries and a cost map that can fetch updates or
fall back to bundled data. It should remain an optional adapter only after direct
adapters become repetitive. **Disposition: BUILD NEXT, contingent on an owner
license decision. Evidence strength: strong for packaging and provider-drift
needs; cross-platform support demand is unmeasured.**

## Recommended feature 3: Acceptance-gated exact-result reuse

### User problem and example

Bounded jobs often repeat: the same revision range may be summarized twice, the
same document may be classified under the same rules, or a CI rerun may package
identical evidence. Calling the model again wastes tokens, time, and review. A
cache hit must not silently mean “similar enough.”

For example, an accepted `change-summary-v1` artifact can be reused only when the
repository/base/target identities, packed excerpts, validation receipts, template,
checker, policy, candidate/model snapshot, adapter contract, and output format all
match the original cache key.

### Expected efficiency benefit and measurement

Count exact eligible lookups, hits, misses by invalidation dimension, avoided
adapter calls, saved observed tokens/cost/time, and human review time on hits.
Report storage and maintenance time. A cache is justified only when the cohort
shows enough exact repetition that avoided calls and review exceed the operational
burden. Do not infer benefit from cache capacity or theoretical similarity.

### Minimal implementation slice

- Define `reuse-key/v1` as a SHA-256 over a canonical object containing every
  material input and contract identity. The existing project canonicalization may
  be retained if it is explicitly specified and cross-language test vectors pass;
  RFC 8785 is a possible interoperability target but is Informational, not an IETF
  Standards Track specification.
- Store an immutable bundle: accepted artifact, original receipt, human
  disposition, key components, classification/namespace, creation time, and
  optional policy expiry.
- Read only from an explicit cache root. Never scan arbitrary directories.
- Permit a hit only for a human-accepted final disposition and current policy.
  Re-run deterministic postflight before return. Return a new reuse receipt that
  links the original receipt and records `adapter_invoked: false`.
- Support inspect/list/delete by exact key; no eviction daemon, remote cache,
  vector store, or semantic lookup in V1.

### Inputs, outputs, ownership, and interactions

- **Inputs:** normalized job identity, all content hashes, contract/version
  identities, consumer namespace/classification, and reuse policy.
- **Outputs:** hit/miss plus a provenance-linked artifact/receipt; never execution
  authority.
- **Ownership:** core helix-offload owns key and store format; DERP applies explicit
  reuse eligibility and current postflight policy; the consumer owns retention,
  classification, deletion, and acceptance.
- **Dependencies:** hashing, canonical JSON, private filesystem operations. No
  embedding model or database is required.

### Portability, verification, burden, and failure modes

Use a caller-selected directory and logical namespace. No absolute path belongs
in a portable receipt. Test one-bit input/version changes, tampered objects,
cross-namespace refusal, expired policy, unaccepted dispositions, postflight drift,
concurrent exclusive writes, and secret-canary non-disclosure.

The main risks are incomplete keys, stale semantic acceptance, sensitive artifact
retention, and a cache hit being misreported as a newly completed model job.
Semantic-cache projects such as GPTCache add embeddings and approximate matching;
that can improve hit rate but creates a different correctness problem. **Disposition:
BUILD ONLY IF the first cohort demonstrates repeated exact work. Evidence strength:
strong that exact reuse removes a repeated call; weak on expected hit rate in
Louis's or another consumer's workload.**

## Boundary map

```text
consumer-owned policy, authority, credentials, disclosure, retention, thresholds
                                  |
                                  v
core helix-offload -----------------------------------------------+
  portable schemas, packers/templates, qualification packs,       |
  artifact/receipt formats, exact reuse store, CLI/package         |
                                  |                                |
                                  v                                |
DERP governor                                                     |
  preflight -> deterministic candidate/reuse recommendation ->     |
  execution-limit checks -> postflight -> outcome accounting       |
  (no authority grant, credential access, or automatic call)       |
                                  | exact separate grant           |
                                  v                                |
execution adapter                                                  |
  one provider/local call, transport translation, deadline,        |
  byte/token bounds, response/usage normalization                   |
                                  |                                |
                                  v                                |
artifact + receipt -> deterministic checks -> human disposition ---+

optional edges: Inspect import/export, MCP/editor wrapper, OTel export,
LiteLLM adapter, provider-native token counter, llama.cpp/Ollama local endpoint
```

### What does not belong in DERP

- secret storage or account setup;
- provider HTTP implementation details;
- a general prompt, vector, or artifact database;
- an editor UI, MCP host, queue, daemon, or scheduler;
- model acquisition, GPU/runtime management, or deployment;
- portfolio priorities, legal licensing, data-classification policy, or human
  semantic acceptance; and
- learned quality scores, invented prices, or automatic frontier escalation.

DERP may return a specific fallback or frontier-review recommendation once the
relevant alternatives are supplied and qualified. It still should not invoke the
fallback or confer authority.

## Existing-tool reuse decisions

### Use directly

- **JSON Schema Draft 2020-12 and the existing `jsonschema` dependency** for
  portable validation. Do not create a second validator language.
- **Python packaging standards** for wheel/source distributions and static project
  metadata. Add installed-artifact tests before adopting a container or installer.
- **Git fixed read-only commands** for repository identities and diffs in bounded
  packers. Git remains the source of facts; the model receives a packet, not a
  repository shell.
- **Provider-native usage fields and token-count endpoints** where available.
  OpenAI's Responses API reports input/output/total usage, and its token-count
  endpoint accepts the intended request shape. Record whether a value is provider-
  observed, locally estimated, or unknown.

### Integrate narrowly

- **Inspect AI:** exchange qualification datasets, recorded outputs, and results.
  Its MIT-licensed project supplies tasks, scorers, providers, logs, and replayable
  run configuration, and it separates generation from later scoring. Do not import
  its agents, arbitrary task execution, retries, or sandbox semantics into the
  helix-offload runtime. Inspect's own security policy says untrusted tasks/solvers/
  scorers are equivalent to untrusted code and that its local sandbox has no
  isolation; this supports keeping packs declarative.
- **LiteLLM:** consider a separately installed adapter if three or more provider
  integrations make direct maintenance demonstrably expensive. Never let its
  router, fallback, or remotely refreshed cost map replace DERP policy or supplied
  price evidence.
- **MCP:** after the CLI and artifact contracts stabilize, expose a thin optional
  tool server with separate `prepare`, `preview`, `execute-with-grant`, and
  `record-disposition` tools. The MCP specification uses JSON Schema and explicit
  per-request metadata, which fits portable interfaces. It should remain stateless,
  local by default, and subject to host confirmation; no server-side agent loop.
- **llama.cpp or Ollama:** use an adapter later rather than embedding a local
  runtime. llama.cpp provides a maintained MIT-licensed local server and CUDA
  builds; Ollama documents non-stateful Responses API compatibility. Compatibility
  is not qualification: exact request fields, structured output, usage, isolation,
  model license, and RTX 5070 Ti behavior still require local evidence.

### Leave outside

- **Provider billing dashboards and secret managers** remain deployment services.
- **OpenTelemetry GenAI** may receive a privacy-filtered exporter later, but its
  GenAI attributes are currently Development and the specification warns that
  input/output message fields can contain sensitive information. Receipts remain
  the product's authoritative record.
- **GPTCache/semantic vector caching** remains outside the initial trust boundary.
- **A general API gateway or agent framework** is not required for one hosted
  adapter and one local candidate.

## Current provider facts and implications

The following changing facts were retrieved on 2026-10-01 and are examples, not
candidate qualifications or a pricing commitment:

- OpenAI lists GPT-6 Luna for focused, high-volume work at standard pricing of
  $0.10 per million input tokens and $0.50 per million output tokens. Its Responses
  documentation reports usage and states that `max_output_tokens` includes visible
  and reasoning tokens. OpenAI recommends pinned versions and evals for consistent
  behavior. Monthly project/organization hard spend limits exist but enforcement
  is not instantaneous, so they are not a per-job cap.
- Google lists Gemini 2.5 Flash-Lite at $0.10 per million input tokens and $0.40
  per million output tokens on its paid standard tier, and distinguishes stable,
  preview, latest, and experimental model names.
- Anthropic lists Claude Haiku 4.5 at $1 per million input tokens and $5 per
  million output tokens, with separate caching prices. Its lifecycle documentation
  explicitly distinguishes active, legacy, deprecated, and retired models and
  recommends testing replacements before retirement.

These rates are not comparable quality evidence. Different tokenizers, caching,
reasoning tokens, long-context tiers, regions, tools, and billing products can
change total job cost. A model manifest therefore records dimensions and sources;
the receipt records actual observed usage/cost when the provider supplies it.
DERP must not turn a price table into a quality score.

## Standalone consumer scenarios

### 1. Independent open-source maintainer

The maintainer installs a wheel, supplies a local policy and two qualified hosted
profiles, and runs a bounded release/change summary over explicit Git revisions.
No repo-cp registry exists. DERP recommends from supplied evidence; one adapter
call returns a draft and receipt; the maintainer accepts or rejects it. A later
identical CI retry may use an accepted exact-cache entry.

### 2. Small operations team processing documents

The team defines a versioned extraction template and data-classification policy,
qualifies a candidate on its own representative documents, and keeps credentials
in its existing secret manager. helix-offload accepts the portable job and grant,
returns a fixed JSON artifact and receipt, and never stores data unless the team's
explicit artifact/cache policy requests it.

### 3. Air-gapped or offline evaluator

An evaluator installs a prebuilt wheel and runs `doctor --offline`, admission,
packing, and fake-adapter rehearsal. Qualification replay scores previously
recorded outputs without credentials or network. A future local adapter talks to
an explicitly configured loopback runtime only after local isolation and model
quality are demonstrated.

### 4. Editor or coding-agent user

An optional MCP/editor wrapper invokes the same stable CLI contracts. It packages
an explicit selection, previews policy results without a model, obtains a human
grant through the host, and returns artifact paths plus receipts. The integration
does not make the editor a policy authority and cannot silently redirect work.

## Explicit deferrals and rejections

- **Outcome forecasting and calibration:** defer until the explicit hosted path
  has live acceptance and a comparable resolved cohort. The separately preserved
  [future-feature record](2026-10-01-helix-offload-outcome-forecasting.md)
  defines immutable pre-execution forecasts, receipt-based resolution, calibration
  limits, and the authority boundary. It adds no trading mechanics and must not
  let uncalibrated predictions silently control routing.
- **Local RTX 5070 Ti adapter:** defer until the hosted path has an accepted job
  and comparable quality pack. Proceed only with measured quality, tokens/second,
  latency, energy or wall-power basis, memory headroom, maintenance time, runtime
  isolation, and model-license evidence. No hardware purchase is indicated.
- **Second provider:** defer until availability, quality, or measured economics
  justify it. Provider diversity alone is not a benefit if it doubles qualification
  and maintenance.
- **Automatic retry:** reject in the current product. A retry recommendation can
  name the failed condition and required new grant; execution remains one attempt.
- **Automatic frontier fallback:** reject. It spends frontier capacity and changes
  authority/data disclosure. Emit a packet and recommendation only.
- **Semantic cache:** reject until exact caching has measured insufficient hits and
  a labeled false-hit evaluation exists. Similarity thresholds are policy claims,
  not deterministic equivalence.
- **Learned router/cascade:** reject for now. FrugalGPT and RouteLLM-style research
  shows potential for learned cost/quality routing at scale, but it needs labeled
  traffic, nontrivial evaluation, and probabilistic policy that is unnecessary for
  the small explicit-candidate system.
- **MCP first:** defer. A protocol wrapper cannot repair an unusable CLI or missing
  acceptance evidence.
- **Daemon, queue, web review application, central database:** reject until a real
  multi-user/throughput requirement appears.
- **OpenTelemetry as the receipt system:** reject. It is an optional export, not
  an authority or durable acceptance record.
- **Provider prompt caching as result caching:** keep separate. Prompt caching can
  reduce repeated input processing but generates a new response and does not prove
  reuse of an accepted artifact.

## Go/no-go criteria

### Qualification Pack V1

Go when one accepted live job and enough realistic cases exist to freeze a
workload-specific held-out set. No-go when cases are synthetic only, the rubric is
unreviewed, or qualification would be copied across job families.

### Portable release bundle

Go when the owner selects a license, the public API/contract versions are named,
and a wheel can be tested in a clean environment. No-go for external distribution
while legal permission, packaged schemas, or source-tree independence is unknown.

### Exact accepted-result cache

Go when the cohort records exact repeats, accepted artifacts, saved review paths,
and an explicit retention/classification policy. No-go when hit rate is effectively
zero, inputs are sensitive without approved storage, or a complete cache key cannot
be defined.

### Provider/local expansion

Go only when a named workload has qualification evidence and the adapter passes
conformance. No-go on price alone, alias identity, owned GPU alone, or an
OpenAI-compatible label without field-level tests.

## Smallest next implementation packet (review-ready, not authorized here)

Name: `HELIX_OFFLOAD_QUALIFICATION_PACK_V1`

Entry condition: the current CLI/`change-summary-v1` work is complete, one bounded
hosted call has an accepted or rejected human disposition, and its evidence can be
used to refine—not leak into—the held-out design.

Scope:

1. Add `qualification-pack-v1.schema.json` and
   `qualification-result-v1.schema.json`.
2. Add canonical digest/render/validate functions with no network, credential,
   repository discovery, or execution capability.
3. Add `qualify-replay --pack PACK.json --outputs OUTPUTS.json` that applies only
   fixed deterministic scorers and merges separately supplied human rubric results.
4. Include one small `change-summary-v1` fixture pack with development and
   held-out case IDs, including literal SHA/status/path preservation, omitted
   failure, conflicting evidence, scope escape, prompt injection in source text,
   malformed output, and adequate output.
5. Produce a qualification result that binds the exact pack, template, checker,
   candidate, model, adapter, and recorded-output hashes and ends in
   `QUALIFIED`, `NOT_QUALIFIED`, or `UNKNOWN`.
6. Document that the result is workload-specific evidence, not execution authority
   or general model qualification.
7. Optionally document an Inspect conversion shape; do not add Inspect as a runtime
   dependency.

Acceptance:

- schemas pass Draft 2020-12 validation;
- identical inputs replay byte-identically;
- any material identity/digest change invalidates the result;
- model-authored fields cannot set human scores, thresholds, or final authority;
- missing human evidence returns `UNKNOWN`;
- development/held-out overlap is refused;
- synthetic canaries do not appear in errors or summary logs;
- installed-wheel tests find schemas and run replay outside the checkout; and
- all existing admission/DERP tests remain unchanged and passing.

Excluded: live model calls, candidate approval, license selection, cache,
additional provider/local adapter, MCP, telemetry backend, retries, dispatch, and
publication.

## Interpretation limits and unresolved assumptions

- No workload-frequency, duplicate-rate, reviewer-time, or live quality dataset
  was available. Rankings are reasoned recommendations, not measured ROI.
- One accepted live call would establish path viability, not reliability or net
  savings. The first cohort remains necessary.
- The existing 20-job completion threshold is a decision threshold, not statistical
  proof. It cannot establish rare failure rates, broad workload quality, or
  counterfactual frontier tokens by itself.
- Clean packaging has not been built or installed in this research task.
- Provider availability, account entitlement, data terms, and negotiated pricing
  were not inspected.
- RTX 5070 Ti runtime compatibility, throughput, energy, and model fit were not
  tested.
- The appropriate external license is an owner/legal decision.

## Source register

All URLs were retrieved or rechecked on 2026-10-01 unless noted otherwise.

### Standards and packaging

- JSON Canonicalization Scheme, RFC 8785 (Informational):
  https://www.rfc-editor.org/rfc/rfc8785.html
- PyPA `pyproject.toml` specification:
  https://packaging.python.org/en/latest/specifications/pyproject-toml/
- PyPA interoperability specifications, including wheel/source distribution and
  `pylock.toml` references:
  https://packaging.python.org/en/latest/specifications/
- Model Context Protocol 2026-07-28 specification path:
  https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/index.mdx
- MCP project/licensing transition evidence:
  https://github.com/modelcontextprotocol/mcpb/blob/main/LICENSE

### Evaluation and routing research

- Inspect AI documentation: https://inspect.aisi.org.uk/
- Inspect AI log/replay documentation: https://inspect.aisi.org.uk/eval-logs.html
- Inspect AI scoring workflow: https://inspect.aisi.org.uk/scoring-workflow.html
- Inspect AI source and MIT license:
  https://github.com/UKGovernmentBEIS/inspect_ai
- Inspect AI security boundary:
  https://github.com/UKGovernmentBEIS/inspect_ai/blob/main/SECURITY.md
- FrugalGPT original paper: https://arxiv.org/abs/2305.05176
- RouteLLM original paper and reference implementation:
  https://arxiv.org/abs/2406.18665
  https://github.com/lm-sys/RouteLLM

Direct upstream HEAD observed 2026-10-01 for Inspect AI:
`6bea9cd4f6981bf50703284e1595710e8dec6ad4` (`main`).

### Provider APIs, lifecycle, usage, and pricing

- OpenAI API overview, credential handling, pinned versions, and eval guidance:
  https://developers.openai.com/api/reference/overview
- OpenAI Responses API reference:
  https://developers.openai.com/api/reference/cli/resources/responses/methods/create
- OpenAI token counting:
  https://developers.openai.com/api/docs/guides/token-counting
- OpenAI GPT-6 Luna model page:
  https://developers.openai.com/api/docs/models/gpt-6-luna
- OpenAI pricing: https://developers.openai.com/api/docs/pricing
- OpenAI spend limits:
  https://developers.openai.com/api/docs/guides/spend-limits
- OpenAI deprecations:
  https://developers.openai.com/api/docs/deprecations
- Anthropic pricing:
  https://platform.claude.com/docs/en/about-claude/pricing
- Anthropic model deprecations:
  https://docs.anthropic.com/en/docs/about-claude/model-deprecations
- Anthropic token counting:
  https://platform.claude.com/docs/en/api/messages/count_tokens
- Google Gemini model/version naming:
  https://ai.google.dev/gemini-api/docs/models
- Google Gemini API pricing:
  https://ai.google.dev/gemini-api/docs/pricing
- Google token counting:
  https://ai.google.dev/gemini-api/docs/tokens

### Optional integrations and local runtimes

- LiteLLM source: https://github.com/BerriAI/litellm
- LiteLLM license boundary:
  https://github.com/BerriAI/litellm/blob/main/LICENSE
- LiteLLM cost-map behavior:
  https://github.com/BerriAI/litellm-docs/blob/main/docs/proxy/custom_model_cost_map.md
- llama.cpp source and local server:
  https://github.com/ggml-org/llama.cpp
  https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- llama.cpp CUDA build documentation:
  https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md
- Ollama OpenAI compatibility, including non-stateful Responses support:
  https://github.com/ollama/ollama/blob/main/docs/api/openai-compatibility.mdx
- GPTCache source and MIT license: https://github.com/zilliztech/GPTCache
- OpenTelemetry GenAI attribute registry and privacy warning:
  https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/
- OpenTelemetry semantic-convention maturity levels:
  https://opentelemetry.io/docs/specs/semconv/general/semantic-convention-groups/

Direct upstream HEADs observed 2026-10-01:

- LiteLLM `ba8cd1ee3159f94281ffb6e261be7e6a56290a84` (`main`)
- llama.cpp `ec7630a640789c393694fb194f1bbbf0369fc62d` (`master`)
- MCP specification `3098fe94caa1b9e0afaaa6d30e040b61d5802471` (`main`)
- GPTCache `a74ac654473f7bf4109118e8576945161616e17a` (`main`)

## Research action record

Repository writes in this task are limited to this research artifact and its
source manifest in an isolated repo-cp checkout. No feature, contract, work-entry,
registry, implementation, credential, account, runtime, model, GPU, deployment,
or canonical branch was changed. No model workload was executed.
