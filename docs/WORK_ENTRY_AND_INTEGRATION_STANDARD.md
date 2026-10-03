# Helix work-entry and integration standard

Status: proposed repository-governance standard
Owner: Louis H. Poulin II
Scope: Helix repositories and services

## 1. Work-entry authentication gate

Every substantive work session begins by verifying that the access required for the intended scope still works.

A previous successful authentication is historical evidence, not current authorization. Before agents diagnose downstream failures or repeat credential provisioning, they must perform the narrowest safe non-mutating verification of the required observer/executor/service path and record the result and, when knowable without exposing secrets, its validity/expiry boundary.

If verification fails or validity cannot support the intended operation, mark the affected path RED or YELLOW as appropriate and repair or reauthorize it before depending on it. Do not revisit a previously closed authentication blocker merely because its historical expiry is unknown: verify current behavior first.

This gate does not expand authority, grant credentials, or supersede auth-cp/Foundation contracts.

## 2. Upstream-first integration rule

When Helix extends an actively maintained upstream project, prefer external integration over modifying upstream source.

Preferred order:
1. configuration and documented extension points;
2. adapters and wrappers;
3. evidence collectors and observers;
4. independent selectors, validators, policy engines, and promotion services;
5. minimal, isolated upstream patches only when the required behavior cannot reasonably live outside upstream.

Keep Helix-specific policy and orchestration separable so upstream upgrades remain practical. Any unavoidable upstream patch must have a stated reason, bounded surface, tests, and an explicit transplant/rebase strategy.

When Helix solves a generally useful upstream problem without coupling it to private infrastructure or policy, prepare the work as a proposal/contribution suitable for upstream review.

## 3. Green / Yellow / Red tracking topology

Use the following fixture for project status reviews:

- GREEN — demonstrated in the relevant environment with current evidence; no known blocker in the stated scope.
- YELLOW — implemented or substantially understood, but incomplete, awaiting current verification, integration, hardening, transplant, or end-to-end proof.
- RED — blocked, failed, unsafe to proceed, or missing a required contract/capability.

Historical success does not remain GREEN indefinitely when freshness matters. A component with stale authorization or unverified live parity becomes YELLOW until reverified.

Status reports should identify the layer/component, color, current evidence, blocker or remaining proof, and next transition needed. The target for an engineering pass may explicitly be "everything at least YELLOW": eliminate unknown/unexamined RED conditions before attempting final GREEN admission.

## 4. Narrow writer-service boundary

In ingestion/publication systems, producer and transformation hosts should not receive casual write access to permanent stores merely to complete a pipeline.

Keep final storage read-only to upstream workers when practical. The final publication service owns the narrowly scoped write capability and performs the authorized commit/promotion into permanent storage.

Design that service as transplantable infrastructure: the temporary implementation may be developed beside the current workload, but its writer capability, publication contract, validation boundary, audit evidence, and rollback semantics must be separable and moved into the final service before production admission.

A successful temporary write path is not proof that the final service has been transplanted or admitted.

## 5. Review invariant

For every pass:
- verify required auth first;
- establish the Green/Yellow/Red topology;
- do not reopen closed blockers without regression evidence;
- preserve upstream replaceability;
- identify temporary capabilities that require transplant;
- drive RED to at least YELLOW before declaring the pass structurally complete;
- reserve GREEN for current evidence.
