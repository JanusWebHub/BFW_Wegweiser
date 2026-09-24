# Documentation Restructuring Tracker

## Orientation (as of 2026-09-23)

Read this section first in any new conversation — it stands in for re-explaining the project from scratch.

### Authority order (current)

`rulebook.md` (canon) → `system-design.md` (technical specification) → `implementation-plan.md` (future-facing plan) → `devlog.md` (past-facing, immutable historical record — hands off).

Critical distinction: the working code/program files still implement the *old* model and are out of compliance with the new rulebook/system-design. Expected, untouched for now — code changes come only after branch merging is fully complete.

### Branch picture (as of 2026-09-23)

- `main` (tip `f3dd43f` — squash commit, see Branch/merge log): original implementation, now carrying the squashed docs restructuring on top.
- `feature/east-wing-prototype` (2 commits ahead of old `4763d6c`): `a39e341` east-wing routing prototype + `5fc294c` rulebook update. Small, self-contained. Still needs rebasing onto new `main` — not yet done.
- `feature/sql` (Janus, 2 commits, `55ec7ef`/`07ae881`, branched off old `docs/restructure` at `6e413e7`): appends rulebook clusters 5 (usage analytics and feedback) and 6 (UI and UX). Still needs rebasing onto new `main` — not yet done. See rebase-preview finding below; not low-risk as originally assumed.
- `backup-before-reset`: orphaned safety branch off old main tip, holds one extra commit `0de4f03` ("Document semantic floor plans and portal graph architecture") never merged anywhere. False start, not salvageable, must never enter `main`'s ancestry. Not yet deleted (W5).
- `docs/restructure`, `local/documentation-restructuring`: deleted, both locally and on `januswebhub`, after the squash-merge (see Branch/merge log). Full history preserved in PR #2 and on `denizmertmercan` fork.
- `copilot/common-design-patterns`: deleted agent-created branch; identical to `main`, never real work.

Remotes: `januswebhub` (`JanusWebHub/BFW_Wegweiser`, the active repo) and `denizmertmercan` (`denizmertmercan/BFW_Wegweiser`, personal fork/archive). Both configured with these names, not `origin`/`fork`.

### Current work-machine branch picture (as of 2026-09-24)

Remote configuration: `januswebhub` only; `floorfox` removed.

| Local branch | Remote branch | Short hash |
| --- | --- | --- |
| `main` | `januswebhub/main` | `e3d1be7` |
| `feature/sql` | `januswebhub/feature/sql` | `07ae881` |
| `feature/east-wing-prototype` | `januswebhub/feature/east-wing-prototype` | `5fc294c` |

### Branch/merge sequence — decided

1. Archive full unsquashed history to `denizmertmercan/BFW_Wegweiser`. — done
2. Squash-merge `docs/restructure` into JanusWebHub `main`. — done
3. Rebase and merge `feature/sql` into `main`. — outstanding
4. Rebase and merge `feature/east-wing-prototype` into `main`. — outstanding
5. Delete `backup-before-reset`. — done
6. Replace the JanusWebHub remote with `FLOORFOX/BFW_Wegweiser` and push. — outstanding

`0de4f03` must never enter `main`'s final ancestry via any path.

### Branch/merge log

