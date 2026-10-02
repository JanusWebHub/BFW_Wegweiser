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

## Using it in another conversation

The page is a published Claude artifact, private to its owner: https://claude.ai/artifact/1s54MKxn2Y6afHkv17D9KR. A new conversation must run under the same account and have the Artifact and ArtifactData tools.

- Read the page: Artifact tool, `action: read`, with that URL.
- Read the marks: ArtifactData, `action: list`, `collection: marks`, with that URL.
- A mark has `kind` (move, add, line, zone, note, remove), `pts` (plan coordinates, SVG viewBox 0 0 1790 1000), `target` (portal or zone id), `text` (the remark). `applied: true` means it is already done: set it with an `update` after applying a mark.
- Update the page: publish the same file with `url` set to the link. The link and the marks are kept.
- The graph is embedded in the page. After the graph changes, regenerate that data and republish. The marks are stored separately and survive.
- Opened as a plain file, the page works, but marks stay in that browser only and nobody else can read them.
- Note: the file in the repo is page version 1. The published page has the later graph and the "Applied marks" toggle.
