# BFW Wegweiser

This is a project for developing an indoor navigation and pathfinding tool for the BFW facility.

## Roles And Artifacts

The project author develops and maintains Wegweiser. The zoning author creates and reviews the building model. The navi-user uses the finished navigation application to request and inspect directions. One person may occupy several roles.

When describing AI-assisted work, "human participant" means the person chatting with the AI assistant, not the navi-user. Use the specific role or artifact name wherever an unqualified term such as "user" or "SVG" could refer to different people or outputs.

The intended outputs are two separate SVGs: the zoning SVG is the visual counterpart of the connectivity graph; the navigation SVG is the map used to present routes to the navi-user. This distinction describes the intended design, not a claim that both outputs are already implemented.

## Architecture

The code is split into an offline compiler and a browser client:

- [src/](src/): Python compiler that parses the floor plan, builds the routing graph, computes the routes, and serializes the routing data.
- [web/](web/): Browser client that takes the navi-user's request and renders the route on the floor plan alongside navigation instructions.

## East-Wing Prototype

The east-wing prototype follows the model in
[docs/rulebook_sorted.md](docs/rulebook_sorted.md) and remains separate from the
existing kiosk. Build its source database and precompute all ordered
zone-to-zone routes:

```powershell
python src/build_database.py
python src/calculate_routes.py
```

This writes `database.json` and `database_with_routes.json` at the repository
root. Serve the repository root so the browser can load the routed database and
the semantic floor-plan SVG:

```powershell
python -m http.server 8765
```

Open `http://localhost:8765/web/east_wing.html`.

## Workspace Layout

```text
wegweiser/
├── .gitignore
├── README.md
├── database.json
├── database_with_routes.json
├── docs/
│   ├── devlog.md                 dated record of changes
│   ├── implementation-plan.md    planned development phases
│   ├── rulebook.md               the navigation model
│   ├── system-design.md          system-level design decisions
│   └── references/
│       ├── docs_guidelines.md    how these docs are written
│       ├── funnel.svg            funnel algorithm diagram
│       ├── funnel_algorithm.md   funnel algorithm notes
│       └── research_notes.md     literature and graph theory
├── src/
│   ├── build_database.py
│   ├── calculate_routes.py
│   ├── main.py
│   └── test_main.py
└── web/
    ├── assets/
   │   ├── bfw-eg-ost.svg
    │   └── Grundriss_mit_Knotenpunkten.png
    ├── data.js
    ├── data.json
   ├── east_wing.css
   ├── east_wing.html
   ├── east_wing.js
    ├── index.html
    ├── script.js
    └── style.css
```

## Conceptual Model

The project is built around computer-assisted modeling under human supervision. It abstracts the real building into two complementary representations, floor plans that people can read and node-and-edge graphs that a machine can search. Lowest-cost routes between all places are precomputed. A navi-user's request is then answered on demand, with the matching route drawn onto the navigation map alongside navigation instructions.

## Implementation Plan

Progress is tracked in GitHub Issues.

- [ ] Phase 1: Floor plan and connectivity graph
- [ ] Phase 2: Routing graph and compiler
- [ ] Phase 3: Zone queries and route search
- [ ] Phase 4: Test suite
