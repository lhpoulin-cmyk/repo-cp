# repo-cp — The Helix Agent Work Contract

`repo-cp` means **repository governance control plane**. Read
[Helix Control Plane: purpose and naming](docs/HELIX_CONTROL_PLANE.md) for the
architecture, the `-cp` convention and the role of human judgment in automation.

## Flagship: disciplined autonomy with evidence

The [Helix Agent Work Contract](docs/AGENT_WORK_CONTRACT.md) is repo-cp's
flagship work: the operator's shared standard for agents that read the right
documentation, investigate intelligently, finish authorized work, and report
exactly what their evidence supports.

**Read the source. Test the assumption. Complete the work. Prove the claim.**

The contract turns those expectations into reviewable obligations: explicit
precedence, source revision identity, bounded experiments, no weakened tests,
scoped PASS claims, witnessed overrides, and verified delivery stages. It makes
initiative accountable without granting new credentials, peer ownership or live
authority. A document cannot guarantee judgment; reviewers assess the work and
its evidence, not a claim that the agent read the rules.

- [Read the contract — release 1.0.0](docs/AGENT_WORK_CONTRACT.md).
- [Review the 1.1.0 candidate — GitHub procedures, staging and commit framing](docs/AGENT_WORK_CONTRACT_CANDIDATE.md#7-make-github-work-deliberate-and-reviewable).
- [Repository voice guide](docs/REPOSITORY_VOICE.md).
- [Adopt it and review a task](docs/AGENT_WORK_ADOPTION.md).
- [Verify the published content digest](pins/agent-work-contract.json).

Repository guidance must reference an exact released revision. Adoption means
an instruction was installed; it does not prove that every agent complies or
that an already-running session has reloaded it. Publication receipts distinguish
verified adoption from pending or inaccessible repositories.

## Repository governance and audit tools

repo-cp inventories the Helix-ARPA repository fleet, checks declared public
metadata, reports drift and prepares review artifacts. Foundation defines
universal conformance; domain repositories retain authority; Louis retains
approval, merge, enrollment and exception decisions.

Version 0.1.0 implements the published Foundation operator-action V1 consumer.
The missing-contract blocker is closed by
[verified acceptance](docs/acceptance/operator-action-v1.md). Original
[handoff evidence](docs/handoffs/foundation-operator-action.md) is preserved.
The target-facet contract remains unresolved in
[Foundation requests](docs/FOUNDATION_REQUESTS.md).

## Read-only interfaces

Requires Python 3.11+ on Linux and requirements.txt dependencies. Provision
those separately, then use:

```sh
./tools/validate
./tools/repo-cp validate
./tools/repo-cp inventory
./tools/repo-cp audit
./tools/repo-cp audit --pilot --text
./tools/repo-cp drift --pilot
./tools/repo-cp propose --pilot
./tools/repo-cp render < tests/fixtures/auth-cp/blocked.json
./tools/repo-cp render < tests/fixtures/auth-cp/ready.json
```

The CLI never executes a declaration or peer tool, elevates, accesses credential
stores, contacts a network or writes files. Reports/proposals go to stdout; an
operator may capture a reviewed artifact. tools/validate separately runs local
synthetic tests and metadata checks, without auditing or executing peers.
Use `--fleet-root /absolute/fleet/path` for a local checkout parent. Unsupported
Git layouts report UNKNOWN, without subprocess or credential fallback.

Rendering verifies accepted Foundation bytes before using its exact parser,
validator and renderer. BLOCKED has no command. READY_FOR_REVIEW displays one
exact copyable command and all Foundation evidence, impact and recovery labels,
ending with EXECUTION_OCCURRED: NO and MUTATION_AUTHORIZED: NO. Rendering is
not approval, readiness, execution or live acceptance. Invalid input returns
exit 2, empty stdout and fixed non-disclosing stderr, without partial commands.

`validate` checks contract integrity and enrollment structure, not fleet health.
Audit/drift return 0 for PASS, 1 for DRIFT or UNKNOWN, and 2 for BLOCKED/invalid
input. PASS applies only to each named property; NOT_APPLICABLE records
unselected scope. RC001 through RC010 are stable check IDs. JSON and human
reports express the same findings.

## Pilot and limits

Three peers are inventoried: **auth-cp and ansible-cp are ENROLLED**; Foundation
remains DISCOVERED. auth-cp retains its seven-file scope at
3bdcde14bb7c0d77775cfeb2d1bd5571488d6f2a. ansible-cp has ten reviewed metadata files
at 554a8509d0b7b30d6e641ac80a15ba2bf22c4b55 under Louis's
[verified enrollment approval](docs/acceptance/ansible-cp-enrollment.md).
The [B70 auth identity refresh](docs/acceptance/b70-auth-identity-refresh.md)
updates auth-cp only. Default audits select both and retain any ansible-cp derived
auth-pin drift until its owner revalidates. RC009 remains UNKNOWN for each;
consult the current audit rather than historical aggregate counts. Earlier pilot
reports and proposals remain historical evidence, not current fleet state.

Only allowlisted metadata and Git HEAD/ref files are read. Unrelated dirty files
and custody payloads are outside the audit. Secret indicators suppress values
but cannot prove arbitrary text secret-free. Submit only reviewed public action
declarations. Local metadata checks describe enrollment readiness, not invented
universal Foundation policy or semantic proof of domain conformance.

V1 does not machine-enforce unique gate IDs, operation classes, action-artifact
checksums, authentication methods, secret-handling policy or expiration and
invalidation conditions. Accepted-code digests do not add those fields to V1.
See [compatibility requests](docs/FOUNDATION_REQUESTS.md).

Read [ownership](OWNERSHIP.md), [provenance](PROVENANCE.md),
[working rules](AGENTS.md) and [operations](docs/OPERATIONS.md) before changes.

The [historical ansible-cp pilot](docs/acceptance/ansible-cp-pilot.md) preserves
the original drift and missing metadata findings. The owner remediation and
independent enrollment review close those findings in the accepted scope.
`./tools/repo-cp audit --repository ansible-cp` selects the enrolled repository.
