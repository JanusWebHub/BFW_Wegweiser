# Review of the Claude Design EG output (local/simpler, up to 11ba7b5)

Date 2026-09-29. Scope: everything added on `origin/local/simpler` after the split at 490ae5a (commits dc99907, 161b9ac, 1a9850e, 74ce542, 11ba7b5). Nothing from before the split was read.

## 1. What was checked and how

| Input | Use |
| --- | --- |
| `graph_format.md`, `zoning_guidelines.md` | Specification. Both are byte-identical since dc99907. |
| `design-prompt.md`, `parallel-message*.md`, `claude-design-response-*.md` | Task instructions and the conversation with Claude Design. |
| `handoff.md`, `claude-remote-branch-tips-review-recap.md`, `copilot-report.md`, `zoning-report*.md` | Accounts to verify. |
| 7 SVG + 7 JSON sets (base, wings 3 to 7, step 8 merge) | Parsed and measured (shapely), all 7 sets. |
| Lageplan PDF (turned 180°) | Overlay of the merged SVG in the frame `SVG = scan px − (40, 77)`. |
| 10 escape-plan photos | Read by eye: exits, door arcs, room labels, escape routes. Sampled, not exhaustive. |

Method for the data: SVG and JSON loaded independently; ids, flags, portal geometry, polygon validity, overlaps, gaps, convexity, reachability and segment containment computed; wing files compared with the base and with the merge; routes searched with the rules of `graph_format.md`. Scripts are in `analysis/` (they need `shapely`). Not done: I did not open the SVGs in a browser, and only about ten door claims were checked against the photos.

## 2. Verdict

The data is structurally sound and disciplined, but the step 8 merge is not deliverable as it stands. Four things need fixing before it can be called the EG graph:

1. **The graph is cut in two for routing.** The long wing, IQ+UKM wing and hexagon (27 crossable zones) are not connected to the rest of the building. From `E.52`, 80 of 172 zones cannot be reached. One missing portal (the fire door `E.flur-tr2-1` / `E.flur-tr7-3`) fixes this. The step 4 check said "every zone reachable" only because it let paths run through `exterior`, which the search rules forbid.
2. **Step 8 broke the frozen skeleton.** It overlaps approved zones (3.4 m² in total), leaves 11.9 m² uncovered and pokes 1.9 m² outside the shell. The report says "only slivers".
3. **The merged SVG breaks the markup rules.** It has a C2PA block and no `<style>`. Three different styles exist.
4. **A handful of content errors:** a room drawn as corridor, one guideline rule not applied (`E.33`), one guideline rule ignored (`E.53.1`/`E.53.2` virtual portal), missing exits (`E.48`, `E.TR8`), Lager missing.

Everything else (ids, JSON/SVG parity, portal geometry in wings 1 to 7, base untouched, counts) is confirmed. Roughly half of the 179 non-virtual portals (my count from the reports: about 84) are assumed rather than read from a plan.

## 3. Inventory of what Claude Design produced

| Set | Zones | Portals | Content |
| --- | --- | --- | --- |
| base (`steps-2.1-to-3.2.md/`) | 63 | 56 | Skeleton (37 zones, 21 virtual portals), east block (18), entrance/foyer (8). The only file with a style. Approved. |
| wing 3 kitchen | +15 | +30 | 3 exits. |
| wing 4 north-west | +20 | +26 | 3 exits. |
| wing 5 long wing | +39 | +36 | 1 exit. |
| wing 6 IQ+UKM | +8 | +10 | 1 exit. |
| wing 7 hexagon | +18 | +21 | 1 exit. |
| step 8 merge | 171 (+ exterior) | 206 | Base + 100 wing zones + 8 middle-area zones; 123 wing portals + 27 new. |

Merge composition verified: 171 = 63 + 100 + 8 and 206 = 56 + 123 + 27. No zone or portal is duplicated across wings, no wing content was altered by the merge, and no wing changed anything of the base. Merged totals: 66 crossable and 105 non-crossable zones; 12 exits (1 main entrance); 27 virtual portals; 885 computed segments.

Commit history (all commit messages are "design data" / "update design data"): dc99907 holds the state after step 2.1 (55 zones, 21 portals), not step 1. 161b9ac is the approved base plus the parallel messages. 1a9850e adds wings 3 to 7, the Copilot report and three utility scripts. 74ce542 adds step 8. 11ba7b5 adds the responses, recap and handoff and moves files.

