# BFW Wegweiser

This is a project for developing an indoor navigation tool for the BFW facility.

## Roles and precise language

- Project author: develops and maintains the project.
- Zoning author: creates and reviews the building model.
- Navi-user: uses the finished navigation application.
- Human participant: the person chatting with the AI assistant.

One person may occupy several roles. Specific role and artifact names are to be used wherever generic terms would be ambiguous.

## Language

Identifiers, documentation and commit messages are in English; comments and user-facing text are in German.

## Architecture

The architecture separates Zoning, Routing and Navigation modules. The compiler and browser-client code are organized as follows:

- [src/](src/): Python compiler that builds the routing graph from the modeled floor plans, computes the routes, and serializes the routing data.
- [web/](web/): Browser client that takes the navi-user's request and renders the route on the floor plan alongside navigation instructions.

## EG corridor movement networks

Generate centerlines and portal connectors for corridor zones from their
outlines in the EG SVG before rebuilding the route data:

```powershell
python src/build_corridor_movement_networks.py
python src/build_routing_graph.py
python src/calculate_routes.py
```

The generated geometry is an unverified draft and should be reviewed against
the floor plan before it is treated as authoritative.

## Workspace Layout

```text
wegweiser/
├── README.md
├── docs/
│   ├── implementation-plan.md    planned development work
│   ├── rulebook.md               model tenets and definitions
│   ├── system-design.md          system-level design decisions
│   └── working-record.md         current decisions and agreements
├── src/                          offline compiler
└── web/                          browser client
```

## Conceptual Model

The project is built around computer-assisted modeling under human supervision. It abstracts the real building into two complementary representations, floor plans that people can read and node-and-edge graphs that a machine can search. Lowest-cost routes between locations in the building are precomputed. A navi-user's request is then answered on demand, with the matching route drawn onto the navigation map alongside navigation instructions.

## Document Responsibilities

| Document | Responsibility |
| --- | --- |
| `README.md` | Project introduction and orientation |
| Rulebook | Model tenets, definitions and constraints |
| System design | Architecture and design decisions |
| Implementation plan | Planned work and implementation methodology |
| Working record | Provisional agreements, qualifications and reasoning |
