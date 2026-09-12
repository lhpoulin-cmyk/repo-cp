# Enrollment, audit and recovery

## Enrollment

Discovery is observation, not enrollment. The local versioned
schemas/repository-enrollment-v1.schema.json defines DISCOVERED, PILOT, ENROLLED
and EXCLUDED. Pilot/enrolled entries require immutable revisions and approved
public metadata digests. ENROLLED requires a Louis-approved enrollment reference.
Schema conformance checks presence, not authenticity: Louis's reviewed Git change
is the approval boundary. Producer-submitted references are not approvals.

Verify peer mission, authority, canonical remote and source revision read-only.
Agree the public allowlist with its owner, collect committed digests, identify
limitations and prepare an exact registry diff with enrollment evidence. Run
tools/validate and the bounded pilot. Louis approves the enrollment diff; peer
declaration/pin changes remain separately authorized peer work. The bot never
commits, pushes or merges enrollment or invokes peer validators.

The [next gate](proposals/auth-cp-enrollment.md) includes an unapplied, tested
enrollment diff. No repository is enrolled. Next batch: auth-cp alone, after owner review of its
B70 Foundation pin and Louis's approval of exact audit scope and enrollment.
Foundation and ansible-cp remain discovered. No sibling discovery enrolls peers.

## Checks

| ID | Property | Limit |
| --- | --- | --- |
| RC001 | Accepted Foundation bytes and separate pins | Reviewed local trust, not action-artifact checksum enforcement |
| RC002 | Explicit enrollment or bounded pilot | No live admission |
| RC003 | Local branch and immutable HEAD match | No remote query or whole-tree cleanliness proof |
| RC004 | Allowlisted public regular files exist | No arbitrary discovery |
| RC005 | Allowlisted bytes match accepted digests | Changed bytes never become accepted authority |
| RC006 | No configured secret indicators | Heuristic; values never printed |
| RC007 | Accepted VERSION has semantic version shape | No release compatibility proof |
| RC008 | auth-cp B70 handoff matches separate Foundation pins | Difference requires owner review, not automatic replacement |
| RC009 | Current remote publication freshness | UNKNOWN offline; separate operator preflight |

PASS means the named property was observed. DRIFT means accepted evidence
differs. BLOCKED means a declared check cannot proceed safely. UNKNOWN means
insufficient evidence. NOT_APPLICABLE means no selected scope/check. Overall
precedence is BLOCKED, DRIFT, UNKNOWN, then PASS; all individual findings remain.
Missing files, symlinks, devices and oversize metadata are unavailable, never
followed or echoed. Ordinary .git directories with loose/packed branch refs or
detached HEAD are supported; worktree indirection reports UNKNOWN. Unrelated
dirty files are outside the allowlist and are not claimed clean by an audit.

## Exceptions and proposals

Active exceptions: NONE. Louis approves exact scope, rationale, owner,
duration/review trigger and evidence in a separate reviewed record. This release
has no automatic exception bypass or expiration enforcement. Missing contract
integrity is never silently waived.

`propose` emits deterministic findings for review, with repository, check ID,
reason, Foundation source and authorization false. It writes nothing. Patch is
null: current findings require owner review; no safe authorized peer patch is
available. This is not an executable plan or READY action. A later concrete
patch must be narrow, traceable, authorized, tested for idempotence and reversal,
and reviewed in its owning repository. Never self-merge or rewrite pins to pass.

## Recovery and durable handoff

Failed renders have no partial output. Review the producer's public source
locally; do not log rejected payloads. For corrupt accepted artifacts, reverify
the canonical commit and restore exact reviewed bytes via a follow-up commit.
No fallback renderer, mutable pin or downloaded-code execution is allowed.

Pin updates require compatibility review, separate immutable repository and
doctrine pins, SHA-256 checks, reference/consumer tests, diff review and normal
publication authority. Preserve historical acceptance. Never create self-referential
commit pins; final handoff commits can follow implementation commits.
Reversal uses a reviewed follow-up commit, never history rewriting. No runtime
rollback is needed because no runtime mutation occurs. Durable handoffs include
commits, acceptance/pilot evidence, checks, limitations, dirty-state handling,
remote parity and the next exact decision. CI proves only local synthetic
properties; no peer credentials or operational/live-infrastructure jobs exist.
