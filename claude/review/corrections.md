# Corrections applied

All in the working graph (`fixed.py`, `batch2.py`); nothing in the repo. Coordinates are SVG units (1790×1000 frame). Portal ids = two zone ids sorted, joined by `_`, `_2` for a second one.

## Round 1: cut-out review (your redlines on the four cut-outs)
1. **Fire door `E.flur-tr2-1`/`E.flur-tr7-3`.** Diagonal, wall to wall, (606.3,545) to (632.9,594); the zone split re-cut along it.
2. **`E.37` door** moved left to x 616.5–627.5 and re-parented to `E.flur-tr2-1` (was `E.flur-tr7-3`).
3. **TR2 junction.**
   - `E.TR2` is only the diamond (525,536), (557,586), (532,625), (502,580).
   - `E.flur-tr2-2` = old -2 + -3 + the left part of the old TR2 (yellow area merged).
   - Double door `E.flur-tr2-2`–`E.flur-tr2-4` at x 463, y 556–593.
   - Virtual portal to `E.flur-tr2-1` stays; no portal `E.TR2`–`E.flur-tr3-1`.
   - `E.flur-tr2-6` door re-parented onto the passage.
4. **TR7/TR9 diagonal door** `E.flur-tr7-1`/`E.flur-tr9-3`: (1011,481) to (1037,528.3). The second virtual portal was wrong; the stretch up to the `E.51` corner is part of `E.flur-tr9-3`, no portal.
5. **`E.53.1` wall:** no door to the corridor.
6. **`E.62` has no door to `R.58`;** `R.58` renamed `E.58`.

## Round 2: my own fixes from the review
- `E.33` crossable (existing "only access" rule).
- `E.flur-tr2-5` and `-6` non-crossable (rooms).
- Virtual portal `E.53.1_E.53.2`.
- Exit `E.48_exterior` at about (646.4,668.7).
- Step 8 zones clipped against the skeleton; 7 portals re-snapped; overlaps removed.

## Round 3: kitchen entrance (12 redline marks; answers "1 yes, 2 yes, 3 yes")
- **`E.TR8`** is the stair only, including the block below it (polygon (848.8,818.4), (875.5,818.6), (875.5,843)…(907.6,845), (907.6,789), (830,789)).
- Left lift removed: `E.aufzug-tr8-a`, `E.TR8_E.aufzug-tr8-a`.
- `E.TR8_E.speisesaal` removed.
- New zones: `E.flur-tr8-1` (bridge, 907.6–955 × 789–819.8), `-2`, `-3`, `-4`, `-5`, `-6` (south corridor, extended to x 1174 for the `E.41b` pocket), `E.aufzug-tr8-b`, `E.schacht-tr8` (Installationsschacht: non-crossable, no portal).
- Virtual portals `-1`→`-2`→…→`-6`, plus `E.flur-tr8-1_E.speisesaal` (assumption).
- `E.TR8_E.flur-tr8-2` at (907.6,829) (assumed). `E.41` opens only to `E.flur-tr8-3`; `E.43` and `E.42` lose thin strips.
- Shell now follows the TR8 stair outline: vertices (837,829), (812,839), (794,800), (830,789) replaced by (875.5,843), (875.5,818.6), (848.8,818.4), (830,789).

## Round 4: batch 2 (75 marks; applied together)
**Your answers:** `E.59` is one room, discard my split and door; "I don't see a door there" (no door); doors always sit on zone boundaries, adapt boundaries to drawn doors and doors to drawn boundaries, smooth gaps and overlaps; the Speisesaal exterior door is real. You then retracted two removals (`E.60a`, `E.56b` doors) by deleting those marks. You approved `block` and nested-room concepts.

