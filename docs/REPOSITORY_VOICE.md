# Repository voice guide

Status: companion to work-contract candidate `1.1.0-rc.3`.
Scope: human-facing repository documentation and development communication.
This is a maintained guide, not a handoff or an authorization source.

## Apply the contract first

Read [the work contract's communication rules](AGENT_WORK_CONTRACT_CANDIDATE.md#3-communicate-decisions-and-results).
Lead with the outcome, explain consequences, distinguish observation from
inference, and make evidence proportional to the claim. Preserve exact technical
terms, machine-readable fields, safety conditions and required report content.
Editorial changes must not soften an obligation or broaden a PASS claim.

The contract governs this guide. Owning repository requirements and the
contract's precedence continue to apply. A voice preference never changes
ownership, credentials, approval, acceptance or publication authority.

## Separate public guidance from a private profile

A repository may maintain an operator-authorized private voice profile. Its
classification controls handling: do not commit, quote, summarize or incorporate
its source history into public artifacts. A stylistic influence is not permission
to disclose the underlying profile or to impersonate its author.

Use a private profile only when its location and access are already authorized
in the current task. Do not search credential stores, custody locations or
unrelated conversations to locate it. Keep it in an approved excluded location
with restricted filesystem access. Git ignore prevents accidental staging; it
is not access control. Never force-add it, scan it with public evidence tooling,
or include it in packages, validation logs or publication receipts.

An unavailable private profile does not block ordinary writing. Apply the public
contract rules and the owning repository's public style. Do not ask the operator
to paste private material into a public task. Identify private inputs only through
an approved opaque reference when necessary; do not export their contents or
fingerprints into public source records. No private profile is vendored here.

## Match the writing to the artifact

| Artifact | Reader needs |
| --- | --- |
| README | Purpose, supported behavior, entry points and material limits |
| Contract or procedure | Scope, owner, obligations, conditions and verifiable acceptance |
| Progress update | New finding, consequence and next step that resolves uncertainty |
| Completion | Result, evidence, actual delivery stage, remaining work and Live effects |
| Commit or PR | Problem, resulting change, relevant verification and review implications |
| Error | What failed, preserved state and a safe next action without sensitive values |

Use clear sentences and familiar words. Explain specialized terms when the
reader needs them. Choose paragraphs, lists or tables for understanding, not
ceremony. Length should follow the decision's complexity. Friendly language is
welcome; unsupported praise, grand claims and repetitive status narration add
little. Do not turn a small change into a manifesto.

## Review the writing

Check that a new reader can find the main result, distinguish facts from plans,
and understand any decision requested. Verify that links lead to the governing
source and that statements match the delivered artifact and tests. Remove
unnecessary repetition and internal implementation detail. Preserve precise
failure, authority and recovery language even when it makes a sentence longer.

Examples or proposed language must be labeled as such; never make an invented
example look like a real verification receipt. Follow the contract's GitHub
section for commit and PR framing. A voice review complements technical review
and does not substitute for it.

## Revision and adoption

Release this guide with the candidate contract; its bytes are bound by the
candidate content record. Once published, reference the same exact source commit
and path. Changes need a reviewed revision and refreshed digest. A private
profile has its own local maintenance and disclosure boundary; publication of
this guide does not publish or adopt that profile elsewhere.
