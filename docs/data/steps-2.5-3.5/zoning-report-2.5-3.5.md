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

### Changes after approval

- The SVG metadata block has been removed. The file now starts with `<defs><style>`, and all colours and fonts live in that one style element. It had been written without either by mistake; the geometry is unchanged.
- The readings above are unchanged; TR2, the Durchgang and the Foyer edge will be checked on site.

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

## Step 2.1 — Rooms, east block (B 7967_058, B 7967_059)

The skeleton is unchanged. 18 zones were added. Room division and labels follow 058/059 (2026); outlines follow the Lageplan walls.

| Zone | Label | Crossable | Note |
| --- | --- | --- | --- |
| `E.56b` | – | no | No label printed on 058/059 |
| `E.56c` | Unterricht | no | L-shaped; wraps around E.56b |
| `E.57` | Unterricht | no | |
| `R.58` | Konferenzraum | **yes** | Only access to E.58a |
| `E.58a` | Techn. | no | |
| `E.54a` | WC D | no | |
| `E.vr-e54a` | VR | yes | Anteroom |
| `E.54b` | WC H | no | |
| `E.vr-e54b` | VR | yes | Anteroom |
| `E.62` | Unterricht | no | |
| `E.63` | Unterricht | no | East edge extrapolated (step 1, item 1) |
| `E.61` | Werkstatt | no | |
| `E.60a` | Büro | no | Printed `E.59a` (known correction) |
| `E.60b` | Büro | no | Printed `E.59b` (known correction) |
| `E.59` | Besprechungsraum | no | |
| `E.59b` | Elt | no | See item 6 |
| `E.wachdienst` | Wachdienst | no | |
| `E.52` | Eingangsbereich/Rezeption | yes | Crossable by the guidelines |

Rooms made crossable in this step: `R.58`, because the only door of `E.58a` opens into R.58 (058, 059). `E.52` and the two VRs are crossable by category.

### Discrepancies, assumptions and readings (for decision)

1. **E.56b / E.56c vs. Lageplan E.56.** The Lageplan has one room, E.56 (71.96 m², "Center RVL"), between E.56a and E.57. 058 shows E.56c and E.56b in that place. The left edge of 058 is a cut line, so the west extent of E.56b is not shown. Drawn: both rooms inside the Lageplan outline of E.56. E.56b runs to the Lageplan wall between E.56 and E.56a (x 1060), and its outline around E.56c is read from 058. If this is right, the Lageplan room E.56 no longer exists, and step 2.8 has only E.56a in that row.
2. **E.57, E.62, E.63, E.61** keep their Lageplan outlines and numbers.
3. **R.58 vs. Lageplan E.58.** The Lageplan prints E.58 "Tagungsraum" (120.70 m²); 058 and 059 print R.58 "Konferenzraum". The id follows the emergency plans.
4. **E.58a, E.54a, E.54b and the VRs.**
   - 058/059: E.58a Techn. above E.54a WC D, with a VR below. E.54b WC H has its own VR below.
   - Lageplan: E.54a and E.54b in the same two columns. The Techn. space at the top of the first column is unlabelled there, and the two anterooms are drawn as one strip with two doors.
   - Drawn: the 2026 order, in the Lageplan columns.
5. **E.59 / E.60a / E.60b.**
   - The Lageplan shows three rooms: E.59a ID, E.59 ID and E.60 (Umbau für RVLi, 65.32 m²).
   - 058/059 show three different rooms: E.59 Besprechungsraum, then two Büros printed E.59a and E.59b, i.e. E.60a and E.60b by the known correction.
   - Drawn:
     - E.59 as the Lageplan E.59a and E.59 combined, bounded by the E.52 diagonal.
     - E.60a and E.60b as the Lageplan E.60 split in half (x 1395 / 1451 / 1508). 058 draws them about equal in width.
