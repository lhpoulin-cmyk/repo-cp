# File-integrity and production-engineering acceptance

INVARIANT=HELIX_NO_HARDLINKS_V1
INVARIANT_VERSION=1.0.0
BASE_REVISION=26158ec19b4fcb62662edd425048d0f5a06ddf9d
AUTOMATIC_EXECUTION=DISABLED
LIVE_MUTATION=NONE
PEER_MODIFICATIONS=NONE
EXISTING_HARDLINK_REMEDIATION=NONE

Louis explicitly requested canonical fleet-wide prohibition of workflow hardlinks
and the accompanying production-engineering requirements, implemented and
published in repo-cp only. The [doctrine and adoption instructions](../FILE_INTEGRITY.md),
[registry](../../registries/file-integrity.json) and
[schema](../../schemas/file-integrity-v1.schema.json) are the canonical review
artifacts. The source identity is the Git commit containing this acceptance;
the immutable base above records its input revision, not a self-referential pin.

## Scope and qualification

The existing RC audit/report conventions now include RC011. Protected multi-link
files BLOCK; ordinary workflow/fixture multi-link files DRIFT; missing metadata
is UNKNOWN; symlinks/nonregular inputs BLOCK with distinct reasons. Explicit
exclusions are not scanned. Aggregate precedence and enrollment are unchanged.
The local scanner is metadata-only. Peer audit uses only existing public file
allowlists; no actual peer audit or B70 operation was run for this acceptance.

The public/synthetic publication reference uses Linux descriptor-relative opens,
no-follow checks, single-link enforcement, exact metadata and SHA-256/byte-count
verification, destination-local exclusive temporary files, atomic no-replace
rename, file/directory fsync, immutable intent and content-bound provenance
receipts, directory locks, controlled catchable signals and explicit recovery.
It rejects root/set-ID execution. No runtime CLI imports or invokes publication.
Existing destinations and violations are preserved. No credentials are handled.

Validation commands:

- `python3 -B -m unittest discover -s tests -p test_hardlink_policy.py -v`:
  51 focused tests, no skips.
- `./tools/validate`: full canonical suite, 103 tests (13 unchanged Foundation
  reference tests plus 90 repo-cp tests), including focused qualification;
  metadata/data, schema, Python/JSON/YAML syntax, public Markdown links,
  secret-indicator heuristics, deterministic local RC011 audit and diff checks.
- The working tree also contains two preexisting, uncommitted checkout-scope
  tests: the complete working-tree suite has 105 tests. They remain outside this
  publication and pass with the updated validator.
- `python3 -B tools/audit-hardlinks` twice: identical scoped JSON, PASS.
- `./tools/repo-cp validate`: accepted Foundation bytes, enrollment and invariant
  schema PASS; no peer execution or network access.
- `git diff --check` and complete staged-diff review before commit/publication.

The focused suite covers compliant protected/workflow files; modeled multi-link
metadata; one actual bounded hardlink rejection test; symlinks and FIFOs;
missing/denied metadata; exclusions before traversal (including same-device and
other-device mounts); no-atime reads; schema weakening; existing RC011 audit and
proposal integration; independent copies; owner/group/mode/device/size/hash
expectations; root rejection; partial writes; full-filesystem and permission
faults; all six applicable fsync boundaries; intent/copy/hash/rename/receipt
failure; ambiguous commit outcomes on both sides; concurrent publication and
stale kernel locks; directory/source substitution and metadata drift; stale
intent resolution; repeated finalization; cleanup failure preservation;
SIGINT/SIGHUP/SIGTERM in bounded subprocesses; and actual different-filesystem
copy between permitted synthetic roots. Exactly one test creates a hardlink,
only to prove rejection, with both names inside its verified temporary root.

Independent non-author agent review examined adversarial directory substitution,
mount exclusions, no-clobber publication, root/capability boundaries, metadata
races, cleanup, signal outcomes, provenance and receipt durability. Findings were
fixed and re-reviewed. Final disposition: APPROVED within the documented
unprivileged public-artifact/cooperating-writer scope. The reviewer independently
ran all 51 focused tests with no skips and checked whitespace.

## Limits, migration and recovery

No new dependency was introduced. Existing pinned requirements and all 19
Foundation artifact bytes are unchanged. Foundation repository pin remains
`999fcf6a4bf181bdba201e9ca0c2f2bc4e7e2af5`; separate doctrine content pin remains
`d2fe6c6291ea1eaffadb15ded6c0240fed0e96ca`. auth-cp and ansible-cp remain ENROLLED;
Foundation remains DISCOVERED. No peer declaration, pin or enrollment changed.

NOT_APPLICABLE / NOT_RUN: database commit and ledger finalization fault injection,
credential prompts, privileged installed launchers, production mounts, live
hosts and peer integration: repo-cp implements none of these execution lanes.
Their MUST requirements are published for owning peers to implement and qualify.
Physical power loss, kernel failure and SIGKILL during storage I/O were not
induced. Interrupted/stale state and failed durability boundaries were tested
synthetically; this is not hardware or storage-firmware qualification.
No skipped test is counted as PASS.

This Linux reference requires O_PATH/O_NOFOLLOW/O_NOATIME, flock, fsync and
renameat2(RENAME_NOREPLACE); unavailable capability fails closed. It does not
protect against malicious root or a malicious process sharing the trusted UID.
Public artifact digests and caller-supplied reviewed revision are provenance
inputs, not proof that running source has attested itself. Privileged use needs
an independently trusted launcher and separate authority; this library refuses it.

Inspection-only recovery cannot infer durable completion from a visible receipt;
it reports RECOVERY_REQUIRED. Explicit finalization verifies state and repeats
the file/directory durability barriers. No automatic rollback, replacement or
violation cleanup exists. Existing-violation remediation requires separately
authorized backup, rollback and evidence. Orphan preparation files require owner
review. Rollback of this repository change is an additive reviewed follow-up;
peer adoption and migrations follow each owner's authority lane.

The preexisting AGENTS.md, README.md, .gitignore, CLAUDE.md,
docs/AGENT_CHECKOUT_RULES.md and tests/test_validation_scope.py are preserved
byte-for-byte and excluded from this commit. The validator is the sole overlap:
its prior private-checkout pruning is retained and extended to the canonical
exclusions. Parent guidance and every peer repository remain untouched.
