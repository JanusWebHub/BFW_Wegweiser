~~# Wegweiser — Zoning guidelines~~

~~How floor plans become zones, portals and obstacles, authored as one semantic SVG per floor.~~

~~## Phase A — Hybrid AI Vectorization (current)~~

~~Tool: **Claude Design**, operated in supervised hybrid mode.~~

~~1. Submit the source material (emergency plan photo, `Lageplan EG` PDF) with the authoring contract above as explicit instructions.~~
~~2. The model emits a schematic SVG: simplified geometry, wall thickness, door leaves, furniture and dimensions removed; zones and portals tagged.~~
~~3. **Human supervision is mandatory and is the quality gate.** Verify against the source: room numbering, adjacency correctness, portal placement at real door positions, corridor connectivity, missing rooms.~~
~~4. Correct by direct SVG edit or by iterating with the model; normalize transforms, strip metadata and chrome.~~
~~5. Commit the reviewed floor SVG to `web/assets`.~~

~~Source hierarchy: the `Flucht- und Rettungsplan` (2026) supersedes the `Lageplan EG v1.2` (2018) wherever they disagree — room numbering has drifted and the personal names on the older plan are stale. The Lageplan remains authoritative for wing layout and overall geometry.~~

~~Architectural door notation matters when reading the source: a door is a line plus a quarter-circle arc. Solid black blocks are wall thickness, not doors — misreading them produces doubled portals.~~

~~Rationale: this collapses the former "trace walls, then place nodes, then transcribe coordinates" sequence into a single supervised pass, and it scales to further floors and wings without per-floor manual drafting.~~

~~Residual risk: the model infers geometry it cannot read from a blurry source. Mitigation is review discipline, not tooling — every zone and portal is checked against the official plan before it is trusted for routing.~~
