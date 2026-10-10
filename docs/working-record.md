# Working Record: Decisions And Agreements

Started: 2026-10-03
Last updated: 2026-10-09
Human participant: Deniz
AI assistants: GitHub Copilot, Claude Code

## Purpose

This is a provisional and amendable record of decisions, agreements, qualifications, insights, ideas, and understanding confirmed by the human participant. It provides a persistent reference point within and across sessions with AI assistants. Confirmed agreements, conditional agreements, provisional terms and recommendations are distinguished explicitly. Changes to recorded agreements require the human participant's explicit confirmation.

Currently it is also the most up to date and the most reflective of the intended direction, because it is where thinking is gathered until it is mature enough for the rulebook and system design. This is a transitional and provisional status, not a higher authority than those documents. The project README, system design and rulebook are updated from this record regularly, and the implementation plan is revised in line with them.

## The BFW zoning work, historical collaboration with Claude, and existing work

The work began as a reformulation of the pipeline. Working on it brought up the need to simplify the documentation, and that in turn brought up the revision of the implementation plan. The plan needed a complete overhaul, and a gap analysis for it was tentatively planned. That required identifying what is present in the workspace and what is to become of it. This proved near impossible due to the high amount of noise, largely caused by the mess of files from the BFW EG zoning review and the BFW zoning work, which also confused AI assistants. Decluttering therefore became prioritized.

Current focus and active work have been the sifting through the remains of the BFW EG zoning review for relevant content to preserve, and their need for a more permanent place has helped the zoning module take concrete shape.

Revising the zoning module README is an instance of the larger effort of cleaning up the remains of the BFW EG zoning review. `local/simpler` carries this work and will become the cleaned `main` by a method not yet decided. The zoning module is developed on a separate feature branch based on that cleaned `main`.

The BFW zoning work is on hold until the zoning module is functional, which awaits the part of the decluttering concerning the files and folders of the BFW EG zoning review. The BFW EG zoning review itself is discontinued as an attempt to make it work locally. Its results, namely the generated graphs, will be absorbed by the zoning module once functional.

The redline artifact originated as a visual communication tool, avoiding the need to express every spatial correction in text. The zoning author communicated intent through marks, and the AI assistant interpreted and applied the changes, ran checks, regenerated the view and returned it for further human review. To that end, the BFW EG zoning review scripts were written by Claude Code in a cloud session without a browser, so they depend on that environment's paths, imports, packages and programs and are not suited to run locally as they are.

## Project design and direction

The system is organized into independent zoning, routing and navigation modules. This permits different buildings to supply compatible authored inputs without changing the routing module, and route-search algorithms to change without changing their routing-graph input.

The zoning module produces zone SVG, connectivity JSON and navigation SVG. Movement geometry, including designer-authored movement lines, is intended to be part of the connectivity graph. The exact movement-geometry encoding and routing module input requirements remain unspecified. Navigation SVG passes from the zoning module to the navigation module.

The routing module contains a graph compiler, routing computer and tuning editor. Connectivity graph and routing configuration feed the graph compiler, which produces a routing graph. The routing computer consumes that graph and produces the precomputed routes dataset. The dataset and zone SVG feed the tuning editor, which uses a repurposed version of the zoning editor to inspect calculated routes on zone SVG and updates routing configuration for the next iteration. The optimized and finalized version of the precomputed routes dataset passes from the routing module to the navigation module.

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

Editing shared boundaries across content layers requires coordination. Each shared boundary is stored once in the project file; any further coordination mechanism is not yet decided.

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

The zoning editor's document is to be a custom-designed JSON project file. It stores each shared boundary once, stores portals by position along a boundary, and keeps unresolved interpretations as records. The zoning editor is intended to be able to import other formats (SVG underlay or geometry, connectivity or routing graphs) as sources of information.

### Artifacts and the zoning module's parts

Confirmed 2026-10-09:

- The chain of artifacts is: source material, plan SVG, zone SVG, navigation SVG. It is a supply chain, not a derivation.
- The zoning module's directory is `cad/`. Its two main parts are the plan tracer and the zoning editor.
- The plan SVG is a vectorized equivalent of the architectural plans, generated by the plan tracer and used in place of the plans as the underlay.
  - **Why:** the sources (the PDF, the emergency-plan photos) are messy and large. None contains all the relevant information, and most contain information that shouldn't be carried over.
  - **How it is made:** the sources need combining and cleaning, and how this works is to be worked out later.
- The original sources are kept in `cad/source material/`.
- The reference underlay is now the plan SVG. The exact input and loading of the underlay into the zoning editor is to be worked out later.
- Zone SVG is the new name for "Zoned SVG".
- Zone SVG is generated by the zoning editor from the project file.
- The project file is the zoning editor's own working document, which it saves and loads. It is separate from the zoning editor's inputs and outputs, as a native file format is from the files a program imports and exports.
- The zoning editor is a visual, domain-aware modeling application: a specialized 2D CAD editor for indoor-navigation models, with a floor plan as its main working surface.
- The navigation SVG is an output generated by the zoning editor.
- `graph_format.md` and `zoning_guidelines.md` describe older formats and are to be harvested for ideas, which are to be integrated into the guiding documents for the zoning editor and the plan tracer.

Terms in the zoning module description that still need definition, to be placed in the rulebook or system design once their level is clear:

- Movement geometry: authored movement paths within zones, replacing the straight-segment assumption of the older graph format. Its encoding is not specified.
- Unresolved interpretation: a stated relationship, such as "these are separate spaces", whose geometry is not yet drawn. Its representation is not decided.
- Plan SVG: the vectorized equivalent of the architectural plans, used as the underlay. Its exact content is open.
- Zone SVG: the SVG generated from the project file. Its exact content is open.
