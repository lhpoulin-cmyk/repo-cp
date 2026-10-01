# repo-cp audit remediation handoff

Date: 2026-09-23
Status: PREPARED; implementation not started
Owner: repo-cp; operator retains acceptance, exception and publication decisions
Baseline: `b9e528dd5088309e69b2718a667d05be3c1b7f6f`
Classification: public engineering handoff; private voice material excluded

## Outcome and authorization

Turn confirmed audit findings into small, reviewable fixes while preserving the
read-only runtime, exact Foundation snapshot, source integrity and honest audit
states. The current operator request authorizes preparation of this handoff.
It does not itself select the design alternatives below or authorize their
implementation, peer changes, enrollment, deployment or publication.

A future authorized implementation should complete ordinary inspection, coding,
testing and supported retries autonomously. Present concrete proposals at the
listed decision boundaries. Do not ask the operator to perform available local
checks or rediscover accessible documents. No action has been delegated or sent
to another agent by creating this document.

## Source record and confidence

All repository source references below were inspected at the baseline commit in
an isolated checkout. The original workspace contains unrelated and previously
published dirty material; do not stage it wholesale or reset it.

| Source | Consequence |
| --- | --- |
| `AGENTS.md`, `OWNERSHIP.md`, `docs/OPERATIONS.md` | Retain ownership, runtime restrictions, mandatory checks and independent publication verification |
| `docs/AGENT_WORK_CONTRACT.md`, release 1.0.0 | Governing adopted contract; candidate publication does not change adoption |
| `docs/AGENT_WORK_CONTRACT_CANDIDATE.md`, 1.1.0-rc.3 | Artifact requiring integrity verification; not silently promoted to governing release |
| `pins/agent-work-contract.json`, `pins/agent-work-contract-candidate.json` | Released/candidate content identities and candidate companion digests |
| `tools/validate`, `src/repocp/cli.py`, `src/repocp/safety.py` | Missing work-contract digest checks and discarded public denial causes |
| `src/repocp/audit.py` | Unconditional offline RC009 UNKNOWN, peer-specific checks and restricted branch parser |
| `src/repocp/consumer.py` | Foundation trust pins and combined validation conditions |
| `src/repocp/publication.py`, `tests/test_hardlink_policy.py` | Unprivileged execution boundary and publication/recovery test behavior |
| `requirements.txt`, `.github/workflows/` | Direct-only dependency pins and no explicit supported-Python matrix |
| `docs/FILE_INTEGRITY.md`, `docs/FOUNDATION_REQUESTS.md` | Existing safety requirements and unresolved Foundation interfaces |

The operator supplied an external audit of the same commit. Its 86% coverage
measurement and count of 20 root-run failures have not been independently
reproduced. Its author reported unavailable private peer access and synthetic
peer testing; those results do not establish actual fleet state. Our prior
unprivileged validation passed 90 repo tests and 13 Foundation reference tests.
Source inspection confirmed the structural findings below; it is not a claim
that every proposed remedy has been qualified. Use current file symbols rather
than relying on the audit's line numbers.

## First implementation package: integrity and diagnosability

### R1 — Verify flagship artifacts during validation

Add bounded verification for the released work contract, candidate and every
required public companion. Use the existing safe public read mechanism, strict
JSON handling and reviewed expected artifact set. Validate metadata types,
release/path consistency and SHA-256 shape before comparison. Reject missing or
unexpected companion entries rather than silently reducing coverage.

Do not let a modified manifest nominate arbitrary files for reading. Reject
absolute paths, traversal, symlinks and protected/private targets. Never repair
a mismatch by regenerating the expected hash automatically. Updated content and
its release record require the existing reviewed release process. A matching
local digest proves consistency, not authenticity against an independently
trusted remote source.

Acceptance: valid released and candidate records pass; changing one byte in each
artifact fails; missing, malformed, duplicate-key or unsafe records fail closed;
removing a required companion cannot bypass verification. Tests must demonstrate
that private or outside-scope bytes are never read or disclosed. Preserve release
1.0.0 bytes and all 19 accepted Foundation artifacts. Decide explicitly whether
this check belongs only to development validation or also a documented runtime
validation surface; do not silently add runtime behavior.

### R2 — Preserve reviewed public reason codes

Keep the existing top-level blocker identity where compatible and add a stable
public reason field for known `Denied` codes. Use an explicit reviewed allowlist;
uppercase formatting alone does not prove safe disclosure. Unknown denial text
and other exceptions retain a constant generic fallback. Never echo exceptions,
paths, arguments, payloads or tracebacks from rejected input.

Acceptance: representative known failures expose only their approved codes;
unknown uppercase strings, strings containing paths/newlines and arbitrary
exceptions reveal no supplied content. Failures produce no partial stdout and
retain documented exit behavior. Update tests and diagnostic documentation to
the deliberately changed interface; retain non-disclosure assertions. Do not
alter vendored Foundation errors or golden fixtures.

### R3 — Make the validation environment explicit

Prefer an early, safe reason code when full publication qualification is run as
root or with set-ID identity, with instructions to use an ordinary unprivileged
environment. Keep production privilege rejection intact. Do not silently turn
skipped qualification into full-suite PASS or change privilege policy to satisfy
a container. If partial root-safe testing is later supported, label its omitted
qualification as NOT_RUN and give it a distinct completion claim.

Acceptance: test the preflight through controlled identity mocks or safe child
processes without obtaining privileges. It rejects before qualification work;
an ordinary unprivileged run exercises the complete existing suite, including
negative privilege-rejection tests. Account for direct test-runner invocation
in documented instructions so its limits are clear.

