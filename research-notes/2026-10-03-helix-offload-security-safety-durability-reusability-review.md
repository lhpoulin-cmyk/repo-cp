# helix-offload / DERP security, safety, durability, and reusability review

Research date and evidence cutoff: **2026-10-03**

Status: **research and recommendation only**. No connector, model, API, GPU,
credential, installation, deployment, or runtime mutation was performed.

Exact published revisions reviewed:

- `lhpoulin-cmyk/helix-offload` canonical `main`:
  `f24cdc317c364aa01c72eac162fb1281fcafa2f5`
- `lhpoulin-cmyk/repo-cp` canonical `main`:
  `04aa7360bc2215fb4557da0280ff0c4bca41b818`

Both revisions were verified by direct remote `refs/heads/main` queries on the
research date. The repo-cp baseline advanced during the review to publish the
latest Work Entry 013 handoff; the helix-offload baseline already contained the
corresponding sanitized result. That evidence was reviewed without interacting
with the live attempt or its private authentication state.

External sources were retrieved on 2026-10-03 unless a publication date is
stated. Their URLs and claim uses are recorded in the companion source manifest.
They are research inputs, not proof that a local control is effective.

## Executive assessment

helix-offload has a better foundation than a typical model wrapper. It keeps
recommendation, admission, execution authority, deterministic postflight, and
human acceptance separate. It uses strict JSON parsing at the main contract
boundary, immutable Git object identities for change-summary packing, fixed
hosted endpoints, disabled ambient proxies and redirects, one-attempt adapters,
bounded output capture, explicit UNKNOWN values, and no automatic application of
model text. The repaired Claude stream path now retains a response before strict
interpretation and correctly distinguishes communication from confirmed
inference. The current local path is a one-shot OpenClaw model completion, not a
tool-using agent. These are meaningful protections, not merely prompt promises.

The system is nevertheless not yet a durable one-use execution system or an
externally reusable product. The most important gaps are:

1. **An execution grant is content-bound but replayable.** It has no unique
   nonce, expiry, or atomic consumption record. Two agents with the same grant
   can each make the authorized-looking call.
2. **Connector evidence is not provider-neutral in implementation.** Claude API
   and Claude Code have the repaired connector boundary; OpenAI and OpenClaw do
   not. Their timeout, HTTP/client, malformed-success, and post-send failures can
   be reported as `execution_occurred: false` when inference is actually unknown.
3. **Crash recovery has an intent record, not a state machine.** A crash after
   submission but before capture leaves no durable phase proving what happened.
   Direct children time out, but descendant/provider work may continue.
4. **Published-envelope sanitization is a key-name blacklist.** It does not
   protect secrets or private identifiers embedded in arbitrary strings, URLs,
   errors, or unknown stream events. The evidence parser is also more permissive
   than the main strict JSON parser.
5. **Private recovery evidence is stored under a disposable checkout tree.** Mode
   `0600` is useful access control, but it is not an independent backup and does
   not protect against same-user agents, backup ingestion, accidental later
   publication, or cleanup of the containing checkout.
6. **Several configured limits are detected after spend, not enforced before
   it.** The newest Claude result observed 5,202 input and 5,574 total tokens
   against 4,000/4,600 workflow ceilings; DERP correctly refused the result, but
   the subscription client had already consumed the work. This is truthful
   accounting, not a pre-call cap.
7. **The OpenClaw packet is placed in process arguments.** On Linux the complete
   command line is exposed through `/proc/<pid>/cmdline` subject to host procfs
   policy. The present path should therefore be restricted to non-sensitive
   input until a supported stdin/file-descriptor boundary exists.
8. **External adoption is legally and operationally incomplete.** The private
   repository has no license grant, its version sources disagree, schemas are
   installed as shared data files, and there is no repository CI/release
   evidence, clean installed-wheel test, supported-environment matrix, or
   standalone configuration guide.

The most important proportional response is not a daemon, policy service, new
registry, generalized permission framework, signature hierarchy, or model
firewall. Before additional live work, add one atomic grant-consumption record,
a small crash-state journal, connector-evidence parity for OpenAI and OpenClaw,
and an allowlist-based public evidence derivative. Keep human semantic review and
the current no-tools/no-auto-apply boundary.

### Suitability conclusion

| Use level | Assessment | Conditions |
| --- | --- | --- |
| Bounded personal use | **Conditionally suitable** | One trusted operator; non-sensitive or explicitly approved input; new result directory; exact pinned task; manual review; no automatic application; no replay after uncertain submission. Fix grant consumption before routine live use. |
| Wider internal/shared use | **Not yet suitable** | First add atomic grant consumption, crash recovery, connector parity, enforceable data classification/egress, allowlist publication, process-tree cancellation, private-evidence backup/restore, and a minimal CI/package gate. |
| External reuse | **Not yet suitable** | In addition to internal-use controls, choose a license, align versioning, test wheel/sdist installation outside the source tree, provide standalone setup/configuration and adapter conformance, and establish release/security response practices. |
| General light-coding execution | **Not yet suitable** | The current AST policy and fixed harness are useful, but the verifier is not an OS sandbox. Retain the narrow pure-function scope until isolation is demonstrated. |

One accepted local extraction proves connectivity and one bounded outcome. The
first two local change-summary results required refusal or frontier continuation;
the latest Claude result was complete at transport but refused on usage and
format. None establishes general quality, production qualification, throughput,
or a 20% efficiency reduction.

## Scope and evidence method

This review inspected the published architecture, safety and threat documents;
admission, recommendation, grants, adapters, connector capture, workflow
preparation, assembly, postflight, measurement, and disposition code; JSON
schemas; all repository tests; packaging and release files; and the published
Work Entry 010, 013, 014, and 015 records relevant to the current lifecycle.
Private recovery contents were inventoried only by path, permissions, file names,
and hashes already available to the workspace; credentials and account stores
were not accessed. The freshly verified repo-cp registry keeps Work Entry 014
parked; this review neither resumed it nor treated it as an implemented path.

Evidence classes are kept distinct:

- **Source evidence:** what the reviewed revision actually implements.
- **Synthetic evidence:** 62 repository tests passed locally at the reviewed
  helix-offload revision; fixtures do not establish live boundary behavior.
- **Live evidence:** the accepted local extraction; local change-summary
  refusals/frontier continuation; and the newly published Claude stream result.
- **Human evidence:** explicit human dispositions, which are not inferred from
  postflight or publication.
- **Documentation claims:** informative unless code/tests/live evidence enforce
  them. In particular, some architecture and safety sections still label controls
  as proposed or future while adjacent sections describe the current slice.

The analysis uses NIST AI 600-1 and SSDF only as coverage aids, RFC 8259 for JSON
interoperability, upstream client/runtime documentation for actual interfaces,
Linux/Python documentation for process and durability properties, and PyPA/SLSA
for package/release expectations. No framework label is treated as proof of a
defect.

## Trust model

### Assets

- explicit user authority and the one-attempt budget;
- source confidentiality, classification, and integrity;
- credentials, subscription sessions, and provider/account metadata;
- candidate, model, runtime, executable, adapter, policy, and source identities;
- model output and its relationship to sources;
- raw recovery evidence and sanitized publication artifacts;
- human dispositions and preparation/review-effort records;
- canonical Git history, research branches, packages, CI, and release artifacts;
- local GPU, process, disk, memory, network, and monetary resources.

### Actors and failure classes