6. **E.59b Elt.** On 058 and 059 the Elt room is at corridor level. It lies between the E.52 diagonal and the east hall, between the line of the E.56/E.57 corridor wall and the hall's south wall. That spot is inside the approved zone `E.flur-tr9-1`. The Lageplan shows open hall there. To keep the skeleton unchanged, Elt is drawn in the north-west corner of E.59, directly below that spot (SVG x 1275–1322, y 563–587). **Proposal:** cut Elt out of `E.flur-tr9-1` (SVG triangle about (1313,529)–(1335,529)–(1335,563)–(1291,563)) and give that area back to E.59. This needs your approval because it changes the skeleton.
7. **Wachdienst vs. Lageplan "Infodienst".** The Lageplan Infodienst box between the corridor and the ramp matches the Wachdienst on 058/059 (and 055). Drawn: Wachdienst = the Infodienst outline east of its diagonal west wall. The part west of that wall is E.51 Pförtner (055, step 2.2). Infodienst is not drawn as a zone of its own. Please confirm that Infodienst and Wachdienst are the same room, so the middle-area step does not draw Infodienst again.
8. **E.52 vs. Lageplan "Wartebereich Empfang".** E.52 is the Wartebereich plus the ramp area south of Wachdienst, down to the south wall with the Haupteingang. Its west edge is the diagonal wall continuing from Wachdienst down to the Speisesaal (Lageplan). The ramp, the Erste-Hilfe point, the counter arc and the black wall blocks are fixtures or wall thickness and are dropped.
9. **E.63 / E.61 east end.** Same extrapolation as step 1, item 1.

### Changes after approval

- **E.59b Elt** is now cut out of `E.flur-tr9-1` where 058/059 show it: SVG (1313,529)–(1335,529)–(1335,563)–(1291,563). That corner goes back to `E.59`. This skeleton change was approved. The portal `E.flur-tr9-1_E.flur-tr9-2` is unaffected.
- Confirmed by the supervisor:
  - E.56b and E.56c lie inside the old Lageplan E.56.
  - Wachdienst and the Lageplan "Infodienst" are the same room, so Infodienst is not drawn in the middle-area step.

### Checks after step 2.1

- Every zone and portal has exactly one SVG element and one graph entry: 55 zones plus `exterior`, and 21 portals.
- The existing portals are unchanged and still lie on their shared boundaries.
- No overlaps (sampling every 2 units).
- The east block is covered without gaps. The only uncovered samples inside wing-1 are the strip west of the Wachdienst diagonal (E.51, wing 2), because the display wing shape uses a straight line there.
- Rooms of the east block have no portals yet; that is step 3.1.

## Step 3.1 — Portals, east block

25 portals were added: 22 doors or openings and 3 exits. No new virtual portals are needed inside the east block; the corridor split `E.flur-tr9-1_E.flur-tr9-2` is from step 1. Door positions were read from 058, cross-checked against 059, and mapped to the plan with an affine fit to ten wall corners (residual ≤ 12 units, typically 5). Each portal line is the door opening (single door 1 m, double door 2 m, WC doors 0.9 m), placed on the shared boundary.

