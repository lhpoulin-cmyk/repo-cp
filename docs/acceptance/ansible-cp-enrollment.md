# ansible-cp enrollment approval and application

Louis explicitly authorized the pilot refresh and conditional enrollment at
`554a8509d0b7b30d6e641ac80a15ba2bf22c4b55`, replacing the pilot pin
`4c40a0ef8aaf820dfec4b8562d4f5b39bd89eb86`. Approval evidence label:
`Louis:approve-ansible-cp-public-metadata-enrollment-554a850`.
The [machine approval receipt](ansible-cp-enrollment.json) records the decision,
scope, verification conditions, source evidence digest and preserved peer state.

## Independent verification before enrollment

repo-cp main was 9a40b40cadb4c495ea9731b67417e078edf0a69e with clean worktree
and direct canonical remote parity. ansible-cp local/upstream/direct remote
HEAD and main matched 554a8509d0b7b30d6e641ac80a15ba2bf22c4b55.
All ten reviewed file digests matched committed and checkout bytes. The B70
handoff matches the exact published auth-cp handoff; operational paths have no
delta from the pilot source. The committed owner remediation evidence was read
and hashed independently; no peer validator was executed for enrollment.

Two independent audits with a temporary refreshed nine-file PILOT registry
reproduced 35 PASS, 1 UNKNOWN, 0 DRIFT, 0 BLOCKED, 0 NOT_APPLICABLE. Both SHA-256:
`cf0e4265c15ac206b74555eacfa88642a9a8ec759842419e91748734eb3e8cb7`.
[Verified pre-enrollment audit](ansible-cp-pre-enrollment-audit.json) preserves
that exact output. This satisfied Louis's conditional authorization before the
canonical registry changed. Prior pilot reports remain historical evidence.

## Enrolled public metadata scope

| File | SHA-256 |
| --- | --- |
| AGENTS.md | 9cd4a451f53c408f88e77d7b07253d4fcdc61af159b79cc9cd3613c17c0506cc |
| OWNERSHIP.md | a03955b6a1ffe898be2b5cac3faa55daa8d62cd4d355d524a55b21ce28b5b9d6 |
| PROVENANCE.md | 5b043ef4731f167361dd41f44db6065be8b107e2c74f5c3f4c95f5b39c394a3c |
| README.md | b856f2b56f3ace3db29a6d4cabe3a05f2d1421e430345ab8da9b2c7dd42a41aa |
| VERSION | e9dd8507f4bf0c6f42458e41aea833ad0bd3f6127272335eee9bf4d58541ed67 |
| contracts/linux-guest-admission/b70-doctrine-reconciliation.json | cde851f6fd46bb6c8ab58c2dc0accc5c399807d807be346af2d433fe74d73c06 |
| contracts/linux-guest-admission/b70-revision-handoff.json | a78b763e57a29b38f5e85e8ff2143bac31952a26218b974b8d24930824870f29 |
| docs/AUTHORITY.md | a6d31c3299d2954eaf75ad5741e385d31dde405fca642f1e9ef74d39690ea064 |
| scripts/validate | cfa541d5b3e7bc7a49a4d0722ef770b2c9853f83383efb390d5ea77abdaef8b1 |
| tools/validate | bede2dd70c5c3a5216a6a66ed198735e35ab31e231ad78dd4645ff89a2964f55 |

The ten-file scope adds the reviewed tools/validate alias to the nine-file
verification pilot. Its three presence/digest/indicator checks explain the final
ansible-cp result: 38 PASS, 1 UNKNOWN, no DRIFT or BLOCKED. The alias is metadata,
never executed by the runtime audit. RC009 remains explicitly UNKNOWN and is
accepted only as a non-blocking enrollment limitation; audit overall remains
UNKNOWN. No exception suppresses the finding or converts it to PASS.

[Enrolled audit](ansible-cp-enrolled-audit.json) and
[fleet audit](fleet-after-ansible-enrollment.json) were each repeated identically.
Default fleet scope is auth-cp plus ansible-cp: 63 PASS, 2 UNKNOWN, no DRIFT or
BLOCKED. Both UNKNOWN findings are RC009. Foundation stays DISCOVERED.

## Effects and recovery

Only repo-cp enrollment metadata, evidence, documentation and isolated test
fixtures changed. No peer repository changed; unrelated ansible-cp dirty documents
and peer untracked documents were preserved. No target admission, target-facet
ownership, desired state, credential grant or APPLY authority follows enrollment.
Foundation repository and doctrine pins remain unchanged and distinct.
Reversal requires a reviewed follow-up restoring PILOT, its nine-file scope and
null enrollment authorization while retaining this receipt as history.

ENROLLMENT_APPLIED=YES
AUTOMATIC_EXECUTION=DISABLED
LIVE_OBSERVATION=NONE
LIVE_MUTATION=NONE
PEER_MUTATION=NONE
SECRET_ACCESS=NONE

## Validation

Full tools/validate suite: 52 tests passed (13 Foundation, 39 repo-cp).
Focused audit/pilot suite: 26 tests passed. Metadata checks passed for 77 files,
28 JSON documents, 12 Python syntax checks, 2 schemas and 1 YAML document;
secret-indicator findings: zero. git diff --check and complete diff review passed.
The machine receipt includes final audit digests and unchanged-peer verification.
