# Synthetic contribution attribution V1

Status: local pilot, not a universal Foundation contract or execution gate.
Implementation baseline: repo-cp `4f47ec6cc4744eaf2a158009c57553a223432cdd`.
Identity dependency: auth-cp `3bdcde14bb7c0d77775cfeb2d1bd5571488d6f2a`.
Louis authorized local implementation and isolated synthetic Git tests only.
No implementation commit, publication, peer edit, credential or workstation
configuration change is authorized. Preserve the dirty source checkout.

## Interface and ownership

`tools/repo-cp attribution-report` accepts one bounded JSON object on stdin and
emits deterministic JSON on stdout. Only fixed errors go to stderr. The reporter
loads its installed code/schema but never discovers files, invokes subprocesses,
reads credentials/configuration/environment, accesses networks or writes files.
The test harness may invoke Git and create disposable local commits/worktrees in
private test-owned temporary directories with synthetic configuration. It must
not authenticate, push, contact networks, invoke credential helpers or change
real repositories. Temporary test effects are not live operations.

repo-cp owns this local format, normalization and reporting. auth-cp owns principal,
account, key/credential bindings and authorization boundaries; ws-cp owns eventual
workstation integration. Registry input is a supplied declaration, not a trust
root. Reuse existing principal IDs. In particular `human.louis` remains proposed/
unverified: this pilot neither creates that principal nor elevates its status.
Additional humans follow the same schema. Fixtures use synthetic identities only.

## Complete data definitions

The JSON Schema is normative for closed object shapes, types and cardinalities;
this document defines relationships and meaning. All fields below are required
unless marked optional. IDs are nonempty ASCII identifiers (letters, digits,
underscore, dot, colon, slash, hyphen), at most 128 characters. Revisions use full
lowercase `sha1:` plus 40 hex digits or `sha256:` plus 64 hex digits. A local-only
repository uses a stable repository ID; a hosting URL is not required. Publishing
adds a separate hosting binding, never a new identity for the same repository.

```typescript
type Reason = "not-recorded" | "not-supplied" | "not-exposed" | "withheld"
            | "unresolved" | "stale" | "not-applicable";
type Role = "design" | "draft" | "implement" | "review" | "execute";
type GitIdentity = {name: string; email: string};
type RepositoryRef = {id: string};
type CommitRef = {repository: RepositoryRef; oid: string};
type WorkRef = {repository: RepositoryRef; id: string; revision: string};
type Scope = {kind: "commit"; target: "self" | CommitRef}
           | {kind: "work"; target: WorkRef};
type Actor = {id: string; kind: "human" | "agent" | "unknown";
              principal: string | null; tool: string | null; models: string[]};
type Model = {id: string; deployment: "local" | "hosted" | "unknown";
              provider: string | null; model_id: string | null;
              tag: string | null; resolved_digest: string | null;
              revision: string | null; quantization: string | null;
              unavailable: {[field: string]: Reason}};
type Declaration = {claim: string; state: "declared"; by: string;
                    method: "statement-v1"; ref: string};
type Unknown = {claim: string; state: "unknown"; reason: Reason};
type Observation = {claim: string; state: "observed"; by: string;
                    method: string; ref: string; at: string};
type Claim = {id: string; subject: string; predicate: string; value: Value;
              scope: Scope; evidence: (Declaration | Unknown)[]};
```

Every null model descriptive field has exactly one unavailable reason; populated
fields have none. Local-model tag, resolved artifact/manifest digest, revision
where exposed and quantization are distinct. Digest must be `sha256:` plus 64 hex
digits when known; `none` quantization means known unquantized. Hosted identifiers
are only those actually exposed. Never infer a model from product or Git identity.
Local actor/model IDs cannot be `record` or overlap one another. Human actors
require tool null and models empty. Agent models empty explicitly
means no identified model, not proof that no model was used. Principal null means
unresolved. Principal references are claims, not authenticated bindings.

All predicates and their complete value definitions:

