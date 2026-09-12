# Applied proposal: historical approval input

Louis approved and this exact patch was applied on 2026-09-12. See the
[current enrollment receipt](../acceptance/auth-cp-enrollment.md). The text below
is retained as the pre-application proposal, not a pending gate.

# Current auth-cp enrollment approval gate

Status: READY FOR LOUIS REVIEW / NOT APPROVED / NOT APPLIED.
This is a repository enrollment proposal, not an operator-action V1 authorization.

[Exact patch](auth-cp-enrollment.patch) SHA-256:
`77e57867db027c848a11e4a3d5191e37c23b4ff7ea5d1dfb96661c87c0dafc30`.
Source auth-cp main: `57815b15533ace72ee3ab2aef82fe3b764925652`.
Preserved policy revision: `c36ec1e23fcd8ec11818a054374de3a6f64e1d4b`.
[Owner review](../acceptance/rc008-owner-review.json): COMPATIBLE, committed at
`57815b15533ace72ee3ab2aef82fe3b764925652`. RC008 now passes.

This supersedes the proposal and gate at the same paths in repo-cp commit
`904a5fd08b26465dd33ea3dea2e5859c04c789c6`, which were tied to
`f84b7292659d6c4b14a4a1f767367343105a0cfa`. Those original bytes remain in Git history and are historical only.
The current proposal uses the new revision and digest set below. The old
approval label cannot approve this replacement proposal.

## Exact decision

> Approve repository-only enrollment of auth-cp at 57815b15533ace72ee3ab2aef82fe3b764925652 for only the seven public metadata files and SHA-256 digests in docs/proposals/auth-cp-enrollment.md, applying its two-field enrollment patch; acknowledge RC009 remains UNKNOWN.

Proposed approval evidence label: `Louis:approve-auth-cp-public-metadata-enrollment-57815b1`.
The label occurs only in this unapplied proposal. It is not evidence of approval;
registries/repositories.json retains state PILOT and enrollment_authorization null.
A later authorized application must preserve Louis's actual decision evidence.

## Reviewed public scope

Canonical repository: `git@github.com:lhpoulin-cmyk/auth-cp.git`, branch `main`.
No peer file is modified, executed or enrolled beyond the public audit scope.

| Public file | SHA-256 |
| --- | --- |
| `AGENTS.md` | `1faf6a118006608095c97a27d631d3415907d301c53e538bfe1e6f37279e8db9` |
| `OWNERSHIP.md` | `71ca5d5802f3e7322661cc7fff6abb5e44b4919b1789b00245c1258e38b07b46` |
| `PROVENANCE.md` | `82de165bb1d43a6a631a574c281df074a3f519ebec2b72d17bc79ea48dc8a37f` |
| `README.md` | `f797a5877fe60c35b3f291995c31aebe2965344ce0114f503f994172ad196711` |
| `VERSION` | `59854984853104df5c353e2f681a15fc7924742f9a2e468c29af248dce45ce03` |
| `registries/b70-revision-handoff.json` | `a78b763e57a29b38f5e85e8ff2143bac31952a26218b974b8d24930824870f29` |
| `tools/validate` | `117a13971af854d9ecb120efd35da2cbc288589e71fab0f3ab0f7c38574045a4` |

## Effect, limits and reversal

Effect: only auth-cp changes PILOT to ENROLLED in the local registry and records
Louis's approval reference. Default audits then inspect this same seven-file
scope and local Git HEAD/ref metadata. No new authority, execution, credential,
network access or target admission is added. Foundation/ansible-cp remain DISCOVERED.

Remaining result: RC009 UNKNOWN (offline remote freshness). The separate direct
remote check during this refresh is point-in-time preflight evidence and is not
incorporated into the audit contract. RC001 through RC008 pass. Overall UNKNOWN:
26 PASS, 0 DRIFT, 0 BLOCKED, 1 UNKNOWN, 0 NOT_APPLICABLE.

Risks: future peer commits or file changes invalidate this selected evidence;
remote freshness is not continuously proven; V1's unsupported structured
properties and target-facet contract remain unresolved. Reverify canonical
revision, exact digests, owner evidence and this patch before any later approval
or application. Changed inputs require regenerating and reviewing the proposal.
Downtime, removals and live effects: NONE.

Success: recorded actual Louis approval, exact reviewed two-field diff, passing
local suite and default audit selecting auth-cp only with UNKNOWN retained.
Failure: missing approval, changed evidence, broader diff, or validation failure;
leave PILOT intact and prepare a corrected proposal. Repeated patch application
must reject without further changes. Reversal: inverse two-field diff in a
reviewed follow-up commit returns to PILOT with approval reference null; retain
historical decision evidence. Existing isolated tests prove apply, rejected repeat,
and exact reversal. No enrollment patch is applied to this repository here.

Return the explicit approve/decline decision, source revision, proposal path and
public approval evidence reference only. No credentials or operational output.
