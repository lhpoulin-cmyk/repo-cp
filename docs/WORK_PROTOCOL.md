# Helix repository work protocol

Standard: `HELIX_REPOSITORY_WORK_PROTOCOL_V1`

Custodian: repo-cp at Louis's direction

Scope: bounded development work and its repository evidence

This standard makes repo-cp the durable protocol boundary for preparing,
executing and reviewing repository work. It does not transfer authority from
Louis, expand a target repository's ownership, authorize peer changes, or turn
the repo-cp CLI into an executor. The machine-readable interfaces are
[`work-entry-v1.schema.json`](../schemas/work-entry-v1.schema.json) and
[`work-result-v1.schema.json`](../schemas/work-result-v1.schema.json).

## Work entry and result

Meaningful work begins with a `HELIX_WORK_ENTRY_V1` document. It identifies the
target and objective, governing standards, granted and withheld authority,
starting revision and dirty state, dependencies, validation, mutation scope,
required evidence and expected result protocol. A prose handoff may explain the
work, but it is not a substitute for these fields.

## Clean Execution Baseline

`HELIX_CLEAN_EXECUTION_BASELINE_V1` is a portfolio-wide invariant for
repositories governed by repo-cp. An agent may inspect a dirty repository, but
must not begin repository mutations in an execution workspace containing
pre-existing, unrelated, mixed or unattributed dirtiness.

At work entry, record the intended canonical ref and resolved HEAD, the source
and execution workspace identities, staged/unstaged/untracked state, attribution
of observed dirtiness, entry phase, isolation mechanism and mutation gate. A
dirty source checkout is an observable condition and is not inherently
`BLOCKED`. A dirty execution workspace containing anything not attributable to
the current work entry closes the mutation gate.

Do not reset, clean, stash, overwrite, absorb or silently reattribute unknown or
pre-existing work. The permitted outcomes are:

1. stop and request resolution or authorization; or
2. when repository policy permits, create or reuse an isolated clean worktree
   or checkout at the intended canonical baseline and retain evidence for both
   the dirty source and clean execution workspaces.

For a `START` entry, an open mutation gate requires a clean execution workspace
at the resolved baseline. For `CONTINUE`, it may also accept dirtiness attributed
exclusively to that same work entry. The conformance CLI reports `OPEN` or
`CLOSED`; it never grants mutation authority. A work result partitions every
ending staged, unstaged and untracked path into current-work-entry,
pre-existing, unrelated or unknown attribution so task-created state cannot
silently absorb earlier state.

After bounded work, the executor emits a `HELIX_WORK_RESULT_V1` document. It
records starting and ending state, changed files, performed and deliberately
omitted mutations, validation, evidence, delivery stage, status topology, live
effects and the recommended next action. Human summaries are projections of
this evidence rather than a second authoritative state record.

The current primitive validates one document from standard input and emits a
small receipt:

```sh
./tools/repo-cp check-work-entry < work-entry.json
./tools/repo-cp check-work-result < work-result.json
```

The [usage guide](WORK_PROTOCOL_USAGE.md) provides fixture-based entry and result
instructions and explains how usage-accounting unknowns are preserved.

Validation never executes the described work, grants authority, writes a file,
contacts a network, discovers a target, or establishes that an assertion is
true. It establishes only bounded schema and relationship conformance. Work
entries and results are task artifacts; repo-cp does not create a global mutable
queue or make every result a committed repository artifact.

The present role mapping is operator (intent, authority, approval and
exceptions), architect (architecture, decomposition, triage and evidence
review), executor (repository inspection, implementation, tests and local
evidence), and expedition agent (optional multi-system work). Role names are
capabilities, not vendor identities. Ordinary repository-local work does not
require an expedition agent.

## Status topology

The result schema represents status as nodes plus directed relationships.
Nodes distinguish `COMPLETED`, `ACTIVE`, `PENDING`, `BLOCKED`,
`NON_BLOCKING_INCOMPLETE`, `UNKNOWN`, `DRIFT`, and
`AUTHORIZATION_REQUIRED`. Node kinds distinguish ordinary work from a
`DEPENDENCY`, `EXTERNAL_DEPENDENCY`, `CROSS_CONTROL_PLANE_REQUEST`, or
`AUTHORIZATION` item.

Relationships express `BLOCKED_BY`, `DEPENDS_ON`, `NON_BLOCKING_FOR`,
`REQUIRES_AUTHORIZATION_FROM`, `OWNED_BY`, `HANDOFF_TO`, and `SUPERSEDES`.
Every endpoint must identify a node in the same result. A completed item cannot
be blocking. A blocked item is blocking, while a non-blocking-incomplete item is
not. Thus completed work is not resurrected as a blocker, incomplete work need
not block unrelated progress, authority needs remain explicit, and peer-owned
work becomes a handoff instead of an implicit mutation.

`PASS`, `UNKNOWN`, `DRIFT`, `BLOCKED`, and `NOT_APPLICABLE` remain the audit and
validation finding vocabulary. They are not collapsed into workflow progress:
for example, a workflow node may be `ACTIVE` while one remote-freshness check is
`UNKNOWN`.

## Upstream-first engineering

Helix integrations prefer keeping Helix behavior outside upstream source when
reasonably feasible. Use adapters, configuration, selectors, wrappers, evidence
collectors, policy layers, publication machinery and external orchestration
before maintaining a private source divergence. This ecosystem-wide standard
is not limited to ARM work.

An upstream modification or fork is permitted when necessary, but its work
entry and result must make the divergence explicit, bounded and justified. The
result must identify the affected upstream revision, validation, maintained
delta and a retirement or upgrade path. Convenience alone is not justification.

## Writer boundary

Processing, ripping, encoding, inspection, discovery and staging services do
not casually receive permanent-storage write access. They produce a candidate
artifact and validation evidence for a narrow promotion/publication boundary.
Read-only access to a final library, including the present B70 arrangement, is a
least-privilege feature rather than a defect.

The destination is not permanent manual publication. The authoritative final
publication service must ultimately hold the narrowly scoped capability to
perform an authorized permanent-storage write:

```text
processing or staging
  -> candidate artifact
  -> validation and evidence
  -> promotion or publication boundary
  -> final publication service
  -> bounded permanent-storage write
```

A transitional writer may exist during development. Its work entry must name
the temporary authority and prohibited scope; its result must retain the
non-blocking incomplete item to transplant that capability into the final
publication service when the service becomes authoritative.

## Ownership and flow

The intended flow is operator intent and authority, architecture and triage,
repo-cp work entry, repository execution, repo-cp work result, evidence review,
and operator involvement only for judgment, authorization, material ambiguity
or exceptions. Louis remains the ultimate authority without serving as the
transport for large prose handoffs.

The target repository owns its implementation and desired state. repo-cp owns
these protocol schemas and their conformance check. A cross-control-plane need
is recorded as a `CROSS_CONTROL_PLANE_REQUEST` node and related with
`HANDOFF_TO`; it is not permission to modify the peer. Foundation continues to
own universal contracts and conformance. This local work protocol does not
extend the Foundation operator-action schema or repository enrollment schema.
