graph_format.md
Grafik_Etage_BFW_rotated180 1.pdf
Steps 2.3 and 3.3 are done: 15 kitchen zones and 30 portals added. I did not render the SVG. It is checked numerically only: portal lines lie on their zone boundaries, and there are no overlaps or gaps in the wing. Nothing that already existed was changed.

The three files are in the project root: bfw-eg.svg, connectivity-graph.json and zoning-report.md (the report has only the new 2.3 and 3.3 sections added). The graph now has 78 zones plus exterior, and 86 portals.

Rooms: E.41 and E.41a–E.41i, E.lueftung-e41, E.42, E.43, E.aufzug-tr8-a and E.aufzug-tr8-b. E.41 is crossable because it is the only access to other kitchen rooms; the lifts are crossable by category.
Portals: 27 doors or openings and 3 exits: the east diagonal at E.41, the east diagonal at E.41b, and the south wall at E.flur-tr8-3.
Assumed doors: E.41_E.41h_2, E.41c_E.flur-tr8-3, E.41b_E.flur-tr8-3, E.flur-tr8-3_E.lueftung-e41 and E.TR8_E.aufzug-tr8-a are guesses, listed in the report. I am least sure of the E.41b_exterior position.
Skeleton edges cutting open floor:
E.41 is open to E.flur-tr8-1 and E.flur-tr8-2 where the skeleton splits the floor. I drew these as real portals and listed a proposal in the report.
The bottom wall of E.43 lies at y 941, but the skeleton corridor E.flur-tr8-3 starts at y 948. I proposed extending the corridor rather than changing it.
TR8 Notausgang: plan 056 shows a Notausgang sign at the TR8 landing, but I couldn't read a door to the outside. I did not draw it, so E.TR8 has no exit. Please decide where it goes.
SVG file: the uploaded bfw-eg.svg again had an empty defs and an embedded metadata block. I removed the metadata and restored a single style element with colours and fonts I chose, as in the earlier steps. Please check the style is what you want.