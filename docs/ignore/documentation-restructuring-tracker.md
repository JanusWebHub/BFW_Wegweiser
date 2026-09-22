# Documentation Restructuring Tracker

Local-only working tracker. Not part of the committed project documentation.

## Orientation (as of 2026-09-22)

Read this section first in any new conversation — it stands in for re-explaining the project from scratch.

### Authority order (current)

`rulebook.md` (canon, already overhauled to the new model) → `system-design.md` (in-progress technical spec of that model, being drafted now) → `implementation-plan.md` (future-facing, rewritten after system-design is done) → `devlog.md` (past-facing, immutable historical record — hands off).

Source material being harvested and retired to archive: `roadmap.md`, `working_notes.md` still pending; `zoning_guidelines.md` fully harvested and deleted. `adr.md` retires alongside the remaining two (see Documents table).

Critical distinction: the working code/program files still implement the *old* model and are out of compliance with the new rulebook/system-design. Expected, untouched for now — code changes come last, after docs are settled.

Sequencing: (1) docs cleanup [current phase] — finish `system-design.md`, then revise `implementation-plan.md`, then archive the retired docs; (2) only then bring code into compliance with rulebook/system-design.

`implementation-plan.md`'s Phases are ordered by actual build dependency, not by mirroring the model's pipeline structure, read the doc for current content. Still needs roadmap.md/working_notes.md harvested in.

Connectivity graph: produced *alongside* the floor plan during zoning (rulebook §3.2), not derived after. `system-design.md` §2.2 still lists it as "derived," unreconciled but not a real conflict, both true from different angles.

`docs/references/` (tracked): `docs_guidelines.md`, `funnel_algorithm.md`, `funnel.svg`, `research_notes.md`.

East-wing prototype (`feature/east-wing-prototype`): working zone/segment derivation and route search exist, but zones/portals are hardcoded, not parsed from the SVG, and terminology (e.g. "walls") isn't rulebook-aligned. Reference for what's reusable vs. new work per Phase.

### Branch picture (as of 2026-09-22)

- `main` (tip `4763d6c`): original implementation. Upload → German→English cleanup, type hints, tests, devlog/ADR introduction → src/web restructure → JSON compiler/web client split → roadmap docs. Baseline all other branches fork from.
- `feature/east-wing-prototype` (2 commits ahead of `4763d6c`): `a39e341` east-wing routing prototype + `5fc294c` rulebook update. Small, self-contained. To be reworked against the new model/system-design after it lands on `main`.
- `local/documentation-restructuring` (27 commits ahead of main, ending `67f1c2d`): the broad docs-restructuring effort — tracker-checkpoint commits interleaved with substantive rulebook refinement (foundations → definitions → model → graph model → cluster headings → abstraction process → visual graph representations).
- `docs/restructure` (branched from `local/documentation-restructuring` at `67f1c2d`, 1 commit ahead: `140d58d` "Restructure project documentation"): current, most focused pass, currently HEAD.
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

#### Rulebook Decisions

- Structure: the rulebook progressed from lettered layers to numbered subject sections and then five conceptual clusters; Cluster 5 was absorbed into Cluster 1, leaving four active clusters.
- Cluster 1: keep zone, separator, portal, and segment distinct. Treat boundary and separator together; separators divide spaces architecturally and are represented as zone boundaries after zoning. Virtual boundaries may separate zones without physical separators. Move the two-dimensional premise and exterior into this cluster. Define the simplified plan as derived from the architectural plans, retaining features relevant to navigation. Define portals as crossable boundary portions represented by midpoints; they may correspond to physical or virtual openings, always join exactly two zones, and remain pair-specific where zones meet at a point.
- Cluster 2: order walkable/non-walkable part, obstacle, movement zone, movement line; preserve their distinctions. Clarify obstacles as fixed obstructions in the non-walkable part of a zone; routes neither end at nor pass through them. Define a movement line as a designer-drawn representation of the path people actually take through a movement zone.
- Cluster 3: define adjacency, zoning and connectivity, and routing in that order using space/separator, zone/portal, and portal/segment terminology. Keep the routing-variant rule after the routing graph definition. Remove the redundant pipeline diagram after reviewing its content against the graph and search definitions.
- Cluster 4: keep query, state, segment, route, and search in dependency order, with search last. Define the query as a zone-level request, states as directed `zone | portal | zone` transitions with special costs, segments as `portal | zone | portal` portions between consecutive states with distance and special costs, routes as alternating zone/portal sequences with total costs, and search as multi-source/multi-target selection of the lowest-cost route. — done (`fcedb6a`)
- Cluster 5: absorb its entries into Cluster 1; do not leave a standalone cluster.

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

