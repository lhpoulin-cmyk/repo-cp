# Clean Execution Baseline from bounded adaptation

Date: 2026-09-27

Context: repo-cp Standard 002 / `repo-cp.work-entry-standard-002`

## Observation

Codex encountered the primary repo-cp checkout on `main` at
`25be360064f87d5cef52e5304da332861a9980e9` with no staged files but multiple
modified and untracked paths. A direct remote check resolved the intended
canonical `origin/main` baseline to
`f1425811f8e7fab2227367cc21b4cacdb9041d0a`, eight commits ahead. Rather than
resetting, cleaning, stashing, overwriting or absorbing work of unresolved
provenance, Codex preserved that source checkout and created the policy-permitted
isolated checkout `.agent-checkouts/codex/work-entry-standard-002` at the
canonical baseline. Standard 002 implementation and validation proceeded there.
The task evidence retained the identity, revision and dirtiness distinction for
both workspaces and reported the original checkout separately.

Subsequent review recognized this successful adaptation as generalizable and
fed it back into Standard 002 as `HELIX_CLEAN_EXECUTION_BASELINE_V1`, a
portfolio-wide repo-cp work-entry invariant.

Evidence: [`comparison and usage record`](../docs/acceptance/work-entry-standard-002-comparison.md),
[`work entry`](../docs/acceptance/work-entry-standard-002-entry.json), and
[`work result`](../docs/acceptance/work-entry-standard-002-result.json).

## Interpretation

An unforeseen operational condition produced a bounded adaptation; the behavior
and its evidence were reviewed; the behavior was abstracted into a reusable
rule; and the rule was incorporated into the institutional control plane. Future
agents can therefore inherit the constraint without sharing the original
agent's conversational state. This is an observed anecdote relevant to research
on generally capable agent systems and recursive institutional learning. It is
not evidence of, or a claim that the system is, AGI.

## Open research question

What combination of machine-checkable provenance, review thresholds and
exception authority best allows useful agent adaptations to become durable
institutional rules without overfitting a single successful episode or turning
local heuristics into unjustified universal policy?
