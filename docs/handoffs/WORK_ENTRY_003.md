# repo-cp Codex Handoff — Work Entry 003

Status: `COMPLETE`

Priority: `GREEN`

Phase: canonical closure

This handoff records findings that must be carried through Work Entry 003. The
initial cleanup phase remains evidence collection and faithful reporting for
Louis + ChatGPT review. It grants no authority to clean, normalize, delete,
reset, stash, overwrite, absorb, publish, or otherwise resolve repository state.
The governing sequence remains:

```text
observe/evidence
  -> Louis + ChatGPT review
  -> classify/provenance
  -> Louis decision/authorization
  -> bounded Codex action, if any
  -> validation
```

## Work topology finding — required before 003 closure

Work Entry 003 discovered that repo-cp needs to distinguish **work state** from **work priority**.

Extend the existing Standard 002 contract/status topology and appropriate repo-cp topology representation with two independent dimensions:

**State** represents lifecycle/execution status.

**Priority** represents urgency/attention and MUST NOT itself grant authority, mutation permission, execution status, or automatic preemption.

Establish at minimum the current priority vocabulary:

- `GREEN` — normal priority
- `YELLOW` — elevated priority
- `RED` — high priority

Use boring machine-readable values; colors/icons are presentation only.

Preserve the important valid combination demonstrated during 003:

- 003: `ACTIVE + GREEN`
- 004: `PARKED + YELLOW`
- 005: `PARKED + RED`

A `PARKED + RED` entry remains parked until the governing workflow/authority advances it. An `ACTIVE + GREEN` entry is not automatically displaced by it.

Integrate this into the existing contract/topology rather than creating a parallel queue mechanism. Update schemas, validation, documentation, fixtures/tests, and machine-readable topology where appropriate.

Record the current work topology:

- 001 — COMPLETE / GREEN
- 002 — COMPLETE / GREEN
- 003 — COMPLETE / GREEN
- 004 — PARKED / YELLOW — publication/evidence infrastructure
- 005 — PARKED / RED — deterministic repository evidence/review tooling; reference `helix-offload`, `ws-doc-writer`, `ws-code-agent`, and `helix-repo-manager-bot`

This change is **necessary for Work Entry 003 closure**, but it does not authorize beginning 004 or 005.

Continue 003's cleanup/reconciliation first. Do not mark 003 complete merely because this topology change validates. 003 still requires its normal review, publication, canonical verification, and closure conditions.

## Finding disposition rule — required before 003 closure

During an active work entry, determine whether each finding is actionable within
that entry's objective and authority.

An actionable finding that falls within the entry's objective and authority may
be incorporated into that entry. A finding that is valuable but not actionable
within the current objective or authority MUST NOT silently expand scope.
Preserve it as a separately identified future goal or work entry with provenance,
state, and priority, then return to the active entry. Creating or prioritizing
that future goal does not authorize its execution.

The observed dispositions during Work Entry 003 are:

- publication/evidence architecture became Work Entry 004, `PARKED + YELLOW`;
- deterministic repository evidence/review tooling became Work Entry 005,
  `PARKED + RED`; and
- state-versus-priority and finding-disposition behavior are actionable workflow
  findings required within Work Entry 003.

This rule prevents valuable discoveries from causing silent architectural or
authority drift while retaining enough provenance to resume separately governed
work later.

## Canonize louis-workflow — required before 003 closure

Work Entry 003 established the need for an explicit human/agent operating model
named `louis-workflow`. It is an operational contract, not a personality
document. Before 003 closes, canonize its cadence, roles, authority boundaries,
deterministic-versus-model work, finding disposition, independent state and
priority, review and authorization, closure/publication, and future-work parking
and resumption.

The written contract must include diffable diagrams for the Louis/ChatGPT/tooling
loop, finding disposition, work lifecycle, and coexistence of `ACTIVE + GREEN`
with `PARKED + RED`. Normative requirements must use the existing work protocol,
schemas, validator and topology mechanisms rather than Markdown alone or a
parallel governance system.

