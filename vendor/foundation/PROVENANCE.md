# Provenance

This repository starts without imported private or authoritative CA state.

## Recorded source leads

| Source | Observed substance | Status |
| --- | --- | --- |
| `auth-cp/policies/operator-ssh-identity-model.md` | Foundation must define SSH CA profile, signing, serial/key-ID, renewal, revocation, rotation, recovery, and escrow policy. | Current peer-policy input; no profile values supplied. |
| `helix-mail-core/docs/project-story.md` | Historical separate `helix-pki` workspace created an offline ECDSA P-256 root and issuing intermediate for mail TLS. | Historical evidence; not migrated authority. |
| `helix-mail-core/evidence/2026-08-01-helix-lab-x509-ca-construction.md` | Historical workspace path `/home/louis/helix-arpa/helix-pki`, construction commit `35aed04`, and public CA hierarchy characteristics. | Source recovery required. |
| `helix-mail-core/evidence/2026-08-01-ca-custody-leaf-and-dns-gate.md` | Historical mail leaf issuance `417a185` and encrypted custody placement on Foundation and Second Foundation. | Private/runtime custody remains outside Git; re-attestation required. |

No item above creates a live trust anchor, proves current custody, or authorizes
signing. Any recovered `helix-pki` history must be classified before migration.

## Current doctrine precedence — 2026-09-11

The [active consolidated doctrine](docs/ACTIVE_DOCTRINE.md) records the canonical repository,
version and operator-selected auth-cp encrypted custody boundary. Earlier
initial/prepared status prose is retained as historical context where later
specific signer and interactive-reauth contracts supersede it. Existing
cryptographic interfaces remain compatible; no runtime is activated here.

## Operator-action contract — 2026-09-11

Louis explicitly authorized establishing HELIX_OPERATOR_ACTION_CONTRACT_V1,
its schema, validator, reference renderer, compatibility guidance and tests
following repo-cp's missing-contract handoff at commit
`a6f9134c9ddad39244810cacd96fb79a12bec36d`,
`docs/handoffs/foundation-operator-action.md`. That handoff supplied acceptance
inputs, not replacement doctrine. Foundation baseline was
`fb129f747c5c9eabaadb8b7c09e433f5b071af4b`; consolidated doctrine content remains
at `d2fe6c6291ea1eaffadb15ded6c0240fed0e96ca`. The new interface is additive;
no existing custody, execution-profile or recovery authority changes.
