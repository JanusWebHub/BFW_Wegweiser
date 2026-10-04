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

The architecture separates building-model authoring, offline compilation and browser presentation. The compiler and browser-client code are organized as follows:

- [src/](src/): Python compiler that builds the routing graph from the modeled floor plans, computes the routes, and serializes the routing data.
- [web/](web/): Browser client that takes the navi-user's request and renders the route on the floor plan alongside navigation instructions.

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
| `README.md` | Introduce the project and guide readers toward its parts. |
| Rulebook | Establish model tenets, definitions and constraints. |
| System design | Specify how those commitments become an organized system: responsibilities, representations, transformations and interfaces. |
| Implementation plan | Outline how planned work is to be implemented. |
| Working record | Preserve current agreements, qualifications and reasoning while they remain provisional. |
