# Work Entry 013 continuation — security review, Claude result and grant reservation

Status: `PARKED / OFFLINE HARDENING PUBLISHED / CLAUDE HUMAN DISPOSITION PENDING`

## Unified evidence

The security research is retained at commit
`4eae1b63e85cdfe42ff64a4ab149e2661ab86150`; its report and manifest hashes are
verified in the separate
[disposition record](../../research-notes/2026-10-03-helix-offload-security-safety-durability-reusability-review-disposition.md).
It remains research rather than implementation proof.

The Work Entry 013 Claude result remains unchanged:

- attempt `work-entry-013-claude-change-summary-live-002-attempt-001`;
- `SENT / RESPONSE_RECEIVED / GENERATION_COMPLETED / DERP_REFUSED`;
- requested/observed `claude-haiku-4-5-20251001` through Claude Code 2.1.283
  and the existing claude.ai Pro subscription;
- one observed client run, zero observable retry events, no tools/MCP, and
  underlying provider request/retry behavior `UNKNOWN`;
- `end_turn`, not truncated, 5,550 ms;
- 5,202 input, 372 output and 5,574 total observed tokens;
- `$0.012261` client-reported list cost and `UNKNOWN` actual marginal
  subscription charge;
- authoritative `REFUSED / USAGE_LIMIT_EXCEEDED` against 4,000 input and 4,600
  total tokens, before parsing/postflight/assembly;
- no artifact; separate unchanged offline diagnostic
  `REFUSED / MALFORMED_OUTPUT`; human disposition `PENDING`.

The completed response and useful measurements demonstrate connector capture,
not semantic success. The packet carried the historical source fact
`NOT_AUTHORIZED_FRESH_ONE_INVOCATION_GRANT_REQUIRED` inside its authority data.
The model treated that data as current authority. The published prompt told the
model to treat excerpts/receipt text as untrusted and not copy authority, but it
did not explicitly distinguish historical authority facts from current
host-enforced authority. This is evidence of boundary confusion in this attempt,
not proof of a particular model or upstream defect.

Prepared follow-up keeps three planes distinct: deterministic preservation of
historical authority facts; current admission/grant authority enforced only by
the host; and model instructions separated from explicitly untrusted source
data. A model never grants or revokes execution.

The source packet contained 8,541 UTF-8 bytes, the generated system instruction
817 bytes and the serialized stdin prompt 9,321 bytes. Claude Code reported
5,202 input tokens but exposed no category breakdown sufficient to attribute
that total to packet, system/client overhead, cached categories or other
provider accounting. Byte counts are not token counts. The input/total checks
were retrospective: they detected the overrun after consumption and were not
preventive caps.

## Implemented hardening

Canonical helix-offload `d6c7f708fa5bee2845fbd11b67a946161898dfe1`
implements `grant-reservation/v1`. The canonical grant digest is the unique key;
the first attempt ID is immutable ownership metadata. Each supported explicit
executor uses one caller-configured absolute private shared store. Exclusive
creation and file/directory fsync happen before adapter construction or
invocation. Any created record blocks reuse permanently in this slice; crashes,
restarts, timeouts and cleanup do not release it.

This provides at-most-once local admission only for callers sharing one reliable
POSIX filesystem store. It does not provide exactly-once provider execution,
crash submission reconciliation, multi-host consensus, hidden-client-retry
detection or protection between independently configured stores.

Validation: 69/69 helix-offload unittests; 158/158 JSON files; 21/21 schemas;
two-process exactly-one fake invocation; different-attempt reuse refusal;
crash/restart refusal; storage-failure no-invocation; compilation, three pinned
digests, changed Markdown links, secret-indicator scan and whitespace passed.

## Protected private recovery evidence

Retain without publication or retirement:

`/home/louis/helix-arpa/repo-cp/.agent-checkouts/codex/work-entry-013-claude-live-002-private/`

The directory remains mode 0700 and its nine files remain mode 0600. On
2026-10-03 a metadata/hash-only verification reproduced the public-copy hashes
for the grant, attempt, connector outcome, receipt and pending disposition, and
the already-published private raw/envelope hashes. The private manifest differs
from the sanitized publication manifest as expected; neither was replaced.
The exact inventory is
[`WORK_ENTRY_013_PRIVATE_CAPTURE_INTEGRITY_20261003.json`](WORK_ENTRY_013_PRIVATE_CAPTURE_INTEGRITY_20261003.json).

Future migration plan, not executed:

1. Louis approves a durable private root outside `.agent-checkouts`, its owner,
   backup/retention policy and disclosure boundary.
2. Freeze the nine-path size/mode/SHA-256 inventory; create the destination
   0700 and copy each file independently with exclusive creation and mode 0600.
3. Recompute every hash and file count, create a new integrity manifest, and
   prove no hardlinks connect source and destination.
4. Restore an independent test copy and verify all hashes before declaring the
   destination durable.
5. Keep this source until Louis separately approves retirement after backup and
   restore evidence; deletion is never implied by a successful copy.

## Remaining registered candidates

The ranked, non-executing candidate group in `registries/work-topology.json`
preserves durable phases/crash reconciliation, private recovery, public
derivatives, connector parity, protected OpenClaw prompt transport, truthful
preventive controls, prompt-authority/token accounting and standalone release
adoption. Work Entry 014 remains parked. No new Work Entry number was allocated.

Exact next action: Louis may record `ACCEPTED`, `REJECTED` or
`FRONTIER_CONTINUATION` for the preserved Claude result. Any new model call or
follow-up implementation requires separate authority; this record grants none.

Live effects: canonical helix-offload review-branch and main publication to
`d6c7f708fa5bee2845fbd11b67a946161898dfe1`, plus authorized repo-cp publication
of the research and control records containing this handoff. No inference,
credential/account change, installation, deployment or runtime-service mutation.
