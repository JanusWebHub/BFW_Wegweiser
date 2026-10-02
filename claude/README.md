# Wegweiser EG review package (2026-10-02)

- `tools/`: the EG Redline page (`eg-redline.html`) and its source (`page-source/`: template, `gen_data.py`, `build.py`).
- `review/RECAP.md`, `review/CORRECTIONS.md`: conversation recap and every correction by round (rounds 1 to 8). `review/SESSION-NOTES.md`: working notes and pipeline rules.
- `review/review-report.md`: the original review of the Claude Design output. `review/SPEC-PROPOSALS.md`: proposed `block` kind and nested-room rule. `review/TIDYUP-PLAN.md`: plan to make the scripts runnable.
- `review/data/`: corrected connectivity and routing graphs (193 zones, 219 portals), `marks_batch2.json` (all marks the pipeline uses), `sugg.json` (current suggestions).
- `review/marks/marks-snapshot.json`: all 236 redline marks, all applied.
- `review/scripts/`: the session scripts (snapshot, not runnable as is). No images are included.

Known gaps: the scripts do not run as they are (hard-coded paths, missing Lageplan renders); the connectivity JSON has no `kind` attribute yet, so blocks appear as ordinary non-crossable zones.
