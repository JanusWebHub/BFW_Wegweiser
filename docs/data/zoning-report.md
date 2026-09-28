# Zoning report — BFW Berlin-Brandenburg, Charlottenburg, EG

Outputs: `bfw-eg.svg`, `connectivity-graph.json` (floor `E`, `provenance: unverified`), this report.

## Step 1 — Skeleton, whole EG

### Frame and method

- Geometry was traced from the Lageplan EG v1.2 (23.01.2018). The PDF is a single scan, stored upside down; it was turned 180° and read at half its native resolution (1754 × 1240 px). SVG coordinates = scan px − (40, 77). `viewBox="0 0 1790 1000"`. Later floors must use the same frame.
- The emergency plans B 7967_052–061 were used to decide which spaces are circulation and where they end. They were not used for outline or scale. Photo to plan: 058 = WA0009, 059 = WA0008, 055 = WA0006, 057 = WA0007, 056 = WA0001, 060 = WA0000, 061 = WA0003, 052 = WA0005, 053 = WA0004, 054 = WA0002.
- `shell` contains the building outline (`shell-outline`) and eight wing shapes (`wing-1` … `wing-8`, numbered in the order of the brief). They are for display only.
- Step 1 contains 37 zones: 9 stairwells, 26 corridor zones, `E.durchgang` and `E.foyer`. It also contains 21 virtual portals. It has no doors, exits or rooms.

### units_per_meter

Inner rectangle in SVG units, measured on the Lageplan, compared with the printed area:

| Room | Wing | w × h (units) | printed m² | units/m |
| --- | --- | --- | --- | --- |
| E.90 | 4 NW | 84.3 × 96.7 | 66.09 | 11.11 |
| E.91 | 4 NW | 98.3 × 97.0 | 77.50 | 11.09 |
| E.62 | 1 East | 59.0 × 67.5 | 30.27 | 11.47 |
| E.59 | 1 East | 56.0 × 66.0 | 30.39 | 11.03 |
| E.60 | 1 East | 113.0 × 67.0 | 65.32 | 10.77 |

Mean 11.09, spread 10.77–11.47 (±3 %). Value used: **`units_per_meter = 11.1`**. Cross-check: with this value the Terrasse polygon covers 146 m² (printed: 142 m²).

### Zones drawn

| Zone | Where |
| --- | --- |
| `E.TR1`, `E.flur-tr1-2`, `E.flur-tr1-1` | Long wing (052): stairwell at the end, widened end of the corridor, straight corridor down to the junction |
| `E.flur-tr2-1` … `-4`, `E.TR2` | Junction at TR2 (052/053): hub, two pieces of the passage between TR2 and E.21, and the corridor towards the hexagon (with E.71) |
| `E.flur-tr3-1`, `E.TR3` | IQ + UKM corridor (053) |
| `E.flur-tr4-1` … `-4`, `E.TR4` | Hexagon (054): waist centre, waist east, Notausgang triangle, corridor between the TR4 core and the E.72 rooms |
| `E.flur-tr5-1` … `-4`, `E.TR5`, `E.durchgang`, `E.flur-tr6-1`, `E.TR6` | North-west wing (060/061) |
| `E.flur-tr7-1` hub, `-2` south strip, `-3` corridor beside the Terrasse, `-4` corridor to the NW wing, `E.foyer`, `E.TR7` | Entrance / Foyer (055/057), plus the middle corridor |
| `E.TR8`, `E.flur-tr8-1` … `-3` | Kitchen (056) |
| `E.flur-tr9-1` hall, `-2` east corridor, `-3` corridor along E.56/E.57, `E.TR9` | East block (058/059) |

### Virtual portals

