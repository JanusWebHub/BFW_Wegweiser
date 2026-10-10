# Review scripts (inspiration only)

Written by Claude Code in a cloud session. They do not run as they are (hardcoded paths, scripts that execute each other's source, missing Lageplan renders). Dependencies: shapely, pillow, cairosvg, pymupdf. Some of their rules were later changed or never approved; take ideas, not rules.

- `load.py`: parser for the zoning SVG and connectivity JSON.
- `check.py`: validator checklist (id parity, portal geometry, overlaps, gaps, outside-shell area).
- `graph.py`: reachability, crossable components, adjacent zones without a portal.
- `geo.py`: convexity ratio, segments leaving their zone.
- `gaps.py`: coverage by difference and union.
- `chk.py`: deviation of final zones from drawn outlines.
- `route.py`: what-if routing with added portals.
- `sugg2.py`: suggestion record with highlight and proposed geometry.
- `render.py`: Lageplan overlay with the BFW registration offset.

`legacy/`: the pipeline that applied the marks (`batch2.py`, `fixed.py`), image renderers and comparison scripts.
