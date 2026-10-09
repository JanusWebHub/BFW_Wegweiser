# Zoning Module Description

## Parts And Artifacts

The zoning module's directory is `cad/`. Its two main parts are the plan tracer and the zoning editor.

The chain of artifacts is: source material, plan SVG, zone SVG, navigation SVG. It is a supply chain, not a derivation.

## Plan Tracer

The plan tracer generates the plan SVG, a vectorized equivalent of the architectural plans, faithful to the source material and used in place of the plans as the underlay.

Architectural sources can be incomplete or contradictory. The source material files are usually messy and large. No single source contains all the relevant information, and most contain information that shouldn't be carried over. They therefore need combining and cleaning.

The original sources are kept in `cad/source material/`.

## Zoning Editor

### Purpose And Nature

The zoning editor is a visual, domain-aware modeling application: a specialized 2D CAD editor for indoor-navigation models, with a floor plan as its main working surface. Its closest practical relatives are floor-plan editors, GIS editors and lightweight CAD applications.

The zoning editor incorporates the project's established review mechanisms. The zoning author works directly on zones, shared boundaries, portals and movement geometry, with the plan SVG underneath. The zoning editor also retains markup and communication with generative AI agents as important capabilities, rather than replacing them with direct editing alone.

The zoning editor is intended to become fully usable without AI assistance. Agents may assist with interpretation, proposals, authorized edits and checks, but must not be necessary to remember or execute the author's decisions.

### Domain-Aware Editing

Editing operates on building-model objects and relationships, not only graphical primitives. Moving a shared boundary differs from independently moving two polygon edges. Creating a portal establishes a crossable portion of a boundary between two zones, not merely a symbol near a wall.

The zoning editor can maintain consequences that are mechanically determined while leaving interpretation to the zoning author.

The same model can be inspected spatially, topologically, semantically and historically: geometry, connections, movement permissions, and requested, changed or approved content. These are complementary views, not four separate editors.

### Review And Decision Authority

Requests, proposals, applied changes and approvals are distinct. Drawn requests remain markup until explicitly applied; direct model edits need not first become drawn requests. Notes need not request a change.

The work is held in separate layers:

- Reference underlay: the plan SVG.
- Approved baseline: the model at the latest checkpoint.
- Working overlay: current changes. Candidate geometry shows proposed and applied edits; revision markup, separately toggleable, shows drawn requests and notes.

An edit lands in the working overlay and the zoning author approves it. It stays in the overlay until the author explicitly establishes a checkpoint, which updates the baseline.

Content category, review state, origin and edit protection (what the content is, where it stands in review, who made it, and whether it is locked) are independent dimensions. Approval does not automatically lock geometry. Only the zoning author grants approval; passing checks does not constitute approval.

Cleanup must preserve intended geometry. It must not silently replace existing geometry, reverse explicit removals or invent connections merely to improve check results.

### Project File And Import

The zoning editor's own working document is a structured project file (JSON) designed as a native file format for the editor, which it saves and loads. It stores each shared boundary once, referenced by both adjacent zones, and stores a portal by its position along a boundary, so the portal follows the boundary when it is edited. Unresolved interpretations are records of their own. The zoning editor draws its view from this file.

The zoning editor is also intended to be able to import other formats as sources of information, such as SVG as underlay or geometry, and connectivity or routing graphs.

### Outputs

The zoning editor generates zone SVG, connectivity JSON including authored movement geometry, and navigation SVG.

Zone SVG and connectivity JSON come from the same explicitly selected approved baseline, excluding the reference underlay and review annotations. Navigation SVG and displayed route geometry share a coordinate frame.
