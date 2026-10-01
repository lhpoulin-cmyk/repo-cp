# Future feature record: outcome forecasting and calibration

Recorded: 2026-10-01

Status: `DEFERRED_RESEARCH_ROADMAP` — not implemented, qualified, admitted, or
authorized for execution

Product: helix-offload

Intended layer: portable evidence contract plus DERP policy input; any later
routing effect remains deployment-policy controlled

## Purpose

Louis's shorthand, “Polymarket everything,” means making outcome predictions
explicit before execution, resolving them against actual receipts, and learning
which candidates deliver reliable net savings. It does **not** mean financial
trading, markets, wagers, tokens, or a Polymarket integration.

The proposed feature would attach one immutable forecast to a logical job before
execution. Where the evidence supports a prediction, it may estimate:

- acceptance probability;
- frontier-continuation probability;
- total job cost;
- elapsed latency;
- human review effort; and
- net frontier displacement.

Every forecast would bind its provenance, candidate, job family, work lane,
evidence basis, resolution criteria, forecast time, and the exact job/evidence
identities available at that time. Known quantities remain deterministic facts,
not forecasts.

## Resolution and calibration boundary

A forecast would be resolved against immutable postflight results, the recorded
human disposition, and observed provider usage. Unresolved outcomes remain
unresolved. Observed facts remain separate from estimated counterfactuals such as
the frontier usage that might otherwise have occurred.

Calibration assessment should use outcome-appropriate scoring, for example a
Brier score and reliability view for binary events and separately reported error
or interval coverage for numeric quantities. Small cohorts, changing candidates,
selection effects, censoring, and incomparable jobs must be stated. A minimum
sample count is a decision threshold, not statistical proof.

The first slice, if later authorized, should permit exactly one supplied forecast
per job. It should not add trading mechanics, competing forecasting agents,
automatic retries, background dispatch, or paid frontier reasoning merely to
forecast small tasks. Forecast generation may be deterministic, externally
supplied, or absent when evidence is inadequate.

## Authority and product boundaries

- Qualification establishes demonstrated suitability for a bounded workload.
- Forecasting estimates a particular job's outcome.
- Admission determines whether supplied candidate evidence satisfies its
  contract.
- An execution grant separately authorizes one bounded adapter attempt.
- Postflight and human disposition determine whether the result is accepted.

None of qualification, forecasting, admission, execution, or acceptance implies
another. An uncalibrated or missing forecast must not silently control routing.
Any future policy use requires an explicit, versioned consumer policy, visible
fallback behavior, and an evidence-backed calibration threshold.

## Deferred acceptance questions

Before implementation, review must establish:

1. which job families have enough comparable resolved receipts to support a
   forecast;
2. which quantities are observed, deterministic bounds, estimates, or
   counterfactuals;
3. how forecast identity and immutability bind to the current workflow and
   receipt contracts;
4. how non-resolution, selection bias, model/version drift, and human-disposition
   changes are represented;
5. which scoring rule and reporting window match each forecasted quantity; and
6. whether measured decision benefit exceeds collection, review, and maintenance
   overhead.

## Current disposition

`DEFER`. Complete the explicit hosted path, obtain separately authorized live
acceptance, and collect a comparable cohort before designing this contract. The
current build must not add forecasting fields, forecast-driven routing,
qualification packs, caching, MCP, a daemon, or any trading mechanism.

Provenance: operator-supplied future-feature framing recorded during Work Entry
010. This record is roadmap evidence only and is not local implementation or live
acceptance evidence.
