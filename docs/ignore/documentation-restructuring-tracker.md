# Documentation Restructuring Tracker

Local-only working tracker. Not part of the committed project documentation.

## Control

### Restructuring Decisions

- `main` remains based on `4763d6c`.
- The documentation restructuring is intentional and remains uncommitted until reviewed.
- A temporary local branch tracks the tracker and restructuring; the ignored tracker is force-added.
- Checkpoint pattern: documentation commit, tracker update naming it, tracker commit.
- The obsolete commit `0de4f03` must not remain in the final `main` or feature-branch ancestry.
- The local `backup-before-reset` branch may be deleted after verification.
- Final documentation files are committed directly on `main`; the temporary branch is then deleted.
- The JanusWebHub remote will be removed entirely at the end.
- `FLOORFOX/BFW_Wegweiser` becomes the final remote only after the migration and feature work are complete.

### Order

1. Create the temporary local branch and force-add the tracker.
2. Review, checkpoint, and finish the documentation restructuring.
3. Commit the final documentation files on `main`.
4. Delete the temporary branch.
5. Rebase `feature/east-wing-prototype` onto the migrated `main`, removing `0de4f03` from its ancestry.
6. Resolve conflicts and validate the feature.
7. Merge the feature into `main`.
8. Delete `backup-before-reset` after verification.
9. Remove the old remote, add the FLOORFOX remote, and push the finished history.

### Live status

- `1` done — branch created; tracker committed as `6246384`.
- `2` active — documentation checkpointed in `7312b93` and `65c0590`.
- Rulebook checkpoint — renamed to `rulebook.md` in `a2d9648`.
- Rulebook definition refinement — opening, 1.1-1.3, 1.5, and 2.4 revised; the routing-variant rule moved to 3.4 in `f27143c` after tracker update `90a83c1`.
- Archive cleanup done — dated snapshots removed; east-wing worktree retained.

## Rulebook review plan

### Process

1. Create a checkpoint. — done
2. Make reorder-only changes in small independent blocks. — done
3. Validate the reordered rulebook and checkpoint. — done
4. Apply obvious, low-risk content changes. — done
5. Validate and checkpoint again. — done
6. Rework the zone/boundary/wall relationship carefully. — done (`cd83b4e`)
7. Rework the graph definitions and derivation sequence. — open
8. Revisit the pipeline explanation and diagram last. — open

Each block remains separate and increasingly invasive.

### Rulebook Decisions

- Structure: the rulebook progressed from lettered layers to numbered subject sections and then five conceptual clusters; Cluster 5 was absorbed into Cluster 1, leaving four active clusters.
- Cluster 1: keep zone, separator, portal, and segment distinct. Treat boundary and separator together; separators divide spaces architecturally and are represented as zone boundaries after zoning. Virtual boundaries may separate zones without physical separators. Move the two-dimensional premise and exterior into this cluster. Define the simplified plan as derived from the architectural plans, retaining features relevant to navigation. Define portals as crossable boundary portions represented by midpoints; they may correspond to physical or virtual openings, always join exactly two zones, and remain pair-specific where zones meet at a point.
- Cluster 2: order walkable/non-walkable part, obstacle, movement zone, movement line; preserve their distinctions. Clarify obstacles as fixed obstructions in the non-walkable part of a zone; routes neither end at nor pass through them. Define a movement line as a designer-drawn representation of the route people actually take through a movement zone.
- Cluster 3: keep zoning first; replace room/wall graph terminology with space/separator terminology and replace the graph table with sequential adjacency, connectivity, and routing definitions. Place the routing-variant rule after the routing graph definition. Defer pipeline prose and diagram review.
- Cluster 4: keep query, state, search, costs, and result in dependency order, with state preceding search. The query includes manual zone-based self-location. Remove the redundant route-notation section; the result is an alternating sequence of zones and portals.
- Cluster 5: absorb its entries into Cluster 1; do not leave a standalone cluster.

## Open decisions

- `edges` versus `connections`: naming rule has no current home.

## Review status

Status: `done` · `active` · `open` · `blocked`

### Documents

| # | Document | Status | Note |
| --- | --- | --- | --- |
| 1 | `convergences.md` | done | Retired. Title + intro survive in `research_notes.md`. Deleted. |
| 2 | `docs_guidelines.md` | done | Line-endings rule added (CRLF working tree, LF repo, `.gitattributes`, repo-wide). Converted to CRLF. |
| 3 | `research_notes.md` | done | Poincare removed, row 6 reworded, sections merged, project refs stripped, intro rewritten. |
| 4 | `zoning_guidelines.md` | open | Most sources, known duplication. |
| 5 | `working_notes.md` | open | |
| 6 | `roadmap.md` | open | |
| 7 | `README.md` | done | Relative links removed, `.gitattributes` added to tree, inline doc descriptors, Python 3.10+, Milestones deduplicated, verification loop added as Quick Start step 4. |
| 8 | `axioms.md` | done | Retired to `docs/ignore/retired`. Replaced by `rulebook.md`. |
| 9 | `adr.md` | open | |
| 10 | `devlog.md` | done | Byte-identical to backup (13 801 B, same mtime). Untouched, as required. |
| 11 | `glossary.md` | done | Retired. Core/Derived/Movement/Roles -> rulebook D.2, D.4, D.14. Rejected-words table dropped (Q3 resolved). `edges` rule survives as roadmap Phase 2 task. |
| 12 | `design_recap.md` | done | Retired. Sections 1-3, 5 already in `working_notes.md`; 7 in `zoning_guidelines.md`; 6, 8, 9 dropped as covered by `roadmap.md`; 4 dropped with Q3. |
| 13 | `graphic_strategy.md` | done | Retired. §1 decision already ADR 5; viewBox guarantee -> `zoning_guidelines.md`; pipeline diagram dropped (superseded by rulebook R.5). Phase B covered by roadmap P2 + geometry added. Phase C -> `working_notes.md`. §5 split: two items covered by roadmap P2, `data-kind` hook added there, multi-floor group -> `zoning_guidelines.md`, verification loop -> README step 4. |
| 14 | `rulebook.md` | active | Definition refinement checkpointed in `f27143c`; Cluster 3 graph rewrite and pipeline review remain open. |