| Portal | Reading |
| --- | --- |
| `E.56b_E.flur-tr9-3` | **Assumed.** 058/059 show no door for E.56b; its west part is cut off on both plans. Placed at the corridor, SVG x ≈ 1106. |
| `E.56c_E.flur-tr9-3` | 058, door in the narrow lower part of E.56c |
| `E.57_E.flur-tr9-3` | 058/059, near the east end of E.57 |
| `E.flur-tr9-1_E.flur-tr9-3` | Fire double door on the diagonal (red dots on 058/059) |
| `E.flur-tr9-1_R.58` | Double door from the hall into R.58 (058/059) |
| `E.58a_R.58` | 058: E.58a's only door opens into R.58 (hence R.58 crossable, step 2.1) |
| `E.62_R.58` | 058: second door of E.62, in its top wall. Not clearly visible on 059; please check. |
| `E.TR9_E.flur-tr9-1` | Stair opening at the upper end of TR9's slanted wall (Lageplan door arc; 058 shows the gap) |
| `E.54a_E.vr-e54a`, `E.flur-tr9-2_E.vr-e54a`, `E.54b_E.vr-e54b`, `E.flur-tr9-2_E.vr-e54b` | WC doors and anteroom doors. The arcs are too small to place exactly, so each is centred on its wall (**assumed positions**). |
| `E.62_E.flur-tr9-2` | 058/059 |
| `E.63_E.flur-tr9-2` | Door at the end of the corridor (058/059) |
| `E.61_E.flur-tr9-2` | 058/059 |
| `E.60b_E.flur-tr9-2`, `E.60a_E.flur-tr9-1` | 058/059. The E.60a door lies on the hall section of the corridor. |
| `E.59_E.flur-tr9-1` | 058 shows two door arcs about 2 m apart. They do not change any route, so they are one portal. |
| `E.59b_E.flur-tr9-1` | **Assumed.** No arc is readable on 058/059; the door is placed on Elt's hall side. |
| `E.52_E.flur-tr9-3` | Opening between Wachdienst and the wall (058/059, green route; Lageplan door) |
| `E.52_E.wachdienst`, `E.52_E.wachdienst_2` | 058: doors at both ends of Wachdienst, about 7 m apart. Two portals. |
| `E.52_exterior` | Haupteingang: `main_entrance` and `emergency_exit` (Notausgang on 058/059; Lageplan "Haupteingang") |
| `E.52_exterior_2` | Notausgang at the south-west corner of E.52 (058 right arrow, 059 left arrow; Lageplan door) |
| `E.61_exterior` | Notausgang in the south wall of E.61 (058/059) |

Not portals:
- The Notausstieg of E.63 (escape window).
- The small stair symbol at the outer corner of R.58. It has no exit sign and is cut off on both plans; please check whether it is an exit.

Doors between wings: the double door `E.flur-tr7-1` / `E.flur-tr9-3` and the west side of E.52 are left for step 4.

### Checks after step 3.1

- 55 zones plus `exterior`, and 46 portals. Each has exactly one SVG element and one graph entry.
- Every portal point is the circle centre and the midpoint of its line.
- Every portal line lies on the boundary shared by its two zones, or on the shell for exits (tolerance 0.6 units).
- No overlaps.
- Every zone of the east block has at least one portal. The zones without portals belong to later wings: TR1–TR8 and `E.flur-tr7-4`.
- `emergency_exit` and `main_entrance` appear only on portals to `exterior`.

## Step 2.2 — Rooms, entrance and foyer (B 7967_055, B 7967_057)

The skeleton and step 2.1 are unchanged. 8 zones were added (63 zones plus `exterior`). `E.foyer`, `E.TR7`, `E.52` and `E.wachdienst` already exist.

| Zone | Label | Crossable | Note |
| --- | --- | --- | --- |
| `E.terrasse` | Terrasse | yes | Crossable by the guidelines |
| `E.51` | Pförtner | no | |
| `E.50b` | WC D | no | |
| `E.wc-beh-e50b` | Beh. WC | no | Unnumbered, see item 3 |
| `E.vr-e50b` | VR | yes | Anteroom |
| `E.50a` | WC H/Beh.-WC | no | |
| `E.vorraum-e50` | Vorraum | yes | Anteroom |
| `E.aufzug-tr7` | Aufzug | yes | Lift |

Rooms made crossable by category, none by exception: Terrasse, both anterooms, lift.

### Method

055 and 057 are rotated: SVG +x is up in the picture and SVG +y is to the right. Outlines follow the Lageplan (measured on a grid at SVG scale); room division and labels follow 055/057.

### Discrepancies, assumptions and readings (for decision)

