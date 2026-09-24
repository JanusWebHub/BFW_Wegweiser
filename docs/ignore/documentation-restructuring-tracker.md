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
- Decision on 2026-09-24: adopt the PR3-style reconstruction (east-wing merged after `4763d6c`, then the PR #2 replay, then the tracker cleanup). Redo the operations on the real branches, not on `preview/*`, and force-push to JanusWebHub. Permissions are arranged; `main` has no branch protection.
- Preserve the original PR #2 squash commit with the annotated tag `archive/pr-2-squash`.
- See "Branch/merge sequence" below for the full plan.

### Later housekeeping

- Convert edited files to CRLF.
- Add root `.gitattributes` with `* text=auto` in its own commit.
- README content issues found during the PR3 preview (not caused by branch operations; fix after branch work is finished):
  - The workspace layout lists `docs/references/` with four files, but the folder does not exist. Present in `f3dd43f` and therefore on real `main`.
  - The `web/` tree lines for `bfw-eg-ost.svg`, `east_wing.css`, `east_wing.html`, and `east_wing.js` are misindented. Introduced by the east-wing commit `a39e341`.
- README layout gap caused by the replay resolution: `docs/rulebook_sorted.md` (an east-wing file) is not listed in the `docs/` tree, because the conflict hunk was resolved with PR #2's side unchanged.

### Operational notes

- The repository lives in OneDrive. OneDrive can seize git's temporary `.git/rebase-merge` folder mid-rebase (it became a read-only, pinned OneDrive folder), so git cannot delete it and keeps reporting a rebase in progress. Keep OneDrive paused or closed during rebases. If it happens: confirm the folder is empty and nothing else is in progress, then delete the empty folder manually. Do not use `git rebase --abort` in that state: the rebase has already finished, and abort exists to return a branch to its pre-rebase position.
- In a rebase, `--theirs` is the commit being replayed. `git checkout --theirs <file>` restores that version from the index (stage 3), even if the file is missing on disk, and overwrites any local edits.
- Never `git checkout --theirs README.md` during the PR #2 replay: it takes the whole PR #2 README and drops the east-wing content that merged automatically. Resolve only the conflicting hunk.
- Use terminal commands, not VS Code Source Control buttons: "Continue" commits with the default message, and "Publish Branch" would push local-only `preview/*` and `backup/*` branches.
- `git add` marks a conflict resolved even if the file still contains conflict markers. Check for markers before staging. If a commit editor opens for a wrong state, an empty message aborts the commit safely.
- Branch deletions in the OneDrive folder leave empty folders under `.git/refs` and `.git/logs` (answer `n` to the retry prompts). They are harmless.

### Branch/merge sequence (as of 2026-09-24)

1. Archive full unsquashed history to `denizmertmercan/BFW_Wegweiser`: done.
2. Squash-merge `docs/restructure` into JanusWebHub `main`: done.
3. Remove the tracker from `main`; rebase `feature/sql` onto the cleaned `main` and retain it separately: done.
4. Preview and evaluate PR3-style east-wing integration before replaying PR #2: done; PR3-style chosen (see "Preview evaluation").
5. Delete `backup-before-reset`: done (work machine and home machine).
6. Redo the PR3-style reconstruction on the real branches and force-push them to JanusWebHub: done (see "Real-branch reconstruction").

### Home-machine branch picture (as of 2026-09-24, after the force-push)

Remote configuration: `januswebhub` only. Remote heads: `main`, `feature/sql`, `tracker-updates`, `feature/east-wing-prototype`. Tag `archive/pr-2-squash` present locally and on the remote. `feature/east-wing-prototype` is also checked out in the linked worktree `wegweiser-east-wing-prototype`.

| Local branch | Remote branch | Short hash |
| --- | --- | --- |
| `main` | `januswebhub/main` | `2623bd7` |
| `feature/sql` | `januswebhub/feature/sql` | `5472812` |
| `feature/east-wing-prototype` | `januswebhub/feature/east-wing-prototype` | `5fc294c` |
| `tracker-updates` | `januswebhub/tracker-updates` | `f2ded33` (before this checkpoint) |

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

Later on the work machine, before switching machines: `tracker-updates` advanced to `2b46f84`, and `preview/replay-pr2` and `preview/sql-after-replay` were pushed to JanusWebHub intentionally.

Since the force-push, the work machine's `main`, `feature/sql` and `tracker-updates` still point at the old history and must be realigned before any work there. Do not `git pull` or use "Sync Changes" there: that would merge the old history back in. The branches must be reset to the JanusWebHub versions instead.

### Branch/merge log (as of 2026-09-24)

- Fork remote added (`denizmertmercan/BFW_Wegweiser`), `origin` renamed to `januswebhub` for clarity. Full history pushed to the fork: `main`, `docs/restructure`, `local/documentation-restructuring`. `feature/east-wing-prototype` and `backup-before-reset` were deliberately excluded; the latter is disavowed content, not archive-worthy.
- On the fork, demonstrated the fast-forward path (`docs/restructure` → fork's `main`) to confirm full-history preservation works as intended: fork's `main` now at `db3b052`, all 85 commits intact. Both `docs/restructure` and `local/documentation-restructuring` kept as named branches on the fork (not deleted), because the branch labels themselves are part of what "keep full history" means, not just the commit content.
- PR #2 opened and squash-merged on `januswebhub`: `docs/restructure` → `main`. One Copilot review suggestion applied (stale `docs/references/` listing in README.md, caught correctly; that folder was deleted in an earlier commit). Squash commit: `f3dd43f`, "Restructure project documentation (#2)". `main` confirmed single-parent (true squash, not a merge commit).
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
- Home-machine sync on 2026-09-24: `git fetch --all --prune`. Local `main` had diverged: `e3d1be7` (superseded tracker commit, 1 ahead) versus remote `a9862c2` (1 behind). `e3d1be7` content was archived as `docs/ignore/archive/documentation-restructuring-tracker-260924.md` and also remains in `tracker-updates` ancestry. `git reset --hard HEAD~1` moved `main` to `f3dd43f`, then `git merge --ff-only januswebhub/main` fast-forwarded it to `a9862c2`. The fast-forward removed the tracker file from disk (expected; it lives on `tracker-updates`). A temporary `archive/main-tracker-e3d1be7` branch was created and later deleted.
- Home-machine sync on 2026-09-24: created local tracking branches `feature/sql`, `tracker-updates`, `preview/replay-pr2`, `preview/sql-after-replay`. Verified `0de4f03` is outside `main` ancestry, then deleted local `backup-before-reset`.
- Correction on 2026-09-24: the `docs/references/` listing is still in the README at `f3dd43f` (and on real `main`), although the folder does not exist there. The Copilot fix recorded above did not remove this listing.
- Correction on 2026-09-24: the first preview's README (`3688fa8`, on `preview/replay-pr2`) lacks the "East-Wing Prototype" section, so it is not a correct reference resolution. Both previews omit `docs/rulebook_sorted.md` from the layout tree.
- PR3-style preview executed on the home machine on 2026-09-24, following the plan below. No real branch moved; nothing pushed. Details in "Completed PR3-style preview".
- Incident on 2026-09-24: after the PR #2 replay, OneDrive locked the empty `.git/rebase-merge` folder; `git rebase --quit` could not remove it even with OneDrive quit and VS Code restarted. Deleted manually in Explorer; `git status` then clean. A harmless stale `REBASE_HEAD` remains. See "Operational notes".
- Tracker checkpoints on the home machine on 2026-09-24: `947d92e` (preview results) and `a5b0b20` (decision and evaluation), both pushed; rebuilt as `dd3d789` and `f2ded33`.

### Preview evaluation (2026-09-24)

- Direct replay (`preview/replay-pr2`): linear history, east-wing commits inline; its README lost the "East-Wing Prototype" section; the tracker line was not tested. It established only that the file states are compatible.
- PR3-style (`preview/candidate-main`): east-wing shows as its own merge loop; README correct; PR #2 content verified unchanged; the result equals real `main` plus east-wing; `feature/sql` and `tracker-updates` rebase cleanly on top. Chosen.
- The "PR3" merge is a local `git merge --no-ff` commit, the same shape GitHub creates with "Create a merge commit". A GitHub pull request could not produce this history, because it merges on top of the current `main` (after PR #2). No PR #3 page will exist; accepted.
- Consequences of the force-push: `f3dd43f` and `a9862c2` leave `main`'s ancestry (`f3dd43f` stays reachable through the tag `archive/pr-2-squash` and the PR #2 page); other clones (work machine, Janus) must realign; `tracker-updates` must carry `947d92e` and later tracker commits onto the rebuilt base.

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

### Completed PR3-style preview

Executed on the home machine on 2026-09-24. All steps of the plan below succeeded; the abort path was not needed.

```text
4763d6c + 5fc294c -> merge (79bd467) -> M2' (aa5e962) -> cleanup' (8494dad) -> SQL1' (b9c22c4) -> SQL2' (b281326)
                                                         cleanup' (8494dad) -> T1'..T5' (c865a04, 6385ca3, 21dd3da, b282018, 929b2cc)
```

1. Backups: four local `backup/*` branches at `a9862c2`, `5fc294c`, `be9b962`, `2b46f84`.
2. Merge: `79bd467`, parents `4763d6c` and `5fc294c`, no conflicts, 10 files and 38,944 insertions staged. Its tree is identical to `5fc294c` (`4f564b5`).
3. PR #2 replay: one conflict hunk in `README.md` (the `docs/` part of the workspace layout). Resolved with "Accept Incoming" for that hunk only; everything else, including the "East-Wing Prototype" section, merged automatically. Rebase commit `7322431`, then message amended to `aa5e962` (original author and date kept). `git diff f3dd43f aa5e962`: additions only, all east-wing files (10 files, 38,943 insertions, 0 deletions), so PR #2 content is unchanged.
4. Cleanup: `git cherry-pick -x a9862c2` produced `8494dad`. `git diff a9862c2 8494dad` shows the same east-wing additions only, so the candidate equals real `main` plus east-wing.
5. SQL: `b9c22c4`, `b281326`, no conflicts; only `docs/rulebook.md` differs from the candidate. Real `feature/sql` unchanged.
6. Tracker: expected modify/delete conflict at `e3d1be7`, resolved with `git checkout --theirs` plus `git add -f`, giving `c865a04`; the other four commits applied cleanly. The tracker blob at `929b2cc` is identical to the one on `tracker-updates` (`65d1e2c`). Real `tracker-updates` unchanged.
7. Verification: graph shows the merge loop; SQL preview differs only in `docs/rulebook.md`; tracker absent on the SQL preview, present on the tracker preview.

Commit-message note: separate `-m` flags create separate paragraphs, and git only parses the last paragraph as trailers. So `Original-PR: #2` counts as a trailer, but `Replayed-from:` does not, and in the merge message only `Followed-by:` does.

### Real-branch reconstruction

Executed on the home machine on 2026-09-24 and force-pushed to JanusWebHub.

```text
4763d6c + 5fc294c -> merge (73141a3) -> PR #2 (0ddf03b) -> cleanup (2623bd7)   main
                                                           cleanup (2623bd7) -> 0b9da17 -> 5472812   feature/sql
                                                           cleanup (2623bd7) -> 000e2a7 ... f2ded33   tracker-updates
```

| Old | New | Commit |
| --- | --- | --- |
| (none) | `73141a3` | Merge east-wing routing prototype at its branch point |
| `f3dd43f` | `0ddf03b` | Restructure project documentation (#2) |
| `a9862c2` | `2623bd7` | Stop tracking restructuring tracker |
| `c7e454f` | `0b9da17` | feat: add SQL database support |
| `be9b962` | `5472812` | feat: improve UX/UI for the guidance workflow |
| `e3d1be7` | `000e2a7` | update tracker |
| `862ffbd` | `fda2025` | update tracker |
| `5d24b83` | `3f52bec` | Update tracker after SQL rebase |
| `970b19d` | `6c86723` | Overhaul tracker structure |
| `2b46f84` | `a9f40e3` | Record reconstruction previews |
| `947d92e` | `dd3d789` | Record PR3-style preview results |
| `a5b0b20` | `f2ded33` | Record PR3-style decision and preview evaluation |

- Commit messages: the merge carries `Source-branch: feature/east-wing-prototype`; the two replays carry `Replayed-from: <old hash>`. The PR #2 replay keeps its original author and date.
- Verification before the push: each rebuilt branch has the same files as its preview; each differs from its old tip only by the ten east-wing files (additions only); `git range-diff` showed the SQL and tracker commits unchanged (the first tracker commit now creates the file); `5fc294c` is in `main`, `0de4f03` and the original `f3dd43f` are not; `git fsck` clean.
- Push: `git ls-remote` confirmed JanusWebHub unchanged since the last fetch, then `git push --force-with-lease januswebhub main feature/sql tracker-updates`.
- Backups: reused the three preview backups and added `backup/tracker-before-pr3` at `a5b0b20`. After verification and before the push, deleted all local `preview/*` and `backup/*` branches. After the push, deleted the remote `preview/replay-pr2` and `preview/sql-after-replay`.
- The old commits are no longer on any branch; `f3dd43f` stays reachable through tag `archive/pr-2-squash`.
- Incident during the PR #2 replay: the resolve step was skipped and `README.md` was staged with conflict markers. The commit was cancelled with an empty message (git also refused an amend mid-cherry-pick), the conflict was then resolved with "Accept Incoming", and the result matched the preview. The in-between commits `6f6f5ec` and `1fc30fa` were replaced by the message amends and are on no branch.

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