Document that the workflow was derived empirically from Work Entries 002–003.
Preserve observation versus interpretation. This finding motivates Work Entry
005 but does not authorize beginning it. Canonization also does not replace the
primary Work Entry 003 purpose: review and reconciliation of the preserved dirty
repo-cp state.

## Control plane / work surface boundary — final 003 workflow finding

Before 003 closes, `louis-workflow` must record repo-cp as the portfolio control
plane and primary Louis + ChatGPT work surface. repo-cp owns portfolio reasoning
and topology, work-entry creation and lifecycle, standards and contracts,
finding disposition, state and priority, evidence review, cross-repository
coordination, authorization/decision provenance, acceptance and canonical
closure.

Individual `*-cp` repositories are bounded agent work surfaces. Agents act there
under explicit work-entry authority and return evidence/results to repo-cp for
review. `helix-offload`, `helix-repo-manager-bot`, `ws-code-agent`, and
`ws-doc-writer` are supporting tools or services and must not independently
become competing portfolio control planes.

Preserve the topology Louis ↔ ChatGPT ↔ repo-cp → bounded agent/tool work
surfaces → evidence/results → repo-cp → Louis + ChatGPT. This is the final new
workflow/topology finding before reconciliation. It does not authorize beginning
004 or 005; after validation, freeze further workflow design and return to the
existing 003 review queue.

## Dependency-aware scheduling finding

Work Entry 006 attempted priority preemption but correctly stopped without
mutation because its required louis-workflow and current-topology governance is
unpublished Work Entry 003 state. Scheduling eligibility is determined
independently by lifecycle state, priority and dependencies. Priority never
satisfies a dependency or grants authority, mutation, execution or preemption.
Work requiring unpublished predecessor governance is `BLOCKED` until that
governance is canonical.

Before 003 publication, record 006 as `BLOCKED + RED`, dependent on 003, and
ineligible for scheduling. Canonical publication satisfies that dependency and
returns 006 to `PARKED + RED`; it remains unstarted and unauthorized. 004 and
005 remain parked. This finding does not authorize any of them.

## Pause/resume continuity finding

A pause/resume handoff must preserve workspace state and attribution, the
mutation gate, in-flight invocation disposition and attribution, session
binding/release, the exact continuation point, and required revalidation. A
paused entry closes its mutation gate. Resumption retains the work-entry identity
and may reopen the gate only after the baseline, workspace, dependencies,
authority and listed continuation requirements are revalidated.

These findings are required 003 work. After integrating and validating them,
return to the frozen reconciliation queue; the remediation handoff is the next
read-only review item.

## Remediation handoff disposition

Louis + ChatGPT reviewed
`docs/handoffs/repo-cp-audit-remediation-20260923.md` and accepted the following
semantic disposition. The source handoff remains preserved primary-checkout
evidence; it is not transplanted as an active canonical handoff.

| Finding | Disposition | Preserved relationship or evidence |
| --- | --- | --- |
| R1 | `SATISFIED / SUPERSEDED` | Canonical contract-integrity validation |
| R2 | `SATISFIED / SUPERSEDED` | Canonical allowlisted diagnostics |
| R3 | `SATISFIED / SUPERSEDED` | Canonical validation privilege preflight |
| R4 | `PRESERVED` future-work candidate | `hardening/correctness` group; remediation handoff provenance |
| R5 | `PRESERVED` future-work candidate | `hardening/correctness` group; concrete current correctness finding: valid dotted Git branch names are rejected |
| R6 | `PRESERVED` future-work candidate | `diagnostics/state fidelity` group; remediation handoff provenance |
| R7 | `PRESERVED` future-work candidate | `evidence/trust architecture` group; remediation handoff provenance |
| R8 | `PRESERVED` future-work candidate | `evidence/trust architecture` group; remediation handoff provenance |
| R9 | `PRESERVED` future-work candidate | `diagnostics/state fidelity` group; remediation handoff provenance |
| R10 | `NO CURRENT ACTION` | Current rejection boundary is acceptable; no present requirement justifies added alias capability |
| R11 | `NO CURRENT ACTION` | Current reference location is acceptable; no present requirement justifies relocation churn |
| R12 | `SATISFIED` | Canonical human-facing purpose and command discovery |

