Steps 2.6 and 3.6 are drawn and the three files are updated, but the rooms only fit the skeleton loosely. The corridor E.flur-tr3-1 is 10–22 units off the real corridor, and rooms have to share its edge exactly. E.29, E.31 and E.33 come out too big, and E.32 and E.34 come out with the wrong size. I did not change the corridor; the report proposes new wall lines for it.

Rooms (71 zones plus exterior): I added 8 wing 6 zones: E.71, E.29, E.31, E.33, E.33a, E.32, E.34 and the lift E.aufzug-tr3. The lift is the only room made crossable.
Portals (66 in total): I added 10 — 7 doors from rooms and the lift to the corridors, 1 door between E.33 and E.33a, the TR3 door, and the TR3 Notausgang. There are no virtual portals in this wing. I did not check the SVG in the preview myself; my own geometry checks found no overlaps, and every portal sits on its boundary to within 0.01 units.
Lager missing: The Lager next to TR3 is not drawn because it lies inside E.flur-tr3-1. The report proposes cutting it out of the corridor.
Assumed doors: The doors of E.29 and E.33, the lift door, the E.33/E.33a door, the TR3 door and the exit position are assumptions.
Uncovered areas: Nothing was added for rooms that belong to wings 5 and 7, so some areas stay empty for now. One of them is the unlabelled area beside E.71.
SVG file: The attached bfw-eg.svg again had an empty defs and a metadata block. I removed the metadata and restored a style element, so please check the style (colours and fonts are my choice).
Files are in uploads/:

bfw-eg.svg
connectivity-graph.json
zoning-report.md