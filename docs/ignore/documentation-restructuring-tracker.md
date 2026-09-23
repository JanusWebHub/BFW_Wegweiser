# Documentation Restructuring Tracker

## Orientation (as of 2026-09-23)

Read this section first in any new conversation — it stands in for re-explaining the project from scratch.

### Authority order (current)

`rulebook.md` (canon, already overhauled to the new model) → `system-design.md` (in-progress technical spec of that model, being drafted now) → `implementation-plan.md` (future-facing, rewritten after system-design is done) → `devlog.md` (past-facing, immutable historical record — hands off).

Critical distinction: the working code/program files still implement the *old* model and are out of compliance with the new rulebook/system-design. Expected, untouched for now — code changes come only after branch merging is fully complete.

### Branch picture (as of 2026-09-23)

- `main` (tip `4763d6c`): original implementation. Upload → German→English cleanup, type hints, tests, devlog/ADR introduction → src/web restructure → JSON compiler/web client split → roadmap docs. Baseline all other branches fork from.
- `feature/east-wing-prototype` (2 commits ahead of `4763d6c`): `a39e341` east-wing routing prototype + `5fc294c` rulebook update. Small, self-contained. To be reworked against the new model/system-design after it lands on `main`.
- `local/documentation-restructuring` (branched from main, ending `67f1c2d`): the broad docs-restructuring effort — tracker-checkpoint commits interleaved with substantive rulebook refinement (foundations → definitions → model → graph model → cluster headings → abstraction process → visual graph representations).
- `docs/restructure` (branched from `local/documentation-restructuring` at `67f1c2d`): current, most focused pass, currently HEAD — check `git log` for the live tip, not this doc. 85 commits total, ~25 pure tracker-checkpoint noise.
- `origin/feature/sql` (Janus, 2 commits, branched off `docs/restructure` at `6e413e7`): appends rulebook clusters 5 (usage analytics and feedback) and 6 (UI and UX). Only touches `docs/rulebook.md`, append-only. Predates the current rulebook restructuring; will need rebasing.
- `backup-before-reset`: orphaned safety branch off main tip, holds one extra commit `0de4f03` ("Document semantic floor plans and portal graph architecture") never merged anywhere. This is a false start, not salvageable material — explicitly obsolete, must never re-enter `main` or feature-branch ancestry (see Restructuring Decisions). No devlog entry owed for it (W1). Branch slated for deletion once verified (W5).
- `origin/copilot/common-design-patterns`: a rejected/closed Copilot PR, identical to `main`, never real work. Ignore; not tracked as a branch to merge or clean up.

### Branch/merge sequence — decided

1. Archive full, unsquashed history (including all tracker-checkpoint noise) to `denizmertmercan/BFW_Wegweiser` (personal fork) first, before anything below touches `JanusWebHub/BFW_Wegweiser`. This is the permanent record of the granular process; nothing here needs to stay clutter-free.
2. Open a PR: `docs/restructure` → `main` on `JanusWebHub/BFW_Wegweiser`. Squash and merge via GitHub (not a local squash) so the PR page permanently preserves all original commits even after the source branches are deleted.
3. Rebase `feature/sql` onto the new `main` tip, resolve any conflicts (low risk — append-only, touches only `rulebook.md`), merge in as its own small step.
4. Rebase `feature/east-wing-prototype` onto the same `main` tip, dropping `0de4f03` from its ancestry (it was never actually in east-wing's history, but confirm), resolve/validate, merge in as its own small step.
5. Delete `backup-before-reset` after verification (see W5, Final wrap-up).
6. Only once `main` is fully merged and clean: remove the JanusWebHub remote, add `FLOORFOX/BFW_Wegweiser`, push finished history.

`0de4f03` must never enter `main`'s final ancestry via any path.

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
| `rulebook.md` | active | Renamed and checkpointed in `a2d9648`; definitions revised in `f27143c`; model refined (Cluster 1/2 wording, Cluster 4 query/state/segment/route/cost/search) in `fcedb6a`; Cluster 3 graph model and derivation sequence overhauled in `6aacf4d`. |
| `system-design.md` | active | Settled in `fee1077`; F11/F13/F14 fixed in `c26df5c`; pipeline steps 3-4 split in `97a7a1f`. Harvest complete — nothing in `working_notes.md` was needed. |
| `implementation-plan.md` | active | Restructured in `c282fb9`; F12/F15 fixed in `c26df5c`; Phase 2/3 and heading nesting fixed in `97a7a1f`; E13 folded into Authoring procedure in `962da60`. Harvest complete — nothing in `working_notes.md` was needed. |

## Final wrap-up

| # | Item | Status |
| --- | --- | --- |
| W1 | Devlog entry for the documentation restructuring. The old commit `0de4f03` was reset out of history, so no entry is owed for it. | open |
| W2 | Review final state of all files | open |
| W3 | Line endings: convert files edited in chat to CRLF | open |
| W4 | Remote swap to FLOORFOX — see "Branch/merge sequence — decided", step 6 | open |
| W5 | Delete branch `backup-before-reset` once satisfied | open |
| W6 | `.gitattributes` with `* text=auto` at project root | open — own commit; renormalises the whole repo once |
