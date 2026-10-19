# zoning module specification

This specification is provisional and amendable, and the specification is authoritative for the development of the zoning module. Changes to the specification require the explicit confirmation of the human participant.

## purpose

- The plan tracer is a drawing application in which the zoning author draws the plan SVG over the architectural plans.
- The plan SVG is a vectorized equivalent of the architectural plans, faithful to the source material and used in place of the plans as the underlay of the zoning editor.
- The plan tracer is not an automated process. Automating it is later work.
- The zoning editor is an interface where the zoning author draws zones on top of the floor plan.
- The zoning editor is a visual, domain-aware modeling application: a specialized 2D CAD editor for indoor-navigation models, with a floor plan as its main working surface.
- Its closest practical relatives are floor-plan editors, GIS editors and lightweight CAD applications.
- The zoning editor generates the outputs zone SVG, connectivity graph JSON and navigation SVG.

## model

### model and zoning file

- The model is the zoning editor's data about the building, held in memory while the program runs. The model builds on the concepts defined in the rulebook.
- The zoning file holds the model on disk. Saving writes the model to the zoning file and loading reads the zoning file back into the model.
- The zoning file uses a custom format designed for the zoning editor, JSON text in a stable order, so changes show up as small readable diffs.
- The zoning file is `zoning.json`. It is private to the zoning editor.
- Zone ids and portal ids originate in the zoning file.

### floors

- The model holds the floors of the building. Each floor has an id, a level, the path of its plan SVG, a frame and a scale.
- The zoning file takes the id, the level, the frame and the scale of a floor from the plan SVG.

### model elements

- The zoning editor represents the model elements zones, boundaries, portals, movement lines, each with its own id. Ids follow the notation in the file format specification, and a portal id is built from the ids of its two zones.
- Each boundary is a straight line with its own start and end coordinates.
- Each zone lists the zone's boundaries by id, and two zones that share a boundary refer to the same boundary, so the boundary is stored once.
- Each zone has a floor and the properties crossable and navigable. Each floor has its own exterior zone, which is navigable and not crossable.
- Each portal is a straight line with its own start and end coordinates, the crossable section of the boundary between its two zones, chosen from positions along the portal's boundary.
- The portal's midpoint is derived from the start and the end, and represents the portal in the connectivity graph as a single coordinate.
- A vertical portal, between zones on two floors, has one position per joined floor instead of the start, the end and the midpoint.
- A portal is virtual or not, and a portal to the exterior can be marked as an emergency exit or a main entrance.
- Each movement line is one polyline with its own ordered defining coordinates.

### building content groups

| Building Content | Meaning |
| --- | --- |
| Building outline | Boundary between building interior and exterior |
| Circulation layout | Main circulation areas and their boundaries |
| Detailed spaces | Rooms, subdivisions, blocks and similar modeled areas |
| Connection elements | Doors, openings and virtual portals |

## behavior

### underlays

- The zoning author loads the source material as underlays on an SVG drawing surface.
- Several underlays can be loaded at the same time.
- Each underlay can be moved, rotated, scaled and toggled separately, so that the zoning author can fit them into one coherent plan to draw on.
- An underlay is an image file (JPG or PNG). A PDF source is converted to an image before it is loaded, because an SVG image element cannot display a PDF.

### drawing surface

- The drawing surface has a floor id, a level, a reference frame and a scale in units per meter.
- The zoning author types in these values.
- These values originate in the plan tracer. The zoning file takes them from the plan SVG.

### tracing

- The zoning author traces the underlays by drawing on the surface: lines, polylines, circles, paths, text, and symbols from a library of warehouse symbols.
- Every traced element has an id. An id is never reused in a drawing.
- Text can be attached to a traced element by its id.
- Traced elements belong to named layers.

### start

- On starting, the zoning author initializes a new zoning file or loads an existing one. Either way the data is held in memory only, and the zoning file comes before the plan SVG.
- A new zoning file starts as a skeleton. Nothing is written to disk before the first save, where the zoning author chooses the file location.
- The zoning author then loads the plan SVG as the reference underlay: one plan SVG for a new zoning file, the plan SVG referenced by each floor for an existing one.
- For a new zoning file, the zoning editor creates the floor from the plan SVG, the viewer takes its frame and scale, and saving is enabled.
- For an existing zoning file, the zoning editor checks the floor's id, level, frame and scale against the plan SVG, because they exist in both files.

