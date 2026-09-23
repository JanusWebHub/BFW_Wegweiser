# Documentation Restructuring Tracker

## Orientation (as of 2026-09-23)

Read this section first in any new conversation — it stands in for re-explaining the project from scratch.

### Authority order (current)

`rulebook.md` (canon, already overhauled to the new model) → `system-design.md` (in-progress technical spec of that model, being drafted now) → `implementation-plan.md` (future-facing, rewritten after system-design is done) → `devlog.md` (past-facing, immutable historical record — hands off).

Source material being harvested and retired to archive: `roadmap.md`, `working_notes.md`, `zoning_guidelines.md` — all deleted, fully harvested or confirmed to hold nothing further needed. `adr.md` retired.

Critical distinction: the working code/program files still implement the *old* model and are out of compliance with the new rulebook/system-design. Expected, untouched for now — code changes come last, after docs are settled.

Sequencing: (1) docs cleanup [current phase] — finish `system-design.md`, then revise `implementation-plan.md`, then archive the retired docs; (2) only then bring code into compliance with rulebook/system-design.

`docs/references/` deleted entirely: `docs_guidelines.md`, `funnel_algorithm.md`, `funnel.svg`, `research_notes.md` archived out of git tracking.

East-wing prototype (`feature/east-wing-prototype`): working zone/segment derivation and route search exist, but zones/portals are hardcoded, not parsed from the SVG, and terminology (e.g. "walls") isn't rulebook-aligned. Reference for what's reusable vs. new work per Phase.

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

### FLOORFOX migration — distinctly separate, far downstream

Not part of the docs restructuring or branch-merge work above. Only relevant after all of the above (docs cleanup, code brought into compliance, branch consolidation) is complete: remove the JanusWebHub remote entirely, then add `FLOORFOX/BFW_Wegweiser` as the final remote, then push finished history. Do not conflate this with the nearer-term branch/merge sequencing.

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
- `adr.md` is retired. Preserve a local copy under `docs/ignore/` and remove it from Git tracking.
- The canonical filenames remain `rulebook.md` and `devlog.md`; `model-specification.md` and `development-log.md` are not adopted as replacements.
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

### Overall status

Status: `done` · `active` · `open` · `blocked`

### Live status

~~- `1` done — branch created; tracker committed as `6246384`.~~
~~- `2` active — documentation checkpointed in `7312b93` and `65c0590`.~~
- Rulebook checkpoint — renamed to `rulebook.md` in `a2d9648`.
- Rulebook definition refinement — opening, 1.1-1.3, 1.5, and 2.4 revised; the routing-variant rule moved to 3.4 in `f27143c` after tracker update `90a83c1`.
- Rulebook model refinement — Cluster 1/2 wording and Cluster 4 query, state, segment, route, cost, and search structure revised in `fcedb6a` after tracker update `f6fa1b3`.
~~- Abstraction process description added to `working_notes.md` in `9070003`.~~
- Cluster 3 graph model and derivation sequence overhauled in `rulebook.md` in `6aacf4d`.
~~- Visual representation terminology clarified in `working_notes.md` in `a4c78b2`.~~
~~- Archive cleanup done — dated snapshots removed; east-wing worktree retained.~~
~~- ADR retirement decided — move `adr.md` to ignored `docs/ignore/` and remove it from the Git index.~~
- Filename decision reversed — retain `rulebook.md` and `devlog.md`.
- system-design.md / implementation-plan.md refined — see Documents #15/#16. Committed as `fee1077`.
~~- Hard line-wrapping removed repo-wide, whitespace-only — `abfc0fd`.~~
~~- `zoning_guidelines.md` struck — see Documents #4/#16. Catch-up entry; `6a4586d`/`abfc0fd` too small to log individually.~~
~~- `zoning_guidelines.md` fully struck, nothing left unstruck — `1286c29`. Ready for archive.~~
- `zoning_guidelines.md` deleted; implementation-plan.md Phases and Phase 1 detail restructured — `c282fb9`.
- system-design/implementation-plan consistency flags F11-F15 resolved; adjacency graph added to implementation-plan Future direction — `c26df5c`.
- README.md rewritten; system-design/implementation-plan pipeline split; roadmap.md deleted — `97a7a1f`.
- `working_notes.md` trimmed to two sections (kept nothing else needed) — `cb2aad8`; deleted entirely, everything else already outdated or already integrated. `962da60`.
- `docs/references/` deleted entirely — `docs_guidelines.md`, `research_notes.md`, `funnel_algorithm.md`, `funnel.svg` archived out of git tracking — `d14a3cd`.

### Documents

