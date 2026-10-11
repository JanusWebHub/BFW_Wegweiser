# zoning editor specification

This specification is provisional and amendable, and the specification is authoritative for the development of the zoning editor. Changes to the specification require the explicit confirmation of the human participant.

## purpose

- The zoning editor is an interface where the zoning author draws zones on top of the floor plan.
- The zoning editor generates the outputs zone SVG, connectivity JSON and navigation SVG.

## model

### model and project file

- The model is the zoning editor's data about the building, held in memory while the program runs. The model builds on the concepts defined in the rulebook.
- The project file holds the model on disk. Saving writes the model to the project file and loading reads the project file back into the model.
- The project file uses a custom format designed for the zoning editor, JSON text in a stable order, so changes show up as small readable diffs.

### model elements

- The zoning editor represents the model elements zones, boundaries, portals, movement lines, each with its own id.
- Each boundary is a straight line with its own start and end coordinates.
- Each zone lists the zone's boundaries by id, and two zones that share a boundary refer to the same boundary, so the boundary is stored once.
- Each portal is a straight line with its own start and end coordinates, chosen from positions along the portal's boundary.
- The portal's midpoint is derived from the start and the end, and represents the portal in the connectivity graph as a single coordinate.
- Each movement line is one polyline with its own ordered defining coordinates.

## behavior

### editing

- The model changes only through edit operations, such as moving a boundary or adding a portal.
- The move boundary operation moves a boundary by changing the boundary's own start and end coordinates and nothing else.
- Drawn elements snap to each other within a given distance, to ensure exactly matching coordinates.
- The zoning author can change the model either directly or by drawing a request for an AI assistant or script using markup.

### rules and checks

- The zoning editor checks the model against a set of rules and shows the zoning author a report of the violations.
- The check runs automatically at events such as loading, saving or checkpoint, or can be started on demand.

### layers and markup

- The zoning editor holds the work in three layers: reference underlay, approved baseline, working overlay.
- The reference underlay is the plan SVG.
- The working overlay holds current edits.
- Candidate geometry shows proposed and applied edits.
- Revision markup, separately toggleable, shows drawn requests and notes.
- A note can be a plain remark and does not have to ask for a change.

### review workflow

- Requests, proposals, applied edits and approvals are distinct.
- Drawn requests remain markup until explicitly applied.
- An edit lands in the working overlay.
- The zoning author approves the edit.
- The edit stays in the working overlay until the zoning author explicitly establishes a checkpoint.
- A checkpoint integrates all edits approved since the previous checkpoint into the approved baseline.
- The approved baseline is the model at the latest checkpoint.
- Outputs are generated from the same explicitly selected approved baseline.

### decision authority

- The zoning author can ask a program or AI assistant to propose a resolution of a violation found by the check or flagged by the zoning author.
- Only the zoning author grants approval.
- Approval does not automatically lock geometry.
- Passing checks does not constitute approval.
- The zoning editor never changes geometry on its own to make a check pass.

### files

- The zoning editor remembers a file the zoning author picked and saves back to the file. Requires a Chromium-based browser.
- For import and export, the zoning author chooses the file location in a file-selection window.

## architecture

- The zoning editor's components include the edit operations, the viewer, the import code, the generate code, and the code that loads and saves the project file.
- Pan and zoom change which rectangle of the drawing is visible.

## technology

- No geometry library is used at this point, because the zoning editor needs only a few simple calculations, written for the zoning editor's own elements.
- The viewer draws the model as SVG and lets the zoning author click on shapes directly.
- The zoning editor is built in plain JavaScript, with no build step and no types.
- The zoning editor runs as a web page in a browser.

## open issues

- How a connection between two boundary ends is recorded, and how it is checked and enforced are to be worked out.
- How the start and the end coordinates of a portal are related to the positions on its boundary is to be worked out.
- How a portal follows a boundary that moves, and how the rule that a portal sits on the portal's boundary is enforced are to be worked out.
- Boundaries that are not straight would need more than two coordinates, potentially as an SVG polyline or path. How a portal sits on them must be worked out as well.

## potential features

- The zoning editor could later run outside a web browser, both headless, such as with Node, and in a window of its own.
- A routing point other than the midpoint can be added later as an optional stored crossing point that overrides the midpoint.
- Ids for geometry points, such as a corner.
- Stated relationships whose geometry is not yet drawn, such as "these are separate spaces".
