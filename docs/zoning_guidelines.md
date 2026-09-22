# Wegweiser — Zoning guidelines

How floor plans become zones, portals and obstacles, authored as one semantic SVG per floor.

The plan and the route overlay live in the same `viewBox`, so they cannot drift apart. That is what one asset serving both consumers buys, and it is why the rules below are non-negotiable.

## Data Model: Zones and Portals

The asset encodes the zones and portals fixed by `axioms.md`, which supersedes the flat coordinate lists currently hardcoded in `src/main.py`:

| Concept | SVG carrier | Meaning |
| :--- | :--- | :--- |
| Zone | `<polygon>` / `<rect>` / `<path>` with `id`, `data-kind`, `data-label` | A space: room, corridor, hall, stairwell, or service area |
| Portal | `<circle>` with `id`, `data-a`, `data-b` | A boundary between **exactly two** zones; carries the routing coordinate |
| Obstacle | shape with `data-zone` | A non-walkable fixture inside a zone: counter, booth, seating, atrium void |
| Exterior | reserved zone id `aussen` | Building egress; anchors entrances |
| Floor link | `data-kind="stairs"` / `elevator` | Vertical transition, weighted separately |

Only the portal record is authored. The zone index (zone → its portals) and the segment list (all portal pairs within a zone) are **derived by inversion** (axioms 5–6) and must never be written by hand.

**Axiom 4 is the zone test:** within a zone, every portal must be reachable by an unhindered path from every other. If it is not, it is not one zone — split it with a virtual portal. This is the only rule needed for data entry; no zone categories are required.

A portal need not be a door. A doorless opening, or a line drawn across a corridor at a corner, is equally a portal. Two portals between the same pair of zones are kept separate only when the choice between them changes a route — adjacent double doors merge into one.

`data-kind` doubles as the accessibility filter for step-free routing: excluding `stairs` requires no separate graph.

Multi-floor: one `<g id="floor:eg">` per floor, toggled by CSS. Vertical portals connect them.

## Authoring Contract (non-negotiable for parseability)

1. **Zero transforms on routing groups.** `#zones`, `#portals` and `#obstacles` must have no `transform` attribute; coordinates are absolute in `viewBox` space. Presentation padding belongs in CSS or an outer wrapper, never on data groups.
2. **Layer separation by group id:** `#shell`, `#zones`, `#portals`, `#obstacles`, `#labels`, `#decor`, `#legend`. Only the first four are parsed; `#legend` and `#decor` are stripped or CSS-hidden in the kiosk build.
3. **Stable ids** per the naming conventions below. Zone ids are printed room numbers (`E.54a`, `R.58`) or lowercase ASCII slugs (`flur_nord`, `atrium`); `aussen` is reserved for the exterior; portal ids are sequential (`p01`) and must not be renumbered once published. Labels are German as printed on the plan.
4. **Every portal references exactly two existing zone ids** via `data-a` / `data-b` (or the reserved `aussen`), and never the same zone twice. Dangling references fail the build.
5. **Every zone has at least one portal**, and its two zones must share a wall, not merely a corner.
6. **No metadata blobs.** Strip C2PA / editor metadata before the file enters `web/assets`.
7. **Uniform `viewBox` per floor** so multi-floor layers stack without rescaling.

The contract is machine-checked by `validate_plan.py`, which additionally verifies axiom 4 (zone convexity as a proxy for unhindered reachability), axiom 1 (no overlapping zones), and graph connectivity.

## Naming conventions in data

- Zone ids: room number as printed (`E.54a`, `R.58`) or a lowercase ASCII slug (`flur_nord`, `atrium`). Exterior is `aussen`.
- Portal ids: sequential (`p01`, `p02`).
- Labels: German, as on the plan (`Unterricht`, `Besprechungsraum`).

## Duplicate portals

Two portals between the same pair of zones are worth keeping separate only if they are far enough apart that the choice between them changes a route. Adjacent doors → one portal. Doors at opposite ends of a corridor → two.

## Phase A — Hybrid AI Vectorization (current)

Tool: **Claude Design**, operated in supervised hybrid mode.

1. Submit the source material (emergency plan photo, `Lageplan EG` PDF) with the authoring contract above as explicit instructions.
2. The model emits a schematic SVG: simplified geometry, wall thickness, door leaves, furniture and dimensions removed; zones and portals tagged.
3. **Human supervision is mandatory and is the quality gate.** Verify against the source: room numbering, adjacency correctness, portal placement at real door positions, corridor connectivity, missing rooms.
4. Correct by direct SVG edit or by iterating with the model; normalize transforms, strip metadata and chrome.
5. Commit the reviewed floor SVG to `web/assets`.

Source hierarchy: the `Flucht- und Rettungsplan` (2026) supersedes the `Lageplan EG v1.2` (2018) wherever they disagree — room numbering has drifted and the personal names on the older plan are stale. The Lageplan remains authoritative for wing layout and overall geometry.

Architectural door notation matters when reading the source: a door is a line plus a quarter-circle arc. Solid black blocks are wall thickness, not doors — misreading them produces doubled portals.

Rationale: this collapses the former "trace walls, then place nodes, then transcribe coordinates" sequence into a single supervised pass, and it scales to further floors and wings without per-floor manual drafting.

Residual risk: the model infers geometry it cannot read from a blurry source. Mitigation is review discipline, not tooling — every zone and portal is checked against the official plan before it is trusted for routing.

## Floor plan work

Source hierarchy established:

- **Lageplan EG v1.2 (2018)** — geometry, room numbers, wing layout.
- **Flucht- und Rettungsplan B 7967_059 (07.05.2026)** — door positions at usable fidelity, current room use. Supersedes the Lageplan where they disagree: room numbering has drifted, and the personal names on the 2018 plan are eight years stale.
- The Rettungswege drawn on those plans are professionally-drawn movement lines.

A schematic SVG of the east block was produced, then redrawn in Claude Design to the same markup contract: `<g id="zones">` with `data-kind` and `data-label`, `<g id="portals">` with `data-a` and `data-b`. The contract makes the portal record a one-pass parse of the drawing.

**Corrections that landed across iterations:**

- WC vestibules modelled as separate zones — you pass through a Vorraum to reach a WC.
- The wing boundary made explicit as an `anschluss` zone.
- Doorless portals drawn as dashed boundaries, derived from axiom 4 without being named.
- Architectural door notation clarified: a line plus a quarter-circle arc. Solid black blocks are wall thickness, not doors. This fixed the doubled portals.
- Adjacent double doors merged into one portal.
- Non-room partitions demoted from zones to obstacles.

**Open at end of session:** `E.56c` non-convex (0.855); `TR9` with a single portal, implausible for a Treppenhaus on an escape plan; E.52/Wachdienst overlap pending the obstacle conversion.
