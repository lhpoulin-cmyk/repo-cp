# Next exact enrollment approval gate

Status: BLOCKED / NOT APPROVED / NOT APPLIED.
Artifact: [exact registry diff](auth-cp-enrollment.patch).

Prerequisite: auth-cp's owner reviews RC008 (its earlier Foundation repository
handoff pin), retaining distinct doctrine and repository revisions, and records
the compatibility disposition. No peer rewrite is supplied or authorized here.
If that review changes the selected auth-cp revision or any inspected file,
regenerate and retest this proposal before approval. This proposal cannot approve
itself or convert an observer/pilot into authority.

Once the prerequisite is satisfied without invalidating this proposal, the exact
Louis decision is: approve auth-cp alone for repository-only audit at
f84b7292659d6c4b14a4a1f767367343105a0cfa, using the existing seven public files
and their digests in registries/repositories.json, and approve the two-field
enrollment diff. Approval evidence label:
Louis:approve-auth-cp-public-metadata-enrollment-v1.
That string in the proposed patch is a placeholder for the future recorded
decision, not evidence that approval has occurred.

Scope: change auth-cp state PILOT to ENROLLED and record enrollment approval.
Effect: ordinary default audits will include that same bounded public scope.
No new files, peer repositories, privileges or network/live actions are added.
Risks: the audit still reports remote freshness UNKNOWN; V1's unsupported
structured guarantees remain unsupported. Downtime and removals: NONE.

Success: exact reviewed diff, local schema/full tests pass, default audit selects
only auth-cp, and retained evidence identifies Louis's decision. Failure: changed
source, allowlist, digest, unresolved prerequisite or different diff; stop and
prepare a new proposal. Reapplying the patch fails without changes. Reversal is
the inverse two-field diff in a reviewed follow-up commit, returning to PILOT.
Synthetic tests prove apply, rejected repeat without mutation and exact reversal.

Return only the explicit approve/decline decision, this artifact path, source
revision, and the public owner-review evidence reference. Do not return secrets
or operational output. No command execution, patch application, enrollment,
credential issuance/adoption or live mutation has occurred through this gate.
