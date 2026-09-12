# ansible-cp owner review required

Review-only proposals for source `4c40a0ef8aaf820dfec4b8562d4f5b39bd89eb86`.
No peer patch, enrollment proposal, execution instruction or approval is supplied.
The [pilot receipt](../acceptance/ansible-cp-pilot.json) fixes the public scope and
hashes. Foundation defines contracts; ansible-cp owns its derived evidence;
Louis retains approval. repo-cp cannot declare compatibility on the owner's behalf.

1. RC008: owner-review the two public B70 JSON handoff records against Foundation
   repository `999fcf6a4bf181bdba201e9ca0c2f2bc4e7e2af5`, preserving separate doctrine
   `d2fe6c6291ea1eaffadb15ded6c0240fed0e96ca`. Determine compatibility from intervening
   history and local revision-handoff requirements before proposing any change.
2. RC010: review those records against auth policy
   `c36ec1e23fcd8ec11818a054374de3a6f64e1d4b` and containing source
   `57815b15533ace72ee3ab2aef82fe3b764925652`. Preserve their distinction. The existing
   auth owner review supports comparison, not automatic downstream adoption.
3. RC004/RC007 UNKNOWN: ask the ansible-cp owner whether version, ownership and
   provenance should have explicit public declarations under existing local policy.
   Do not invent root files or Foundation requirements. Any alternative enrollment
   model needs a separately reviewed local schema change; PILOT nulls cannot enroll.
4. RC009 UNKNOWN: retain offline semantics. Any later freshness assertion requires
   separately scoped direct evidence and an explicit reviewed policy change.

The smallest next gate is Louis's authorization for a repository-only ansible-cp
owner review of RC008 and RC010, preserving unrelated dirty documents and every
live gate. This task has not granted that peer mutation scope.

Any resulting peer patch must cite authority, change only compatible derived
public evidence, preserve policy and live gates, pass that repository's required
checks within their authorized scope, and provide a reviewed follow-up reversal.
Risk: treating a newer pin as automatic policy adoption or confusing a containing
handoff revision with a policy revision. Recovery: retain historical evidence and
revert only approved metadata changes through a follow-up commit, never history
rewriting. After publication, refresh only changed public digests and repeat the
pilot before considering enrollment. No downtime or removals are proposed.
