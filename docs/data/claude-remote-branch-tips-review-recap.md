# Handoff recap: Wegweiser routing graph and EG floor plan work

Dates: 2026-09-28 to 2026-09-29. Repo: JanusWebHub/BFW_Wegweiser (local workspace: wegweiser).

## Assistant rules from the user

- Be transparent about what is being done and ask permission before any tool call or action.
- Keep answers short. No em dashes, no bold in documentation prose, no ALLCAPS, no relative links between docs. Use careful, hedged language in docs.
- Avoid vague or performative vocabulary (for example "contract"). Use the user's terms: adjacency graph, connectivity graph, routing config, routing graph.
- The user runs state-changing git commands. Nothing has been written to the repo so far.

## Repo state (as reviewed)

- local/simpler (490ae5a) is the newest direction: only planning docs under docs/design/, no code changes. Idea: build a working router in small testable steps from a demo graph, real building data only at the end. Route search is offline; the browser only looks up precomputed routes and never tracks position.
- Inconsistencies in those docs are exploration material; the user said not to get hung up on them.

## Agreed graph model (current valid version)

Three graphs, in the user's words:
- Adjacency graph: from architectural plans. Spaces are nodes, separators (walls) are edges. Deferred.
- Connectivity graph: derived from the adjacency graph, created alongside the simplified semantic floor plan SVG. Zones are nodes, portals are edges.
- Routing graph = connectivity graph + routing config. Segments are computed while building it.