**Zones**
- Blocks: `E.block-e50`, `E.block-e52-a`, `E.block-e52-b`, `E.lueftung-e41`, `E.schacht-tr8`.
- WC row: `E.vorraum-e50`, `E.50a` with nested `E.wc-beh-e50a`, `E.vr-e50b`, `E.50b` with nested `E.wc-beh-e50b`. Nested rooms are cut out of their hosts.
- East block: `E.TR9` as drawn; `E.59b` as drawn (Elt room; `E.flur-tr9-1` extended to its wall x ≈ 1324); `E.aufzug-tr7` as drawn.
- Gap fill within the touched area to the neighbour sharing the longest edge, preferring crossable ones; user-drawn non-crossable rooms and blocks do not absorb.

**Portals removed:** `E.41h_E.flur-tr8-3_2`, `E.42_E.flur-tr8-2`, `E.42_E.flur-tr8-4`, `E.48_E.TR7`, `E.48_E.flur-tr7-3`, `E.49_E.TR7`, `E.52_E.speisesaal`, `E.52_E.wachdienst_2`, `E.52_exterior_2`, `E.TR7_E.aufzug-tr7` (re-added elsewhere), `E.TR7_E.speisesaal` (re-added elsewhere), `E.abstell-e37_E.flur-tr7-3` (so `E.abstell-e37` is unreachable by choice), `E.flur-tr7-2_E.vorraum-e50`, `E.flur-tr8-6_E.lueftung-e41`.

**Portals moved** (to your drawn positions): `E.41_E.41b`, `E.41b_E.flur-tr8-6`, `E.41f_E.41h`, `E.41f_E.flur-tr8-6`, `E.41g_E.41i`, `E.41g_E.flur-tr8-6`, `E.50b_E.vr-e50b`, `E.51_E.wachdienst`, `E.52_E.flur-tr9-3`, `E.54a_E.vr-e54a`, `E.54b_E.vr-e54b`, `E.56a_E.flur-tr7-1`, `E.56c_E.flur-tr9-3`, `E.57_E.flur-tr9-3`, `E.58_E.58a`, `E.58_E.flur-tr9-1`, `E.59_E.flur-tr9-1`, `E.59b_E.flur-tr9-1`, `E.60b_E.flur-tr9-2`, `E.61_E.flur-tr9-2`, `E.61_exterior`, `E.62_E.flur-tr9-2`, `E.63_E.flur-tr9-2`, `E.TR8_E.flur-tr8-2`, `E.TR9_E.flur-tr9-1`, `E.flur-tr7-2_E.speisesaal` (widened; now a real double door), `E.flur-tr9-1_E.flur-tr9-3`, `E.flur-tr9-2_E.vr-e54a`, `E.flur-tr9-2_E.vr-e54b`, `E.vr-e50b_E.wc-beh-e50b`. Each is re-parented by geometry if the zones changed.

**Portals added:** `E.TR8_exterior` (emergency), `E.42_E.flur-tr8-3`, `E.41d_E.flur-tr8-6`, `E.41b_E.41c`, `E.50a_E.wc-beh-e50a`, `E.56a_E.flur-tr9-3_2`, `E.56a_E.56b` (e56–e56a), `E.TR7_E.aufzug-tr7` (aufzugtür), `E.TR7_E.speisesaal` (tr7–e49), `E.42_E.TR8` (tr8–e42), `E.speisesaal_exterior` (emergency exit), wc herren vorraum–flur door. Discarded: "e.59 – e.59a".

**Door-to-boundary step.** Doors that sit within 0.6 stay; user doors 0.6–4.5 off move the wall (strip clipped to the losing zone); others snap to the boundary; exits snap to the shell. A sign bug moved walls the wrong way at first (28 doors off); fixed (9 off).

