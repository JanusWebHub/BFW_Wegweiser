# BFW Wegweiser

This is a project for developing an indoor navigation tool for the BFW facility.

## Roles and precise language

- Project author: develops and maintains the project.
- Zoning author: creates and reviews the building model.
- Navi-user: uses the finished navigation application.
- Human participant: the person chatting with the AI assistant.

One person may occupy several roles. Specific role and artifact names are to be used wherever generic terms would be ambiguous.

## Language

Identifiers, documentation, interface text, code comments and commit messages are in English in all development modules (plan tracer, zoning editor, tuning editor). User-facing text of the browser client is in German.

## Architecture

The architecture separates zoning, routing and navigation modules. The modules are organized as follows:

- [cad/](cad/): The zoning module, with the plan tracer, which draws the plan SVG, and the zoning editor, which models the building.
- [src/](src/): The routing module, with the graph compiler, which builds the routing graph, the route computer, which produces the precomputed routes, and the tuning editor, in which the zoning author sets the costs and variants.
- [web/](web/): The navigation module, a browser client that takes the navi-user's request and renders the route on the navigation map alongside navigation instructions.

## Workspace Layout

```text
wegweiser/
├── readme.md
├── cad/                          zoning module
│   ├── plan tracer/              plan SVG drawing
│   ├── zoning editor/            zone modeling
│   └── source material/          original sources
├── src/                          routing module
├── web/                          navigation module
└── docs/
    ├── implementation-plan.md    planned development work
    ├── rulebook.md               model tenets and definitions
    ├── system-design.md          system-level design decisions
    └── working-record.md         current decisions and agreements
```

## Conceptual Model

The project is built around computer-assisted modeling under human supervision. It abstracts the real building into two complementary representations, floor plans that people can read and node-and-edge graphs that a machine can search. Lowest-cost routes between locations in the building are precomputed. A navi-user's request is then answered on demand, with the matching route shown on the navigation map alongside navigation instructions.

## Document Responsibilities

| Document | Responsibility |
| --- | --- |
| `readme.md` | Project introduction and orientation |
| Rulebook | Model tenets, definitions and constraints |
| System design | Architecture and design decisions |
| Implementation plan | Planned work and implementation methodology |
| Working record | Provisional agreements, qualifications and reasoning |
