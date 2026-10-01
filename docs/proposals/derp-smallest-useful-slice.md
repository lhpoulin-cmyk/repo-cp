# Work Entry 010 — smallest useful DERP slice

Status: review-only scope proposal; implementation is not authorized.

DERP means Deterministic Engine for Policy and Routing. The name does not define
an architecture. The only recovered functional statement is canonical
helix-offload `3073fd4e4c552a692d506489597faaf3f5e1038a`: Work Entry 010 / DERP
owns future deterministic routing or policy selection, while Execution Admission
V1 performs supplied-profile matching and explicit selection without routing.

## Overlap and smallest gap

| Existing capability | Unresolved recurring decision | Proposed owner | Smallest missing capability |
| --- | --- | --- | --- |
| repo-cp topology and work protocol record lifecycle, priority, dependencies, scheduling eligibility and explicit authority | Which recorded candidate may even be considered next without rereading every handoff? | repo-cp | Compact current-state projection; supplied by `CURRENT_STATE.md`, not DERP |
| Work Entry 006 deterministically advises whether explicit constrained-capacity evidence supports considering one otherwise-eligible entry | Which eligible target/profile should be chosen? | Work Entry 006 remains capacity adviser only | None in 006; do not turn capacity advice into routing or authority |
| Work Entry 005 validates one execution request, matches supplied qualified profiles and validates an explicit selected identity | When multiple already-qualified candidates are supplied, which one best satisfies an explicit operator policy? | DERP logical function; implementation repository still UNKNOWN | Deterministic selection among supplied, already-admissible candidate identities; return a proposal, never execute |
| Existing helix-offload matching returns zero, one or multiple candidates and refuses ambiguity | How should policy break an ambiguity without hiding uncertainty or inventing candidate data? | DERP, with helix-offload owning the admission interface it consumes | One stable policy evaluator over explicit candidate metadata; no scheduler, queue, adapter or fallback |
| Work Entry 008 proposes deterministic repository facts, evidence/semantic-delta preparation, dependency analysis and compact context | What evidence should be prepared for a routing decision? | 008 if later accepted; owning repository facts stay with each source | A future evidence producer may supply bounded facts, but DERP must not duplicate repository inspection |

## Proposed slice: deterministic candidate recommendation

The first slice accepts only caller-supplied, versioned data:

- one request identity and content digest;
- the exact set of candidate `{id, sha256}` identities returned by a valid 005
  admission result;
- for each candidate, an allowlisted policy-fact object whose schema and source
  revision are explicit;
- one explicit operator-approved policy revision; and
- the caller's authority reference as opaque provenance, never as proof.

Rules are deliberately small:

1. Reject malformed, duplicate, unbound or stale candidate/fact identities.
2. Never add a candidate and never reinterpret a 005 denial or refusal.
3. Apply only total-order rules present in the supplied policy revision, in
   declared order. A useful first rule set is exact required capability match,
   then explicit preferred profile IDs, then a stable lexical identity tie-break
   only when the policy expressly permits it.
4. Return one recommendation only when the rules yield exactly one candidate.
5. Return `UNKNOWN` for absent or stale facts and `REFUSED` for conflicts,
   unsupported policy, no candidate or unresolved ambiguity.
6. Preserve `authority_effect: NONE`, `execution_occurred: false` and
   `adapter_invoked: false`; do not invoke 005, a model, an adapter or a peer.

Output is a deterministic review artifact containing the request digest, policy
identity, ordered candidate identities, decision (`RECOMMENDED`, `UNKNOWN`, or
`REFUSED`), stable reason codes, selected identity only when unique, evidence
references, and the next evidence needed. It is not an admission result, command,
schedule or execution receipt.

## Acceptance criteria

- Same canonical inputs produce byte-identical output independent of input order.
- Invalid, duplicate, stale, missing and contradictory facts fail closed without
  rejected values in diagnostics.
- Every recommendation names an input candidate and the exact rule/evidence that
  selected it; unresolved ties never choose silently.
- Tests prove DERP cannot turn 005 `DENIED`, `REFUSED` or `MATCHED` into
  `ADMITTED`, cannot grant authority and cannot invoke execution.
- A reuse review confirms that no existing helix-offload or repo-cp function
  already performs the selected rule set before implementation begins.
- The implementation repository/owner and publication authority are explicit.

Estimated efficiency benefit, not a measured result: for recurring routing
reviews involving 005, 006, 008 and topology evidence, the current-state view
reduces status reconstruction from at least five records to one. The proposed
DERP slice could then replace a repeated multi-candidate comparison with one
deterministic review artifact. Validate that estimate against three real routing
decisions before expanding the rules or building orchestration.

Smallest next decision: name the repository and owner for this review-only
evaluator, or keep Work Entry 010 parked. No implementation follows from this
proposal.
