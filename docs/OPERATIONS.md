# Enrollment, audit and recovery

## Local repository creation

Use [repository creation](REPOSITORY_CREATION.md) for the explicit local `create`
command, generated AGENTS.md and desktop project Instructions. Creation does not
add or change enrollment records. Existing audit commands remain read-only.

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

The auth-cp RC008 owner review is complete and COMPATIBLE. Louis approved the
exact seven-file enrollment scope; the [enrollment receipt](acceptance/auth-cp-enrollment.md)
records application. Default audits select auth-cp and ansible-cp. RC009 stays UNKNOWN for each.
The [ansible-cp approval receipt](acceptance/ansible-cp-enrollment.md) records its
verified ten-file enrollment. Foundation remains discovered. Further enrollment requires a new
explicitly scoped approval; no sibling discovery enrolls peers.

## Checks

The operator-directed [file-integrity doctrine](FILE_INTEGRITY.md) records
`HELIX_NO_HARDLINKS_V1`, its schema-backed production-engineering requirements,
verified copy/publication reference and peer adoption process. Run
`python3 -B tools/audit-hardlinks` for local metadata-only findings. Standard
peer audits add RC011 only for existing selected public allowlists. Neither
operation repairs violations or expands peer scope.

| ID | Property | Limit |
| --- | --- | --- |
| RC001 | Accepted Foundation bytes and separate pins | Reviewed local trust, not action-artifact checksum enforcement |
| RC002 | Explicit enrollment or bounded pilot | No live admission |
| RC003 | Local branch and immutable HEAD match | No remote query or whole-tree cleanliness proof |
| RC004 | Allowlisted public regular files exist | No arbitrary discovery |
| RC005 | Allowlisted bytes match accepted digests | Changed bytes never become accepted authority |
| RC006 | No configured secret indicators | Heuristic; values never printed |
| RC007 | Accepted VERSION has semantic version shape | No release compatibility proof |
| RC008 | Reviewed B70 handoff records match separate Foundation pins | Difference requires owner review, not automatic replacement |
| RC009 | Current remote publication freshness | UNKNOWN offline; separate operator preflight |
| RC010 | ansible-cp derived auth policy and containing handoff pins | Independent compatible auth owner-review evidence; no automatic replacement |
| RC011 | Governed regular-file single-link integrity | Protected violations BLOCKED; ordinary workflow violations DRIFT; unavailable metadata UNKNOWN; exclusions unscanned |

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
publication authority. Preserve historical acceptance. Never create
self-referential commit pins; final handoff commits can follow implementation
commits. Reversal uses a reviewed follow-up commit, never history rewriting. The
read-only interfaces require no runtime rollback. Local creation has its own
staging, publication and recovery boundaries in the creation procedure. Durable
handoffs include commits, acceptance/pilot evidence, checks, limitations,
dirty-state handling, remote parity and the next exact decision. CI proves only
local synthetic properties; no peer credentials or
operational/live-infrastructure jobs exist.

## Historical ansible-cp pilot

The earlier `--pilot --repository ansible-cp` workflow selected the authorized
pilot. ansible-cp is now enrolled and needs no --pilot flag. The repository selector never grants enrollment or pilot authorization.
The additive local V1 enrollment schema permits null digests for the three
explicitly absent ansible-cp metadata paths in PILOT only. Null is absence
evidence, not accepted content or a waiver: absence reports UNKNOWN; newly
appearing content reports DRIFT until reviewed. ENROLLED requirements are unchanged.
The absence of VERSION, OWNERSHIP.md and PROVENANCE.md does not establish a
universal Foundation violation. docs/AUTHORITY.md is reviewed domain evidence,
not an invented replacement file. scripts/validate is hashed, never executed.

RC010 compares the derived policy pin to the separate reviewed auth policy
commit, and the observed published pin to the containing auth handoff commit.
Missing or stale independent owner evidence yields UNKNOWN. RC008/RC010 drift
requires ansible-cp owner compatibility review; historical observation is not
desired state. See the [pilot report](acceptance/ansible-cp-pilot.md) and
[review proposals](proposals/ansible-cp-remediation.md).
