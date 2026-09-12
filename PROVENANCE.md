# Provenance

Initial repo-cp: `2f309d732d34344930cd895ba0584bb154a6c6da`. Original blocked
handoff: `a6f9134c9ddad39244810cacd96fb79a12bec36d`. Its docs/handoffs files
remain unchanged historical evidence.

Louis supplied Foundation repository revision
`999fcf6a4bf181bdba201e9ca0c2f2bc4e7e2af5` and separate doctrine revision
`d2fe6c6291ea1eaffadb15ded6c0240fed0e96ca`, authorized consumption and the
repository-only auth-cp pilot, and retained the unresolved target-facet dependency.
The 19 vendor/foundation files are exact public Git artifacts from that commit:
guidance, doctrine, contract, schema, registry, implementation, CLI, tests and
fixtures. This is a consumer snapshot, not a new Foundation authority. Upstream
Markdown links beyond the selected snapshot resolve in canonical Foundation;
upstream prose and code are not rewritten.

[Acceptance](docs/acceptance/operator-action-v1.md) records immutable pins,
digests and compatibility. The [pilot](docs/acceptance/auth-cp-pilot.md) separates
public repository observations, synthetic rendering, enrollment and live state.
No credentials, private keys or runtime state were imported. jsonschema 4.23.0
is the reference dependency; PyYAML checks local CI YAML syntax only.
