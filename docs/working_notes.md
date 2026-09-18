# Working notes

Ideas as they are thought of or discussed, dated. Not a specification;
`axioms.md` is. Entries here feed the axioms, ADRs and roadmap, and are
pruned once absorbed.

---

## 2026-09-16 — Two-tier architecture

Deployment targets are a standalone kiosk now, possibly phones later, with no
confirmed hosting budget. The destination scope — the entire building — and the
routing algorithm were both still evolving. Reimplementing graph traversal
directly in JavaScript, in `Wegweiser_Frontend/frontend/script.js`, had already
caused logic drift and edge-direction bugs across copies. What was needed was a
clean division of responsibilities and a workspace layout that works out of the
box across environments.

Rejected:

- Live backend API — premature infrastructure and hosting cost, and it
  introduces runtime network failure into offline kiosks.
- Duplicating pathfinding in JavaScript — causes logic drift, and the same
  routing logic has to be maintained in two languages.
- `builder/` and `viewer/` — expressive of pipeline roles, but non-standard, so
  it needs explicit configuration across tooling and test runners.
- `python/` and `web/` — categorizes by implementation language rather than by
  architectural responsibility.

Consequences:

- Zero hosting cost. Static files run locally in kiosks, including direct
  `file://` viewing, and can be hosted statically for phones with no backend.
- A single source of truth for routing algorithms and building data in Python.
- Standard tooling — test discovery, linters, language servers — works without
  custom configuration.
- Later changes such as Dijkstra, multi-floor transitions or a thin API wrapper
  affect `src/` only, with no algorithmic change in `web/`.

---

## 2026-09-16 — Analytics

Usage insights would help improve signage and instructions: which destinations
are popular, where people get confused. Nothing is built during early
development.

Routing is a read-only static delivery path. Analytics is a write path, from
client to collector, and cannot reuse static JSON distribution. So whenever it
is built, it stays completely decoupled from routing.

Phasing:

- Kiosk phase: local, append-only log files, no external infrastructure.
- Mobile or hosted phase: a minimal event-collection endpoint, or a
  privacy-focused third-party service.
- Privacy by design: never collect or store anything traceable to an individual
  user, and formalize a privacy policy before switching any collection on.

What this buys: no premature infrastructure or telemetry code during
prototyping; routing stays static, self-contained and fast whatever is decided
later; privacy and compliance constraints set deliberately upfront rather than
retrofitted.

---

## 2026-09-16 — Test suite

To focus on later, as one subject rather than piecemeal: `validate_plan.py`
checking the SVG against the constraints, `test_main.py` checking the export,
and whatever else is needed.

What "as one subject" means concretely — the checks are reviewed together
against these criteria:

- Every constraint in the rulebook's C layer is checked exactly once. That layer
  is a finite list, so this is an audit that can be completed rather than an
  intention.
- No check duplicates another.
- No check contradicts another.
- For each check, it is clear which boundary owns it.

Alongside that: files in sensible places, named consistently, and one command
that runs everything.

`test_main.py`'s `RoutingContractTests` already checks the export structure —
top-level keys, coordinate format, every destination having a valid route. That
is the encoding check, and it exists. It needs rewriting when the export
contract changes in Phase 2.

The second class, `PathfindingAlgorithmTests`, holds the graph traversal checks.
Both live in `src/test_main.py` under standard unittest discovery; a root
`tests/` directory is deferred until the test count warrants it.

JavaScript tests are deferred while `web/` contains no routing logic — a Node.js
and npm dependency for nothing. Revisit if the viewer ever gains logic worth
testing.

What the boundary checks buy: a schema change in Python would otherwise break
the browser silently, and a malformed plan would otherwise reach the compiler
unnoticed. Both are caught with no external testing dependencies or build tools.

---

## 2026-09-16 — Navmesh and the funnel algorithm