## 4. The accounts checked

| Claim | Result |
| --- | --- |
| Base untouched by all wings and the merge | Confirmed (zone geometry, portal lines, JSON, shell). |
| SVG and JSON match one to one | Confirmed for all 7 sets. |
| Wing counts 15/30, 20/26, 39/36, 8/10, 18/21 | Confirmed. |
| Copilot: merge simulation 164 zones and 179 portals | Confirmed (63 + 100 + exterior = 164; 56 + 123 = 179). |
| Step 8: 171 zones and 206 portals | Confirmed; exterior is not counted (171 + exterior = 172 JSON zones). The earlier 169/201 was the pre-Lageplan version. |
| "Doors added at merge: 8" (one message) vs seven rooms (other message and report) | Seven: `E.23`, `E.27`, `E.28`, `E.30`, `E.vr-e25`, `E.37`, `E.abstell-e37`. |
| Portal lines lie on the shared boundary (≤ 0.6) | Confirmed for wings 1 to 7. Refuted for 9 step 8 portals (up to 1.24 units off). |
| "No overlaps" (every report, sampled at 1.5 to 2 units) | Refuted. Real overlaps exist, including 66 units² in the approved base (see 5.3). |
| Step 8: "only edge slivers left; no real overlap or hole" | Refuted: 1464 units² uncovered (49 pieces, largest 443), 418 units² overlap, 237 units² outside the shell. |
| Step 4: "every zone reachable from exterior over crossable zones, except `E.33a`" | Technically true, practically false: it works only through the 12 exits (see 5.1). |
| "5.6% of wing 6 unclaimed" | 5.4% before step 8. After step 8, 0.5% remains, but part of that was filled wrongly (5.2). |
| Overlay: "each wing fitted separately because wings were drawn at different scales" | Not supported. One global transform (−40, −77) aligns all wings to the Lageplan within a few px; the frame is consistent. |
| Style choice open, three styles | Confirmed: warm (base), green (wing 5 and step 8 `.txt`, byte-identical), and none in the wing/merge SVGs. |
| C2PA stripped from wing SVGs | Confirmed for wings 3 to 7. The step 8 SVG has the block again and no style. |
| Utilities in `docs/utilities` | Broken on the current tree: they read `data/connectivity-graph.json` and `bfw-eg.svg`, which 11ba7b5 moved into `steps-2.1-to-3.2.md/`. They also sample at 2 units, which is why they missed the overlaps. |
| Handoff: specs at `docs/design/…` | Moved to `docs/data/` in 11ba7b5; the handoff path is stale. |

Two smaller history findings: (a) step 3.1 also modified `E.52` (it lost vertex (1275, 587), 60 units²) besides the approved `E.flur-tr9-1`, `E.59b`, `E.59` change; it is a consequence of the cut but was not reported. (b) `E.59` in the SVG is Lageplan `E.59a` + `E.59` combined (70 m² vs 30.39 printed for one of them); this is documented.

## 5. Findings and proposed solutions

### 5.1 Blocker: the building is disconnected for routing

Evidence: the crossable graph has two components (39 and 27 zones) with no link between them. Component 2 is the long wing corridors, `E.TR1` to `E.TR4`, IQ+UKM corridor, hexagon corridors and lifts.

- From `E.52`: 80 of 172 zones unreachable; from `E.01`, `E.72a`: 92 of 172 unreachable.
- Routes as delivered: `E.01` → `E.52` and `E.21` → `E.52` are `unreachable`.
- After adding the one fire-door portal only `E.33a` is unreachable, and that is because of 5.4 (a).

Cause: the fire door `E.flur-tr2-1` / `E.flur-tr7-3` was "left for the portal steps" in step 1, again in 3.5, and never added in step 4. Other doors on the same list were also never added:

