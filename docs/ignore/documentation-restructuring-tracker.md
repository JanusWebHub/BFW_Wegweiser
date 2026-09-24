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
- The tracker is tracked only on `tracker-updates`; it has been removed from `main` and `feature/sql`.
- Retain `feature/sql` as a separate rebased branch; do not merge it into `main` for now.
- Evaluate a reconstructed history in which `feature/east-wing-prototype` is merged after `4763d6c`, followed by a replay of PR #2 and the tracker cleanup. Use local preview branches before changing real branches.
- Preserve the original PR #2 squash commit with the annotated tag `archive/pr-2-squash`.
- See "Branch/merge sequence" below for the full plan.

### Later housekeeping

- Convert edited files to CRLF.
- Add root `.gitattributes` with `* text=auto` in its own commit.

### Branch/merge sequence (as of 2026-09-24)

1. Archive full unsquashed history to `denizmertmercan/BFW_Wegweiser`. — done
2. Squash-merge `docs/restructure` into JanusWebHub `main`. — done
3. Remove the tracker from `main`; rebase `feature/sql` onto the cleaned `main` and retain it separately. — done
4. Preview and evaluate PR3-style east-wing integration before replaying PR #2. — ongoing
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
| `main` | `januswebhub/main` | `a9862c2` |
| `feature/sql` | `januswebhub/feature/sql` | `be9b962` |
| `feature/east-wing-prototype` | `januswebhub/feature/east-wing-prototype` | `5fc294c` |
| `tracker-updates` | `januswebhub/tracker-updates` | `970b19d` |
| `preview/replay-pr2` | none | `b1e657c` |
| `preview/sql-after-replay` | none | `77a7048` |

### Branch/merge log (as of 2026-09-24)

- Fork remote added (`denizmertmercan/BFW_Wegweiser`), `origin` renamed to `januswebhub` for clarity. Full history pushed to the fork: `main`, `docs/restructure`, `local/documentation-restructuring`. `feature/east-wing-prototype` and `backup-before-reset` were deliberately excluded; the latter is disavowed content, not archive-worthy.
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
- Tracker checkpoints on 2026-09-24: `tracker-updates` advanced through `5d24b83` (SQL-rebase record) and `970b19d` (tracker-structure overhaul), both pushed to JanusWebHub.
- SQL rebase on 2026-09-24: verified `docs/rulebook.md` was identical at `6e413e7` and `f3dd43f`; rebased `feature/sql` with `git rebase --onto f3dd43f 6e413e7`, yielding `c208b0d` and `205833c`; force-pushed the rewritten branch to JanusWebHub. The branch now changes only `docs/rulebook.md` relative to `main`.
- Decision on 2026-09-24: retain `feature/sql` as a separate rebased branch; do not merge it into `main` for now. Remove the tracker file from `main` with a cleanup commit, then rebase `feature/sql` onto the updated `main`.
- Tracker isolation on 2026-09-24: committed and pushed `a9862c2` on `main` to stop tracking `docs/ignore/documentation-restructuring-tracker.md` while leaving the ignored worktree file available.
- Final SQL cleanup rebase on 2026-09-24: rebased the two SQL commits from `f3dd43f` onto `a9862c2`, yielding `c7e454f` and `be9b962`; force-pushed `feature/sql`. Verification showed only `docs/rulebook.md` differs from `main` and the tracker is absent from the branch.
- PR #2 preservation on 2026-09-24: created and pushed annotated tag `archive/pr-2-squash` at original squash commit `f3dd43f`.
- Replay preview on 2026-09-24: local `preview/replay-pr2` replayed `f3dd43f` onto `feature/east-wing-prototype`. The only conflict was `README.md`; resolving it in favor of the PR #2 documentation produced `3688fa8`. Cherry-picking `a9862c2` then produced cleanup commit `b1e657c`.
- SQL preview on 2026-09-24: local `preview/sql-after-replay` rebased the SQL commits from `a9862c2` onto `b1e657c`, yielding `9061f21` and `77a7048` without conflicts. Verification showed only `docs/rulebook.md` differs from the preview main and the tracker is absent.
- Preview finding: replaying PR #2 preserves east-wing files that PR #2 never touched, including the separate compiler, routing, generated databases, UI, assets, and `docs/rulebook_sorted.md`. The resolved README retains the restructured documentation model and lists the surviving east-wing program files.