All 21 portals are corridor splits: the whole shared boundary, with the point at its midpoint. The ids are:
`E.durchgang_E.flur-tr5-1`, `E.durchgang_E.flur-tr6-1`, `E.flur-tr1-1_E.flur-tr1-2`, `E.flur-tr1-1_E.flur-tr2-1`, `E.flur-tr2-1_E.flur-tr2-2`, `E.flur-tr2-1_E.flur-tr3-1`, `E.flur-tr2-2_E.flur-tr2-3`, `E.flur-tr2-4_E.flur-tr4-2`, `E.flur-tr4-1_E.flur-tr4-2`, `E.flur-tr4-1_E.flur-tr4-3`, `E.flur-tr4-1_E.flur-tr4-4`, `E.flur-tr5-1_E.flur-tr5-2`, `E.flur-tr5-1_E.flur-tr5-4`, `E.flur-tr5-2_E.flur-tr5-3`, `E.flur-tr7-1_E.flur-tr7-2`, `E.flur-tr7-1_E.foyer`, `E.flur-tr7-2_E.flur-tr7-3`, `E.flur-tr7-2_E.foyer`, `E.flur-tr8-1_E.flur-tr8-2`, `E.flur-tr8-2_E.flur-tr8-3`, `E.flur-tr9-1_E.flur-tr9-2`.

Some circulation zones meet at a door, not an open split. These portals are left for the portal steps:

- `E.flur-tr2-1` / `E.flur-tr7-3`: fire door, Lageplan
- `E.flur-tr7-1` / `E.flur-tr9-3`: double door at x ≈ 1050 (scan 1090)
- `E.flur-tr9-3` / `E.flur-tr9-1`: fire door, 058
- both ends of `E.flur-tr7-4`
- `E.flur-tr2-3` / `E.flur-tr2-4`: double door, Lageplan and 053

### Discrepancies, assumptions and readings (for decision)