1. **Terrasse.** Polygon (563,470)–(839,470)–(835,478)–(809,545)–(610,545). South edge = the pier wall shared with `E.flur-tr7-3`; east edge = the Foyer diagonal; west edge = the wall of the long-wing rooms E.26/E.24 (wing 5), ending at (610,545) like the corridor zones. North edge y 470 as in step 1, item 15. Area 144 m² (printed 142 m²).
2. **E.51 Pförtner.** It is the box between `E.flur-tr7-1`, Wachdienst and the WC block (x 1050–1107, y 528–557). It is not drawn on the Lageplan (part of "Infodienst" area, see step 2.1, item 7). Its east edge follows the Wachdienst diagonal and the E.52 diagonal.
3. **E.50b / Beh. WC.** 055/057 print "E.50b WC D" and "Beh. WC" side by side, the Beh. WC without a number. Drawn as two zones: `E.50b` (WC D) north and the unnumbered `E.wc-beh-e50b` south, split at y 579 as on the Lageplan. If "E.50b" also covers the Beh. WC, the two zones must be merged.
4. **E.50a** is one zone: the Lageplan draws a WC H and a wheelchair WC inside it; 055/057 print one label "WC H/ Beh.-WC".
5. **VR `E.vr-e50b`** is the compartment between E.50a and E.50b/Beh. WC (055/057 "VR"). It is named after E.50b, whose two rooms open into it; the Lageplan shows no label.
6. **Vorraum.** On the Lageplan the Vorraum is a narrow room (about 17 units deep, y 579–598) with a stepped, thick north wall (y 566–579). The north edge of the zone is set on the skeleton edge of `E.flur-tr7-1` (y 557), so the zone includes that wall and is deeper than the room. Same for the top edge of the WC block. South edges are at y 600 (wall line of the Speisesaal).
7. **Wall lines south of the block.** The wall between the block and the Speisesaal is at y ≈ 598–600 on the Lageplan; the skeleton corridor `E.flur-tr7-2` ends at y 594. The strip y 594–600 west of x 905 is left for the Speisesaal (step 2.8).
8. **Aufzug.** The notch left out of `E.TR7` in step 1 (item 12) is `E.aufzug-tr7`. 055/057 print "Aufzug".
9. **Speisesaal** is not on 055/057 and stays in step 2.8. The dotted columns on the right of both plans are its columns.

### Changes to files

- `bfw-eg.svg`: the uploaded copy had an empty `defs` and a C2PA metadata block. The metadata block is removed again and the single `style` element is restored in `defs` (colours and fonts I chose; no geometry affected). Please check the style is what you want.

### Checks after step 2.2

- 63 zones plus `exterior`, and 46 portals; every zone and portal has one SVG element and one graph entry.
- No overlaps (sampling every 2 units). Existing portals unchanged.
- Gaps inside wing 2: only a sliver at the west end of the Terrasse (the display wing shape uses (605,545), the zones (610,545)) and the strip in item 7.
- The new rooms have no portals yet; that is step 3.2. The zones without portals are the wing 2 rooms above and those of later wings.

## Step 3.2 — Portals, entrance and foyer

10 portals were added, all doors or openings. No new virtual portals: the four splits of this wing (`E.flur-tr7-1`/`E.flur-tr7-2`, `E.flur-tr7-1`/`E.foyer`, `E.flur-tr7-2`/`E.flur-tr7-3`, `E.flur-tr7-2`/`E.foyer`) come from step 1. No new exits: 055/057 show only the two Notausgänge of E.52, already in step 3.1. Door positions were read from the Lageplan on a 10-unit grid (single door 1 m, double door about 2 m, WC doors 0.9 m) and checked against 055/057.