- Fork remote added (`denizmertmercan/BFW_Wegweiser`), `origin` renamed to `januswebhub` for clarity. Full history pushed to the fork: `main`, `docs/restructure`, `local/documentation-restructuring`. `feature/east-wing-prototype` and `backup-before-reset` deliberately excluded — east-wing lands on `main` via normal rebase anyway (nothing at risk of being flattened), `backup-before-reset` is disavowed content, not archive-worthy.
- On the fork, demonstrated the fast-forward path (`docs/restructure` → fork's `main`) to confirm full-history preservation works as intended — fork's `main` now at `db3b052`, all 85 commits intact. Both `docs/restructure` and `local/documentation-restructuring` kept as named branches on the fork (not deleted) — the branch labels themselves are part of what "keep full history" means, not just the commit content.
- PR #2 opened and squash-merged on `januswebhub`: `docs/restructure` → `main`. One Copilot review suggestion applied (stale `docs/references/` listing in README.md, caught correctly — that folder was deleted in an earlier commit). Squash commit: `f3dd43f`, "Restructure project documentation (#2)". `main` confirmed single-parent (true squash, not a merge commit).
- `docs/restructure` and `local/documentation-restructuring` deleted on `januswebhub` and locally, post-merge. Both fully recoverable via PR #2 and the `denizmertmercan` fork.
- `copilot/common-design-patterns` deleted on `januswebhub` (agent-created branch, identical to old `main`, no real content).
- Rebase preview for `feature/sql` (read-only diff inspection, not an actual rebase attempt): `docs/rulebook.md` at `feature/sql`'s fork point (`6e413e7`) is byte-identical to `docs/rulebook.md` on current `main` — that file's diff will apply cleanly. However `README.md`, `docs/adr.md`, and `docs/roadmap.md` will conflict on a real rebase (modify/delete conflicts — `feature/sql`'s inherited commits still touch files the squash-merge deleted). Corrects the earlier "low risk, append-only" assumption in step 3 above — real conflict resolution is needed on those three files, though `rulebook.md` itself (Janus's actual content) is unaffected.
- Work-machine baseline on 2026-09-24: `main` → `januswebhub/main` (`e3d1be7`); `feature/sql` → `januswebhub/feature/sql` (`07ae881`); `feature/east-wing-prototype` → `januswebhub/feature/east-wing-prototype` (`5fc294c`); `docs/restructure` → `januswebhub/docs/restructure` (`55c8cf3`); `local/documentation-restructuring` → `januswebhub/local/documentation-restructuring` (`67f1c2d`); `backup-before-reset` had no remote (`0de4f03`). Remotes: `januswebhub` and `floorfox`; Janus also had `copilot/common-design-patterns` (`4763d6c`).
- Work-machine operation on 2026-09-24: `git remote remove floorfox` removed the Floorfox remote and its tracking refs.
- Work-machine operation on 2026-09-24: `git fetch --all --prune` removed stale Janus tracking refs for `copilot/common-design-patterns`, `docs/restructure`, and `local/documentation-restructuring`.
- Work-machine operation on 2026-09-24: `git branch -D` deleted local `docs/restructure`, `local/documentation-restructuring`, and `backup-before-reset`.
- Work-machine verification on 2026-09-24: `git ls-remote --heads januswebhub` showed only `main`, `feature/sql`, and `feature/east-wing-prototype`; `git merge-base --is-ancestor 0de4f03 main` confirmed `0de4f03` is outside `main` ancestry.

## Control

### Made Decisions

#### Restructuring Decisions

- A temporary local branch tracks the tracker and restructuring; the ignored tracker is force-added.
- Checkpoint pattern: documentation commit, tracker update naming it, tracker commit.
- See "Branch/merge sequence — decided" above for the full merge plan.

## Status

| Document | Status | Note |
| --- | --- | --- |
| `README.md` | done | Rewritten to match the current model — `97a7a1f`. |
| `rulebook.md` | done | Renamed and checkpointed in `a2d9648`; definitions revised in `f27143c`; model refined (Cluster 1/2 wording, Cluster 4 query/state/segment/route/cost/search) in `fcedb6a`; Cluster 3 graph model and derivation sequence overhauled in `6aacf4d`. |
| `system-design.md` | done | Settled in `fee1077`; F11/F13/F14 fixed in `c26df5c`; pipeline steps 3-4 split in `97a7a1f`. Harvest complete — nothing in `working_notes.md` was needed. |
| `implementation-plan.md` | done | Restructured in `c282fb9`; F12/F15 fixed in `c26df5c`; Phase 2/3 and heading nesting fixed in `97a7a1f`; E13 folded into Authoring procedure in `962da60`. Harvest complete — nothing in `working_notes.md` was needed. |

## Final wrap-up

| # | Item | Status |
| --- | --- | --- |
| W1 | Devlog entry for the documentation restructuring. The old commit `0de4f03` was reset out of history, so no entry is owed for it. | open |
| W2 | Review final state of all files | open |
| W3 | Line endings: convert files edited in chat to CRLF | open |
| W4 | Remote swap to FLOORFOX — see "Branch/merge sequence — decided", step 6 | open — `floorfox` removed locally for now; re-add only after `main` is complete |
| W5 | Delete branch `backup-before-reset` once satisfied | done — deleted locally on 2026-09-24; confirmed outside `main` ancestry |
| W6 | `.gitattributes` with `* text=auto` at project root | open — own commit; renormalises the whole repo once |
