# B70 auth-cp identity authority acceptance refresh

Louis's current B70 task explicitly requires scoped publication and completion
of required repo-cp acceptance. This refresh retains auth-cp ENROLLED and its
existing seven-file public allowlist, updating only its source revision, changed
handoff digest and the current authorization reference. The [receipt](b70-auth-identity-refresh.json)
records exact committed inputs. No ansible-cp, Foundation or other enrollment
entry changes. Historical enrollment receipts remain in place.

Accepted auth-cp containing revision: `3bdcde14bb7c0d77775cfeb2d1bd5571488d6f2a`.
Policy revision: `a2aa36cba34cb7549d1ed173a55c405c779d57e5`.
Foundation repository and doctrine pins remain unchanged. RC008 compatibility
means these separate Foundation references are preserved; it does not claim the
new target privilege grant existed in historical policy or authorize live use.
The owner review now references the published bounded-identity policy.

Auth-cp's existing canonical principal/account schema now records two separate
B70 credentials, conditional proven-match ADOPT/proven-absent ISSUE, ansible-cp
consumer binding and executor-scoped grants. This is domain authority, not
repo-cp policy. Its 138 tests and public validation passed before acceptance.
Actual issuance/adoption remains blocked at the accepted custody-provider gate.
No credentials, secrets, guest changes or automatic execution occur here.

The selected auth-cp audit retains RC009 UNKNOWN because it performs no remote
query. Separate direct Git verification does not relabel this offline check.
The ansible-cp entry retains its accepted bytes and earlier auth pins; any
resulting RC010 drift is reported, not repaired or silently accepted in this lane.
That consumer must independently revalidate the new auth revisions.

Rollback is a reviewed follow-up restoring the previous auth-cp entry and owner
review from 348aea8d0819fc5de7f845ac34bd14ddb5fdd05a, preserving new acceptance
history. No history rewrite or live rollback. Repeated rendering/auditing has
no mutation; synthetic tests exercise enrollment separately from real records.

## Acceptance validation

Full repo-cp validation passed: 13 unchanged Foundation reference tests and
39 local tests, syntax/schema/link/version/indicator checks and diff audit.
[Two identical auth audits](b70-auth-identity-audit.json) report 26 PASS and
1 UNKNOWN (RC009), zero DRIFT/BLOCKED. [Fleet audit](b70-fleet-after-auth-refresh.json)
reports 61 PASS, 2 UNKNOWN and the two expected ansible-cp RC010 stale-auth-pin
findings. Nothing is waived. Ansible-cp files and its enrollment entry remain
unchanged; its owner must consume and revalidate the exact new auth authority.
