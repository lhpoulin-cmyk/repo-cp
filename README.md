# Repository fleet governance

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
57815b15533ace72ee3ab2aef82fe3b764925652. ansible-cp has ten reviewed metadata files
at 554a8509d0b7b30d6e641ac80a15ba2bf22c4b55 under Louis's
[verified enrollment approval](docs/acceptance/ansible-cp-enrollment.md).
Default audits select both: 63 PASS, 2 UNKNOWN, no DRIFT/BLOCKED. RC009 remains
UNKNOWN for each repository; overall status remains UNKNOWN. Earlier pilot
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
