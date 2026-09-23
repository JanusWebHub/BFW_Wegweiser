# Working notes

Ideas as they are thought of or discussed, dated. Not a specification; `rulebook.md` is.

---

## 2026-09-21 Abstraction Process Description (latest approved)

The abstraction process is a **human-in-the-loop, computer-assisted modeling pipeline** with two complementary representation types:

- **Visual representations**: architectural plans, simplified floor plans, spatial routing plans, and graph visualizations.
- **Machine-readable symbolic representations**: serialized graph models containing nodes, edges, and attributes.

The adjacency, connectivity, and routing graphs are **interdependent abstractions of the same building**, developed within one modeling process. Zoning is the central design activity in that process.

1. Architectural plans are visual source representations of the building and are digitally interpreted into a machine-readable adjacency graph.
2. The plans and adjacency graph are used in zoning to produce the simplified floor plans as visual representations and the connectivity graph as a machine-readable symbolic representation.
3. The designer constructs the routing graph from the connectivity graph, serializes it as machine-readable data, and renders it as a graph visualization.

Useful terminology:

- **graph model**: the abstract mathematical structure
- **graph representation**: a concrete way of expressing that model
- **graph serialization**: storing the graph in a machine-readable format
- **JSON encoding** or **JSON representation**: the graph’s JSON form
- **JSON object**: the technical JSON equivalent of a dictionary
- **nodes, edges, and attributes**: the contents of the graph representation
- **simplified floor plan**: represents zones, boundaries, portals, obstacles, movement zones, and movement lines
- **spatial routing plan**: represents the routing graph in its building locations, optionally using the simplified floor plan as a faded spatial reference
- **graph visualization**: represents graph structure abstractly, without preserving building locations
- **spatial representation**: a plan or map showing geometry
- **symbolic representation**: an abstract notation using identifiers and relations
- **semantic interpretation**: assigning model meaning to features in a plan
- **digitization**: converting source material into digital data
- **abstraction**: reducing a detailed physical reality to model-relevant elements
- **human-in-the-loop modeling**: computational assistance with human decisions remaining authoritative
- **computer-assisted authoring**: tools support the designer’s work without replacing the designer

---

## 2026-09-15 — Elements, graphs, query mechanism

### Elements

The building is modelled on its 2D floor plan. Height is discarded; every element loses one dimension relative to reality.

Five kinds of element. Zones are the reference; each of the others is defined by its relation to zones.

| Element | Dim. | Relation to zones | Transit |
|---|---|---|---|
| **Zone** | 2D | is the space | — |
| **Wall** | 1D | boundary between two zones | no |
| **Portal** | 0D | point on a boundary between two zones | yes |
| **Path** | 1D | inside one zone, from one of its portals to another | yes |
| **Obstacle** | 2D | inside one zone | no |

The four non-zone elements fill a 2×2:

| | in one zone | between two zones |
|---|---|---|
| **no transit** | obstacle | wall |
| **transit** | path | portal |

**Portals are modelled as points.** Physically an opening is a line. Modelled as a line, a wide opening would allow several paths between the same two portals of a zone, depending on where along the line one crosses. Choosing one point — the midpoint — keeps exactly one path per portal pair per zone.

**Axiom 2 is absolute.** Where three corridors meet, the shared point is not a portal. Each pair of corridors gets its own portal at the midpoint of the boundary they share, as if the third corridor were not there. Three portals close together, each joining two zones.

**Zones and portals play different roles.** They are not two kinds of node. Zones do not appear in the routing graph; they appear at its edges — as the names the user gives for start and target, as the zone each path lies in, and as the names used in the instructions.

**Which spaces become zones is the designer's decision**, made when determining zones from the architectural plan. Some enclosed spaces drawn there are lumped into one zone (WC cubicles); some become obstacles (waiting areas); some are decided case by case (the Wachdienst booth). Adjacent doors between the same two zones are handled at the same stage.

**Movement zones and movement lines.** The movement zone is the walkable part of a zone — obstacles excluded — and lies wholly within that zone. The movement line is the route people actually take through it: a single spine in a corridor, possibly bent or branched in a hall. It is derived by convex decomposition of the movement zone and adjusted by hand where real behaviour departs from the geometric result. Transit segments follow the movement line; access segments — the first and last of a route — run directly from the terminus portal to the preceding one. The order of a zone's portals along its movement line is what gives "third door on the left".

