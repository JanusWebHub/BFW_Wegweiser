# Working Record: Decisions And Agreements

Started: 2026-10-03
Last updated: 2026-10-20
Human participant: Deniz
AI assistants: GitHub Copilot, Claude Code

## Purpose

This is a provisional and amendable record of decisions, agreements, qualifications, insights, ideas, and understanding confirmed by the human participant. It provides a persistent reference point within and across sessions with AI assistants. Confirmed agreements, conditional agreements, provisional terms and recommendations are distinguished explicitly. Changes to recorded agreements require the human participant's explicit confirmation.

Currently it is also the most up to date and the most reflective of the intended direction, because it is where thinking is gathered until it is mature enough for the rulebook and system design. This is a transitional and provisional status, not a higher authority than those documents. The project README, system design and rulebook are updated from this record regularly, and the implementation plan is revised in line with them.

## historical reconstruction

This section reconstructs how the project reached its present state. The account is the human participant's, checked against the evidence below. The code was first written as a single script for finding a path on a floor plan image. It was then split into an offline compiler and a static client, documented, and a first conceptual model of the building was drafted. That model was soon reconsidered, and a model overhaul remade the model documents (rulebook, system design, implementation plan, root readme) and rebuilt the shared `main`. The simplification of the project as a whole (worktree, branches, local files, documentation and the abstract design) began from there, with the branch `local/simpler`, which carries this work and will become the cleaned `main` by a method not yet decided. Within it, the implementation plan was restructured from phases into levels and the pipeline views were separated by module and process, with GitHub Copilot. Independently, because a workable zone SVG was needed, Claude Design zoned the whole EG floor and Claude Code in a cloud session reviewed that work; together this became known as the Claude review. Its material was saved to the local file system after the plan and the views, with the intention to continue it locally and turn the redline artifact into a standalone app. That intention was given up during decluttering: the cloud scripts were not worth adapting, the app plan was replaced by a zoning module with a zoning editor, and new concepts changed the model rules. The remains of the Claude review became part of the simplification because the implementation plan could not be overhauled without clearing them away. The rulebook and system design, finalized for their time, are now outdated against the newer decisions, and this record exists to hold those decisions.

### course of events

Each entry names its source: Git (commits and branch reflog), file system (times on disk), documents (contents of the archived files, since removed), session records (Copilot and Claude sessions, since removed from the repository), this record, or the human participant's account (given on 2026-10-13 and not recorded elsewhere). Times are local time (UTC+2).