```typescript
participation: {role: Role; present: true | false | null}
coverage: "complete" | "partial" | "unknown"
responsibility: "accepted" | null
authorization: {decision: "approved" | "denied" | null; action: string}
provenance: {relation: "rebased-from" | "cherry-picked-from" | "squashed-from"
                       | "copied-from" | "merged-from";
             source: CommitRef | null}
identity-binding: {registry_revision: string; binding_id: string} | null
descriptor-field: {pointer: string; expected: string | null}
git-header: {field: "author" | "committer"; name: string; email: string}
signature: {signer_reference: string | null; valid: true | false | null}
commit-execution: {executor: string | null;
                   mechanism: "git-cli" | "desktop-client" | "hosting-web"
                              | "hosting-api" | "automation" | null;
                   acting_principal: string | null;
                   unknown: {[field: string]: Reason}}
```

Participation, responsibility, authorization and identity-binding subjects reference
local actors.
Descriptor subjects reference an actor/model and pointer names an existing scalar
string/null field (one `/field`, no nested traversal). Other subjects are `record`.
Git-header/signature require commit scope. Exactly one logical commit-execution
claim is required, scoped to containing commit self. Its executor is an actor ID
or null. Its unknown map names exactly the null executor/mechanism/acting_principal
fields. A partially known tuple is a declaration with explicit unknown fields;
a wholly unknown tuple requires Unknown evidence. Authorization cannot target self.

A true participation assertion claims a role; false explicitly denies that role;
null is unknown. True and false both require declarations. Null participation,
unknown coverage, null responsibility/binding/authorization decision/provenance
source, null descriptor expectation and null signature validity require Unknown
evidence only. Other claims
require declarations only. Evidence claim IDs must match; declaration `by` must
name a local actor. External observed/verified evidence is unsupported, never
silently downgraded. Observations are generated by the reporter only and establish
facts about supplied input, not authenticity of commit objects or identity.
Verified means independently corroborated exact claims; it is reserved and never
emitted by this pilot. Signature declarations cannot elevate other claims.

Role execute is development activity (for example tests), not commit creation or
live execution. The executor directly initiates creation, independently of Git
author/committer, contributors, mechanism, acting principal and transport account.
An agent using human-looking headers remains the declared agent executor. Nothing
here establishes permission. Responsibility is separate from participation.

## Input envelope and identity matching

```typescript
type PrincipalReference = {id: string; kind: "human" | "agent" | "unknown";
                           source_status: string};
type GitIdentityBinding = {id: string; principal_id: string; name: string;
                           email: string; repository_ids: string[];
                           source_status: string};
type RegistryProjection = {source_repository_id: string; source_revision: string;
                           principals: PrincipalReference[];
                           git_identity_bindings: GitIdentityBinding[]};
type CommitInput = {repository_id: string; oid: string; parents: string[];
                    author: GitIdentity; committer: GitIdentity; message: string};
type IdentityProfile = {profile_id: string | null; author: GitIdentity | null;
                        committer: GitIdentity | null;
                        fetch_destinations: string[] | null;
                        push_destinations: string[] | null;
                        transport_account_ref: string | null;
                        signing_key_ref: string | null};
type ProfileCheck = {id: string; repository_id: string;
                     expected: IdentityProfile; observed: IdentityProfile};
type Input = {schema_version: 1; captured_at: string; registry: RegistryProjection;
              commits: CommitInput[]; profile_checks: ProfileCheck[]};
```

Capture time is a valid UTC `YYYY-MM-DDTHH:MM:SSZ` instant supplied by the caller.
Registry IDs must be unique and bindings reference existing principals. No fuzzy
name/email matching: compare exact tuples within explicit repository scope.
Multiple matching bindings yield UNKNOWN even if they name the same principal.
Header matching is an observation of a supplied registry declaration, not proof
of participation or executor identity. Retain source_status exactly. Resolve actor
aliases only through an identity-binding claim naming this exact registry revision,
a binding in the containing repository, and a compatible declared principal/kind.
No binding means actor identity stays source-qualified, even if names coincide.
An unresolved or ambiguous binding never supplies authority or trust.

Profile comparison considers all fields. Null in either side means UNKNOWN (even
null/null), empty destination arrays mean known none, destination arrays compare
as sets. Known differences yield MISMATCH, then UNKNOWN, then MATCH. Profile IDs
are markers, not authentication. No profile check performs its described operation.

