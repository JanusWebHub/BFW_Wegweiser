# Zoning Module Course Of Actions

The steps as they would happen in reality, from source material to generated outputs. Each step has a status: agreed (settled), open (mechanism or detail not decided) or idea (raised, not decided). A step in two cases is numbered with A and B. Steps 1 to 7 (plan tracer) are approved, steps 8 to 11B (start of the zoning editor) tentatively, steps 12 to 23 are drafts not yet reviewed by Deniz.

- 01, agreed: The source material (plans, emergency-plan photos) is kept in cad/source material/.
- 02, agreed: The zoning author starts the plan tracer.
  - Note: The plan tracer is a drawing application. The first version is a working module with manual tracing; automating it is later work.
- 03, agreed: The zoning author loads the source material as underlays on the plan tracer's SVG drawing surface. The surface can hold several underlays, such as the plan PDF and the emergency-plan photos.
  - Note: An SVG image element cannot display a PDF, so a PDF source has to be converted to an image before it can be loaded as an underlay. How the loading and the conversion work is not specified.
- 04, agreed: The author moves, rotates and scales the underlays until they form one coherent plan. Each underlay can be toggled separately.
- 05, agreed: The author sets the floor id, the level, the reference frame and the scale on the drawing surface. They are the fundamental values passed along the line.
  - Note: Open: where the plan SVG records the floor id, the level and the scale.
- 06, agreed: The author traces what the plans show, by drawing on the surface as SVG: lines, polylines, circles and paths for walls and outlines, text such as printed room numbers, and symbols, each with an id, in named layers. No zones or portals.
- 07, agreed: The author saves the drawing as the plan SVG. The tracing repeats for each floor and gives one plan SVG per floor.
  - Note: The plan SVG also stores the placement of the underlays (moves, rotations, scales, toggles), as references to the source files with their transforms, not embedded images, in a group separate from the traced lines.
- 08, agreed: The zoning author starts the zoning editor.
- 09A, agreed: The zoning author initializes the zoning file skeleton, in memory only.
- 09B, agreed: The author loads an existing zoning file, and the editor reads it into memory.
- 10A, agreed: The author loads a plan SVG as the underlay, and the viewer shows it as the underlay.
- 10B, agreed: The author loads the plan SVG referenced by each floor, and the viewer shows it as the underlay.
- 11A, agreed: The editor creates the floor from the plan SVG: its id, level, svg path, frame and scale. The drawing surface takes the frame and scale, and saving the zoning file is enabled.
- 11B, agreed: The editor checks the floor's id, level, frame and scale against the plan SVG.
- 12, agreed: The viewer draws the plan SVG as the reference underlay.
- 13, agreed: The viewer draws the model over it as SVG shapes, each carrying the id of its element. Both share the floor's frame (view_box) and scale (units_per_meter).
- 14, agreed: The author toggles layers: plan SVG, approved baseline, applied edits, proposed edits and revision markup.
  - Note: The specification still makes only revision markup toggleable (line 47).
- 15, agreed: The author edits through edit operations. Each applied edit lands in the working overlay and shows as candidate geometry.
  - Note: Open separately: whether applied and proposed edits are serialized as operations with arguments or as resulting elements.
- 16, agreed: The author draws requests and notes as revision markup.
- 17, agreed: The author asks a program or AI assistant to propose a resolution or a change. Proposals are previewed as candidate geometry and do not alter the model.
- 18, agreed: The editor checks the model against its rules and shows the author a report of violations. This runs at loading, saving and checkpoint, or on demand.
- 19, agreed: The author approves edits. Only the author grants approval, and passing checks is not approval.
- 20, agreed: The author sets a checkpoint, which integrates all approved edits into the approved baseline.
- 21, idea: The author saves and the editor writes the zoning file. A temp file is overwritten on every change for recovery.
  - Note: In A, the first save asks for the file location in the save dialog. Idea, not decided: the temp file would live in the browser's own storage, because the page cannot create a sibling of a single picked file. It holds the last checkpoint and the edits since; earlier checkpoints are not kept.
- 22, agreed: The author finalizes. That sets the zoning_file_version on the approved baseline at the latest checkpoint, stamped on the zoning file. Only finalizing sets it.
  - Note: Checkpoints carry no version, so the file's content can be ahead of its stamp.
- 23, agreed: The author selects the finalized version and commands generation. The editor produces the connectivity graph, the zone SVG and the navigation SVG, all with that zoning_file_version.
