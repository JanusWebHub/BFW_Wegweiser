# Handoff: Wegweiser graph design and EG zoning

State on 2026-09-29. Numbers come from Claude Design messages and the Copilot review report; they have not been re-verified. Authoritative specs are docs/design/graph_format.md and docs/design/zoning_guidelines.md; this file only summarises them and records decisions and state.

## Model

- Adjacency graph (deferred): spaces and separators from architectural plans.
- Connectivity graph: zones (nodes) and portals (edges), made alongside the simplified semantic SVG.
- Routing graph = connectivity graph + routing config. Segments are computed: in each crossable zone, a straight line between every pair of portals; distance is line length over units_per_meter. Non-crossable zones have none.
- One zone `exterior`, no floor. Vertical portals (stairs, lifts) join floors, deferred while only EG exists.
- Costs are per direction, default 0. Variants are named lists of extra non-crossable zones. Climbing effort is a state cost.
- Search: start and target must differ; only intermediate zones must be crossable; "unreachable" is valid; cost = segment distances + segment extra costs + state extra costs.
- Ids: zone = room number as printed (E.62, R.58) or lowercase name with `-` (E.flur-tr9-1); split zones `-1`, `-2`; name clashes `-a`, `-b`; no `_` in zone ids. Portal = both zone ids sorted, joined by `_` (`_2` for a second). Keys use `|`. SVG ids `zone-<id>`, `portal-<id>`.
- Portal flags: virtual; emergency_exit and main_entrance only on portals to exterior.
- Files: connectivity-graph.json, routing-config.json, routing-graph.json in data/ (committed); demos in src/fixtures/.
- Deferred: adjacency graph format, movement lines, obstacles, walked-distance realism, rulebook additions (floors, vertical portals), units_per_meter from the SVG, Notausstieg (possible later variant, undecided), merging anterooms.

## Sources for EG

- Lageplan 2018 (v1.2, Stand 23.01.2018, scan, no scale bar): outline, wing shapes, scale; only source for the middle area.
- Rettungspläne B 7967_052 to 061 (07.05.2026, photos): room division, walls, doors, numbers, labels, exits; not for geometry. Where they disagree with the Lageplan they apply; every discrepancy goes to the report for the user.
- Frame: viewBox 0 0 1790 1000, SVG = scan px minus (40, 77), units_per_meter 11.1 (five rooms, range 10.77 to 11.47).
- Known corrections: the Büros printed E.59a/E.59b are E.60a/E.60b (checked by the user). The hexagon room above E.80 and the room labelled E.84 appear to be one room, E.84; not yet checked by the user.

## Zoning decisions

- Draw fine, merge later (merging is an open, important decision). Every numbered room, anteroom, technical space is its own zone. Corridors named by wing-end stairwell (E.flur-tr1-1), lifts after their stairwell, stairwells E.TR1 to E.TR9.
- Crossable: circulation, anterooms, stairwells, lifts, E.speisesaal, E.terrasse, E.52, plus rooms that are the only access to another room (E.41, R.58). E.68 and E.66 were made crossable by Claude Design's readings (open decision 4). Rest non-crossable; each exception listed in the report.
- E.53.1 and E.53.2: two zones, virtual portal. Infodienst = Wachdienst (confirmed).
- Exits: every Notausgang and the Haupteingang is a portal to exterior. Notausstiege left out.
- SVG: groups shell, zones, portals, labels; portal = line plus midpoint circle, virtual dashed; no transforms; one style element in defs.

## Pipeline and progress

Claude Design drew the SVG and JSON from the Lageplan and photos in stop-gated steps: 1 skeleton, then per wing 2.N rooms and 3.N portals (wings 1 east block, 2 entrance/foyer, 3 kitchen, 4 north-west, 5 long wing, 6 IQ+UKM, 7 hexagon, 8 middle area), then merge and cross-wing check. The user approved steps 1 to 3.2 in order. Wings 3 to 7 were run in parallel sessions from the same base (messages docs/design/parallel-message-wing*.md) and each returned files under docs/data/steps-2.N-3.N/; no approval of their outputs or of the step 8 merge is recorded.

Result per wing (zones, portals added): 3 kitchen 15/30; 4 north-west 20/26; 5 long wing 39/36; 6 IQ+UKM 8/10; 7 hexagon 18/21.

Copilot review (docs/data/copilot-report.md, scripts in docs/utilities): all mechanical checks pass, no base content changed, merge simulation gave 164 zones and 179 portals. C2PA blocks were stripped from the five wing SVGs.

Step 8 and merge (docs/data/step-8-and-merge): Claude Design produced the merged EG, reportedly 171 zones and 206 portals (the message does not say whether exterior is counted; an earlier message said 169 zones plus exterior and 201 portals), provenance unverified, every zone has a portal and is reachable from the exterior. Middle area was redone with the Lageplan attached: E.53.1, E.53.2, E.56a, E.48, E.49, E.speisesaal (crossable by assumption, only link to TR8 and the kitchen). All middle-area doors are assumed from shared walls. Over crossable zones only, E.33a is unreachable (behind office E.33).

Known tooling problem: Claude Design's environment strips the style element on save and inserts a C2PA metadata block. The stylesheet is delivered separately as bfw-eg-style.txt (step 8). Copilot found two other styles: a warm one in docs/data/bfw-eg.svg and a green one in docs/data/steps-2.5-3.5/bfw-eg-style-2.5-3.5.txt. The step 8 file was not compared with them. The style choice is open.

## Open decisions for the user

1. E.flur-tr3-1 is offset from the real corridor by up to about 22 units; wing 5 and 6 rooms and portals depend on it.
2. About 5.6% of the wing 6 shape is unclaimed (room west of E.71, unlabelled area east of it, Lager triangle E.lager-tr3).
3. Skeleton proposals: E.41 open to the corridors (perhaps one space); extend E.flur-tr8-3 to y 941; split E.flur-tr5-2 at the fire door x 877; extend E.flur-tr4-3 and -1 to the wall and close shell hairline gaps.
4. Room identity and crossability guesses: E.23, E.27, E.28 numbers differ between Lageplan and 052/053; E.66 crossable only if the E.67a opening belongs to it; E.82 and E.83 crossable on the guess that E.82a and E.83a open into them (E.74 is crossable as the only access to E.73); E.technik-tr4-a/-b are placeholders; E.84 hexagon room.
5. Exits: least certain E.41b_exterior; TR1, TR3, TR6 and Durchgang exits placed from signs only; TR2, TR4, TR8 have signs but no readable outer door.
6. Many doors are assumed (reports list them). At merge Claude Design added assumed doors for E.23, E.27, E.28, E.30, E.vr-e25, E.37, E.abstell-e37 (one message counts 8 doors, the other names these seven rooms).
7. On-site checks flagged in earlier steps: TR2 passage, Durchgang position, Foyer edge, E.62 second door into R.58, E.56b, E.59b Elt, E.50b and lift doors, closed Terrasse to Foyer wall, stair symbol at R.58, Beh. WC (own zone or part of E.50b).
8. Claude Design asked whether room splits should follow the 2018 Lageplan instead (E.59a/E.59/E.60, E.56 vs E.56b/c, E.72 vs E.72a/b/c, E.68 vs E.68a/b). Claude Design kept the 2026 splits and asked; no answer is recorded. The guidelines say the escape plans apply.
9. Middle area still Lageplan-only; the user plans to photograph it.
