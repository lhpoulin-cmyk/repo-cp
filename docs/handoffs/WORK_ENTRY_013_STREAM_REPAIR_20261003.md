# Work Entry 013 — Claude Code subscription stream repair

Status: `PARKED / OFFLINE REPAIR PUBLISHED / NEXT GRANT UNISSUED / NOT SENT`

Canonical helix-offload commit
`15b86e6c09a5602bc40125fe6bee2a45727c787a` publishes the offline repair and its
corrected 147-file JSON evidence count. The
subscription adapter now captures bounded Claude Code `stream-json` evidence,
chooses only a single final terminal result, and delegates all JSON,
source-reference and postflight authority to DERP. It no longer uses the
client's `--json-schema` validation.

The prior attempt and its recovery evidence are unchanged. Its reported
650-character/missing-field candidate was not returned as output, so no artifact
was recovered; provider execution, actual model and usage remain `UNKNOWN`.

The next packet uses the same source packet as Work Entry 015 and attempt 001:
`f5bb1cd016bd36f847d9129efd2057b6a36ddc9d67bbddce56e6384e07966f41`.
The workflow SHA-256 is
`5e623d2c4b43c7746507aa9570a45b09ad6e71b2854fac0a825e244cd4e7f93f`,
preview SHA-256 is
`be693bcc30b56eedec5bee93b6b45693326d1c902b5dd4b2954daf41fd60587a`,
and proposed-grant SHA-256 is
`a7e0750f532c8e1cec8c59ee2c485ae0dae2f5b0f5581cce6662ad61785a80e9`.
The proposal wrapper is deliberately not an executable grant.

Exact next action: after fresh authorization for exactly one Claude Code client
run, issue the real content-bound `execution-grant/v1`, persist a new attempt
identity and intent, and invoke once. Work Entry 014 remains parked.

Live effects: canonical/review-branch Git publication only. No model/API call,
credential/account change, installation or runtime mutation occurred.
