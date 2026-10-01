# repo-cp agent guidance

Claude and Codex must apply [shared checkout rules](docs/AGENT_CHECKOUT_RULES.md).
Both may idempotently create private, isolated task checkouts inside this
repository under `.agent-checkouts/<agent>/<task>/`, within sandbox permissions.
This authorization covers development setup, not runtime or live actions.

Apply parent Helix instructions and HELIX_AGENT_EXECUTION_DOCTRINE_V1. Louis
retains approval, merge, exception and ultimate authority. Foundation defines
universal contracts and conformance. repo-cp inventories declarations, audits
public repository evidence and produces review artifacts. Each domain repository
retains desired state. Observation and implementation never confer ownership.
Do not create virtualization-cp or infer an unpublished target-facet contract.

Read README.md, OWNERSHIP.md, PROVENANCE.md, VERSION, both Foundation pins,
docs/acceptance/operator-action-v1.md, docs/OPERATIONS.md and applicable tests.
Historical docs/handoffs records remain evidence, not current acceptance.
Verify path, branch, HEAD, status, origin, upstream, history and direct canonical
remote parity before edits/publication. Preserve unrelated work and continue
in-scope repairs. Peer enrollment and modifications require separate scope.

Use reviewed public metadata allowlists only. Never read credential stores,
secret-bearing environments, private material or live dumps. Runtime CLI must
not spawn processes, execute actions or peer validators, discover arbitrary
files, elevate, contact networks, or write repositories. Test runners may run
local synthetic tests only. Never print suspected secret values. Indicator
scans are heuristics, not proof that arbitrary content is secret-free.

Keep the 19 accepted Foundation artifacts byte-identical. Independently verify
canonical pins, digests, compatibility and tests before updates. Never take pins
from a declaration or bypass failed integrity checks. Preserve distinct
repository and doctrine content revisions. V1 rendering is neither authorization
nor execution. Do not extend its schema; route universal changes to Foundation.

Enrollment is separate from bootstrap/pilot acceptance. Default audits select
ENROLLED entries only; --pilot adds explicitly schema-approved PILOT entries. Local metadata
readiness checks are not a new universal Foundation standard. Do not rewrite
peer pins merely to pass. Preserve UNKNOWN and DRIFT findings. Proposals are
stdout-only review artifacts; no patch is supplied without a safe approved scope.

Run tools/validate, focused tests, syntax and secret checks, git diff --check,
and inspect the complete diff before cohesive commits. Publish only when
authorized to verified canonical repo-cp. Never self-merge, rewrite history or
use destructive Git operations. Prove local/upstream/direct-remote parity.
Report exact tests, pins, enrollment, limitations and NONE for absent live effects.

<!-- BEGIN HELIX_GITHUB_REFERENCE_FALLBACK -->
## Missing local references: canonical GitHub fallback

For authorized work, a missing local peer checkout or referenced file is a
lookup step, not by itself a blocker. Follow explicit repository/file URLs in
the task, handoffs, README, ownership/provenance records and repository registry;
use the owning repository's verified GitHub remote when a relative link or
local path is unavailable. Do not guess repository identity from a host name
or assume every peer is hosted on GitHub.

Check the exact referenced path and revision first through the available GitHub
connector/API or other already-authorized read-only access. Prefer targeted
file/tree/history reads over cloning or broad searches. If the file moved or
is absent at that revision, inspect the owning repository's default branch and
path history; distinguish historical evidence from current governing material.
Cite the canonical URL, exact source commit and path for findings. Preserve
pinned revisions and report local/remote differences; never silently substitute
a newer document for a pinned contract or rewrite pins to make checks pass.

Do not ask the operator to paste a document or grant permission again when
existing authorized access can retrieve it. For private repositories, use the
existing approved connection; do not inspect credentials, change identity,
expand access, or disclose private content across trust boundaries. Treat 403/404
as potentially denied access, not proof the repository/file does not exist.
If permitted routes fail, report the exact repository/path/ref, methods tried
and access or absence result, and continue independent work.

This is development-agent read-only reference discovery. It grants no peer
write, publication, enrollment, runtime execution or live-mutation authority;
existing secret restrictions and runtime CLI network prohibitions still apply.
<!-- END HELIX_GITHUB_REFERENCE_FALLBACK -->

<!-- BEGIN HELIX_AGENT_WORK_CONTRACT -->
## Required Helix agent work contract

Before substantive work, read and apply
[HELIX_AGENT_WORK_CONTRACT_V1, release 1.0.0](https://github.com/lhpoulin-cmyk/repo-cp/blob/4ede9b73501b38a2b0ba5a50c9c32875a2d0eb19/docs/AGENT_WORK_CONTRACT.md).
Source commit: `4ede9b73501b38a2b0ba5a50c9c32875a2d0eb19`.
Content SHA-256: `a4838c4bfd8e1d27ed794c48ca1d475d76929309fabc212368234c4073df7674`.
Use a local copy only when its bytes match this pin; otherwise retrieve the exact
canonical source through existing authorized GitHub access. Do not substitute a
newer revision silently or ask the operator to paste accessible documentation.
Read the governing task-specific documents, record source identity, test failed
assumptions with bounded experiments, and complete supported remedies in scope.
Follow the contract's precedence and acceptance rules. Report scoped evidence,
actual delivery stage and `Live effects:` including remote writes. This adoption
changes agent working instructions, not peer ownership, credentials, enrollment
or live authority. Existing stricter safety and secret boundaries remain in force.
<!-- END HELIX_AGENT_WORK_CONTRACT -->