| Actor/failure | Realistic concern |
| --- | --- |
| Accidental operator or agent error | Wrong range, reused grant, publication of raw evidence, stale model/profile, mistaken acceptance, or cleanup of the only private copy. |
| Malicious repository/document input | Prompt injection, fabricated authority language, secret-bearing text, active markup, misleading citations, or resource-exhaustion structures. |
| Malicious or defective model output | Unsupported claims, scope escape, invalid syntax, command/tool proposals, deceptive references, or denial-of-service output. |
| Compromised provider/client/runtime/dependency | Hidden retries/fallback, data exfiltration, altered event schemas, wrong model, hook/plugin execution, or falsified usage. |
| Concurrent same-user agent/process | Replay of the same grant, result-path races, reading argv/private files, or swapping paths/executables. |
| Remote/release compromise | Force-pushed/deleted branch, malicious dependency/update, altered package, or unsupported claim attached to the wrong revision. |
| Host administrator/root | Out of the present threat boundary; can read memory/files, alter binaries, and subvert observations. |

### Compact trust-boundary diagram

```text
 Louis / consumer authority
        |
        | supplied policy, classification, source selection, acceptance
        v
 +---------------- trusted deterministic controller ----------------+
 | pack Git objects -> preflight -> recommendation -> admission      |
 | -> preview -> content-bound grant -> result reservation/intent     |
 +-------------------------+-----------------------------------------+
                           | one adapter invocation
                           v
        +--------- execution boundary ---------+
        | OpenClaw CLI -> loopback Ollama/GPU  |
        | Claude Code -> claude.ai subscription|
        | fixed HTTPS API transports           |
        +------------------+--------------------+
                           | untrusted envelope/output
                           v
 +---------------- trusted deterministic controller ----------------+
 | raw private capture -> strict parse -> postflight -> assembly      |
 | -> untrusted artifact + receipt -> separate human disposition      |
 +---------------+----------------------+----------------------------+
                 |                      |
                 v                      v
      private recovery store       sanitized Git evidence
      (not Git/public)             (review/publication boundary)

 Untrusted on entry: repository/document text, model output, provider errors,
 stream events, model/runtime files, client dependencies, and remote metadata.
 Hashes bind bytes; they do not authenticate origin or establish truth.
```

### Boundary enforcement and limits

| Boundary | Current enforcing mechanism | Limit |
| --- | --- | --- |
| Source to packet | Immutable commit resolution; Git object diff; allowlisted changed paths/excerpts; no external diff/textconv; bounded bytes | Data classification and secret/PII review are caller responsibilities; only document excerpts are filtered. |
| Packet to policy | Strict schema, canonical hash, admission/recommendation identity | Hash authenticates content only within the trusted local process; policy provenance is caller-supplied. |
| Policy to execution | Separate admission and execution grant; exact candidate/adapter/mode binding | Grant is deterministic, has no expiry/nonce, and is not atomically consumed. |
| Controller to model | Fixed adapters, one attempt, no tools/fallback, deadlines/output limits | Some client/runtime behavior is observable only after execution; input/total cost limits may not be enforceable pre-call. |
| Model to artifact | Strict parse, source-ID validation, deterministic assembly, postflight | Reference existence is not claim entailment; semantic adequacy remains human. |
| Artifact to effect | `automatic_application: false`; separate human disposition | Outside consumers must honor the contract; no universal enforcement after export. |
| Raw to published evidence | Mode-0600 raw capture plus a redacted derivative and manual scan | Key blacklist misses arbitrary text secrets; private storage/backup policy is incomplete. |

Prompt text that says “repository content is data” is defense in depth. The
enforced protections are the absence of tools, fixed adapter shape, deterministic
policy outside the model, strict parsing, and no automatic application. The
latest Claude output demonstrates the distinction: historical authority text in
the packet changed the model’s response, but did not grant execution or apply an
artifact.

## Important protections already working

1. **Strict primary JSON boundary.** `admission._parse_document` rejects duplicate
   keys, non-finite numbers, invalid UTF-8, excessive bytes, and non-canonical
   integer ranges (`src/helix_offload/admission.py:34-86`). This is stronger than
   Python’s default JSON behavior and matches RFC 8259 interoperability guidance.
2. **Fail-closed schemas.** The public request/admission/workflow schemas usually
   use `additionalProperties: false`, version constants, bounded identifiers,
   and impossible-state checks. Recommendation remains side-effect-free.
3. **Strong Git evidence packing.** `workflow._resolve_revision`, `_changed_paths`,
   and `_git` use immutable commit objects, `--no-renames`, controlled Git config,
   disabled hooks/external diff, safe path syntax, time/byte bounds, and no worktree
   traversal (`workflow.py:622-675`). A later worktree symlink does not change an
   already packed commit object.
4. **Known facts are deterministic.** The compact model response contains only
   summary/risks/review notes with short source IDs. Repository identities,
   changes, validation, authority, and receipt facts are assembled by the host.
5. **Fixed hosted destinations.** OpenAI and Anthropic API transports have fixed
   HTTPS URLs, disabled ambient proxies, and a no-redirect opener
   (`adapters.py:921-1035`). Credentials stay outside serialized workflows and
   are accepted by the CLI through a caller-opened descriptor.
6. **Narrow local execution.** The OpenClaw adapter creates an ephemeral config
   with one exact loopback Ollama model, no fallback, no tools, and one local
   simple-completion call (`adapters.py:681-918`). Upstream OpenClaw documents
   this surface as a lean model run without an agent turn, tools, or MCP.
7. **Claude stream fail-closed behavior.** The adapter uses stdin for source
   data, a temporary working directory, restricted/safe modes, empty tools/MCP,
   no session persistence, one turn, bounded capture before interpretation, and
   exactly one final terminal result. Tool/retry events, ambiguous results, and
   incomplete streams fail closed.
8. **Truthful Claude HTTP accounting.** `connector-outcome/v1` separates
   submission from response and terminal generation. `execution_occurred` is
   `null` for HTTP errors, malformed responses, timeout, or uncertain submission;
   an HTTP response alone is not called inference.
9. **Unknown is not zero.** Missing tokens, cost, review time, model identity, and
   provider-request counts remain null/UNKNOWN. Estimates and observations are
   separate. Failed and unrouted logical opportunities remain visible.
10. **No semantic overclaim in postflight.** Passing structural/reference checks
    yields review required, not semantic acceptance. Human disposition is a
    separate content-bound record; no generated prose is automatically applied.
11. **Coding verification is deliberately narrow.** It rejects imports,
    attributes, dynamic execution, dangerous builtins, unallowlisted paths, and
    model-supplied commands, then uses a fixed harness in disposable storage.
12. **Historical evidence is preserved.** Strict refusals are not silently
    rewritten; offline reprocessing creates a linked record with normalization
    actions. Work Entries distinguish source, synthetic, live, and human evidence.

## Ranked findings

Priority means expected harm reduction relative to implementation and operating
cost for the current bounded product. It is not a generic vulnerability score.

