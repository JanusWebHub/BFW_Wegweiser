# Documentation Restructuring Tracker

## Orientation (as of 2026-09-24)

Read this section first in any new conversation to avoid re-explaining the project and ongoing actions from scratch.

### Core documents

| Document | Role | Status | Note |
| --- | --- | --- | --- |
| `README.md` | project entry point | done | Rewritten to match the current model in `97a7a1f`. |
| `rulebook.md` | canon | done | Model and graph definitions complete. |
| `system-design.md` | technical specification | done | Technical specification complete. |
| `implementation-plan.md` | future-facing plan | done | Plan complete. |
| `devlog.md` | past-facing historical record | immutable | Hands off. |

Critical distinction: the working code/program files still implement the *old* model and are out of compliance with the new rulebook/system-design. Implementation work is deferred.

### Branch Cleanup Decisions (as of 2026-09-24)

- `tracker-updates` temporarily tracks the ignored tracker; the file is force-added there.
- Checkpoint pattern: documentation commit, tracker update naming it, tracker commit.
- The tracker is intended to be tracked only on `tracker-updates`; remove it from `main` and `feature/sql` before continuing implementation work.
- `feature/east-wing-prototype` remains a reference branch; selected code will be ported into a new branch from current `main`.
- See "Branch/merge sequence" below for the full plan.

### Later housekeeping

- Convert edited files to CRLF.
- Add root `.gitattributes` with `* text=auto` in its own commit.

### Branch/merge sequence (as of 2026-09-24)

1. Archive full unsquashed history to `denizmertmercan/BFW_Wegweiser`. — done
2. Squash-merge `docs/restructure` into JanusWebHub `main`. — done
3. Rebase `feature/sql` onto `main` and retain it as a separate branch. — ongoing
4. Create a new branch from the updated `main` and selectively port the useful implementation from `feature/east-wing-prototype`. — outstanding
5. Delete `backup-before-reset`. — done

### Home-machine branch picture (as of 2026-09-23)

- `main` (tip `f3dd43f` — squash commit, see Branch/merge log): original implementation, now carrying the squashed docs restructuring on top.
- `feature/east-wing-prototype` (2 commits ahead of old `4763d6c`): `a39e341` east-wing routing prototype + `5fc294c` rulebook update. Small, self-contained. Still needs rebasing onto new `main` — not yet done.
- `feature/sql` (Janus, 2 commits, `55ec7ef`/`07ae881`, branched off old `docs/restructure` at `6e413e7`): appends rulebook clusters 5 (usage analytics and feedback) and 6 (UI and UX). Still needs rebasing onto new `main` — not yet done. See rebase-preview finding below; not low-risk as originally assumed.
- `backup-before-reset`: orphaned safety branch off old main tip, holds one extra commit `0de4f03` ("Document semantic floor plans and portal graph architecture") never merged anywhere. False start, not salvageable, must never enter `main`'s ancestry. Not yet deleted (W5).
- `docs/restructure`, `local/documentation-restructuring`: deleted, both locally and on `januswebhub`, after the squash-merge (see Branch/merge log). Full history preserved in PR #2 and on `denizmertmercan` fork.
- `copilot/common-design-patterns`: deleted agent-created branch; identical to `main`, never real work.

Remotes: `januswebhub` (`JanusWebHub/BFW_Wegweiser`, the active repo) and `denizmertmercan` (`denizmertmercan/BFW_Wegweiser`, personal fork/archive). Both configured with these names, not `origin`/`fork`.

### Work-machine branch picture (as of 2026-09-24)

Remote configuration: `januswebhub` only; `floorfox` removed.

| Local branch | Remote branch | Short hash |
| --- | --- | --- |
| `main` | `januswebhub/main` | `f3dd43f` |
| `feature/sql` | `januswebhub/feature/sql` | `205833c` |
| `feature/east-wing-prototype` | `januswebhub/feature/east-wing-prototype` | `5fc294c` |
| `tracker-updates` | `januswebhub/tracker-updates` | `5d24b83` |

