import argparse
import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OLD = ROOT / "web" / "eg-routing-graph.json"
DEFAULT_NEW = ROOT / "web" / "eg-routing-graph-new.json"
DEFAULT_OUTPUT = ROOT / "web" / "eg-routing-graph-diff.html"

MISSING = object()
Difference = tuple[str, Any, Any]


def segment_key(segment: Any, index: int) -> str:
    if isinstance(segment, dict):
        portals = segment.get("portals")
        if isinstance(portals, list) and len(portals) == 2:
            return f"[{portals[0]} | {portals[1]}]"
    return f"[index {index}]"


def compare_segment_lists(old: list[Any], new: list[Any], path: str) -> list[Difference]:
    old_by_key = {segment_key(segment, index): segment for index, segment in enumerate(old)}
    new_by_key = {segment_key(segment, index): segment for index, segment in enumerate(new)}
    differences = []

    for key in sorted(old_by_key.keys() | new_by_key.keys()):
        old_segment = old_by_key.get(key, MISSING)
        new_segment = new_by_key.get(key, MISSING)
        if old_segment != new_segment:
            differences.append((f"{path}{key}", old_segment, new_segment))

    return differences


def collect_differences(old: Any, new: Any, path: str = "") -> list[Difference]:
    if old is MISSING or new is MISSING:
        return [] if old is new else [(path, old, new)]
    if old == new:
        return []

    if (
        path.startswith("segments.")
        and isinstance(old, list)
        and isinstance(new, list)
    ):
        return compare_segment_lists(old, new, path)

    if isinstance(old, dict) and isinstance(new, dict):
        differences = []
        for key in sorted(old.keys() | new.keys()):
            child_path = f"{path}.{key}" if path else str(key)
            differences.extend(
                collect_differences(
                    old.get(key, MISSING),
                    new.get(key, MISSING),
                    child_path,
                )
            )
        return differences

    if isinstance(old, list) and isinstance(new, list):
        differences = []
        for index in range(max(len(old), len(new))):
            child_path = f"{path}[{index}]"
            differences.extend(
                collect_differences(
                    old[index] if index < len(old) else MISSING,
                    new[index] if index < len(new) else MISSING,
                    child_path,
                )
            )
        return differences

    return [(path, old, new)]


def corridor_change_category(path: str) -> str | None:
    if path.startswith("segments.E.flur-tr1-1["):
        return "segment"
    if path == "zones.E.flur-tr1-1" or path.startswith("zones.E.flur-tr1-1."):
        return "zone"
    return None