| Rank | Finding and class | Evidence at reviewed revision | Realistic failure | Existing mitigation / residual exposure | Confidence | Priority | Minimal correction and verification | Compatibility / cost |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Grant can be replayed or concurrently consumed** — confirmed defect | `execution-grant/v1` has no grant ID, issue/expiry time, or consumption state; `create_execution_grant` is deterministic; `validate_execution_bundle` only recomputes content (`workflow.py:248-305`, `adapters.py:1143-1157`). | Two agents each validate the same file and invoke once, producing two calls under one authority. | Result-directory reservation stops collision only when both use the same directory. Separate directories both succeed. | High | **Immediate** | Reserve a local consumption record keyed by grant digest with `O_EXCL`/lock, attempt ID, expiry, and `RESERVED -> SUBMISSION_UNCERTAIN/COMPLETE`. Two-process race test: exactly one reaches a fake adapter. | Additive local execution state; keep grant v1 readable. No service or central registry needed for single-host scope. |
| 2 | **OpenAI/OpenClaw failure accounting lacks connector evidence** — confirmed defect | Connector schema enumerates only Anthropic/Claude; OpenAI transport discards HTTP body/status before strict parse; OpenClaw raises failures without connector outcome. DERP defaults adapter failures with no connector outcome to `execution_occurred=False` (`derp.py:334-349`; `adapters.py:748-798,921-966`). | Timeout or malformed 200 after send is labeled no execution, encouraging unsafe resend and undercounting usage. | One attempt/no auto-retry reduces amplification. Claude paths are corrected. | High | **Immediate** | Extend the existing connector boundary to OpenAI Responses and OpenClaw; capture before parse, preserve HTTP status/client return, and map absence of proof to UNKNOWN. Reuse, do not create a second receipt system. | Connector schema version or additive enum update; preserve old receipts. Small adapter/test change. |
| 3 | **Crash state is not durable after intent** — confirmed design gap | Result directory and intent are fsynced before invocation, but no durable `SENT`/capture/complete phase journal exists. Connector writes fsync files but not their directory (`connector_evidence.py:270-283`). | Power loss after provider acceptance leaves only `INTENT_RECORDED_BEFORE_SEND`; later operator cannot tell launch failure from possible spend. | Existing intent and exclusive files prevent a false complete manifest; policy says do not retry uncertainty. | High | **Immediate** | Add append-only/exclusive phase files and directory fsync after each: reserved, crossing-send-boundary, response-captured, terminal-complete. Resolver maps every nonterminal post-intent state conservatively to SUBMISSION_UNCERTAIN. Inject crashes at each write in offline tests. | Local evidence change; no need to mutate historical receipts. A few files per run. |
| 4 | **Public-envelope redaction is a blacklist** — confirmed defect | `_redact` removes values only when an exact lowercased key matches a short list and otherwise recursively publishes arbitrary values/events (`connector_evidence.py:19-29,92-191,292-310`). | A token, email, private path, prompt excerpt, or account identifier in an error string becomes publishable. | Raw files are mode 0600; latest live evidence used an additional hand-built reduced derivative. Manual scans help but are heuristic. | High | **Immediate** | Make the publishable derivative an allowlisted typed summary: counts, hashes, bounded status/reason, selected usage/model fields. Keep arbitrary provider text private. Test canary secrets in keys, values, URLs, nested arrays, stderr, and JSONL events. | Existing private envelopes remain unchanged; publish a new derivative version. Lower review burden than expanding regex redaction. |
| 5 | **Private recovery resides under disposable checkout storage** — confirmed durability risk | Work Entry 013 private evidence exists at `.agent-checkouts/codex/work-entry-013-private-evidence/result/`, mode 0700/0600, outside Git but inside a tree routinely retired. | Checkout cleanup or machine loss destroys the only raw response; backup tooling may also ingest it without classification. | File hashes/manifests and access modes detect/limit some failures. Git contains sanitized derivatives. | High | **Immediate** | Move future private evidence to a dedicated consumer-configured 0700 root outside worktrees, record retention/backup class and manifest hash, and run a restore verification before checkout retirement. Never put raw private material in Git. | Deployment policy, not portable hard-coded path. Existing evidence can be copied only under separate authorized handling. |
| 6 | **Input/total limits on subscription client are post hoc** — confirmed operational limit | Latest Claude result reports 5,202 input / 5,574 total against 4,000 / 4,600 ceilings; DERP refused only after the client completed. Client flags directly bound output/turns, not effective hidden/system input. | A job exceeds intended usage or context budget even though the receipt fails correctly. | Exact post-call accounting and refusal are truthful; output remained under 600. | High | **Immediate policy clarification** | Classify each limit as PRE-CALL ENFORCED, CLIENT-ENFORCED, PROVIDER-ENFORCED, or POST-CALL OBSERVED. For subscription clients, preflight a conservative packet ceiling that reserves measured client overhead; treat hard input/cost caps as unavailable unless the interface documents them. | No new service/schema required initially; receipt/preview documentation and one field can be added only if consumers need machine enforcement. |
| 7 | **OpenClaw sends the complete prompt in argv** — confirmed disclosure risk | `OpenClawLocalAdapter.command` supplies `--prompt`, including schema and packet, as a command argument (`adapters.py:735-746`). Linux exposes the complete command line in `/proc/<pid>/cmdline`; upstream OpenClaw documents `--prompt`, not a stdin equivalent on the reviewed page. | Same-user/concurrent process or process inventory captures private repository excerpts. Large input can also hit argv limits. | Current accepted inputs were synthetic/published evidence; local loopback prevents provider egress. | High | **High for sensitive local work** | Prefer a documented upstream stdin or protected file-descriptor interface when available. Until then, make argv exposure an explicit route capability and reject INTERNAL/RESTRICTED packets on this adapter. Verify `/proc` policy separately; do not claim it as portable protection. | May temporarily limit local workloads; no speculative OpenClaw patch inside helix-offload. |
| 8 | **Evidence JSON parser disagrees with the strict contract parser** — confirmed defect | `_json_or_none` uses default `json.loads`, which accepts duplicate names and non-finite values, while `admission._parse_document` rejects them (`connector_evidence.py:285-289`). | A raw envelope is summarized differently from later strict parsing or cannot be canonically hashed (`allow_nan=False`). | Provider-specific strict parsing still fails the result; raw bytes remain. | High | **High** | Reuse one bounded strict parser with explicit maximum depth/node count for evidence. Treat duplicates/non-finite/depth overflow as unparseable while retaining raw hashes. Differential parser corpus verifies identical decisions. | Internal behavior tightens fail-closed handling; version public derivative if shape changes. |
| 9 | **No JSON depth/node bound or normalization display policy** — confirmed design risk | Primary parser has 1 MiB limit and strict values but no explicit nesting/node count; schema validation and recursive redaction can recurse. Unicode identifiers/text are byte-hashed but rendering has no stated bidi/control-character treatment. | Deep JSON causes recursion/CPU failure; bidi/control text misleads a reviewer without changing the hash. | Size limit bounds total damage; many schemas bound arrays/strings. | Medium-high | **High** | Add depth/node limits and catch recursion in all parsers. Preserve exact bytes/hashes, but escape or visibly label bidi/control characters in human renderings. Fuzz offline with deep/duplicate/non-finite/surrogate/bidi cases. | Parser hardening may reject previously accepted pathological inputs; document as a security tightening. |
| 10 | **Timeout kills the direct client, not necessarily the process tree/provider work** — design risk / missing operational evidence | Adapters use `subprocess.run(..., timeout=...)` without a new process session or process-group cleanup (`adapters.py:454-480,748-784`). Python can kill/wait the direct child; descendants or already accepted provider work are not proven canceled. | Client times out while a helper/remote request continues; resources and billing outlive the local deadline. | Timeout is recorded as uncertain on Claude, and no retry occurs. | Medium-high | **High** | Launch client in a new process session, terminate then kill its process group on deadline, bound the grace period, and always retain inference UNKNOWN. Offline helper-process test proves descendants die. Provider cancellation remains unprovable unless its API exposes it. | Small platform-specific implementation; document Windows behavior separately or initially support POSIX only. |
| 11 | **Executable/model identity is checked but not fully bound or observed** — confirmed design gap | `shutil.which`/`Path.is_file` does not bind executable bytes/version/owner/mode to the grant. OpenClaw verifies Ollama tag digest before execution, then reports the configured expected digest as the result digest (`adapters.py:699-733,849-918`). | Executable or model changes between preview/preflight and exec; receipt overstates an “actual” digest that was only pre-call observed. | Exact model name/digest preflight catches ordinary drift; remote result identity is checked. | High | **High** | Record resolved executable path, version, file digest where meaningful, and model digest observation time/basis; recheck immediately before exec and optionally after. Label digest `PRE_EXECUTION_OBSERVED` unless returned by runtime. | Receipt extension, not stronger authenticity. Signatures deferred for single-user scope. |
| 12 | **Loopback model verification can follow redirects** — confirmed defect with limited impact | OpenClaw base URL must be loopback, but `_verify_model` uses default `urllib.request.urlopen`, whose redirect behavior is not disabled (`adapters.py:705,849-855`). | Compromised local endpoint redirects the tag check to a remote URL, causing unintended metadata egress or false identity input. | No real credential is attached and parsed digest must still match. Invocation itself is configured to the original loopback URL. | High | **Medium** | Use the same no-proxy/no-redirect opener and validate the connected/redirect destination remains numeric loopback. Synthetic redirect test must fail before invocation. | Very small, compatible hardening. |
| 13 | **Subscription client retains a managed-policy hook surface** — design risk / missing evidence | Adapter uses `--restricted`, `--safe-mode`, empty tools/MCP, and temporary cwd. Official docs say restricted mode loads only managed settings plus `--settings`; safe mode disables customizations but managed policy hooks may still apply. Current init checks tools/MCP, not hook execution. | Managed command/HTTP hook runs with user authority or sends session metadata despite adapter tool restrictions. | User/project settings, plugins, skills, commands, MCP, and normal hooks are suppressed. Tools/MCP are observed empty in the published run. | Medium | **Medium** | Record effective setting sources/client version; include hook lifecycle events where supported and reject any unexpected hook execution. Document that managed hooks are outside the adapter’s unilateral control; mark the route unsuitable where this cannot be established. | May expose more diagnostic events privately; public derivative must remain allowlisted. Do not bypass managed policy. |
| 14 | **Repository evidence can still steer model behavior** — confirmed usefulness/safety design risk | The latest Claude result interpreted a historical packet authority value, `NOT_AUTHORIZED_FRESH_ONE_INVOCATION_GRANT_REQUIRED`, as a current instruction and declined the requested JSON. | Malicious or stale source text changes answer framing, omits work, or requests unsafe action. Current no-tools boundary prevents direct effects. | Deterministic authority remains outside the model; output was refused and not applied. | High | **Medium** | Clearly delimit evidence; label authority/source fields as quoted historical facts that cannot change the current task; avoid valid source IDs in prompt examples; add held-out injection cases. Keep mechanical tool denial as the real control. | Prompt/template change requires workload requalification, not a new permission framework. |
| 15 | **Citation validation proves identity, not support or coverage** — known residual risk | Compact output rejects unknown source IDs, but postflight does not test whether cited sources support the claim or whether material changes were omitted. Docs correctly require human review. | A complete, fully cited summary is materially misleading. | Human disposition separate; artifact remains untrusted; exact source registry enables review. | High | **Medium** | Add workload-specific held-out cases with claim-to-source and material-omission rubrics. For current scale, human review is preferable to a second model judge. Visually separate generated analysis from deterministic facts. | Review cost remains; do not misrepresent schema checks as semantic proof. |
| 16 | **Prompt example can contaminate citations** — design defect | A concrete valid source ID in an output example can be copied and pass existence when `S01` is present. | Model cites the example ID by habit rather than evidence. | Source-ID existence and human review still catch some cases. | Medium-high | **Medium-low** | Use a sentinel outside the valid namespace, such as `SOURCE_ID`, or avoid concrete IDs in examples. Test that the prompt contains no valid packet source token unless required. | Tiny template change; re-run synthetic prompt/assembly tests. |
| 17 | **Receipt v4 schema is shallow for shared fields** — confirmed interoperability gap | Many v4 members are only typed as `object`; the Python renderer separately projects into v3 and validates recommendation semantics. An external JSON-Schema-only consumer misses those constraints. | External consumer accepts a malformed-but-schema-valid receipt. | First-party renderer applies extra checks; v1-v3 remain strict. | High | **Medium** | Make the next receipt schema self-contained using shared `$defs`/references, or publish the semantic validator requirement as normative with conformance vectors. Preserve v4 history. | Schema maintenance work; do not rush a v5 unless external consumers exist. |
| 18 | **Result path handling is exclusive but not descriptor-relative** — design risk | Files use `O_EXCL` and private modes, but parent directories can be symlinked/swapped by the same UID; writes do not use `openat`/`O_NOFOLLOW` anchored to a verified root. | Concurrent same-user process redirects evidence to an unintended location. | New result directory, no overwrite, safe file names, and parent fsync reduce accidental damage. | Medium | **Medium for shared hosts** | Require an owned private output root and use descriptor-relative opens with no-follow semantics where supported. Verify ownership/mode before reserving. | Platform-specific; defer full hardening for single-user non-adversarial hosts. |
| 19 | **Reprocessing does not bind the new policy/tool revision strongly enough** — design gap | Recovery preserves original hashes and normalization actions, but the record does not consistently identify the exact code/policy revision performing reprocessing. | Same original evidence is normalized differently after upgrade without an obvious comparator. | Original bytes/receipt are immutable and linked; actions are listed. | Medium-high | **Medium** | Record reprocessor package/source revision, postflight policy/schema digest, and original/new timestamps in every recovery result. Golden replay proves old artifact remains untouched. | Additive recovery metadata; do not rewrite prior records. |
| 20 | **Measurement is conservative but not independently assembled** — design risk | Cohort inputs carry receipt/disposition hashes and caller-supplied numeric fields; the aggregator does not open and cross-check the source artifacts. One missing value makes an aggregate null, hiding known subtotal coverage. | Optimistic caller values or missing records distort decisions; useful known totals disappear. | Unknown is never zero; failed/unrouted jobs stay in denominator; counterfactual estimates are separate. | High | **Medium-low** | Add an optional offline cohort assembler that reads artifacts, verifies hashes, and emits known subtotal plus observed-count/coverage. Keep manually supplied imports supported and labeled. | No telemetry service; modest CLI addition after lifecycle hardening. |
| 21 | **Package/release/export is incomplete** — confirmed product gap | No LICENSE; repository is private; `VERSION` is `0.4.0-draft` while `pyproject.toml` is `0.4.0.dev1`; no checked-in CI workflow, lock/constraints, supported environment matrix, clean wheel/sdist install test, or release provenance. Schemas use `data-files`. | External user cannot determine rights, install reproducibly, locate schemas reliably, or know what passed for a release. | Source layout, console script, bounded dependency range, README, changelog, and portable JSON interfaces exist. | High | **High before export** | Owner chooses license; single-source version; package schemas as resources; build wheel/sdist in a clean environment; install and run offline conformance; minimal CI and tagged release notes. Defer SBOM/signing until release need is real. | License is owner/legal choice. CI/package work is bounded; no runtime service. |
| 22 | **Implemented/proposed documentation is internally uneven** — confirmed documentation gap | `ARCHITECTURE.md` opens as proposed/unselected, then describes the implemented governor; `SAFETY.md` calls controls future while current docs claim subsets implemented. README is more current. | External adopter overestimates or underestimates enforced behavior. | Work-entry evidence and current contracts provide detail. | High | **Medium-low** | Add one current capability matrix: implemented/tested/live-accepted/deferred, with revision. Keep historical design but label sections consistently. | Documentation only; avoid duplicating contracts. |

