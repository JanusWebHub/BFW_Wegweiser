# support notes for conversation

This file exists to keep ai agents Claude and Copilot from losing content and awareness within and across sessions. State says where things are. Settled keeps settled wording from being reopened. History holds the continuity.

## 1. State

- The project is being simplified as a whole on the branch `local/simpler` (repo `C:\projects\wegweiser`). The simplification covers the worktree, branches, local files, documentation and the abstract design.
- Decluttering is the current part of the larger simplification effort. Its focus is on the `cad/legacy/`, currently on the `cad/legacy/specs/`.
- Dealing with the legacy items led to the specification documents. see commit `ecb08b8`.
- The plan tracer is one strand within this, on the branch `feature/plan-tracer`, which is ahead of `local/simpler`.
- The course of actions for the zoning module is kept as a file in `cad/` and as a shared Artifact.

## 2. Settled, do not reopen

- The snap item: "Drawn elements snap to each other within a given distance, to ensure exactly matching coordinates." The second sentence ("stored data has no tolerances") was dropped on purpose.
- "The zoning author can change the model either directly or by drawing a request for an AI assistant or script using markup."
- The check item "...loading, saving or checkpoint..." is as Deniz wrote it.
- "The zoning editor remembers a file the zoning author picked and saves back to the file. Requires a Chromium-based browser." The short fragment after a full sentence is a precedent for a constraint on that sentence, and is used only for that.
- "The zoning author can ask a program or AI assistant to propose a resolution of a violation found by the check or flagged by the zoning author." ("Ask someone to do something" is the construction; "request from" is not.)
- Technology has no "initially". The plan SVG is the only reference underlay, with no gloss and no interim item.
- "Edit" and "change" as defined in the working record. "Outputs" is named in purpose and used in the review workflow.
- The specification says "concepts" (not "meanings") defined in the rulebook.
- The concept of base elements is dropped (Deniz, 15.10.26). It was a provisional support for devising the format specification. The contract between two modules does not need it and is worked out later.
- "Review annotations" and "review state" as terms in the specification are dropped.
- The architecture items on who may read or change the model, keeping the data out of reach, and visible failure on violation are dropped: implied by the editing rule, and an implementation technique, not a requirement. The viewer-reaction item was implied too.
- The "mechanical consequences" item is dropped. Its source was the working record's section "Domain-Aware Editing"; its only real example, a portal following a moving boundary, is an open question.
- "Unresolved interpretations" as a term is dropped. The concept survives as the potential feature "Stated relationships whose geometry is not yet drawn".
- The cleanup paragraph of the old cad readme is dropped: other specification items give it.

## 3. History (append only)

New entries go at the end, dated.

### 09.10.26, earlier session (README work)

- Three one-sentence sections were added to the legacy README. Four items offered by Claude (assisted tracing, rule-based suggestions, multi-floor, the BFW outputs as a reference) were declined.
- The Copilot session that produced the zoning README was rebuilt and read. It began with research only, drifted into poetic prose that Deniz rejected, and then produced the adopted formulation: "a visual, domain-aware modeling application: a specialized 2D CAD editor for indoor-navigation models". A README was drafted with status labels and pruned; Deniz removed the status paragraph, the historical-inspiration section and the open-details section himself.
- First critique round: rejected the pointer to the working record, links to other documents and an "authorized by whom" fix; accepted terms going to the working record, the `legacy/` line (later removed again), the Review section split, and the name and wording fixes. Approved wording: "is intended to become fully usable without AI", "could accommodate ... potentially before their geometry is complete", "is intended to be able to import" other formats. Claude invented a criticism of a fine sentence and conceded wrongly, then rechecked and corrected.
- Working record cleanup: the "Local continuation" section removed; "Standalone app development" became "Zoning module development"; the "Last updated" date fixed; the review paragraphs consolidated into one; the Copilot observation integrated in the past tense into the evidential-roles paragraph; redundancies handled except the decluttering story told three times, which Deniz said to treat separately; some edits applied by Deniz.
- Zoning README: terminology fixes ("zoning editor" replaced module, editor and application) and the sections Parts And Artifacts and Plan Tracer added. Deniz restructured it: a "Zoning Editor" parent heading, "Scope And Independence" removed (the `legacy/` mention is gone intentionally), the AI-independence paragraph moved into Purpose And Nature, the interpretation section dissolved. Decided: older documents are not integrated into the README, and "to be worked out later" status sentences do not belong in it. The README is finished.
- Mistakes Deniz corrected: condensing approved wording, sorting by kind instead of status, wrongly conceding a point, treating something unsaid as missing, stating analyses too definitively, proposing rewrites before asking for guidance, analyzing paragraphs in isolation, raising non-issues, re-flagging the "Zoned SVG" rename, misreading "pending", verbosity. A memory was saved: approved items stay in approved wording, sorted by status, with no labels.