## Round 5: hub redraw (10 marks)
- **`E.flur-tr7-1`** is your big hub polygon (1037,528), (974,557), (966,566), (911,566), (860,545), (905,478), (1010,480). Name kept as you chose.
- **`E.flur-tr7-2`** lower-left flur (911,566), (893,598), (809,596), (809,545), (860,545).
- **`E.flur-tr7-5`** east flur (1037,528), (1050,528), (1050,557), (975,555).
- **`E.foyer`** regular crossable zone again (849,478), (905,478), (860,545), (809,545), so the seating area can be a destination. Obstacle idea dropped.
- **`E.terrasse`** grows to meet the foyer's left edge.
- Thin pieces `-6` and `-7` gone.
- Virtual portals along whole shared edges: foyer↔hub, foyer↔`-2`, hub↔`-2` (you confirmed a door exists there), hub↔`-5`. Also `-2`↔`E.flur-tr7-3`, `-5`↔`E.flur-tr9-3` by edge.
- `E.53.2_E.flur-tr7-1` moved to x 908–932 on the hub's top edge. `E.flur-tr7-2_E.flur-tr9-3` removed.
- Real door `E.flur-tr7-1_E.flur-tr9-3` kept.

## Page style requests (redline page, v6 to v12)
Lageplan less prominent; circulation vs rooms clearly distinct; crossable rooms (incl. terrasse, foyer, Speisesaal) lighter and close to non-crossable; return to the original warm palette; stairs and lifts distinct from circulation; closer fill ratio; outlines more prominent (indigo, greyscale underlay); Style panel added.


## Round 7: your redraws after the "botched" complaint (59 marks)
- **Cause of the earlier mess (mine):** gap leftovers were grown outward in small steps (scalloped, zigzag edges), whole strips went to whichever neighbour was crossable, and unions were rounded with tiny buffers. Replaced by: drawn outlines exact; leftover gaps split among neighbours by nearest-neighbour regions with straight cuts; drawn zones never grow into gaps; excess a drawn zone gained goes back to its neighbours.
- **E.48 / E.49 / kitchen:** E.49 and E.48 follow your diagonal split; new `E.kueche-ma` (Küche für Mitarbeiter Speisesaal); `E.abstell-e37` replaced by block `E.schacht-e37`. Doors: E.49–E.48, E.49–kitchen, kitchen–Speisesaal, E.49–TR7 (your "tr7 - e49"), E.48 exit. E.49 crossable (only access to E.48); kitchen not.
- **TR2 junction:** `E.schacht-tr2` is your outline (block, no door); `E.flur-tr1-1`, `-1-2`, `-1-3`, `E.flur-tr2-1`, `-2-3` follow your redraws; tr1-1 and tr2-1 no longer touch; `E.aufzug-tr2-b`, `E.37`, `E.block-tr2` redrawn; row bottom on your straight line (553.5,623)–(666.2,624.9).
- **Wing 1 WC group:** `E.01` (WC-H), `E.vr-e01`, `E.03` (WC-D), `E.vr-e03`, `E.TR1`, new `E.block-tr1`, `E.flur-tr1-2`, with your four doors.
- **West hexagon:** `E.72a`, `E.72b` redrawn; `E.82` is the Vorraum (crossable), `E.82a` the WC; `E.73` east boundary is your straight line; tr4-3/tr4-8 boundary on your line; moved doors snapped; all E.76 doors removed, E.72a keeps its first door.
- **Outer frame (shell) pulled back:** west edge of the IQ+UKM wing, E.33a bottom, TR3 bottom and the E.34 tip; `E.flur-tr3-2` has an exit to the outside (assumed emergency exit).
- **Corridor `E.flur-tr3-1`:** exactly your strip; rooms beside it extend to it with straight walls.

## Round 8: last 12 marks
Doors of E.23, E.27 to E.33 snapped onto the corridor wall at your positions; second E.34 door and `E.TR3_exterior` removed; east wall of the wing is one straight line (459.3,866.6)–(606.5,623.8) with the outer frame and rooms following it.

## State now
193 zones, 219 portals (36 virtual, 14 exits), one connected component, 0 overlaps, gaps 315 units², outside shell 21. Still off a wall: `E.TR9_E.flur-tr9-1` (4.2). Suggestions regenerated (28 items) for the current graph.

