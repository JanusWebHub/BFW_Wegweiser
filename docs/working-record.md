# Working Record: Decisions And Agreements

Started: 2026-10-03
Last updated: 2026-10-15
Human participant: Deniz
AI assistants: GitHub Copilot, Claude Code

## Purpose

This is a provisional and amendable record of decisions, agreements, qualifications, insights, ideas, and understanding confirmed by the human participant. It provides a persistent reference point within and across sessions with AI assistants. Confirmed agreements, conditional agreements, provisional terms and recommendations are distinguished explicitly. Changes to recorded agreements require the human participant's explicit confirmation.

Currently it is also the most up to date and the most reflective of the intended direction, because it is where thinking is gathered until it is mature enough for the rulebook and system design. This is a transitional and provisional status, not a higher authority than those documents. The project README, system design and rulebook are updated from this record regularly, and the implementation plan is revised in line with them.

## historical reconstruction

This section reconstructs how the project reached its present state. The account is the human participant's, checked against the evidence below. The code was first written as a single script for finding a path on a floor plan image. It was then split into an offline compiler and a static client, documented, and a first conceptual model of the building was drafted. That model was soon reconsidered, and a model overhaul remade the model documents (rulebook, system design, implementation plan, root readme) and rebuilt the shared `main`. The simplification of the project as a whole (worktree, branches, local files, documentation and the abstract design) began from there, with the branch `local/simpler`, which carries this work and will become the cleaned `main` by a method not yet decided. Within it, the implementation plan was restructured from phases into levels and the pipeline views were separated by module and process, with GitHub Copilot. Independently, because a workable zone SVG was needed, Claude Design zoned the whole EG floor and Claude Code in a cloud session reviewed that work; together this became known as the Claude review. Its material was saved to the local file system after the plan and the views, with the intention to continue it locally and turn the redline artifact into a standalone app. That intention was given up during decluttering: the cloud scripts were not worth adapting, the app plan was replaced by a zoning module with a zoning editor, and new concepts changed the model rules. The remains of the Claude review became part of the simplification because the implementation plan could not be overhauled without clearing them away. The rulebook, system design and root readme, finalized for their time, are now outdated against the newer decisions, and this record exists to hold those decisions.

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
- 2026-10-05. At 00:29, "Consolidate system design documentation": seven design files were deleted (build-pipeline, development-lifecycle, operation-flow, system-model, system-overview and two Excalidraw drawings) and `docs/system-design.md` changed. At 01:09, "Archive outdated or superseded docs": ai-agent-responses.md, content.txt, current-state-report.md and plan.md were deleted, together with copilot-report.md, handoff.md and claude-remote-branch-tips-review-recap.md from `docs/data/`. At 23:29, "batch update": among other changes, `claude/review/tidyup-plan.md` was deleted. The file index `docs/file-index-261005T1813.md` and `docs/implementation-replan.md` (the start of the gap analysis, with the decluttering groups and their sequence) exist. In a Claude session the human participant decided not to make the cloud scripts run locally and to focus on the zoning editor, keeping the scripts as inspiration only. Sources: Git, documents, session record.
- 2026-10-07 to 2026-10-08. AGENTS.md and the catch-up skill were added and updated, and a note on the EG prototype was added to this record. At 22:23 on 10-08, "declutter" (75 files): the material under `claude/` was moved into `authoring/legacy/` or deleted, including graph_format.md and zoning_guidelines.md. Source: Git.
- 2026-10-09 to 2026-10-12. This record confirms on 2026-10-09 the artifact chain and the zoning module's two parts, the plan tracer and the zoning editor, in `cad/`. On 10-10 at 00:18, `authoring/` was renamed `cad/`, `sources/README.md` moved into `cad/source material/` and this record changed. On 10-11 at 01:42, file names were lowercased and `cad/readme.md`, the plan tracer and zoning editor readmes and the zoning editor specification were added. The specification changed on 10-11 at 17:15 and on 10-12 at 00:19. Sources: this record, Git.
- 2026-10-13. The remains of the Claude review were removed: `claude/review` and `claude/transcripts`, and then, reviewed one file at a time, everything under `docs/ignore/texts`, so that `claude/` no longer exists. The file index `docs/file-index-261013T0719.md` was created, `docs/implementation-replan.md` marks the decluttering steps done, and the subfolders of `docs/ignore` were dissolved. The removal under `docs/ignore` is not in Git, because that folder is ignored. Sources: Git, file system, human participant.

