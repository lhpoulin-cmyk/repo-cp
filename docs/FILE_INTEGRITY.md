# Helix control-plane file integrity

`HELIX_NO_HARDLINKS_V1`, version 1.0.0, is the canonical operator-directed
Helix-ARPA control-plane workflow invariant recorded by repo-cp in
[registries/file-integrity.json](../registries/file-integrity.json), validated by
[schemas/file-integrity-v1.schema.json](../schemas/file-integrity-v1.schema.json).
It follows repo-cp's existing registry, schema, RC audit, and acceptance pattern.
Louis explicitly authorized this fleet-wide rule and its publication here.
Foundation retains universal contract ownership; its accepted V1 contract,
19 artifacts, pins and doctrine revision are unchanged. This rule does not claim
Foundation ratification, peer adoption, enrollment or live admission.

## Prohibition and rationale

Hardlinks MUST NOT be workflow machinery for protected files or credentials;
ceremony ledgers, intents, receipts, recovery state or backups; evidence or
publication staging; cross-checkout reuse; repository migration or synchronization;
snapshots; normal fixtures; or any control-plane operation copying, preserving,
publishing or restoring a file. Protected regular files MUST have `st_nlink == 1`.
Reject an invalid link count before reading protected bytes or beginning mutation.

Shared inodes undermine independent custody, mode/ownership changes, rollback
and provenance: changing one pathname changes other names for the same file.
Link creation also depends on filesystem, mount and privilege configuration.
Independent verified copies remove this dependency without weakening isolation.

