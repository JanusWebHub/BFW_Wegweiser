# Devlog

Running log of notable changes and the reasoning behind them. Complements commit messages with slightly more context. Each entry is headed by timestamp and contributor initials. Entries don't map 1:1 to commits. Ordered most recent first. Covers changes made after forking; upstream history predates this log.

## 2026-09-11 10:45 - DM

Documented project roadmap checklist and established trunk-based development workflow conventions for contributor collaboration.

In [README.md](README.md), added a distilled high-level roadmap checklist mapping the project's four active development phases, and documented workflow guidelines: routine changes commit directly to `main`, while multi-commit or disruptive refactors use short-lived task branches rebased and fast-forward merged onto `main` to preserve a clean, linear commit history.

In [docs/roadmap.md](docs/roadmap.md), added an Execution & Tracking section formalizing the project tracking model: macro-level phases in [README.md](README.md) map 1:1 to container GitHub Milestones, while detailed technical bullet points in [docs/roadmap.md](docs/roadmap.md) serve directly as actionable micro GitHub Issues assigned to individual contributors.

## 2026-09-09 14:10 - DM

Restructured [src/test_main.py](src/test_main.py) into two distinct test classes and established a minimal testing policy in [docs/adr.md](docs/adr.md).

To catch cross-tier data breakages without slowing prototyping, testing is structured into two classes sharing module fixtures via `setUpClass`:

- `RoutingContractTests`: Validates the interface between the compiler and the viewer. Checks presence of top-level keys (`start`, `points`, `destinations`, `routes`), ensures coordinates are numeric pairs, and confirms every declared destination has a valid non-empty route starting at `startpunkt` and ending at the destination.
- `PathfindingAlgorithmTests`: Isolates route traversal checks for `build_graph()` and `find_path()`, keeping graph logic verified independently from export formatting.

Tests remain co-located in [src/test_main.py](src/test_main.py) using standard unittest discovery (`python -m unittest discover -s src`). JavaScript tests and a dedicated root `tests/` directory are deferred to keep dependencies at zero while the viewer contains no routing logic.

## 2026-09-09 11:35 - DM

Synchronized multi-machine development by integrating the architectural decision record on `main` and cleanly rebasing the script-split pipeline.

Before pulling the decoupled `src/` and `web/` layout implemented on the secondary machine, [docs/adr.md](docs/adr.md) was finalized and committed to `main`. The record formally establishes the project's core architecture: Python acts as an offline graph compiler exporting precomputed static data, while the browser client operates strictly as an algorithm-free presentation layer, with usage analytics deferred and decoupled.

To integrate the new implementation without creating divergent branches or merge bubbles, we completed Phase 2 of [docs/temp_branch_strategy.md](docs/temp_branch_strategy.md):

- Committed [docs/adr.md](docs/adr.md) directly to `main`.
- Rebased the remote `script-split` feature branch onto updated `main`, placing the repository restructuring and compiler export cleanly on top of the ADR.
- Fast-forward merged `main` to the rebased branch tip and pushed to `origin`.
- Pruned the temporary `script-split` branch reference both locally and from the remote.

This leaves `main` with a strictly linear history, unifying the architectural rationale with the split repository structure ready for algorithmic upgrades (such as Dijkstra and cost modeling).

Commits: `1bdf03f` (ADR), `dcaac7f`..`e39133e` (rebased pipeline)

## 2026-09-08 23:55 - DM

Added direct local file execution support by exporting routing data as a JavaScript asset alongside the JSON artifact, resolving browser CORS restrictions when opening the client via local file URIs (`file:///`).

During browser testing, opening [web/index.html](web/index.html) directly from the filesystem caused Chrome and Edge to block `fetch("data.json")` under strict local same-origin policies, triggering an error message in the status panel. While serving through `python -m http.server -d web 8000` functioned as expected, requiring a running HTTP process complicates offline kiosk deployment scenarios.

To support both execution modes:

- In [src/main.py](src/main.py), updated `export_data()` to write both [web/data.json](web/data.json) and a companion [web/data.js](web/data.js) assigning data to `window.ROUTING_DATA`.
- In [web/index.html](web/index.html), added `<script src="data.js" defer></script>` prior to [web/script.js](web/script.js).
- In [web/script.js](web/script.js), updated `loadRoutingData()` to check for `window.ROUTING_DATA` first for immediate synchronous initialization, falling back to `fetch("data.json")` when served over HTTP.

This enables opening [web/index.html](web/index.html) directly via double-click in Explorer without local server dependencies while retaining standard JSON contract compatibility.

## 2026-09-08 23:31 - DM

Decoupled the routing pipeline into an offline Python data compiler and a static browser visualizer, implementing the client-server separation without requiring an active HTTP server process.

In [src/main.py](src/main.py), removed `matplotlib` and image loading routines (`load_map()`, `draw_path()`) along with interactive console prompts. Added `compile_routing_data()` and `export_data()` to precalculate all routes from `startpunkt` to checkpoints and serialize coordinates, destinations, and route paths directly into [web/data.json](web/data.json).

In [web/script.js](web/script.js), removed hardcoded network tables (`connections`, `points`, `destinations`) and the client-side BFS `findPath()` implementation, which previously appeared to exhibit a directed-edge traversal bug. Added `loadRoutingData()` to asynchronously fetch [web/data.json](web/data.json) on startup and resolve paths via constant-time lookup (`appData.routes[destination]`), binding coordinates directly to the SVG route overlay.

In [web/index.html](web/index.html), updated the floor plan image reference to [web/assets/Grundriss_mit_Knotenpunkten.png](web/assets/Grundriss_mit_Knotenpunkten.png), ensuring the static client remains self-contained. In [src/test_main.py](src/test_main.py), removed headless matplotlib backend configuration and added `test_compile_routing_data_structure` to verify the compiled data output.

Commits: `0d298b3`

## 2026-09-08 23:15 - DM

Reorganized the repository into a symmetrical two-tier layout separating offline Python tooling from static web assets.

Moved [src/main.py](src/main.py) and [src/test_main.py](src/test_main.py) into [src/](src/). Relocated the map asset into [web/assets/Grundriss_mit_Knotenpunkten.png](web/assets/Grundriss_mit_Knotenpunkten.png) so static hosting environments may serve the site without parent directory traversal. Imported baseline frontend files ([web/index.html](web/index.html), [web/script.js](web/script.js), [web/style.css](web/style.css)) from the original author's repository into [web/](web/) as a starting point for the client interface.

Added [docs/adr_directory_structure.md](docs/adr_directory_structure.md) evaluating repository layout options (such as [src/](src/) and [web/](web/) versus builder and viewer pairings), documenting the choice of [src/](src/) and [web/](web/) for standard Python tooling and static host compatibility. Added [docs/current_state.md](docs/current_state.md) to record the active baseline and next milestones. Added an initial [README.md](README.md) describing the two-tier architecture, directory structure, and local execution instructions.

Commits: `0aa6e6d`

## 2026-09-08 21:23 - DM

Documented a temporary branch synchronization strategy in [docs/temp_branch_strategy.md](docs/temp_branch_strategy.md) to coordinate work across multiple development machines.

Because the secondary machine holds unpushed local commits on `main` (including architectural decision records), pushing new work directly to `origin/main` from this machine would likely cause branch divergence. Established the procedure to isolate the script-splitting changes on a temporary `script-split` branch, rebase onto local `main` on the secondary machine, fast-forward merge, and delete `script-split` to preserve a clean, linear history. Initialized the `script-split` branch under this workflow.

Commits: `9c3fecb`

## 2026-09-03 09:19 - DM

Added type hints to `build_graph`/`find_path` parameters — the minimum needed for Pylance's Basic type-checking mode to catch call-site type mismatches. Return types and local variables are already inferred automatically by Pylance, so left unannotated to keep the change minimal. Earlier attempt annotated the whole file (module-level data, return types, locals); reverted in favor of this minimal version so the import-removal, debug-cleanup, and type-hint changes could each land as their own commit.

Commits: `285931a`

## 2026-09-03 09:15 - DM