### Completed direct-replay preview

This first preview tested a linear reconstruction without a merge commit:

```text
M1 (4763d6c) -> E1 (a39e341) -> E2 (5fc294c) -> M2' (3688fa8) -> cleanup' (b1e657c) -> SQL1' (9061f21) -> SQL2' (77a7048)
```

No real branch was changed or pushed. The following commands and resolutions produced the preview:

```powershell
# 1. Create a disposable branch at the original PR #2 squash commit.
git branch preview/replay-pr2 f3dd43f
git switch preview/replay-pr2

# 2. Replay only the PR #2 squash changes after the east-wing tip.
git rebase --onto feature/east-wing-prototype 4763d6c

# README.md was the only conflict. In the merge editor, retain the incoming
# f3dd43f documentation structure, complete the merge, and continue.
git add README.md
git rebase --continue

# Result: replayed documentation commit 3688fa8.

# 3. Replay the tracker-file deletion on the same preview branch.
git cherry-pick a9862c2

# Result: cleanup commit b1e657c.

# 4. Copy feature/sql and rebase the copy onto the cleaned preview.
git branch preview/sql-after-replay feature/sql
git switch preview/sql-after-replay
git rebase --onto preview/replay-pr2 a9862c2

# Results: SQL commits 9061f21 and 77a7048.

# 5. Verify the reconstructed history and branch scope.
git log --graph --oneline --decorate -7
git diff --name-status preview/replay-pr2..HEAD
git ls-tree -r --name-only HEAD -- docs/ignore/documentation-restructuring-tracker.md
```

The replay completed with one expected `README.md` conflict. The final SQL preview changed only `docs/rulebook.md`, and the tracker file was absent. This established that the file states are compatible, but the linear history does not preserve a PR-style east-wing merge loop.

### Safe PR3-style reconstruction preview plan

All `preview/*` and `backup/*` branches remain local and must not be pushed.

```powershell
# 1. Confirm a clean worktree and preserve current real tips.
git status --short
git branch backup/main-before-pr3-preview main
git branch backup/east-before-pr3-preview feature/east-wing-prototype
git branch backup/sql-before-pr3-preview feature/sql
git branch backup/tracker-before-pr3-preview tracker-updates

# 2. Create a PR3-style merge commit after 4763d6c.
git switch -c preview/pr3-east 4763d6c
git merge --no-ff --no-commit feature/east-wing-prototype
git status
git diff --cached --stat
git commit -m "Merge east-wing prototype before documentation replay" -m "Source-branch: feature/east-wing-prototype" -m "Original-tip: 5fc294c" -m "Followed-by: documentation replay from f3dd43f (PR #2)"

# 3. Replay PR #2 after that merge.
git switch -c preview/candidate-main f3dd43f
git rebase --onto preview/pr3-east 4763d6c

# Resolve README.md in favor of the PR #2 documentation structure.
git add README.md
git rebase --continue
git commit --amend -m "Restructure project documentation (#2)" -m "Replayed-from: f3dd43f" -m "Original-PR: #2"

# 4. Replay the tracker cleanup.
git cherry-pick -x a9862c2

# 5. Preview SQL without changing feature/sql.
git branch preview/sql-after-pr3 feature/sql
git switch preview/sql-after-pr3
git rebase --onto preview/candidate-main a9862c2

# 6. Preview tracker-updates without changing the real tracker branch.
git branch preview/tracker-after-pr3 tracker-updates
git switch preview/tracker-after-pr3
git rebase --onto preview/candidate-main f3dd43f

# If the tracker has a modify/delete conflict, retain the replayed version.
git checkout --theirs docs/ignore/documentation-restructuring-tracker.md
git add -f docs/ignore/documentation-restructuring-tracker.md
git rebase --continue

# 7. Verify history, SQL scope, and tracker placement.
git switch preview/sql-after-pr3
git log --graph --oneline --decorate -10
git diff --name-status preview/candidate-main..HEAD
git ls-tree -r --name-only HEAD -- docs/ignore/documentation-restructuring-tracker.md
git ls-tree -r --name-only preview/tracker-after-pr3 -- docs/ignore/documentation-restructuring-tracker.md

# 8. If a preview is unsuitable, abort an active rebase if necessary.
git rebase --abort
```