- 2026-06-29 to 2026-06-30. Janus, the person who created the project, uploaded its first files (first commit 0f2eaeb, "Add files via upload"): a single Python script that finds a path on a floor plan image. Sources: Git, documents (the development log, since removed).
- 2026-09-01 to 2026-09-08. The human participant came in as the second contributor, working in a fork. The script was cleaned up (English identifiers, error handling, tests), a development log was started, and Janus's uncommitted local changes were integrated by hand. Most of the work from here on was done by the human participant, with occasional additions by Janus. Sources: Git, documents, human participant.
- 2026-09-08 to 2026-09-11. The program was split into an offline compiler (`src/`) and a static browser client (`web/`), and Janus merged the fork into the shared repository on 09-09 (pull request 1, merge commit a0a6855). Architectural decision records, a roadmap and notes on routing algorithms were written. The last commit of this stage, 4763d6c on 09-11, added a roadmap checklist and a trunk-based workflow. Sources: Git, file system, documents.
- 2026-09-11 12:21. One commit, 0de4f03 "Document semantic floor plans and portal graph architecture", documented a new conceptual model: axioms, a glossary, decision records, a design recap and a rewritten roadmap, built on portals as nodes (the "dual graph"). It reached the shared repository that evening and was soon reconsidered. Sources: Git, documents.
- 2026-09-15 to 2026-09-18. The model overhaul. Ideas were recorded on 09-15 in working notes, with a list of the framings now known to be wrong. Around 09-16, Claude Cowork (a Claude feature) migrated the model documents: the axioms and glossary were retired and replaced by a rulebook with lettered entries. The migration was left uncommitted. On 09-16 the local main was reset to the commit before it, and by 09-18 the shared main followed. A numbered rulebook ("sorted") followed on 09-17 and 09-18, and the east-wing routing prototype, committed on 09-17 as a39e341, cites it. On 09-18 the migration was reviewed in passes with a tracker, and a list of unfinished business was kept. Sources: Git, file system, documents, human participant.
- 2026-09-18 evening to 2026-09-23. The restructure was done on a branch. The numbered rulebook became `docs/rulebook.md` and was refined, the system design was restructured and the implementation plan was restructured into phases, the readme was rewritten, and the working notes and reference documents were deleted. A restructuring tracker recorded each step. On 09-23 at 23:00 the branch was merged into the shared main as pull request 2, squashed into one commit (f3dd43f, later tagged `archive/pr-2-squash`). Sources: Git, documents.
- 2026-09-23 to 2026-09-24. Janus added a branch with SQL database support and interface changes, which was rebased onto the new main on 09-24. A third pull request (PR3) was planned for merging the east-wing prototype and previewed on trial branches, but it was not needed and did not happen. Sources: Git, human participant.
- 2026-09-24, evening. The shared main was rebuilt: the east-wing prototype was merged at its branch point, the squashed restructure was replayed on top of it, and the restructuring tracker was untracked. The last of these commits, 2623bd7, "Stop tracking restructuring tracker", was created at 22:30 (author date 09:45) and is the base of `local/simpler`. Sources: Git, reflog.
- 2026-09-25 22:25. The branch `local/simpler` is created from 2623bd7. Source: Git reflog.
- Undated, from the start. The branch was created as the frame for simplifying the project as a whole: the worktree, the branches, the local files, the documentation and the abstract conceptualization of the program and its implementation. This was the intention all along and was never recorded in any conversation. Source: human participant.
- Undated, independent of the branch. A workable zone SVG (then called zoned SVG or simplified floor plan SVG) was needed. Claude Design zoned the whole EG floor in stop-gated steps from the Lageplan and the escape-plan photos, and Claude Code in a cloud session then reviewed that work. The start of this work is not known, and no record of the cloud session is in the repository. Sources: human participant; handoff.md for the Claude Design stage as of 2026-09-29.
- Undated. The redline artifact originated as a visual communication tool, avoiding the need to express every spatial correction in text. The zoning author communicated intent through marks, and the AI assistant interpreted and applied the changes, ran checks, regenerated the view and returned it for further human review. To that end, the BFW EG zoning review scripts were written by Claude Code in a cloud session without a browser, so they depend on that environment's paths, imports, packages and programs and are not suited to run locally as they are. Source: this record (earlier wording).
- 2026-09-26. Last-modified times of the earliest drafts: content.txt 07:44, ai-agent-responses.md 10:42, pipeline-overview.excalidraw 11:29. content.txt links the plan as `../memories/session/plan.md`. In ai-agent-responses.md, Response 1 refers to "the earlier level plan", Response 3 calls the draft overview `pipelines.md` and proposes `system-overview.md`, rejecting `big-picture.md`, and Response 4 says the design folder is untracked on `local/simpler` and that five drafts were populated. Sources: file system, documents.
- 2026-09-28 05:58 to 06:14. development-lifecycle.md was last modified at 05:58 and current-state-report.md at 06:13. The first commit on the branch, "Restructure pipeline visualizations" (05:59, amended at 06:14), added ten files under `docs/design/`: ai-agent-responses.md, build-pipeline.md, content.txt, current-state-report.md, development-lifecycle.md, operation-flow.md, pipeline-overview.excalidraw, plan.md, system-model.md and system-overview.md. None of the ten was ever renamed in Git. The state report is a snapshot checked on 2026-09-28. Sources: file system, Git, documents. The human participant remembers that the multi-level plan came first and the separate pipeline views after it, born through it or thought of separately.
- 2026-09-28 22:08 to 2026-09-29 21:16. Five commits titled "design data" or "update design data" added the Claude Design material: graph_format.md, zoning_guidelines.md and the design prompt (09-28 22:08); the parallel messages for wings 3 to 7 (09-29 06:18); copilot-report.md and step packages (09-29 11:22); the step 8 and merge outputs (09-29 18:42); claude-remote-branch-tips-review-recap.md, handoff.md and the Claude Design responses (09-29 21:16). handoff.md gives the state of 2026-09-29, cites the Copilot review report as a source of its numbers, and records approval for steps 1 to 3.2 only. copilot-report.md is a Copilot review of the wing 3 to 7 outputs. Last-modified times: copilot-report.md 09-29 18:18, claude-remote-branch-tips-review-recap.md 18:34, handoff.md 19:54. Sources: Git, documents, file system.
- From 2026-09-28 22:08 on, undated. When the Claude material was first saved to the file system, the intention was to continue the work of Claude Design, incorporating what Claude Code had done in reviewing it, to turn the redline artifact into a standalone app (similar to the zoning editor now), and to continue the review locally with the cloud scripts adjusted to the local file system. Source: human participant.
- 2026-10-01 19:58 to 2026-10-02 10:40. "Add claude/ tools and review snapshot" added `claude/review/`, including TIDYUP-PLAN.md, review-report.md, the fixed graphs and the scripts. "Update EG review data and tools" followed at 23:17. "Update EG review" added app-plan.md and sugg.json and renamed TIDYUP-PLAN.md, CORRECTIONS.md and RECAP.md to lowercase. tidyup-plan.md was last modified on 10-01 at 23:12. Sources: Git, file system.
- 2026-10-02 20:23:01. The creation time shown on disk for all the archived copies. Source: file system.
- 2026-10-03. `docs/design/working-record.md` was added at 10:36 and overhauled at 20:43. In a Copilot session, Copilot analyzed the review package. The human participant stated that the review had been done with Claude Code in its cloud working directory and that the standalone app would be developed on a separate feature branch. Two tracks resulted: continuing the review locally, and developing a standalone zoning app. The human participant remembers that the working record was started because ideas and decisions became too many to remember across conversations, sessions and assistants. Sources: Git, session record, human participant.
- 2026-10-04. At 06:44 the design prompt and the parallel messages moved from `docs/design/` to `claude/claude design/`. At 09:03, "Begin documentation simplification with cleanup": the three scripts in `docs/utilities` moved to `claude/tools/legacy/`, `docs/devlog.md` was deleted and the working record moved to `docs/working-record.md`. At 10:26, "Add authoring module". In a Copilot session the human participant stated the intent to distinguish the effort of reformulating the pipeline and rethinking the documents from the Claude review and zoning work, and that this is why the branch is called `local/simpler`. Sources: Git, session record.
- From 2026-10-04, during decluttering, undated. Adapting the cloud scripts to the local file system proved difficult, so they were given up. The app plan was then discarded, because the standalone app had no home and would not work as planned, and a dedicated zoning module with a zoning editor was designed instead. New concepts from the EG zoning and the review changed the model rules themselves, among them the zoning module and the model elements. The implementation plan could not be overhauled without first clearing the mess. By then the rulebook and system design were finalized for that time and many old documents were archived or removed. Source: human participant.
- 2026-10-05. At 00:29, "Consolidate system design documentation": seven design files were deleted (build-pipeline, development-lifecycle, operation-flow, system-model, system-overview and two Excalidraw drawings) and `docs/system-design.md` changed. At 01:09, "Archive outdated or superseded docs": ai-agent-responses.md, content.txt, current-state-report.md and plan.md were deleted, together with copilot-report.md, handoff.md and claude-remote-branch-tips-review-recap.md from `docs/data/`. At 23:29, "batch update": among other changes, `claude/review/tidyup-plan.md` was deleted. The file index `docs/file-index-261005T1813.md` (since removed) and `docs/implementation-replan.md` (the start of the gap analysis, with the decluttering groups and their sequence) exist. In a Claude session the human participant decided not to make the cloud scripts run locally and to focus on the zoning editor, keeping the scripts as inspiration only. Sources: Git, documents, session record.
- 2026-10-07 to 2026-10-08. AGENTS.md and the catch-up skill (both since removed) were added and updated, and a note on the EG prototype was added to this record. At 22:23 on 10-08, "declutter" (75 files): the material under `claude/` was moved into `authoring/legacy/` or deleted, including graph_format.md and zoning_guidelines.md from docs/data/. Source: Git.
- 2026-10-09 to 2026-10-12. This record confirms on 2026-10-09 the artifact chain and the zoning module's two parts, the plan tracer and the zoning editor, in `cad/`. On 10-10 at 00:18, `authoring/` was renamed `cad/`, `sources/README.md` moved into `cad/source material/` and this record changed. On 10-11 at 01:42, file names were lowercased and `cad/readme.md`, the plan tracer and zoning editor readmes (all three since removed) and the zoning editor specification were added. The specification changed on 10-11 at 17:15 and on 10-12 at 00:19. Sources: this record, Git.
- 2026-10-13. The remains of the Claude review were removed: `claude/review` and `claude/transcripts`, and then, reviewed one file at a time, everything under `docs/ignore/texts`, so that `claude/` no longer exists. The file index `docs/file-index-261013T0719.md` (since removed) was created, `docs/implementation-replan.md` marks the decluttering steps done, and the subfolders of `docs/ignore` were dissolved. The removal under `docs/ignore` is not in Git, because that folder is ignored. Sources: Git, file system, human participant.