Removed obsolete debug print statements from `main()` (`print(user_input)`, `print(os.getcwd())`, `print(os.listdir())`). These were leftover artifacts from debugging the original hardcoded image-path bug and served no purpose for the end user once the path was fixed.

Commits: `1b87f1b`

## 2026-09-03 09:14 - DM

Removed a redundant `deque` import inside `find_path()` — it was already imported at module level, so the inner import was dead duplication left over from earlier iterations. No behavior change.

Commits: `4c570d8`

## 2026-09-03 08:26 - DM

Established the project's language convention and renamed all German identifiers to English accordingly: identifiers, code structure, commit messages, and docs stay English; comments and user-facing strings stay German for the course's German-speaking audience. Graph node label *values* (e.g. `"knoten_1"`, `"startpunkt"`, `"ost_1"`) were deliberately left German too — they share one namespace with user-typed checkpoint names (which must stay German), so keeping the whole namespace uniform avoided a worse, mixed-language graph. Renamed: `startpunkt`→`start_point`, `knotenpunkte`→`nodes`, `verbindungen`→`connections` (incl. its `verbindungN`→`connectionN` keys), `nutzer_eingabe`→`user_input`, `punkt_a`/`punkt_b`→`point_a`/`point_b`, `karte`→`map_image`, `ziel`→ `target`, `weg`→`path`.

Commits: `1c0fa7a`

## 2026-09-02 14:04 - DM

Added `__pycache__` to `.gitignore`. The folder was generated as a side effect of testing `import main` (to verify the `__main__` guard below doesn't trigger side effects on import) and showed up as untracked — Python's compiled bytecode cache should never be version-controlled.

Commits: `cc82513`

## 2026-09-02 14:01 - DM

Wrapped executable script logic in a `main()` function guarded by `if __name__ == "__main__":`. Previously, every line (input prompt, image loading, pathfinding) executed immediately at module load, so importing `main.py` from elsewhere would trigger all of it as a side effect. Data and function definitions stay at module level; only the runtime logic moved into `main()`. No behavior change — verified with a piped-input test run and an `import main` test.

Commits: `3c907c1`

## 2026-09-02 13:50 - DM

Added validation for the user's checkpoint input. Previously, an invalid target string caused `find_path` to silently return `None`, printing `Pfad: None` with no explanation. Now checks the input against `checkpoints` and prints a clear German error message before exiting.

Commits: `1914d74`

## 2026-09-02 13:45 - DM

Added error handling around `plt.imread()`. A missing or renamed map image previously crashed with an unhandled traceback; now fails with a clear German error message instead.

Commits: `46990aa`

## 2026-09-02 13:41 - DM

Fixed the hardcoded absolute path to `Grundriss_mit_Knotenpunkten.png` (originally pointing to the original author's local machine path, `E:\TN_Daten\Schmitz\Code_Projekts\...`), which broke the script for any other contributor. Now resolved relative to the script's own directory via `__file__`, independent of the caller's working directory.

Commits: `5d26c44`

## 2026-09-02 13:18 - DM

Added `images/` to `.gitignore`. While deciding where the map image should live, it was briefly moved into an `images/` subfolder and then back to the project root (kept at root, since it's a required runtime asset, consistent with the original author's layout). Along the way, an unrelated `images/` folder containing personal photos appeared in the working directory (likely synced in from elsewhere) — excluded via `.gitignore` rather than tracked.

Commits: `bcae946`

## 2026-09-01 14:02 - DM

Updated the environment snapshot doc after upgrading `pip`/`setuptools`/ `wheel` globally and creating the project's `.venv` with `matplotlib` installed. Reformatted the table into Global vs. Project venv sections.

Commits: `2089dd8`

## 2026-09-01 13:47 - DM

Added `.venv/` to `.gitignore` after creating the project's virtual environment, so it isn't accidentally committed.

Commits: `8cee102`

## 2026-09-01 13:41 - DM

Created `docs/environment_snapshot.md` to record installed tool versions (Python, pip, Git, VS Code, PowerShell) at project setup time, for reproducibility and onboarding as a new contributor to the fork.

Commits: `365a2b4`

