# Wegweiser Agent Guide

## Get oriented

- At the start of a task, confirm the active workspace path, repository, branch, and worktree state. Do not assume the repository and workspace contain the same files.
- Use `/wegweiser-catch-up` to gather project and workspace context before continuing complex or stale work.
- Read [README.md](README.md) for project orientation. Use [rulebook.md](docs/rulebook.md) for model definitions and constraints, [system-design.md](docs/system-design.md) for intended architecture, [implementation-plan.md](docs/implementation-plan.md) for planned work, and [working-record.md](docs/working-record.md) for confirmed and provisional agreements.
- Current documents and implementation may not fully capture the project author's intent, which may exist only in transcripts or session history. Consult relevant records when needed to clarify the task.
- Keep confirmed decisions, provisional agreements, and recommendations distinct. Do not infer approval or treat a roadmap as an implementation status report. Ask when relevant intent is unclear.

## Trace before changing

- Identify the active entry point, generated data, and consumer before changing behavior. The `src/main.py` and `web/index.html` path is distinct from `src/build_database.py` -> `src/calculate_routes.py` -> `database_with_routes.json` -> `web/east_wing.js`; trace the relevant path instead of assuming they share a contract.
- Treat artifacts under `claude/review/` and `docs/data/` as evidence from their stated stage. Check their dates and current source files before relying on them as current decisions or data.
- Keep zoning/model authoring separate from the navigation client. Do not expand a task across those boundaries without a concrete dependency.
- Use English for identifiers and documentation; use German for code comments and user-facing text, following the project README.

## Validate carefully

- Run the narrowest relevant check. Existing Python test discovery is `& "$PWD/.venv/Scripts/python.exe" -B -m unittest discover -s src -p "test_*.py"`. The current tests cover the older `main.py` path, not the database builder or route calculator.
- The data-generation scripts can overwrite JSON outputs. Inspect their arguments and choose explicit temporary output paths when validating them; do not regenerate tracked project data casually.
- Report what was checked and any relevant coverage gap. Preserve unrelated worktree changes and keep edits within the requested scope.
