# Implementation plan

The following implementation targets are unordered.

- Validated floor-plan asset. Produce a semantic SVG that represents the navigation model and satisfies the SVG implementation contract.

- Topology extraction and compiler handoff. Parse the authored asset, derive the zone index, segment list, connectivity graph, and routing graph, and serialize the resulting routing data for the browser client. Derived representations are not authored separately.

- Zone queries and route search. Implement queries between zones, directed states, canonical alternating routes, and lowest-cost search.

- Movement geometry and costs. Implement movement zones, movement lines, segment distances, and special costs assigned to states and segments.

- Validation and testing. Validate authored plans, serialized routing data, and route behavior at their respective system boundaries.

- Facility coverage. Extend the validated asset and compiler pipeline to the complete building.