### interpretation

- The model overhaul came before the simplification. The overhaul rewrote the model documents and, by the restructuring tracker's own statement, left the program code on the old model. `local/simpler` was created on 2026-09-25 at 22:25, the evening after `main` was rebuilt, from the same commit as the branch `model-overhaul`. Basis: Git, documents.
- The simplification effort is the frame of everything else. Basis: the branch was created on 2026-09-25 and named for it, before the earliest draft times (09-26) and the first commit, and the human participant states its scope as the intention all along. The earlier wording of this record, that the work began as a reformulation of the pipeline and brought up the simplification, is superseded.
- Within that frame there were two distinct things: the restructuring of the implementation plan into levels, and the separation of the pipeline views by module and process. The human participant remembers the plan first. "The earlier level plan" in Response 1 supports this, and only that reply does. Git cannot show the order, because all ten files were committed together. The remark that the design folder was untracked suggests the views were drafted on the branch before that commit.
- The Claude Design and Claude Code work was independent of the simplification, and its start is not known. Git shows only when it was saved: from 2026-09-28 22:08 and, for the Claude Code review, 2026-10-01. Nothing here says whether it began before or after the plan and the views. The name Claude review came to cover both stages.
- The intention at saving, to continue the Claude work locally, matches the two tracks set in the Copilot session of 2026-10-03.
- The plan changed during decluttering from 2026-10-04: the scripts were given up, the app plan was discarded, and the zoning module with a zoning editor was designed. The session record of 2026-10-05 already names the zoning editor as the focus, and this record confirms the module's structure on 2026-10-09. The date of the decision itself is not recorded.
- The remains of the Claude review became part of the simplification through decluttering, because the implementation plan could not be overhauled without clearing them away. The commits of 2026-10-04 to 2026-10-08 fit this.
- The decisions made during decluttering, such as the zoning module and the model elements, came after the rulebook, system design and root readme were finalized. Those documents therefore need reconciliation with this record, which was started on 2026-10-03 to hold decisions spread across sessions and assistants.
- The suffixes 261004 and 261005 in the archive file names probably mark the day of archiving, not authorship. The creation time 2026-10-02 20:23 on disk marks a copy, not authorship.
- Not known: when Claude Design began, when the level plan was drafted, and the date the zoning module was decided.

## Project design and direction

The system is organized into independent zoning, routing and navigation modules. This permits different buildings to supply compatible authored inputs without changing the routing module, and route-search algorithms to change without changing their routing-graph input.

The zoning module produces zone SVG, connectivity JSON and navigation SVG. Movement geometry, including designer-authored movement lines, is intended to be part of the connectivity graph. The exact movement-geometry encoding and routing module input requirements remain unspecified. Navigation SVG passes from the zoning module to the navigation module.

The routing module contains a graph compiler, routing computer and tuning editor. The tuning editor, a repurposed version of the zoning editor, takes the connectivity graph and zone SVG and contains the graph compiler and the routing computer. The graph compiler produces a routing graph from the connectivity graph and the routing configuration, which starts empty. The routing computer consumes that graph and produces the precomputed routes dataset. The tuning editor is used to inspect calculated routes on zone SVG, and it updates routing configuration for the next iteration. The connectivity graph persists across tuning iterations. Its geometry, including movement geometry, is editable in the zoning editor and fixed in the tuning editor. Tuning changes only the routing configuration, which holds costs and variant restrictions. The tuning editor saves the routing configuration, the routing graph and the precomputed routes dataset. The optimized and finalized version of the precomputed routes dataset passes from the routing module to the navigation module.

## Authoring Concepts

The following sections on layers and on intent, application and approval record agreed authoring concepts for the zoning editor. Human decision authority applies regardless of software implementation.

### Layers and independent dimensions

