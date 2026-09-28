# Usage advice: a bounded deterministic governor

repo-cp provides a small, advisory-only tool for one operational question:

> Given an explicitly observed constrained-capacity window, its reset timing,
> canonical Work Entry context, and conservative work-size information, does
> capacity evidence presently support considering this work?

It does not answer whether work is authorized. It does not dispatch work,
change lifecycle state, inspect an account, or write a ledger. Every
machine-readable result says `authority_effect: NONE`.

## Inputs and trust boundary

`repo-cp usage-advice` reads one JSON observation from stdin or an explicitly
named file. It never searches for observations. The initial source class is
`PROVIDER_UI_MANUAL`: the operator transcribes a provider-reported percentage,
timestamp, and reset. Manual entry is intentional. It keeps credentials,
private session logs, provider APIs, and format-sensitive collectors outside
the decision path.

An observation has this form:

```json
{
  "schema_version": 1,
  "protocol": "HELIX_USAGE_OBSERVATION_V1",
  "windows": [
    {
      "provider": "openai",
      "resource_pool": "codex-plan",
      "window_id": "weekly",
      "semantic": "REMAINING",
      "percentage": 72,
      "observed_at": "2026-09-27T08:00:00Z",
      "reset_at": "2026-09-29T08:00:00",
      "reset_timezone": "America/Detroit",
      "display_resolution": 1,
      "source": "PROVIDER_UI_MANUAL"
    }
  ]
}
```

`semantic` is mandatory and is exactly `REMAINING` or `USED`. Bare values such
as `72%` are rejected. `USED` may be normalized to remaining capacity only
because its meaning is explicit. Percentages outside 0 through 100, timestamps
without a usable timezone, unsupported source classes, duplicate windows, and
unsafe input files are rejected. Display resolution is preserved when known.

Each `(provider, resource_pool, window_id)` is independent. Percentages are
never added across windows or providers. When more than one pool or window
could apply, the operator must select it with `--resource-pool` and
`--capacity-window`; otherwise the answer is `REVIEW`.

## Work and topology

The command requires a Work Entry ID and exactly one of:

- `--size S`, `--size M`, or `--size L`; or
- `--expected-percentage-points NUMBER`.

S, M, and L are ordinal labels. repo-cp has no empirical mapping from them to
percentage points, so ordinal input produces `REVIEW`. It never invents a
mapping.

The existing `registries/work-topology.json` remains the only queue and
lifecycle source. The tool validates that canonical topology and reports the
Work Entry's state, priority, dependencies, and scheduling eligibility before
capacity. An absent, parked, paused, blocked, or complete Work Entry cannot
become eligible through headroom. Priority names `GREEN`, `YELLOW`, and `RED`
remain topology terms and are not capacity labels.

## Capacity and advice

Capacity is reported as:

- `ADEQUATE`: explicit expected consumption fits both remaining capacity and
  the current pacing heuristic;
- `CONSTRAINED`: explicit expected consumption exceeds remaining capacity or
  the current pacing heuristic;
- `STALE`: the selected observation is older than 12 hours; or
- `UNKNOWN`: evidence cannot support a capacity conclusion.

Advice is narrower still:

- `FIT`: capacity evidence does not presently argue against considering an
  otherwise eligible Work Entry;
- `REVIEW`: evidence is insufficient for deterministic capacity advice; or
- `DEFER`: topology is ineligible or present capacity evidence argues for
  preserving constrained capacity.

`FIT` is not authorization. All advice is informational and has no lifecycle,
dispatch, mutation, or publication effect.

For a fresh selected window, the tool calculates:

```text
remaining percentage points / fractional days until reset
```

The result is labeled `pacing_heuristic_percentage_points_per_day`. It is not
provider billing truth, token or cost accounting, or a prediction of future
availability. No missing observations are interpolated. Missing observations,
stale evidence, a passed reset, unclear window selection, and ordinal-only
sizing fail closed to `REVIEW` unless topology already requires `DEFER`.

Examples:

```sh
./tools/repo-cp usage-advice --work-entry 006 --size S --input observation.json
./tools/repo-cp usage-advice --work-entry 006 \
  --expected-percentage-points 5 --json < observation.json
```

Human-readable output is the default; `--json` emits deterministic structured
output. The optional `--propose-ledger` field is included in the same stdout
result. It never creates a tracked file or database. `--after-input` can supply
a later observation, and `--attribution-context` records whether the operator
knows the interval was `EXCLUSIVE`, `CONCURRENT`, or `UNKNOWN`. Attribution
remains `UNKNOWN` without explicit exclusivity, or when concurrency, a reset,
missing evidence, invalid order, or unexplained capacity increase contaminates
the interval. Before and after records preserve original semantics, display
resolution, window identity, and timestamps.

## Deliberately deferred seams

The observation protocol and structured stdout are narrow seams for a future,
separately authorized adapter. Provider APIs, ccusage or other commodity
analytics, automatic session correlation, telemetry enablement, persistent
storage, billing reconciliation, dashboards, schedulers, and automated
dispatch are deferred. None is in the operational decision path. A later
adapter may translate reviewed evidence into this input or consume this output
without making repo-cp's lifecycle authority depend on that adapter.

## Operator observation: Work Entry 006

The following is Louis's operator/design observation, not a normative repo-cp
requirement or universal rule.

Louis considers Work Entry 006 a particularly useful example of using
available tools, external open-source research, and explicit cost-benefit
analysis to reduce an initially larger engineering idea to a much smaller,
locally controlled implementation. The valuable sequence was:

```text
inspect the problem
  -> determine what evidence actually exists
  -> research what GitHub/open-source software already solves
  -> compare reuse against custom implementation
  -> analyze complexity versus demonstrated operational value
  -> implement only the smallest missing local capability
```

Louis sees this as supporting a personal development hypothesis: locally
generated software, supported by the broader GitHub/open-source ecosystem, may
represent an increasingly important development model. Local software can be
generated for a specific operator and environment while mature public projects
provide reusable implementations, architectural precedent, validation targets,
and evidence that prevents unnecessary reinvention.

Work Entry 006 is retained as a case study for evaluating that hypothesis in
future work. The observation does not establish a universal policy.