1. **E.63 east edge.** The scan is cut and smeared at the right edge. The E.61/E.63 end wall is extended along its visible slope to the top edge of E.62/E.63. This gives E.63 ≈ 103 m² (printed 102.10). The vertex at (1747, 468) is extrapolated.
2. **TR2.** The Lageplan shows a "Treppenhaus" vestibule: a pentagon with a slanted narrow box on its east side, with doors to the long corridor, the hexagon corridor and the hub. 052 and 053 show TR2 as a stair with a Flur passing between it and E.21, joining the hexagon corridor to the long corridor. Drawn: the Lageplan outline, split into `E.TR2` (stair, including the slanted box) and a two-piece passage along E.21 (`E.flur-tr2-2`, `-3`). The passage's opening to the hub is short (~1.8 m), where the Lageplan has a door. Its width and the stair's extent are my best reading.
3. **North-west wing, west end.** The Lageplan (2018) shows E.68 across the whole west end, with the Treppenhaus inside it. 060/061 (2026) show the Flur continuing along the south wall to TR5, then turning north past Technik/Elt-Vert/Aufzug to TR5, beside E.70a/E.70b. Drawn: `E.flur-tr5-2` extended west to E.70a, and the stub `E.flur-tr5-3` up to TR5. `E.TR5` is the Lageplan Treppenhaus box, widened to the outer wall (060 shows TR5 reaching the outer wall).
4. **Durchgang.** On 060 the label sits at the junction where the corridor from the middle area enters and the corridor steps. Drawn: the step between the two parts of the NW corridor, east of the junction square (x 1112–1177). The junction square itself (`E.flur-tr5-1`) is drawn as Flur. The boundary between Durchgang and junction is assumed open (the green route on 060 passes through). The Lageplan line at that position may be a wall.
5. **Short corridor north to E.66a.** Drawn as `E.flur-tr5-4`. It has no stairwell of its own, so it is numbered in the TR5 series.
6. **Corridor from the middle area to the NW wing** (Lageplan only). No stairwell lies in the middle area. It is named `E.flur-tr7-4` because it hangs off the TR7 hub. It could be renamed if you prefer.
7. **Corridor along E.56/E.57** (`E.flur-tr9-3`). It is shown on both 058 and 055, so it belongs to the earlier wing (1) and is named in the TR9 series. It is separated from the hub `E.flur-tr7-1` by the double door and from the hall `E.flur-tr9-1` by the fire door.
8. **Foyer and Flur.** The Lageplan shows one open "Flur" between E.53.2, the Terrasse, E.50a/b and Vorraum. 055/057 split it into a furnished Foyer on the Terrasse side and a Flur on the south and east. Drawn: `E.foyer` bounded east at x 905 and south at y 545, with virtual portals to `E.flur-tr7-1` (east) and `E.flur-tr7-2` (south). The exact Foyer edge is not drawn on the plans; I read it from the change in shading.
9. **Hub / south strip link.** Because the Vorraum juts into the space, `E.flur-tr7-1` and `E.flur-tr7-2` share only a 12-unit (≈1.1 m) boundary. Most routes will pass through the Foyer.
10. **Hexagon.** 054 shows one continuous Flur: the waist between the hexagons, the triangle to the Notausgang, and the corridor beside the TR4 core. It was split into four convex zones. The corridor between the core and E.72 follows the Lageplan walls. 054 shows E.72 split into E.72a/b/c (rooms, step 2).
11. **Kitchen.** The unlabelled Lageplan area between the Treppenhaus and the Aufzug (x 910–950, y 789–829) is given to `E.TR8`. The strip in front of TR8 and the Aufzug is `E.flur-tr8-1`. 056 shows it as a small "Flur"; its extent is my reading.
12. **TR7** is the triangle between the two diagonal walls under the corridor beside the Terrasse. The Aufzug area inside the triangle is left out for step 2. On the Lageplan the door on its north side (x ≈ 820–840) opens into TR7, as does the TR7 door on 055/057.
13. **TR6, TR9.** TR6 follows the stepped east end on the Lageplan. TR9 is the Lageplan Treppenhaus trapezoid.
14. **Lift beside TR8.** On the Lageplan and on 056 it sits outside the wall line. It is included in the shell now, so that the shell does not change in step 2.
15. **Terrasse.** The Terrasse is inside the shell. Its north edge (y 470) is not drawn on the Lageplan. It is taken from 057 (double line) and checked against the printed 142 m².
16. **Wing shapes** are approximate, for display only. They are placed at E.56/E.56a vs. E.56b/E.56c (x 1060) and between Wachdienst and E.51 (x 1093). They do not decide which wing a room belongs to.
17. **For later steps (not drawn yet):**
    - Lageplan "Infodienst" vs. 055/058 "Wachdienst" + "E.51 Pförtner" in the same place.
    - Lageplan E.56 / E.56a vs. 058 E.56c / E.56b.
    - Lageplan E.58 "Tagungsraum" vs. 058/059 "R.58 Konferenzraum".
    - Lageplan "Wartebereich Empfang" vs. 2026 "E.52 Eingangsbereich/Rezeption".
    - Lageplan E.59a/E.59/E.60 vs. 058 E.59 / E.59a / E.59b (i.e. E.60a / E.60b by the known correction).
    - The renumbered long wing and IQ + UKM wing (e.g. Lageplan E.28 "Kopierer" vs. 053 E.23 "Kopierer").

### Checks after step 1

- Every zone and portal in the graph has exactly one SVG element, and every SVG zone or portal element has an entry in the graph: 37 zones plus `exterior`, and 21 portals.
- Each portal `point` equals its circle centre and the midpoint of its line.
- Each portal line lies on the boundary shared by its two zones (checked numerically, tolerance 0.6 units).
- Sampling every 2 units found no overlaps between zones. All zones lie inside the shell.
- Gaps: rooms are not drawn yet, so the rest of the shell is intentionally empty.
- Roughly convex:
  - All corridor zones pass, apart from small bends at the E.26 corner of `E.flur-tr2-1` (1–2 units) and at `E.flur-tr9-1` / `E.flur-tr4-4`.
  - The stairwells `E.TR2`, `E.TR6` and `E.TR7` are not convex (TR7 because the Aufzug is cut out).
- Validity rules: met, except "every zone has at least one portal". These zones have no portal yet, as the brief allows:
  - all nine stairwells
  - `E.flur-tr7-4` and `E.flur-tr9-3` (reached only through doors)
  - `exterior`
