Step 2.2 (rooms of the entrance and foyer wing) is delivered as bfw-eg.svg, connectivity-graph.json and zoning-report.md. The report has a new "Step 2.2" section. I haven't looked at the drawing myself, and the checks below cover overlaps and area only. A background review is running.

I added 8 zones, so the EG now has 63 zones plus exterior:

Terrasse: E.terrasse, crossable, 144 m² against 142 m² printed.
Pförtner: E.51.
Toilets: E.50b (WC D), E.wc-beh-e50b (Beh. WC) and E.50a (WC H/Beh.-WC).
Anterooms and lift: E.vr-e50b, E.vorraum-e50 and E.aufzug-tr7, all crossable. The lift is the notch that step 1 left out of E.TR7.
The skeleton and step 2.1 are unchanged. Sampling every 2 units found no overlaps. The new rooms have no portals yet, which is step 3.2. Two small gaps remain inside the wing and are in the report. One is a sliver at the Terrasse's west end. The other is the strip south of the Foyer corridor, which is left for the Speisesaal in step 2.8.

Things I need you to check, all listed in the report:

Style block: the uploaded bfw-eg.svg had an empty defs and a C2PA metadata block. I removed the metadata and restored one style element in defs. The colours and fonts are my choice, so please check them.
Beh. WC: the plans print it without a number next to "E.50b WC D". I drew it as its own unnumbered zone. If it is part of E.50b, the two zones must be merged.
Vorraum and toilet block, north edge: they sit on the existing corridor boundary at y 557, so the Vorraum zone includes a thick wall and is deeper than the room.
Please approve step 2.2, or tell me what to change, before I start step 3.2 (the portals of this wing).

Created 8 files
Step 2.2 approved. Keep the Beh. WC as its own zone for now; I will check it on site. The Vorraum depth is fine. Ignore the metadata/style issue in downloaded files; it is handled outside. Continue with step 3.2.
Step 3.2 (portals of the entrance and foyer wing) is delivered as bfw-eg.svg, connectivity-graph.json and zoning-report.md. The report has a new "Step 3.2" section. The EG now has 56 portals. I checked that each portal lies on the boundary of its two zones and that every portal has one SVG element and one graph entry. I haven't looked at the drawing.

I added 10 door portals and no virtual portals or exits:

Pförtner (E.51): doors to the Flur and to Wachdienst.
Toilets (E.50b, E.50a, Beh. WC): the VR's door to the Flur, the VR to Beh. WC, E.50b to the VR, and E.50a to the Vorraum.
Vorraum: its door to E.flur-tr7-2.
Terrasse: the double door from E.flur-tr7-3.
TR7: the double door to E.flur-tr7-2, and the lift door.
Two of these are assumed because no arc is readable on the plans: the E.50b door and the lift door. I left the Terrasse–Foyer wall closed because neither the Lageplan nor 055/057 shows a door there. TR7 has no exit portal, since 055/057 show no exit sign there.

I left the doors that touch other wings' zones for step 3.8 or step 4. They include the north doors of E.flur-tr7-1 to E.53.1 and E.53.2, and the door from E.flur-tr7-2 to the Speisesaal. All are listed in the report.

Please approve step 3.2, or tell me what to change, before I start step 2.3 (kitchen rooms).