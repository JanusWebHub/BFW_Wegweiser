# plan tracer specification

This specification is provisional and amendable, and the specification is authoritative for the development of the plan tracer. Changes to the specification require the explicit confirmation of the human participant.

## purpose

- The plan tracer is a drawing application in which the zoning author draws the plan SVG over the architectural plans.
- The plan SVG is a vectorized equivalent of the architectural plans, faithful to the source material and used in place of the plans as the underlay of the zoning editor.
- The plan tracer is not an automated process. Automating it is later work.

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

### files

- The zoning author saves the drawing as the plan SVG through a file dialog, one file per floor. The file name `<floor id>-plan.svg` is offered.
- The plan SVG stores the placement of the underlays as references to the source files with their transforms, not as embedded images, in a group separate from the traced elements.
- The zoning author can leave the underlay references out when saving.
- Opening a plan SVG reads it back. The underlay images are picked again, by the file names stored in the plan SVG.
- The structure of the plan SVG is in the file format specification.

## technology

- The plan tracer is a single HTML file in plain JavaScript.
- The plan tracer runs in a desktop browser.
- Identifiers, documentation, interface text and code comments are in English.