| Missing portal | Shared boundary | Proposed point (midpoint) | Source note |
| --- | --- | --- | --- |
| `E.flur-tr2-1_E.flur-tr7-3` | (610,545)–(622,594), 50 units | (616, 569.5) | Fire door, Lageplan; width to read there |
| `E.flur-tr2-3_E.flur-tr2-4` | x = 450, y 556–573 | (450, 564.5) | Double door, Lageplan and 053 |
| `E.flur-tr7-1_E.flur-tr9-3` | x = 1050, y 480–528 | (1050, 504) | Double door at x ≈ 1050 (step 1) |
| `E.TR2_E.flur-tr2-4` and/or `E.TR2_E.flur-tr3-1` | adjacent | to be read | Lageplan vestibule door; 053 route enters TR2 from `E.flur-tr3-1` |
| `E.53.1_E.flur-tr5-2` (door to the corridor y 279) | y ~ 279, 150 units | none proposed | Listed in 3.4, not added; no door arc readable on the Lageplan along this wall (see cut-out 4), so probably not a door |

Consequences beyond reachability: without the double door `E.flur-tr2-3`/`-4`, routes between the hexagon corridor and the long wing go through the stairwell `E.TR2` and `E.flur-tr2-6` (e.g. `E.72a` → `E.21`: 38.4 m via the stair, 36.4 m with the door). Without the `E.flur-tr7-1`/`E.flur-tr9-3` door, `E.90` → `E.60a` is 104.7 m via the Speisesaal instead of 79.8 m.

Proposed solution: add the portals above (points measured from the Lageplan, doors on the Lageplan at these junctions), then add a check "the crossable graph plus exterior-free connectivity is one component" to the validator so this cannot pass again. Search rules forbid passing through `exterior`; the validator must do the same.

### 5.2 Blocker: step 8 zones and classification

1. **`E.flur-tr2-5` is a room, not a corridor.** The Lageplan prints "Fr. Sygulla / Hr. Ackermann" in this space (x 338–386, y 592–628), next to `E.71 W/F`. Step 8 made it a crossable corridor. Wing 6 had already said it is a room. Fix: make it non-crossable and give it a room id (or merge it into `E.71`); ask the user which (D5).
2. **`E.flur-tr2-6`** (x 422–494, y 592–630, east of `E.71`) is an unlabelled white area on the Lageplan. It got a corridor id and an assumed door to `E.TR2`. Its nature is unknown (lobby, shaft, part of `E.TR2`). Fix: decide with a photo (D5); until then non-crossable.
3. **`E.speisesaal` crossable is supported.** Photos 055 and 057 draw the escape route from the second Notausgang across the Speisesaal to the double door into the Flur. Keep it crossable.
4. **`E.53.1` / `E.53.2`:** the guidelines and the handoff say "two zones joined by a virtual portal"; step 8 drew none ("dashed = movable partition"). Fix: add `E.53.1_E.53.2`, virtual, at the middle of the boundary y = 372 (or record an explicit exception, D7).
5. The step 8 report says "first placeholder version replaced": true; the committed report has no "Mitte" rows. But it also lacks the sections for wings 3, 4, 5 and 6 (only the wing 7 sections survive), so the assumptions of those wings are only in the per-wing reports.

### 5.3 Major: geometry (overlaps, gaps, outside the shell)

Overlaps (units²; 123.2 units² = 1 m²):

| Pair | Area | Cause | Fix |
| --- | --- | --- | --- |
| `E.TR7` / `E.speisesaal` | 120.6 | Speisesaal drawn over the stairwell diagonal | Clip Speisesaal |
| `E.TR8` / `E.speisesaal` | 65.8 | same | Clip Speisesaal |
| `E.aufzug-tr8-b` / `E.speisesaal` | 47.9 | same | Clip Speisesaal |
| `E.41a` / `E.speisesaal` | 24.5 | same | Clip Speisesaal |
| `E.flur-tr7-4` / `E.56a` | 22.2 | step 8 over skeleton | Clip `E.56a` |
| `E.flur-tr5-2` / `E.53.1` | 18.7 | step 8 over skeleton | Clip `E.53.1` |
| `E.37` / `E.48` (+ small `E.abstell-e37`, `E.aufzug-tr7`, `E.TR7` with `E.48`) | 14.5 (+1.2) | step 8 over wing 5 | Clip `E.48` |
| `E.71` / `E.flur-tr2-6` | 13.3 | step 8 over wing 6 | Clip |
| `E.flur-tr4-2` / `E.flur-tr2-5`; `E.flur-tr2-4` / `-5`, `-6`; `E.TR2` / `E.flur-tr2-6` | 12.8; 2.9; 2.5; 3.7 | step 8 over skeleton | Clip |
| `E.flur-tr9-3` / `E.52`, `E.wachdienst`, `E.51` | 32.9, 27.5, 6.2 | approved base: bottom edge y 528 vs 529 sloping | Insert vertex (1183, 528) in `E.flur-tr9-3`; 0.5-unit sliver only |

