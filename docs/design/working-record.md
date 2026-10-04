# Working Record: Decisions And Agreements

Started: 2026-10-03
Last updated: 2026-10-04
Human participant: Deniz
AI assistant: GitHub Copilot

## Purpose

This is a provisional and amendable record of decisions, agreements, qualifications, insights, ideas, and understanding confirmed by the human participant. It provides a persistent reference point within and across sessions with AI assistants. It does not replace authoritative project documents.

Confirmed agreements, conditional agreements, provisional terms and recommendations are distinguished explicitly. Changes to recorded agreements require the human participant's explicit confirmation.

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
- Navigation SVG: a separate map for displaying routes to the navi-user. Generation point not yet specified.

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

- [README.md](../../README.md): roles and project overview.
- [system-design.md](../system-design.md): pipeline and SVG purposes.
- [rulebook.md](../rulebook.md): navigation rules to reconcile with review decisions.
- [app-plan.md](../../claude/review/app-plan.md): incremental zoning-app development.