Connectivity graph (now):
- floors, zones (with floor, crossable), portals (with point, virtual flag authored with the portal; optional emergency_exit and main_entrance flags, only on portals to exterior).
- One single zone `exterior`, no floor, no floor prefix (rulebook 1.6 unchanged). A portal to exterior takes the floor of its other zone.
- units_per_meter written in the floor entry for now. Zones must be drawn roughly convex (zoning person's responsibility).
- Segments are not authored. They are straight lines between every pair of portals in a crossable zone, computed from zones and portals (rulebook 3.2 requires all pairs). Distance equals line length times scale.

Routing config (separate file): extra state costs and segment costs, per direction, default equal both ways unless authored; variants as named lists of extra non-crossable zones. Stair climbing effort is a state cost (no length_m on vertical portals). Vertical portals (stairs, lifts) join zones on two floors; deferred for now while only EG is drawn.

Validity rules (agreed): unique ids; portal joins two different existing zones; every zone has at least one portal (only enforced after portal step); segments only in crossable zones between two different portals; at most one segment per portal pair, and in crossable zones every pair has one; non-crossable zones have no segments; costs and distances >= 0; cost keys refer to existing crossings or segments.

Search rules: start and target zone in; start equals target is an invalid query (skipped/rejected); intermediate zones must be crossable, start and target may be non-crossable; unreachable is a valid answer; cost = segment distances + segment extra costs + state extra costs including the first crossing.

Ids:
- Zone id = room number as printed (E.62, R.58, E.53.1). Numbers printed on several floors get the floor code (E.TR9, 1.TR9). Made-up names lowercase with `-` between words (E.flur-tr1-1). Split zones get `-1`, `-2`. Name clashes get letters (E.aufzug-tr2-a, -b). No `_` in zone ids, all ids unique. No rule that ids start with a floor code.
- Portal id = both zone ids sorted, joined by `_` (E.62_E.flur-tr9-1), `_2` for a second portal between the same zones. Kept derived for readability; can switch to independent ids later.
- State and segment keys use `|` (portal|zone|portal).
- SVG ids: `zone-<id>`, `portal-<id>`.

Files planned: connectivity-graph.json, routing-config.json, routing-graph.json in data/ (routing graph is committed, not ignored); demo versions in src/fixtures/.

Deferred to later levels: adjacency graph format, movement lines and how portals connect to them, obstacles inside zones, walked-distance realism, rulebook additions for floors and vertical portals and several exterior zones, how the SVG supplies units_per_meter (root attribute or width/height in mm), analytics (separate branch), Notausstieg (escape windows) as possible variant, merging of anterooms.

## Sources and zoning decisions (EG)

Sources:
- Lageplan BFW BB_Charlottenburg, EG, Stand 23.01.2018, v1.2 (scanned PDF, upside down, no scale bar, some room areas printed, smear on right edge). Decides outline, wing shapes, scale. Only source for the middle area (numbers there unverified).
- Rettungspläne B 7967_052 to 061, 07.05.2026 (10 photos, angled, no scale). Decide room division, walls, doors, numbers, labels, exits. Not usable for geometry.
- Every discrepancy goes into the report for the human to decide. Where sources disagree the escape plans may also decide walls, the Lageplan then only gives outline and scale.
- Scale: neither source has a scale bar. Take it from printed room areas of rectangular rooms (square root of SVG area over m2), at least two rooms in different wings.
- About 100 rooms, wings meet at 60 degrees. The Lageplan is stored upside down, a smear clips the E.63 and E.61 labels. Stairwells are numbered TR1 to TR9 on the escape plans; lifts and corridors are unnumbered. The 2026 plans renumbered and added rooms since 2018 (the older prototype's R.58, E.52, E.56b/c and Wachdienst are right for 2026).
- Coverage gap: no photo covers the middle area (E.48, E.49, Speisesaal, E.53.1/2, E.56/E.56a, Infodienst, diagonal corridor to the NW wing). Follow the Lageplan there and mark its numbers unverified; the user photographs it later.

Decisions:
- E.59a/E.59b (Büros) are really E.60a/E.60b; the Elt room stays E.59b. Hexagon room above E.80 treated as one zone E.84 (user to check).
- Draw fine, merge later (merging is an important open decision; it only removes a portal, splitting needs redrawing): every numbered room, anteroom (VR), technical or storage space is its own zone. Kitchen E.41a to E.41i own zones, non-crossable. Anterooms named after the WCs behind them (E.vr-e50b). Technical spaces named like E.technik-tr5.
- Large spaces own zones: E.foyer, E.speisesaal, E.durchgang, E.vorraum-e50, E.terrasse (crossable). Infodienst is the same room as Wachdienst (confirmed), non-crossable.
- E.53.1 and E.53.2: two zones joined by a virtual portal.
- Corridors named by the stairwell at the wing end: E.flur-tr1-1, -2 ... Stairwells E.TR1 to E.TR9. Lifts named after their stairwell (E.aufzug-tr7). Umlauts as ae/oe/ue.
- Crossable: circulation spaces, Speisesaal, Terrasse, E.52 (exceptional), plus any room that is the only access to another room (E.41, R.58). Everything else non-crossable; each case listed in the report.
- Exits: doors marked Notausgang and the Haupteingang become portals to exterior (flags emergency_exit, main_entrance). Exits through stairwells are portals from the stairwell zone. Notausstiege left out.

## Drawing rules given to Claude Design (SVG and JSON)

Goal: simplified semantic floor plan SVG plus connectivity-graph.json for the whole EG, from the Lageplan and the escape plan photos. The earlier east wing prototype's ids and markup must not be reused. The rules live in zoning_guidelines.md (sources, zoning, ids, SVG markup, report, passes) next to graph_format.md; the old zoning guidelines were used only selectively.

SVG markup:
- One viewBox, absolute coordinates, no transforms, no editor metadata, a single style element in defs. Later floors use the same viewBox and origin.
- One group each for shell, zones, portals, labels. Ids zone-<id> and portal-<id> as real XML ids (chosen over data- attributes; the prefix is needed because ids like 1.TR9 start with a digit). Every JSON zone and portal has exactly one matching SVG element.
- Portals are drawn as a line on the shared boundary with its midpoint marked (rulebook 1.4), not as bare circles. Virtual boundaries are dashed.
- A room enclosed by another room is cut out of the outer shape as a hole. No overlaps, no gaps (rulebook 1.2), zones roughly convex, two zones must share a wall, not only a corner.
- Simplify: drop wall thickness, door leaves, furniture, dimensions. A door in the plan is a line plus a quarter-circle arc; solid black blocks are wall thickness, not doors. Adjacent double doors are one portal; far-apart doors between the same zones are separate portals.
- Movement lines and obstacles are left out entirely for now.

JSON and report:
- provenance values demo, unverified, verified; the prompt asks for unverified. No vertical portals while only EG is drawn; stairwells and lifts go into the report.
- Report lists: unclear numbers and labels, assumed doors or openings, merge candidates (for example WC anterooms), rooms made crossable, stairwells and lifts, how the scale was measured, every source discrepancy, numbers that come only from 2018. Instruction: list uncertainties instead of guessing.
- Validity checks apply only to what exists so far; a zone may lack portals until its wing's portal step.
- Rooms shown on two wings' plans belong to the earlier wing in the order, so no room is drawn twice.

Pass design (single prompt, stop-gated): coarse to fine, skeleton first and frozen, then per wing rooms then portals, then a whole-building check. The prompt says: stop after each step, never start the next on your own, do not change approved work unless asked, steps are numbered, any step can be restarted in a fresh session with the approved files attached. To start: attach Lageplan PDF, all 10 photos, zoning_guidelines.md, graph_format.md, paste prompt.md, add "Start with step 1." Later replies: "Step N approved. Continue with step M." or specific corrections.

## Claude Design workflow

Files produced in Claude chat (not in this workspace; re-supply if needed): zoning_guidelines.md, graph_format.md, prompt.md (stop-gated steps), an HTML artifact of the format, parallel-message files per wing. Claude Design outputs bfw-eg.svg, connectivity-graph.json, zoning-report.md.

Steps: 1 skeleton for whole EG (outline, corridors, Durchgang, Foyer, stairwells, virtual portals, scale); then per wing 2.N rooms and 3.N portals; step 4 whole-building check and cross-wing portals. Stop after each step for approval; earlier approved work stays frozen unless the user allows a change.

Wings: 1 east block (058, 059); 2 entrance and foyer (055, 057); 3 kitchen (056); 4 north-west (060, 061); 5 long wing (052); 6 IQ+UKM (053); 7 hexagon (054); 8 middle area (Lageplan only).

Models: Opus 5.5 for step 1, step 4 and wing 8; Sonnet 5.5 (selectable, released 2026-09-28) for wings if a comparison on one wing looks as good; no Haiku. Merge parallel results by script.

## Progress

- Steps 1, 2.1, 3.1, 2.2, 3.2 approved. Graph now has 63 zones plus exterior and 56 portals, covering the east block and entrance/foyer wing fully. Other wings only have the skeleton.
- Skeleton change allowed once: E.59b Elt cut out of E.flur-tr9-1.
- Full step results and readings are in zoning-report.md. Step 1 gave 37 zones, 21 virtual portals, units_per_meter 11.1 (mean of five rooms, range 10.8 to 11.5). Later steps added rooms and portals for the east block and entrance/foyer wing. Exits so far: E.52_exterior (main entrance and emergency exit), E.52_exterior_2, E.61_exterior. Naming examples: E.flur-tr7-4, E.flur-tr9-3, E.flur-tr5-4, E.wc-beh-e50b, E.aufzug-tr7.
- Order alternates: 2.1, 3.1, 2.2, 3.2, and so on. Parallel wings use combined messages ending "Do steps 2.N and 3.N now, in the order above, then stop." with a self-check and correction between rooms and portals.
- A clean base set (SVG without C2PA block, style element restored, verified against JSON) replaced the old three files in the project folder.
- Plan: run wings 3 to 7 in parallel sessions from the base set, using five ready-made messages (N filled in). The skeleton stays frozen there; needed changes are only reported. 052 and 053 overlap around E.21 to E.30, so those rooms belong to wing 5. Keep the Claude Design GitHub repo attachment on None (old contradictory material).
- Next: run the five sessions, collect results, merge by script (check duplicate ids, overlaps, junction portals, validity), then wing 8 and step 4 in one Opus session.

## Known issues and watch points

- Downloads from Claude Design carry a C2PA metadata block and lose the style element in defs (unstyled SVG renders black), although its own file seems correct, so the export step is the likely cause. Strip and restore by script before anything goes into the repo. It also wrote an unrequested github.md; ignore it.
- The user must check on site: TR2 passage between stair and E.21, Durchgang position, Foyer edge, E.62 second door into R.58, assumed doors (E.56b, E.59b Elt, E.50b, lift E.aufzug-tr7), closed Terrasse to Foyer wall, stair symbol at R.58 as possible exit, Beh. WC (own zone or part of E.50b), E.84 hexagon room, E.56b/E.56c inside old E.56.
- Graph currently unconnected across wings; cross-wing doors come in step 4 (for example east block to wing 2, E.flur-tr7-1 to E.53.1/E.53.2, E.flur-tr7-2 to Speisesaal).
- Long sessions with Claude Design lose prompt cache; restart with the same prompt, guidelines, format, and last approved three files, plus a line stating which steps are approved.