Game-industry technique, and the closest existing pipeline to this design:
decompose the walkable floor into convex polygons, shared edges between adjacent
polygons become portals, a graph search over polygons returns a portal sequence,
and the **funnel algorithm** pulls a taut line through that sequence to give the
walked path.

Two uses here.

**Now:** it is where the routing graph's extra step comes from. Splitting the
problem into a portal sequence first and geometry second is standard practice
there, and is not part of IndoorGML.

**Later:** the funnel algorithm may compute movement lines automatically,
leaving hand-drawing for the places where people deviate from the taut line.
Worth reading before drawing movement lines by hand. See `research_notes.md`,
row 10 and the navigation mesh paragraph.

---

## 2026-09-16 — IndoorGML

The OGC standard for indoor navigation data. Its core was re-derived here
independently; see `research_notes.md` for the standard itself. Open items:

- **Read Part 1.** IndoorGML 2.0 Part 1: Conceptual Model, OGC document
  22-045r5. Not for validation but for pre-solved edge cases — multi-floor,
  accessibility and stairs-as-transitions have been implemented against the
  standard for years. Phases 5–7 may be shorter than the roadmap assumes.
- **MLSM for Phase 6.** The standard handles floors, accessibility variants and
  step-free routing by overlapping semantic space layers joined at anchor nodes.
  The roadmap instead plans to filter `data-kind="stairs"`. Compare the two
  before Phase 6 begins.
- **Vocabulary bridge.** Searching literature or asking a model about
  "CellSpace" returns useful results; "zone" does not. Add a mapping table to
  `research_notes.md` — zone to CellSpace, portal to navigable
  CellSpaceBoundary, and so on. Do **not** rename project terms to the
  standard's; the table is the bridge.

---

## 2026-09-15 — Elements, graphs, query mechanism

### Elements

The building is modelled on its 2D floor plan. Height is discarded; every
element loses one dimension relative to reality.

Five kinds of element. Zones are the reference; each of the others is
defined by its relation to zones.

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

**Portals are modelled as points.** Physically an opening is a line. Modelled
as a line, a wide opening would allow several paths between the same two
portals of a zone, depending on where along the line one crosses. Choosing
one point — the midpoint — keeps exactly one path per portal pair per zone.

**Axiom 2 is absolute.** Where three corridors meet, the shared point is not
a portal. Each pair of corridors gets its own portal at the midpoint of the
boundary they share, as if the third corridor were not there. Three portals
close together, each joining two zones.

**Zones and portals play different roles.** They are not two kinds of node.
Zones do not appear in the routing graph; they appear at its edges — as the
names the user gives for start and target, as the zone each path lies in,
and as the names used in the instructions.

**Which spaces become zones is the designer's decision**, made when
determining zones from the architectural plan. Some enclosed spaces drawn
there are lumped into one zone (WC cubicles); some become obstacles
(waiting areas); some are decided case by case (the Wachdienst booth).
Adjacent doors between the same two zones are handled at the same stage.

**Movement zones and movement lines.** The movement zone is the walkable
part of a zone — obstacles excluded — and lies wholly within that zone. The
movement line is the route people actually take through it: a single spine
in a corridor, possibly bent or branched in a hall. It is derived by convex
decomposition of the movement zone and adjusted by hand where real
behaviour departs from the geometric result. Transit segments follow the
movement line; access segments — the first and last of a route — run
directly from the terminus portal to the preceding one. The order of a
zone's portals along its movement line is what gives "third door on the
left".

**Every zone divides into a movement zone and a non-movement zone.**
Obstacles belong to the non-movement zone; segments to the movement zone.
To decide: whether the non-movement zone is only obstacles, or also
walkable area outside the circulation stripe — and if the latter, whether
an access segment from a door may cross it, or the movement zone must
reach every portal. Candidate.