### 10 and 11.10.26, session on `local/simpler`

- Naming: "review" as a noun dropped, fixed phrases decided and applied in the working record and `cad/readme.md`.
- Stack decided (later removed from the specification): plain JavaScript first with no build step and no types, a web page in a browser first, the viewer draws SVG, UI framework deferred, Node with Vite, Vitest and TypeScript an alternative for later.
- Topology decided; corner ids dropped; terms model, edit operations, viewer, project file (since renamed to "zoning file") fixed; "only the zoning author decides, a program may at most propose"; "other formats are imported as an underlay only for now, geometry import is a later decision" (later removed); the cleanup paragraph of the old cad readme dropped.
- Model discussion: the terms of the working record (model element, geometry, defining coordinates, geometry point, shape, component, movement lines, polyline); boundaries and portals (straight boundary, portal midpoint derived, the on-boundary rule, non-straight boundaries open, routing point override as a later option); principles (no silent resolution of a violation, a check is a real reading of stored data, unresolved interpretations removed from the model).
- First specification draft in sections, with six unplaced items. Pronouns and shorthands replaced by explicit terms, items split to one statement each. "Review state" and "review annotations" kept for the time being.

### 11.10.26, later: consolidation and restructure of the specification

- Consolidation by claims and roles, section by section (the check items merged into one, layers, construction, files, purpose). Then a thematic restructure (purpose, model, behavior, architecture, technology, open issues), verified for content loss by a sorted diff before the later deliberate drops.
- Decisions: the model and project file (since renamed to "zoning file") as three items; the model changes only through edit operations; checks run at loading, saving and checkpoint or on demand; the checkpoint defined; the review workflow sorted into stages; decision authority split off; the four dimensions item removed; imports first decided "included", then the whole import line removed; geometry import dropped; the plan SVG the only reference underlay; the interim underlay, the toolchain and UI framework items removed; the navigation SVG coordinate frame line moved to the reconcile list.
- The snap item was overhauled; the intent was found by comparing with the legacy plan (see the working record): tolerance in the drawing aid, not in the data. "Positional relations" was Deniz's own coinage and was abandoned.
- Memory files saved: consolidation method and critical review.
- Mistakes: surface merges, two overstated "tensions", reopening the settled check wording, invented reasons, unchanged text in previews, proposals with too many options.
- A handoff recap ("midterm", 12.10.26) was written before context compaction.

### 12.10.26

- Architecture trimmed after discussion: the viewer-reaction item, who may read or change the model, data kept out of reach, and visible failure on violation were removed (implied or an implementation technique).
- The mechanical consequences item was traced to the working record ("Domain-Aware Editing") and removed. The check items merged into "checks the model against a set of rules". The decision authority wording was rewritten ("ask ... to propose a resolution of a violation found by the check or flagged by the zoning author"), and its items reordered (approval authority before the lock item).
- The Chromium item moved from open issues into the files item as a constraint fragment. Open issues split into "open issues" and "potential features"; "unresolved interpretations" renamed to "stated relationships whose geometry is not yet drawn".
- A full check-up of the specification: "outputs" named in purpose, "edit" and "change" sorted (working record), the layers colon, the technology comma. Section headers reconsidered: no logical consolidation. The specification was declared done for the moment.
- Claude proposed unrequested items (a subsection note, a move of the pan and zoom item) against the saved memory; Deniz corrected it and an apology followed.
- notes.md restructured into the seven sections above; the older recaps were folded in.

### 13.10.26, decluttering and history reconstruction

Earlier in the day:

- The specification stayed as it was (done for the moment). notes.md was restructured into seven sections with an append-only history.
- Decluttered `claude/review`, `claude/transcripts` and `claude/claude design` with Deniz deciding each item: app-plan.md and the cloud scripts were discarded, a few ideas went into the working record, and what is worth keeping from the review sits in `cad/legacy/` (fixed graphs, redline page, the two older spec files, a short readme). Deniz confirmed that what remains in `cad/legacy/` is fine.
- Compared the file indexes. `docs/file-index-261005T1813.md` was the old snapshot, `docs/file-index-261013T0719.md` the new one. Decluttering was narrowed to `docs/ignore/texts/`, then widened to all of it.
- First reconstruction of the project history in the working record, built from Git, file times, documents and Deniz's own account (simplification as the frame, Claude Design and Claude Code work as an independent effort). A memory was saved: read every implicated file before reporting.

This part:

