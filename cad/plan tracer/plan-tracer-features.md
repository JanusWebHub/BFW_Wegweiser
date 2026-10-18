# plan tracer features

This document describes what the plan tracer does. It follows the tool and is not authoritative. The requirements are in the plan tracer specification.

## floor values

- The floor id, the level, the frame (x, y, width, height) and the units per meter are typed in.
- The frame is shown on the drawing surface as a dashed rectangle.
- Saving is refused with a message when the floor id is empty, or the frame width, the frame height or the units per meter is not above zero.

## underlays

- One or more images can be loaded. A list selects the underlay that the underlay controls act on.
- An underlay is placed by dragging it with the Underlay tool or by typing x, y, rotation and scale. Arrow buttons nudge it by a step.
- The Rotate tool turns it about the center of its visible part as it is dragged (Shift: 15 degree steps).
- Make horizontal: click two points that should be level, and the underlay turns about the first.
- Calibrate: enter a real distance in meters, then click two points that far apart on the underlay, and the underlay is rescaled to match.
- Crop: drag a rectangle on the underlay with the Crop tool, and the rest of the image is hidden. Clear crop removes it.
- Fit to frame fits the visible (cropped) part to the frame.
- Opacity, brightness, contrast, visible, locked, flip horizontal and flip vertical apply to the chosen underlay.
- An underlay can be named, raised or lowered in the drawing order, and removed.

## drawing

- Tools: line, rectangle, polyline, circle, path, text and symbol.
- Line: click the start and the end, or drag from the start to the end. After the start a length in meters can be typed, followed by Enter.
- Chain lines continues a line from the last end.
- Rectangle: click two opposite corners.
- Polyline and path: click the points, then right-click, press Enter, or click the last point again to finish. A path can be a smooth curve, open or closed.
- Circle: click the center, then a point on the circle.
- Line thickness and color apply to new lines. Apply to selected lines changes existing ones.
- Ortho, by its button, its checkbox or the Shift key, locks the direction to 45 degree steps while drawing. It makes rectangles square and keeps moves and line-end drags on one axis.
- Right-click ends a chain or cancels a pending point. Esc cancels.

## snapping and guides

- Points snap to line ends, midpoints, intersections and the grid. A marker at the cursor shows the kind of snap.
- Tracking guides, switched by a checkbox, snap the cursor level with the ends and midpoints of lines and with the start point, onto the extension of a line beyond its end, and where two guides cross.
- While drawing, the cursor also snaps to the perpendicular foot on a line, parallel to a hovered line, and to polar angles of 0, 30, 45, 60 and 90 degrees and so on around the start point. Ortho turns the tracking off while a line is drawn.
- Snapping and tracking use straight lines only. Hidden layers are left out.
- A grid can be shown, with a spacing, and snapped to.

## selecting and editing

- Select: click an element, Shift-click to add, drag on empty space to select a box, drag to move, drag a line end, a polyline or path vertex, or a circle radius to reshape.
- Delete, Duplicate, Undo, Redo and Select all. Keys: Delete, Ctrl+Z, Ctrl+Y or Ctrl+Shift+Z, Ctrl+A.
- Every element has an id, shown in the Edit section and renamable there.
- Offset: select lines, set a distance in meters, click the side. Each copy keeps the thickness and color of its line.
- Trim: click a line, and the part between the nearest crossings with other lines on either side of the click is removed. The rest of the line stays, as two lines when crossings lie on both sides. With a crossing on one side only, the part from that crossing to the end of the line on the click's side is removed. With no crossing, a message says so.
- Extend: click a line near one end, and that end is lengthened to the first line it meets. With none, a message says so.
- Join collinear joins touching or overlapping collinear lines of the same thickness, color and layer. It works on the selected lines, or on all editable lines when none is selected.
- Arrange aligns the selection left, right, top, bottom, centered horizontally or vertically, and distributes it horizontally or vertically.
- Measure: click two points to read the distance.
- Dimension: click two points, then where the dimension line goes. It creates two extension lines, the dimension line and a text with the length, as ordinary lines and a text.

## text

- Text is typed in the Text field and placed with the Text tool. A preview follows the cursor.
- A click on a line, polyline, path, circle or symbol attaches the new text to it. The option can be switched off.
- Attached text follows its element, lies along lines, and its offset can be dragged. Attach text and Detach text change the attachment of selected elements.
- Deleting an element deletes its attached texts.
- A selected text can be edited, and its font size changed.

## symbols

- Types: stairs, shelf or rack, door with swing, gate or roller door, loading dock door, column, pallet, ramp, elevator.
- A symbol is placed with a click, centered on it. Its width and depth are set in meters and use the units per meter.
- A symbol is rotated in 90 degree steps. Type, size and rotation of a selected symbol can be changed.

## layers

- Layers can be added, renamed and deleted. A deleted layer's elements move to the first remaining layer.
- A layer can be hidden or locked. Hidden layers are not drawn, snapped to or exported. Locked layers cannot be picked.
- New elements go to the chosen layer. Selected elements can be moved to it.

## view

- Pan: Pan tool, middle mouse button or two fingers. Zoom: wheel, pinch or the zoom buttons.
- Zoom to frame, zoom to drawing, and Zoom window, which zooms to a dragged rectangle.
- Rulers read meters from the frame's top-left corner. A scale bar shows a round length. One checkbox switches both.
- A minimap, switched by a button, shows the whole drawing. Clicking or dragging in it moves the view.

## files

- Save writes the plan SVG through a file dialog. A checkbox leaves the underlay references out.
- Open reads a plan SVG. The underlay images are picked again. An older file without layers puts its elements in a default layer.
- Export PNG saves the frame area as a picture, with the visible underlays and traced elements and without grid or guides.
- New clears everything and needs a second click within three seconds.
- The work is autosaved in the browser: floor values, traced elements and underlay placement, not the images. It is restored at the next start.
- Closing the page with unsaved changes asks for confirmation.

## interface

- The panel has collapsible sections, and its width is adjustable by dragging the bar beside it.
- The theme cycles system, light and dark.
- The status bar shows the active tool, a hint for it, the live length and the angle while drawing.
- An info box in the top right corner of the drawing shows the tool and hint, the cursor coordinates, the selection count, the length of the selection, the drawing length and the angle.
- A toast shows short messages over the drawing.
- A Help box explains the controls and can be minimized.
- The theme, the collapsed sections, the panel width, the last view and the minimap state are remembered in the browser.
- In windows narrower than 700 pixels the panel sits above the drawing.
