# Implementation plan

The rulebook and system-design define what the system is and must be. This document lists the planned implementation targets, outlining in detail the nature of each and the constraints, properties, and criteria it must satisfy.

## Phases

<!-- future chronological ordering outstanding -->

- Validated floor-plan asset. Produce a semantic SVG that represents the navigation model and satisfies the SVG implementation contract.

- Topology extraction and compiler handoff. Parse the authored asset, derive the zone index, segment list, connectivity graph, and routing graph, and serialize the resulting routing data for the browser client. Derived representations are not authored separately.

- Zone queries and route search. Implement queries between zones, directed states, canonical alternating routes, and lowest-cost search.

- Movement geometry and costs. Implement movement zones, movement lines, segment distances, and special costs assigned to states and segments.

- Validation and testing. Validate authored plans, serialized routing data, and route behavior at their respective system boundaries.

- Facility coverage. Extend the validated asset and compiler pipeline to the complete building.

## SVG implementation contract

authored SVG is subject to an operational contract that ensures parseability and conformance with the model.

The SVG representation has:

- semantic groups for zones, portals, and obstacles
- absolute coordinates in the shared `viewBox`
- stable ids for zones and portals
- portals that reference exactly two zones
- at least one portal for every zone
- no transforms on routing groups
- no dangling portal references
- no editor metadata in routing assets
- consistent coordinate conventions across floors