- Claude review group reviewed one file at a time against the kept documents. All discarded. Rule set by Deniz: judge deletion only by the contents, never by Git or backups (memory saved).
- Copilot group: the five views were removed together, then content-261005.txt (checked against src/ and web/), plan-261005.md, current-state-report-261005.md and ai-agent-responses-261005.md one by one. All discarded. Deniz rejected every salvage candidate (the search vocabulary, the analytics separation, the operation behaviors).
- The other files of `docs/ignore/texts/` (the overhaul and pre-overhaul material) were scanned for dates and Git history, then reviewed newest to oldest. All were superseded or outdated and all discarded.
- History reconstruction extended backwards from 2026-09-24 to the first upload on 2026-06-29, from the commit log, the reflog, PR #2 and the files' contents. Deniz's corrections: Janus created the project, Deniz joined on 09-01 and did most of the later work, Cowork is Claude Cowork, PR3 was planned and not needed. The working record now has the earlier phases in `course of events`, an opening in the overview, the 09-24 rebuild of `main`, a rewritten 10-13 entry and "since removed" for the documents.
- The record has no labels such as "false start". Deniz asked to drop labels altogether.
- `docs/implementation-replan.md`: every decluttering item and every step of the sequence is marked done. Deniz dissolved the subfolders of `docs/ignore` (`texts`, `visuals`). The picture files now sit directly in `docs/ignore/`.
- Mistakes Deniz corrected: verbose answers (keep short), a salvage suggestion that left out items from the review (list every item, state clearly), Git cited as a reason to delete, "not in Git" claimed before checking the PR history, fixating on labels.

### 14.10.26, file format specification

- Removed "unresolved interpretations" from the working record.
- Reviewed `cad/legacy/specs/graph_format.md` and `zoning_guidelines.md` against the fixed graphs and the documents. Deniz restored `graph_format.md` to its legacy state. The review produced the base elements and the new file `cad/file_format_specification.md`, written by consolidating the legacy ids and fields into one section per model element, then rewriting it in notation form.
- Renamed "project file" to "zoning file" in the specification, working record, notes and legacy readme.
- Built the format specification: file types table, file structure, model elements, ids and fields. Decided floor codes, zone ids with the floor code in front, `navigable`, segments per direction, `entry_portal` and `exit_portal`, `format` labels, two timestamps in place of `version`.
- Wrote `docs/ignore/stack-rules.md`, naming rules per technology, then corrected it and generalized all sections but the last.
- Recorded the confirmed id and format decisions and the deferred items in the working record.
- Mistakes Deniz corrected: treating excluded prototype files as current, adding unrequested "what this does to the proposal" paragraphs, hypotheticals instead of verified facts, resisting his idea of a shared base before testing it, misattributing editor warnings, and errors in the first stack-rules draft.
- After the compaction: the portal fields were reworked (`point` became `midpoint`, new `line`, `points` replaces both on a vertical portal) and the examples updated.
- `stack-rules.md` was renamed `stack-constraints.md` and made project-agnostic. Its "Applied to our ids" section was removed after checking the specification against it (no violations); three items went into the working record.
- The global `CLAUDE.md` got a "No padding, no performance of rigor" section, and the git section's Why line was reworded.
- The working record got the base elements, the floor ids, the exterior, segments and keys, the portal fields, the corridor naming item and the later items.
- Mistakes Deniz corrected: a wrong explanation of the exterior clause right after the compaction, a padded consistency check, adjusting the length of a rule instead of finding its cause, and wording for `midpoint` that was wrong ("the portal's crossable section", when the portal is that section) or insufficient ("the midpoint of the portal").
- Routing config: the variant design was settled (`standard`, `non_crossable`, `non_navigable`, costs outside the variants), the specification and both full-file examples were updated, and inline examples were added to the portal, state, segment and variant sections. The working record has the same.
- Mistake Deniz corrected: calling the base variant implicit ("the configuration does not need to list it"), which he had not said.

### 15.10.26, routing

- Walked through the real steps: the author finalizes a zoning file version, selects it and commands the zoning editor to generate the connectivity graph, the zone SVG and the navigation SVG. The editor does not generate on its own.
- Deniz saw the missing link: the routing flow was designed before the zoning file. His idea, adopted: the tuning editor internalizes the compiler and the computer, starts with an empty config, and the author tunes in the viewer.
- Mistake Deniz corrected: saying the compiler and the computer would sit inside the tuning editor "without a bridge" under plain JavaScript, when both exist as Python scripts.
- A check of the specification, the working record, `notes.md` and the constraints file found them in step, except the working record's routing module paragraph, which was stale and was rewritten sentence by sentence with Deniz's confirmation.
- Started aligning `cad/zoning editor/specification.md` with the decisions since its last edit.- After the compaction, in order: the finalize reading (the stamp is set only by finalize, on the zoning file and the outputs); the layers and what the working overlay holds (applied edits, proposed edits, revision markup), with every layer toggleable and the viewer drawing the model over the plan SVG; the temp file idea and the overlay question (open); a talk about what the plan SVG is (lines and text, and a possible snap to its lines).
- The course of actions was written as a shared Artifact. Deniz reworked the plan tracer part (steps 1 to 7) and the start of the zoning editor (steps 8 to 11B, tentatively approved); the rule check was added as step 18.
- Deniz dropped the concept of base elements; the working record and these notes were adjusted (the term, the list and the contract sentence removed; the contract between modules deferred).
- `notes.md` was taken out of `.gitignore` and added to Git, and the session's changes were committed and pushed on `local/simpler`. Then the branch `feature/plan-tracer` was created from `local/simpler` and pushed to the remote `januswebhub` with its upstream set.

