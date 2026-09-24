Core idea: repo-cp becomes the only thing allowed to dispatch agent work. Scheduled tasks don't call Codex directly. They ask repo-cp, and repo-cp checks the budget first. That keeps a single writer in charge of spending.

1. Budget state, failing closed

usage/state.yaml holds the plan usage %, when it was read, the reset date, and the credit cap.
You update it by hand for now (repo-cp usage set 72). Check whether Claude or Codex offers a usage API before building around one; I wouldn't assume it.
If the reading is stale (older than ~12h), treat it as yellow. No fresh reading means no heavy work.
Daily allowance = (100% − used) ÷ days until reset. This is the part that actually paces you. Instead of burning through everything in three days and coasting for six, each day gets a share.

2. The queue replaces "doing other stuff"

queue/*.yaml, one file per task: size (S/M/L), which agent, priority, dependencies, and a spec-ready flag.
Anything you think of while over budget goes into the queue, not into an agent.

3. The dispatch gate

Green: any task that's spec-ready and fits today's allowance.
Yellow: only S tasks.
Red: nothing gets dispatched. The only allowed action is repo-cp queue add.
Refusals are logged the same way as dispatches.

4. Efficiency rules (where the savings come from)

No spec, no dispatch. Vague tasks are the biggest waste: agents explore, guess and redo.
Context packs. Each task lists the files it needs, so the agent doesn't scan the whole repo.
Stop when there's no progress. If the same test fails N times, or the same file is rewritten N times, halt and record evidence instead of retrying.
Batch small tasks into one run, so the shared context is loaded once.
Per-task caps on turns or time. L tasks are split into S and M pieces before they get queued.

5. Evidence

usage/ledger.jsonl is append-only: task, agent, size class, zone at dispatch, and the plan % before and after (entered by you).
After a few cycles you'll know what an L task really costs, and your size estimates stop being guesses.

6. One combined scheduled task

Runs daily. It reads the budget state, and if the reading is stale it stops and asks you for one. Otherwise it dispatches the top tasks that fit today's allowance.
On reset day it front-loads the L tasks while you're in green.
