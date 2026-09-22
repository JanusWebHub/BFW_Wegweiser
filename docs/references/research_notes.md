# Wegweiser — Research notes

Concepts derived from first principles during design and their established names in the literature, where that established work applies to this project, and general graph theory terms. For reference and further reading.

---

## Full set

| # | Derived | Established name | Field |
| --- | --- | --- | --- |
| 1 | Three-stretch decomposition: reach a known hub, precomputed hub-to-hub middle, inverse for the last stretch | HPA\* (Botea, Müller, Schaeffer 2004); Transit Node Routing (Bast et al. 2006); multi-level graphs | Game AI; road-network route planning |
| 2 | Nearest-hub-first can miss shorter routes that bypass the nearest hub | Optimality loss under fixed cluster entrances | Hierarchical pathfinding |
| 3 | Subway-exit signage: assign landmarks by real access cost, not birds-eye distance | Graph Voronoi diagram; arc flags (Lauther 2004) | Network analysis; road routing |
| 4 | Direction pruning, repeated at each decision point | Routing tables, distance-vector routing; flow fields / Dijkstra maps | Computer networking; game development |
| 5 | Zones as edges, portals as nodes | Dual graph / line graph; Node-Relation Graph of IndoorGML | Graph theory; GIS; OGC indoor standards |
| 6 | "If two portals aren't reachable by an unhindered path, it isn't one zone — split it" | Convex cell decomposition of free space | Robot motion planning |
| 7 | A portal joins exactly two zones; the portal record inverts to the zone index | Bipartite incidence structure; incidence matrix | Combinatorics; topology |
| 8 | State written `zone \| portal \| zone`, direction carried by the order | Edge-based expansion; turn-aware routing | Road routing; state-space search |
| 9 | Canonical alternating zone-portal-zone chain | Portal sequence ("channel", "corridor") | Navmesh pathfinding |
| 10 | Convex cells → virtual portals → polyline through them | Navigation mesh pipeline; funnel algorithm (string-pulling) | Game AI; robotics |
| 11 | Three route cases by zone adjacency (axiom 15) | Locality filter — TNR's fallback to local search for near pairs | Road routing |
| 12 | A portal is where the zone-before differs from the zone-after | Boundary in point-set topology; portal in rendering | Topology; computer graphics (Doom/Quake portal culling) |
| 13 | Prescribed paths people actually walk, not geometric optima | Desire lines; preferred-path networks | Urban planning; architecture |
| 14 | Movement as a series of dimensionless directed instants | Velocity field / flow field; continuous-time trajectory | Physics; control theory |
| 15 | Movement zones and lines; initial/terminal vs transit portals | Core network + access edges; medial axis / skeleton | Transit node routing; computational geometry |

---

## Where established work applies

**Navigation mesh construction** is the closest existing pipeline to this design, and covers rows 6, 9 and 10 as one method:

> Decompose free space into convex polygons → shared edges become portals → graph search over polygons yields a portal sequence → the **funnel algorithm** (Lee & Preparata 1984; "Simple Stupid Funnel Algorithm" for a readable modern treatment) pulls a taut shortest path through that sequence.

The funnel step is the one part not yet derived here, and it addresses the same problem as prescribed movement lines: given a chain of portals, what is the actual walked line. Worth reading before hand-drawing movement lines, since it may compute a usable default to override only where human behaviour departs from taut-string geometry.

**IndoorGML** (OGC standard) formalises rows 5 and 7 — cells, boundaries, and the node-relation graph — and has already done the standardisation work for indoor navigation specifically.

**Transit Node Routing** (rows 1, 11, 15) is the closest match for the access/transit split and the locality fallback.

---

## IndoorGML

OGC standard for indoor navigation data. IndoorGML 2.0 separates the conceptual
abstraction from its physical outputs across three layers.

### Layer 1 — Conceptual model (UML)

What exists and how it connects, drawn as classes and relations, independent of
database syntax, platform or schema. Unlike IFC or CityGML, it isolates cellular
space and topological networks specifically for indoor location-based services
and routing.

**Primal and dual space.**

| Primal space | Dual space |
| --- | --- |
| Rooms, corridors, stairs — *CellSpace*. Physical areas with walls. | A network graph. Each cell becomes a node — *State*; each boundary becomes an edge — *Transition*. |

Boundaries are *CellSpaceBoundary*. The standard distinguishes an **adjacency**
graph, where cells are linked by any shared boundary, from a **connectivity**
graph, where they are linked only by navigable ones.

**Multi-Layered Space Model (MLSM).** A building may be represented
simultaneously across different semantic contexts — topographic layout, Wi-Fi
footprint, security access — as overlapping space layers.

### Layer 2 — Constraints (OCL)

UML shows structure but cannot express mathematical rules or geometric
consistency. The Object Constraint Language supplies vendor-independent formal
invariants that data must satisfy to count as a valid indoor navigation map.
Data breaking them is flagged as an error before it reaches a client.

Typical constraints:

- **Bijective mapping** — every CellSpace maps to exactly one State. No cell
  without a node, no node without a cell.
- **Adjacency validation** — a Transition may exist between two States only if
  their CellSpaces share a valid spatial boundary.
- **Layer isolation** — paths may not cross space layers except through
  explicitly defined anchor nodes.

### Layer 3 — Encoding rules

How the abstract model and its constraints become text a machine can parse,
store and transmit.

```text
[ UML conceptual model ]   classes: CellSpace, State, Layer
          |
          v
[ OCL invariants ]         rules: every CellSpace must have a State
          |
          v
[ encoding rules ]         GML / XML Schema, JSON Schema, SQL DDL
```

IndoorGML is standardised as an application schema of OGC GML 3.2.1; UML classes
convert systematically into XML Schema. Part 2 of the 2.0 standard adds JSON
schemas for web and mobile clients, and SQL/PostGIS DDL mappings. Because SQL
engines cannot parse OCL, those invariants become database triggers or spatial
indexing constraints at this stage.

### Sources

- OGC, *IndoorGML 2.0 Part 1: Conceptual Model* — `docs.ogc.org/is/22-045r5/22-045r5.html`
- `ogc.org/standards/indoorgml/`
- `indoorgml.net`


---

## Graph theory terms

**Node** and **edge** — the mathematical words. Used throughout, because every
paper and library uses them and a local vocabulary costs a translation tax on
every lookup. "Edge" is a fossil from polyhedra and describes nothing here; keep
it anyway.

- **Dual** names a relationship between two graphs, not a kind of graph. A dual
  graph is an ordinary graph.
- **Planar dual:** faces become nodes, linked where two faces share an edge.
  Countries on a map.
- **Line graph:** edges become nodes, linked where two edges shared an endpoint.
  Roads on a street network.
- Both constructions keep one kind of element only.
- **Multigraph:** more than one edge allowed between the same pair of nodes.
- **Hypergraph:** an edge may join any number of nodes.