### 15.10.26, evening: the plan tracer

- Deniz asked for the simplest functional plan tracer, quickly. Claude's first draft was in German; Deniz corrected it: all development modules are English.
- The tool was published as a private Artifact for testing from the phone, and grew with quality-of-life features.
- Deniz dropped the limit to lines and text: the tool also draws polylines, circles and paths, with ids, attached text, symbols and layers, plus AutoCAD-style aids. Desktop browser only.
- The features were built in five stages, each laid out for Deniz's go, tested and committed before the next. The last stage changed the plan SVG format, a provisional choice of Claude's.

### 16.10.26, tests and the purpose of the documents

- The skill `retrace-actions` was written for recaps of our actions.
- A full test of the plan tracer was written in `cad/plan tracer/tests/`, grouped by cross-interaction and not by the order the features were built, and run by `run.mjs`. The checks only a human can do are listed separately. The tests found no defect in the tool.
- Deniz had both documents purged of the build and test narrative, and settled what each is for: the working record holds the intended direction and the decisions about the model, `notes.md` keeps Claude's continuity.

### 17.10.26, sources and specifications

- Task agreed: compare `notes.md` and the working record with the specifications and move what belongs there. Duplicates go to the fitting target, conflicts go to Deniz first, and nothing leaves the sources until a check confirms it is covered.
- Plan tracer: a specification and a features document in its folder, the latter drawn from the tool itself. Deniz approved every deviation of the tool from his approved feature list.
- The plan SVG layout went into the format specification as notation, its rules into the plan tracer specification.
- The format specification holds established information only. Deniz removed the "encoding not yet specified" sections, and open items belong in the working record.
- The zoning editor specification was brought up to the decisions since 14.10.
- The four independent dimensions were dropped. The building content groups stay, no longer labeled a content category; how they are used is open.
- How the plan SVG is used as the reference underlay is left open.
- A routing module specification was started in `src`.
- The course of actions became a file in `cad`, titled "Zoning Module Course Of Actions", next to its Artifact.
- The sources were purged of what the specifications now hold. The working record took the reconcile list, the zoning editor open items, the terms and the decisions with their reasons. `notes.md` is cut to State, Settled and History.
- The gap in History between 15.10 and today was closed by reading the transcript backwards: the sections "15.10.26, evening: the plan tracer" and "16.10.26, tests and the purpose of the documents" were reconstructed and then trimmed of detail found elsewhere.
- The sources-to-specifications pass was committed as one commit.
- After Claude misread State as a stale branch name, Deniz fixed the frame.
- State section was rebuilt on that frame and cut to orientation.
- `notes.md` was renamed `continuity-log.md`.

### 18.10.26, open issues and readmes

- Task: the working record from its Confirmed section on against the specifications. Only settled content moves. Open questions stay in the working record only, so the specifications carry none.
- The open issues and the potential features of the routing, zoning editor and plan tracer specifications went to the working record, verbatim.
- Deniz deleted the course of actions, the two file index files, `agents.md` and the skills, and renamed the specifications and the features document to the `-spec` and `-features` names with hyphens.
- The Open section was regrouped by module or theme instead of by document. The reconcile items stay under document names.
- Deniz decided to remove the readmes in `cad/`, `cad/plan tracer/`, `cad/zoning editor/` and `cad/legacy/`. What was worth keeping went to the plan tracer and zoning editor specifications and the working record. The AI independence paragraph was dropped on purpose and recorded as such.
- The root readme was brought up to date: the language rule, `cad/` in the architecture and the layout, and the module descriptors. Its reconcile items and the Language section left the working record.
- The file formats and ids items of the working record were checked against the specifications. Two were removed and the timestamp item was corrected for the plan SVG.
- The working record got "since removed" on history entries, a new date and no mentions of deleted files.
- The pass over the settled content of the working record was not reached.
- Mistakes Deniz corrected: raising the dropped AI independence paragraph as an open question, twice; saying this log held its wording when it holds a fragment; proposing descriptors with conjugated verbs, and wordings that were too long.