## Requirement-to-control matrix

| Requirement | Implemented control | Verification evidence | Gap / residual risk |
| --- | --- | --- | --- |
| Exact source identity | Commit resolution, packet/source hashes, canonical serialization | Git packer tests and published packet identities | Hash is not origin authentication; private repos/providers need trusted pins. |
| No arbitrary source discovery | Explicit repo/range/path request; allowlisted document excerpts | `prepare_collects_only_bounded_allowlisted_git_evidence` | No small provider-egress classification gate; caller can select secret-bearing committed text. |
| Traversal/symlink resistance | Git object reads, safe path syntax, no worktree file open for excerpts | Type/path negative tests | Result/output roots remain susceptible to same-UID parent-path races. |
| Prompt injection containment | Deterministic policy; no tools; no auto-apply; untrusted-output labeling | Current code and live refusal | Latest Claude output shows evidence can still steer content; semantic resilience unqualified. |
| Credential isolation | Fixed endpoints; descriptor delivery; credentials absent from workflow/receipts; sanitized repr | Synthetic request/repr tests | Subscription session and managed client policy remain ambient; arbitrary errors can leak secrets into private/public derivatives. |
| Destination control | Fixed API endpoints; no redirects/proxies; OpenClaw loopback requirement | Transport tests | Local tag verification uses redirect-capable `urlopen`. |
| One authorized attempt | Grant says max_attempts 1; adapters have no retry loop; retry events fail closed | Tests and live records | Same grant replay/concurrent consumption is not prevented; client/provider hidden requests may remain unknown. |
| Pre-call resource bounds | Packet bytes, deadline, output max, estimated cost gate | Workflow/adapter tests | Subscription input/total/cost caps are post-call observations; latest live attempt exceeded them. |
| Timeout cleanup | Subprocess timeout; HTTP timeouts; uncertain state on Claude | Timeout fixtures | Descendant/provider cancellation not proven; OpenAI/OpenClaw accounting weak. |
| Response preservation | Claude raw stream before parse; OpenClaw stdout before strict parse | Work Entry 013 published live evidence | OpenAI lacks capture; connector file directory fsync absent; public derivative unsafe by default. |
| Strict generated syntax | Duplicate/nonfinite rejection in main parser; schema and content bounds | Negative fixtures | Evidence parser disagreement; no explicit depth/node limit. |
| Source reference validity | Short IDs resolved against deterministic registry; unknown IDs rejected | Workflow tests | Existence is not entailment or coverage. |
| Human authority | Separate disposition; acceptance requires matching artifact and receipt | Disposition tests and live records | External consumer can ignore labels; no auto-application is the essential current boundary. |
| Evidence durability | O_EXCL, file fsync, some directory fsync, hash manifests, Git publication | Code inspection and evidence manifests | No complete phase journal, no dedicated private store/independent backup/restore proof. |
| Private/public separation | Mode-0600 raw evidence; sanitized publication sets | Work Entry 013 practice | Blacklist sanitizer and checkout-local private evidence; same-user/backup risks remain. |
| Schema compatibility | Version constants, old receipt versions retained, explicit change-summary v2 | Schema/test corpus | v4 shallow; migration/support policy not published for external consumers. |
| Portable deployment | Consumer-supplied profiles/policy/URLs/model IDs; no runtime repo-cp import | Source inspection | Examples/evidence Helix-heavy; license/install/release/conformance incomplete. |
| Supply-chain integrity | Narrow Python dependency, recorded executable/model identities in evidence | Source/evidence review | No reproducible environment, dependency review cadence, CI, package provenance, or executable digest binding. |
| Trustworthy measurement | UNKNOWN/null, observed/estimated split, logical jobs, failures/unrouted retained | Measurement tests | Caller-supplied cohort values not cross-checked; no established comparable cohort; 20-job gate is not statistical proof. |

