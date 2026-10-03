# Plan: Zoning Studio, a standalone web app (GitHub Pages)

## Goal
Static, client-only web app (no server, no accounts) for a zoning author to create and review a semantic zoning SVG and its counterpart connectivity graph, serialized as JSON, with derived routing data. The intended end goal is self-sufficient authoring without AI assistance, informed by the BFW Charlottenburg EG review. Hosted on github.io; all project data stays in the browser; projects import/export as files.

## Roles and incremental development

The zoning author operates this app to create and review the building model. When discussing communication with an AI assistant, "human participant" means the person chatting with that assistant. The navi-user uses the separate Wegweiser navigation application, not this authoring app. The zoning SVG is distinct from the navigation SVG used to present routes to the navi-user.

The visual interface initially serves primarily as a communication tool: the zoning author records requested changes as marks, and an AI assistant interprets and applies them, saves model data, runs checks, and regenerates the view for further review. A requested change is not the same as an applied model edit; both states must remain distinguishable.

Development should bring those operations into the app incrementally: first persist and communicate intent, then support applying changes directly, then checking and regenerating the model and its views. The eventual complete workflow is usable by a zoning author without AI assistance, with undo and inspection of changes. Assistance may remain optional rather than necessary to remember or execute decisions.

Start with a few clear interface controls rather than exposing every combination of content categories, review states, origins and edit protection at once.

The app is developed on a separate feature branch. Recovery and continuation of the BFW review in the local working directory are independent work and do not wait for the app. The review informs requirements and supplies candidate reference data; its historical scripts are not automatically the app's implementation.

The detailed proposals below remain subject to explicit reconciliation with the rulebook, system design, and confirmed review decisions. This clarification does not approve all proposed rules or change the detailed milestones.

## Inputs to read first (in this repo / the claude-updated.zip)
- `docs/data/zoning_guidelines.md`, `docs/data/graph_format.md` (the spec; authoritative)
- `claude/review/SPEC-PROPOSALS.md` (zone kind `block`, nested rooms; adopt as spec)
- `claude/review/CORRECTIONS.md`, `RECAP.md` (what the review learned; rules below come from it)
- `claude/tools/page-source/*` (existing redline UI: template, tools, style panel)
- `claude/review/scripts/` (geometry pipeline: `batch2.py`, `fixed.py`; the logic to port)
- `claude/review/data/*.json` (reference output = acceptance fixture)

## Data model (single project file `*.zoning.json`)
- `meta`: name, floor, `units_per_meter`, frame (viewBox), underlay image ref/offset/scale/rotation.
- `zones[]`: id, polygon (+holes), kind (`room|corridor|stair|lift|anteroom|terrace|block|exterior`), `crossable`, label, flags.
- `portals[]`: id (`A_B`, `_2` suffix), zones, point, kind (`door|virtual|opening|emergency_exit|main_entrance`), `assumed` flag.
- `underlay`: the plan image/PDF **embedded in the project file** as base64 (default; e.g. a 511 KB PDF becomes ~680 KB), plus rotation (the BFW Lageplan PDF is stored upside down, so rotate 180° on import), offset, scale, opacity, greyscale. Option "don't embed" (reference by file name; zoning author re-selects it on open). Warn above 10 MB. PDFs render via pdf.js, kept as PDF (not rasterised) in the file.
- `marks[]` (optional history of edits, for undo/audit).
- Derived (never hand-edited): routing segments, validation report.
- Export: `connectivity-graph.json`, `routing-graph.json`, semantic `plan.svg` (classes per kind, ids = zone ids, portals as `<circle>`), `report.md`.

## Core rules (from the review; must be enforced by code)
1. Zones tile the shell: **no gaps, no overlaps**, shared boundaries exact (snap tolerance ~0.8 units).
2. Every door lies on the shared boundary of its two zones (≤0.6 units). Drawn doors win up to ~4.5 units (wall moves), beyond that the door snaps to the wall.
3. `block` = inaccessible (shaft, wall mass, column, ventilation): never crossable, no portal, hatched.
4. Nested room: cut out of host as notch/hole; host crossable only if sole access.
5. Split halls/corridors: whole shared edge = one virtual portal.
6. Routing graph = connectivity + straight segments between portal pairs inside crossable zones; segments must stay inside their zone (non-convex zones need splitting or visibility-graph routing); distance = length / units_per_meter.
7. Geometry drawn by the zoning author is exact: **no smoothing, no buffering, no zigzag**. Leftover gaps are split between neighbours by straight Voronoi cuts, never by growing shapes.
8. Validity: one connected component (except blocks), every non-block zone has a portal, assumed doors flagged and listed.

## Architecture
- Vanilla JS/TS + Vite build, output to `docs/` or `gh-pages`. No backend.
- Geometry in-browser: `polygon-clipping` (union/diff/intersection), `flatten-js` or `turf` helpers, `rbush` index. Voronoi-gap split: sample boundaries, nearest-neighbour regions (port of `_faces`).
- Rendering: SVG canvas with pan/zoom, underlay image/PDF (`pdf.js`), layers panel, style panel (reuse existing palette and Style panel).
- Storage: IndexedDB autosave + import/export file; optional "share" = download. URL hash for view state only.
- Port Python pipeline to TS modules: `snap`, `merge`, `faces`, `fill/trim`, `doors`, `portals`, `routing`, `validate`, `export`. Keep Python scripts as a reference/test oracle only.

## Workflow (UI)
1. **Import** plan image/PDF; calibrate (two points + real distance → `units_per_meter`; rotation/offset).
2. **Shell**: draw/trace outer outline.
3. **Zones**: draw polygons, set kind/label/crossable; tools: split, merge, cut, snap-to-line, move vertex.
4. **Doors**: add/move/remove; kind and `assumed` toggle; auto-propose doors on shared walls.
5. **Auto-tidy** (button): runs rules 1–5, shows a diff of what changed; never silent.
6. **Validate**: live panel (gaps, overlaps, off-wall doors, unreachable zones, missing portals), click to jump.
7. **Route test**: pick two zones, show shortest path and length.
8. **Export** all artifacts.
Also: suggestion layer (rule-based proposals; accept/reject per item) and notes/comments pins, as in the redline page.

## Optional later: assisted tracing
Browser-side vectorization of the underlay (wall detection, door arcs) to pre-draw candidate zones; everything remains reviewable. Optionally an LLM call with an API key provided by the zoning author. Out of scope for v1.

## Milestones
1. Scaffold + project model + SVG canvas + underlay + calibration.
2. Drawing/editing tools + snapping + undo/redo.
3. Port geometry rules (coverage, doors, blocks, nested) + validator.
4. Routing graph + route tester.
5. Exports + import of existing JSON (load BFW fixture).
6. Style panel, suggestions/notes, polish, docs, GitHub Pages workflow (Actions).

## Acceptance tests
- Load `connectivity-graph-fixed.json` + `routing-graph-fixed.json`: app reproduces 193 zones, 219 portals, 0 overlaps, one component.
- Sample routes match reference: `E.01→E.52` 112.8 m, `E.72a→E.62` 123.9 m, `E.90→E.60a` 80.1 m, `E.34→E.41a` 73.8 m, `E.33a→E.02` 75.4 m (tolerance ±0.5 m).
- Exported JSON validates against `graph_format.md`; SVG ids match JSON.
- Unit tests for every rule in "Core rules"; visual regression on the BFW fixture.
- Works offline after first load; no network calls.

## Out of scope for v1
Multi-floor stitching (design the model with `floor` and stair/lift links so it can be added), accounts, real-time collaboration, native apps.