| Building Content | Meaning |
| --- | --- |
| Building outline | Boundary between building interior and exterior |
| Circulation layout | Main circulation areas and their boundaries |
| Detailed spaces | Rooms, subdivisions, blocks and similar modeled areas |
| Connection elements | Doors, openings and virtual portals |

Provisional idea: a zone category "mass", particularly for wall masses. Its definition and relationship to navigable and non-navigable zones are not yet settled.

| Working Arrangement | Meaning |
| --- | --- |
| Reference underlay | Plan SVG |
| Approved baseline | Model state at latest checkpoint |
| Working overlay | Current markup and model changes |

Within the working overlay, candidate geometry shows proposed changes and applied edits, including edits already approved during the session. Separately toggleable revision markup shows drawn requests, notes and remarks communicating intent.

Four independent dimensions distinguish the work:

- Content category: building outline, circulation layout, detailed spaces or connection elements.
- Review state: requested, proposed, applied awaiting review, approved; rejected and superseded where applicable.
- Origin: zoning author, AI assistant or script.
- Edit protection: editable or locked, with explicit unlocking. Approval does not automatically lock geometry.

Editing shared boundaries across content layers requires coordination. Each shared boundary is stored once in the zoning file; any further coordination mechanism is not yet decided.

### Intent, application and approval

A request records intent. A proposal describes a candidate implementation. Applying a change alters the working model but does not imply approval.

A drawn request may resemble geometry but remains markup until explicitly applied. A proposal can be previewed without altering the model. The zoning author can draw requested changes for an AI assistant or script to apply, or leave notes asking an AI assistant to propose changes. Notes need not be change requests.

Approved edits remain in the working overlay until the zoning author explicitly establishes a new revision checkpoint and updates the baseline. Not every editing batch creates a checkpoint. The baseline remains inspectable during review; approval does not guarantee absolute correctness.

Checkpoints need not be retained as separate revisions within the zoning editor. Regular Git commits at checkpoints are a best practice for preserving history, not a requirement.

AI assistants and scripts may propose changes or apply authorized changes; only the zoning author grants approval. Passing checks does not constitute approval. Existing geometry is not to be silently replaced, explicit removals are not to be reversed to satisfy connectivity, and approval is not to be inferred.

## Historical EG demo

On 2026-10-07, the EG navigation prototype was added on branch `feature/eg-prototype`. It is to be completely ignored and excluded from any work or consideration as far as this document is concerned.

## Zoning module development

Bring the operations of the redline workflow into the zoning editor incrementally: persist and communicate intent, support applying changes directly, then support checking and regenerating the model and views. The end goal is a self-sufficient zoning editor that generates semantic SVG and graph outputs, usable without AI assistance. Optional assistance may remain, but must not be necessary to remember or execute decisions.

The zoning editor's document is to be a custom-designed JSON zoning file. It stores each shared boundary once and stores portals by position along a boundary. The zoning editor is intended to be able to import other formats (SVG underlay or geometry, connectivity or routing graphs) as sources of information.

### Artifacts and the zoning module's parts

Confirmed 2026-10-09:

- The chain of artifacts is: source material, plan SVG, zone SVG, navigation SVG. It is a supply chain, not a derivation.
- The zoning module's directory is `cad/`. Its two main parts are the plan tracer and the zoning editor.
- The plan SVG is a vectorized equivalent of the architectural plans, drawn by the zoning author in the plan tracer and used in place of the plans as the underlay.
  - **Why:** the sources (the PDF, the emergency-plan photos) are messy and large. None contains all the relevant information, and most contain information that shouldn't be carried over.
  - **How it is made:** the zoning author loads the sources as underlays in the plan tracer and traces them by hand. Automating this is later work.
- The original sources are kept in `cad/source material/`.
- The reference underlay is now the plan SVG. The exact input and loading of the underlay into the zoning editor is to be worked out later.
- Zone SVG is the new name for "Zoned SVG".
- Zone SVG is generated by the zoning editor from the zoning file.
- The zoning file is the zoning editor's own working document, which it saves and loads. It is separate from the zoning editor's inputs and outputs, as a native file format is from the files a program imports and exports.
- The zoning editor is a visual, domain-aware modeling application: a specialized 2D CAD editor for indoor-navigation models, with a floor plan as its main working surface.
- The navigation SVG is an output generated by the zoning editor.
- `graph_format.md` and `zoning_guidelines.md` describe older formats and are to be harvested for ideas, which are to be integrated into the guiding documents for the zoning editor and the plan tracer.

