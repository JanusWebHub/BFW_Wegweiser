# Implementation plan

The rulebook and system-design define what the system is and must be. This document lists the planned development work of building the program itself, ordered into phases by dependency. Each phase outlines what to build (a script, a process, a test suite) and the constraints, properties, and criteria it must satisfy.

## Phases

Ordered by dependency: each phase builds on the previous phase's output.

1. Floor plan and connectivity graph. Zoning produces the simplified floor plan, authored as a semantic SVG, and the connectivity graph, together. The SVG satisfies the implementation contract. Validated by its own validator script, checking SVG contract compliance and graph connectivity. Minimal smoke test only; full coverage in Phase 4.

2. Routing graph and compiler. Parse the authored asset, derive the zone index and segment list, construct the routing graph from the connectivity graph using movement geometry, including segment distances and special costs assigned to states and segments, and serialize the resulting routing data for the browser client. Minimal smoke test only; full coverage in Phase 4.

3. Zone queries and route search. Implement queries between zones, directed states, canonical alternating routes, and lowest-cost search. Minimal smoke test only; full coverage in Phase 4.

4. Test suite. Review the minimal tests written during Phases 1-3 against the rulebook's constraints, close any gaps, and remove any duplication or contradiction between checks.

## Future direction

Distant, surface-level ideas, not yet detailed to the level of the phases above.

- Facility coverage. Extend the proven asset and compiler pipeline to the complete building.
- Adjacency graph. Interpret architectural plans into a machine-readable adjacency graph.

## Phase 1: Floor plan and connectivity graph

### Contract

The SVG representation has:

- semantic groups for zones, portals, and obstacles
- movement zones and movement lines
- absolute coordinates in the shared `viewBox`; the plan and the route overlay share one frame of reference, so they cannot drift apart
- stable ids for zones and portals
- portals that reference exactly two zones
- at least one portal for every zone
- no transforms on routing groups
- no dangling portal references
- no editor metadata in routing assets
- consistent coordinate conventions across floors
- the wing boundary made explicit as its own labeled zone
- virtual boundaries drawn as dashed lines

### Validator

A validator script:

- checks the authored SVG against the contract above
- verifies that every zone's portals are mutually reachable without obstruction
- verifies no overlapping zones
- verifies connectivity of the resulting graph

### Authoring procedure

1. Submit the source material with the contract above as explicit instructions.
2. The model emits a schematic SVG: simplified geometry, wall thickness, door leaves, furniture and dimensions removed; zones and portals tagged.
3. Human verification against the source is the quality gate: room numbering, adjacency correctness, portal placement at real door positions, corridor connectivity, missing rooms.
4. Correct by direct edit or by iterating with the model; normalize transforms, strip metadata and chrome.

Reading the source: a door is a line plus a quarter-circle arc.