## Trailer grammar and strict parsing

The final paragraph is preceded by an empty line and consists entirely of trailer
lines: ASCII alphanumeric/hyphen key, colon, one space, value. One optional final
LF is permitted. Attribution key matching is ASCII case-insensitive; JSON keys and
IDs are case-sensitive. Ordinary trailer keys are ignored. Recognized or unknown
`Attribution-*` lines elsewhere are malformed, not missing. No folded values.

```text
Attribution-Version: 1
Attribution-Work: <WorkRef JSON; optional, at most one>
Attribution-Actor: <Actor JSON; zero or more>
Attribution-Model: <Model JSON; zero or more>
Attribution-Claim: <Claim JSON; zero or more>
```

No attribution keys means missing. Keys without version mean invalid. Unsupported
versions mean unsupported. Unknown attribution keys are invalid. Version/work
singletons cannot repeat. Other identical definitions with the same ID collapse
with occurrence positions retained; different definitions under one ID are invalid.
Equivalent assertions with different IDs retain all evidence but count once.
Unknown never overwrites known; true/false for same actor/role/scope conflict.
Conflicting coverage or other singleton assertions are also visible, not last-wins.
Authorization compares decisions per action; identity bindings compare per binding
ID; signatures compare per signer reference. Multiple distinct actions or bindings
are not conflicts merely because the predicate repeats.

Reject duplicate JSON keys at every depth, unknown fields, malformed UTF-8/JSON,
BOM, lone surrogates (literal or escaped), NaN/Infinity, floats and integer tokens
longer than 19 digits or outside signed 64-bit range. A valid escaped surrogate pair
is accepted as its Unicode scalar. No implicit coercion. Maximum container nesting
is 12. Reject controls and bidirectional formatting in metadata; LF is allowed only
in the commit-message container. CR and NUL are rejected. Metadata strings are at
most 2048 characters; identifiers 128; messages 128 KiB UTF-8; attribution lines
8 KiB; actors/models 32 each; claims 128; evidence 8 per claim. Input is at most
16 MiB and 1000 commit records. Registry lists/profile checks/parents are bounded
at 1000; smaller descriptor lists are bounded at 32. Structural failures of the
outer envelope are atomic errors. Malformed attribution inside a structurally safe
commit yields an invalid row without payload echo. No exceptions escape the CLI.

## Normalization, tallies and reproducibility

Commit scope key: repository ID + full object ID. Work scope key: owning repository
ID + work ID + exact revision. Resolve self after reading the containing record;
never embed a self-referential object hash. Explicit commit targets remain separate
historical claims and contribute only when that target is present in this batch.
Work links create a scope row, never participation. Work claims create their exact
scope row even without a work trailer. Separate work revisions never combine.

Commit tallies use only claims targeting that commit. Work tallies use only explicit
work claims. Complete commit rosters never imply complete work coverage, and the
reverse is also prohibited. Deduplicate repeated equivalent assertions while
retaining qualified source references. Different supplied bytes for the same
repository/object are conflicting; identical records collapse with input occurrence
counts. Count unique object IDs separately from repository occurrences. Integration
commits have two or more parents. Logical work-entry count excludes revision;
work-scope tallies include revision. Unlinked commits remain visible.

Only positive participation counts. False and null never count. Mixed means positive
human plus agent. Human-only/agent-only require a complete unconflicted roster and
no unknown-kind positive actor or unresolved potentially additional participant.
Otherwise undetermined. Exclusive participation requires a complete roster and
one actor; shared means at least two positive actors; otherwise unknown. The same
rule applies to role views. Unknown alongside a known assertion for the same
actor/role does not override it. Contradictions make the affected record/scope
unclassifiable. Invalid records remain in denominators but contribute no claims.
Retain safe work links and report excluded source counts. Missing safe linkage is
counted at batch level; the batch never proves complete discovery of work.