### Rulebook review order

1. Create a checkpoint. — done
2. Make reorder-only changes in small independent blocks. — done
3. Validate the reordered rulebook and checkpoint. — done
4. Apply obvious, low-risk content changes. — done
5. Validate and checkpoint again. — done
6. Rework the zone/boundary/wall relationship carefully. — done (`cd83b4e`)
7. Rework the graph definitions and derivation sequence. — done (`6aacf4d`)
8. Revisit the pipeline explanation and diagram last. — done — the pipeline diagram was removed from the rulebook after its graph and search content was distributed across Clusters 3 and 4.

Each block remains separate and increasingly invasive.

## Status

### Overall status

Status: `done` · `active` · `open` · `blocked`

### Live status

- `1` done — branch created; tracker committed as `6246384`.
- `2` active — documentation checkpointed in `7312b93` and `65c0590`.
- Rulebook checkpoint — renamed to `rulebook.md` in `a2d9648`.
- Rulebook definition refinement — opening, 1.1-1.3, 1.5, and 2.4 revised; the routing-variant rule moved to 3.4 in `f27143c` after tracker update `90a83c1`.
- Rulebook model refinement — Cluster 1/2 wording and Cluster 4 query, state, segment, route, cost, and search structure revised in `fcedb6a` after tracker update `f6fa1b3`.
- Abstraction process description added to `working_notes.md` in `9070003`.
- Cluster 3 graph model and derivation sequence overhauled in `rulebook.md` in `6aacf4d`.
- Visual representation terminology clarified in `working_notes.md` in `a4c78b2`.
- Archive cleanup done — dated snapshots removed; east-wing worktree retained.
- ADR retirement decided — move `adr.md` to ignored `docs/ignore/` and remove it from the Git index.
- Filename decision reversed — retain `rulebook.md` and `devlog.md`.
- system-design.md / implementation-plan.md refined — see Documents #15/#16. Committed as `fee1077`.
- Hard line-wrapping removed repo-wide, whitespace-only — `abfc0fd`.
- `zoning_guidelines.md` struck — see Documents #4/#16. Catch-up entry; `6a4586d`/`abfc0fd` too small to log individually.
- `zoning_guidelines.md` fully struck, nothing left unstruck — `1286c29`. Ready for archive.
- `zoning_guidelines.md` deleted; implementation-plan.md Phases and Phase 1 detail restructured — `c282fb9`.

### Documents

| # | Document | Status | Note |
| --- | --- | --- | --- |
| 1 | `convergences.md` | done | Retired. Title + intro survive in `research_notes.md`. Deleted. |
| 2 | `docs_guidelines.md` | done | Line-endings rule added (CRLF working tree, LF repo, `.gitattributes`, repo-wide). Converted to CRLF. |
| 3 | `research_notes.md` | done | Poincare removed, row 6 reworded, sections merged, project refs stripped, intro rewritten. |
| 4 | `zoning_guidelines.md` | done | Deleted; Phase A migrated to implementation-plan.md. |
| 5 | `working_notes.md` | open | |
| 6 | `roadmap.md` | open | |
| 7 | `README.md` | done | Relative links removed, `.gitattributes` added to tree, inline doc descriptors, Python 3.10+, Milestones deduplicated, verification loop added as Quick Start step 4. |
| 8 | `axioms.md` | done | Retired to `docs/ignore/retired`. Replaced by `rulebook.md`. |
| 9 | `adr.md` | open | Retired; move to ignored `docs/ignore/` and remove from Git tracking. |
| 10 | `devlog.md` | done | Byte-identical to backup (13 801 B, same mtime). Untouched, as required. |
| 11 | `glossary.md` | done | Retired. Core/Derived/Movement/Roles -> rulebook D.2, D.4, D.14. Rejected-words table dropped (Q3 resolved). `edges` rule survives as roadmap Phase 2 task. |
| 12 | `design_recap.md` | done | Retired. Sections 1-3, 5 already in `working_notes.md`; 7 in `zoning_guidelines.md`; 6, 8, 9 dropped as covered by `roadmap.md`; 4 dropped with Q3. |
| 13 | `graphic_strategy.md` | done | Retired. §1 decision already ADR 5; viewBox guarantee -> `zoning_guidelines.md`; pipeline diagram dropped (superseded by rulebook R.5). Phase B covered by roadmap P2 + geometry added. Phase C -> `working_notes.md`. §5 split: two items covered by roadmap P2, `data-kind` hook added there, multi-floor group -> `zoning_guidelines.md`, verification loop -> README step 4. |
| 14 | `rulebook.md` | active | Model refinement checkpointed in `fcedb6a`; Cluster 3 graph model overhauled in `6aacf4d`. |
| 15 | `system-design.md` | active | Opening description, Modeling pipeline, Representations, Costs sections settled in `fee1077`. Still to receive harvest from roadmap/working_notes/zoning_guidelines. |
| 16 | `implementation-plan.md` | active | Opening, Phases, and Phase 1 detail restructured; zoning_guidelines migrated in. Still to harvest roadmap/working_notes. |

