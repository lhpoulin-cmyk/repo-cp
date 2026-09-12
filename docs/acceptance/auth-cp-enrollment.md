# auth-cp repository-only enrollment

Louis explicitly approved the exact proposal on 2026-09-12. The
[approval receipt](auth-cp-enrollment.json) preserves the verbatim decision,
approval label, source revision, all seven approved public digests and exact
patch hash. The two-field patch from repo-cp
185cc3526eb47a582a4a80661c92e730a499f66d was applied without changing source,
digests, scope or any other repository entry.

ENROLLED_REPOSITORIES=auth-cp
AUTOMATIC_EXECUTION=DISABLED
LIVE_MUTATION=NONE

Source: 57815b15533ace72ee3ab2aef82fe3b764925652. The seven committed public
files and patch digest were reverified before application. Foundation and
ansible-cp remain DISCOVERED. No peer file, target or credential was changed.
Untracked auth-cp observation work was preserved.

Default audit now selects only auth-cp. Two runs returned identical bytes and
unchanged peer status. RC001 through RC008 PASS; RC009 and overall result remain
UNKNOWN. Counts: 26 PASS, 0 DRIFT, 0 BLOCKED, 1 UNKNOWN, 0 NOT_APPLICABLE.
See [JSON](auth-cp-enrolled-audit.json) and [text](auth-cp-enrolled-audit.txt).
Point-in-time remote verification does not change the offline freshness policy.

The original [proposal](../proposals/auth-cp-enrollment.md), patch and pilot
reports remain historical approval inputs. Synthetic enrollment tests use an
exact pre-application inventory fixture so apply, rejected repeat and reversal
remain testable after enrollment. No test modifies the real registry or peers.

Reversal requires a reviewed follow-up change returning auth-cp to PILOT and
clearing the active approval reference, while retaining this decision history.
No live admission, credential issuance/adoption or operational action is approved.