Total 418 units² (3.4 m²). Clipping the eight step 8 zones against everything else removes all of them (each loses 0 to 2% of its area), but it shifts 7 portal lines by up to 0.9 units, so portals must be re-snapped after the clip.

Outside the shell: 237 units². `E.53.1` 147, `E.56b` 35 (approved wing 1), `E.56a` 17, `E.49` 13, `E.flur-tr2-6` 7.5, `E.63` 7.5 (approved), `E.68a` 6.5. Fix: intersect all zones with the shell; the shell itself may need one correction (the extrapolated `E.63` corner, D9).

Gaps: 1464 units² = 11.9 m² in 49 pieces. Largest: 443 units² at (1093, 665) (south-east part of the Speisesaal), 286 at (998, 392) (between `E.53.2` and the diagonal corridor), 140 at (484, 666) (wing 5/6 junction), 100 at (697, 763) (south of `E.49`), 84 at (398, 555) (hairline, 153 × 2), 83 at (1039, 464). After clipping, the Speisesaal-side gap grows to 643 units². These cannot be closed by script; they need a redraw of the Speisesaal/E.49/E.48 outlines and of `E.53.x` against the Lageplan (or with the middle-area photos the user plans). Interior gaps of wings 1 to 7 are essentially zero except the wing 6 and 2 items in 5.5.

Convexity (spec: a straight line between two portals of a zone stays inside it). Segments leaving their zone by more than 0.5 units: 71 of 885 (8%), in `E.41` (46 of 78 pairs, max 117 units outside), `E.52` (9), `E.flur-tr7-4` (5), `E.TR7` (3), `E.58` (2), `E.68` (2), `E.speisesaal` (1, 175 units), `E.TR2`, `E.flur-tr9-1`, `E.TR6`. The worst are wrap-around shapes (`E.41`, `E.52`). Proposal: split `E.41` and `E.52` into convex pieces with virtual portals (draw-fine principle), or accept and rely on movement lines later; split `E.flur-tr7-4` at its bend. Decide in D8.

### 5.4 Major: content and spec deviations

a. **`E.33` must be crossable.** It is the only access to `E.33a` (guideline: a room that is the only access to another room is crossable). Currently `E.33a` is unreachable as a target. Setting it crossable makes `E.33a` → `E.02` = 76 m via `E.33`. Alternatively an on-site door from `E.33a` to the corridor (photo 053 shows `E.33a` next to the lift and `TR3`; no door readable) changes this.

b. **Missing exits.**
- `E.48`: photo 052 shows a Notausgang sign and door in the outer wall south-east of `Abstell`, near SVG (646, 669), which lies on the west shell edge of `E.48`. Wing 5 reported it (3.5 item 11) as belonging to the middle area; step 8 never added it. Proposed portal `E.48_exterior` with `emergency_exit` at ≈ (646.4, 668.7).
- `E.TR8`: photo 056 shows a Notausgang sign with an arrow down and a door leaf at the TR8 landing beside `E.42`. The wing 3 report could not read a door and left it out. Verify on site; proposed `E.TR8_exterior` or `E.flur-tr8-1_exterior`.
- The other exits match the photos: kitchen (three on the east and south walls), `E.52` (two), `E.61`, hexagon west tip, `TR1`, `TR3`, `TR5`, `TR6`, Durchgang. `E.TR2`, `E.TR4` show only a running-man route sign inside; `E.TR7`, `E.TR9` show none. Photo 055/057: Notausgang 2 sits at the corner between `E.52` and the Speisesaal, and its escape route runs through the Speisesaal; the zone owning that door (`E.52` or `E.speisesaal`) should be checked on site.
- `E.flur-tr7-2_E.speisesaal` is virtual, but 055/057 show a double door there (3.2 item 4). Minor; either model is defensible.

