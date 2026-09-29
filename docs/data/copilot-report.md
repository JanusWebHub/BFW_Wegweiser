# Review of the wing 3 to 7 outputs

I've read all five wing outputs. The review itself changed nothing; afterwards the C2PA block was stripped from the five SVGs (see Housekeeping). The analysis scripts are in `docs/utilities` (`wing_check.py`, `wing_merge_check.py`, `wing_gap.py`).

## Mechanical checks: all pass

| Wing | Zones added | Portals added |
| --- | --- | --- |
| 3 kitchen | 15 | 30 |
| 4 north-west | 20 | 26 |
| 5 long wing | 39 | 36 |
| 6 IQ+UKM | 8 | 10 |
| 7 hexagon | 18 | 21 |

- **Base untouched:** no base zone or portal was removed or changed, and no base geometry or shell moved.
- **Ids:** every id follows the rules, and the portals are sorted correctly.
- **SVG and JSON:** they match one to one in each wing.
- **Portal lines:** each lies on its boundary, and each midpoint matches its point. Exit flags appear only on portals to `exterior`.
- **Overlaps:** none.
- **Merge simulation in memory:**
  - No duplicate zones or portals, and no overlaps between wings.
  - The result has 164 zones and 179 portals, and both counts add up.

## Housekeeping

- The five SVGs contained a C2PA metadata block, even though the reports say Claude Design removed it. The block has been stripped from all five files with a script. Zone and portal ids are unchanged and the XML still parses.
- The SVGs still have no `<style>` and render as black shapes. The merge has to add one. Two styles exist: the warm one in `docs/data/bfw-eg.svg` and the green one in `steps-2.5-3.5/bfw-eg-style-2.5-3.5.txt`. The choice is still open.
- `tmp_wing7-2.7-3.7.json` was a stray working file of the wing 7 session, with an outdated draft of its zone polygons. It has been deleted.

## Needs your decision

1. **Corridor `E.flur-tr3-1` is offset from the real corridor.** This is the biggest issue.
   - Wing 6 measured it: the corridor sits up to about 22 units off, and it proposes replacing the corridor.
   - Wing 5's rooms also sit on this corridor. Wing 6's rooms and portals depend on it as well.
   - A fix moves the corridor edges and every portal on them, including wing 5's seven proposed step 4 doors. I'd decide this before step 4.
2. **Unclaimed area in wing 6.** After the merge about 5.6% of the wing 6 shape is uncovered.
   - It is the room west of `E.71` and the unlabelled area east of it, plus the Lager triangle (wing 6's proposed `E.lager-tr3`).
   - Wing 6 said "wing 5 please decide", but wing 5 couldn't see it, and wing 7 doesn't cover it either. The only real gap I found.
3. **Other skeleton proposals:**
   - Wing 3: `E.41` is open to the corridors, so those may be one space. Also extend `E.flur-tr8-3` to y 941.
   - Wing 4: split `E.flur-tr5-2` at the fire door at x 877, and add a portal there.
   - Wing 7: extend `E.flur-tr4-3` and `E.flur-tr4-1` to the wall, and fix the hairline gaps on the shell.
4. **Room identity and crossability guesses:**
   - Wing 5: E.23, E.27 and E.28 have different numbers on the Lageplan and on 052/053.
   - Wing 4: the Claude Design wing 4 session made `E.66` crossable only because it read the `E.67a` opening as belonging to `E.66`. If the opening belongs to `E.67` or to both rooms, the crossable room changes.
   - Wing 7: `E.82` and `E.83` are crossable only on the guess that E.82a and E.83a open into them.
5. **Exits:**
   - Least certain: `E.41b_exterior`.
   - Positions placed from signs only: TR1, TR3, TR6 and the Durchgang.
   - Signs with no door in the outer wall, so no portal: TR2, TR4, TR8.
6. **Assumed doors.** There are many, for example one centred door per office in wing 5. They are flagged in the reports, and you can check them on site.

## Still unconnected after the merge

These are waiting for step 4, and the proposed portals are already in the wing 5 report:

- `E.23`, `E.27`, `E.28`, `E.30`, `E.37` and `E.abstell-e37`
- `E.25a`, `E.25b` and `E.vr-e25`, which form a separate group
- `E.flur-tr7-4`

Every stairwell has at least one portal.

## Proposed next steps

1. You decide items 1 to 3, and I'd draft the answers.
2. I write the merge script, which adds the chosen style. It writes into a new folder, so the base set stays as it is.
3. Wing 8 and step 4 follow in Claude Design.

Should I go ahead with step 2 before you've decided items 1 to 3? The merge doesn't depend on them.
