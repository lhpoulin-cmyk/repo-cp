# Work Entry 013 continuation — durable recovery and execution lifecycle

Status: `PARKED / OFFLINE HARDENING PUBLISHED / CLAUDE ATTEMPT REJECTED`

## Human disposition

Louis recorded `REJECTED` for
`work-entry-013-claude-change-summary-live-002-attempt-001` because the
authoritative result was `USAGE_LIMIT_EXCEEDED`. A separately labelled offline
diagnostic also found that the unchanged returned text did not satisfy the
requested JSON contract.

Canonical helix-offload commit
`3f99e0fda9a84b99b52019cf463a061da906215a` publishes the disposition as a
new, content-bound record. It is bound to canonical receipt SHA-256
`c3a365fd47b7ad6b128aaf768380ba40df8d89bdcdcff483caef488dee3c7b36` and
the preserved attempt evidence. `artifact_sha256` remains null: authoritative
postflight and assembly did not run, so no artifact exists. Preparation and
review durations remain `UNKNOWN`. Earlier `PENDING` records and all original
attempt evidence remain unchanged.

The original execution outcome remains:

`SENT / RESPONSE_RECEIVED / GENERATION_COMPLETED / DERP_REFUSED`

This disposition does not retroactively raise limits, repair the response or
prove a provider defect.

## Durable private recovery domain

The deployment now uses the explicitly configured private root
`/home/louis/.local/state/helix-offload/recovery-v1`, outside repositories,
disposable checkouts and temporary directories. The deployment-domain identity
is `louis-ws-hadrian-helix-offload-v1`; its root marker SHA-256 is
`abf6132bfd6759667944ad3266f81fe0e00c5688a6eecc21c002f547dd36bad9`.
Directories are mode `0700`; regular files are mode `0600`, owned by the
effective user and single-linked. Symlinks, unsafe ownership or modes, and
repository/temp/checkouts roots are refused.

This is persistent local XDG state. It is not an independent backup and does
not protect against loss of the workstation or its storage. The portable
contract contains no Louis-specific path: callers provide the deployment
root explicitly.

## Durable execution phases

Helix-offload now records an append-only, SHA-256-linked lifecycle after the
one-use grant reservation:

1. `GRANT_RESERVED`
2. `INVOCATION_INTENT_PERSISTED`
3. `SUBMISSION_BOUNDARY_ENTERED`
4. `SUBMISSION_EVIDENCE_RECORDED`
5. `RESPONSE_OBSERVED`
6. `CAPTURE_COMMITTED`
7. `PROCESSING_COMPLETED` or `PROCESSING_FAILED`

Each numbered event is exclusively created and fsynced, with its predecessor
hash recorded; containing directories are also synchronized. A partial,
missing or corrupt event prevents continuation. Phases never regress.

`SUBMISSION_BOUNDARY_ENTERED` is a pre-send marker and cannot prove that a
request was sent. A crash before later adapter evidence is `SUBMISSION
UNCERTAIN`. `SUBMISSION_EVIDENCE_RECORDED` records only what the adapter can
support. A response may be observed before its capture is durably committed;
missing capture does not prove no response arrived. Later parse, postflight or
processing failure cannot turn a sent or uncertain attempt into `NOT_SENT`.

All five explicit execution commands share this lifecycle boundary. Fake runs
remain labelled synthetic. The boundary supplies at-most-once local admission
within one correctly shared reservation/recovery domain; it does not provide
exactly-once provider execution or coordination across independent stores.

## Read-only reconciliation

`helix-offload recovery-reconcile` validates root safety, the ordered hash
chain and private-capture references, then reports the last durable phase,
confirmed facts, explicit uncertainties, integrity findings and next
permissible recovery action. It never invokes an adapter, replays a request,
releases a reservation, issues a grant or edits evidence. A reserved attempt
remains blocked after a crash.

## Protected-capture migration

The published nine-file integrity inventory was verified before copying from:

`/home/louis/helix-arpa/repo-cp/.agent-checkouts/codex/work-entry-013-claude-live-002-private/`

The files were copied into the configured durable root with exclusive
creation. Source and destination path, size, SHA-256, mode, ownership, link
count and distinct inode were verified. The original nine-file migration
record has SHA-256
`fb19fa241d28392bb0e9a66cce34d8582b9c905ec5406f399b47851c1649242c`.
The new private `REJECTED` disposition was copied separately; its migration
record has SHA-256
`1a7cb0d53dc7f70a2e975392c68ef24af96f0d5e36d54749132ff8e1eaa59e88`.

Independent retained restore-test copies were made and verified for all ten
files; their public verification-record hashes are
`b28ff49ad1bc60e0227cf4e77a69b9a7954733e92f6173af64d4eeb0f5bd9aa1`
and
`d31cc71b10b63813dc6c5a33e92c76652a97a26c6378d79439c8158ed4b7cb4e`.
These copies test restoration mechanics but are on the same local durability
boundary and are not independent backup.

The legacy source remains intact as a preserved copy. It was not deleted or
retired. Raw provider/client captures remain private; Git contains only the
already-approved sanitized evidence plus integrity and migration metadata.

## Verification and compatibility

- 80 of 80 helix-offload offline unit tests passed.
- Two-process reservation races, changed-attempt reuse, crashes after
  reservation and around submission/capture, restart reconciliation, partial
  records, corrupt hashes, storage failures, unsafe paths/modes/symlinks,
  successful/failed migration and restore verification passed.
- 173 of 173 repository JSON files parsed; 28 of 28 schemas passed the Draft
  2020-12 metaschema.
- Compilation, three pinned governance digests, changed-document links,
  whitespace, bounded secret-indicator and hard-link checks passed.
- No model, provider API or GPU invocation occurred.

Existing workflow, execution-grant and receipt contracts remain compatible.
Explicit executors now require the deployment-provided recovery root. Claude
and OpenClaw preserve private raw captures there. OpenAI connector raw-capture
parity remains future work; its durable lifecycle cannot claim evidence the
adapter does not expose.

## Separate Claude-failure research

Prompt/model failure analysis is deliberately out of scope for this hardening
slice. Its evidence package and bounded questions are preserved in
[`WORK_ENTRY_013_CLAUDE_FAILURE_RESEARCH_HANDOFF_20261003.md`](WORK_ENTRY_013_CLAUDE_FAILURE_RESEARCH_HANDOFF_20261003.md).
No prompt, model, output contract, usage limit or subscription-adapter behavior
was changed to address that failure. Work Entry 014 remains parked.

Live effects: created one configured private local recovery domain, copied and
verified the protected evidence without deleting the legacy copy, published
the scoped helix-offload implementation and sanitized evidence, and recorded
the rejected human disposition. No inference, API/GPU call, retry, credential
or account change, installation, deployment, paid-route substitution or
runtime-service mutation occurred.
