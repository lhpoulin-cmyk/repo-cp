# repo-cp Codex Handoff — Standard #2: Work Entry, Upstream-First, Status Topology, Writer Boundary, and Agent Work Protocol

You are working in **repo-cp**, the governance/control-plane repository for the Helix repository ecosystem.

This task has two related purposes:

1. Make four engineering/control-plane principles permanent repo-cp standards.
2. Begin turning repo-cp into the protocol boundary between Louis, ChatGPT, Codex, Work, and individual `-cp` / `-service` repositories so Louis does not have to remain the manual message bus between agents.

Treat this as repository/control-plane engineering, not merely documentation cleanup.

## 0. Preserve existing work first

Before changing anything, inspect repo-cp thoroughly.

Establish and retain evidence for:

- current branch
- HEAD
- configured upstream
- local/upstream/direct-remote parity where practical
- recent relevant commits
- staged files
- unstaged files
- untracked files
- existing repository validation/audit state
- any pre-existing dirtiness

Do **not** discard, reset, overwrite, stash, commit, amend, or otherwise normalize pre-existing work simply because it is inconvenient.

Determine, where reasonably possible, whether existing dirtiness predates this task.

The final report must clearly distinguish:

- pre-existing state
- changes made by this task
- unresolved or unknown provenance

Do not commit or push merely to produce a clean tree.

---

# 1. Permanent standard: work-entry

Formalize the idea that meaningful agent work should begin from an explicit **work-entry contract** rather than an unstructured prose prompt.

The conceptual flow is:

Louis  
→ intent / authority  
→ ChatGPT architecture and triage  
→ repo-cp work-entry contract  
→ Codex repository execution  
→ repo-cp work-result evidence  
→ ChatGPT review / interpretation  
→ Louis only when judgment, authorization, ambiguity, or exception handling is required.

The objective is **not** to remove Louis from authority.

The objective is to stop requiring Louis to act as the human message bus carrying large prose handoffs between agents.

repo-cp should increasingly carry that protocol.

Investigate existing repo-cp mechanisms before inventing new ones. Reuse or extend existing enrollment, acceptance, evidence, audit, repository metadata, schemas, tooling, or conventions wherever coherent.

A work-entry should eventually be able to resolve or record at minimum:

- target repository
- objective
- governing repo-cp standards
- authority granted
- authority explicitly not granted
- starting HEAD
- starting dirty state
- relevant dependencies
- expected validation
- allowed mutation scope
- prohibited mutation scope
- required evidence
- expected result format

Do not build an enormous orchestration framework during this task.

Build the **smallest durable foundation** that makes this a real repo-cp concept rather than another Markdown convention.

If an executable/schema-backed representation is appropriate, prefer that over making Markdown carry the entire protocol.

Markdown may document the interface; it should not necessarily *be* the interface.

---

# 2. Permanent standard: upstream-first engineering

Make **upstream-first** a repo-cp engineering standard.

When integrating or extending an upstream project, Helix should prefer keeping its behavior outside upstream source whenever reasonably feasible.

Preferred mechanisms include:

- adapters
- configuration
- selectors
- wrappers
- evidence collectors
- policy layers
- promotion/publication machinery
- external orchestration
- narrowly scoped patches only where necessary

Avoid creating or maintaining a large private fork merely because modifying upstream source is convenient.

The goal is to preserve:

- upstream compatibility
- rebasing/upgrading ability
- provenance
- maintainability
- separation between Helix policy and upstream implementation

A fork or source modification is not absolutely forbidden.

When it is necessary, it should be explicit, bounded, justified, and visible as technical debt or a maintained divergence.

This principle originated from the ARM work but is **not ARM-specific**. It is an ecosystem-wide engineering standard.

---

# 3. Permanent standard: status topology

Repositories and agents need a consistent way to communicate operational status.

Formalize a **status topology** that distinguishes concepts that have repeatedly become conflated in handoffs.

At minimum, status reporting should distinguish:

- completed
- currently active
- pending
- blocked
- non-blocking incomplete work
- unknown
- drift
- dependency
- external dependency
- authority/approval required

Where appropriate, status should also express relationships rather than just labels.

For example:

A is blocked by B.

C remains incomplete but does not block D.

E requires authorization from Louis.

F is complete and must not continue appearing as a blocker.

G belongs to another control plane and must be handed off rather than silently mutated here.

The purpose is to prevent agents from repeatedly rediscovering or resurrecting already-resolved blockers.

Investigate whether existing repo-cp audit/enrollment status vocabulary can be extended rather than creating a competing status system.

The topology should be machine-consumable where practical.

Human-readable reports should be projections of that state rather than the only authoritative representation.

---

# 4. Permanent standard: writer boundary

Formalize the storage/publication boundary we established during ARM/media-promotion work.

Processing, ripping, encoding, staging, inspection, discovery, and similar intermediate services should **not casually receive write access to permanent/final storage**.

Read-only final-library access is often a feature, not a defect.

Permanent publication should occur through a narrow, explicit writer capability.

However, capture the important architectural destination:

**the final publication service will ultimately possess that write capability.**

We are not designing around permanent manual intervention.

During development, a temporary or transitional writer mechanism may exist. The architecture must explicitly preserve the requirement to **transplant the writer capability into the final publication service** when that service becomes authoritative.