## Data handling and provider-egress policy

A small enforceable policy is missing. Use four classes supplied by the consumer,
not a Helix-specific registry:

| Class | Provider rule | Storage/publication rule |
| --- | --- | --- |
| `PUBLIC` | Eligible for any admitted adapter after exact packet preview | Raw still private by default; sanitized facts may be published after review. |
| `INTERNAL_APPROVED` | Local adapter by default; hosted only with explicit exact-content, destination, and retention approval | Private evidence only; publish hashes/typed status unless separately reviewed. |
| `RESTRICTED` | Refuse hosted. Local only if input is not exposed through argv and the runtime/evidence boundary is approved | Encrypted/controlled private retention; no Git. |
| `SECRET_CREDENTIAL` | Never model input; refuse all routes | Never packet, prompt, fixture, receipt, error derivative, or Git. Use only approved runtime injection. |

The output inherits the highest source class. Raw connector evidence inherits the
input class. The current OpenClaw argv boundary is suitable only for `PUBLIC`
until a supported protected input channel exists. A deterministic preflight gate
can enforce this enum and adapter capability; it does not require content scanning
to pretend it can discover all secrets. Secret scanning remains a heuristic
warning, not authorization.

## Authority and execution lifecycle

The intended chain is sound:

```text
caller instruction
 -> prepared immutable packet and supplied policy
 -> deterministic recommendation (authority NONE)
 -> matching admission evidence (suitability, not authority)
 -> preview (authority NONE)
 -> explicit content-bound execution grant
 -> one adapter attempt
 -> connector outcome and receipt
 -> deterministic postflight
 -> untrusted artifact
 -> separate human disposition
 -> separately authorized apply/publication, if any
```

The missing property is **consumption**, not content binding. The grant binds the
workflow, preview, limits, candidate, adapter, mode, and authority reference. It
does not say “this instance has been used” in a way two processes share. For the
present single-machine/single-operator product, a private filesystem ledger is
enough. Cryptographic signatures are not proportionate: they would authenticate
an issuer but still would not prevent replay. Signatures become relevant only if
grant issuers and executors cross mutually distrustful systems.

Tool proposals should remain inert data. If a future roadmap actually adds tools,
each tool needs a host-owned allowlist, strict argument schema, resource identity,
least-privilege process credential, and a separate human or deterministic grant.
Model text must never become authority merely because it matches a tool schema.
No generalized permission framework is justified while the current roadmap is
inference-only.

## Validation and semantic safety

The current design correctly separates these stages:

1. transport/envelope received;
2. generated syntax valid;
3. source IDs valid;
4. source supports each claim;
5. requested task sufficiently covered;
6. human accepts the artifact;
7. separate authority allows application/publication.

Stages 1–3 are mostly deterministic. Stages 4–5 are not solved by schema checks.
The latest Claude result is instructive: transport completed, token accounting
was observed, but the workflow limit failed; independently, the terminal prose
was not the required JSON and confused historical evidence with current
authority. It therefore produced no artifact and no postflight success despite
a completed generation.

For current workloads:

- **Field extraction:** deterministic exact-field and preservation checks can be
  decisive when the complete source and rules are explicit; human review can be
  sampled after qualification.
- **Rule classification:** label membership and quoted evidence can be checked,
  but entailment against the supplied rule still needs held-out evaluation and
  human handling for ambiguity.
- **Change summary:** structure, source-ID validity, literal status/SHA/path
  preservation, and bounded length are deterministic. Claim support, material
  omissions, risk judgment, and misleading emphasis require human acceptance.
- **Light coding:** syntax, exact path/diff bounds, fixed tests, and AST policy
  are deterministic; security, maintainability, architectural fit, and general
  semantics are not. Current execution isolation is insufficient for broad code.

Normalization must remain auditable. Original bytes and original receipt stay
immutable; a later parser/postflight result must name its own code/policy digest
and list every change. No silent repair, truncation, reference invention, or
promotion from refusal is acceptable.

## Durability and recovery

### Current durability layers

- New result directories and files use exclusive creation; workflow writes fsync
  files and containing directories.
- Intent is recorded before adapter invocation.
- Raw connector bytes and JSON envelopes are captured before provider-specific
  parsing on the repaired Claude paths.