**Many portals on one zone — to decide.** A straight corridor with 30 doors
is one convex zone with 496 portal pairs. How the segment length between any
two of them is obtained without storing every pair is open. One proposal —
projecting each portal onto the movement line and storing its position, with
a short hop from the portal to that position — is discarded as an AI artifact.
The question stands, and determines how movement lines and segments through a
zone are drawn.

### Graphs

Three graphs.

| Graph | Nodes | Edges | Purpose |
|---|---|---|---|
| **Adjacency** | rooms as drawn on the architectural plan | walls between them | the building as it is; check that zoning loses no room |
| **Connectivity** | zones | portals | which zones can be reached from which |
| **Routing** | portals | paths | route search |

- **Adjacency graph:** the building exactly as drawn — every room a node,
  every shared wall an edge. Objective, and the same representation BIM
  uses. A large hall or a long corridor is one node here.
- **Zoning:** the designer's step between the adjacency graph and the
  simplified floor plan. Splits halls and corridors into zones by convex
  decomposition, places virtual portals, declares obstacles, lumps or drops
  sub-partitions. Movement zones and movement lines are drawn in the same
  step.
- **Connectivity graph:** zones as nodes, portals as edges. Read from the
  SVG.
- **Routing graph:** each portal becomes a node. Two portals are linked when
  they lie on the same zone; the link is the path between them. Paths take
  their shape and length from the movement lines.

Axiom candidates: the routing graph is portals and paths only; every path
lies in exactly one zone.

The direction of a segment is given by the order in which its two portals
are written, left to right. A segment's length is independent of direction.

**Note for later.** If a BIM model of the building becomes available, the
adjacency graph is read from it directly and most pre-processing
disappears. Long term. Recorded because it confirms the order: start from
the realistic representation, then zone — not from a plan with zoning
already done.

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

Left column: authoring, plans down to the routing graph. Right column:
translation, the search result back up to the user.

### Query mechanism

**Multi-source, multi-target.**

> A query names a start zone and a target zone. The search begins from every
> portal of the start zone simultaneously and ends when the first portal of
> the target zone is reached. With *n* start portals and *m* target portals
> it is *n*-source, *m*-target; either may be 1. The mechanism mirrors the
> walker: any door of the start room is a valid exit, any door of the target
> room a valid arrival.

Consistent with axiom 12 — the *n* sources are its outbound states, the *m*
targets its inbound states. Candidate to replace or extend 12.

**User → algorithm.** The user names a room. The zone → portals inversion
(axiom 5) turns that name into a set of portals.

**Algorithm → user.** The result is a chain of portals. The zone each path
lies in gives the sequence of zones crossed. The order of a zone's portals
along it gives each portal's position in that zone — "third door on the
left". Together these produce the instructions.

**Why start and target are zones, not points.** A precise navigation tool
pinpoints the user's position and the destination, as GPS does. This program
has no positioning; the user states their location, and states it as a room.
So the start position is replaced by the set of the start zone's portals,
and the target position by the set of the target zone's portals. The
imprecision that results — the walk from wherever one stands to the chosen
door is not counted — comes from manual self-location, not from the model.

### To purge

The framing introduced by AI assistants and now known to be wrong:

- "dual graph"
- "portals as nodes, zone crossings as edges"
- portals replacing zones, in any wording
- the graph-versus-index layer split

Present in `adr.md` (ADR 4), `README.md`, `roadmap.md`,
`graphic_strategy.md`, `glossary.md`, `convergences.md`, `design_recap.md`.
ADR titles and the axioms are to be reevaluated as part of the overhaul, so
per-file fixes are not listed here.

---

## 2026-09-11 — Floor plan tooling

### Options Evaluated (reference)