| Portal | Reading |
| --- | --- |
| `E.51_E.flur-tr7-1` | Door arc in the west wall of E.51 (Lageplan; 055/057) |
| `E.51_E.wachdienst` | Door in the diagonal wall between Pförtner and Wachdienst (Lageplan; 055/057) |
| `E.flur-tr7-1_E.vr-e50b` | Door arc in the north wall of the VR (Lageplan) |
| `E.vr-e50b_E.wc-beh-e50b` | Door arc in the wall between VR and Beh. WC (Lageplan) |
| `E.50b_E.vr-e50b` | **Assumed.** No arc readable; centred on the shared wall |
| `E.50a_E.vorraum-e50` | Door arc in the west wall of E.50a (Lageplan; 055/057) |
| `E.flur-tr7-2_E.vorraum-e50` | Door arc at the south end of the Vorraum's west wall (Lageplan; 055/057) |
| `E.flur-tr7-3_E.terrasse` | Double door in the pier wall (Lageplan; 055/057) |
| `E.TR7_E.flur-tr7-2` | Double door in the north wall of TR7 (Lageplan; 055/057) |
| `E.TR7_E.aufzug-tr7` | **Assumed.** No lift door is readable; placed in the middle of the lift's east side, facing the stairs |

### Readings and open points (for decision)

1. **Terrasse ↔ Foyer.** The wall between them has no door on the Lageplan and none on 055/057; drawn as closed. The Terrasse is reached only through the double door from `E.flur-tr7-3`.
2. **E.vr-e50b.** Only the north door (to the Flur) is clear. The WC D door is assumed (above).
3. **Vorraum.** One door only (to `E.flur-tr7-2`); the south wall to the Speisesaal has none on the Lageplan.
4. **Left for step 3.8 / step 4** (they touch zones of other wings):
   - Double door in the north wall of `E.flur-tr7-1` (x 909–930, y 478) and a door near its north-east corner (x 974–980), both to the middle-area rooms `E.53.1`/`E.53.2`.
   - Double door (x 860–883, y ≈ 596) between `E.flur-tr7-2` and the Speisesaal.
   - The double door `E.flur-tr7-1` / `E.flur-tr9-3`, the fire door `E.flur-tr2-1` / `E.flur-tr7-3`, and both ends of `E.flur-tr7-4`.
5. **TR7** has no exit on 055/057, so it has no portal to `exterior`.

### Checks after step 3.2

- 56 portals, 63 zones plus `exterior`; every zone and portal has one SVG element and one graph entry.
- Each new point is the circle centre and the midpoint of its line; each line lies on the boundary of its two zones (tolerance 0.6 units).
- Existing portals and zones are unchanged.
- Every zone of wing 2 has at least one portal. Zones still without a portal belong to later wings: `E.TR1`–`E.TR6`, `E.TR8`, `E.flur-tr7-4`. `E.TR7` has portals now.

## Step 2.5 — Rooms, long wing (B 7967_052)

The skeleton and steps 1, 2.1, 3.1, 2.2, 3.2 are unchanged. 39 zones were added (102 zones plus `exterior`).

### Which rooms belong to wing 5

- 052 shows: E.01–E.04, E.06–E.26 (as printed, with E.07a, E.07b, E.11a), and at the junction E.23, E.25a, E.25b, VR, E.27, E.28, E.30, two Aufzüge, E.37, Abstell.
- 053 also shows E.21, E.23, E.25a, E.25b, VR, E.26, E.27, E.28 and E.30. By the rule "earlier wing first" they are drawn here. Rooms only on 053 stay with wing 6: E.29, E.31–E.34, E.33a, E.71, the Lager and Aufzug at TR3.
- E.37 and Abstell lie in the display shape of wing 8, but they are printed only on 052 and are drawn here.
- The corridor Flur, TR1 and TR2 already exist. No other wing's zone was touched.

### Zones added