- Manifests contain hashes and only a final complete manifest represents a
  completed result.
- Sanitized evidence is published to Git while raw evidence remains local.
- Historical strict results are not overwritten by offline reprocessing.

### Survival analysis

| Event | Current outcome | Needed minimum |
| --- | --- | --- |
| Process crash before send | Reserved directory/intent may remain; not complete | Recovery resolver classifies NOT_SENT only when launch failure is positively known. |
| Crash just after submission | Intent only; submission ambiguous | Durable phase journal; classify SUBMISSION_UNCERTAIN and prohibit retry. |
| Disk full during capture | Write/fsync raises; partial new file may exist; no final manifest | Directory fsync, explicit capture-failed state where possible, restore raw from provider only if independently available; never report complete. |
| Capture overflow | Bounded prefix and overflow flag on connector paths | Public derivative must not contain arbitrary prefix text; preserve full absence explicitly. |
| Network interruption | Claude marks uncertain; other adapters inconsistent | Connector parity and no-retry recovery rule. |
| Machine loss | Git evidence survives; private raw may not | Independent classified backup for private evidence plus tested restore, or explicit policy that raw is intentionally ephemeral after disposition. |
| Checkout retirement | Published evidence survives; checkout-local private data may not | Dedicated evidence root and cleanup preflight that verifies manifest/backup. |
| Branch deletion/force-push | Local/other clones may retain objects, but remote branch is not backup | Canonical Git plus independent backup/archival policy for durable public evidence. |
| Schema/software upgrade | Old schemas remain; reprocessing can be linked | Published support/migration policy and golden corpus across supported versions. |
| Sensitive Git publication | Git immutability conflicts with erasure | Never publish raw/private content; if leakage occurs, treat confidentiality and credential response as a separately authorized incident, including history rewrite when necessary. |

### Minimal retention policy

Retain verbatim, privately and for a stated period:

- exact grant, attempt intent/phases, raw connector bytes, original output, and
  terminal connector outcome needed to resolve a disputed attempt;
- original and normalized artifacts separately;
- human disposition and review/preparation effort when observed.

Retain reproducibly and safely publish when classification permits:

- workflow/packet hashes and source revision registry;
- policy, admission, grant, adapter/client/model/runtime and code revisions;
- deterministic transforms, validation results, receipt, manifest, and public
  typed connector derivative.

Never put in Git:

- API keys, OAuth/session tokens, cookies, client auth stores, browser state;
- unsanitized provider/client streams or private prompts/source excerpts;
- raw stderr/debug logs or account/rate-limit details;
- consumer-private host paths or identifiers not needed for public review.

Store private evidence under a consumer-configured 0700 root outside disposable
checkouts. Record whether it is independently backed up, encrypted at rest, and
scheduled for deletion. Verify manifest hashes before cleanup and perform a
periodic or pre-retirement restore drill. Remote Git publication is neither an
independent backup nor proof of recoverability.

## Reusability and standalone adoption

### Minimum usable standalone product

A consumer without repo-cp should be able to:

1. install a versioned wheel in a clean supported Python environment;
2. run `helix-offload doctor` or an offline conformance command without network;
3. supply portable JSON policy, candidate/profile, admission, workflow, and
   authority references;
4. prepare/preview a synthetic job and execute the fake adapter;
5. configure one adapter using explicit consumer-owned paths/endpoints and a
   documented credential injection boundary;
6. receive a private result directory, untrusted artifact, receipt, and human
   disposition template;
7. validate/replay the evidence later using the exact package/schema version;
8. do all of this without Helix hostnames, repo-cp registries, Louis-specific
   paths, or hidden manual setup.

The runtime code is mostly portable today: repo-cp is not imported, and models,
URLs, candidates, and policy arrive through inputs. The accidental coupling is
in operations and evidence: Helix-specific examples dominate, private evidence
uses checkout paths, release/install support is absent, and several contracts are
easier to understand through portfolio work records than standalone docs.

### Portability checklist

- [ ] Owner-selected LICENSE and matching `pyproject.toml` license metadata.
- [ ] One authoritative version source; tagged changelog and supported-schema
      table.
- [ ] Schemas packaged as importable package resources, not only shared
      environment `data-files`.
- [ ] Clean sdist/wheel build and install in a new environment; CLI/schema lookup
      works outside the source tree.
- [ ] Supported Python/OS matrix; POSIX-only process guarantees labeled where
      applicable.
- [ ] Dependency constraints/lock for development and release tests; documented
      vulnerability update/response cadence.
- [ ] Minimal CI runs strict tests, schema metaschema validation, package build,
      installed-package smoke, diff checks, and secret-canary publication tests.
- [ ] Adapter capability/conformance document: submission unit, retry visibility,
      tool boundary, input channel, endpoint, redirects/proxies, capture, token/
      cost observability, and enforceable vs post hoc limits.
- [ ] Consumer-configured private/public evidence roots and retention policy.
- [ ] Standalone tutorial using only synthetic fixtures, then an exact separately
      authorized live packet.
- [ ] Error taxonomy and exit codes stable enough for wrappers; unknown fields and
      schema migration policy documented.
- [ ] Release artifact hashes/provenance and rollback instructions. SLSA-style
      provenance/signing can wait until actual external release distribution.

### Premature abstractions to avoid

Do not add a daemon, queue, multi-tenant authorization service, general agent
framework, semantic cache, provider gateway, MCP control plane, automated retry
cascade, or signature PKI to solve the current gaps. The existing CLI plus files
is adequate once consumption and recovery are correct. Add an adapter registry
only when an external adapter needs a stable plugin boundary; until then explicit
classes and conformance fixtures are simpler and safer.

## Operational reliability and the 20% goal

The current accounting semantics are directionally correct:

- accepted work without frontier preparation or continuation is distinct from a
  routed job;
- actual usage/cost is distinct from estimates and subscription allowance;
- local compute is not called free;
- failures, pending outcomes, and unrouted eligible opportunities remain visible;
- review and preparation effort can remain UNKNOWN rather than zero.

The 20% target should be defined primarily as:

```text
accepted comparable eligible jobs completed without frontier preparation or
continuation / all comparable eligible opportunities
```

Report separately:

- observed frontier tokens displaced on matched comparable jobs;
- hosted cash charges and subscription allowance effects;
- local energy estimate with method, not as an observed API cost;
- end-to-end elapsed time, including queue/preparation/review;
- human preparation and review minutes;
- refusal, rejection, retry, frontier-continuation, and material-defect rates;
- model/runtime/client/version, quantization, context, and cold/warm state.

Twenty jobs are an operational decision gate, not statistical proof. A useful
low-overhead design is a prospective cohort with a fixed workload definition and
eligibility rule. Record every opportunity before routing, use the same acceptance
rubric, and reserve a small held-out subset rather than repeatedly tuning on the
same examples. When no matched frontier baseline exists, label displacement as
estimated and show its method/range; do not combine task percentage, tokens,
money, time, and review effort into one “20% saved” figure.

Overhead can erase the gain when packet preparation and human review approach the
frontier baseline, when small models repeatedly fail and trigger frontier
continuation, when subscription usage has no marginal cash reduction, or when
maintenance/requalification dominates a small job volume. The latest Claude run
is an example of offload effort that produced no accepted artifact and consumed
5,574 reported tokens plus preparation/review time. It belongs in the denominator.

Concurrency should remain one per grant and initially one per local runtime. Add
a queue only if measurement shows actual contention. Preallocate bounded disk
capture, reject oversize before full parse, and label provider cost/input caps as
post hoc unless the provider/client enforces them. Observing a limit violation
after the call is valuable accounting, not resource prevention.

