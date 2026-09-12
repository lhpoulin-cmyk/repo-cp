# Active Foundation and encrypted credential custody

Operator decision recorded 2026-09-11. Repository architecture is authorized;
credential issuance, adoption, live recovery and deployment remain closed.

## Canonical decision and version

Canonical Foundation implementation: `/home/louis/helix-arpa/foundation-cp`,
branch `main`, baseline `24446a9627f222e3441bdf09bf9518dd924d5341`.
Its OWNERSHIP, trust policy, signer contracts and history beginning at
`ac6fb24` establish the implementation consumed by auth-cp. The legacy
`helix-arpa-private/projects/foundation` describes an *intended* local-only
continuity governance repository, not an activated competing implementation.
Its sibling source checkout is retained history. `helix-pki` is absent at its
recorded path and explicitly historical in Foundation PROVENANCE. None is
promoted, migrated or published by this decision. Foundation USB denotes a
custody medium, not a Git repository or new authority.

Exactly one active doctrine is recorded in
`../registries/active-doctrine.json`. Version `1.0.0` is the first explicit
semantic version of this consolidated doctrine, replacing the unversioned
baseline above. Neither repository previously had a VERSION file or release
tag; `schema_version: 1` and existing `*-v1` contracts are data/interface
versions, not evidence of a previous major release. There is no major bump.
Existing v1 request/authorization/public-key formats, CA fingerprint, fixed
PT8H and separate PT72H profiles, single allocator and passive recovery
semantics remain compatible. This version does not activate a runtime.

Auth-cp owns encrypted operational credential custody and lifecycle. Foundation
retains continuity and cryptographic trust doctrine, CA custody policy,
recipient/recovery trust requirements, and existing bounded signer mechanics.
Neither Git repository becomes a plaintext vault or another secret service.
Protected media/runtime realization is separate from policy ownership.
Existing workstation-specific keys stay local; no historical credential is
moved, re-encrypted, reclassified as B70, or newly adopted by this decision.

## Selected custody architecture

New custody representation is SOPS YAML using age recipients. Portable-device
credentials belong on removable USB; workstation, VM, hypervisor and similar
credentials may use a protected encrypted local location. Git may carry only
reviewed auth-owned ciphertext and public metadata, never decryption identities.
Recovery copies must survive loss of ws-hadrian: intended durable destinations
are the Seagate Expansion attached to hv-matrix, GitHub, Football USB and
Foundation USB. These are requirements, not verified current replicas. Exact
live device paths and completeness are UNVERIFIED. Prior recorded paths remain
dated evidence, not current device selection. No media was inspected here.

`reauth` remains the authorization boundary. The selected future flow is an
interactive invocation that identifies the approved Foundation USB, automounts
it, and prompts the operator for its password using a trusted terminal/native
unlock agent; no password in arguments, environment, logs or Git. No background
mount, network unlock, unattended signing or implicit entitlement is allowed.
An already-mounted volume still requires the bounded reauth authorization.
Device ambiguity, cancellation, absent trust pins or unavailable trusted local
prompt fails closed. ws-cp owns platform mount/unlock realization. Existing
reauth adapters are not claimed to implement this new recovery flow.

Intended disaster experience: use the operator's phone to trigger delivery of
the reviewed encrypted GitHub release, open a terminal on ws-alpha-win, run
reauth, authenticate and recover. GitHub distributes ciphertext only; phone
access cannot authorize decryption or promote a signer. No workflow, runner,
GitHub secret, USB or workstation is changed here. Loss of Hadrian must not
lose the only decryption identity, trusted verification pin or serial evidence.
A real independently authorized recovery test from ws-alpha-win, without
Hadrian, is REQUIRED before this design can be called proven.

## Integrity, replay and recovery

An authenticated manifest binds bundle_id, schema_version, generation,
authorized_purpose, ciphertext_sha256 and ledger identity/next serial. The
selected signature is detached Ed25519 over a domain-separated canonical JSON
manifest. A verifier public key is pinned independently in operator-approved
reauth configuration; it must never be taken from the bundle. Selecting or
creating a real manifest signing identity requires a later bounded ceremony;
no SSH CA key is silently repurposed. Missing pin means DENY, not unsigned mode.

Reauth verifies signature, exact bundle/purpose, approved schema, ciphertext
hash and independent high-water evidence BEFORE any SOPS decryption/use.
SOPS/age authenticated decryption then detects corruption; a valid old SOPS
bundle alone does not prove freshness. Reject duplicate/unknown fields,
unsupported algorithms, changed digest at the same generation, rollback,
ledger mismatch, missing evidence and conflicting replicas. Emit only a
non-secret reason; retain previous accepted state, never partially expose
plaintext. Library validation of a synthetic bundle is not live acceptance.

Generation is allocated from the EXISTING Foundation serial.next_serial under
its existing single SQLite transaction/allocator lock. A later authorized
migration may add a bundle event table to that same database and increment
that same serial row, retaining epoch, consumed authorizations and issuance
history. No new allocator, reset, timestamp seed or active/active recovery is
permitted. Allocation is durable before publication; gaps after interruption
are allowed and never reused. No production ledger migration occurs here.
Until migration and reconciliation are accepted, bundle creation stays closed.

Reauth's high-water state is a verified receipt, not an allocator. Persist
bundle identity, generation, digest and ledger identity/next_serial atomically;
verify independently held Git and USB evidence at recovery and use the highest
consistent authenticated generation. Missing state cannot initialize itself
from the delivered bundle. Conflicts require reconciliation, not choosing the
most convenient copy. If every independent copy is stale, offline freshness
cannot be proved: deny promotion. A replica is never an independent signer.

Successful decryption and custody validation precede durable acceptance.
Atomic ciphertext/manifest/receipt publication uses a same-filesystem immutable
transaction directory, fsync and rename; a crash before activation preserves
the old release. Rollback revokes delivery/activation but never decreases
high-water or serial state; restoring old content requires a new generation.
Legacy export_recovery_state.py's unsigned digest manifest remains a snapshot
transport check only and cannot satisfy the new authenticated recovery gate.

## Supersession and implementation limits

This single doctrine supersedes the unversioned B70 request's assumption that a
new Foundation must be created, and AUTOMATION_SECRET_CUSTODY's proposed
manual-only/no-automount rule for the future interactive recovery workflow.
Historical raw-age bundles remain retained evidence and are not migrated.
The earlier initial README/profile-gap descriptions are historical snapshots;
`policies/ssh-user-ca-signing-control.md` and `policies/interactive-reauth.md`
retain the accepted bounded signer controls. The legacy registry's prepared
profile entry is not a fresh live acceptance or a second signer authorization.

Foundation `src/custody_generation.py` implements the additive transaction
primitive without a production entry point or migration invocation. It requires
an existing serial row, epoch and issuance history, never bootstraps state,
reserves one global serial per bundle event, and resumes an identical event
without reallocating. Its tests use only an in-memory synthetic ledger.
`src/custody_integrity.py` verifies public manifests and supplies a pure reauth
plan. Live USB identification, trusted prompting, signing-key selection,
atomic high-water persistence and Windows integration remain later authorized
realization work; no preparation test claims those platform properties.
