# Work Entry Standard 002 comparison and usage record

Date: 2026-09-27

Task evidence: [`WORK_ENTRY_STANDARD_002.md`](../handoffs/WORK_ENTRY_STANDARD_002.md)

## Repository comparison

The original checkout began on branch `main` at
`25be360064f87d5cef52e5304da332861a9980e9`. Its cached `origin/main` initially
matched. A direct canonical query observed `origin/main` at
`f1425811f8e7fab2227367cc21b4cacdb9041d0a`; a read-only fetch confirmed that the
original checkout was eight commits behind. Those commits publish the agent work
contract, validation diagnostics, local repository creation, usage-governance
notes and lab-time guidance.

The original checkout already contained uncommitted work before this task.
`PROVENANCE.md`, `docs/AGENT_WORK_ADOPTION.md`,
`docs/AGENT_WORK_CONTRACT.md`, `docs/HELIX_CONTROL_PLANE.md`, and
`pins/agent-work-contract.json` match the newly fetched canonical blobs.
`AGENTS.md`, `OWNERSHIP.md`, `README.md`,
`docs/AGENT_WORK_CONTRACT_CANDIDATE.md`, `docs/REPOSITORY_VOICE.md`, and
`pins/agent-work-contract-candidate.json` differ from canonical. `.gitignore`,
`CLAUDE.md`, `docs/AGENT_CHECKOUT_RULES.md`,
`docs/handoffs/repo-cp-audit-remediation-20260923.md`, and
`tests/test_validation_scope.py` are absent from canonical. Their detailed
authorship remains unresolved; all predate this task's first write and were
preserved.

The governing uncommitted inputs consulted from that original checkout were
captured on 2026-09-27 against base `25be360064f87d5cef52e5304da332861a9980e9`:

| Path | SHA-256 |
| --- | --- |
| `AGENTS.md` | `7c39301f18b0a4c9ef78736197cec8e6397a84dd494dbc462bded875b8faaea0` |
| `README.md` | `099827b8b080cc345a013d4406be92ab561985ab9743478da7d6f97c78ecc31d` |
| `OWNERSHIP.md` | `3b2b7e11a462c33943568c3a8dce4b1e4b638c38d62a3fdab795ae968ec82c83` |
| `PROVENANCE.md` | `7d1cefc35ae98eda6d9946409ee6cbbabf1b056c6e19c36152886d82f854da1a` |
| `docs/AGENT_CHECKOUT_RULES.md` | `1754c2769672d14072971e762ccfaaa14db2f6f0b49a75881f2a71919fc5a0c9` |
| `docs/AGENT_WORK_CONTRACT.md` | `a4838c4bfd8e1d27ed794c48ca1d475d76929309fabc212368234c4073df7674` |

The resulting verbatim handoff has SHA-256
`752f3a49d8ca9ac9688009070573110a0df024ece08ced2e68a6f5aeeeb6ac9c`.
The governing execution doctrine was read from arpa-docs commit
`e0cf21539ccad3cc1d57ebe3408c9a6d542fc7dc` with SHA-256
`213b702e9d56878b8b0b2ff1d5d991c166e7fd2e16c877e3ae6415752ae539a4`.

Because canonical changes overlap the CLI, validator and several pre-existing
files, implementation moved to the authorized private checkout
`.agent-checkouts/codex/work-entry-standard-002` on branch
`codex/work-entry-standard-002`, based at and tracking canonical
`f1425811f8e7fab2227367cc21b4cacdb9041d0a`. This avoids silently overwriting or
normalizing the original dirty work while making the protocol changes against
the current source.

Review of that adaptation established `HELIX_CLEAN_EXECUTION_BASELINE_V1` as a
portfolio-wide invariant. The work-entry evidence now distinguishes the dirty
source checkout from the clean canonical execution checkout and exposes an
`OPEN`/`CLOSED` mutation gate. The work result separately accounts for every
ending dirty path attributable to Standard 002; none is attributed to the
pre-existing primary-checkout state. The research note
[`2026-09-27-clean-execution-baseline.md`](../../research-notes/2026-09-27-clean-execution-baseline.md)
records the observation, interpretation and open question.

## Standards comparison

Before this task, repo-cp had repository enrollment and audit schemas, a
read-only operator-action consumer, agent work guidance, and prose-only usage
governance. It did not have a schema-backed work-entry/result pair, workflow
status relationships, or permanent upstream-first and writer-boundary standards.

This task adds those concepts without extending Foundation V1, changing
enrollment, or creating an executor. The new CLI operations validate bounded
stdin and emit non-authorizing receipts. Status nodes reuse the audit vocabulary
where it represents findings, while keeping workflow progress separate so an
active task is not confused with audit `UNKNOWN` or `DRIFT`.

## Usage record

- Exact plan percentage before/after: `UNKNOWN` — no authoritative meter was
  exposed to repository tooling.
- Exact model-token usage: `UNKNOWN` — no authoritative counter was exposed.
- Network use: direct canonical parity query and read-only Git fetches only.
- Repository writes: local task files in the original checkout and the private
  task checkout; no commit, push, merge or peer write.
- Execution: local schema checks and synthetic tests only; no declared action,
  peer validator, deployment, service, or storage mutation.
- Live effects: NONE.

See [`WORK_PROTOCOL_USAGE.md`](../WORK_PROTOCOL_USAGE.md) for the operator and
agent usage procedure.
