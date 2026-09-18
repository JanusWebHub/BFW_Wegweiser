# Architectural decisions

## 1. Offline graph compiler (`src/`) and static presentation client (`web/`)

Status: Accepted

Adopt a decoupled two-tier architecture:

- `src/`: Python serves as an offline build tool and graph compiler. It defines
  coordinates, edge weights, and pathfinding rules, precomputing routes and
  exporting static artifacts (`web/data.json` and companion `web/data.js`).
- `web/`: A self-contained static frontend. It performs constant-time lookups
  against the precomputed data and renders SVG paths onto the floor plan,
  containing zero graph traversal or routing algorithms.

Standard directory naming (`src/` and `web/`) is adopted to ensure immediate
compatibility with linters, test runners, and static file servers without custom
path configuration.

## 2. Testing sits at the pipeline's boundaries

Status: Accepted

Each handover in the pipeline gets one minimal, contract-focused check: the
floor plan against the rulebook before it enters the compiler, and the exported
data against its contract before it reaches the viewer. Algorithm checks are
isolated from both, so the routing algorithm can change without either contract
being rewritten.

The boundaries are where a change on one side breaks the other silently. Nothing
in between needs guarding, and testing anywhere else costs more than it catches.
