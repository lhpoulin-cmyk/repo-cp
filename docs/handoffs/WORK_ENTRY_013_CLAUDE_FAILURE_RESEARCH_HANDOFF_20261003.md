# Work Entry 013 — separate Claude failure research handoff

Status: `PRESERVED / NOT STARTED / NO EXECUTION AUTHORITY`

This handoff separates later Claude failure analysis from the completed durable
recovery hardening. It authorizes no prompt, model, adapter or usage-limit
change and no model invocation.

## Evidence set

- Original bounded source packet: packet SHA-256
  `f5bb1cd016bd36f847d9129efd2057b6a36ddc9d67bbddce56e6384e07966f41`
  in helix-offload
  `docs/evidence/work-entry-013-claude-stream-repair-20261003/`.
- Model instructions and generated-content contract: helix-offload
  `docs/contracts/CHANGE_SUMMARY_V1.md` and the exact workflow/preview/grant in
  that prepared evidence directory, as published before the attempt.
- Attempt and sanitized envelope: helix-offload
  `docs/evidence/work-entry-013-claude-stream-live-002-20261003/attempt.json`
  and `response-envelope-public.json`.
- Complete returned output and private client envelope: the migrated durable
  private copy bound by migration metadata SHA-256
  `fb19fa241d28392bb0e9a66cce34d8582b9c905ec5406f399b47851c1649242c`.
  Access remains private and must use the recovery-domain inspection path; raw
  material is not published.
- Connector outcome and usage: helix-offload
  `docs/evidence/work-entry-013-claude-stream-live-002-20261003/connector-outcome.json`
  and `receipt.json`.
- Authoritative result: helix-offload
  `docs/evidence/WORK_ENTRY_013_CLAUDE_STREAM_LIVE_002_RESULT.md`.
- Separately labelled output-shape diagnostic: helix-offload
  `docs/evidence/work-entry-013-claude-stream-live-002-20261003/offline-output-diagnostic.json`.
- Human disposition: helix-offload
  `docs/evidence/work-entry-013-claude-stream-live-002-20261003/human-disposition-rejected.json`.

All public helix-offload references above are fixed at canonical commit
`3f99e0fda9a84b99b52019cf463a061da906215a`; the attempt itself was first
published at `f24cdc317c364aa01c72eac162fb1281fcafa2f5` and remains unchanged.

## Preserved observations

- The attempt is
  `work-entry-013-claude-change-summary-live-002-attempt-001`.
- Outcome: `SENT / RESPONSE_RECEIVED / GENERATION_COMPLETED / DERP_REFUSED`.
- Requested and observed model: `claude-haiku-4-5-20251001` through Claude Code
  2.1.283 and the existing claude.ai Pro subscription.
- One client run was observed; provider request count remains `UNKNOWN`.
- Observable retries: 0; no tool or MCP event occurred.
- Completion: `end_turn`, not truncated; elapsed 5,550 ms.
- Usage: 5,202 input, 372 output and 5,574 total tokens. Client-reported list
  cost: $0.012261. Actual marginal subscription charge: `UNKNOWN`.
- DERP authoritatively refused `USAGE_LIMIT_EXCEEDED` against 4,000 input and
  4,600 total tokens before generated-content parsing, postflight or assembly.
- No artifact exists. Louis's human disposition is `REJECTED`; preparation and
  review durations remain `UNKNOWN`.
- The separate offline diagnostic found that the unchanged text was not the
  required JSON object. It is diagnostic evidence, not retroactive postflight.

## Research questions

1. Trace the exact prompt/data boundary and determine why a historical
   `authority` field in source data was interpreted as current permission to
   pause. Keep historical authority facts, current host-enforced execution
   authority, model instructions and untrusted source text separate. Do not
   remove or rewrite historical facts merely to improve model behavior.
2. Account for the 5,202 reported input tokens across visible packet content,
   client/system overhead, tool or policy scaffolding, cache categories and any
   categories the client does not expose. Packet bytes alone do not establish
   causation.
3. Treat the 4,000-input and 4,600-total checks as retrospective detection:
   consumption had already occurred. Identify only documented preventive
   controls; do not relabel post-response refusal as a provider-side cap.
4. Compare the complete private output with the published sanitized envelope
   and connector outcome without exposing raw material or changing historical
   evidence.
5. Distinguish model behavior, prompt design, client behavior and upstream
   defects. The prior reported defect is a possible explanation, not a proven
   root cause.

## Completion boundary

A later research task may produce findings and a reviewed design. It must not
change the current prompt/model/contract/limits/adapter, issue a model request,
or treat this rejected attempt as accepted without separate implementation and
execution authority. Work Entry 014 stays parked.