## Development and release assessment

### What is working

- Isolated review branches, explicit publication authority, direct remote
  verification, full diff review, and historical evidence preservation are
  consistently documented and visible in Work Entries.
- The test suite exercises malformed inputs, impossible states, connector HTTP
  errors, stream ambiguity, tool/retry events, timeouts, usage limits, exact grant
  binding, Git evidence bounds, assembly, recovery, disposition, and measurement.
- The 62-test suite passed at `f24cdc3...` during this review without a model or
  network call.
- Live failures have led to contract repairs rather than retroactive acceptance.

### Missing enforcement/evidence

- The repository itself contains no CI workflow or evidence that canonical main
  is protected by required checks. GitHub branch protection can require reviews
  and status checks, but repository procedure alone is not remote enforcement.
- There is no release build/install gate, dependency lock/constraints, package
  provenance, or documented rollback from a released distribution.
- Secret-indicator scans are useful heuristics but do not exercise arbitrary text
  leakage through the actual sanitizer.
- Many fixtures mirror implementation happy paths. One two-process grant race,
  one crash-injection recovery suite, one sanitizer canary suite, and one clean
  installed-package test would provide more risk reduction than additional
  schema-only assertions.
- Public evidence claims can become stale immediately when canonical main moves;
  every report should name the exact reviewed revision and avoid “current” without
  a retrieval timestamp.

## Required failure scenarios

| Scenario | Current behavior and evidence | Expected behavior | Residual risk and smallest improvement |
| --- | --- | --- | --- |
| Two agents use the same grant | Both can validate and invoke if they choose separate result directories; no shared consumption state. | Exactly one process atomically reserves the grant; loser stops before adapter construction. | Same-host filesystem ledger and two-process race test. Distributed use later needs a shared store, not now. |
| Crash immediately after submission | Intent exists, but no durable phase identifies the crossing; directory has no complete manifest. | Recovery classifies possible submission as `SUBMISSION_UNCERTAIN`, preserves evidence, and refuses resend. | Phase journal with directory fsync; provider work may remain unknowable. |
| Provider HTTP error after accepting request | Anthropic records response/provider error and inference UNKNOWN. OpenAI lacks equivalent connector outcome. | Preserve HTTP status/body hash, communication, and UNKNOWN inference; never infer no execution. | Apply connector parity; providers may not reveal whether inference started. |
| CLI diagnostic resembles final answer | Claude requires one final terminal result and does not concatenate diagnostics; OpenClaw parses a strict envelope. | Only documented terminal channel can become model output; stderr/intermediate events remain evidence. | Retain strict parser and conformance fixtures for client upgrades. |
| Secret in arbitrary error reaches sanitizer | Current key-name blacklist can publish it unchanged. | Raw stays private; public record includes allowlisted typed facts/hashes only. | Canary tests across arbitrary values, URLs, arrays, stderr, and events. |
| Source changes or becomes symlink after preparation | Current change-summary packet uses resolved Git commit objects, so worktree mutation does not change packed bytes. | Continue using immutable objects and packet hash; future worktree packers must use descriptor-safe reads and reject symlinks. | No change needed for current Git packer beyond tests documenting this strength. |
| Complete, cited answer is materially misleading | Syntax/reference checks may pass; human review remains required. | Artifact clearly separates generated claims from facts; reviewer checks entailment and omissions before acceptance. | Held-out semantic rubric; do not add model-as-judge by default. |
| Response normalized under newer policy | Original receipt/output is preserved and linked; new policy/tool identity is incomplete. | New result names exact original and new code/schema/policy digests and all normalization actions. | Add recovery provenance; no rewrite of old records. |
| Private recovery only in checkout slated for removal | Confirmed for Work Entry 013 private result tree. Cleanup can destroy the sole raw copy. | Cleanup gate proves copy/backup and verifies hashes in dedicated evidence root. | Retention/restore policy; mode 0600 alone is insufficient. |
| Provider/client update changes event order/schema | Strict Claude parser fails closed, which protects authority but may lose output. Executable version is reported in evidence, not grant-bound. | Pinned/tested client identity and frozen conformance streams; unknown event/order fails closed. | Bind version/hash and require offline conformance before upgrade; no live diagnostic call needed. |
| Malicious repository instruction asks for tool/credentials | It can influence prose, as latest live evidence shows, but current adapters expose no model tools and output cannot grant authority or auto-apply. | Treat source as quoted data; retain mechanical tool denial and separate application authority. | Improve delimiters/held-out injection tests; no new permission framework while tool-free. |
| External user installs without repo-cp/Helix | Code is consumer-input driven, but no license, tested distribution, CI, standalone setup, or durable evidence defaults exist. | Clean install, fake lifecycle, explicit config, private/public roots, and conformance work without Helix. | Complete portability checklist before calling the toolkit externally reusable. |

## Minimal hardening plan

### Immediate fixes before routine live execution

1. **Atomic one-use grant consumption.** A private execution-state directory,
   keyed by grant SHA-256, atomically reserves one attempt and records terminal or
   uncertain state. Add expiry/freshness in the reservation metadata rather than
   redesigning all policy contracts.
2. **Provider-neutral connector evidence.** Route OpenAI and OpenClaw through the
   existing capture/outcome abstraction; use UNKNOWN on any post-send failure that
   lacks proof of terminal inference.
3. **Crash-safe phase recording.** Fsync evidence directories; distinguish intent,
   send-boundary, response capture, and completion. Provide an offline resolver.
4. **Allowlist public derivatives.** Stop publishing recursively redacted raw
   event trees. Retain raw privately; publish typed facts, hashes, counts, and
   explicitly reviewed generated text only.
5. **Classify enforceability.** Mark each byte/token/time/cost limit as pre-call,
   client, provider, or post-call. Do not call observed-after-completion ceilings
   preventive controls.
6. **Small prompt correction.** Make historical authority/source fields explicitly
   quoted data and remove valid source IDs from examples. This improves usefulness
   but does not replace mechanical boundaries.

### Next bounded work slice

Implement and test an **execution integrity and recovery slice** containing only:

- filesystem-backed one-use grant reservation/consumption;
- durable phase files and recovery classification;
- OpenAI/OpenClaw connector-outcome parity;
- directory fsync and process-group timeout cleanup; and
- offline race, crash, timeout, malformed/HTTP, and secret-canary tests.

Do not add a service, daemon, queue, database, automatic retry, or new execution
provider. Preserve existing receipts and consume the new state only in live CLI
commands. The first engineering action inside that slice should be the one-use
grant reservation and its two-process race test, because it closes a direct
authority violation before any further call.

### After lifecycle integrity, before wider/internal use

- data-classification/egress gate and OpenClaw argv limitation;
- strict evidence parser with depth/node bounds;
- executable/model observation-basis binding and no-redirect loopback preflight;
- dedicated private evidence root, retention manifest, backup status, and restore
  test;
- clean installed-package test, minimal CI, current-capability matrix;
- owner license decision and aligned versioning before external distribution.

### Deferred until evidence justifies them

- cryptographic grant signatures or remote attestation;
- multi-host consumption service/database;
- SBOM/signing/hosted artifact attestations before an external release exists;
- semantic model judges, learned routing, automatic retry/fallback, tool execution;
- generalized OS sandbox portability beyond the next actual coding use case;
- queueing, daemon, cache, MCP integration, provider gateway, or telemetry service.

### Retain, simplify, or remove

- **Retain:** strict parser, content hashes, fixed endpoints/no redirects, no tools,
  one attempt, immutable original evidence, human disposition, UNKNOWN semantics,
  Git object packing, deterministic assembly.
