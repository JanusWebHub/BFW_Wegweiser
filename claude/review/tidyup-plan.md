# Plan: make the review scripts runnable

Goal: from a clean checkout plus the Lageplan PDF, one command regenerates the review data and images. Images stay out of the repo.

1. Config. Put all paths in one place at the top of `scripts/load.py`: repo root, path to the Lageplan PDF, output folder. Replace every hard-coded path in the other scripts with it.
2. Lageplan render. Add `scripts/make_lageplan.py`: turn the PDF into `lp_full.png` (full size) and `lp_half.png` (half size) with PyMuPDF. The PDF is stored upside down; the scripts rotate it 180 degrees. The SVG frame is `scan px - (40, 77)` on the half-size image.
3. Remove the source-text chaining. `graph.py`, `fixed.py`, `drawgraph.py`, `cutouts3.py` and `doors.py` currently `exec` each other's source, cut at marker comments. Turn the shared parts into importable functions and import them.
4. One entry point. Add `scripts/run_all.py` that runs in order: checks (`check.py`, `cmp.py`, `graph.py`, `geo.py`, `gaps.py`, `route.py`), corrected graph and routing graph (`fixed.py`, writing `data/`), cut-outs (`cutouts3.py`), door panels (`doors.py`), routing images (`drawgraph.py`). Create the output folders it needs.
5. Scripts README. Replace the snapshot note with: `pip install shapely pillow cairosvg pymupdf`, `python make_lageplan.py <pdf>`, `python run_all.py`.
6. Source of the base data. The scripts read the committed step files under `docs/data/`. Keep them reading from there. When the corrected graph is accepted, add a switch to read it instead.
7. Test. Run everything once from an empty output folder and compare the numbers with `../review-report.md` (171 zones and 206 portals in the merge; 80 of 172 zones unreachable from `E.52` before the fixes; one connected component after).
8. Do not commit generated PNGs. If a few are wanted for the report, add them by hand.
