# Helix Control Plane: purpose and naming

In Helix repository names, **`-cp` means “control plane.”** For example,
`repo-cp` is the repository governance control plane and `network-cp` is the
network control plane. Use the full phrase when introducing either to a reader.

The Helix Control Plane is the coordinated system of domain-owned policies,
contracts, observations and authorized automation that helps operate Helix.
The singular name describes the overall approach; individual control planes
retain their own responsibilities and authority.

This document explains that concept and its naming. It does not create a new
central controller, assign domain ownership, grant access or establish a new
Foundation interface. Current owning contracts remain authoritative.

## What a control plane does

A Helix control plane makes a domain's intended state, boundaries and operational
rules explicit. Depending on its charter, it maintains declarations, checks
observed evidence against requirements, prepares changes, or realizes authorized
changes. Its repository provides versioned instructions and evidence that humans
and agents can inspect and review.

A repository name alone proves none of those capabilities. Documentation,
implementation, tests, authorization and observed results establish what is
actually available. A control plane may be observation-only; an accepted
contract may still have no live executor.

The systems doing the everyday work remain distinct: applications serve users,
workers transform media, and storage systems hold data. Their control planes
define or coordinate the relevant rules and permitted management operations.
Hosting a workload does not automatically confer ownership of its application,
identity, network or storage policy.

## One system, explicit owners

The portfolio's [architecture and ownership map](https://github.com/lhpoulin-cmyk/arpa-docs/blob/e0cf21539ccad3cc1d57ebe3408c9a6d542fc7dc/README.md)
distinguishes portfolio coordination, domain control planes, products,
deployments, private records, live systems and the human operator.

| Surface | Role in that division |
| --- | --- |
| `arpa-docs` | Maps the portfolio and cross-domain relationships |
| Foundation | Owns universal contracts and conformance; retains its defined trust and custody responsibilities |
| Domain control planes | Own their declared domain policies and desired state |
| Products and services | Own their reusable capabilities and application behavior within peer contracts |
| Deployment records | Bind a particular release to particular infrastructure |
| Human operator | Decides goals and retains the approval and exception authority defined by governing rules |

For example, network policy belongs to the network control plane. GPU allocation
belongs to the GPU control plane. A media application consumes those capabilities
without absorbing their authority. An automation system realizes only the state
and operations its governing contracts authorize.

Within this repository, [repo-cp's ownership](../OWNERSHIP.md) is narrower:
inventory, enrollment records, accepted pins, repository audits, drift reports
and review artifacts. It also maintains the operator-directed agent work
contract. Its runtime CLI does not execute proposed actions or mutate peers.
Neither an inventory entry nor a successful audit grants live authority.

## Agentic automation with human judgment

The intended behavior is for agents to carry authorized work forward: discover
the governing sources, inspect current evidence, prepare or implement supported
changes, run the applicable checks and verify the outcome. Humans should receive
a clear result or a concrete decision at a genuine authority boundary.

A useful conceptual cycle is:

1. Establish the outcome, owning authority and current state.
2. Prepare a bounded change with acceptance and recovery evidence.
3. Check whether existing authorization covers the exact operation. Where a
   new decision is required, present the prepared proposal to the human.
4. Execute only through an available, authorized mechanism.
5. Verify the postconditions; record completion, uncertainty or recovery needed.

Existing authorization should carry ordinary work forward without repeated
permission requests. Missing authority, changed scope and unsafe or uncertain
state must remain visible. Silence is not approval, and an agent's ability to
perform an operation does not establish permission.

This cycle explains the design direction; it is not a newly implemented workflow
engine or approval protocol. Foundation's current operator-action V1 describes
reviewable declarations, not execution authorization. Consult the
[accepted interface and limits](acceptance/operator-action-v1.md) and the
[agent work contract candidate](AGENT_WORK_CONTRACT_CANDIDATE.md) for the actual
rules and supported behavior.

## How to write the name

- Use **Helix Control Plane** for the overall concept, then explain its domain
  structure when relevant.
- Write **control plane** in ordinary prose. Introduce an identifier as, for
  example, “the repository governance control plane (`repo-cp`).”
- Keep exact repository names in paths, links, commands and technical references.
  This explanation does not rename repositories or break existing references.
- Avoid a standalone “CP” in public titles, navigation or introductory text.
  Spell it out so readers do not have to infer an abbreviation's meaning.
- Describe each control plane's actual scope. Avoid implying a universal
  administrator, automatic execution, or authority over another domain.

## Source and maintenance

The portfolio explanation above follows `arpa-docs/README.md` at
`e0cf21539ccad3cc1d57ebe3408c9a6d542fc7dc`. The repo-cp role follows
[OWNERSHIP.md at release 1.0.0](https://github.com/lhpoulin-cmyk/repo-cp/blob/4ede9b73501b38a2b0ba5a50c9c32875a2d0eb19/OWNERSHIP.md).
The human-in-the-loop emphasis and naming guidance reflect the operator's
2026-09-23 direction. These are source identities for this explanation, not
claims that every peer is currently deployed or conforms.

Maintain this as a public explanatory companion to the agent work contract.
Change ownership through the owning authority's procedure; update this guide to
explain the accepted result. Do not use an explanatory edit to invent authority.