- **Simplify:** public evidence to an allowlist summary rather than an ever-growing
  redactor; capability matrix rather than duplicated status prose; one connector
  outcome abstraction rather than provider-specific accounting.
- **Remove/avoid:** valid source IDs from examples; claims that a post-call usage
  check enforced a pre-call cap; claims that mode 0600 equals durable/confidential
  preservation; `actual_model_digest` when only expected/preflight digest is known.

## Proposed offline qualification and recovery-test packet

Name: `execution-integrity-recovery-offline-v1` (proposal only; no schema or
implementation was created by this research).

### Frozen inputs

- synthetic workflows/grants for Fake, OpenAI, Anthropic, Claude Code, and
  OpenClaw adapters;
- connector fixtures for launch failure, timeout, disconnect, HTTP 401/429/500,
  malformed 200, oversized payload, incomplete/ambiguous JSONL, changed event
  order, tool/retry/hook events, and redirect;
- JSON corpus with duplicate keys, NaN/Infinity, extreme nesting/node count,
  oversized integers, invalid UTF-8/surrogates, Unicode bidi/control text, and
  unknown fields;
- Git repository fixture with type changes, symlink target, untracked replacement,
  changed worktree after packet creation, and immutable base/target commits;
- sanitizer canaries placed in key names, arbitrary string values, nested arrays,
  URLs, stdout, stderr, provider errors, and intermediate stream events;
- process helper that spawns a descendant and survives unless the process group is
  terminated;
- held-out change summaries with valid-but-unsupported citations, material
  omissions, conflicting evidence, and historical authority prompt injection;
- clean wheel/sdist installation fixture outside the checkout.

### Offline actions

1. Start two local processes against the same grant reservation; assert exactly
   one reaches a FakeAdapter counter.
2. Inject process termination or write failure after reservation, intent, send
   boundary, raw capture, connector outcome, receipt, and manifest.
3. Run the recovery resolver on every partial directory. No incomplete state may
   become success or authorize retry; all retained hashes must verify.
4. Simulate process timeout and prove the direct child and descendant terminate.
5. Feed frozen HTTP/client envelopes through capture and parsing without network;
   validate submission, response, inference, and parse states independently.
6. Produce a public derivative from every secret-canary fixture; assert no canary
   or arbitrary raw text appears while typed facts/hashes remain sufficient.
7. Differentially parse the JSON corpus through every public/evidence boundary;
   decisions must agree and fail without recursion crash.
8. Pack Git evidence, mutate the worktree/symlink/untracked files, and prove the
   prepared packet remains bound to commit objects.
9. Run structural/reference postflight on semantic-negative cases; verify they
   remain review-required or refused and are never labeled semantically accepted.
10. Build/install the distribution in a clean offline environment with supplied
    wheels/cache; run fake lifecycle and locate all schemas without source-tree
    paths.

### Acceptance criteria

- no network/model call and no credential access;
- exactly one process consumes a grant;
- every crash state resolves deterministically, with possible submission UNKNOWN
  and no retry authority;
- no public derivative contains a secret canary or arbitrary private event text;
- connector accounting is equivalent across providers for equivalent evidence;
- timeouts leave no descendant process;
- strict JSON behavior is consistent and bounded;
- Git packet hash is unchanged by later worktree mutation;
- original evidence is immutable and restored bundles reproduce exact hashes;
- installed-package fake workflow passes outside the repository.

This single packet is more valuable than adding many schema assertions that
exercise only in-memory happy paths.

## Explicit unknowns

The following require later authorized inspection, consumer decisions, or live
measurement. They were not inferred:

- actual remote branch-protection/ruleset configuration and required status
  checks for the private repositories;
- backup inclusion, encryption, retention, and successfully tested restoration
  of the current private evidence root;
- effective Linux procfs `hidepid`/same-user isolation and backup/indexing agents
  on the execution hosts;
- effective Claude managed settings/hooks at run time beyond the published empty
  tool/MCP observations;
- whether the exact OpenClaw version offers a supported protected prompt input
  not documented in the reviewed upstream infer page;
- provider-side request/retry/cancellation behavior hidden behind subscription
  clients;
- whether OpenAI/Anthropic hard budget controls exist and apply in the exact
  account; no account inspection was performed;
- exact executable provenance/digests and package-manager update behavior on the
  execution hosts;
- model/runtime weight provenance beyond the recorded Ollama tag digest;
- independent backup and disaster recovery objectives for private vs public
  evidence;
- external consumer environments and redistribution/license choice;
- a prospective comparable cohort with measured preparation/review time, accepted
  outcomes, cold/warm state, energy, and matched frontier baselines;
- semantic defect/omission rate on held-out `change-summary-v1` cases;
- whether one accepted local extraction and current refused/continued summaries
  lead to net savings after all human and maintenance overhead.

## Exact recommended next engineering action

Implement a **filesystem-backed, one-use grant reservation keyed by the canonical
grant digest and attempt ID**, using exclusive creation in an owned private state
root. Record `RESERVED`, `SUBMISSION_UNCERTAIN`, and `COMPLETE` without rewriting
history; refuse a second consumer before adapter construction. Add one two-process
race test and crash injection immediately after reservation. This is the smallest
change that prevents a real authority violation and creates the anchor needed for
the subsequent crash journal and connector-parity work.

No additional inference is needed to verify that action.

## External primary sources

The companion manifest records retrieval dates and claim use. Principal sources:

- Claude Code CLI, settings, and hooks documentation:
  `https://code.claude.com/docs/en/cli-reference`,
  `https://code.claude.com/docs/en/settings`, and
  `https://code.claude.com/docs/en/hooks`.
- OpenClaw maintained infer documentation:
  `https://github.com/openclaw/openclaw/blob/main/docs/cli/infer.md`.
- Ollama Generate and List Models APIs:
  `https://docs.ollama.com/api/generate` and
  `https://docs.ollama.com/api/tags`.
- Python subprocess, urllib, and JSON documentation:
  `https://docs.python.org/3/library/subprocess.html`,
  `https://docs.python.org/3/library/urllib.request.html`, and
  `https://docs.python.org/3/library/json.html`.
- RFC 8259 JSON interoperability:
  `https://www.rfc-editor.org/rfc/rfc8259.html`.
- Linux `proc_pid_cmdline(5)`, `fsync(2)`, and `open(2)`:
  `https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html`,
  `https://man7.org/linux/man-pages/man2/fsync.2.html`, and
  `https://man7.org/linux/man-pages/man2/open.2.html`.
- NIST AI 600-1 (2024-07-26) and NIST SP 800-218 (2022-02-03):
  `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf` and
  `https://csrc.nist.gov/pubs/sp/800/218/final`.
- PyPA packaging specifications and tutorial:
  `https://packaging.python.org/en/latest/specifications/pyproject-toml/`,
  `https://packaging.python.org/en/latest/specifications/pylock-toml/`, and
  `https://packaging.python.org/en/latest/tutorials/packaging-projects/`.
- SLSA provenance and GitHub protected-branch documentation:
  `https://slsa.dev/spec/v1.2/provenance` and
  `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches`.

## Research limitations

This was a source, contract, fixture, published-evidence, and documentation
review. It did not inspect credentials, subscription/account controls, browser or
client session stores, private infrastructure, live host configuration, GitHub
repository settings, backups, provider history, or runtime traffic. It did not
execute adversarial payloads against a live system. The code findings are exact
for the reviewed revisions; operational findings are labeled unknown where the
published evidence cannot establish them.

Live effects: creation and validation of this isolated research artifact and its
source manifest, followed by the separately authorized non-forced research-branch
publication. No canonical-main change, connector invocation, model/API/GPU call,
credential access, installation, deployment, or runtime mutation.