Human/agent, actor, model and role participation views overlap and are labelled
non-additive. Executor counts are separate and do not imply contribution. Counts
measure recorded participation, never effort, quality, percentage or permission.
Model references in participation views are source-qualified; repeated positive
assertions union their model references rather than overwrite them. Commit-scope
conflicts across sources exclude those source records from every participation
view. Conflicting work claims remain visible in their work scope without converting
them into commit claims.

Byte-identical output requires identical input bytes (including capture time and
ordering), reporter/schema bytes and pinned dependencies. Reporter observations
use input capture time only; never read the clock. Emit UTF-8, sorted JSON keys,
compact comma/colon separators, ASCII string escaping, integer counts and one LF.
Sort commit rows by repository/object, work rows by repository/work/revision,
claims/descriptors by ID, findings by fixed code, and source positions numerically.
No environment, host, random ID, temporary path or generation time enters output.
Output observations have the Observation fields above plus a `value` object. For
header matching that object contains binding_id/principal_id (nullable) and status
UNKNOWN or DECLARED_MATCH; a match also preserves binding_source_status and
principal_source_status. This observes the supplied binding, not account ownership.

Reports include supplied registry revision and source statuses, input SHA-256,
reporter version, scope rows, exclusions and totals. No total implies authorization.

Exit 0 means conforming/classifiable records with no unresolved attribution/profile
fields. Exit 1 means missing/unknown attribution or profile findings. Exit 2 means
invalid/unsupported input, conflicts or profile mismatch. Well-formed batches retain
safe invalid rows. Outer failure produces empty stdout and exactly
`BLOCKER=REPO_CP_NONCONFORMANCE` plus LF on stderr. No rejected values or traceback.

## Provenance, privacy and recovery

Rebase/amend/cherry-pick/copied commits retain source references but require new
self declarations. Squash explicitly reconciles contributors; it never concatenates
coverage or approvals. Merge preserves parent evidence and separately attributes
integration/conflict resolution. Lost sources remain unknown. A new object requires
new exact-object review/signature/approval evidence. Work authorization refers to
an immutable work entry; applicability is independent of a copied declaration.
Exact-object approval targets an existing object outside itself. No metadata grants
permission, changes trust, or satisfies any execution gate.

Only operator-reviewed public input is accepted. Exclude prompts, private chats,
reasoning transcripts, credentials, sensitive personal facts and private paths.
Do not hash prohibited private material as a substitute for disclosure. Secret
indicators suppress values but are heuristics, not proof of safe publication.
The reporter omits raw messages, input header emails, registry identity tuples and raw
profile values from output. Accepted attribution descriptors/claims must already be
approved public content; the reporter cannot authenticate that approval. Evidence
references must identify approved public artifacts; never fetch them. Withdrawal
changes availability, not history. No private-evidence or verification service.
Optional human-approved reflections remain editorial, never authentication evidence;
preserve human wording and never infer motivations, diagnoses or personality.

Tests use synthetic profiles A/B and humans under one generic schema. Wrong-profile
checks must occur before the harness creates a candidate commit. A passing test is
not account ownership, credential custody or publication proof. Cleanup removes
only test-owned temporary directories. Retain the uncommitted task checkout for
review; no broad cleanup, history rewriting, peer changes or publication.

## Local delivery checkpoint

The initial task checkout at `.agent-checkouts/codex/attribution-pilot/` acquired
unrelated work-topology/test edits during this session. They were preserved. Only
the 13 attribution pilot paths were copied (without hardlinks) to the independent
`.agent-checkouts/codex/attribution-pilot-implementation/` checkout, branch
`codex/attribution-pilot-implementation`, at the same authorized baseline. The
original dirty source checkout was not edited. No topology change is part of this
pilot. No implementation commit or publication is authorized.

Role design records requirements/tradeoff choices; draft records candidate material;
implement records incorporated changes; review records evaluation, not approval.
Responsibility and authorization are separately declared and excluded from tallies.

Examples and golden outputs live in `tests/fixtures/attribution/`. Run the reporter
with a reviewed fixture on stdin. Run `python3 -B -m unittest discover -s tests
-p test_attribution.py -v` and the corresponding `test_git_identity.py` suite, then
`tools/validate`, as an ordinary user. Validation already discovers these tests and
the new schema; no change to its acceptance rules is needed.