### interpretation

- The model overhaul came before the simplification. The overhaul rewrote the model documents and, by the restructuring tracker's own statement, left the program code on the old model. `local/simpler` was created on 2026-09-25 at 22:25, the evening after `main` was rebuilt, from the same commit as the branch `model-overhaul`. Basis: Git, documents.
- The simplification effort is the frame of everything else. Basis: the branch was created on 2026-09-25 and named for it, before the earliest draft times (09-26) and the first commit, and the human participant states its scope as the intention all along. The earlier wording of this record, that the work began as a reformulation of the pipeline and brought up the simplification, is superseded.
- Within that frame there were two distinct things: the restructuring of the implementation plan into levels, and the separation of the pipeline views by module and process. The human participant remembers the plan first. "The earlier level plan" in Response 1 supports this, and only that reply does. Git cannot show the order, because all ten files were committed together. The remark that the design folder was untracked suggests the views were drafted on the branch before that commit.
- The Claude Design and Claude Code work was independent of the simplification, and its start is not known. Git shows only when it was saved: from 2026-09-28 22:08 and, for the Claude Code review, 2026-10-01. Nothing here says whether it began before or after the plan and the views. The name Claude review came to cover both stages.
- The intention at saving, to continue the Claude work locally, matches the two tracks set in the Copilot session of 2026-10-03.
- The plan changed during decluttering from 2026-10-04: the scripts were given up, the app plan was discarded, and the zoning module with a zoning editor was designed. The session record of 2026-10-05 already names the zoning editor as the focus, and this record confirms the module's structure on 2026-10-09. The date of the decision itself is not recorded.
- The remains of the Claude review became part of the simplification through decluttering, because the implementation plan could not be overhauled without clearing them away. The commits of 2026-10-04 to 2026-10-08 fit this.
- The decisions made during decluttering, such as the zoning module and the model elements, came after the rulebook and system design were finalized. Those documents therefore need reconciliation with this record, which was started on 2026-10-03 to hold decisions spread across sessions and assistants.
- The suffixes 261004 and 261005 in the archive file names probably mark the day of archiving, not authorship. The creation time 2026-10-02 20:23 on disk marks a copy, not authorship.
- Not known: when Claude Design began, when the level plan was drafted, and the date the zoning module was decided.

