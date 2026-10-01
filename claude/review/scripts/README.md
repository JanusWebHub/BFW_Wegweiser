# Review scripts (snapshot, not runnable yet)

These are the scripts used in the review session, copied as they were. They do not run from this folder as they are.

- Paths are hard-coded to the session's folders (`/home/user/BFW_Wegweiser/docs/data/...`, a scratchpad for outputs).
- Several scripts read each other's source text and cut it at marker comments, so they only work together in the original layout.
- They need `lp_full.png` and `lp_half.png`, renders of the Lageplan PDF that are not in the repo.
- Dependencies: `shapely`, `pillow`, `cairosvg`, `pymupdf`.

Making them runnable is planned in `../TIDYUP-PLAN.md`.

Order of use: `load.py` (loader) → `check.py`, `cmp.py`, `graph.py`, `geo.py`, `gaps.py`, `route.py` (checks) → `fixed.py` (corrected graph, routing graph) → `drawgraph.py`, `cutouts3.py`, `doors.py`, `render.py` (images).

Added since the first snapshot: `batch2.py` (executed from `fixed.py` just before the validation section; applies the redline marks of batch 2 and the hub redraw from `../data/marks_batch2.json`), `markview.py` (marks overlay). `fixed.py` also contains the kitchen re-zoning. Same caveats: paths are hard-coded and the scripts only work together in the original layout.