| Approach / Tool | Pros | Assessment |
| :--- | :--- | :--- |
| **Claude Design, supervised hybrid** *(chosen)* | Produces semantically tagged SVG (zones, portals, kinds) in one pass; no drafting skill required; scales across floors | Requires disciplined human verification against source plans |
| Inkscape manual tracing | Free, offline, unlimited, pristine human-verified geometry | Sound fallback; per-floor drafting effort, and topology must be added separately |
| Automated image-to-vector *(Autotracer, Vectorization.org, Trace Bitmap)* | Fast, no drawing | Vectorizes text, pictograms and smudges; jagged double-walled paths; unusable node counts |
| Paint pre-clean + auto-trace | Avoids vector tooling | Still squiggly and double-walled; erasing clutter costs as much as drawing walls |
| OpenCV filter pipeline | Scales to many plans | Hours of tuning; deferred to Phase C |
| Sweet Home 3D / Floorplanner | Polished 2D/3D layouts | Free tiers capped (projects/floors); CAD overhead; messy SVG export |
| Figma / Miro | Quick schematics | Not fully free, account-bound; nested transforms and clip paths in export |
| Graph data encoded by hand in a drawing editor | Single file | Editors rewrite ids and inject transforms; visual edits break the parser — solved here by generating the SVG programmatically instead |

### Full automation — deferred

Only if plan volume justifies the investment: OpenCV pre-processing — HSV
masking of emergency pictograms, morphological cleanup, binarization — feeding
an auto-tracer, plus post-processing: path simplification, orthogonal snapping,
`svgo`. Out of scope while supervised hybrid output is sufficient.

---

## 2026-09 — Design session recap

Record of a design conversation, September 2026.

### Starting point

The opening proposal: break routing into three stretches — reach a known hub,
cross a precomputed hub-to-hub middle, invert the first stretch for the last
leg. Users are assumed to know where they are and where they want to go.

This maps to **HPA\*** and **transit node routing**. Two concerns raised at the
outset, both of which turned out to be central:

- Nearest-hub-first can miss shorter routes that bypass the nearest hub.
- Recovery after a wrong turn needs named landmarks the user can report.

### The reframing

Several turns in, the model was restated in a way that changed the project:

> *"For traversing each zone, the start and end points get updated, leading to
> segments that form a chain."*

This is not places linked by corridors.

The inherited code was the conventional model. Consequences:

- Cost lives on the traversal, so turn penalties need no special machinery.
- Arrival direction is expressible, which the conventional model cannot do.
- Rooms are never crossed.

### What was derived

Formalisation proceeded by correction rather than addition. The load-bearing
results, in the order they settled:

**Arity-2** (axiom 2) makes zone→portals a pure inversion of the portal record,
makes the segment list derivable rather than authored, and reduces direction
tracking to picking the other element of a pair. A portal joining three zones
would require a hypergraph.

**Axiom 4 as the boundary test.** This is not an observation about buildings but
the definition of a zone, and it gives a working rule for data entry that needs
no categories.

**The state** (axiom 7). The algorithm is Dijkstra over states; search space is
2 × portal count.

Result: **19 axioms**.

### Algorithm evaluation

At this scale every candidate runs in well under a millisecond, so speed is not
a criterion. What discriminates: correctness under loops, instruction quality,
deviation robustness, authoring cost, and the asymmetry between ~300
destinations and ~20 decision points.

**Shortlist:**

- **Dijkstra over states** as the engine and ground truth. Unglamorous, always
  correct, handles the cost model.
- **Graph Voronoi + arc flags** as the layer above, because they produce
  something printable and inspectable and match the building's star shape.
- **Yen's k-shortest paths** later, for step-free and accessibility variants.

**Rejected for this building:** A\* (straight-line heuristic is actively bad in a
star topology), D\* Lite (recomputing is cheaper than repairing at this scale),
contraction hierarchies and hub labelling (continental-scale machinery).

**Kept as reference:** BFS, as the original implementation and an algorithmic
regression baseline.

One observation that shaped the shortlist: **route choice is rare in this
building.** The star topology means most of the graph has exactly one sensible
path. Any algorithm competing on pathfinding quality competes over a small prize;
the real difficulty is turning a node sequence into usable German instructions.