### Branch/merge log (as of 2026-09-24)

- Fork remote added (`denizmertmercan/BFW_Wegweiser`), `origin` renamed to `januswebhub` for clarity. Full history pushed to the fork: `main`, `docs/restructure`, `local/documentation-restructuring`. `feature/east-wing-prototype` and `backup-before-reset` deliberately excluded — east-wing lands on `main` via normal rebase anyway (nothing at risk of being flattened), `backup-before-reset` is disavowed content, not archive-worthy.
- On the fork, demonstrated the fast-forward path (`docs/restructure` → fork's `main`) to confirm full-history preservation works as intended — fork's `main` now at `db3b052`, all 85 commits intact. Both `docs/restructure` and `local/documentation-restructuring` kept as named branches on the fork (not deleted) — the branch labels themselves are part of what "keep full history" means, not just the commit content.
- PR #2 opened and squash-merged on `januswebhub`: `docs/restructure` → `main`. One Copilot review suggestion applied (stale `docs/references/` listing in README.md, caught correctly — that folder was deleted in an earlier commit). Squash commit: `f3dd43f`, "Restructure project documentation (#2)". `main` confirmed single-parent (true squash, not a merge commit).
- `docs/restructure` and `local/documentation-restructuring` deleted on `januswebhub` and locally, post-merge. Both fully recoverable via PR #2 and the `denizmertmercan` fork.
- `copilot/common-design-patterns` deleted on `januswebhub` (agent-created branch, identical to old `main`, no real content).
- Rebase analysis for `feature/sql`: its two own commits touch only `docs/rulebook.md`, which is byte-identical at its fork point (`6e413e7`) and `f3dd43f`. A plain rebase would replay inherited documentation history; `git rebase --onto f3dd43f 6e413e7` correctly reapplies only the two SQL commits.
- Work-machine baseline on 2026-09-24: `main` → `januswebhub/main` (`e3d1be7`); `feature/sql` → `januswebhub/feature/sql` (`07ae881`); `feature/east-wing-prototype` → `januswebhub/feature/east-wing-prototype` (`5fc294c`); `docs/restructure` → `januswebhub/docs/restructure` (`55c8cf3`); `local/documentation-restructuring` → `januswebhub/local/documentation-restructuring` (`67f1c2d`); `backup-before-reset` had no remote (`0de4f03`). Remotes: `januswebhub` and `floorfox`; Janus also had `copilot/common-design-patterns` (`4763d6c`).
- Work-machine operation on 2026-09-24: `git remote remove floorfox` removed the Floorfox remote and its tracking refs.
- Work-machine operation on 2026-09-24: `git fetch --all --prune` removed stale Janus tracking refs for `copilot/common-design-patterns`, `docs/restructure`, and `local/documentation-restructuring`.
- Work-machine operation on 2026-09-24: `git branch -D` deleted local `docs/restructure`, `local/documentation-restructuring`, and `backup-before-reset`.
- Work-machine verification on 2026-09-24: `git ls-remote --heads januswebhub` showed only `main`, `feature/sql`, and `feature/east-wing-prototype`; `git merge-base --is-ancestor 0de4f03 main` confirmed `0de4f03` is outside `main` ancestry.
- Tracker split on 2026-09-24: created and pushed `tracker-updates` at `862ffbd`, preserving tracker commits `e3d1be7` and `862ffbd`; reset and force-pushed `main` back to `f3dd43f`.
- SQL rebase on 2026-09-24: verified `docs/rulebook.md` was identical at `6e413e7` and `f3dd43f`; rebased `feature/sql` with `git rebase --onto f3dd43f 6e413e7`, yielding `c208b0d` and `205833c`; force-pushed the rewritten branch to JanusWebHub. The branch now changes only `docs/rulebook.md` relative to `main`.
- Decision on 2026-09-24: retain `feature/sql` as a separate rebased branch; do not merge it into `main` for now. Remove the tracker file from `main` with a cleanup commit, then rebase `feature/sql` onto the updated `main`.
