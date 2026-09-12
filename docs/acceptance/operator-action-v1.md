# Operator-action V1 acceptance

FOUNDATION_OPERATOR_ACTION_CONTRACT_MISSING=CLOSED
OPERATOR_ACTION_V1_CONSUMER=IMPLEMENTED_AND_TESTED
AUTOMATIC_EXECUTION=DISABLED
LIVE_MUTATION=NONE

## Immutable authority

Accepted canonical Foundation: git@github.com:lhpoulin-cmyk/foundation-cp.git,
branch main. Exact repository revision:
999fcf6a4bf181bdba201e9ca0c2f2bc4e7e2af5.
Separate consolidated doctrine revision:
d2fe6c6291ea1eaffadb15ded6c0240fed0e96ca; doctrine version 1.0.0.
Contract: contracts/HELIX_OPERATOR_ACTION_CONTRACT_V1.md;
identity HELIX_OPERATOR_ACTION_CONTRACT_V1; interface 1.0.0.

Preflight host ws-hadrian, user louis, repo-cp main at
 a6f9134c9ddad39244810cacd96fb79a12bec36d (clean), canonical origin
https://github.com/lhpoulin-cmyk/repo-cp.git and origin/main parity verified.
Direct Foundation remote HEAD/main and checkout HEAD matched the supplied
999fcf6 revision. Both doctrine artifacts and VERSION match the doctrine commit;
intervening changes add the V1 contract and retain doctrine 1.0.0 compatibility.
The exact contract, schema, registry, renderer, CLI, tests and all five fixtures
were verified in the committed tree and against checkout bytes before copying.
The 13 exact upstream reference tests passed from the isolated consumer snapshot.
The consumer uses the normative reference parser/validator/renderer unchanged;
all 19 artifact digests are checked before loading code. Independent pins come
from reviewed repo-cp code/manifests, never from action input. These local trust
records require reviewed Git updates; self-asserted producer pins are not trust.

The original blocker and docs/handoffs files at
 a6f9134c9ddad39244810cacd96fb79a12bec36d remain unchanged historical evidence.
This record closes missing operator-action authority only. Target-facet authority
remains unresolved and bootstrap acceptance does not enroll any repository.

## Accepted artifact SHA-256

Paths are relative to the exact Foundation repository revision above and to
vendor/foundation in repo-cp. Machine records are
[pins/foundation-repository.json](../../pins/foundation-repository.json) and
[pins/foundation-doctrine.json](../../pins/foundation-doctrine.json).

| Artifact | SHA-256 |
| --- | --- |
| `AGENTS.md` | `18adc511d076fd014813e1a56ca1be981889312b8d9319c4828dfad196f9c72c` |
| `OWNERSHIP.md` | `f43c23d755e88ed75ddfd7409f546f6bca72dfae90c47ec9f68b1151cc4fe9e0` |
| `PROVENANCE.md` | `3f141b392405f523dbebaad3367ac5f6d4e97dd56a124df33b3c088db526d453` |
| `README.md` | `2eba1475de46422a2982027e5f797feed5dd089c69960ea0d12a89bcce9e1c2c` |
| `VERSION` | `59854984853104df5c353e2f681a15fc7924742f9a2e468c29af248dce45ce03` |
| `contracts/HELIX_OPERATOR_ACTION_CONTRACT_V1.md` | `864270803ec502be52341fb20be2b1ac474c34f860afc06061153ba88d084407` |
| `docs/ACTIVE_DOCTRINE.md` | `034751e03ae51672ff6df1cea50dd18c5a6c7da0eb92ad01286c4873486804c6` |
| `docs/OPERATOR_ACTION_VALIDATION.md` | `0be0a2c564911624ba9baa3c4f1da73d4c4ff94a1004b1e61edd3f5f61e7634f` |
| `registries/active-doctrine.json` | `49eb46a68a9363e9d4cafdf11ad483e92c920cd555112aaed92464a11ac748fe` |
| `registries/operator-action.json` | `d7065b1bc5551f6d9e452d14b2e8ba68c3c54428b7390ac8600e204d39982bf9` |
| `schemas/operator-action-v1.schema.json` | `9dc8cfcb530c818a92391983b4f2d91cb12480ab9eddd7c5516ee2188f1b1f50` |
| `src/operator_action.py` | `57cfd243ca8132c94b5e64712141413c08e7610ad815848a039ee415d6704bb7` |
| `tests/fixtures/operator_action/blocked.json` | `efaca6bbfc5ca4879e218146cb1f6af6ee0a64061bd3096df34c3dd3e2466b67` |
| `tests/fixtures/operator_action/blocked.txt` | `40d197e0e5b39fdca4d0a0f13c9f2ce07f0c8e08e72670356340d33ac0f2aac1` |
| `tests/fixtures/operator_action/invalid-blocked-command.json` | `9f2061cf87683a5d32d32bb131a1e19cdba275818af74f068d7878bdff6c5efc` |
| `tests/fixtures/operator_action/ready.json` | `175903ec239f6ee97961cf253e2bb635e9fd64fde1fce32067a9d4896b065681` |
| `tests/fixtures/operator_action/ready.txt` | `9bbfa237ba84552dcd7d02299979d04408b1ca41b4740b7993bb677bdcfc6f08` |
| `tests/test_operator_action.py` | `d2ae715c4afbe2031359b212daa6657fcbbe221e7d1446c1e1589c3f62b79f19` |
| `tools/render_operator_action.py` | `0260846973154393f9419c2bf1cffe031b30938e0cf335e01bfe586ea85ab697` |

## Boundaries

Foundation status remains REPOSITORY_CONTRACT_ONLY. Valid output is a declaration
for review, not authorization or execution. Missing structured V1 capabilities
and target-facet authority are tracked in [Foundation requests](../FOUNDATION_REQUESTS.md).
No private material or live observations were used. Foundation's unrelated
untracked docs/WINDOWS_BACKUP_CUSTODY.md remains untouched. auth-cp's untracked
contracts/ws-wowzer-win-observation.md and ansible-cp's modified
 docs/SEMAPHORE_RECOVERY.md and docs/WS_WOWZER_WIN_ADMISSION.md remain untouched.
Foundation/auth-cp/ansible-cp were not modified or operationally executed.