def render_value(value: Any) -> str:
    if value is MISSING:
        return "(absent)"
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def build_report(old_path: Path, new_path: Path) -> str:
    old_graph = json.loads(old_path.read_text(encoding="utf-8"))
    new_graph = json.loads(new_path.read_text(encoding="utf-8"))
    differences = collect_differences(old_graph, new_graph)

    sections: dict[str, list[Difference]] = {}
    for difference in differences:
        top_level = difference[0].split(".", 1)[0]
        sections.setdefault(top_level, []).append(difference)
    visible_count = sum(
        corridor_change_category(path) != "segment"
        for path, _, _ in differences
    )

    rows = []
    for section, section_differences in sorted(sections.items()):
        visible_in_section = sum(
            corridor_change_category(path) != "segment"
            for path, _, _ in section_differences
        )
        group_hidden = " hidden" if visible_in_section == 0 else ""
        rows.append(
            f'<section class="group"{group_hidden}><h2>{html.escape(section)} '
            f'<span class="group-count" data-total="{len(section_differences)}">'
            f'{visible_in_section}/{len(section_differences)} Aenderungen sichtbar</span></h2>'
        )
        for path, old_value, new_value in section_differences:
            escaped_path = html.escape(path)
            searchable = html.escape(path.lower(), quote=True)
            category = corridor_change_category(path) or "other"
            category_class = f" {category}-change" if category != "other" else ""
            hidden_attr = " hidden" if category == "segment" else ""
            rows.append(
                f'<details class="change{category_class}" data-search="{searchable}" '
                f'data-category="{category}"{hidden_attr}>'
                f"<summary><code>{escaped_path}</code></summary>"
                '<div class="values">'
                '<section class="old"><h3>Alt</h3><pre>'
                f"{html.escape(render_value(old_value))}</pre></section>"
                '<section class="new"><h3>Neu</h3><pre>'
                f"{html.escape(render_value(new_value))}</pre></section>"
                "</div></details>"
            )
        rows.append("</section>")

    if not differences:
        rows.append('<p class="empty">No differences found.</p>')

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Routing-Graph-Vergleich</title>
  <style>
    :root {{ color-scheme: light; font: 14px/1.45 "Segoe UI", sans-serif; color: #202a31; background: #f3f5f5; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; }}
    header {{ position: sticky; top: 0; z-index: 2; padding: 16px 22px; background: #fff; border-bottom: 1px solid #d3d9dc; }}
    h1 {{ margin: 0 0 8px; font-size: 20px; }}
    .files {{ color: #53616a; overflow-wrap: anywhere; }}
    .toolbar {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }}
    input, button {{ min-height: 34px; padding: 6px 10px; border: 1px solid #b7c0c5; border-radius: 3px; background: #fff; color: inherit; }}
    input {{ flex: 1 1 260px; }}
    button {{ cursor: pointer; }}
    .toggle {{ display: flex; align-items: center; gap: 7px; }}
    .toggle input {{ flex: 0 0 auto; min-height: 0; margin: 0; padding: 0; }}
    main {{ max-width: 1500px; margin: 0 auto; padding: 16px 22px 48px; }}
    .group {{ margin: 0 0 22px; }}
    .group h2 {{ display: flex; gap: 10px; align-items: baseline; margin: 0 0 8px; font-size: 16px; }}
    .group h2 span {{ color: #64737c; font-size: 12px; font-weight: 400; }}
    .change {{ margin: 5px 0; border: 1px solid #d1d8db; border-radius: 3px; background: #fff; }}
    .change[hidden], .group[hidden] {{ display: none; }}
    summary {{ padding: 8px 10px; cursor: pointer; }}
    summary code {{ overflow-wrap: anywhere; }}
    .values {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); border-top: 1px solid #d1d8db; }}
    .values section {{ min-width: 0; padding: 10px; }}
    .values section + section {{ border-left: 1px solid #d1d8db; }}
    .old h3 {{ color: #9b362a; }}
    .new h3 {{ color: #13714e; }}
    h3 {{ margin: 0 0 6px; font-size: 12px; text-transform: uppercase; }}
    pre {{ max-height: 65vh; overflow: auto; margin: 0; padding: 10px; background: #f5f7f7; white-space: pre-wrap; overflow-wrap: anywhere; }}
    .empty {{ padding: 18px; background: #fff; }}
    @media (max-width: 760px) {{ .values {{ grid-template-columns: 1fr; }} .values section + section {{ border-left: 0; border-top: 1px solid #d1d8db; }} }}
  </style>
</head>
<body>
  <header>
        <h1>Routing-Graph-Differenzen: {len(differences)}</h1>
        <p id="visible-count" aria-live="polite">Sichtbar: {visible_count} / {len(differences)}</p>
        <div class="files">Alt: {html.escape(str(old_path))}<br>Neu: {html.escape(str(new_path))}</div>
    <div class="toolbar">
            <input id="filter" type="search" placeholder="Aenderungspfade filtern">
            <label class="toggle"><input id="hide-segments" type="checkbox" checked> Segmente in E.flur-tr1-1 ausblenden</label>
            <label class="toggle"><input id="hide-zone-changes" type="checkbox"> Zonen&auml;nderungen in E.flur-tr1-1 ausblenden</label>
            <button id="expand" type="button">Alle aufklappen</button>
            <button id="collapse" type="button">Alle zuklappen</button>
    </div>
  </header>
  <main>{''.join(rows)}</main>
  <script>
    const filter = document.querySelector('#filter');
        const hideSegments = document.querySelector('#hide-segments');
        const hideZoneChanges = document.querySelector('#hide-zone-changes');
        const totalDifferences = {len(differences)};

        function updateVisibility() {{
      const query = filter.value.toLowerCase();
            let visibleDifferences = 0;
            for (const group of document.querySelectorAll('.group')) {{
                let visibleInGroup = 0;
                const rows = group.querySelectorAll('.change');
                for (const row of rows) {{
                    const hiddenByCategory = (hideSegments.checked && row.dataset.category === 'segment')
                        || (hideZoneChanges.checked && row.dataset.category === 'zone');
                    row.hidden = hiddenByCategory || !row.dataset.search.includes(query);
                    if (!row.hidden) visibleInGroup += 1;
                }}
                group.hidden = visibleInGroup === 0;
                visibleDifferences += visibleInGroup;
                group.querySelector('.group-count').textContent = `${{visibleInGroup}}/${{rows.length}} Aenderungen sichtbar`;
            }}
            document.querySelector('#visible-count').textContent = `Sichtbar: ${{visibleDifferences}} / ${{totalDifferences}}`;
        }}

        filter.addEventListener('input', updateVisibility);
        hideSegments.addEventListener('change', updateVisibility);
        hideZoneChanges.addEventListener('change', updateVisibility);
    document.querySelector('#expand').addEventListener('click', () => document.querySelectorAll('.change:not([hidden])').forEach(row => row.open = true));
    document.querySelector('#collapse').addEventListener('click', () => document.querySelectorAll('.change').forEach(row => row.open = false));
        updateVisibility();
  </script>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create an HTML diff for two routing graphs")
    parser.add_argument("old", nargs="?", type=Path, default=DEFAULT_OLD)
    parser.add_argument("new", nargs="?", type=Path, default=DEFAULT_NEW)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report(args.old, args.new)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote routing graph comparison to {args.output}.")


if __name__ == "__main__":
    main()