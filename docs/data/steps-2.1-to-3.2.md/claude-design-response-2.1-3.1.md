Step 1 (skeleton of the whole EG) is ready for your review. I've written bfw-eg.svg, connectivity-graph.json and zoning-report.md, and opened the SVG for you.

What's in it:

The building outline plus eight rough wing shapes, which are for display only.
37 zones: all 26 corridor sections, the Durchgang, the Foyer, and stairwells E.TR1 to E.TR9.
21 virtual portals where a corridor is split. Where two corridors meet at a door, the portal waits for the portal step.
units_per_meter = 11.1, the mean of E.90, E.91, E.62, E.59 and E.60 (they range from 10.8 to 11.5). With this value the Terrasse comes to 146 m², against 142 m² printed.
I checked the files by script: portal lines lie on the shared boundaries, no zones overlap, and all zones are inside the outline. The only validity rule not met is "every zone has at least one portal". The stairwells, two door-only corridors and exterior have no portal yet, which the brief allows at this step.

Readings you need to decide on (all listed in the report):

TR2: the Lageplan shows a stair vestibule, but 052 and 053 show a Flur passing between the stair and E.21. I split the Lageplan space into the stair and a two-piece passage.
North-west wing: the Lageplan has E.68 across the west end. 060 and 061 show the Flur running on to TR5, so I extended the corridor there.
Durchgang: I placed it at the step in the NW corridor, next to the junction.
Foyer: its edge against the Flur isn't drawn on any plan. I read it from the shading on 055 and 057.
E.63: the scan cuts off its east corner, so I extended the end wall along its slope. That gives about 103 m², against 102.10 printed.
Names:
The corridor from the middle area to the NW wing has no stairwell of its own. I named it E.flur-tr7-4 because it joins the TR7 corridors.
The corridor along E.56 and E.57 appears on both 058 and 055, so it goes to the earlier wing as E.flur-tr9-3.
The short corridor to E.66a became E.flur-tr5-4.
I also added a short github.md linking the project to the BFW_Wegweiser repo, which you didn't ask for.

I'll wait for your approval before starting step 2.1 (rooms of the east block).

Created 44 files
Step 1 approved, with these changes: remove the metadata block from the SVG, add a style element in defs. where is github.md? Keep the listed readings; I will check TR2, Durchgang and the Foyer edge on site. Then continue with step 2.1.
I fixed the SVG and added the east block rooms (step 2.1); the SVG is open for you. The skeleton is unchanged.

SVG fix: my first save had wrapped the SVG in a metadata block and dropped the contents of the style element. It is now saved as plain text: no metadata block, and a single <style> inside <defs> that holds all colours and fonts. The geometry did not change.

github.md: it is in the project root. It records the repo (JanusWebHub/BFW_Wegweiser, branch main) and where the two files belong in it, and I've updated it for this step.

Step 2.1: 18 rooms added, so the graph now has 55 zones plus exterior. The script found no overlaps and no gaps in the east block, and the step 1 portals still sit on their boundaries.

Crossable: R.58 is new, because the only door of E.58a opens into it. E.52 and the two VR anterooms are crossable by category.
Renumbered: the two Büros printed E.59a and E.59b are E.60a and E.60b, per the known correction.
Decisions needed (all in the report):

E.59b Elt: 058 and 059 place it at corridor level, inside the hall zone E.flur-tr9-1 you approved in step 1. To leave the skeleton alone, I drew it in the corner of E.59 just below that spot. I propose cutting it out of the hall instead; that changes the skeleton, so it needs your OK.
E.56b / E.56c: the Lageplan shows one room, E.56, where 058 shows these two. I drew both inside the old E.56 outline. If that's right, step 2.8 only has E.56a left in that row.
Wachdienst: it sits where the Lageplan has "Infodienst". Please confirm they are the same room, so the middle-area step doesn't draw Infodienst again.
E.56b has no label printed on either plan, so its label is empty.
The step 1 readings stay as listed for your site check (TR2, Durchgang, Foyer edge). I'm stopping here until you approve; step 3.1 (the east block portals) is next.

Edited 11 files
Step 2.1 approved with one change: cut E.59b Elt out of E.flur-tr9-1 where 058/059 show it; this skeleton change is allowed. E.56b/E.56c inside the old E.56 are correct. Wachdienst and Lageplan Infodienst are the same room. Then continue with step 3.1.
I cut E.59b Elt out of E.flur-tr9-1 and gave that corner back to E.59, then added the east block portals (step 3.1). The three files are updated, and the SVG is open for you.

What step 3.1 adds: 25 portals, so the graph now has 55 zones plus exterior and 46 portals. That is 22 doors or openings and 3 exits:

E.52_exterior is the Haupteingang, marked as both main entrance and emergency exit.
E.52_exterior_2 is the Notausgang at the south-west corner of E.52.
E.61_exterior is the Notausgang in E.61's south wall.
The script check finds every portal line on its shared boundary and no overlaps. Every east block zone now has at least one portal.

Please check:

Assumed doors: neither plan shows a door for E.56b or for E.59b Elt. I placed E.56b's on the corridor and Elt's on its hall side.
Assumed positions: the WC and anteroom doors are too small to place exactly, so each is centred on its wall.
Read from 058 only: a second door for E.62 into R.58. I can't see it clearly on 059.
Merged or split:
E.59's two door arcs are only about 2 m apart, so they are one portal.
Wachdienst's two doors are about 7 m apart, so they are two.
Possible exit: a small stair symbol at R.58's outer corner has no exit sign and is cut off on both plans, so I didn't treat it as an exit.
The two doors between the east block and wing 2 are left for step 4, as the brief says.

I'm stopping here until you approve; step 2.2 (entrance and foyer rooms) is next.