Terms in the zoning module description that still need definition, to be placed in the rulebook or system design once their level is clear:

- Movement geometry: authored movement paths within zones, replacing the straight-segment assumption of the older graph format. Its encoding is not specified.
- Plan SVG: the vectorized equivalent of the architectural plans, used as the underlay. Its exact content is open.
- Zone SVG: the SVG generated from the zoning file. Its content is specified provisionally in `cad/file_format_specification.md`, a work in progress.

Confirmed 2026-10-14 (id notation, drafted in `cad/file_format_specification.md`):

- SVG element ids are the zone and portal ids themselves, without a prefix, because they start with a letter and are valid XML ids as they are.
- The underscore stays as the separator in portal ids.
- A portal id lists its two zone ids sorted, by character code: code point order, which the default sort of Python and JavaScript gives for ASCII. `localeCompare` does not.
- Ids keep mixed case: floor codes and printed room numbers in uppercase as printed, names in lowercase.
- Ids are ASCII only. Umlauts and ß are transliterated (`ae`, `oe`, `ue`, `ss`), as far upstream as possible.
- Field names are snake case (`view_box`, `units_per_meter`).
- Every file carries two timestamps in ISO 8601 UTC with milliseconds: `zoning_file_version`, the version of the zoning file it derives from, set when a version is finalized in the editor, and `saved_at`, when the file itself was saved. They replace the integer `version`.
- The `format` value of any file that has one is its file name without the extension, in kebab case (`connectivity-graph`, `routing-graph`, `routing-config`), without a project prefix.
- The floor holds the frame (`view_box`) and the scale (`units_per_meter`).
- States, segments, routes, costs, variants, movement lines, boundaries, and the navigable and crossable properties are attached to, or derived from, zones and portals. Spaces, separators and the adjacency graph are sidelined.
- The zone id and the portal id originate in the zoning file. The floor id, the level, the frame and the scale originate in the plan tracer, and the zoning file takes them from the plan SVG. Every other file is a view of the zoning file and takes what its module needs.
- Floor ids are `UG2`, `UG1`, `EG`, `OG1`, `OG2`, with levels -2, -1, 0, 1, 2.
- A zone id starts with its floor id and a dot.
- Each floor has its own exterior zone, `<floor id>.exterior`, which is navigable and not crossable. This does not conflict with the rulebook.
- A further portal between the same two zones appends `_2`, `_3`.
- Segments are stored per direction, two per pair of portals in a zone. A segment lists `[entry_portal ; exit_portal]` and its key is `entry_portal | zone | exit_portal`. The state key is `zone_from | portal | zone_to`.
- `provenance` is removed from the files.
- Each file type has a fixed file name, listed in the specification (`zoning.json` for the zoning file).
- The file format specification is notation only: field name, value shape, short note. It contains no prose and no rules.
- A portal has `line` (the start and end of the crossable section of the boundary between its two zones) and `midpoint` (the midpoint of `line`). A vertical portal has `points` instead, one position per joined floor.
- The base variant is named `standard`: the variant with nothing restricted, and a key in `variants`. A variant's value lists the zones it makes non-crossable and the zones it makes non-navigable, only the exceptions.
- The format specification carries one inline example, with invented ids that follow the notation and none of the building's own, in the section of each element whose value nests or is not obvious from the field list: portal, state, segment and variant.

Confirmed 2026-10-15 (file format concepts):

- The concept of base elements is dropped. It was a provisional support for devising the file format specification, and the specification does not use it.
- The contract between two modules, what a passed file guarantees and keeps unchanged in meaning, does not need that concept. It is worked out later.

Confirmed 2026-10-15 (routing):