| Zone | Label | Crossable | Note |
| --- | --- | --- | --- |
| `E.01` | WC H | no | |
| `E.vr-e01` | VR | yes | Anteroom of E.01 |
| `E.03` | WC D | no | |
| `E.vr-e03` | VR | yes | Anteroom of E.03 |
| `E.02` | Besprechung | no | |
| `E.04`, `E.06`, `E.08`, `E.10`, `E.12`, `E.14`, `E.16`, `E.18`, `E.20`, `E.22`, `E.24`, `E.26` | Büro | no | East row, from TR1 to the junction |
| `E.07a`, `E.07b`, `E.07`, `E.09`, `E.11a`, `E.11`, `E.13`, `E.15`, `E.17`, `E.19`, `E.21` | Büro | no | West row, from TR1 to the junction |
| `E.aufzug-tr2-a`, `E.aufzug-tr2-b` | Aufzug | yes | Lifts south of the hub |
| `E.37` | – | no | 052 prints only the number |
| `E.abstell-e37` | Abstell | no | |
| `E.23` | Kopierer | no | |
| `E.28`, `E.30` | Büro | no | |
| `E.25a` | WC H | no | |
| `E.25b` | WC D | no | |
| `E.vr-e25` | VR | yes | Anteroom of E.25a and E.25b |
| `E.27` | Archiv | no | |

Rooms made crossable by category, none by exception: the three anterooms and the two lifts.

### Method

- Outlines are read from the Lageplan (embedded scan at full resolution, turned 180°). Room division, numbers and labels follow 052.
- The office rows lie between the skeleton corridor edge and the shell. The partition walls were measured on the Lageplan where they meet the outer wall, then drawn perpendicular to the wing axis until they meet the skeleton corridor edge. Room corners on the skeleton edges are therefore new vertices on existing edges; no existing zone was changed.
- The outer edge of the east row follows the shell to (563,470) and then the west edge of `E.terrasse` to (610,545). `E.26` shares that edge with the Terrasse.

### Discrepancies, assumptions and readings (for decision)

1. **Office numbers.** Lageplan and 052 agree on E.01–E.26 (west row odd, east row even). The Lageplan draws fewer rooms:
   - Lageplan E.11 (72 units along the wall) is E.11 and E.11a on 052. The wall between them is assumed at the middle; E.11a is the north one, as on 052.
   - Lageplan E.07 "KVS Besprechung" (108 units) is E.07a, E.07b and E.07 on 052. The two walls are assumed at equal thirds.
   - Lageplan E.04 and E.06 are one area "BT" with a dashed partition; drawn as two rooms with the wall at the dashed line (y ≈ 125 on the outer wall).
2. **Labels.** All offices are "Büro" as on 052. The Lageplan prints E.19 "Archiv"; 052 prints "Büro", used here. E.02 is "Besprechung" (052); the Lageplan prints "BT". E.37 has no label on 052; the Lageplan text is unreadable.
3. **Numbers at the junction differ between the sources.** On the Lageplan the copier next to the lifts is printed E.28 and the copier room further south E.27; 052/053 print E.23 Kopierer and E.27 Archiv. Drawn with the 052 numbers: the room below the lifts is `E.23`, the room south of it `E.28` (Lageplan E.28, Büro), then `E.30`. On the other side of the corridor, the Lageplan "WC H" and "E.25 WC D" are `E.25a` and `E.25b` on 052/053. Please confirm.
4. **Skeleton edges vs. Lageplan walls.** The skeleton corridor edges of `E.flur-tr1-1` lie about 8 units (≈ 0.7 m) east of the Lageplan walls in the west row, and the west edge of `E.flur-tr3-1` lies 5–15 units east of the room walls. The rooms extend to the skeleton edges, so they are slightly larger than on the Lageplan and the corridor slightly narrower than drawn there. **Proposal:** none needed unless you want the skeleton refitted.
5. **E.01, E.03 and their anterooms.** 052 shows two VRs side by side at the corridor, one below E.03 and one next to E.01. The Lageplan shows only sanitary fixtures and door arcs. Drawn:
   - `E.vr-e03` in the corridor-side 20 units of the E.03 band, so `E.03` is only 3 m² (25 units of wall).
   - `E.vr-e01` beside the corridor end (`E.flur-tr1-2`), 20 units deep, bounded by the wall between E.01 and E.03.
   - `E.01` takes the rest of the top end; its top edge follows the shell. The depth of the VRs and the wall positions are my reading of the 052 sketch.