## Not applied or still open
Blocks exist in the working graph and on the redline page, but the exported connectivity JSON has no `kind` attribute yet, so they appear there as ordinary non-crossable zones. The scripts that produced all of this are a snapshot and do not run as they are (hard-coded paths).
Hub thin triangles (later); `block`/nested-room rules into `docs/data`; skeleton fixes (`E.flur-tr3-1` refit, `E.flur-tr5-2` arc and split, `E.lager-tr3`, convexity of `E.41`/`E.52`); middle-area gaps and doors; `E.flur-tr2-6` identity; `E.TR8` exit (photo 056).

## Round 6: TR2, TR3 and west hexagon (69 marks)
- **Removed zones:** `E.flur-tr2-5` ("not a separate flur", merged into the new flur), `E.flur-tr2-6` ("in exterior": cut out of the shell), `E.technik-tr4-a`/`-b` (replaced). `E.flur-tr3-1`, `E.TR3`, `E.aufzug-tr3` were removed and redrawn under the same ids.
- **New or reshaped zones (ids chosen by me):** `E.flur-tr4-5` (south corridor), `-6` (west vestibule), `-7` (north), `-8` (split from `-3`), `E.flur-tr2-3`, `E.flur-tr1-3`, `E.flur-tr3-2`, `E.vr-e72c`, `E.vr-e84`, `E.vr-e25b`, `E.putzmittel-tr4`, `E.lager-tr3`; blocks `E.schacht-tr4`, `E.block-tr4-a/-b`, `E.block-tr2`. Reshaped to your outlines: `E.flur-tr4-1` to `-4`, `E.TR4`, `E.aufzug-tr4`, `E.74`, `E.74a`, `E.75`, `E.76`, `E.80` to `E.84`, `E.83a`, `E.flur-tr2-2`, `E.25a`/`E.25b`/`E.vr-e25`, `E.aufzug-tr2-b`, `E.37`, `E.TR3`, `E.aufzug-tr3`, `E.flur-tr3-1`.
- **Doors:** 20 adds, the `E.flur-tr2-4`/`E.flur-tr4-2` move (x 384), `E.TR4_E.aufzug-tr4` removed, `tr2-flur` door `E.TR2`–`E.flur-tr2-3`. Old doors kept by relocating them onto the room's wall: `E.80`, `E.82_E.82a`, `E.25a`, `E.29`, `E.31`, `E.33`. Dropped: `E.TR3_E.flur-tr3-1`, `E.flur-tr3-1`-side leftovers, `E.flur-tr1-1_E.flur-tr2-1` (no longer adjacent), `E.flur-tr4-3_E.technik-tr4-a`.
- **Assumed by me:** door `E.flur-tr4-5_E.vr-e84` (no door was marked for the E.84 Vorraum); `E.82` kept crossable although you drew it as "wc-h".
- **Result:** 190 zones, 230 portals (39 virtual), one component, 0 overlaps, gaps 391 units², outside shell 70. Doors off boundary by more than 1.5: `E.25a_E.vr-e25` 4.6, `E.72a_E.flur-tr4-4_3` 4.6, `E.flur-tr4-4_E.schacht-tr4` 3.4, `E.25b_E.vr-e25` 2.6, `E.76_E.flur-tr4-4` 2.4, `E.83_E.83a` 2.1, `E.80_E.flur-tr4-6` 1.9, `E.76_E.flur-tr4-4_2` 1.8, `E.flur-tr4-1_E.flur-tr4-4` 1.8, `E.73_E.flur-tr4-7` 1.6; virtual `E.flur-tr4-4_E.flur-tr4-7` and `E.flur-tr1-3_E.flur-tr2-1` about 10.
- **Route note:** `E.72a`→`E.62` now passes through the TR2 stair via your `tr2-flur` door.