- The tuning editor takes the connectivity graph and the zone SVG as input. It contains the graph compiler and the route computer, so no separate run of either is needed.
- The first routing config is created inside the tuning editor and is empty: no costs, and `standard` with empty lists. The first routing graph then has distance as its only cost. It exists as data inside the tuning editor, the route computer runs on it directly, and the routes are shown on the zone SVG.
- The zoning author tunes costs and creates variants in the tuning editor and sees the changed routes there. When finished, the editor saves the routing config, the routing graph and the precomputed routes dataset.
- The zoning file stays private to the zoning editor. The connectivity graph is the interface between the zoning module and the routing module.
- The zoning editor generates the connectivity graph, the zone SVG and the navigation SVG only when the zoning author selects a finalized zoning file version and commands it. All three carry that `zoning_file_version`.
- A finalized version is the approved baseline at the latest checkpoint. Finalizing sets the `zoning_file_version`, stamped on the zoning file itself and on the outputs generated from it. Only finalizing sets it, so checkpoints carry no version.
- Loading reads the zoning file into the model in memory. The viewer draws the model as SVG shapes over the plan SVG, and both share the floor's frame and scale. Every layer is toggleable.

Confirmed 2026-10-15 (plan tracer):

- The plan tracer is a drawing application. The zoning author starts it, loads the source material as underlays on an SVG drawing surface, and traces only what the plans show, as lines and text, by drawing on that surface.
- The drawing surface can load several underlays, move, rotate and scale each of them, and toggle each separately, so that the zoning author can fit them into one coherent plan to draw on.
- The drawing surface has a floor id, a level, a reference frame and a scale. They are fundamental values that are passed along the line.
- The zoning author saves the drawing as the plan SVG, one per floor.
- The plan SVG also stores the placement of the underlays (moves, rotations, scales and toggles), so that the work can resume. It holds references to the source files with their transforms, not embedded images, in a group separate from the traced lines and text. The zoning editor draws only the traced lines and text.
- An SVG image element cannot display a PDF, so a PDF source has to be converted to an image before it can be loaded as an underlay.
- The first version is a working module with manual tracing. Automating it is later work.

Confirmed 2026-10-15 (plan tracer first version):

- The plan tracer is a single HTML file in plain JavaScript that runs in a desktop browser: `cad/plan tracer/plan-tracer.html`.
- It loads image files (JPG or PNG) as underlays. A PDF source is converted to an image beforehand.
- The floor id, level, frame and units per meter are typed in on the drawing surface.
- The zoning author saves the plan SVG through a file dialog and can leave the underlay references out of it. Opening a plan SVG reads it back; the underlay images are picked again.
- The plan tracer is no longer limited to lines and text. It also draws polylines, circles and paths, gives every traced element an id, attaches text to an element by its id, and offers a warehouse symbol library and named layers. This replaces "as lines and text" and "traces only what the plans show" in the plan tracer list above, and "The zoning editor draws only the traced lines and text". These parts come last in the build, and the plan SVG format for them is not defined yet.

Provisional (plan SVG written by `plan-tracer.html` so far): the frame as `viewBox`; `data-floor-id`, `data-level` and `data-units-per-meter` on the root element; a group `underlays` with one `image` per underlay (file name as `href`, transform, opacity, and `data-` attributes for position, rotation, scale, flips, lock and crop, a crop as a `clipPath`); a group `trace` with the lines (each with its own stroke color and thickness) and text. The file name offered on saving is `<floor id>-plan.svg`.

Confirmed 2026-10-15 (language): all development modules (plan tracer, zoning editor, tuning editor) use English for identifiers, documentation, interface text and code comments. German is for the navigation client's user-facing text only.

Confirmed 2026-10-15 (plan tracer build): the plan tracer is built in five batches, each built, tested and committed on its own: aids and feedback (batch 1), drawing (batch 2), snaps and guides (batch 3), underlay and view (batch 4), and last the plan SVG format changes (batch 5). Left out: arrow-key nudging, an underlay thumbnail, a phone layout, corner join, mirror, rotate and scale of a selection, base-point move and array, a properties panel, a snap settings list, a keyboard shortcuts list. In batch 2 a dimension is drawn as ordinary lines and a text, with no link to the measured line. In batch 3 the snaps and guides are one switch, "Tracking guides", on by default, with no list of separate snap settings: alignment with the ends, midpoints and start point, extension beyond line ends, perpendicular, parallel to a hovered line, and polar angles of 0, 30, 45, 60 and 90 degrees in every direction. Snaps to ends, midpoints and intersections win over guides, and guides win over the grid; ortho turns tracking off while a line is being drawn.