### Decision record

| # | Item | Decision |
| --- | --- | --- |
| D1 | Q1 — glossary definitions | Resolved — into `rulebook.md`: partition into D.2, portal-need-not-be-a-door and virtual portal into D.4, role table into D.14 |
| D2 | Q2 — graphic_strategy §1 | Resolved — decision stays ADR 5; the shared-`viewBox` consequence went to `zoning_guidelines.md`, not the rulebook, since it follows from a tooling decision not from the model |
| D3 | Q3 — discarded/rejected terms | Resolved — table dropped entirely. Hub dead; branch/leaf superseded by D.16; crossable now a rulebook property (D.7) so rejecting it would be wrong; junction and decision point still live but not worth a doc |
| D4 | ADR 4 rewrite | Text quoted; awaiting rewrite. Last purge hit in a kept doc |
| D5 | Axiom 12 vs multi-source formulation | Resolved — merged in rulebook S.2: outbound/inbound states plus the stopping rule |
| D6 | Two axiom candidates | Resolved — "routing graph is portals and segments only" is D.15; "every segment lies in one zone" is D.5 |
| D7 | GS Phase B — roadmap topology.json lacks zone geometry | Resolved — geometry added to roadmap Phase 2 |
| D8 | GS Phase C — OpenCV pipeline uncovered | Resolved — in `working_notes.md` after the Options table |
| D9 | GS §5 — `data-kind` CSS hook, `<g id="floor:eg">`, verification loop | Resolved — all three applied |

### Flags — substantive

| # | Flag | Where |
| --- | --- | --- |
| F10 | `roadmap.md`, `working_notes.md`, and `zoning_guidelines.md` cite retired `axioms.md`; `zoning_guidelines.md` also reserves zone id `aussen` where the rulebook says "exterior" | roadmap, working_notes, zoning_guidelines |
| F9 | `docs_guidelines.md` has no rule for code naming; `edges` not `connections` has no home outside roadmap Phase 2 | docs_guidelines |
| F1 | Resolved — the axioms 17–18 reading is discarded. A doorless portal from splitting a zone is an ordinary portal | glossary |
| F2 | "Rooms are never crossed" contradicts axioms 8/19 | working_notes recap entry |
| F3 | Contract rule 5 merges two rules ("…its two zones must share a wall") | zoning_guidelines |
| F4 | Resolved — "segment" is the term. `working_notes.md` still says "path" in places | working_notes |
| F5 | Obstacle rule conflict: glossary "booths → obstacle always" vs working_notes "designer's decision, case by case" | glossary, working_notes, zoning_guidelines |
| F6 | `validate_plan.py` not in repo; roadmap path `docs/ignore/files_260911/` does not exist | roadmap |
| F7 | Roadmap P2 says `start_point` is orphaned; code no longer is | roadmap |
| F8 | Recap "This is not places linked by corridors" left without its positive counterpart after the purge | working_notes |

### Flags — editorial

| # | Flag | Where |
| --- | --- | --- |
| E1 | Intro describes only the convergences table; doc now also holds graph theory notes and node/edge paragraph | research_notes |
| E2 | Naming rules appear twice (contract rule 3 + Naming conventions section) | zoning_guidelines |
| E3 | Source hierarchy appears twice (GS Phase A + design_recap §7) | zoning_guidelines |
| E4 | Duplicate portals covered twice (GS §2 paragraph + glossary section) | zoning_guidelines |
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
| W6 | Place `funnel_algorithm.md`, `funnel.svg`, and `convex-segments.svg` if still required | open |
| W7 | Promote `validate_plan.py` into `src/` if still required | open |
| W8 | Correct the funnel wording in `research_notes.md` | open |

### Housekeeping

| # | Item | Status |
| --- | --- | --- |
| H1 | `_to_delete/` removed; retired docs deleted in place from now on | done |
| H2 | `.gitattributes` with `* text=auto` at project root | open — own commit; renormalises the whole repo once |
| H3 | Convert `working_notes.md` and `docs_guidelines.md` to CRLF | done |
| H4 | Future prompts: ban all git commands, not only write operations | noted |

## Archive

Backups are in `docs/ignore/archive`.
Non-documentation artifacts are in `docs/ignore/archive/other`.

## Docs review mentality

- State each fact once, where readers naturally seek it.
- Remove repetition and explanatory scaffolding.
- Derive rather than assert what follows from prior rules.
- Preserve distinctions that change model semantics.
- Treat wording as semantic precision.
- Keep designer choices explicit where topology cannot decide.
- Reject assistant-invented infrastructure.
- Separate model truth from procedure, rationale, uncertainty, and implementation.
- Keep entries only when they earn their existence.
- Cut duplication without erasing necessary distinctions.
- Consolidate only after conceptual dependencies are understood.
- Order items by dependency, establishing what needs the fewest other statements first, then building progressively throughout the document.
- Use top-down or bottom-up progression, from wholes to parts or parts to wholes, as a secondary ordering criterion.
- Express schemas, pipelines, and derivations in prose; use diagrams or explanatory structure only when they carry source-of-truth reasoning.