### editing

- The model changes only through edit operations, such as moving a boundary or adding a portal.
- The move boundary operation moves a boundary by changing the boundary's own start and end coordinates and nothing else.
- Renaming a zone is an edit operation and changes only the zoning file.
- Drawn elements snap to each other within a given distance, to ensure exactly matching coordinates.
- The zoning author can change the model either directly or by drawing a request for an AI assistant or script using markup.

### rules and checks

- The zoning editor checks the model against a set of rules and shows the zoning author a report of the violations.
- The check runs automatically at events such as loading, saving or checkpoint, or can be started on demand.

### layers and markup

- The zoning editor holds the work in three layers: reference underlay, approved baseline, working overlay.
- The reference underlay is the plan SVG.
- The working overlay holds current edits.
- Candidate geometry shows applied edits and proposed edits.
- An applied edit has altered the model and includes approved edits awaiting a checkpoint. A proposed edit has not altered the model.
- Revision markup shows drawn requests and notes.
- A note can be a plain remark and does not have to ask for a change.
- Every layer is toggleable.
- The viewer draws the plan SVG as the reference underlay and the model as SVG shapes over it. Both share the floor's frame and scale.

### review workflow

- Requests, proposals, applied edits and approvals are distinct.
- Drawn requests remain markup until explicitly applied.
- An edit lands in the working overlay.
- The zoning author approves the edit.
- The edit stays in the working overlay until the zoning author explicitly establishes a checkpoint.
- A checkpoint integrates all edits approved since the previous checkpoint into the approved baseline.
- Not every editing batch creates a checkpoint.
- Checkpoints need not be retained as separate revisions within the zoning editor. Regular Git commits at checkpoints are a best practice for preserving history, not a requirement.
- The approved baseline is the model at the latest checkpoint.
- A finalized version is the approved baseline at the latest checkpoint.
- Finalizing sets the `zoning_file_version` of that baseline, stamped on the zoning file. Only finalizing sets it, so checkpoints carry no version and the file's content can be ahead of its stamp.
- The zoning editor generates the outputs only when the zoning author selects a finalized version and commands it. All outputs carry its `zoning_file_version`.

### decision authority

- The zoning author can ask a program or AI assistant to propose a resolution of a violation found by the check or flagged by the zoning author.
- Only the zoning author grants approval.
- Passing checks does not constitute approval.
- The zoning editor never changes geometry on its own to make a check pass.
- Explicit removals are not reversed to satisfy connectivity, and approval is not inferred.

### files

- The zoning author saves the drawing as the plan SVG through a file dialog, one file per floor. The file name `<floor id>-plan.svg` is offered.
- The plan SVG stores the placement of the underlays as references to the source files with their transforms, not as embedded images, in a group separate from the traced elements.
- The zoning author can leave the underlay references out when saving.
- Opening a plan SVG reads it back. The underlay images are picked again, by the file names stored in the plan SVG.
- The structure of the plan SVG is in the file format specification.
- The zoning editor remembers a file the zoning author picked and saves back to the file. Requires a Chromium-based browser.
- For import and export, the zoning author chooses the file location in a file-selection window.

## architecture

- The zoning editor's components include the edit operations, the viewer, the import code, the generate code, and the code that loads and saves the zoning file.
- Pan and zoom change which rectangle of the drawing is visible.

## technology

- The plan tracer is a single HTML file in plain JavaScript.
- The plan tracer runs in a desktop browser.
- No geometry library is used at this point, because the zoning editor needs only a few simple calculations, written for the zoning editor's own elements.
- The viewer draws the model as SVG and lets the zoning author click on shapes directly.
- The zoning editor is built in plain JavaScript, with no build step and no types.
- The zoning editor runs as a web page in a browser.
- Identifiers, documentation, interface text and code comments are in English.
