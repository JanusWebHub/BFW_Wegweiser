# System design

This document specifies the current system design.

## 1. System architecture

The system has two parts:

- [src/](../src/) contains the offline Python tooling used to process the building model and generate routing data.
- [web/](../web/) contains the static browser client used to present the building plan and render route output.

## 2. Modeling pipeline

The system implements a human-in-the-loop, computer-assisted modeling pipeline with two complementary representation types:

- visual representations: architectural plans, simplified floor plans, spatial routing plans, and graph visualizations
- machine-readable symbolic representations: serialized graph models containing nodes, edges, and attributes

1. Architectural plans are interpreted into a machine-readable adjacency graph.
2. The plans and adjacency graph are used in zoning to produce simplified floor plans and a connectivity graph.
3. The routing graph is constructed from the connectivity graph.
4. Routing data is serialized for the browser client.
5. The browser renders routes on the building plan.

## 3. Representations

### 3.1 Authored representation

The authored floor-plan asset is a semantic SVG used to encode the model’s zone and portal structure.

It contains:

- zones
- portals
- obstacles
- the exterior zone

### 3.2 Derived representations

The following are derived from the authored representation rather than authored directly:

- zone index
- segment list
- connectivity graph
- routing graph
- serialized routing data (computed)

## 4. SVG implementation contract

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
