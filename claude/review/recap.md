# Recap (2026-09-29 to 2026-10-01)

## Project and setup
- Repo `JanusWebHub/BFW_Wegweiser`, branch `local/simpler`, working copy `/home/user/BFW_Wegweiser` at `11ba7b5`, clean.
- Goal: a simplified EG plan SVG plus connectivity graph for BFW Charlottenburg. Graph = zones and portals; routing graph adds computed segments (straight lines between every portal pair inside a crossable zone; distance = length / `units_per_meter` 11.1). Specs: `docs/data/zoning_guidelines.md`, `docs/data/graph_format.md`.
- Pipeline: Claude Design drew it in stop-gated steps (skeleton, wings 1 to 8, merge). You approved steps 1 to 3.2 only; wings 3 to 7 and the step 8 merge were never approved. I read only what was added after 490ae5a.
- Sources: 10 escape-plan photos B 7967_052 to 061; Lageplan PDF (stored upside down; `SVG = scan px − (40,77)` at half size after turning 180°); SVG frame viewBox 0 0 1790 1000.
- Your preferences: extremely brief answers; restate each correction in one line; collect corrections and apply only when told; don't send files at every correction; no pushes.

## The review
Report: scratchpad `review/review-report.md`, figures `fig1` to `fig4`.
1. **Disconnected graph.** Long wing, IQ+UKM wing and hexagon cut off; from `E.52`, 80 of 172 zones unreachable. The step 4 "reachable" claim held only through exits. Missing: a fire door and two double doors.
2. **Step 8 broke the frozen skeleton:** 3.4 m² overlaps, 11.9 m² gaps, 1.9 m² outside the shell. Reports called them "slivers"; the checks missed them.
3. **Merged SVG markup:** C2PA block, no style. Three competing styles existed; I recommended the warm palette with green portal coding.
4. **Content errors:** `E.flur-tr2-5` is a room, not a corridor; `E.33` must be crossable; `E.53.1`/`E.53.2` lack a virtual portal; exits missing for `E.48` and `E.TR8`; `TR3` Lager missing.
5. **Other:** `E.flur-tr3-1` off by 10 to 22 units; 71 of 885 segments leave their zone (`E.41`, `E.52`); step 8 report lacks the wing 3 to 6 sections; about 84 of 179 non-virtual portals are assumed.
6. **Verified correct:** base untouched; SVG matches JSON in all 7 sets; merge is exactly 171 zones and 206 portals.

## Corrections
Full account in `CORRECTIONS.md`. Applied in my working graph (`fixed.py` plus `batch2.py`), not in the repo. Rounds: early cut-out fixes, kitchen (12 marks), batch 2 (75 marks), hub redraw (10 marks).

**Current state:** 178 zones, 207 portals (32 virtual, 14 exits), one connected component, 0 overlaps, gaps 740 units² (was 1459), 54 units² outside shell. Doors within 0.6 of a boundary except 8 off by 0.6 to 1.3. Sample routes: `E.01`→`E.52` 111.9 m, `E.72a`→`E.62` 123.8 m, `E.90`→`E.60a` 79.9 m, `E.34`→`E.41a` 73.8 m, `E.33a`→`E.02` 76.0 m.

## Concepts approved
- Zone kind `block`: inaccessible space (shaft, wall mass, obstacle, ventilation, counters). Never crossable, no portal, exempt from "every zone has a portal" and reachability, neutral colour, hatched.
- Nested rooms: cut out of the host (notch or hole); the host–nested door is a normal portal; the host is crossable only when it is the only access (existing rule, not an exception).
- Door policy: doors lie on zone boundaries (≤0.6). Drawn doors win: wall moves up to 4.5 units, otherwise door snaps to the wall. Where your drawn boundary and a door disagree, the door adapts to your boundary.
- Hall/corridor splits: whole shared edge is one virtual portal.
- Written in `claude-folder/review/SPEC-PROPOSALS.md` (not yet in `docs/data`).

