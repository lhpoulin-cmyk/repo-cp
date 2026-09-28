# Agent checkout operating procedure

Scope: repo-cp development tasks that explicitly adopt this procedure through
repo-cp instructions or a bounded work entry

Authority: none independently; the governing work entry and Louis's decisions
control scope, mutation and publication

This document explains how to operate an isolated checkout under the canonical
contracts. It does not redefine them or apply itself to another repository.
Peer repositories must adopt the procedure explicitly under their own local
authority.

Apply these canonical sources first:

- [`HELIX_REPOSITORY_WORK_PROTOCOL_V1`](WORK_PROTOCOL.md), including the Clean
  Execution Baseline, owns workspace state, mutation-gate and structured
  provenance requirements.
- [`HELIX_LOUIS_WORKFLOW_V1`](LOUIS_WORKFLOW.md) owns roles, work topology,
  review, authorization and closure.
- [`HELIX_AGENT_WORK_CONTRACT_V1`](AGENT_WORK_CONTRACT.md) and
  [`AGENTS.md`](../AGENTS.md) own repository checks, delivery evidence and
  completion behavior.
- [`HELIX_NO_HARDLINKS_V1`](FILE_INTEGRITY.md) owns file-integrity and governed
  traversal policy.

## Placement and access

Place a private task checkout at `.agent-checkouts/<agent>/<task>/` inside the
owning repository. Use a stable, non-sensitive task name and an agent-specific
branch such as `<agent>/<task>`. The parent repository must ignore
`/.agent-checkouts/` so nested Git metadata and work files cannot be staged as
parent-repository content.

Keep `.agent-checkouts/` owner-only where the platform supports permissions.
Git ignore is publication hygiene, not access control. Do not store credentials,
private runtime payloads or copied credential configuration in the checkout.

Reject a symlinked checkout root or a path that escapes the owning repository.
Never force-add nested checkout content to the parent repository.

## Independent checkout creation

Prefer an independent clone with its own Git metadata and a verified canonical
origin. A verified local committed public source may seed the clone with
`--no-hardlinks`; then configure the canonical origin explicitly and fetch the
intended baseline before work. Do not copy source-workspace untracked files,
credential configuration or private material into the new checkout.

Use a linked worktree only when shared Git metadata is permitted and both the
repository tooling and required audits support that layout. Otherwise use an
independent clone and retain any resulting `UNKNOWN` honestly rather than
weakening validation.

Apply the canonical work-entry checks for repository identity, branch, HEAD,
upstream, remote freshness, dirty state and mutation gate. Those structured
fields—not a prose note in this procedure—are the authoritative workspace
provenance.

## Safe reuse and collisions

Before reusing a task checkout, verify that its origin, branch, baseline,
ownership and dirty state match the current work entry. Reuse is safe only when
all observed changes are attributable to that entry as permitted by the Clean
Execution Baseline.

If the requested path already exists with unexpected identity or state, do not
repoint, reset, overwrite or delete it. Preserve the collision and use a distinct
task name or close the mutation gate for review. Reject symlink substitutions and
paths outside `.agent-checkouts/<agent>/`.

Repeated setup must leave an already-correct checkout, parent exclusion and
permissions unchanged. Keep task dependencies inside the permitted sandbox; do
not broaden mounts, credentials, privileges or network authority to make setup
convenient.

## Traversal and evidence

Ordinary traversal rooted at the parent repository—including validation,
packaging, broad searches and discovery—must prune `.agent-checkouts/` before
inspecting nested content. The reviewed file-integrity registry supplies that
exclusion.

This pruning does not prohibit explicitly targeted inspection, validation or
evidence collection inside the authorized active checkout. The checkout is the
execution workspace, so its task diff, tests and structured result evidence must
remain reviewable. It must not be accidentally rediscovered as parent-repository
content.

## Validation, publication and retention

Validate, review, commit and—when separately authorized—publish directly from
the isolated execution checkout. Do not copy or merge task changes into a dirty
source checkout merely to stage or publish them. Normal canonical parity,
review, authorization and closure requirements still apply.

The work entry and work result record source and execution workspace identities,
baseline and ending revisions, dirty state and attribution. These structured
artifacts are authoritative; supplementary prose must not silently replace or
contradict them.

Retain a checkout while it contains unreviewed, uncommitted or unpublished work
needed for recovery. Removal or archival is a separately bounded housekeeping
action after the result is recoverable and its disposition is known. Never
delete an unexpected checkout as generic cleanup.
