# Review scripts (snapshot, not runnable yet)

These are the scripts used in the review session, copied as they were. They do not run from this folder as they are.

- Paths are hard-coded to the session's folders (`/home/user/BFW_Wegweiser/docs/data/...`, a scratchpad for outputs).
- Several scripts read each other's source text and cut it at marker comments, so they only work together in the original layout.
- They need `lp_full.png` and `lp_half.png`, renders of the Lageplan PDF that are not in the repo.
- Dependencies: `shapely`, `pillow`, `cairosvg`, `pymupdf`.

Making them runnable is planned in `../TIDYUP-PLAN.md`.

Order of use: `load.py` (loader) → `check.py`, `cmp.py`, `graph.py`, `geo.py`, `gaps.py`, `route.py` (checks) → `fixed.py` (corrected graph, routing graph) → `drawgraph.py`, `cutouts3.py`, `doors.py`, `render.py` (images).
