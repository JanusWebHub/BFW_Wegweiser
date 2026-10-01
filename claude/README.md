# Wegweiser EG review package (2026-10-01)

- `tools/`: the EG Redline page (`eg-redline.html`, version 12) and its source.
- `review/RECAP.md`, `review/CORRECTIONS.md`: conversation recap and every correction by round.
- `review/review-report.md`: the original review of the Claude Design output.
- `review/SPEC-PROPOSALS.md`: proposed `block` kind and nested-room rule for `docs/data`.
- `review/TIDYUP-PLAN.md`: plan to make the scripts runnable.
- `review/data/`: corrected connectivity and routing graphs (178 zones, 207 portals), the batch 2 marks used.
- `review/marks/marks-snapshot.json`: all 97 redline marks, all applied.
- `review/scripts/`: the session scripts (snapshot, not runnable as is). No images are included.

Known gaps: the scripts do not run as they are (hard-coded paths, missing Lageplan renders); the connectivity JSON has no `kind` attribute yet, so blocks appear as ordinary non-crossable zones.