R4–R9 are grouped findings, not six work entries; they have no execution
authority. R10–R11 are not parked work. The remediation handoff status is
`REVIEWED / SEMANTICALLY EXHAUSTED` for Work Entry 003.

## Bounded reconciliation discovery recheck

Date: 2026-09-27

Status: `RECONCILIATION_REVIEW_CLOSED`. Louis + ChatGPT review, authorization,
commit/publication and canonical-main verification subsequently completed.

Coverage actually examined:

- the preserved primary checkout identity, HEAD, local upstream ref, staged,
  unstaged and untracked path inventory;
- SHA-256 continuity for all 16 original dirty paths against the preserved 003
  evidence artifact;
- the original path-to-canonical comparisons: five canonical duplicates,
  superseded `OWNERSHIP.md`, the four-file checkout-isolation package, the
  `AGENTS.md`/`README.md` pair, the three-file rc.4 delta and the remediation
  handoff;
- every accepted reconciliation/disposition recorded above and the corresponding
  isolated-checkout implementation;
- the complete isolated-checkout diff surface, schema/semantic conformance,
  focused tests, full repository validation and `git diff --check`.

Findings:

- new actionable in-scope findings: `NONE`;
- new out-of-scope findings requiring preservation/routing: `NONE` beyond the
  already preserved R4–R9 candidate groups;
- previously reviewed items requiring reopening because of changed evidence:
  `NONE`.

Remaining `UNKNOWN` or deliberately unexamined scope:

- authorship and original conversational intent of preserved primary-checkout
  dirtiness beyond the recorded bytes, timestamps and semantic review:
  `UNKNOWN`. This exact evidence boundary was surfaced to Louis. He supplied
  later research context about two observed agent behaviors, but that context
  does not identify the authorship or original intent of these dirty paths. The
  UNKNOWN is therefore retained without wider search and is not a blocker; the
  separate research context is preserved in
  `research-notes/2026-09-27-clean-execution-baseline.md`;
- peer repositories, live/runtime systems, credentials, private material and
  remote service state, which are outside Work Entry 003 scope;
- new network freshness evidence: no fetch was performed during this recheck;
  the local canonical ref remains `456c9bc7b2b2372c96b503c73ab2780961bb340f`;
- implementation design for preserved R4–R9 candidates, which 003 does not
  authorize.

The primary checkout's ahead/behind display changed from eight to nine commits
behind, while both endpoint revisions and all 16 dirty-path hashes remained
unchanged. This metadata-only difference does not reopen a reviewed item.
The bounded discovery pass found no additional findings within the coverage
above; it makes no claim about unexamined scope. Louis's contextual response
satisfied the resolvable-UNKNOWN checkpoint, so reconciliation review closes
with the bounded provenance UNKNOWN preserved.

## Canonical closure

Louis authorized publication on 2026-09-27. Commit
`27ac0626d151c5a8dea5cb4198ce728413feea2d` was published to canonical `main` as
an ordinary non-forced fast-forward from
`456c9bc7b2b2372c96b503c73ab2780961bb340f`. An independent remote query and
fetch resolved canonical `main` exactly to the published commit; the fetched
tree matched the isolated checkout and passed full validation.

Work Entry 003 therefore satisfies its review, authorization, publication,
canonical-verification and closure requirements and transitions to `COMPLETE +
GREEN`. Work Entry 006's dependency on canonical 003 governance is satisfied;
006 returns to `PARKED + RED` without beginning execution or receiving new
authority. The preserved primary checkout remains outside the publication path.