c. **Lager at `E.TR3` missing** (wing 6 proposal `E.lager-tr3`, the triangle east of the lift, door arc at about (440, 845)). The guideline requires every unnumbered space to be a zone. Needs the corridor refit (5.5).

d. **Doors modelled as virtual or open without a plan reading:** all 14 middle-area doors are assumed from shared walls (the Lageplan shows no door symbols at scan resolution). `E.flur-tr2-6`–`E.TR2` is a real door on that basis.

e. **Ids:** all rules pass (no `_`, sorted portal ids, consecutive split counters, `-a`/`-b`). Two nitpicks: `E.flur-tr3-1` and `E.flur-tr6-1` are single zones but carry `-1` (the spec adds `-1` only when a space is split); `E.flur-tr7-4` is not next to `E.TR7`. Ids are hard to change later, so decide now (D12).

f. **Portal class `portal exit`** on the 12 exit portals: the spec allows only `portal` and `portal virtual`. Harmless, but either change the spec or the file. Eight zones have empty `data-label` (`E.56b`, `E.37`, `E.74a`, `E.75`, `E.82a`, `E.83a`, `E.technik-tr4-a`, `-b`): matches the plans (no label printed).

g. **Report and format:** `floors.E.svg` is `web/assets/bfw-eg.svg`, which does not exist yet (only `bfw-eg-ost.svg`). Folder names are inconsistent (`steps-2.1-to-3.2.md/`, `-8` suffixes). The label group contains a third text per unnumbered zone (`label-id`), not required by the spec.

### 5.5 Major: skeleton and wing 5/6 geometry

- `E.flur-tr3-1` is offset from the real corridor: 10–22 units (1–2 m). My overlay (`fig4`) confirms the band does not follow the corridor walls at the lower part. Rooms `E.29`, `E.31`, `E.33` come out too big, `E.32`, `E.34` distorted, and every door on this corridor is placed up to about 20 units off. Wing 6's proposal (new wall lines through about (486,705), (455,750), (430,785), (409,820), (388,858) west and (508,700), (478,750), (456,782), (447,820), (460,867) east) is sound. It changes the skeleton, so it needs your approval (D3), then wing 5's seven step 4 doors and all wing 6 rooms, doors and the exit follow by a scripted vertex move plus a check.
- Scale check: 26 rooms from the reports imply 11.3 units/m (median), against 11.1 used. The 5 rooms used give 11.09. Zones run to wall centre lines (about 2% inflation), so 11.1 is reasonable. Distances carry about ±3%; leave as is.
- Other skeleton proposals still open (D3): extend `E.flur-tr8-3` to y 941; split `E.flur-tr5-2` at the fire door x 877 (the door is not a portal now, so routes ignore it); extend `E.flur-tr4-3` and `E.flur-tr4-1` to the wall (4 to 6 units); close two shell hairline gaps at (101,563) and (337–362,555); `E.41` is open to `E.flur-tr8-1`/`-2` and drawn as real portals (3 of them); a door at x ≈ 1140 inside `E.durchgang`.

### 5.6 Markup and packaging (spec `zoning_guidelines.md`, SVG section)

| Set | C2PA/metadata | `<style>` | Note |
| --- | --- | --- | --- |
| base | none | 1 (warm) | The only compliant file. |
| wings 3 to 7 | stripped by Copilot | none | Renders black. |
| step 8 merge | present (`xmlns:c2pa` + `<metadata>`) | none | Style in `bfw-eg-style-8.txt`. |

Group order (`shell`, `zones`, `portals`, `labels`), absolute coordinates, no transforms, ids `zone-`/`portal-`, `viewBox` = `width`/`height`: all fine in every set. No zone needs a hole; there are no `path` zones.

Styles (`fig3`): the warm style has larger fonts (8/7/5.5 px) and reads better on the canvas; the green style has 6/5/3.6 px fonts but separates portals by type (door red, virtual blue, exit green) and circulation by colour. Both use the same class names, so either can be injected. Suggestion: warm palette for zones and labels, green's portal coding.

## 6. Per-wing assessment (data plus photos)

