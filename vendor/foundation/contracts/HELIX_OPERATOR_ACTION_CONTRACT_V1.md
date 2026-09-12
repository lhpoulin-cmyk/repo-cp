# HELIX_OPERATOR_ACTION_CONTRACT_V1

Contract version: `1.0.0`. Authority: `foundation-cp`. Status:
`REPOSITORY_CONTRACT_ONLY`. Established under Louis's explicit authorization
on 2026-09-11 in response to the repo-cp Foundation handoff.

## Purpose and authority

This contract defines a public, pre-execution operator-action declaration and
its terminal presentation. It gives Louis the information needed to review a
proposed action or understand a stop. It neither executes commands nor grants
permission. Local operator authority remains above auth-cp, automation consumers
and managed environments. Auth-cp retains identity, grant and custody authority;
consumers retain their domain implementation. Foundation owns these shared
presentation and declaration semantics.

`READY_FOR_REVIEW` means the declaration is complete enough to present. It does
not mean operational readiness, authorization, verified capability or acceptance.
`BLOCKED` means no command may be presented. Neither status permits execution.
The renderer cannot enroll repositories, invoke a shell, elevate, issue/adopt
credentials, run reauth, access custody or open an APPLY gate. An exact APPLY
string, including the reserved B70 acknowledgement, remains subject to its
separate owning-authority gate. Execution profiles and signer, ledger, serial,
independent integrity and recovery contracts retain all existing requirements.

## Versioned interfaces

* [Schema](../schemas/operator-action-v1.schema.json)
* [Registry](../registries/operator-action.json)
* [Validator and reference renderer](../src/operator_action.py)
* [CLI](../tools/render_operator_action.py)
* [Conformance tests](../tests/test_operator_action.py)
* [Synthetic fixtures](../tests/fixtures/operator_action/ready.json)

The schema is closed: every listed property is required and unknown properties
are rejected, including inside source and command objects. Schema validation
alone is insufficient; the reference validator's parsing, safe-text and pin
checks are normative too. Consumers must reject unsupported versions rather
than drop fields, guess defaults or silently downgrade.

| Field | Required meaning |
| --- | --- |
| schema_version, contract_id, contract_version, authority | Exact schema constants; names confer no authority. |
| source | Separate exact Foundation repository and consolidated doctrine content Git revisions. |
| repository, target, operation | Owning repository, stable logical target and exact proposed operation; never infer target from incidental addressing. |
| phase | PREPARATION or REVIEW; describes proposal work, never execution. |
| status, stop_reason | BLOCKED requires a substantive reason and null command; READY_FOR_REVIEW requires null reason and a command. |
| evidence | Collected public evidence or opaque references; empty means NONE, not a successful observation. Distinguish synthetic, repository and live evidence explicitly. |
| command | Null when blocked; otherwise exact shell, working_directory and command text for manual review. |
| scope, effects, risks, downtime, removals | Explicit bounded impact declarations, each a nonempty list. Use NONE only when established; use UNVERIFIED with explanation for unresolved facts. |
| preconditions | Identity, revision, capability, authorization and safety conditions the owning consumer must independently establish before execution. |
| success_evidence, failure_evidence | Exact observable acceptance and failure criteria; a proposed criterion is not collected evidence. |
| recovery, rollback | Recovery from interruption/failure and reversal limits. Explain irreversible effects; never invent a safe rollback. |
| return_output | Exact public output or reviewed evidence Louis should return, with exclusions for sensitive output. |
| execution_occurred, mutation_authorized | Both must be boolean false. An action already executed requires a separate owning-domain result record. |

All strings are nonblank printable ASCII, at most 4096 characters. No control
characters, tabs, line breaks, ANSI escapes, Unicode directional controls or
invisible characters are accepted. Lists contain at most 64 items. This v1
restriction makes the single-line command and terminal labels unambiguous;
unsupported text fails closed rather than being altered. Commands needing a
script must name a separately reviewed, revision-pinned script. The renderer
does not rewrite, quote, expand, wrap, combine with `cd`, or execute command text.
Bash and PowerShell are presentation shell identifiers, not proven adapters.
The working directory is displayed separately and must be established manually.

Only reviewed public metadata belongs in declarations, commands and return
output. Passwords, tokens, private keys, raw environments, custody payloads and
secret-bearing dumps are prohibited. Character/schema validation is not a
secret detector, command safety analyzer, provenance verifier or authorization
engine. Producers must review content before invoking this renderer. An opaque
reference alone cannot establish authenticity, freshness, authority or safety.

## Consumption and terminal behavior

Consumers independently approve and pin the canonical Foundation repository
revision and the consolidated doctrine content revision separately. Verify
canonical repository identity and retrieve the contract, schema, registry,
renderer and fixtures from that exact repository revision; record their SHA-256
digests in consumer evidence. Never choose trusted pins from the action itself.
The doctrine content revision identifies the consolidated doctrine and registry;
it need not equal the repository revision introducing this additive contract.
Review intervening changes and compatibility before accepting new pins.

`load_action(bytes)` accepts at most 131072 UTF-8 bytes and rejects duplicate
JSON keys at every depth, nonfinite constants, malformed encoding and JSON.
`validate_action(action, expected_source=...)` requires independent expected
pins and returns declaration conformance with execution, mutation authorization
and live acceptance all false. Consumers loading JSON themselves must preserve
these strict parsing rules. Comparison proves only equality to caller-supplied
pins; callers remain responsible for authenticating those pins and the code.

`render_action` first validates the complete declaration, then returns one
stable newline-terminated string. It never mutates the input. The exact label
order, indentation, command line and final negative execution/authorization
statements are fixed by the reference implementation and checked-in golden
fixtures. No timestamps, color, shell prompts, Markdown fences or environment
lookups are added. Command text appears as one exact line. Prose items remain
indented under their label and cannot inject terminal lines.

The CLI consumes stdin and requires `--foundation-revision` and
`--doctrine-revision`. Successful rendering returns exit 0. Invalid declarations
return exit 2, no stdout, and a fixed public blocker/reason code on stderr;
rejected payload content is never echoed. CLI argument errors also return 2.
A consumer must not display a partial action or fall back to a less strict
renderer on failure. Rendering success never requests automatic execution.

A synthetic demonstration (the hashes below are fixture pins, not authority):

```sh
python3 -B tools/render_operator_action.py \
  --foundation-revision 1111111111111111111111111111111111111111 \
  --doctrine-revision 2222222222222222222222222222222222222222 \
  < tests/fixtures/operator_action/ready.json
```

## Compatibility and evidence

This is the first version of this interface. It is additive to consolidated
Foundation doctrine `1.0.0`; VERSION and the consolidated doctrine content
remain unchanged. No earlier universal operator-action contract is superseded.
The repo-cp missing-contract handoff is an acceptance input, not prior doctrine.
Existing domain-specific auth-cp mutation gates and Ansible acknowledgement
checks remain independent requirements, not interchangeable implementations.

Consumers claiming v1 conformance must pass the positive/golden and fail-closed
cases, including malformed input, unknown fields/version, pin mismatch,
unsafe terminal text, blocked commands and false execution/authorization claims.
Changing required semantics or output requires explicit version/compatibility
review; consumers must not silently accept an expanded interface. A future
execution/result protocol needs its own contract; this v1 never gains an
AUTHORIZED status by inference.

The Python reference implementation is implemented and tested with synthetic
public declarations. Fleet consumers, platform adapters, enrollment and live
behavior remain unverified. Foundation publication enables repo-cp to review
and implement consumption; it does not complete repo-cp bootstrap acceptance.
Live observations, live mutations, issuance, adoption and secret access: NONE.
