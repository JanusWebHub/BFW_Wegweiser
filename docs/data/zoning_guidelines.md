# Zoning guidelines

How the architectural plan and the emergency plans of one floor become the simplified floor plan SVG and the connectivity graph. The connectivity graph format is defined in `graph_format.md`.

## Sources

- Lageplan BFW BB_Charlottenburg, Erdgeschoss/EG, Version 1.2, Stand 23.01.2018: building outline, wing shapes, scale. For the middle area (Speisesaal, `E.48`, `E.49`, `E.53.1`, `E.53.2`, the rooms numbered `E.56` and `E.56a` there, Infodienst, the corridor to the north-west wing) it is the only source; room numbers there are unverified.
- Flucht- und Rettungspläne B 7967_052 to B 7967_061, 07.05.2026: room division, walls, doors, room numbers, labels, exits. Where they disagree with the Lageplan, they apply.
- The emergency plans are photos, taken at an angle and rotated differently; they do not decide outline or scale.
- Every discrepancy between the sources is listed in the report and decided by the human supervisor.
- Personal names on the plans are not used.

## Known corrections

- The two Büros printed `E.59a` and `E.59b` on the emergency plans are `E.60a` and `E.60b`. The Elt room at the corridor stays `E.59b`.
- The large hexagon room above `E.80` and the room labelled `E.84` are one room, `E.84`.

## Reading the plans

- A door is a line plus a quarter-circle arc. Solid black blocks are wall thickness, not doors.
- A doorless opening between two spaces is read like a door.
- Wall thickness, door leaves, furniture, fixtures and dimensions are dropped.

## Zones

- Zones are drawn fine; merging is decided later.
- Every numbered room is one zone, including the kitchen rooms `E.41a` to `E.41i`.
- Every unnumbered space is one zone: anterooms (VR, Vorraum), technical and storage spaces, lifts, Foyer, Speisesaal, Durchgang, Infodienst, Terrasse.
- `E.53.1` and `E.53.2` are two zones joined by a virtual portal.
- Halls and corridors are split into roughly convex zones, so that a straight line between any two portals of a zone stays inside it. Splits go at corners, junctions and where a hall narrows.
- A room enclosed by another room is cut out of the outer zone as a hole.
- Zones cover the inside of the shell without gaps or overlaps. Neighbouring zones share their boundary exactly, along the centre line of the wall between them.
- The exterior is one zone, `exterior`, and is not drawn.
- Obstacles and movement lines are not drawn.

## Crossability

- Crossable: corridors, Durchgang, Foyer, Vorraum and anterooms, stairwells, lifts, Speisesaal, Terrasse, and `E.52`.
- Non-crossable: all other rooms and spaces.
- A room that is the only access to another room is crossable, e.g. `E.41`.
- Every room made crossable is listed in the report.

## Portals

- A portal joins exactly two zones that share a boundary, not only a corner.
- A door or doorless opening becomes one portal, with its point at the midpoint of the opening.
- Adjacent double doors are one portal. Two openings between the same zones that are far enough apart to change a route are two portals.
- Where a hall or corridor is split, the whole shared boundary is one virtual portal, with its point at the midpoint of the boundary.
- Every door marked Notausgang on the emergency plans is a portal to `exterior` with `emergency_exit: true`, including exits from stairwells.
- The Haupteingang is a portal to `exterior` with `main_entrance: true`.
- Notausstiege (escape windows) are not portals.
- No vertical portals while only one floor is drawn.
- Every zone has at least one portal.

## Ids

- Numbered rooms: the room number as printed, e.g. `E.62`, `E.54a`, `E.53.1`, `R.58`.
- Stairwells: `E.` plus the printed number, `E.TR1` to `E.TR9`.
- Unnumbered spaces: `E.` plus a lowercase ASCII name with `-` between words and `ae`, `oe`, `ue`, `ss` for umlauts and ß:
  - corridors after the stairwell of their wing: `E.flur-tr1`
  - lifts after the stairwell next to them: `E.aufzug-tr7`, or after a room next to them if no stairwell is near: `E.aufzug-e41`
  - anterooms after the rooms behind them: `E.vr-e54`
  - technical and storage spaces after their use and the nearest stairwell or room: `E.technik-tr5`, `E.lager-tr3`, `E.lueftung-e41`
  - large spaces after their printed name: `E.foyer`, `E.speisesaal`, `E.durchgang`, `E.vorraum-e50`, `E.infodienst`, `E.terrasse`
- Where two spaces would get the same id, `-a`, `-b`, … are appended, e.g. `E.aufzug-tr2-a`, `E.aufzug-tr2-b`.
- A space split into several zones gets `-1`, `-2`, … appended, counted from the nearest junction outwards: `E.flur-tr1-1`. No other word of a name is only digits.
- Zone ids contain no `_`.
- Portals: the two zone ids sorted by character code and joined by `_`, e.g. `E.62_E.flur-tr9-1`, `E.52_exterior`. A second portal between the same zones gets `_2`.
- Labels: German, as printed on the plan.

## SVG markup

- One SVG per floor with `viewBox="0 0 W H"` and `width`/`height` equal to W and H. Later floors use the same viewBox and origin, so that floors stack.
- Absolute coordinates, no `transform` anywhere, no editor metadata.
- Top-level groups in this order: `shell`, `zones`, `portals`, `labels`. Nothing else.
- `shell`: the building outline, for display.
- `zones`: one `polygon`, `rect` or `path` per zone with `id="zone-<zone id>"` and `data-label="<label>"`. A zone with a hole is a `path` with `fill-rule="evenodd"`.
- `portals`: one `g` per portal with `id="portal-<portal id>"`, containing a `line` along the crossable section of the boundary and a `circle` at its midpoint. Virtual portals have `class="portal virtual"` and a dashed line; all others `class="portal"`.
- `labels`: room number and label per zone as `text`, for display.
- `class` attributes set appearance only. Colours and fonts live in one `style` element inside `defs`.
- The `zone-` and `portal-` prefixes are needed because an XML id cannot start with a digit.

## Scale

The Lageplan has no scale bar and no dimensions, but prints the area of many rooms. `units_per_meter` is the square root of a rectangular room's area in SVG units² divided by its printed area in m². At least two rooms in different wings are measured; the value is written into the floor entry of the connectivity graph.

## Checks before delivery

- Every zone and portal in the connectivity graph has exactly one element in the SVG, and every zone and portal element in the SVG has an entry in the connectivity graph.
- Each portal's `point` equals the centre of its circle, and the circle sits at the midpoint of its line.
- Each portal line lies on the boundary shared by its two zones.
- Zones have no gaps or overlaps inside the shell.
- The connectivity graph satisfies the validity rules in `graph_format.md`.

## Report

Everything not read directly from the sources:

- every discrepancy between the Lageplan and the emergency plans
- room numbers taken only from the Lageplan
- unreadable or conflicting room numbers and labels
- assumed doors and openings
- rooms made crossable
- the rooms and areas used to measure `units_per_meter`, with the resulting values