6. **Sliver at TR1.** The 3-unit triangle between TR1's east edge and the shell at the top ((313,31)–(316,31)) is part of `E.02`.
7. **E.25a, E.25b, VR.** 052 shows E.25b WC D, VR and E.25a WC H as a block on the west side of the corridor beside TR2. The Lageplan shows a triangle under TR2 ("WC H"), a "WC D" box and thick wall bars. Drawn:
   - `E.25a`: the triangle under TR2's V-shaped notch, bounded by TR2 and the diagonal outer wall.
   - `E.vr-e25`: a small compartment at the corridor, 25 × 13 units, between E.25a and E.25b.
   - `E.25b`: the box below E.25a and the VR, down to the wall to E.27.
   - The inner walls are read from the Lageplan bars and are approximate. E.71 (wing 6) shares the diagonal wall with E.25a and E.25b.
8. **West edge of the block E.25b / E.27.** The shell line of wing 6 lies about 12 units west of the room walls on the Lageplan. `E.25b` stops at the diagonal wall; `E.27` extends to the shell line so that no gap is left. The 12-unit strip north of it (461–473, y 630–631) remains for E.71 (wing 6).
9. **Lifts.** The Lageplan shows a triangular wedge and two shafts ("Aufzüge") below the hub; 052 shows two Aufzug boxes. The wedge is added to the west lift. Names follow the guidelines' example: `E.aufzug-tr2-a` (west), `E.aufzug-tr2-b`.
10. **E.37 and Abstell.**
    - E.37 is the quadrilateral east of the lifts (Lageplan "E 37, Rettungszentrale?").
    - Abstell is the triangle between the two slanted thick walls east of it. The Lageplan prints no label there. 052 also draws a thin bar between E.37 and Abstell; it is read as wall and dropped.
    - Both open to `E.flur-tr7-3` (wing 2 zone), see step 3.5.
11. **Notausgang at the outer wall south-east of Abstell.** 052 shows a Notausgang sign and door at about (645, 668). It belongs to the middle-area rooms (step 2.8) and is not drawn.
12. **Not convex.** `E.01`, `E.02`, `E.24`, `E.28`, `E.25a`, `E.25b` and `E.vr-e03` are not convex; this only concerns rooms.
13. **SVG style.** The uploaded `bfw-eg.svg` again had an empty `defs` and a C2PA metadata block. The metadata block is removed and the single `style` element is written again in `defs` (colours and fonts chosen by me; no geometry affected).

### Checks after step 2.5

- 102 zones plus `exterior`; every zone has one SVG element and one graph entry.
- No overlaps with existing zones or between new zones (sampling every unit).
- All new zones lie inside the shell.
- Gaps: the wing 5 shape is covered without gaps except the numerical sliver between the shell's top edge and the corridor-end zones (< 0.5 units).
- Areas at 11.1 units/m: offices 11–17 m², E.21 20 m², E.26 21 m², E.02 25 m².

## Step 3.5 — Portals, long wing

36 portals were added: 35 doors or openings and 1 exit (92 portals in total). No new virtual portals: the corridor splits of this wing come from step 1. Each door is one metre wide (10 units; anteroom doors 0.9 m). Each line lies on the boundary of its two zones (checked numerically, tolerance 0.6 units).

| Portal | Reading |
| --- | --- |
| `E.<n>_E.flur-tr1-1` for the 24 offices `E.02`, `E.04`–`E.26` | **Assumed positions.** One door per office, in the middle of the wall to the corridor. 052 shows the doors near the middle of each room; the Lageplan arcs agree where readable (E.21, E.26) |
| `E.01_E.vr-e01`, `E.03_E.vr-e03` | 052: door from the WC into its VR (arcs on the wall) |
| `E.flur-tr1-2_E.vr-e01`, `E.flur-tr1-1_E.vr-e03` | 052: door arcs of the VRs onto the corridor |
| `E.aufzug-tr2-a_E.flur-tr2-1`, `E.aufzug-tr2-b_E.flur-tr2-1` | Lift doors on the north side (Lageplan). Centred on the shaft; **assumed** |
| `E.25a_E.vr-e25`, `E.25b_E.vr-e25` | **Assumed.** Centred on the shared walls |
| `E.TR1_E.flur-tr1-2` | Door arc at the east end of TR1's south wall (Lageplan). 052 shows the stair open to the corridor there |
| `E.TR2_E.flur-tr2-3` | Opening from the passage into the stair (green route on 052/053), 2 m wide, **assumed** |
| `E.TR2_E.flur-tr2-1` | Door from the hub into TR2 (Lageplan vestibule door), **assumed** in the middle of the shared wall |
| `E.TR1_exterior` | Notausgang of TR1 (`emergency_exit`). The sign on 052 points towards the north end of the stair; the door is **assumed** in the middle of TR1's north wall |