The intended shape is roughly:

processing/staging service  
→ candidate artifact  
→ validation/evidence  
→ promotion/publication boundary  
→ final publication service  
→ narrowly scoped permanent-storage write capability

Prefer least privilege.

Do not accidentally document the current read-only B70 arrangement as the desired final architecture.

B70's inability to casually write the final library is useful.

The eventual publication service's ability to perform an authorized, bounded write is also required.

Both statements are true.

---

# 5. Standard agent result contract

Investigate and establish the foundation for a compact, structured result emitted after bounded repository work.

Conceptually this may become something like:

`WORK_RESULT.json`

The exact filename/schema should follow repo-cp conventions discovered during inspection rather than this handoff blindly dictating implementation.

The result should be able to communicate at minimum:

- target repository
- objective/work-entry identifier
- starting HEAD
- ending HEAD
- starting dirty state
- ending dirty state
- files changed
- mutations performed
- mutations explicitly not performed
- tests/validation executed
- validation results
- evidence produced
- completed work
- remaining work
- blockers
- non-blocking incomplete items
- unknowns
- dependencies discovered
- cross-control-plane requests
- authorization required
- recommended next action

This should dramatically reduce the amount of prose Louis must shuttle between ChatGPT and Codex.

The human summary can then be short because the structured evidence carries the detailed state.

---

# 6. Respect control-plane ownership

This task must reinforce, not weaken, repository boundaries.

If repo-cp discovers that another repository needs modification:

- identify it
- describe the requested change
- produce a bounded handoff/request
- do not silently mutate the peer repository unless existing authority explicitly permits it

Examples include:

- `network-cp`
- `auth-cp`
- `ws-cp`
- `ansible-cp`
- `hv-cp`
- service repositories

Cross-repository convenience is not authority.

---

# 7. ChatGPT, Codex, Work, and Louis roles

Capture this division without hard-coding vendor assumptions so deeply that the protocol becomes unusable with future agents.

The present operational model is:

**Louis**
- intent
- authority
- approval
- judgment
- exception resolution

**ChatGPT**
- architecture
- decomposition
- triage
- interpretation
- cross-control-plane reasoning
- review of evidence
- preparation of bounded execution contracts

**Codex**
- repository inspection
- implementation
- testing
- diff generation
- repository-local evidence

**Work**
- optional multi-system / multi-repository expedition capability
- useful where the task genuinely spans browsers, files, repositories, external systems, or long multi-step workflows
- not automatically preferable for ordinary repository-local engineering

repo-cp should allow these roles to communicate through durable contracts rather than depending upon Louis copying prose between them.

The protocol should remain agent-neutral enough that another executor could replace Codex or another reasoning layer could replace ChatGPT later.

---

# 8. Avoid overengineering

Do not attempt to build the final autonomous Helix agent platform today.

This task should leave us with:

1. coherent permanent standards;
2. a clear work-entry model;
3. a clear structured work-result model;
4. machine-readable foundations where they provide immediate value;
5. compatibility with existing repo-cp governance;
6. tests/validation for anything executable or schema-driven;
7. an obvious path toward future automation.

Prefer one small working primitive over ten speculative abstractions.

---

# 9. Review repo-cp itself

After implementing the above, perform the repo-cp review Louis requested.

Report:

- current branch
- HEAD
- upstream/tracking state
- direct remote parity if repo-cp normally verifies it
- recent relevant commits and what they introduced
- staged changes
- unstaged changes
- untracked files
- pre-existing dirtiness
- task-created dirtiness
- unresolved provenance
- tests run
- audits run
- PASS / UNKNOWN / DRIFT / BLOCKED state where supported
- failures or warnings
- exactly what this task changed

Pay particular attention to recent work that may already partially implement these ideas.

Do not duplicate existing mechanisms merely because this handoff uses different terminology.

---

# 10. Acceptance criteria

This task is successful when:

- work-entry is a recognizable repo-cp standard and has a durable foundation;
- upstream-first is an ecosystem-wide engineering standard;
- status topology can distinguish blockers from merely incomplete work and represent dependency/authority relationships;
- writer-boundary semantics clearly preserve least privilege while explicitly targeting eventual final-service publication authority;
- repo-cp has a credible structured work-result direction or initial implementation;
- existing repo-cp mechanisms were reused where appropriate;
- peer control-plane boundaries remain intact;
- validation covers new executable/schema behavior;
- no unrelated work was destroyed;
- repo-cp's current Git state is comprehensively reported;
- the final response is compact enough that Louis can paste it back to ChatGPT without becoming the protocol himself.

## Final response format

Lead with a concise verdict.

Then report:

**IMPLEMENTED**  
What changed.

**VALIDATION**  
Tests/audits and exact results.

**REPO-CP STATE**  
Branch, HEAD, parity, and dirtiness.

**STATUS TOPOLOGY**  
Completed, blocking, non-blocking incomplete, unknown, and authorization-required items.

**CROSS-CP REQUESTS**  
Only if another repository actually needs work.

**NEXT DECISION**  
Only decisions that genuinely require Louis or architectural review.

Do not inflate the report with a diary of commands.

Evidence over narration.
