# Current project state

Snapshot checked on 2026-09-28. This report separates the implemented prototype, the intended design, and decisions still open.

## Repository

The worktree was clean on `local/simpler` at `4d2b422`. All six local branches matched their corresponding JanusWebHub heads when checked:

| Branch | Tip | Relation to `main` |
| --- | --- | --- |
| `main` | `2623bd7` | Current base |
| `model-overhaul` | `2623bd7` | No additional commits |
| `local/simpler` | `4d2b422` | Adds seven tracked design files |
| `feature/east-wing-prototype` | `5fc294c` | Already in `main` ancestry |
| `feature/sql` | `5472812` | Changes only the rulebook relative to `main` |
| `tracker-updates` | `0b918f4` | Adds the historical tracker relative to `main` |

There were no untracked, non-ignored workspace files. Local files absent from Git are under the ignored `docs/ignore/archive/`. The inventory excluded `.git` and `.venv`; it did not cover the separate east-wing worktree or Desktop attachments.

## Documents and program

The [rulebook](../rulebook.md) is the canonical model and currently specifies zone-to-zone queries. [System design](../system-design.md) describes the human-guided modeling pipeline and cost tuning. The [implementation plan](../implementation-plan.md) orders SVG/connectivity, graph compilation, route computation, and tests, but has no browser phase. Its deferral of adjacency-graph production needs to be distinguished from the conceptual pipeline in system design.

The [design views](system-overview.md) explain an intended build and operation flow; they do not describe completed implementation. The east-wing prototype still builds data from hardcoded rows in [build_database.py](../../src/build_database.py), precomputes routes in [calculate_routes.py](../../src/calculate_routes.py), and uses zone selection and route lookup in [east_wing.js](../../web/east_wing.js). The room-number and name-input proposals on `feature/sql` are not part of the current rulebook on `local/simpler`.

## Development strategy

The earlier fixture-first levels remain a proposal, not an agreed schedule. Build artifacts have a dependency order, but implementation and testing can proceed in a different order once the interfaces between components are chosen. Controlled fixtures remain useful for future changes and buildings; fictional data must not be presented as verified guidance.

## Candidate paths and current gaps

The earlier plan proposes defining a minimal routing-graph contract, then testing offline route computation against a controlled graph while human-verified SVG authoring, validation, and graph compilation proceed separately. A later integration check would require compiled graphs to satisfy the same contract and the displayed plan to pass human review. A browser demo at each level, file moves, and the exact order of these efforts remain proposals, not requirements adopted by this report.

The prototype does not yet provide that boundary: graph data is duplicated in Python rows rather than parsed from the SVG; route computation excludes only `aussen` as an intermediate and accounts for special state costs but not segment special costs; the browser fetches the full routed database. These are implementation gaps to account for when choosing increments, not evidence that the proposed contract or export format has been settled.

Decisions not yet finalized:

- The minimal routing-graph contract and assumptions required by the route algorithm, including cost constraints.
- Where the location catalog is authored and whether it is bundled with browser route data or delivered separately.
- The granularity and completion criteria of development increments, including whether each must deliver a browser result.
- How the adjacency-graph step in system design relates to its deferred implementation.

A useful next planning step is to settle the smallest shared contract needed for independently developing graph compilation and offline route computation, then revisit the implementation order.
