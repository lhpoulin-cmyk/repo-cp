# Claude and Codex repository checkout rules

These operator-authorized working rules apply to Helix `-cp` and other
repositories, with domain ownership and local security requirements preserved.
They implement HELIX_AGENT_EXECUTION_DOCTRINE_V1 for development work; they do
not change Foundation contracts, enrollment, publication or live authority.

## Private placement and identity

Claude and Codex are authorized to create and reuse their own isolated checkouts
for an authorized task without asking again. Store them inside the owning
repository at `.agent-checkouts/claude/<task>/` and
`.agent-checkouts/codex/<task>/`. Use a stable, non-sensitive task identifier and
separate branches such as `claude/<task>` and `codex/<task>`. Do not put these
checkouts in a sibling repository, a home-wide checkout pool or `/tmp`.

Exclude `/.agent-checkouts/` from the owning repository's Git tracking before
creation. Keep this root private to the operator and agent using owner-only
directory permissions where supported. Git ignore is publication hygiene, not
an access-control boundary; actual sandbox permissions still apply. Do not store
credentials or private runtime payloads there. Validators, packaging, searches
and evidence collection must prune this directory before traversal. Review
staged paths; never force-add checkout contents.

Prefer an independent clone with its own Git metadata and verified canonical
origin. A local committed public source may seed a clone with `--no-hardlinks`
when appropriate; verify its source revision and configure the canonical origin
explicitly. Do not copy credential configuration, untracked files or private
material from the source. Linked worktrees share repository metadata: use them
only when that shared access is permitted and isolation remains adequate. Never
weaken an audit to make unsupported worktree layouts pass; use an ordinary clone
or retain UNKNOWN. Read the original parent and repository guidance before
relocation, and carry that instruction context into the isolated checkout.

## Idempotent setup and continuation

Before creating or reusing a checkout, verify the owning repository, canonical
remote, branch, HEAD, upstream, recent history and applicable local rules. Reuse
an existing task checkout only after checking its identity, ownership and dirty
state. Preserve in-scope work and unrelated work. Do not reset, delete, overwrite
or repoint an unexpected existing directory; investigate the collision and use
a distinct task namespace if appropriate. Reject symlinked checkout roots or
paths escaping the owning repository. Repeated setup must leave correct existing
checkouts, exclusions and guidance unchanged, without duplicate rule blocks.

Keep task artifacts and dependencies in the permitted sandbox. Resolve ordinary
path, branch, namespace and dependency failures there. Avoid unnecessary mounts
by using committed public source and local synthetic fixtures. Do not request
host mounts merely to reproduce a workstation path. Do not change mount policy,
escape namespaces, disable sandbox enforcement or broaden privileges.

Use anonymous canonical access for public repositories when credentials are
unnecessary. Where authentication is required, use only an already authorized
tool capability consistent with local credential rules. Never inspect credential
stores, copy another agent's credentials, change identity or weaken TLS/SSH
verification to make setup succeed. Retry a permitted network operation through
the platform approval mechanism when needed. If remote access is unavailable,
continue safe local work where local policy permits and report freshness as
unverified; never claim canonical parity from a cached ref.

## Completion and boundaries

Implement, validate and review the complete authorized change. Record which
checkout and commit contain the result so work is recoverable. Transfer only
reviewed task changes back within the authorized scope, preserving concurrent
work; publication and merging retain their existing approval requirements.
Do not delete a checkout with untransferred work. Adding these rules to another
repository must preserve its guidance and vendored snapshots; shared parent
rules apply without rewriting peer pins or enrolling peers.

Before a genuine stop, refresh HEAD, status and recent history. Report
`BLOCKER=`, `operation=`, `observed=`, `expected=`, `authority=` and
`why_not_ordinary_debugging=`. An unavailable safe capability or conflicting
authority is a real boundary; routine setup and test failures require repair.
These are development-agent permissions. They grant no additional capabilities
to the repo-cp runtime CLI or permission to execute peers or mutate live state.
