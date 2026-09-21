# Rulebook

This rulebook defines the project's navigation model and is its source of truth. Every project file that concerns the navigation model must conform to it.

## 1. Structural elements and topology

Defines the spaces, zones, boundaries, portals, and segment relations that structure navigation.

### 1.1

Architectural and simplified floor plans are two-dimensional representations of the building. The simplified plan is derived from the architectural, retaining only features relevant to navigation.

### 1.2

A zone is a two-dimensional space that partitions the simplified floor plan without gaps or overlaps.

A zone may be crossable or non-crossable. A non-crossable zone may be a route's start or target, but cannot be passed through.

### 1.3

A separator is a fixed, non-crossable division between two spaces in the architectural plan.

A boundary is a one-dimensional division between two zones in the simplified floor plan. It may represent a physical separator or be virtual.

### 1.4

A portal represents the crossable portion of a boundary and is drawn in the simplified floor plan as a highlighted section with its midpoint marked. In the navigation model, it is represented by that midpoint.

A portal may correspond to a physical door or other opening between distinct architectural spaces, or to a virtual opening on a virtual boundary.

A portal always joins exactly two zones. Because a boundary is a line, multiple zones may meet at a point but do not share a portal there; each pair of zones has its own shared boundary and portal.

### 1.5

A segment is a traversal through one zone, from one portal to another. It lies in the zone’s interior.

### 1.6

The exterior is a single zone surrounding the building. A route may begin or end there but never cross it.

## 2. Movement geometry and constraints

Defines walkable space, obstacles, movement zones, movement lines, and segment geometry.

### 2.1

A zone divides into a walkable part and a non-walkable part.

### 2.2

An obstacle is a fixed obstruction in the non-walkable part of a zone; routes neither end at nor pass through it.

### 2.3

The movement zone is the circulation space within the walkable part.

### 2.4

A movement line is a designer-drawn representation of the path people actually take through a movement zone.

## 3. Zoning and graph construction

Defines how the simplified floor plans are produced from the architectural plans, and how the adjacency, connectivity, and routing graphs are derived.

### 3.1

The adjacency graph is the machine-readable abstraction of the spaces and separators in the architectural plans. Its nodes are spaces and its edges are separators.

### 3.2

Zoning is the process of converting spaces and separators into zones and boundaries and creating portals, movement zones, and movement lines that form essential elements of the navigation model.

The connectivity graph is produced alongside the simplified floor plans. Its nodes are zones and its edges are portals.

Every zone must have at least one portal, and its portals must be mutually reachable without obstruction.

### 3.3

The routing graph is constructed from the connectivity graph using movement geometry and routing decisions. Its nodes are portals, and its edges are segments.

Marking additional zones as non-crossable creates a routing variant in which those zones remain reachable but cannot be passed through.

## 4. Queries and search

Defines queries, states, routes, costs, and the search for lowest-cost routes.

### 4.1

A query is a user's request for navigation from one location to another. Start and target locations can only be specified as zones. Precise positions within those zones are not represented.

### 4.2

A state is a directed transition from one zone through a portal into another zone. It is written `zone_from | portal | zone_to`. A state may be assigned special costs.

### 4.3

A segment between two consecutive states is written `portal | zone | portal`. A segment may be assigned special costs in addition to its distance cost.

### 4.4

A route is an alternating sequence of zones and portals, beginning with the start zone and ending with the target zone. It is written `zone | portal | zone | ... | portal | zone`.

Total route cost is the sum of distances and special costs from its segments and states.

### 4.5

The search is multi-source and multi-target and returns the route with the lowest total cost. The routing graph is searched from the outbound states of the start zone to the inbound states of the target zone.

### 4.6

The search produces a portal chain. The portal chain determines the zone sequence and the zone of each segment. The route is interpreted as navigation instructions and rendered on the building plan.
