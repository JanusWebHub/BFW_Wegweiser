# zoning editor specification

This specification is provisional and amendable, and the specification is authoritative for the development of the zoning editor. Changes to the specification require the explicit confirmation of the human participant.

## definition and description

- The zoning editor has a snap distance. When the zoning author draws a corner within the snap distance of an existing corner, the zoning editor attaches the new corner to the existing corner by the existing corner's id, so the stored data is exact.
- The zoning editor can maintain consequences that are mechanically determined while leaving interpretation to the zoning author.
- A program may at most propose a match, and only the zoning author decides.
- When the zoning editor loads a project file, the zoning editor checks the rules (an outline is closed, a portal sits on the portal's boundary, and so on) and shows any violation to the zoning author.
- The check on loading also catches changes an AI assistant made by editing the project file's text directly.
- The generated graphs of the BFW EG zoning review will be absorbed by the zoning module, either by redrawing the generated graphs over the underlay or by a later geometry import.

### what the zoning editor is and produces

- The zoning editor is an interface where the zoning author draws zones on top of the floor plan.
- The zoning editor generates zone SVG, connectivity JSON (including authored movement geometry) and navigation SVG.
- Zone SVG and connectivity JSON come from the same explicitly selected approved baseline, excluding the reference underlay and review annotations.
- Navigation SVG and displayed route geometry share a coordinate frame.

### model

- The model is the zoning editor's data about the building as held while the program runs: corners, boundaries, zones and portals, each with an id.
- The project file is the zoning editor's model data about the building saved on disk.
- Loading a project file puts the project file's data into the model, and saving writes the model back to the project file.
- The zoning editor represents the model with different kinds of element: zones, shared boundaries, portals, movement geometry and unresolved interpretations.
- Unresolved interpretations are records of their own.
- The zoning editor's model has corners, each with an id; boundaries, each joining two corners by the corners' ids; zones, each a list of boundaries; and portals.
- The zoning editor has edit operations that change the model, such as moving a boundary or adding a portal.
- The zoning editor has rules such as "a zone outline is closed".
- The model builds on the meanings in the rulebook.
- Defining the model's structure precisely is a distinct and fundamental step in creating the zoning editor.
- Two zones that share a boundary refer to the same boundary by the boundary's id, so the boundary is stored once.
- The "move boundary" operation moves a boundary by changing the numbers stored for the boundary's two corners.
- Each zone lists the zone's boundaries by id.
- Each portal stores a position along the portal's boundary.
- Zones and portals therefore change position with the moved boundary and need no separate update.

### layers, review and decisions

- The zoning editor holds the work in three layers (reference underlay, approved baseline, working overlay).
- The zoning editor describes content by four independent dimensions (content category, review state, origin and edit protection).
- The reference underlay is the plan SVG.
- The approved baseline is the model at the latest checkpoint.
- The working overlay holds current changes.
- Candidate geometry shows proposed and applied edits.
- Revision markup, separately toggleable, shows drawn requests and notes.
- Content category, review state, origin and edit protection (what the content is, where it stands in review, who made the content, and whether the content is locked) are independent dimensions.
- An edit lands in the working overlay and the zoning author approves the edit.
- The edit stays in the working overlay until the zoning author explicitly establishes a checkpoint; the checkpoint updates the baseline.
- Approval does not automatically lock geometry.
- Requests, proposals, applied changes and approvals are distinct.
- Drawn requests remain markup until explicitly applied.
- Only the zoning author grants approval.
- Passing checks does not constitute approval.
- The zoning author can change the model directly, without first drawing a request for an AI assistant or script to apply.
- A note can be a plain remark and does not have to ask for a change.
- The zoning editor retains markup and communication with generative AI agents as secondary capabilities, next to direct editing.
- The zoning editor checks the model for problems (gaps, overlaps, a portal off the portal's boundary, an unreachable zone) and shows the problems to the zoning author.
- The zoning editor never changes geometry on its own to make a check pass.
- Resolving the gaps, overlaps and other discrepancies that the checks report is done by the zoning author.
- A program or AI assistant may propose a resolution, and the zoning author decides.

### project file, persistence and import

- The zoning editor's own working document is a structured project file (JSON) designed as a native file format for the zoning editor, and the zoning editor saves and loads the project file.
- The zoning editor saves the work as the project file.
- The project file is text with a stable order, so changes show as small readable diffs and AI agents can edit the project file.
- The zoning editor remembers a file the zoning author picked and saves back to the file.
- For import and export, the zoning author chooses the file location in a file-selection window.
- The zoning editor loads an underlay.
- The zoning editor is intended to be able to import other formats as sources of information, such as SVG as underlay or geometry, and connectivity or routing graphs.
- A file in another format, such as an old graph, is imported only as an underlay: shown, not converted.
- The zoning author draws the zones in the zoning editor.
- Importing geometry from files in another format is a later, separate decision.
- If that decision is made, every match of corners is shown to the zoning author for approval and no match is made silently.

### construction

- The zoning editor is a program made of code.
- The zoning editor's components include the edit operations, the viewer, the import code, the generate code, and the code that loads and saves the project file.
- Only the edit operations, such as "move boundary", change the numbers stored in the model once the model exists.
- All other code may read the model, for example to draw the model, but may not change the model.
- The model's data is kept where only the edit operations can reach it.
- If any other code tries to change the model's data, the attempt is rejected or the program fails visibly.
- Loading a project file builds the model from the project file, so loading a project file is the one way the model comes into existence without going through the edit operations.
- The viewer reacts to the zoning author's mouse clicks and drags on the screen.
- The viewer does not change the model itself.
- When the zoning author drags a boundary, the viewer runs the "move boundary" operation with that boundary's id and the new position.
- The viewer and the generate code only read the model.
- The generate code produces the zone SVG, connectivity JSON and navigation SVG from the model.
- The import code reads a file in another format.
- An imported file is only an underlay and never touches the model.
- If geometry import is ever decided, geometry import would have to use the edit operations as well.
- Pan and zoom change which rectangle of the drawing is visible.

### initial choices

- No geometry library is used at this point.
- The zoning editor needs only a few simple calculations, written for the zoning editor's own elements.
- The viewer draws the model as SVG.
- SVG matches the output format.
- SVG lets the zoning author click on shapes directly.
- Because the model is separate from the viewer, the drawing surface can be replaced later without changing the model.
- The zoning editor is initially built in plain JavaScript, with no build step and no types.
- The zoning editor initially runs as a web page in a browser.
- A program installed on the computer with the program's own window is not for the beginning.

## open decisions and future potentials

- Toolchain: Node, with Vite, Vitest and TypeScript, is an alternative to consider later.
- Where the zoning editor runs: other options than a web page in a browser may be considered later.
- A browser can remember a file the zoning author picked and save back to the file only through the browser's directory-access feature.
- As far as known, the feature exists only in Chromium-based browsers such as Chrome and Edge.
- That the feature exists only in those browsers is to be verified.
- The limitation constrains the item on remembering a picked file.
- Future potential: the zoning editor usable both through a window interface and through headless operation.
- Headless operation means the program runs without the window interface.
- Headless operation needs a way to run the edit operations outside the browser.
- That way means Node or a similar program for running JavaScript.
- The need for that program interacts with the toolchain decision.
- UI framework: deferred.
