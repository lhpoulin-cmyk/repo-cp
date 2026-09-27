# Work protocol usage

Use `HELIX_WORK_ENTRY_V1` for bounded repository work that needs durable scope,
authority and evidence. Keep a short human prompt for context, but put the
executable boundary in JSON. Use `HELIX_WORK_RESULT_V1` after the work so a
reviewer can distinguish completed work, real blockers, non-blocking remainder,
unknowns, drift, dependencies, peer handoffs and approval needs without
reconstructing the session.

## Prepare an entry

Start from [`entry.json`](../tests/fixtures/work-protocol/entry.json), replace all
synthetic values, resolve the intended canonical ref to an immutable HEAD, and
record the source and execution workspace identities and dirty paths. Attribute
the observed state explicitly. Authority must say both what is granted and what
is explicitly withheld. Mutation scope and expected validation should be bounded
enough that an executor can finish without guessing.

For a new task, `mutation_gate: OPEN` requires a clean execution workspace at the
resolved baseline. If the source is dirty, preserve it and either close the gate
pending operator resolution or use a policy-permitted isolated checkout/worktree.
Never clean, stash, reset or absorb the source merely to make the entry pass. A
continuation may use an open gate with dirty state only when every dirty path is
attributable to that same work entry.

Validate it locally:

```sh
./tools/repo-cp check-work-entry < work-entry.json
```

A PASS receipt means only that the document conforms. Check its `mutation_gate`:
`CLOSED` prohibits repository mutation, while `OPEN` establishes only the clean
baseline precondition and does not itself grant authority. The receipt does not
dispatch an agent, verify the target, or reserve usage budget. The command exits
`1` for a conforming closed gate, `0` for a conforming open gate, and `2` for
nonconforming input so automation fails closed without mislabeling the document.

## Emit a result

Start from [`result.json`](../tests/fixtures/work-protocol/result.json). Preserve
the work-entry identifier, record both repository states, list performed and
omitted mutations, and attach validation evidence. Partition every ending dirty
path by current-work-entry, pre-existing, unrelated or unknown attribution.
Represent work state with nodes and relationships; do not call an item blocked
merely because it remains incomplete.

Validate it locally:

```sh
./tools/repo-cp check-work-result < work-result.json
```

The receipt is intentionally compact and non-executing. Store the full result in
the owning task's approved evidence location only when durable evidence is
needed; the validator itself writes nothing.

## Usage accounting

The work protocol carries work scope and result evidence; it does not invent an
agent-plan usage reading. Follow [`usage-governor.md`](usage-governor.md) for
budget state, queueing and ledger policy. Record plan percentage or other quota
data only when an authoritative meter exposes it. If it is unavailable, record
`UNKNOWN` rather than estimating token or plan consumption.

For this implementation task, exact plan percentage and model-token usage were
not exposed to repository tooling, so both remain `UNKNOWN`. Observed resource
use was bounded to local repository reads and edits, synthetic local tests, one
direct-remote parity query, and read-only fetches for the original checkout and
the authorized private task checkout. No dispatch, deployment, publication,
peer mutation, or live service/storage action occurred.
