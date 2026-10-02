# Work Entry 014 — ChatGPT/OpenAI implementation and comparison

Status: `PARKED`

Priority: `GREEN` (normal attention)

Scheduling eligibility: `INELIGIBLE_STATE`

## Objective and sequence

Implement and evaluate ChatGPT/OpenAI only after Work Entry 013 establishes the
Claude comparison following the Work Entry 010 local baseline. Compare the same
bounded extraction workload, acceptance criteria and measurement definitions
against both established baselines.

Keep OpenAI API billing separate from ChatGPT or Codex subscription allowance.
The published OpenAI Responses adapter is preserved, as are the documented
limitations of subscription-backed clients: no path is suitable unless its
supported interface can enforce the required tool, retry, fallback, deadline and
output boundaries. Do not assume ChatGPT can redirect internal reasoning or
subscription usage to an external API, and do not repurpose undocumented auth.

No live request, account/credential change, subscription/API purchase or adapter
expansion is authorized by this parked registration.

Dependency: Work Entry 013 Claude implementation and comparison.

Live effects: NONE.
