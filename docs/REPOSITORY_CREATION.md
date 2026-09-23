# Create a local repository

The operator requested a repository-creation command and automatic generation of
baseline agent guidance and desktop project Instructions. This is an explicit
exception to the previous all-CLI-read-only rule, limited to new local repositories.
Audit, render, inventory, drift, propose and validate keep their existing behavior.
No Foundation artifact, released contract, candidate, trust anchor or enrollment
record changes as part of creation.

## Usage

Run as an ordinary Linux user with Python dependencies and Git installed:

```sh
python3 -B tools/repo-cp create /absolute/parent/example-cp \
  --purpose "Maintain example domain declarations" --owner Louis --dry-run
python3 -B tools/repo-cp create /absolute/parent/example-cp \
  --purpose "Maintain example domain declarations" --owner Louis
```

Omit `--dry-run` to create. `--purpose` is required; `--owner` defaults to Louis
and records stewardship, not a delegation of ultimate operator authority. Both
fields must contain public one-line text, at most 400 characters. The repository
name is the destination's final component: 1–64 lowercase letters, digits,
underscores or hyphens, beginning with a letter or digit. Existing targets,
including empty directories and dangling symlinks, are refused. There is no
`--force`, implicit overwrite, package install or interactive prompt.

Use an absolute path with an existing, user-owned parent that is not group- or
world-writable. Path components must not be symlinks; traversal and ambiguous
paths are rejected. For temporary testing, first create a private temporary
parent, then pass a new child path. Direct creation under world-writable `/tmp`
is deliberately refused. No repository name or real infrastructure is inferred.

## Generated baseline

| File | Purpose |
| --- | --- |
| AGENTS.md | Local agent guidance with purpose, stewardship and immutable released-contract reference |
| OPENAI_PROJECT_INSTRUCTIONS.md | Self-contained text for the desktop project's Instructions field |
| README.md | Purpose, initial state, desktop setup and verification |
| OWNERSHIP.md | Supplied stewardship and explicit limits |
| PROVENANCE.md | Template version, public inputs and exact contract source/digest |
| .gitignore | Basic Python cache, environment and local dotenv exclusions |
| .repo-cp-create.json | Versioned creation intent with public inputs, generator source hashes and generated file digests |

Git is initialized on `main` with an empty template, no hooks, remote or initial
commit. Files are ordinary independent copies, created mode 0600 in a mode 0700
repository directory. No application stack, test framework or license is guessed.
The guidance names the released 1.0.0 contract, its full canonical publication
commit, path and SHA-256. It does not adopt the candidate implicitly. Generation
verifies the batch-1 contract integrity checks before writing.

## Desktop app setup

For a local Codex project, attach the generated repository as the primary folder.
Codex discovers its `AGENTS.md` as documented in
[OpenAI's agent guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
For a project offering an Instructions field, paste the complete generated
`OPENAI_PROJECT_INSTRUCTIONS.md` text there. Generation does not modify app
settings or assert that the file is automatically imported.

[OpenAI's projects documentation](https://learn.chatgpt.com/docs/projects)
distinguishes project sources and instructions from a local project's attached
folders. A sources-only project needs uploaded or connected repository context;
a file path in instructions does not provide access. Start a new task or ask an
existing task to reread updated guidance. Update the settings text when guidance
changes; no automatic synchronization or behavioral enforcement is claimed.

## Commit boundary and recovery

Creation locks the owner-controlled parent and exclusively creates an unpredictable
private sibling named `.repo-cp-create-<random>`. It writes and fsyncs an intent,
creates the fixed baseline files, then invokes only local `git init` with a minimal
environment, a 30-second timeout, empty templates, and global/system Git configuration
disabled. Inherited Git environment variables cannot redirect initialization.
It verifies the generated files and initial Git state, fsyncs the staging tree,
then publishes using Linux `renameat2(RENAME_NOREPLACE)` and fsyncs the parent.
It independently verifies the published directory identity and expected content.
The rename is the filesystem commit boundary; no cross-system transaction exists.
There is no hardlink fallback or delete-and-recreate path.

Before the rename attempt, failures report `CREATE_PREPARATION_FAILED` (or
`CREATE_INTERRUPTED` for catchable cancellation) and retain
any staging state. After the attempt, failures report `CREATE_RECOVERY_REQUIRED`:
the final repository may already exist. Inspect the exact target or retained
staging directory, never infer absence from the exit code:

```sh
python3 -B tools/repo-cp create /absolute/parent/example-cp --inspect
```

Inspection reads the intent, regenerates the expected baseline, and checks file
bytes and initial Git state. It reports `RECOVERY_REQUIRED`, `VERIFIED` or
`INCOMPLETE_OR_CHANGED` content, `TARGET` or `STAGING`, and unconfirmed durability.
It writes nothing and does not claim a previously interrupted operation completed.
Review retained evidence before any separately scoped cleanup or retry; a retry
never changes an existing target. No glob cleanup, automatic resume, rollback,
remote publication or enrollment occurs. Normal post-creation edits can make
inspection report changed content; it is a bootstrap recovery check, not an audit.

Catchable termination is controlled; SIGKILL or power loss may leave staging or
a published target without a success response. Storage failure can prevent an
intent from becoming durable; missing or malformed evidence fails closed. Locks
coordinate compliant creators, not hostile same-UID processes or root. This
unprivileged operation has no credential, privileged deployment, database or
cross-filesystem-copy capability. Those production-engineering requirements are
outside its scope. Changes to existing repositories remain separate operations.

## Results and verification

Exit 0: creation verified, or a successful read-only preview. Exit 1: recovery
inspection requires review. Exit 2: refusal or creation failure; inspect the
fixed blocker/reason. Successful JSON distinguishes local mutation, remote
creation, enrollment, initial commit and manual project-settings installation.
Errors keep stdout empty and do not echo input, paths or subprocess diagnostics.
The secret-indicator check is a heuristic; callers must supply public metadata.

Tests use only synthetic temporary parents. They cover Git creation, matching
instructions, preview, repeated invocation, existing targets, symlinks, ownership
policy, root rejection, contract tampering, ambient Git configuration, failed
initialization, cancellation, fsync failure, concurrent target creation and lost
acknowledgement after rename. Independent non-author review remains a release
requirement for this state-changing command. Tests do not establish live adoption.
