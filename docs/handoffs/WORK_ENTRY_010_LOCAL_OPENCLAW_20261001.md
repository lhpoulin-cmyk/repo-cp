# Work Entry 010 — local OpenClaw acceptance disposition

Date: 2026-10-01 EDT / 2026-10-02 UTC. Owner boundary: helix-offload owns
portable DERP evaluation, adapters and execution evidence; repo-cp records
authority, work sequence and evidence disposition.

Louis redirected the active slice from hosted troubleshooting to the owned local
path. No further Claude or OpenAI invocation was authorized. The two failed
Claude attempts remain immutable historical evidence and were assigned to parked
Work Entry 013; the existing OpenAI boundary was assigned to parked Work Entry
014. Neither registration starts implementation or grants a hosted call.

## Verified topology

OpenClaw `2026.7.1-2` build `0790d9f` runs on `ws-hadrian` as the one-shot
client/orchestrator. It reaches Ollama `0.32.0+helix.repeatlimit.1` over the
existing loopback SSH transport into VM 320 `cuda-compute-katra` on `hv-katra`.
Ollama, not OpenClaw, executes `phi4-mini:latest` digest
`78fad5d182a7c33065e153a5f8ba210754207ba9d91973f57dffa7f487363753`
on the passed-through NVIDIA GeForce RTX 5070 Ti. The installed default OpenClaw
agent profile was rejected as unsuitable because it permits tools. The accepted
path uses `openclaw infer model run --local` with an isolated one-model config,
no fallbacks, all tools denied and elevated tools disabled.

## Authorized result

Exactly one test-only local attempt,
`work-entry-010-openclaw-local-live-001`, was **SENT** after an exact admission
result and content-bound LIVE grant. The 38-byte synthetic Ada/Basic/`REF-42`
input produced customer `Ada`, plan `Basic`, and preserved `REF-42`. DERP's four
deterministic document checks passed. The artifact is untrusted and semantic
adequacy remained Louis's decision. Louis subsequently recorded `ACCEPTED`,
0 ms preparation effort and 120,000 ms (2 minutes) review effort. This accepts
the one artifact; it does not broaden model qualification or execution authority.

The adapter elapsed time was 9,432 ms from a cold state. The post-call Ollama
snapshot reported 3,087,615,917 bytes loaded and the same amount in VRAM at
context 4096, supporting full GPU residency at that snapshot. Token counts,
energy integral and operating cost are `UNKNOWN`. One result is connectivity,
bounded-behavior and human-acceptance evidence only, not
throughput, production qualification, comparative savings or proof of the 20%
frontier-usage target.

Canonical helix-offload main and review branch
`codex/work-entry-010-local-openclaw` were independently verified at
`811b952da451a21ebc2e68df0751c012df63dddc`. Detailed sanitized evidence is in
helix-offload at `docs/evidence/WORK_ENTRY_010_OPENCLAW_LOCAL_RESULT.md` and
`docs/evidence/work-entry-010-openclaw-local-20261001/`.

The later disposition commit
`ca9998755a463980bf9f618338d4e9303cd1f7bc` publishes Louis's acceptance and
reported effort on canonical helix-offload main and review branch
`codex/work-entry-010-local-acceptance-disposition`. It does not modify the
original artifact, receipt or response envelope.

Exact next action: separately resume Work Entry 013 if Louis authorizes Claude
implementation/comparison. The accepted local baseline satisfies its comparison
prerequisite but does not activate the parked entry or authorize a hosted call.
Work Entry 014 remains parked behind 013.

Live effects: one bounded local inference request ran through OpenClaw and
Ollama on the existing cuda-compute-katra RTX 5070 Ti; the helix-offload review
branch and canonical main were published non-forced. No hosted request, retry,
fallback, download, upgrade, installation, credential/account change, network
exposure, resource reallocation, service mutation, generated-text application
or cohort run occurred.
