# Wegweiser — Rulebook

What is true in this model, such that every drawing, script and algorithm in the project agrees. This is the source of truth. Other documents implement it; they do not restate or renegotiate it.

## 1. Elements

### 1.1

The building is represented on its floor plan. Height is discarded, so every element loses one dimension relative to reality. Movement between floors is a special cost, not a geometry.

### 1.2

A zone is a two-dimensional space, created via zoning process by converting enclosed spaces, such as rooms, halls and corridors, into areas in which every portal is reachable from every other without obstruction. Zones partition the plan. Every point of the building belongs to exactly one zone, without gaps or overlaps. Every zone has at least one portal.

A zone is marked crossable or not. A non-crossable zone may be a start or a target but is never passed through. Marking further zones non-crossable produces a variant of the routing data, in which those zones may still be reached but not traversed.

### 1.3

A wall is a boundary between two enclosed spaces in the architectural plan. represented after zoning as one-dimensional (their thickness being neglegted, incorporated into zones). Not crossable.

### 1.4

A portal represents the crossable portion of a boundary between two zones. Physically an opening is a line on a floor plan, here it is modelled as a single point at midpoint, which ensures the possibility of exactly one segment per portal pair per zone.

A boundary is a line, and three areas can share a point but never a line. A portal therefore joins exactly two zones, always. Where three corridors meet, the meeting point is not a portal: each pair has its own shared boundary and its own portal, giving three portals close together. This matches how people walk, cutting the corner rather than passing through the meeting point.

A portal need not be a door, a doorless opening, or a line drawn across a corridor at a corner, is equally considered a portal by the model. One that has no physical counterpart is called a virtual portal, created by the designer when splitting a single enclosed space into multiple zones.

### 1.7

A segment is a traversal of one zone, from one of its portals to another. One-dimensional, lying in the interior of that zone. All travel is of this kind: there is no movement that is not a segment.

### 1.8

An obstacle is a fixed thing inside a zone that is not walkable and that nobody routes to or through. Two-dimensional.

### 1.11

The exterior is a single zone surrounding the building. A route may begin or end there but never cross it.

## 2. Zoning and movement geometry

### 2.1

Zoning is the designer's step between the adjacency graph and the simplified floor plan:

- splitting halls and corridors into zones
- placing portals that have no door
- declaring obstacles
- drawing movement zones and movement lines

Which enclosed spaces on the architectural plan become zones of their own, which are absorbed into a larger zone, and which become obstacles is decided by the designer. It does not follow from the topology. Governed by `zoning_guidelines.md`.

### 2.3

A zone divides into a walkable part and a non-walkable part. The non-walkable part is its obstacles. The movement zone is the circulation space within the walkable part, where people usually move.

### 2.5

A movement line is the route people actually take through a movement zone: a single spine in a corridor, bent or branched in a hall. Drawn by the designer.

## 3. Graphs and derivation

### 3.1

There are three graphs.

| Graph | Nodes | Edges |
| --- | --- | --- |
| Adjacency | rooms | walls |
| Connectivity | zones | boundaries |
| Routing | portals | segments |

### 3.4

The connectivity graph is derived from the adjacency graph by zoning. Zoning replaces rooms with zones: one room may become several zones, and several rooms may be absorbed into one. Each wall corresponds to the boundary between the zones its rooms became.

### 3.5

The routing graph is built from the connectivity graph. Each portal becomes a node; two portals are linked when they lie on the same crossable zone, and the link is the segment between them.

### 3.6

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

## 4. Routes and queries

### 4.1

A query names a start zone and a target zone.

### 4.2

The search is multi-source and multi-target. The start set is the outbound states of the start zone, one per portal; the target set is the inbound states of the target zone. The search runs from the start set and ends when it reaches the first state of the target set.

### 4.3

A state is written `zone_from | portal | zone_to`. Each portal yields exactly two, one per direction. The order gives the direction, and both zones are named, so a state stands alone without lookup.

### 4.7

Special costs are assigned by the designer to individual states. They are separate from distance.

### 4.9

The result of a query is a chain of portals. The zone each segment lies in gives the sequence of zones crossed.

A route is one strictly alternating sequence, beginning and ending with a zone:

```text
zone₁ portal₁ zone₂ portal₂ zone₃ … portalₙ zoneₙ₊₁
```

### 4.17

user's position within a zone is not counted, because the program has no precise positioning due to manual self-location.
