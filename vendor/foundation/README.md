# Foundation Control Plane

`foundation-cp` is the Helix-ARPA authority for foundational cryptographic
trust. It defines and records trust policy; it is not a mail product, network
control plane, credential vault, or live certificate service.

## Current state

Version 1.0.0 consolidates the active repository doctrine. This repository
contains public trust records and the existing bounded signer implementation;
private CA material and mutable runtime state remain outside Git. The checked-in
signer configuration is disabled at rest. Repository validation does not prove
current installed state, B70 credential acceptance or live recovery.

See [OWNERSHIP.md](OWNERSHIP.md), [the trust policy](policies/trust-policy.md),
and [provenance](PROVENANCE.md).

## Current doctrine precedence — 2026-09-11

The [active consolidated doctrine](docs/ACTIVE_DOCTRINE.md) records the canonical repository,
version and operator-selected auth-cp encrypted custody boundary. Earlier
initial/prepared status prose is retained as historical context where later
specific signer and interactive-reauth contracts supersede it. Existing
cryptographic interfaces remain compatible; no runtime is activated here.

The additive [universal execution profiles v1](docs/EXECUTION_PROFILES.md)
define session and privilege guarantees consumed by auth-cp. All platform
implementation evidence remains unverified; these contracts grant no live
account, credential, elevation or custody authority.

The [operator-action contract v1](contracts/HELIX_OPERATOR_ACTION_CONTRACT_V1.md)
provides a versioned public proposal schema and deterministic terminal renderer.
It presents commands for independent review and never authorizes or executes them.
