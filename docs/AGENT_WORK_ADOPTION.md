# Adopt and review the Helix Agent Work Contract

[Release 1.0.0](AGENT_WORK_CONTRACT.md) is repo-cp's flagship agent working
agreement. Its [release record](../pins/agent-work-contract.json) identifies the
exact content. Adoption is an operator-authorized instruction change, separate
from Foundation conformance, repo-cp enrollment and runtime permissions.

## Install a reviewed reference

Read the owning repository's current guidance and preserve it. Add one clearly
marked adoption block to its root AGENTS.md. Name `HELIX_AGENT_WORK_CONTRACT_V1`,
release `1.0.0`, the full canonical repo-cp publication commit, the contract's
path and SHA-256. Link to the immutable commit URL, not only the default branch.
Use a local copy only after verifying its bytes match the adopted release.
If unavailable locally, retrieve that exact source through approved GitHub access.

Require the agent to read the contract and the applicable task-specific documents
before substantive work. Retain the contract's precedence, secret boundaries and
scoped authorization. A missing document is a lookup step, not an automatic
request for the operator to paste it. Never substitute a newer release silently.

Review the exact diff, perform the owning repository's required checks, commit
only authorized guidance, and verify its canonical remote branch. Record the
publication commit and result for each repository. A local change, an inaccessible
remote or a missing remote is not a published adoption. Never create a repository,
change hosting, unarchive a repository or force-push merely to complete rollout.

Root guidance applies within its normal repository scope. Inspect nested agent
instructions when they govern the task; a more-specific file may narrow the
contract but cannot silently relax it. Existing sessions must reread the new
guidance; publishing it does not restart agents or prove enforcement.

## Review the behavior, not a reading claim

| Situation | Required observable response |
| --- | --- |
| Referenced peer document is missing locally | Resolve its canonical owner/path/ref and try an approved targeted read. |
| First attempt fails | Identify the failed assumption; change an input or test a concrete explanation before retrying. |
| Test expectation conflicts with the implementation | Consult the governing requirement; do not loosen acceptance just to pass. |
| Source is uncommitted | Identify the permitted bytes by digest, or explicitly withhold identity for secret material. |
| Operator overrides a rule | Record the instruction, scope and displaced rule/revision within binding boundaries. |
| Agent says committed, pushed, merged or published | Verify that particular state with the corresponding artifact or remote evidence. |
| Agent reports completion | Compare the outcome with the request and inspect limitations and `Live effects:`. |

Use only the rows relevant to the task. A small documentation edit does not need
a ceremonial experiment, and a checklist does not prove comprehension. The
contract's normative rules govern when this guide is abbreviated.

## Maintain the release

Do not change released contract bytes in place under the same release number.
Publish subsequent revisions with their own release identity, digest and change
record. Keep prior commits reachable. Updating peer references is a separately
reviewed adoption change; publishing a release does not update existing pins.

A rollout receipt must distinguish instruction publication from agent behavior,
software deployment and live acceptance. This release adds no hooks or runtime
executor. Proposed automated checks must test observable claims without reading
credentials, private runtime payloads or unrelated repositories.