## Open items

### Circle-back items — harvested from archive

| # | Item | Source | Target |
| --- | --- | --- | --- |
| ~~C1~~ | ~~Concrete cost model: distance + turn/door/floor-change penalties. Rulebook §4.2-4.3 only mention "special costs" abstractly, no concrete penalty table.~~ | ~~`docs/ignore/archive/wegweiser-design.md` §3~~ | ~~Resolved — light-touch clarification only, no penalty table (would over-prescribe). Landed as `system-design.md` §3 Costs in `fee1077`.~~ |
| ~~C2~~ | ~~Algorithm evaluation (BFS vs Dijkstra vs A\* vs Voronoi/arc-flags/HPA\*) against real building shape (star + eastern block with cycles).~~ | ~~`docs/ignore/archive/eval.md`~~ | ~~Resolved — discarded. Algorithm choice deferred to when implementation-plan actually needs it; nothing to harvest now without prescribing.~~ |

### Open Decisions

~~- `edges` versus `connections`: naming rule has no current home. Resolved as `edges`, consistent with the rulebook.~~

| # | Item | Decision |
| --- | --- | --- |
| ~~D1~~ | ~~Q1 — glossary definitions~~ | ~~Resolved — into `rulebook.md`: partition into D.2, portal-need-not-be-a-door and virtual portal into D.4, role table into D.14~~ |
| ~~D2~~ | ~~Q2 — graphic_strategy §1~~ | ~~Resolved — decision stays ADR 5; the shared-`viewBox` consequence went to `zoning_guidelines.md`, not the rulebook, since it follows from a tooling decision not from the model~~ |
| ~~D3~~ | ~~Q3 — discarded/rejected terms~~ | ~~Resolved — table dropped entirely. Hub dead; branch/leaf superseded by D.16; crossable now a rulebook property (D.7) so rejecting it would be wrong; junction and decision point still live but not worth a doc~~ |
| ~~D5~~ | ~~Axiom 12 vs multi-source formulation~~ | ~~Resolved — merged in rulebook S.2: outbound/inbound states plus the stopping rule~~ |
| ~~D6~~ | ~~Two axiom candidates~~ | ~~Resolved — "routing graph is portals and segments only" is D.15; "every segment lies in one zone" is D.5~~ |
| ~~D7~~ | ~~GS Phase B — roadmap topology.json lacks zone geometry~~ | ~~Resolved — geometry added to roadmap Phase 2~~ |
| ~~D8~~ | ~~GS Phase C — OpenCV pipeline uncovered~~ | ~~Resolved — in `working_notes.md` after the Options table~~ |
| ~~D9~~ | ~~GS §5 — `data-kind` CSS hook, `<g id="floor:eg">`, verification loop~~ | ~~Resolved — all three applied~~ |

### Flags — substantive