### Doors to zones of other wings (left for step 4)

These doors join a wing 5 room to a corridor zone of another wing. Rooms E.23, E.27, E.28, E.30, E.37 and Abstell have no portal yet because of this. Proposed positions (line end points, midpoint = portal point):

- `E.37_E.flur-tr7-3`: (623.15, 594) – (634.25, 594), point (628.7, 594)
- `E.abstell-e37_E.flur-tr7-3`: (643.65, 594) – (654.75, 594), point (649.2, 594)
- `E.23_E.flur-tr3-1`: (554.6, 626.8) – (549.64, 636.73), point (552.12, 631.77)
- `E.28_E.flur-tr3-1`: (539.99, 656.04) – (535.02, 665.96), point (537.5, 661)
- `E.30_E.flur-tr3-1`: (509.58, 716.85) – (504.61, 726.77), point (507.1, 721.81)
- `E.flur-tr3-1_E.vr-e25`: (531.07, 626.81) – (525.99, 636.69), point (528.53, 631.75)
- `E.27_E.flur-tr3-1`: (514.56, 658.9) – (509.49, 668.77), point (512.03, 663.84)

Readings behind them: E.28 (door arc on the Lageplan), E.30 and E.27 (arcs in the corridor wall) are read from the Lageplan; E.23, the VR, E.37 and Abstell are centred on the shared wall (**assumed**). E.37 has a door arc at its north-west corner (Lageplan, x 617–627), which straddles the corner of `E.flur-tr2-1` and `E.flur-tr7-3`; it is placed on `E.flur-tr7-3`.

Also left for step 4 (zones of other wings):
- `E.TR2` to `E.flur-tr2-4` (hexagon corridor) and to `E.flur-tr3-1`. The Lageplan vestibule has a door towards the hexagon corridor; the route on 053 enters TR2 from `E.flur-tr3-1`.
- The double door `E.flur-tr2-3` / `E.flur-tr2-4`, and the fire door `E.flur-tr2-1` / `E.flur-tr7-3` (both from step 1).

### Readings and open points (for decision)

1. **TR2 exit sign.** 052 and 053 show a Notausgang sign inside TR2, but TR2 does not touch the outer wall, so there is no portal to `exterior`. It is probably a route sign. Please check on site.
2. **TR1 exit.** Only the direction of the sign is known (see table). If the door is elsewhere, only the point of `E.TR1_exterior` changes.
3. **Small triangles on 052.** A triangle at the outer corner of TR1 and a white triangle inside its corner are not exits (no exit sign) and are not portals.
4. **E.03 and E.01** are reached only through their VRs; `E.vr-e01` and `E.vr-e03` have no door between them.

### Checks after step 3.5

- 103 zones including `exterior`, 92 portals; every zone and portal has one SVG element and one graph entry.
- Each new point is the centre of its circle and the midpoint of its line.
- Existing zones and portals are unchanged.
- `emergency_exit` appears only on the portal to `exterior`.
- Zones of wing 5 without a portal: `E.23`, `E.27`, `E.28`, `E.30`, `E.37`, `E.abstell-e37` (doors to other wings, see above). Others without a portal belong to later wings: `E.TR3`–`E.TR6`, `E.TR8`, `E.flur-tr7-4`.