Tentatively approved 2026-10-15 (zoning editor start):

- On starting, the zoning author either initializes a new zoning file or loads an existing one. Either way the data is held in memory only, and the zoning file comes first, before the plan SVG.
- A new zoning file starts as a skeleton in memory. Nothing is written to disk before the first save, where the zoning author chooses the file location.
- The zoning author then loads the plan SVG as the underlay and the viewer shows it. For a new zoning file the zoning author loads a plan SVG. For an existing one the plan SVG referenced by each floor is loaded.
- For a new zoning file, the zoning editor creates the floor from the plan SVG: its id, level, `svg` path, frame and scale. The drawing surface takes the frame and the scale, and saving is enabled.
- For an existing zoning file, the zoning editor checks the floor's id, level, frame and scale against the plan SVG. They exist in both files, so the check catches a plan SVG that was traced again.

To be worked out later (stated 2026-10-14 while drafting `cad/file_format_specification.md`):

- The exterior zone carries a floor code in its id, so each floor has its own exterior zone. The routing logic has to accommodate this exception.
- The names of the plan SVG files, one per floor, such as `EG-plan.svg`. The plan tracer offers `<floor id>-plan.svg` for now.
- Whether the pipes in state, segment and route notation have spaces around them in files. The specification writes them with spaces as a depiction.
- How the state and segment keys are written in files: as strings with a separator, as structured entries, or as a new composite key. Pipes and spaces in a string key are unsafe in file names, URLs and Markdown tables.
- The characters and separators of ids: the dot between floor code and name and the underscore between zones. Few characters are valid in every technology used. The dot needs `CSS.escape` in selectors and bracket access in JavaScript.
- Keeping the deployed generated files, and the routing config keyed by their ids, in step with a changed zoning file. This belongs to operations. The zoning editor's edit operations change only the zoning file.
- The encodings of movement geometry, movement lines and boundaries.
- The technology of the tuning editor, its graph compiler and its route computer: probably plain JavaScript in a browser, as for the zoning editor. The existing compiler and computer are Python scripts for the old data format. The choice is between a Python runtime inside the page and a JavaScript rewrite.
- Which files carry a portal's `line`.
- Validation of the files, for example that a zone's `floor` field equals the floor id its id starts with. The files are not required to state such rules.
- The structures of the zoning file, the adjacency graph, the precomputed routes dataset and the SVG files in the format specification.
- The naming of corridor zones. Names such as `flur-tr9-1` (and the portal ids built from them, such as `EG.E.62_EG.flur-tr9-1_2`) are long and convoluted. Shorter names such as `flur-1`, `flur1` or `f1` are being considered.
- Whether costs differ per variant. If they do, the cost fields move into the variant, which complicates the nested notation of `variants`. For now the costs are top-level fields common to all variants.
- What the zoning file holds of the working overlay: the approved baseline only, or the baseline plus the overlay's applied edits, proposed edits and revision markup. The plan SVG stays a separate file. The leaning is to hold all four, but saving revision markup at every click is cumbersome.
- How applied edits and proposed edits are serialized: as operations with arguments, or as resulting elements.
- Recovery of the working state: one temp file while the program runs, overwritten on every change, holding the last checkpoint and the edits since. It would live in the browser's own storage. Whether it has the structure of the zoning file is open.
- Snapping drawn elements to lines of the plan SVG. The snap item in the zoning editor specification covers only drawn elements snapping to each other.
- How a PDF source is converted to an image for use as an underlay in the plan tracer. The first version loads image files through a file picker, and the zoning author converts a PDF beforehand.
- Where the plan SVG records the floor id, the level and the scale. The plan tracer provisionally writes them as attributes of the root element.
- The plan SVG format of the polylines, circles, paths, ids, attached text, symbols and layers of the last build batch.
- The contract between two modules: what the file passed from one module to the next guarantees, and how its meaning is kept unchanged.
- What the zoning editor does when the check of a floor against its plan SVG fails or the plan SVG cannot be found, including whether drawing is enabled only after the check succeeds.