| # | Flag | Where |
| --- | --- | --- |
| F10 | ~~zoning_guidelines side resolved — `axioms.md` citation and `aussen`-reserved-zone-id content struck with the rest of the Data Model table (`30bfbb3`)~~. `roadmap.md` and `working_notes.md` still cite retired `axioms.md` | roadmap, working_notes |
| F9 | `docs/references/docs_guidelines.md` has no rule for code naming; `edges` not `connections` has no home outside roadmap Phase 2 | docs_guidelines |
| F1 | ~~Resolved — the axioms 17–18 reading is discarded. A doorless portal from splitting a zone is an ordinary portal~~ | glossary |
| F2 | "Rooms are never crossed" contradicts axioms 8/19 | working_notes recap entry |
~~| F3 | Resolved — the whole Authoring Contract section (including rule 5) was struck (`30bfbb3`) | zoning_guidelines |~~
| F4 | Not resolved — "segment" is the term, but `working_notes.md` still uses "path" throughout, including a whole element-table row (Elements section, ~line 130-220) | working_notes |
| F5 | Obstacle rule conflict: glossary "booths → obstacle always" vs working_notes "designer's decision, case by case" | glossary, working_notes, zoning_guidelines |
| F6 | `validate_plan.py` not in repo; roadmap path `docs/ignore/files_260911/` does not exist | roadmap |
| F7 | Roadmap P2 says `start_point` is orphaned; code no longer is | roadmap |
| F8 | Recap "This is not places linked by corridors" left without its positive counterpart after the purge | working_notes |

### Flags — editorial

| # | Flag | Where |
| --- | --- | --- |
| E1 | Intro describes only the convergences table; doc now also holds graph theory notes and node/edge paragraph | research_notes |
~~| E2 | Resolved — both copies (contract rule 3 and the standalone Naming Conventions section) struck (`30bfbb3`) | zoning_guidelines |~~
~~| E3 | zoning_guidelines side resolved — the "Floor plan work" copy struck; Phase A's copy is now the only one left in this file (`3c266ca`) | zoning_guidelines |~~
~~| E4 | zoning_guidelines side resolved — both the inline sentence and the standalone "Duplicate portals" section struck (`30bfbb3`) | zoning_guidelines |~~
| E5 | "To purge" section still lists wrong framings and retired docs by name | working_notes |
| E6 | 13 relative links remain (README 2, roadmap 11), against the new rule | README, roadmap |
| E7 | Options table row says "deferred to Phase C" — only valid if Phase C lands (see D8) | working_notes |
| E8 | Build order dropped, but recap and roadmap disagree on multi-floor vs guidance order | roadmap |
| E9 | Purge wording edits to verify: "Used for the graphs", roadmap P2 dropped "at the graph layer", "encodes the zones and portals" | research_notes, roadmap, zoning_guidelines |
| E10 | Roadmap open questions 1–2 reverted to recap wording — verify | roadmap |
| E11 | Recap entry dated to month only ("2026-09"); evidence points to 09-10/11 | working_notes |
| E12 | Phase A Rationale and Residual risk migrated though not in the mapping | zoning_guidelines |

## Completion

### Final wrap-up

| # | Item | Status |
| --- | --- | --- |
| W1 | Devlog entry for the documentation restructuring. The old commit `0de4f03` was reset out of history, so no entry is owed for it. | open |
| W2 | Review final state of all files | open |
| W3 | Line endings: convert files edited in chat to CRLF | open |
| W4 | After the feature merge, remove the old remote, add FLOORFOX, and push the finished history | open |
| W5 | Delete branch `backup-before-reset` once satisfied | open |
| W6 | Place `funnel_algorithm.md`, `funnel.svg`, and `convex-segments.svg` if still required | partly done — `funnel_algorithm.md` and `funnel.svg` moved from `docs/ignore/research_references/` to tracked `docs/references/`; `docs_guidelines.md` also moved there. `convex-segments.svg` still unplaced. |
| W7 | Promote `validate_plan.py` into `src/` if still required | open |
| W8 | Correct the funnel wording in `research_notes.md` | open |

### Housekeeping

| # | Item | Status |
| --- | --- | --- |
| H1 | `_to_delete/` removed; retired docs deleted in place from now on | done |
| H2 | `.gitattributes` with `* text=auto` at project root | open — own commit; renormalises the whole repo once |
| H3 | Convert `working_notes.md` and `docs/references/docs_guidelines.md` to CRLF | done |
| H4 | Future prompts: ban all git commands, not only write operations | noted |

## Archive

Backups are in `docs/ignore/archive`.
Non-documentation artifacts are in `docs/ignore/archive/other`.
