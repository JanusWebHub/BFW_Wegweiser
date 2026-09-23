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
- `docs/restructure` (branched from `local/documentation-restructuring` at `67f1c2d`): current, most focused pass, currently HEAD — check `git log` for the live tip, not this doc.
- `backup-before-reset`: orphaned safety branch off main tip, holds one extra commit `0de4f03` ("Document semantic floor plans and portal graph architecture") never merged anywhere. This is a false start, not salvageable material — explicitly obsolete, must never re-enter `main` or feature-branch ancestry (see Restructuring Decisions). No devlog entry owed for it (W1). Branch slated for deletion once verified (W5).

### Branch/merge sequence — two alternatives under consideration

Not yet settled which one governs; both recorded until decided.

**A — direct-to-main (original decision, line 11 and Review Order below):** `main` stays based on `4763d6c`; final documentation files are committed directly on `main`; `local/documentation-restructuring` and `docs/restructure` are scratch/temporary branches discarded (not merged forward) once their content lands on `main`; then `feature/east-wing-prototype` rebases onto migrated `main`, dropping `0de4f03` from its ancestry, and merges in.

**B — forward-merge chain (newer, being reconsidered):** `docs/restructure` merges into `local/documentation-restructuring` → that merges or is cherry-picked into `main` → `feature/east-wing-prototype` rebases onto that post-restructuring `main` commit, merges in, and is then reworked to match the new model/system-design, eventually becoming the new `main`.

Both alternatives agree on: `0de4f03` never enters final ancestry; east-wing rebases (not merges as-is) onto a post-restructuring `main`; east-wing gets reworked to the new model after landing.

## Control

### Made Decisions

#### Restructuring Decisions

- `main` remains based on `4763d6c`.
- The documentation restructuring is intentional and remains on the temporary branch until reviewed and transferred to `main`.
- A temporary local branch tracks the tracker and restructuring; the ignored tracker is force-added.
- Checkpoint pattern: documentation commit, tracker update naming it, tracker commit.
- The obsolete commit `0de4f03` must not remain in the final `main` or feature-branch ancestry.
- The local `backup-before-reset` branch may be deleted after verification.
- Final documentation files are committed directly on `main`; the temporary branch is then deleted.
- The JanusWebHub remote will be removed entirely at the end.
- `FLOORFOX/BFW_Wegweiser` becomes the final remote only after the migration and feature work are complete.

### Sequence

#### Review Order

1. Create the temporary local branch and force-add the tracker.
2. Review, checkpoint, and finish the documentation restructuring.
3. Commit the final documentation files on `main`.
4. Delete the temporary branch.
5. Rebase `feature/east-wing-prototype` onto the migrated `main`, removing `0de4f03` from its ancestry.
6. Resolve conflicts and validate the feature.
7. Merge the feature into `main`.
8. Delete `backup-before-reset` after verification.
9. Remove the old remote, add the FLOORFOX remote, and push the finished history.

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
| W4 | After the feature merge, remove the old remote, add FLOORFOX, and push the finished history | open |
| W5 | Delete branch `backup-before-reset` once satisfied | open |
| W6 | `.gitattributes` with `* text=auto` at project root | open — own commit; renormalises the whole repo once |
