# Rulebook

This rulebook defines the project's conceptual model. Module specifications make module-specific design decisions, and the file-format specification defines how data is represented in files. All documents use these model terms consistently.

## 1. Floors, zones, boundaries, and portals

### 1.1

An architectural plan is a source representation of a floor. The plan tracer produces a plan SVG, a vectorized equivalent used as the zoning editor's reference underlay.

The zoning editor produces a zone SVG, a view of the modeled zones and portals, and a Navigation SVG for displaying routes.

### 1.2

A zone is a modeled area on one floor. Each zone has two independent properties:

- **Navigable**: the zone may be selected as the start or target of a navigation query.
- **Crossable**: a route may pass through the zone.

Each floor has its own exterior zone. The exterior is navigable and not crossable.

### 1.3

A boundary is a straight line that separates zones. When two zones share a boundary, they refer to the same boundary.

### 1.4

A portal is a crossable section of a boundary between exactly two zones. It may represent a door or other opening, or a virtual connection. A portal is represented in the connectivity graph by its midpoint, derived from the ends of its line.

A portal to the exterior may be marked as an emergency exit or a main entrance. A vertical portal connects zones on different floors and has one position on each joined floor.

## 2. Movement lines and segments

### 2.1

A movement line is a designer-drawn polyline representing a path through a zone.

### 2.2

A segment is a traversal through one zone from an entry portal to an exit portal. Its geometry and distance are part of the routing graph, not the zoning model.

## 3. Graphs and routing configuration

### 3.1

The connectivity graph represents floors, zones, portals, and movement lines. Its nodes are zones and its edges are portals.

### 3.2

The routing graph is derived from the connectivity graph and routing configuration. It represents directed transitions through portals and segments between portals.

### 3.3

A routing variant may restrict zones by making them non-crossable or non-navigable. A restriction narrows the available routes; it does not add connections.

## 4. Queries and routes

### 4.1

A navigation query specifies a start zone, a target zone, and a routing variant. The start and target must be navigable.

### 4.2

A state is a directed transition from one zone through a portal into another zone. It is written `zone_from | portal | zone_to`.

### 4.3

A segment between two consecutive states is written `entry_portal | zone | exit_portal`. A segment has a distance cost and may have an additional cost. A state may also have an additional cost.

### 4.4

A route is an alternating sequence of zones and portals, beginning with the start zone and ending with the target zone. It is written `zone | portal | zone | ... | portal | zone`.

The total route cost is the sum of its segment distances and any additional state and segment costs.

### 4.5

The route computer finds the lowest-cost route for each supported start, target, and variant. The precomputed routes dataset is used by the navigation module to serve a navi-user's request.