| Wing | Result | Main issues |
| --- | --- | --- |
| 1 east block | Good. Photo 058/059 labels, exits (E.52 ×2, E.61), `E.58` (formerly R.58) and `E.58a` doors match; the `E.62`/`E.58` door I first read from the photo does not exist (you corrected it). | 4 WC/VR doors and the `E.56b`, `E.59b` doors assumed; `E.flur-tr9-3` sliver; `E.56b` 35 units² outside the shell; `E.63` corner extrapolated. |
| 2 entrance/foyer | Good. | `E.50b`, lift doors assumed; Terrasse–Foyer closed (photo agrees); Beh. WC separate zone (on-site). |
| 3 kitchen | Good. All kitchen rooms of photo 056 present; 3 of 4 exit signs modelled. | 5 assumed doors; `E.TR8` exit missing; `E.41` non-convex, open to corridors. |
| 4 north-west | Good; all 060/061 rooms present. | `E.68`, `E.66` crossable by exception; `E.67a` bay straddles the `E.66`/`E.67` wall on photo 060, so the opening may belong to both rooms; fire door x 877 not modelled. |
| 5 long wing | Good; 24 office doors assumed (photo 052 shows doors at about mid-wall, plausible). | 7 doors added at merge; `E.23`/`E.27`/`E.28` numbers differ between Lageplan and 052/053; `E.flur-tr1-1` has 27 portals. |
| 6 IQ+UKM | Weakest wing. | Corridor offset; Lager missing; door positions up to 20 units off; `E.33a` only via `E.33`. |
| 7 hexagon | Good. | `E.72a/b/c`, `E.74a`, `E.82`/`E.82a`, `E.83`/`E.83a`, core rooms and technik boxes partly guessed; `E.74`, `E.82`, `E.83` crossable on guesses. |
| 8 middle | Placeholder-level. | Lageplan only, doors assumed, overlaps and gaps (5.2, 5.3), missing exit `E.48`. |

## 7. Decisions and open questions for you

| # | Question | Recommendation |
| --- | --- | --- |
| D1 | Follow 2026 escape-plan splits (`E.59b/E.60a/b`, `E.56b/c`, `E.72a/b/c`, `E.68a/b`) or the 2018 Lageplan? Claude Design asked; no answer recorded. | 2026 (the guidelines say so). Record the Lageplan differences as known discrepancies. |
| D2 | Style for the final SVG. | Warm palette and fonts plus green portal coding; one `<style>` injected by the merge script. |
| D3 | Approve one skeleton amendment: refit `E.flur-tr3-1`; extend `E.flur-tr8-3`, `E.flur-tr4-1/-3`; split `E.flur-tr5-2` at the fire door; add `E.lager-tr3`; close the shell hairlines. | Approve as one batch; apply by script; re-run wing 5/6 doors. |
| D4 | `E.66` / `E.67` / `E.67a`: which rooms open to the bay? | Site check. If both: `E.67a` connects both (or make `E.67a` a zone and both crossable). Default keep `E.66`. |
| D5 | What are `E.flur-tr2-5` (Sygulla/Ackermann room) and `E.flur-tr2-6` (white area east of `E.71`)? | Make both non-crossable now; photograph both. |
| D6 | `E.33` crossable (guideline) or a door `E.33a`–corridor? | Crossable now; site check. |
| D7 | `E.53.1`/`E.53.2` virtual portal (guideline) or exception? | Add the virtual portal. |
| D8 | Convexity: split `E.41`, `E.52`, `E.flur-tr7-4`, `E.TR7`, `E.TR2` now, or accept non-convex zones until movement lines exist? | Split `E.41` and `E.52`; accept the rest. |
| D9 | `E.63`/shell: keep the extrapolated corner (scan cut off)? | Keep, check on site. |
| D10 | Exits: add `E.48_exterior`; add `E.TR8` exit; confirm which zone owns Notausgang 2 (`E.52` vs Speisesaal). | Add `E.48`; TR8 after a photo. |
| D11 | Crossability guesses: `E.74`, `E.82`, `E.83`, `E.68`, `E.66`. | Keep, all flagged in the report; revisit after the site check. |
| D12 | Rename `E.flur-tr3-1` and `E.flur-tr6-1` (single zones)? | Keep ids as they are (already referenced); note as spec nit. |
| D13 | Portal class `portal exit`: allow in the spec? | Yes; update `zoning_guidelines.md`. |
| D14 | Provenance flag stays `unverified` until the middle-area photos and the site checks (list below) are done? | Yes. |
| D15 | Commit the 2.7 MB overlay PNG and the per-wing intermediate folders, or keep only the final set? | Keep intermediates for now, tidy after the merge. |

