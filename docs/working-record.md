# Working Record: Decisions And Agreements

Started: 2026-10-03
Last updated: 2026-10-05
Human participant: Deniz
AI assistants: GitHub Copilot, Claude Code

## Purpose

This is a provisional and amendable record of decisions, agreements, qualifications, insights, ideas, and understanding confirmed by the human participant. It provides a persistent reference point within and across sessions with AI assistants. It does not replace authoritative project documents.

Confirmed agreements, conditional agreements, provisional terms and recommendations are distinguished explicitly. Changes to recorded agreements require the human participant's explicit confirmation.

## Project design and documentation

Pipeline reformulation and documentation simplification are distinct from the local BFW review and zoning work. They inform one another without either effort being a prerequisite for the other.

### Confirmed direction

Development lifecycle belongs in the implementation plan. The levels direction is suspended. Building the implementation plan from scratch is being considered, with a gap analysis tentatively planned. Decluttering the worktree is prioritized, before any plan can be done properly.

The system is organized into independent Zoning, Routing and Navigation modules. This permits different buildings to supply compatible authored inputs without changing the Routing module, and route-search algorithms to change without changing their routing-graph input.

The zoning module produces Zoned SVG, connectivity JSON and Navigation SVG. Movement geometry, including designer-authored movement lines, is intended to be part of the connectivity graph. The exact movement-geometry encoding and Routing module input requirements remain unspecified. Navigation SVG passes from the Zoning module to the Navigation module.

The Routing module contains a graph compiler, routing computer and tuning editor. Connectivity graph and routing configuration feed the graph compiler, which produces a routing graph. The routing computer consumes that graph and produces the precomputed routes dataset. The dataset and Zoned SVG feed the tuning editor, which uses a repurposed version of the zoning interface to inspect calculated routes on Zoned SVG and updates routing configuration for the next iteration. The optimized and finalized version of the precomputed routes dataset passes from the Routing module to the Navigation module.

## Historical review and existing work

Zoning is the authoring stage of Wegweiser, separate from its navigation client.

The cloud review was directed by the zoning author, with AI assistance in interpreting, applying and checking changes.

The redline artifact originated as a visual communication tool, avoiding the need to express every spatial correction in text. Initially, the zoning author communicates intent through marks; the AI assistant interprets and applies changes, saves model data as JSON, runs checks, regenerates the view, and returns it for further human review.

The review scripts were written by Claude Code during the cloud review, in a session without a browser. They applied the marks to the graph, checked it with shapely, and rendered images with Pillow and cairosvg so that the assistant could inspect the geometry and the zoning author could see results in chat.

Certain ideas and decisions arose during that review that necessitated modifying existing rules and methods, for example blocks outside navigable zones, distinct from obstacles within zones. These are now reflected in the rulebook.

Source photographs, the older whole-building plan, composites, overlays and simplified models have different evidential roles.

For the initial BFW EG model, the 2018 Lageplan supplied outline, geometry and scale; the May 2026 emergency-plan photos supplied room divisions, doors, labels and exits. Discrepancies required the zoning author's judgment.

The middle area was initially modeled from the Lageplan without corresponding emergency-plan photos. Its room numbers and doors included unverified readings or assumptions; this records the evidence gap at that stage, not the current availability of photographs.

The 2026-09-29 handoff recorded approval through step 3.2, but no approval of the parallel wing outputs or step-8 merge. This is the original approval boundary, distinct from subsequent human-led review and approvals.

Proposed observation by Copilot: the existing materials also serve different working purposes. Marks communicate intent; scripts apply and check changes; generated artifacts represent results; accounts and plans written by AI describe or propose work. Their presence does not make every statement in them a confirmed decision.

## Authoring Concepts

The following sections on layers and on intent, application and approval record agreed authoring concepts. They do not establish that corresponding app capabilities exist in the transferred cloud files. Human decision authority applies regardless of software implementation.

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
| Reference underlay | Source PDF or image |
| Approved baseline | Model state at latest checkpoint |
| Working overlay | Current markup and model changes |

Within the working overlay, candidate geometry shows proposed changes and applied edits, including edits already approved during the session. Separately toggleable revision markup shows drawn requests, notes and remarks communicating intent. Approved edits remain in the overlay until a checkpoint updates the baseline.

Four independent dimensions distinguish the work:

- Content category: building outline, circulation layout, detailed spaces or connection elements.
- Review state: requested, proposed, applied awaiting review, approved; rejected and superseded where applicable.
- Origin: zoning author, AI assistant or script.
- Edit protection: editable or locked, with explicit unlocking. Approval does not automatically lock geometry.

Editing shared boundaries across content layers requires coordination; the mechanism is not yet decided.

### Intent, application and approval

A request records intent. A proposal describes a candidate implementation. Applying a change alters the working model but does not imply approval.

A drawn request may resemble geometry but remains markup until explicitly applied. A proposal can be previewed without altering the model. The zoning author can draw requested changes for an AI assistant or script to apply, or leave notes asking an AI assistant to propose changes. Notes need not be change requests.

Approved edits remain in the working overlay until the zoning author explicitly establishes a new revision checkpoint and updates the baseline. Not every editing batch creates a checkpoint. The baseline remains inspectable during review; approval does not guarantee absolute correctness.

Checkpoints need not be retained as separate revisions within the app. Regular Git commits at checkpoints are a best practice for preserving history, not a requirement.

AI assistants and scripts may propose changes or apply authorized changes; only the zoning author grants approval. Passing checks does not constitute approval. Existing geometry is not to be silently replaced, explicit removals are not to be reversed to satisfy connectivity, and approval is not to be inferred.

## Local continuation

The cloud review scripts are not made runnable locally; the zoning editor is the next focus. The corrected graphs, marks and correction log remain in `claude/review`. Remaining review corrections are expected to wait for the editor. `graph_format.md` and `zoning_guidelines.md` remain to be reconciled.

## Historical EG demo

The following work was a one-off demo, not part of or connected to project development on any other branch. Ignore its outputs, implementation choices, and commit history when working on the current project unless explicitly instructed. It establishes no model verification, design approval, or implementation requirement.

On 2026-10-07, the EG navigation prototype was added on Janus branch `feature/eg-prototype` in commit `f66181a`. Its process record, `docs/eg-prototype-process-record.md`, documents its creation, implementation choices, checks, and limitations. The source graph remains `unverified`; its SVG is prototype output, not the finalized Navigation SVG.

The Python build adapts `claude/review/data/routing-graph-fixed.json` and precomputes route pairs into a compact portal-index table. A separate SVG builder uses the underlay and geometry embedded in `claude/tools/eg-redline.html`; the browser combines those assets to reconstruct and display the selected route. The build scripts and tests remain on `feature/eg-prototype`, not `local/simpler`.

## Standalone app development

Standalone zoning app: develop an uncomplicated authoring tool on a separate feature branch, independently of the local review but sharing its concepts and compatible outputs, without requiring reuse of its scripts.

Bring the operations of the historical review workflow into the app incrementally: persist and communicate intent, support applying changes directly, then support checking and regenerating the model and views. The end goal is a self-sufficient semantic SVG authoring app usable without AI assistance. Optional assistance may remain, but must not be necessary to remember or execute decisions.

Recommendation by Copilot: content, review state, origin and edit protection could be implemented through SVG layers, filters or a combination.

Recommendation by Copilot: potential feature for the app; linking each request or proposal to the resulting edits and approval decision, provided this adds little complexity.
