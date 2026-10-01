# Work Entry 010 — DERP recovery registration

Name: DERP — Deterministic Engine for Policy and Routing

Status: `PARKED` — recovery and scope preparation complete; implementation absent

Priority: `GREEN` (normal attention)

Operator health: `BLUE` — preserved from Louis's statement that DERP was newly
created and in development. No current evidence supports changing that health.
`BLUE` remains separate from the canonical priority vocabulary.

## Recovery boundary

Louis's 2026-10-01 follow-up establishes that Work Entry 010 belongs to DERP.
It authorizes recovery and registration, not implementation. The
machine-readable recovery entry is [WORK_ENTRY_010.json](WORK_ENTRY_010.json).

No DERP implementation content was found in freshly fetched canonical repo-cp main
`d46ac50128ea3491886476b81c5b75b7d6b0bd76`, any fetched remote or local branch,
registered worktree, preserved checkout, handoff, repository history, reflog,
or unreachable Git blob. A repository-wide search under
`/home/louis/helix-arpa` found no separate DERP implementation artifact before
this recovery record was written.

Accordingly, this record preserves only facts supplied by Louis:

- identifier: Work Entry `010`;
- name: DERP — Deterministic Engine for Policy and Routing;
- prior health: `BLUE` because it was newly created and in development.

Later reconciliation found one bounded scope statement in canonical
helix-offload commit `3073fd4e4c552a692d506489597faaf3f5e1038a`:
Execution Admission V1 performs matching and explicit selection only, and Work
Entry 010 / DERP owns any future deterministic routing or policy selection.
That makes completed Work Entry 005 an interface/reuse dependency and rules out
duplicating admission. It does not identify DERP's implementation repository,
detailed owner, architecture, earlier branch, code or validation evidence.

The intended implementation content, owning repository/control plane, detailed
owner, earlier branch or checkout, validation evidence and implementation
authority remain `UNKNOWN` or absent. No implementation progress, readiness,
architecture or runtime claim is reconstructed. The machine-readable START
record remains historical; the canonical topology carries the later `PARKED`
state.

## Relationship to the GPU work

The GPU pilot remains Work Entry 009. The execution-host capacity assessment
was initially assigned 010 in local commit
`1df7226210012096dde02b84593b4c29351ee14f`; it is now Work Entry 011. The
immutable historical commit is retained, and the correction is documented in
[WORK_ENTRY_010_011_RENUMBER.md](WORK_ENTRY_010_011_RENUMBER.md).

## Exact next action

Review [the smallest useful slice proposal](../proposals/derp-smallest-useful-slice.md)
and select an implementation repository/owner or supply any operator-held DERP
handoff. Reconcile that decision without overwriting recovery provenance. Do
not begin implementation until the owner, accepted slice and authority are
explicit.

Live effects: NONE.