Site-check list (all items from the reports plus new ones): TR2 passage and doors; Durchgang position and door x 1140; Foyer edge; stair symbol at `E.58` (formerly R.58); note: the `E.62`/`E.58` door does not exist and was removed; `E.56b` and `E.59b` Elt doors; lift doors; Beh. WC own zone; `E.33a` door; `E.flur-tr2-5`/`-6`; `E.TR8` exit; `E.48` exit; Notausgang 2 owner; bay `E.67a`; `E.82a`/`E.83a` doors; `E.41b_exterior`; E.23/E.27/E.28 numbering.

## 8. Plan to merge everything

Principle: approved base and wings are frozen; every change is scripted, listed and re-validated; no hand edit of an SVG.

**Phase 0 (no decisions needed).**
1. New folder `data/eg/` (final files) and `build/` (scripts). Keep the wing folders as source.
2. Write `validate_eg.py`, replacing the three broken utilities. Checks from the two specs plus the ones the reports missed: exact overlap, gap and outside-shell areas (thresholds e.g. 0.5 units²), portal on boundary (≤ 0.6), one crossable component without `exterior`, reachability from a set of test starts, segment containment per zone, id rules, `floors.E.svg` path exists.
3. Fixture routes from section 5.1 (`E.01`→`E.52`, `E.21`→`E.52`, `E.90`→`E.60a`, `E.72a`→`E.21`, `E.33a`→`E.02`) as regression tests.

**Phase 1 (mechanical, safe).**
1. Start from the step 8 merge; strip the C2PA block; inject one style (D2); rename outputs to `bfw-eg.svg` and `connectivity-graph.json`.
2. Base sliver: add vertex (1183, 528) to `E.flur-tr9-3`.
3. Clip the eight step 8 zones against all other zones and the shell; re-snap the affected portals onto the shared boundary.
4. Add the missing portals of 5.1 (points from the table), `E.53.1_E.53.2` (virtual), `E.48_exterior`, `E.33` crossable, `E.flur-tr2-5`/`-6` non-crossable.
5. Run the validator; expected result: connected, no overlaps, gaps only in the middle area.

**Phase 2 (after D3 to D6).**
1. Skeleton amendment as one scripted change set: new `E.flur-tr3-1` outline, moved wing 6 room edges and doors, `E.lager-tr3`, other skeleton edits; portal points recomputed as midpoints of their lines.
2. Redraw the middle area from your photos in one Opus Claude Design session: the input is the current SVG and the gap map (`fig1`), the rule is "do not alter frozen zones, fill the gaps, no overlap". Deliver into a new folder.
3. Convexity splits (D8) with virtual portals.

**Phase 3 (verification).**
1. Site check list of section 7; per item set `provenance` for the file only when everything is verified.
2. Re-run the validator and route fixtures; generate `routing-graph.json` from an empty `routing-config.json`; commit `connectivity-graph.json`, `routing-config.json`, `routing-graph.json` to `data/` and the SVG to `web/assets/`.

**Acceptance criteria.** Validator green (no overlap > 0.5 units², no gap > 0.5 units² inside the shell except documented ones, one crossable component, all fixture routes found, 100% segments inside their zone or documented exceptions); report complete (sections for every step including wings 3 to 6, all discrepancies, assumed doors); `provenance: unverified` until Phase 3.

## 9. Files

- `fig1-gaps-overlaps-disconnect.png`: overlaps (red), gaps (orange), outside shell (magenta), the disconnected component (yellow) and the missing fire door (circle).
- `fig2-merged-on-lageplan.png`: merged SVG on the Lageplan (global transform).
- `fig3-style-warm-vs-green.png`: both styles on the merge.
- `fig4-iq-ukm-corridor-offset.png`: the `E.flur-tr3-1` offset.
- `analysis/`: the scripts behind the numbers (`check.py`, `cmp.py`, `graph.py`, `geo.py`, `gaps.py`, `route.py`, `render.py`).

Note: the figures and cut-out images named here are not in the repository. See `TIDYUP-PLAN.md` for regenerating them.