## Redline page (EG Redline artifact, version 12)
https://claude.ai/artifact/1s54MKxn2Y6afHkv17D9KR
- Tools: pan, move door, add door, wall/cut, zone outline, note, remove. Marks stored in `marks` collection as SVG coordinates. All 97 marks so far (12 kitchen, 75 batch 2, 10 hub) are `applied`.
- Added: grid layer, applied-marks toggle, cursor x/y, block hatching, **Style panel** (Lageplan opacity default 45%, fill strength, outline strength, outline colour, grey Lageplan, colour pickers for circulation, vertical connections, crossable rooms, other rooms; reset; saved in the browser).
- Style: original warm palette kept as the base. Circulation (corridors, plus lifts/anterooms that are not stairs) strongest; vertical (stairs, `aufzug`) separate taupe; crossable rooms (including terrasse, foyer, Speisesaal) light sand; other rooms near-white cream. Fill ratio circulation 60 / vertical 55 / crossable rooms 40 / other rooms 30 %. Indigo `#2f3fa8` outlines, thicker, over a greyscale Lageplan.

## Other deliverables and status
- `claude.zip` (619 KB) sent earlier; now outdated (lacks page v12, `fixed.py` with kitchen and batch 2, updated JSONs).
- Push of a `claude/` folder (tools plus review, no images) failed with 403: the Claude GitHub App has no access to your org repo. Local commit reset, folder moved out of the repo, zip sent. Never retried.
- `TIDYUP-PLAN.md` (in the zip): make scripts runnable (path config, `make_lageplan.py`, `run_all.py`).
- Known gap: the session scripts are a snapshot. Paths are hard-coded, several scripts read each other's source text, and they need Lageplan renders that are not included, so they do not run as they are (see `review/scripts/README.md` and `TIDYUP-PLAN.md`).
- Side-by-side render of original versus current colours sent.

## Superseded
Earlier proposals A to F are resolved by your drawings: `E.53.2_E.flur-tr7-1` moved and `E.53.2_E.foyer` removed, `E.52_E.speisesaal` removed, TR7 lift redrawn.

## Open items
- Hub thin triangles held as drawn; you plan to carve the remaining polygons into triangles later.
- Write the `block` and nested-room rules into `docs/data`; add `kind` to the connectivity JSON.
  - Known gap: the exported connectivity JSON has no `kind` attribute yet, so blocks appear there as ordinary non-crossable zones (only the redline page hatches them, via its own `b` flag). Add `"kind": "block"` to the writer in `fixed.py` once the spec is accepted.
- Regenerate routing images and JSONs; re-package the zip (no PNGs in the repo).
- Skeleton and middle area: arc at x 1061–1072 on the `E.flur-tr5-2` south wall; `E.flur-tr3-1` refit; convexity splits for `E.41` and `E.52`; middle-area gaps (part of the 740 units²); `E.flur-tr2-6` identity; `E.TR8` exit (door leaf seen on photo 056); assumed doors and door review images A to F only partly checked; bridge opening to the Speisesaal (virtual portal is my assumption).
- 8 doors still off boundary by 0.6 to 1.3: `E.flur-tr2-5_E.flur-tr4-2`, `E.53.1_E.53.2`, `E.41b_E.flur-tr8-6`, `E.56a_E.flur-tr9-3` and `_2`, three virtual hub portals.

## Update (2026-10-02)
- Geometry rewritten to follow your drawn outlines exactly (no growth/smoothing); see CORRECTIONS.md rounds 6 to 8. Page: style panel, suggestions layer (28 current items), newest marks on top.
- Current graph: 193 zones, 219 portals, one component, 0 overlaps. Marks in db: all applied (236 total).
- Open: hub thin triangles (later), `block`/nested-room rules into `docs/data`, `kind` attribute in the JSON, runnable scripts, door `E.TR9_E.flur-tr9-1` 4.2 off wall, stair outlines vs Lageplan, assumed doors (about 84 originally) unverified.
