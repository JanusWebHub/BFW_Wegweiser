# EG Redline

`eg-redline.html` is a markup page for the EG plan. It shows the Lageplan with the connectivity graph on top. You draw corrections on it, and they are saved as exact plan coordinates for Claude to read.

It runs as a published Claude artifact. The saved marks need that artifact's shared storage. Opened as a plain file it works, but marks stay in that browser only.

## What you can do

- Pan and zoom: drag, wheel or pinch. The area menu jumps to a region.
- Move door (M): drag a door, or one of its ends.
- Add door (D): drag along the doorway, or click start then end.
- Wall / cut (L): draw a wall, boundary or re-cut line.
- Zone outline (Z): click the corners, then Enter or Finish zone.
- Note (N): click where the remark belongs and type it.
- Remove (X): click a door or zone to mark it for removal.
- Type what each mark means in the text field. Snap and layer toggles are in the header.
