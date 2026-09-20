# Rulebook

This rulebook defines the project's navigation model and is its source of truth. Every project file that concerns the navigation model must conform to it.

## 1. Cluster 1 — elements: zone, separator, portal, segment

### 1.1

Architectural and simplified floor plans are two-dimensional representations of the building. The simplified plan is derived from the architectural, retaining only features relevant to navigation.

### 1.2

A zone is a two-dimensional space that partitions the simplified floor plan without gaps or overlaps.

A zone may be crossable or non-crossable. A non-crossable zone may be a route's start or target, but cannot be passed through.

### 1.3

A separator is a fixed, non-crossable division between two spaces in the architectural plan. In the simplified floor plan, it is represented as a one-dimensional boundary between two zones. A virtual boundary may separate zones where no physical separator exists.

### 1.4

A portal represents the crossable portion of a boundary between two zones. Although drawn as a line on a floor plan, it is represented in the model by its midpoint.

A portal may correspond to a physical door or other opening between distinct architectural spaces, or to a virtual opening on a virtual boundary.

A portal always joins exactly two zones. Because a boundary is a line, multiple zones may meet at a point but do not share a portal there; each pair of zones has its own shared boundary and portal.

Every zone has at least one portal, and every portal is reachable from every other without obstruction.

### 1.5

A segment is a traversal through one zone, from one portal to another. It lies in the zone’s interior.

### 1.6

The exterior is a single zone surrounding the building. A route may begin or end there but never cross it.

## 2. Cluster 2 — obstacle and movement geometry

### 2.1

A zone divides into a walkable part and a non-walkable part.

### 2.2

An obstacle is a fixed obstruction in the non-walkable part of a zone; routes neither end at nor pass through it.

### 2.3

The movement zone is the circulation space within the walkable part.

### 2.4

A movement line is a designer-drawn representation of the route people actually take through a movement zone.

## 3. Cluster 3 — zoning and the three graphs

### 3.1

Zoning is the designer's process of converting enclosed spaces such as rooms, halls, and corridors into zones and preparing the simplified floor plan:

- splitting halls and corridors into zones
- placing portals that have no door
- declaring obstacles
- drawing movement zones and movement lines

Which enclosed spaces become zones of their own, which are absorbed into a larger zone, and which become obstacles is decided by the designer. It does not follow from the topology. Governed by `zoning_guidelines.md`.

### 3.2

There are three graphs.

| Graph | Nodes | Edges |
| --- | --- | --- |
| Adjacency | spaces | separators |
| Connectivity | zones | boundaries |
| Routing | portals | segments |

### 3.3

The connectivity graph is derived from the adjacency graph by zoning. Zoning replaces spaces with zones: one space may become several zones, and several spaces may be absorbed into one. Each separator corresponds to the boundary between the zones its spaces became.

### 3.4

The routing graph is built from the connectivity graph. Each portal becomes a node; two portals are linked when they lie on the same crossable zone, and the link is the segment between them.

Marking additional zones as non-crossable creates a routing variant in which those zones remain reachable but cannot be passed through.

### 3.5

```text
   architectural plans                     navigation instructions
           │                                          ▲
           ▼                                          │
   adjacency graph                         zone sequence
           │                                          ▲
           ▼  zoning                                  │
           │                                          │
   simplified floor plan (SVG)             zone of each segment
   ├ zones, portals, obstacles                        ▲
   └ movement zones and lines                         │
           │                                          │
           ▼                                          │
   connectivity graph                      portal chain
           │                                          ▲
           ▼  segments from movement lines            │
           │                                          │
   routing graph ─────────────► search ───────────────┘
```

## 4. Cluster 4 — query, search, route

### 4.1

A query names a start zone and a target zone. Because the user manually inputs both positions as zones, the position within the start or target zone is not counted.

### 4.2

A state is written `zone_from | portal | zone_to`. Each portal yields exactly two, one per direction. The order gives the direction, and both zones are named, so a state stands alone without lookup.

### 4.3

The search is multi-source and multi-target. The start set is the outbound states of the start zone, one per portal; the target set is the inbound states of the target zone. The search runs from the start set and ends when it reaches the first state of the target set.

### 4.4

Special costs are assigned by the designer to individual states. They are separate from distance.

### 4.5

The result of a query is an alternating sequence of zones and portals, beginning with the start zone and ending with the target zone.