**Every zone divides into a movement zone and a non-movement zone.** Obstacles belong to the non-movement zone; segments to the movement zone. To decide: whether the non-movement zone is only obstacles, or also walkable area outside the circulation stripe — and if the latter, whether an access segment from a door may cross it, or the movement zone must reach every portal. Candidate.

**Many portals on one zone — to decide.** A straight corridor with 30 doors is one convex zone with 496 portal pairs. How the segment length between any two of them is obtained without storing every pair is open. One proposal — projecting each portal onto the movement line and storing its position, with a short hop from the portal to that position — is discarded as an AI artifact. The question stands, and determines how movement lines and segments through a zone are drawn.

### Graphs

Three graphs.

| Graph | Nodes | Edges | Purpose |
|---|---|---|---|
| **Adjacency** | rooms as drawn on the architectural plan | walls between them | the building as it is; check that zoning loses no room |
| **Connectivity** | zones | portals | which zones can be reached from which |
| **Routing** | portals | paths | route search |

- **Adjacency graph:** the building exactly as drawn — every room a node, every shared wall an edge. Objective, and the same representation BIM uses. A large hall or a long corridor is one node here.
- **Zoning:** the designer's step between the adjacency graph and the simplified floor plan. Splits halls and corridors into zones by convex decomposition, places virtual portals, declares obstacles, lumps or drops sub-partitions. Movement zones and movement lines are drawn in the same step.
- **Connectivity graph:** zones as nodes, portals as edges. Read from the SVG.
- **Routing graph:** each portal becomes a node. Two portals are linked when they lie on the same zone; the link is the path between them. Paths take their shape and length from the movement lines.

Axiom candidates: the routing graph is portals and paths only; every path lies in exactly one zone.

The direction of a segment is given by the order in which its two portals are written, left to right. A segment's length is independent of direction.

**Note for later.** If a BIM model of the building becomes available, the adjacency graph is read from it directly and most pre-processing disappears. Long term. Recorded because it confirms the order: start from the realistic representation, then zone — not from a plan with zoning already done.

### Provenance

```
   architectural plans                     navigation instructions
           │                                          ▲
           ▼                                          │
   adjacency graph                         zone sequence
           │                                          ▲
           ▼  zoning                                  │
           │                                          │
   simplified floor plan (SVG)             zone of each path
   ├ zones, portals, obstacles                        ▲
   └ movement zones and lines                         │
           │                                          │
           ▼                                          │
   connectivity graph                      portal chain
           │                                          ▲
           ▼  paths from movement lines               │
           │                                          │
   routing graph ─────────────► search ───────────────┘
```

Left column: authoring, plans down to the routing graph. Right column: translation, the search result back up to the user.

### Query mechanism

**Multi-source, multi-target.**

> A query names a start zone and a target zone. The search begins from every
> portal of the start zone simultaneously and ends when the first portal of
> the target zone is reached. With *n* start portals and *m* target portals
> it is *n*-source, *m*-target; either may be 1. The mechanism mirrors the
> walker: any door of the start room is a valid exit, any door of the target
> room a valid arrival.

Consistent with axiom 12 — the *n* sources are its outbound states, the *m* targets its inbound states. Candidate to replace or extend 12.

**User → algorithm.** The user names a room. The zone → portals inversion (axiom 5) turns that name into a set of portals.

**Algorithm → user.** The result is a chain of portals. The zone each path lies in gives the sequence of zones crossed. The order of a zone's portals along it gives each portal's position in that zone — "third door on the left". Together these produce the instructions.

**Why start and target are zones, not points.** A precise navigation tool pinpoints the user's position and the destination, as GPS does. This program has no positioning; the user states their location, and states it as a room. So the start position is replaced by the set of the start zone's portals, and the target position by the set of the target zone's portals. The imprecision that results — the walk from wherever one stands to the chosen door is not counted — comes from manual self-location, not from the model.

### To purge

The framing introduced by AI assistants and now known to be wrong:

- "dual graph"
- "portals as nodes, zone crossings as edges"
- portals replacing zones, in any wording
- the graph-versus-index layer split

Present in `adr.md` (ADR 4), `README.md`, `roadmap.md`, `graphic_strategy.md`, `glossary.md`, `convergences.md`, `design_recap.md`. ADR titles and the axioms are to be reevaluated as part of the overhaul, so per-file fixes are not listed here.

