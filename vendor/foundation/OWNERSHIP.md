# Foundation Trust Authority

## Owns

- SSH user and host CA authority;
- generic X.509 CA authority;
- CA private-key custody policy;
- cryptographic requirements and certificate profiles;
- generic signing interfaces;
- serial and key-ID policy;
- trust-anchor policy;
- revocation mechanisms;
- rotation, recovery, escrow, and lost-device policy; and
- public trust-anchor and CA-profile registries.

## Does not own

- human or service identity, roles, entitlements, or approval to issue a
  credential (`auth-cp`);
- workstation key generation, private-key storage, SSH client configuration,
  or certificate placement (`ws-cp`);
- mail identities, mail hostname/SAN requirements, Stalwart configuration, or
  mail certificate deployment (`helix-mail-core`);
- DNS, network reachability, hypervisor mechanics, or live service state.

Foundation establishes cryptographic trust. It does not infer issuance
authorization from custody, and it cannot issue credentials merely because a
consumer requests them.

Private keys, encrypted custody packages, runtime CA databases, and signing
credentials must not be committed to this repository.

## Current doctrine precedence — 2026-09-11

The [active consolidated doctrine](docs/ACTIVE_DOCTRINE.md) records the canonical repository,
version and operator-selected auth-cp encrypted custody boundary. Earlier
initial/prepared status prose is retained as historical context where later
specific signer and interactive-reauth contracts supersede it. Existing
cryptographic interfaces remain compatible; no runtime is activated here.

Foundation also owns the shared
[operator-action declaration and presentation contract](contracts/HELIX_OPERATOR_ACTION_CONTRACT_V1.md).
Consumers own action realization; auth-cp retains authorization and custody.
Presentation conformance grants no operational authority.
