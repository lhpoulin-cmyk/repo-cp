# foundation-cp agent guidance

`foundation-cp` is the canonical Helix-ARPA cryptographic trust and
continuity-contract repository. It defines Foundation doctrine, schemas,
contracts, trust boundaries, cryptographic profiles, compatibility, recovery
requirements and conformance.

The authority order is:

```text
local operator authority > auth-cp > automation consumers > managed environments
```

Foundation supports this order. It is not a second identity authority,
consumer desired-state repository or general secret service.

## Current authority boundary

`auth-cp` owns identity lifecycle, authorization, encrypted operational
credential custody, registry, controlled export or lease, reconciliation,
rotation, revocation and recovery authorization.

Foundation retains cryptographic trust doctrine, CA custody policy,
recipient/recovery trust requirements, public trust records and its existing
bounded signer mechanics. Those mechanics may act only from a valid, exact,
one-time auth-cp authorization. Repository presence, custody or a consumer
request never authorizes issuance.

Private keys, SOPS or age decryption identities, encrypted custody packages,
mutable runtime databases, signing credentials and plaintext secret material
must not be committed here.

## Read this before working

Read, in order:

1. the applicable parent portfolio `AGENTS.md`;
2. `README.md`;
3. `OWNERSHIP.md`;
4. `PROVENANCE.md`;
5. `VERSION`;
6. `docs/ACTIVE_DOCTRINE.md`;
7. `registries/active-doctrine.json`;
8. applicable policy, contract, schema and target-specific validation records;
9. `tools/validate` and the relevant repository-native tests.

The active consolidated doctrine and its registry take precedence over older
general or prepared prose. Do not silently reinterpret historical text. If a
conflict would change authority, custody, compatibility, issuance or recovery,
stop with the exact conflict.

## Version and supersession

Version `1.0.0` is the first explicit semantic version of the consolidated
Foundation doctrine. Earlier `schema_version: 1` and `*-v1` names are data
or interface versions, not proof of a previous semantic release.

Preserve Git history. Do not create a competing active Foundation, doctrine,
allocator or recovery authority. A major-version change requires an explicit
baseline, supersession record and compatibility statement.

## Signer and ledger invariants

The checked-in signer configuration remains disabled by default. Repository
validation does not prove installation, activation, current custody or live
capability.

Preserve the existing single monotonic serial allocator, epoch, consumed
authorizations and issuance history. Never reset, fork, time-seed or reuse a
serial. Gaps after interruption are allowed. Passive recovery state must not
become an active second allocator without separately authorized promotion.

Every adapter capability is `implemented`, `unsupported` or `unverified`.
Synthetic tests and generic interfaces do not prove production support.

## Integrity and recovery

SOPS YAML with age recipients is the selected encrypted representation for new
auth-cp custody. Encryption is not authorization and authenticated decryption
does not prove freshness.

Before decryption or use, `reauth` must verify the independently pinned
manifest authentication key, canonical manifest, bundle identity, purpose,
ciphertext digest, monotonic generation and independent high-water evidence.
Rollback, same-generation substitution, missing independent state or replica
conflict fails closed.

Foundation records the recovery contract. Platform mount/unlock realization
belongs to the applicable consumer, and encrypted operational bundle custody
belongs to auth-cp. No GitHub workflow, USB, workstation, signer or live
recovery behavior is proven merely by repository tests.

## B70 boundary

The B70 observer work remains preparation only. No dedicated B70 credential is
issued, adopted, accepted or installed by doctrine publication. The shared
fleet observer credential remains excluded. No guest staging, SSH reload,
Semaphore credential, live template or APPLY is authorized.

The reserved acknowledgement does not open a gate:

```text
APPLY B70_ENCODE_MATRIX_OBSERVER_ADMISSION b70-encode-matrix
```

Issuance or adoption, installer rehearsal, staging, and APPLY each require
their own later authorization and exact revision revalidation.

## Working rules

Before mutation, recheck repository path, branch, HEAD, remote, upstream
parity, status, history, version and applicable authority. Classify dirty and
untracked state; preserve unrelated work.

Use safe public metadata and opaque references only. Do not read private-key
content, raw secret-bearing environments, custody payloads or full live dumps.
Synthetic credentials belong only in isolated temporary locations and must be
removed by the test fixture.

Foundation repository work does not authorize edits to auth-cp, ansible-cp,
another peer repository, removable media or a live host. Commit peer
repositories separately.

Make the smallest coherent change. Keep doctrine, ownership, provenance,
version, registries, schemas, contracts, validators and compatibility aligned.
Do not weaken validation to obtain a pass.

## Validation and publication

Before committing or pushing, run:

```text
tools/validate
```

Also run applicable syntax checks, the relevant focused tests, a
private-material indicator scan and `git diff --check`. Inspect the complete
diff and preserve unrelated changes.

Push only to the verified canonical remote and prove local/remote parity.
Report repository evidence separately from live evidence. Use `NONE` for
live observations, mutations, issuance, adoption or secret access when none
occurred. Never claim recovery, revocation, installation or live capability
beyond direct evidence.

## Universal execution profile contract

Read `docs/EXECUTION_PROFILES.md`, `registries/execution-profiles.json`, its
versioned schema and `src/execution_profiles.py` before editing execution
semantics. Foundation defines profiles; auth-cp binds principals/accounts,
credentials and grants. Contracts and declaration checks do not activate
adapters or accounts. Historical observer sudo helpers do not satisfy the
new observer no-elevation contract. Preserve existing signer, ledger and
independent reauth boundaries. Run the execution-profile negative tests with
repository validation; profile names never confer custody authorization.