## Project design and direction

The system is organized into independent zoning, routing and navigation modules. This permits different buildings to supply compatible authored inputs without changing the routing module, and route-search algorithms to change without changing their routing-graph input.

## Historical EG demo

On 2026-10-07, the EG navigation prototype was added on branch `feature/eg-prototype`. It is to be completely ignored and excluded from any work or consideration as far as this document is concerned.

## Confirmed Items

### Naming of "review"

- The word "review" is not used as a noun naming one specific thing. Fixed phrases, always in full: "the BFW zoning work" (the job), "the BFW EG zoning review" (the collaboration with Claude on that job), "the remains of the BFW EG zoning review" (its files and folders), "the redline workflow" (marks, interpretation, applying, checks, regeneration). Applied in this record.

### Dropped on purpose

Confirmed 2026-10-15 (file format concepts).

- The four independent dimensions (content category, review state, origin, edit protection), a leftover from the redline workflow.
- "A program may at most propose a match" and "no match is made silently".
- The whole geometry import topic including the BFW graphs absorption, the import capability item in purpose, imported raster or vector images as interim underlay, and the toolchain and UI framework items (Node with Vite, Vitest, TypeScript).
- The statement that the zoning editor is intended to become fully usable without AI assistance, and that agents must not be necessary to remember or execute the author's decisions.
- "Movement geometry" was the older umbrella for movement lines and movement zones.
- `provenance` in the files.
- The integer `version`, because a constant integer gave no traceability.
- Opaque ids, rejected by Deniz. Ids stay readable.

## Open Items

### File formats

To be worked out later (stated 2026-10-14 while drafting `docs/file-format-specification.md`).

