# Working Record: Decisions And Agreements

Started: 2026-10-03
Last updated: 2026-10-04
Human participant: Deniz
AI assistant: GitHub Copilot

## Purpose

This is a provisional and amendable record of decisions, agreements, qualifications, insights, ideas, and understanding confirmed by the human participant. It provides a persistent reference point within and across sessions with AI assistants. It does not replace authoritative project documents.

Confirmed agreements, conditional agreements, provisional terms and recommendations are distinguished explicitly. Changes to recorded agreements require the human participant's explicit confirmation.

## Project design and documentation

Pipeline reformulation and documentation simplification are distinct from the local BFW review and zoning work. They inform one another without either effort being a prerequisite for the other.

### Confirmed direction

The active core documents are the rulebook, system design, implementation plan and working record. README is the entry point.

System design describes intended architecture, not implementation status. Diagrams explain responsibilities, flows and handoffs; prose records substantive decisions and qualifications rather than paraphrasing diagrams.

Development lifecycle belongs in the implementation plan. Implementation levels describe increasing capability, whereas lifecycle activities recur during development and maintenance. Their detailed organization will be reconsidered separately.

The system is organized into independent authoring, compiler and browser-client modules. This permits different buildings to supply compatible authored inputs without changing the compiler, and route-search algorithms to change without changing their routing-graph input.

Authoring produces Zoned SVG, connectivity JSON and Navigation SVG. Movement geometry, including designer-authored movement lines, is intended to be part of the connectivity graph.

Navigation SVG passes from authoring to the browser client. The precomputed browser dataset passes from the compiler to the browser client.

The routing/tuning editor edits routing configuration to tune calculated route outcomes. Movement geometry is editable in the zoning editor but fixed and inspectable in the routing/tuning editor. This restriction is scoped to the editor, not permanent immutability or automatic locking through approval.

The system overview is to show the three modules and their handoffs, accompanied by a detailed pipeline diagram for each. Module boundaries do not decide programming languages, directory placement or interfaces.

### Provisional design direction

Deniz proposed placing iterative configuration editing and tuning within the compiler module. Zoned SVG would provide the visual basis for inspecting calculated routes; connectivity JSON would supply authored movement geometry for computation.

The connectivity graph would persist across tuning iterations, while routing graphs and routes would be derived under the selected configuration.

A repurposed redline interface is a candidate for the tuning editor, not a selected implementation.

### Still unresolved or not approved

Copilot recommends keeping variant-specific restrictions in routing configuration, separate from the connectivity graph's base properties. Deniz explicitly raised their placement as a question; this recommendation has not been confirmed.

The exact movement-geometry encoding and compiler input requirements remain unspecified. If connectivity JSON carries all required geometry, numerical route computation need not parse Zoned SVG; this is a conditional observation, not a finalized interface decision.

The conceptual-model diagram was rejected as unhelpful and confusing. Its replacement remains for later discussion with Deniz.

### Rejected or superseded approaches

Consolidating the design views by shortening their prose or replacing existing pipeline lists was rejected. Their visual purpose and the document's structure must guide integration.

Copilot's recommendation to place routing configuration editing in authoring was challenged by Deniz's compiler-side tuning proposal; it is not an adopted responsibility.

## Historical review and existing work

Zoning is the authoring stage of Wegweiser, separate from its navigation client.

The cloud review was directed by the zoning author, with AI assistance in interpreting, applying and checking changes.

The redline artifact originated as a visual communication tool, avoiding the need to express every spatial correction in text. Initially, the zoning author communicates intent through marks; the AI assistant interprets and applies changes, saves model data as JSON, runs checks, regenerates the view, and returns it for further human review.

Certain ideas and decisions arose during that review that would necessitate modifying existing rules and methods, for example blocks outside navigable zones, distinct from obstacles within zones.

Source photographs, the older whole-building plan, composites, overlays and simplified models have different evidential roles.

Proposed observation by Copilot: the existing materials also serve different working purposes. Marks communicate intent; scripts apply and check changes; generated artifacts represent results; accounts and plans written by AI describe or propose work. Their presence does not make every statement in them a confirmed decision.

## Authoring Concepts

The following sections on representations, layers, and intent, application and approval record agreed authoring concepts. They do not establish that corresponding app capabilities exist in the transferred cloud files. Human decision authority applies regardless of software implementation.

### Representations and generated outputs

One editable project supports distinct representations, not three independently edited SVG files:

- Zoning working view: the model plus review layers, used during authoring and review.
- Zoned SVG (provisional name): clean semantic floor plan paired with connectivity JSON, without review annotations. Both are generated from an explicitly selected approved baseline revision, excluding the reference underlay and pending review overlays.
- Navigation SVG: a separate map for displaying routes to the navi-user, generated by the authoring module.

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

The latest cloud review state is to be brought into the local workspace so the BFW review can continue without waiting for the app. A reference snapshot would help keep the recovered existing work distinct from future changes.

Confirmed decisions need to be reflected in the rulebook and system design. Changes and plans recommended by AI still require the human author's review and approval.

## Standalone app development

Standalone zoning app: develop an uncomplicated authoring tool on a separate feature branch, independently of the local review but sharing its concepts and compatible outputs, without requiring reuse of its scripts.

Bring the operations of the historical review workflow into the app incrementally: persist and communicate intent, support applying changes directly, then support checking and regenerating the model and views. The end goal is a self-sufficient semantic SVG authoring app usable without AI assistance. Optional assistance may remain, but must not be necessary to remember or execute decisions.

Recommendation by Copilot: establish the app branch after rule reconciliation and bounded baseline recovery.

Recommendation by Copilot: content, review state, origin and edit protection could be implemented through SVG layers, filters or a combination.

Recommendation by Copilot: potential feature for the app; linking each request or proposal to the resulting edits and approval decision, provided this adds little complexity.

## Related Documents

- [README.md](../README.md): roles and project overview.
- [system-design.md](system-design.md): pipeline and SVG purposes.
- [rulebook.md](rulebook.md): navigation rules to reconcile with review decisions.
- [app-plan.md](../claude/review/app-plan.md): incremental zoning-app development.
