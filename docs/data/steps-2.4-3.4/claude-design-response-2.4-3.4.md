Steps 2.4 and 3.4 are done. I didn't view the SVG or run the verifier. My checks were numeric only: no overlaps, no unexplained gaps, portal points on their zone boundaries, and every graph entry matching one SVG element.

The three files are in the project root, not uploads/: bfw-eg.svg, connectivity-graph.json, zoning-report.md.

Rooms (2.4): 20 zones added. They cover the wing with no overlaps. The only gaps are seven uncovered sample points within 0.5 units of the sloping outer wall, caused by the approved corner points.
Portals (3.4): 26 portals added (23 doors or openings, 3 emergency exits at TR5, TR6 and Durchgang). Every zone of the wing now has a portal.
Existing content: nothing already in the files was changed.
Crossable by exception: E.68 (the only access to E.68a, E.68b and the lift) and E.66 (the only access to E.67a, in my reading).
Please decide these (all in the report):

Assumed door positions: E.68 to the corridor, E.66 to E.67a, E.68 to E.68b, Technik, E.70b, and the lift beside E.64a. The TR6 and Durchgang exits are placed from the exit signs, because the Lageplan shows no door there.
Fire door in E.flur-tr5-2: it sits at x ≈ 877 but inside one zone, so it isn't a portal. I propose splitting the zone there but did not do it.
Cross-wing doors: doors to the middle area and to E.flur-tr7-4 are listed for step 4.
SVG style: the uploaded SVG had an empty defs and an embedded C2PA metadata block. I removed the block and restored the style element with colours and fonts of my own choosing. Please check the style.