The only exception is a hardlink created inside one bounded negative rejection
test, confined to its verified temporary root and never reused as a normal
fixture. Git-internal, OS, package-manager and unrelated application hardlinks
outside governed artifacts are not prohibited. Clone workflows MUST disable
hardlink reuse (for example Git's `--no-hardlinks`) and preserve independent
artifact copies. Merely having different checkout paths does not prove isolation.

## Detection, scope and classification

RC011 extends existing audit results; ordering and aggregate precedence remain
BLOCKED, DRIFT, UNKNOWN, PASS. Missing evidence is never success.

| Observation | RC011 result |
| --- | --- |
| Governed regular file, one link | PASS / SINGLE_LINK_REGULAR |
| Protected regular file, multiple links | BLOCKED / HARDLINK_FORBIDDEN |
| Ordinary governed workflow file or normal fixture, multiple links | DRIFT / HARDLINK_FORBIDDEN |
| Zero link count, unsafe path, nonregular file or symlink | BLOCKED; distinct reason, never mislabeled as a hardlink |
| Missing/unreadable metadata or incomplete coverage | UNKNOWN |
| Explicitly excluded scope | NOT_APPLICABLE; no scan |

All existing enrolled/pilot public metadata is treated as protected integrity
input. `audit`, `drift` and `propose` use only existing schema-approved enrollment
file paths; they never discover private peer files. Default selection stays
ENROLLED; `--pilot` adds PILOT. RC009 remains UNKNOWN offline. RC004 can independently
BLOCK a missing required file even when RC011 is UNKNOWN.

`python3 -B tools/audit-hardlinks` audits only the local repo-cp tree, using
metadata-only descriptor-relative traversal. It reads no artifact contents.
It prunes `.git`, private agent checkouts, virtual environments, dependency trees,
caches and system/mount paths before descent, including same-device mountpoints
reported by Linux mount metadata. The reviewed registry lists exact exclusions
and protected prefixes (`pins`, `registries`, `docs/acceptance`). Do not blanket
exclude `vendor`: the accepted Foundation snapshot is governed public evidence.
Other repository-defined non-governed exclusions require an owning review and a
registry revision; command-line exclusions cannot hide a finding. Local discovered
names are not echoed; deterministic ordinal labels avoid leaking arbitrary names.
PASS is scoped to the selected files at observation time, not perpetual fleet
conformance or proof of content provenance. Source review must also eliminate
hardlink-dependent code even when no hardlink happens to exist during an audit.

Exit codes: PASS 0; UNKNOWN/DRIFT 1; BLOCKED or invalid invocation 2. JSON uses the
existing report shape, stable sorting, explicit `automatic_execution: false`
and `live_mutation: NONE`. No audit changes files, launches validators or supplies
a remediation patch. Excluded Git reference reads retain their prior semantics;
governed `read_public` inputs additionally enforce one link and stable metadata.
No-atime reads fail closed when the necessary owner capability is unavailable.

## Verified copy and publication

The required sequence is: open without symlink traversal; `fstat` a regular
single-link source; exclusively create a restrictive unpredictable temporary
file on the destination filesystem; copy bytes without logging them; apply exact
owner/group/mode; verify byte count and SHA-256 through opened descriptors;
`fsync` the file; atomically rename on that filesystem; `fsync` the directory;
then independently verify published type, identity, ownership, mode, device,
byte count, hash and single-link status. Source changes are failures. The source
may be on another filesystem; the temporary-to-final rename MUST NOT be.

[src/repocp/publication.py](../src/repocp/publication.py) is an unprivileged,
public/synthetic-only reference library. Read-only CLI commands never import it.
The operator-requested local `create` command reuses its unprivileged, locking
and exclusive-rename primitives, under the separate [creation
procedure](REPOSITORY_CREATION.md). It is not a privileged helper, credential
publisher, remediation executor or new automatic action lane. The caller must
hold exact operation authority and supply absolute paths, expected metadata and
public content digest, the exact reviewed source revision, and a stable
cryptographically random operation identifier. Digests here are public artifact
integrity values, never password hashes or other credential material.

`copy_and_publish` creates a NEW destination only. It refuses existing targets,
intents and receipts. Linux `renameat2(RENAME_NOREPLACE)` supplies atomic no-clobber;
there is no hardlink fallback or check-then-overwrite emulation. A kernel or
filesystem lacking it is an unavailable capability. Root and set-ID execution are rejected. The owner-controlled
destination directory is locked using nonblocking `flock`; independent publishers
must use this protocol. This cannot defend against a malicious same-UID process
or root that can rewrite the trusted directory. Privileged deployment requires
an independently trusted launcher and separately approved ownership design.

A durable immutable intent binds operation, policy/version, tool version, reviewed
source revision, temporary inode, expected
public content and final target before the primary rename. Receipt publication
follows verified durable primary state. SIGINT/SIGHUP/SIGTERM produce controlled
interruption and a value-free outcome record when storage permits; otherwise the
intent remains recovery evidence. Handlers are restored. Kernel locks release on termination.
SIGKILL/power loss require intent-based recovery, not a signal handler.

| State/phase | Meaning and action |
| --- | --- |
| STARTED / MUTATION_PREPARED | Intent is durable; primary commit has not been established |
| FAILED / MUTATION_NOT_STARTED or MUTATION_PREPARED | This invocation did not attempt primary rename; inspect retained intent before retry |
| INTERRUPTED | Catchable cancellation before primary rename; source/previous destination preserved |
| RECOVERY_REQUIRED / PRIMARY_STATE_COMMIT_ATTEMPTED | Commit may have occurred; never report an ordinary failed mutation |
| RECOVERY_REQUIRED / RECEIPT_PENDING | Primary verified committed, receipt not established |
| RECOVERY_REQUIRED / ROLLBACK_REQUIRED | Resolver verified primary absent; inspect preparation before separately authorized cleanup/retry |
| RECOVERY_REQUIRED / OPERATOR_ADJUDICATION | Evidence missing, changed or contradictory; no automatic repair |
| COMPLETED / OPERATION_COMPLETED | Published identity/content and durable receipt independently verified |

`resolve_publication(..., finalize=False)` inspects stale operations under the
same resource lock without creating files. `finalize=True` is a separate,
explicitly authorized operation that durably acknowledges a verified committed
primary. Repeating finalization re-verifies and fsyncs the primary, existing receipt and
containing directory. Inspection alone reports RECOVERY_REQUIRED even for a
visible valid receipt: cached presence cannot prove an earlier fsync succeeded.
The resolver never deletes or rewrites a target. A new operation after failed
preparation requires review of current state and separately authorized cleanup.
Orphan temporary files created before durable intent require operator review;
no glob-based cleanup is permitted. The library preserves existing violations.

Detection and remediation MUST remain separate. Remediating an existing violation
requires explicit authorization, backup, rollback and evidence. This release
performs none. Do not unlink/relink in place, silently copy over a violation,
or delete the last known-good state in generic cleanup. A new-file publication
has a single filesystem commit boundary; no cross-system atomicity is claimed.
Database/ledger coordination belongs to each peer's versioned intent/finalization
protocol and must satisfy the requirements below before adoption.

## Production-engineering requirements

The schema-backed `production_engineering` member of the same invariant records
the following MUST requirements. They apply to privileged, security-sensitive,
state-changing and publication code. Existing repo-cp distinctions remain:
read-only observations use PASS/UNKNOWN/DRIFT/BLOCKED and never confer action
authority; ordinary utilities retain applicable local rules. There is no new
risk score or competing admission framework. Peers must document applicability,
including non-applicable capabilities, rather than claim unimplemented checks.

### Privilege and execution integrity

- Never execute ignored, generated, untracked, dirty or user-substitutable source with elevated privileges.
- Bind privileged execution to an exact reviewed revision, tracked file set, expected repository identity, clean relevant scope and verified ownership.
- Verify before execution through a trusted launcher or previously installed root-owned entry point; a running program cannot establish trust in its own source.
- Never add global Git safe.directory exceptions; any exception must be command-scoped, exact-path, ownership-checked and end with the command.
- Separate public inspection, preparation, authorization and mutation operations.
- Read-only commands must not write caches, bytecode, lock files or metadata, or change atime through sensitive copies.
- Use least privilege; never grant unrestricted shells, blanket sudo, Docker group/socket access or broader filesystem access for a narrow operation.
- Privileged helpers must expose a fixed documented interface and reject unknown operations or arguments.

### Filesystem and path safety

- Use absolute paths for protected operations; reject empty, relative, ambiguous, traversal-containing or unexpectedly resolved paths.
- Never follow symlinks for protected sources or destinations; use descriptor-relative operations, O_NOFOLLOW and exclusive creation where available.
- Validate opened descriptors with fstat; require expected type, owner, group, mode, device and link count, not only a pathname precheck.
- Fail on changes to inode, device, ownership, size, link count or policy-relevant metadata during an operation.
- Create unpredictable temporary names with secure platform randomness in the destination directory/filesystem, with restrictive permissions at creation.
- Never assume /tmp permits atomic target publication; never use shell globs for protected mutation targets.
- Never recursively mutate before independently validating the exact resolved boundary.

### Durable state and transactions

- Define preconditions, intended mutation, commit point, success evidence, rollback boundary and crash recovery for every state change.
- Never claim atomicity across systems without a shared transaction mechanism.
- Database-plus-filesystem protocols must durably distinguish mutation not started, prepared, primary committed, receipt pending, completed, rollback required and operator adjudication.
- Persist and fsync intent before the irreversible boundary; make completion and recovery idempotent.
- Report explicit indeterminate/recovery-required state when primary commit may have happened; never report an ordinary failed mutation then.
- Every retry must inspect current state and decide safely whether to resume, finalize, roll back or stop; provide a governed stale-operation resolver.
- Use resource-appropriate locking; detect concurrent writers and fail closed; timestamps alone are not identities or concurrency controls.
- Preserve previous valid state until replacement is verified and durably published.
- Version migrations, identify one-way effects, repeat safely where possible and test rollback or forward recovery.

### Signals, cancellation and cleanup

- Handle SIGINT, SIGHUP and SIGTERM where supported; record value-free controlled interruption and release locks.
- Assume SIGKILL, power loss, kernel and storage failure; recovery cannot rely exclusively on handlers.
- Cleanup must preserve the original failure and never falsely claim rollback success.
- Remove temporary artifacts only after revalidating identity and ownership; never delete the last known-good copy in generic cleanup.

### Input and credential handling

- Validate structural and policy requirements before durable mutation wherever possible.
- Treat account identifiers as application-defined opaque values unless a schema proves stronger semantics; reject controls and unsafe encodings, and do not infer email semantics.
- Never put credentials, recovery material or private keys in argv, environment, process listings, URLs, receipts, exceptions, tests or logs.
- Obtain secrets only through an approved trusted prompt or protected descriptor; keep secret/account prompts on the trusted terminal, not stdout.
- Clearly label hidden prompts and announce length/format rules first; bound retries for correctable input mistakes.
- Distinguish cancellation, authentication failure, policy rejection, integrity failure, concurrency conflict and internal failure without exposing values.
- Use established cryptographically secure randomness and library cryptography; never invent cryptographic algorithms or password-hashing formats.
- Use constant-time library comparison for authentication-sensitive fixed-length values where applicable.
- Never use unrestricted pickle or unsafe YAML deserialization; parameterize database operations rather than interpolating credential input.

### Subprocess and shell safety

- Prefer libraries; pass argument arrays, never interpolated shell strings or shell=True for protected operations.
- Privileged subprocesses require absolute executables, verified executable identity/package provenance, a minimal controlled environment and known working directory.
- Set explicit timeouts and bounded output, check return codes, and retain stderr only for redacted private diagnosis.
- Use stable machine-readable interfaces rather than human-output parsing; bound retries to proven repeatable operations.

### Error and status integrity

- Fail closed on unknown authority, schema, ownership, provenance or state; preserve materially distinct outcomes.
- Public errors may be concise; durable private records require value-free categorical causes.
- Public receipts must never contain credentials, usable credential hashes, prompt contents or private paths.
- Broad exceptions must re-raise or map to explicit safe states; never use language assertions for security enforcement.
- Success requires independent postcondition verification, not command exit zero alone.
- STARTED, FAILED, INTERRUPTED, RECOVERY_REQUIRED and COMPLETED have distinct meanings; absent evidence remains UNKNOWN.

### Determinism and reproducibility

- Use stable schemas, ordering, encodings and value types; durable timestamps must be UTC with explicit timezone.
- Inject clocks, randomness, host identity and filesystem boundaries in tests; do not depend on ambient live state.
- Normalize only proven semantic equivalences and document every accepted normalization.
- Bind receipts/transitions to content, policy identity and relevant state, not Git ancestry alone.
- Generated artifacts must record inputs, tool version, schema version and immutable source revision.
- Repeated validation of unchanged input must be semantically identical.
- Audits inspect/classify only; peer validator execution or mutation requires a separately authorized execution lane.

### Dependencies and supply chain

- Pin production dependencies and record authoritative source and integrity; avoid floating branches, mutable tags and unverified downloads.
- Separate acquisition from privileged installation/execution; verify before use and never execute network streams.
- Minimize privileged-helper dependencies; record introduced dependency licenses, provenance and versions.
- Updates require tests, review, rollback instructions and an explicit revision change.

### Tests

- Ordinary tests must not require root, credentials, production mounts, network or live infrastructure; integration tests require separate classification and authorization.
- Use isolated temporary roots with verified identities; never discover/reuse live state and keep cleanup within those roots.
- Normal fixtures use independent copied files; only a bounded negative rejection test may create a hardlink.
- Inject failures at intent write, file copy, hash verification, file fsync, database commit, atomic rename, directory fsync, receipt publication and ledger finalization where applicable.
- Test signals, stale locks/STARTED events, concurrency, partial writes, full filesystem, permission denial, ownership drift, symlinks, hardlinks and cross-filesystem behavior.
- Test recovery with both unchanged and already-committed primary state.
- Skipped or environment-blocked tests are NOT_RUN, never PASS; distinguish implementation, fixture, platform-capability and qualification-environment failures.
- Preserve reproducible failure artifacts only when secret-free; otherwise preserve sanitized metadata and permitted hashes.
- Run focused tests and the complete suite before publication.

### Code quality and maintainability

- Separate policy from transport, prompts, filesystems, databases and presentation; centralize invariants for commands, audits and tests.
- Prefer small functions with explicit inputs and typed outcomes; avoid hidden globals and import-time side effects.
- Imports must not write files, contact networks, mutate environments or perform authority checks.
- Document assumptions next to enforcement; version schemas and reject unsupported versions.
- Compatibility cannot weaken security or falsify state; remove dead compatibility paths after governed migration.
- Comments explain why; public interfaces document stable machine-readable output and exit codes.

### Review and release

- Security-sensitive changes require independent non-author review covering adversarial assumptions, recovery, privilege and failure semantics.
- Publish additively unless history rewriting is explicitly authorized and the affected revision is proven unpublished.
- Identify exact changed files, tests run/not run, limitations, migration effects and rollback procedure.
- Verify local HEAD, upstream tracking and directly queried canonical remote; check before claiming a clean worktree.
- Do not claim peer/live effects without direct evidence; automatic execution stays disabled until the applicable admission authority enables it.

## Peer adoption

1. Through the peer's owner lane, pin the reviewed repo-cp commit containing this
   registry/schema/doctrine and record their digests. Do not change Foundation
   pins or claim a universal Foundation contract update.
2. Declare the governed file set, protected classes, non-governed exclusions and
   mount boundaries. Audit metadata without reading credentials or private
   ceremonies. Record UNKNOWN where capability or evidence is missing.
3. Review workflow source for hardlink APIs, link-based copy flags, snapshots,
   fixture setup, migration and staging dependencies. Replace those dependencies
   with the verified copy sequence; retain exactly bounded rejection tests.
4. Apply the production-engineering requirements by capability and risk. Record
   the trusted launcher, privilege boundary, locks, durable intent, state machine,
   resolver, prompt and subprocess contracts where applicable. A repo-cp library
   import is not privileged source attestation or approval to access credentials.
5. Evaluate existing violations separately. Obtain explicit authorization,
   independent backup, tested rollback/forward recovery and evidence before any
   repair. Neither this publication nor a DRIFT finding authorizes remediation.
6. Run synthetic fault-injection and full owner validation, obtain independent
   review, publish a versioned adoption receipt with exact source revision and
   limitations, then request any applicable admission separately.

No peer repository, credential lifecycle, live host, B70 operation or existing
hardlink is changed by establishing this invariant. Adoption is not automatic.
Rollback is an additive reviewed follow-up commit; already adopted peers must
review compatibility themselves. Never restore prohibited workflow hardlinks
as a routine rollback technique.
