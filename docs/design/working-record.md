# Working Record: Decisions And Agreements

Started: 2026-10-03
Last updated: 2026-10-03
Human participant: Deniz
AI assistant: GitHub Copilot

## Purpose

This is a provisional and amendable record of decisions, agreements, qualifications, insights, ideas, and understanding confirmed by the human participant. It provides a persistent reference point within and across sessions with AI assistants. It does not replace authoritative project documents.

Confirmed agreements, conditional agreements, provisional terms and recommendations are distinguished explicitly. Changes to recorded agreements require the human participant’s explicit confirmation.

## Roles and precise language

- Project author: develops and maintains the project.
- Zoning author: creates and reviews the building model.
- Navi-user: uses the finished navigation application.
- Human participant: the person chatting with the AI assistant.

One person may occupy several roles. Use specific role and artifact names wherever generic terms would be ambiguous.

## Two independent work tracks

Zoning is the authoring stage of Wegweiser, separate from its navigation client.

- Local BFW review: recover and continue the latest cloud review state locally, without waiting for the app.
- Standalone zoning app: develop an uncomplicated authoring tool on a separate feature branch, informed by the review without requiring reuse of its scripts.

The tracks share concepts and compatible outputs.

Recommendation by Copilot: establish the app branch after rule reconciliation and bounded baseline recovery.

## Rule reconciliation and recovery

First reconcile confirmed review decisions with the rulebook and system design. In particular, distinguish blocks outside navigable zones from obstacles within zones. The review proposal to represent blocks as a zone kind is not automatically the final definition. Other review-driven rule changes also require explicit reconciliation; the AI-written app plan is not a silently adopted specification.

The cloud review was the zoning author's interpretation, drawing, decisions and corrections with AI assistance, not wholesale acceptance of AI output. The supplied conversation summary is intermediate; later work must be considered when establishing the recoverable state. That summary is a temporary contextual aid, intended for deletion after planning, not the baseline itself.

Preserve a reference snapshot of the latest recoverable inputs, scripts, marks and outputs. Make the pipeline runnable locally without intentionally changing its results; compare regeneration against the reference and record discrepancies instead of silently repairing them. Keep recovery separate from improvements. Reproduction establishes reproducibility, not correctness or approval.

Conditional agreement: preserve the inputs, dependencies, scripts and outputs needed for reproduction without imposing excessive maintenance burden. The preservation mechanism is not yet agreed. Keep recovery bounded; its purpose is to preserve and understand the experiment.

Source photographs, the older whole-building plan, composites, overlays and simplified models have different evidential roles. Overlays aid comparison but do not resolve conflicting sources. Detecting larger structures or passing geometry and connectivity checks does not establish architectural truth.

## Representations and generated outputs

One editable project supports distinct representations, not three independently edited SVG files:

- Zoning working view: the model plus review layers, used during authoring and review.
- Zoned SVG (provisional name): clean semantic floor plan paired with connectivity JSON, without review annotations. Both are generated from an explicitly selected approved baseline revision, excluding the reference underlay and pending review overlays.
- Navigation SVG: a separate map for displaying routes to the navi-user. Generation point not yet specified.

## Layers and independent dimensions

| Building Content | Meaning |
| --- | --- |
| Building outline | Boundary between building interior and exterior |
| Circulation layout | Main circulation areas and their boundaries |
| Detailed spaces | Rooms, subdivisions, blocks and similar modeled areas |
| Connection elements | Doors, openings and virtual portals |

| Working Arrangement | Meaning |
| --- | --- |
| Reference underlay | Source PDF or image |
| Approved baseline | Model state accepted by the zoning author at the latest revision checkpoint. |
| Working overlay | Requested or proposed changes, annotations, and applied edits awaiting approval |

Within the working overlay, candidate geometry shows proposed changes and applied edits awaiting approval. Separately toggleable revision markup shows drawn requests, notes and remarks communicating intent.

Four independent dimensions distinguish the work:

- Content category: building outline, circulation layout, detailed spaces or connection elements.
- Review state: requested, proposed, applied awaiting review, approved; rejected and superseded where applicable.
- Origin: zoning author, AI assistant or script.
- Edit protection: editable or locked, with explicit unlocking. Approval does not automatically lock geometry.

Recommendation by Copilot: these distinctions could be implemented through SVG layers, filters or a combination.

Editing shared boundaries across content layers requires coordination; the mechanism is not yet decided.

## Intent, application and approval

A request records intent. A proposal describes a candidate implementation. Applying it changes the working model but does not imply approval. Approval records the zoning author's acceptance and explicitly updates the baseline, preserving the previous revision. The baseline remains inspectable during review; approval does not guarantee absolute correctness.

A drawn request may resemble geometry but remains markup until explicitly applied. A proposal can be previewed without altering the model. The zoning author can draw requested changes for an AI assistant or script to apply, or leave notes asking an AI assistant to propose changes. Notes need not be change requests. "Corrected" is not a review status because it implies correctness prematurely.

AI assistants and scripts may propose changes or apply authorized changes; only the zoning author grants approval. Passing checks does not constitute approval. Do not silently replace existing geometry, reverse explicit removals to satisfy connectivity, or infer approval.

Conditional agreement: lightweight links from requests or proposals to resulting edits and approval decisions should make "what changed and why" recoverable without conversation memory. This must not introduce substantial complexity; implementation details are not agreed.

## Incremental app development

The redline artifact originated as a visual communication tool, avoiding the need to express every spatial correction in text. Initially, the zoning author communicates intent through marks; the AI assistant interprets and applies changes, saves model data as JSON, runs checks, regenerates the view, and returns it for further human review.

Bring those operations into the app incrementally: persist and communicate intent, support applying changes directly, then support checking and regenerating the model and views. The end goal is a self-sufficient semantic SVG authoring app usable without AI assistance. Optional assistance may remain, but must not be necessary to remember or execute decisions.

Prove a small complete workflow: open the BFW project, inspect the underlay, edit a boundary or door, undo, save, reopen, and inspect validation results. Each stage must keep requested changes distinguishable from actual model edits. Expand as review work demonstrates a need, not by blindly porting historical workarounds.

## Related Documents

- [README.md](../../README.md): roles and project overview.
- [system-design.md](../system-design.md): pipeline and SVG purposes.
- [rulebook.md](../rulebook.md): navigation rules to reconcile with review decisions.
- [app-plan.md](../../claude/review/app-plan.md): incremental zoning-app development.