- The encodings of movement lines and boundaries.
- Which files carry a portal's `line`.
- Validation of the files, for example that a zone's `floor` field equals the floor id its id starts with. The files are not required to state such rules.
- The characters and separators of ids: the dot between floor code and name and the underscore between zones. Few characters are valid in every technology used. The dot needs `CSS.escape` in selectors and bracket access in JavaScript.
- The naming of corridor zones. Names such as `flur-tr9-1` (and the portal ids built from them, such as `EG.E.62_EG.flur-tr9-1_2`) are long and convoluted. Shorter names such as `flur-1`, `flur1` or `f1` are being considered.
- How the state and segment keys are written in files is to be worked out: as strings with a separator, as structured entries, or as a new composite key, and whether the pipes have spaces around them. Pipes and spaces in a string key are unsafe in file names, URLs and Markdown tables. The file format specification writes the pipes with spaces as a depiction.
- The notation of a variant's value is to be worked out.
- Where the plan SVG records the floor id, the level and the scale is to be worked out. The plan tracer provisionally writes them as attributes of the root element.
- Whether the plan SVG layout that the plan tracer provisionally writes stands, including the id scheme and the layer groups, is to be worked out.

### Zoning editor

- How the building content groups (building outline, circulation layout, detailed spaces, connection elements) are used within the zoning editor, as part of its functionality and features.
- A zone category "mass", particularly for wall masses. Its definition and relationship to navigable and non-navigable zones are not yet settled.
- How a connection between two boundary ends is recorded, and how it is checked and enforced are to be worked out.
- How the start and the end coordinates of a portal are related to the positions on its boundary is to be worked out.
- How a portal follows a boundary that moves, and how the rule that a portal sits on the portal's boundary is enforced are to be worked out.
- Boundaries that are not straight would need more than two coordinates, potentially as an SVG polyline or path. How a portal sits on them must be worked out as well.
- What the zoning file holds of the working overlay is to be worked out: the approved baseline only, or the baseline plus the applied edits, proposed edits and revision markup.
- How applied edits and proposed edits are serialized is to be worked out: as operations with arguments, or as resulting elements.
- The recovery of the working state is to be worked out: one temp file, overwritten on every change, holding the last checkpoint and the edits since, kept in the browser's own storage, and whether it has the structure of the zoning file.
- How the plan SVG is used as the reference underlay is to be worked out, including whether and how the underlays of the source material are loaded.
- What the zoning editor does when the check of a floor against its plan SVG fails or the plan SVG cannot be found is to be worked out, including whether drawing is enabled only after the check succeeds.
- Snapping drawn elements to lines of the plan SVG is to be worked out.
- The zoning editor could later run outside a web browser, both headless, such as with Node, and in a window of its own.
- A routing point other than the midpoint can be added later as an optional stored crossing point that overrides the midpoint.
- Stated relationships whose geometry is not yet drawn, such as "these are separate spaces".

### Plan tracer

- The phone related parts of the plan tracer code, such as the layout for narrow windows, are to be removed, because the plan tracer is only for desktop browsers.
- How a PDF source is converted to an image is to be worked out.
- Whether snapping and tracking also use the points of polylines, circles, paths and symbols is to be worked out. They use straight lines only now.

### Routing module

- The technology of the tuning editor, its graph compiler and its route computer is to be worked out: probably plain JavaScript in a browser, as for the zoning editor. The existing compiler and computer (`src/build_database.py`, `src/calculate_routes.py`) are Python scripts for the old data format. The choice is between a Python runtime inside the page and a JavaScript rewrite.
- Whether costs differ per variant is to be worked out. If they do, the cost fields move into the variant, which complicates the nested notation of `variants`. For now the costs are top-level fields common to all variants.

### Between modules

- The contract between two modules: what the file passed from one module to the next guarantees, and how its meaning is kept unchanged.
- Keeping the deployed generated files, and the routing config keyed by their ids, in step with a changed zoning file. This belongs to operations. The zoning editor's edit operations change only the zoning file.
- The exterior zone carries a floor code in its id, so each floor has its own exterior zone. The routing logic has to accommodate this exception.

### Legacy files

- `graph_format.md` and `zoning_guidelines.md` describe older formats and are to be harvested for ideas, which are to be integrated into the specifications.

## Reconciliation

The rulebook, system design, and implementation plan were reconciled on 2026-10-20 against the module specifications and file-format specification. The rulebook defines the agreed model terms; the system design describes the current module architecture and data flows; and the implementation plan sequences development of those modules.