~~| # | Document | Status | Note |~~
~~| --- | --- | --- | --- |~~
~~| 1 | `convergences.md` | done | Retired. Title + intro survive in `research_notes.md`. Deleted. |~~
~~| 2 | `docs_guidelines.md` | done | Line-endings rule added (CRLF working tree, LF repo, `.gitattributes`, repo-wide). Converted to CRLF. Archived out of `docs/references/`. |~~
~~| 3 | `research_notes.md` | done | Poincare removed, row 6 reworded, sections merged, project refs stripped, intro rewritten. Archived out of `docs/references/`. |~~
~~| 4 | `zoning_guidelines.md` | done | Deleted; Phase A migrated to implementation-plan.md. |~~
~~| 5 | `working_notes.md` | done | Deleted — `962da60`. Nothing left to harvest; remainder was outdated terminology or already integrated into rulebook/system-design/implementation-plan. |~~
~~| 6 | `roadmap.md` | done | Deleted — `97a7a1f`. |~~
| 7 | `README.md` | done | Rewritten to match the current model — `97a7a1f`. |
~~| 8 | `axioms.md` | done | Retired to `docs/ignore/retired`. Replaced by `rulebook.md`. |~~
~~| 9 | `adr.md` | open | Retired; move to ignored `docs/ignore/` and remove from Git tracking. |~~
~~| 10 | `devlog.md` | done | Byte-identical to backup (13 801 B, same mtime). Untouched, as required. |~~
~~| 11 | `glossary.md` | done | Retired. Core/Derived/Movement/Roles -> rulebook D.2, D.4, D.14. Rejected-words table dropped (Q3 resolved). `edges` rule survives as roadmap Phase 2 task. |~~
~~| 12 | `design_recap.md` | done | Retired. Sections 1-3, 5 already in `working_notes.md`; 7 in `zoning_guidelines.md`; 6, 8, 9 dropped as covered by `roadmap.md`; 4 dropped with Q3. |~~
~~| 13 | `graphic_strategy.md` | done | Retired. §1 decision already ADR 5; viewBox guarantee -> `zoning_guidelines.md`; pipeline diagram dropped (superseded by rulebook R.5). Phase B covered by roadmap P2 + geometry added. Phase C -> `working_notes.md`. §5 split: two items covered by roadmap P2, `data-kind` hook added there, multi-floor group -> `zoning_guidelines.md`, verification loop -> README step 4. |~~
| 14 | `rulebook.md` | active | Model refinement checkpointed in `fcedb6a`; Cluster 3 graph model overhauled in `6aacf4d`. |
| 15 | `system-design.md` | active | Settled in `fee1077`; F11/F13/F14 fixed in `c26df5c`; pipeline steps 3-4 split in `97a7a1f`. Harvest complete — nothing in working_notes.md was needed. |
| 16 | `implementation-plan.md` | active | Restructured in `c282fb9`; F12/F15 fixed in `c26df5c`; Phase 2/3 and heading nesting fixed in `97a7a1f`; E13 folded into Authoring procedure in `962da60`. Harvest complete — nothing in working_notes.md was needed. |

## Completion

### Final wrap-up

| # | Item | Status |
| --- | --- | --- |
| W1 | Devlog entry for the documentation restructuring. The old commit `0de4f03` was reset out of history, so no entry is owed for it. | open |
| W2 | Review final state of all files | open |
| W3 | Line endings: convert files edited in chat to CRLF | open |
| W4 | After the feature merge, remove the old remote, add FLOORFOX, and push the finished history | open |
| W5 | Delete branch `backup-before-reset` once satisfied | open |
~~| W6 | Place `funnel_algorithm.md`, `funnel.svg`, and `convex-segments.svg` if still required | superseded — `docs/references/` deleted entirely, all four files archived out of git tracking. |~~
~~| W7 | Promote `validate_plan.py` into `src/` if still required | superseded — implementation-plan.md Phase 1 defines a validator script to be built fresh against the current contract, not the archived file |~~
~~| W8 | Correct the funnel wording in `research_notes.md` | moot — `research_notes.md` archived out of git tracking |~~

### Housekeeping

| # | Item | Status |
| --- | --- | --- |
~~| H1 | `_to_delete/` removed; retired docs deleted in place from now on | done |~~
| H2 | `.gitattributes` with `* text=auto` at project root | open — own commit; renormalises the whole repo once |
~~| H3 | Convert `working_notes.md` and `docs/references/docs_guidelines.md` to CRLF | done |~~
~~| H4 | Future prompts: ban all git commands, not only write operations | noted |~~

## Archive

Backups are in `docs/ignore/archive`.
Non-documentation artifacts are in `docs/ignore/archive/other`.