## Second package: reproducibility and narrow correctness

### R4 — Lock dependency resolution and test supported Python

Prepare a hash-locked installation path covering the complete resolved graph,
including environment markers. Record the resolver, Python/platform scope and
regeneration procedure. Verify clean installation with hash enforcement in CI.
Use official version-matched documentation and verify immutable action revisions
when updating CI; this handoff does not prescribe unverified action pins.

Exercise the documented minimum Python 3.11 and the existing CI Python 3.12,
using an unprivileged runner. If the supported range is narrowed, that is an
explicit compatibility decision. Acceptance includes successful clean installs
and tests on both versions, rejection of an altered artifact hash, and no
undeclared network access from tests. Avoid unrelated dependency upgrades.

### R5 — Accept safe valid branch names

Replace the overly restrictive branch parser with a bounded implementation of
the relevant Git ref-name rules; do not merely allow every string containing a
dot. Runtime code must not spawn Git. Test `release/1.0`, loose and packed refs,
malformed refs, traversal, control characters and unsafe path components.
Preserve detached-HEAD semantics and branch-versus-revision distinctions.

### R6 — Centralize versions and improve internal diagnosis

Assess version constants individually: tool version and policy version have
different owners and must not be conflated. Derive each from a reviewed source
without import-time I/O or changes to historical receipt interpretation.
Split compound pin checks where distinct constant reasons aid remediation.
Acceptance preserves rejection behavior, accepted snapshot bytes, receipt
compatibility and no-disclosure properties. Coordinate reason codes with R2.

## Design decisions: prepare proposals before changing semantics

| Item | Recommendation and required decision | Acceptance for an approved design |
| --- | --- | --- |
| R7: RC009 remote freshness | Retain UNKNOWN until evidence exists. Define an offline supplied-evidence interface before implementation; do not relabel missing freshness as NOT_APPLICABLE merely to obtain PASS. | Bind canonical repository, exact ref and revision, capture time, expiry/freshness policy and provenance. Reject malformed, mismatched, stale or future evidence. Define replay and trust limits. Reading a supplied snapshot must not contact a network or prove current state beyond its observation time. |
| R8: Declarative cross-pin checks | Propose a bounded registry/schema extension owned by repo-cp. Preserve existing auth/ansible checks and independent trust anchors. | Allowlisted files and bounded selectors only; no code, expressions, arbitrary paths, network or peer execution. Define schema version, migration and equivalence tests. No producer-selected trust pin; no peer pin edits to make results pass. |
| R9: Missing peer checkout | Distinguish an absent checkout from unsafe or inaccessible content; decide report shape and compatibility before short-circuiting. | Absence reports scoped UNKNOWN with useful coverage information. Permission denial, symlinks and unsafe paths remain distinct. Existing/required-file corruption cannot become harmless absence. Test exit codes and structured consumers. |
| R10: Symlinked fleet-root aliases | This changes a deliberate path-security boundary. Prepare the supported-platform and trust-boundary proposal first. | If aliases are admitted at the outer boundary, establish the opened directory identity and handle retargeting/races. Continue rejecting unsafe traversal beneath it. Do not add blanket `resolve()` and assume safety. |

RC009 does prevent aggregate PASS for a nonempty selected peer scope today.
That is an honest limitation of the full claim. Exit 1 deliberately combines
DRIFT and UNKNOWN; structured findings still distinguish them. A new local-only
summary or exit contract needs explicit scope and compatibility decisions.

## Maintenance proposals, not prerequisites

- R11: Assess moving the publication reference to a clearly labeled reference
  area. It already has documented synthetic/reference scope. Do not invent a
  production consumer or execute it live to justify its existence. Preserve
  imports, tests and references if relocation is approved.
- R12: Add a short purpose/quickstart block while preserving the operator's
  explicit flagship positioning and the distinction between contract publishing,
  fleet audits and file-integrity policy. Avoid burying either audience's entry
  point. Documentation examples must not imply deployment or live authorization.

## Execution, validation and delivery

Implement independently reviewable packages after authorization. Before editing,
refresh canonical HEAD, upstream, status and governing instructions; compare any
newer changes against this baseline. Use an isolated task checkout and preserve
other work. Inspect relevant tests before changes. Do not weaken assertions,
expected outcomes, thresholds or qualification to manufacture success.

Run focused positive and failure-boundary tests, then `tools/validate`, required
syntax/integrity/secret checks, local link checks and `git diff --check`. Inspect
the full staged diff and outgoing commit range. Pin updates and diagnostic
interface changes need explicit rationale and corresponding acceptance evidence.
Runtime remains read-only: no processes, networks, credential access, peer
validators, elevation or repository writes. Test fixtures remain local/synthetic.

Delivery must identify the source and output revisions, changed public paths,
checks run and NOT_RUN with reasons, actual delivery stage and unresolved design
decisions. Record both Foundation pins, unchanged artifact integrity and unchanged
enrollment scope. Only claim publication after direct canonical remote evidence.
Report `Live effects:` including any remote push, PR or comment. Never include
the private voice profile in commits, test scans or handoff evidence.

## Next action

The operator or receiving task should select the first implementation package
(R1–R3 is recommended) and its delivery scope. Prepare R7–R10 as concrete design
proposals with compatibility and trust-boundary analysis before requesting their
decisions. Other packages may proceed independently when authorized.

Handoff preparation: local/uncommitted. No remediation code, dependency changes,
CI changes, peer changes or publication performed.
Live effects: NONE
