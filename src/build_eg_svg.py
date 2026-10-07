import html
import json
import math
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
REDLINE_PATH = ROOT / "claude" / "tools" / "eg-redline.html"
GRAPH_PATH = ROOT / "claude" / "review" / "data" / "routing-graph-fixed.json"
OUTPUT_PATH = ROOT / "web" / "assets" / "bfw-eg.svg"
DATA_PATTERN = re.compile(r"const DATA = (\{.*?\});\r?\nconst SUGG =", re.DOTALL)
IMAGE_PATTERN = re.compile(r'const IMG = ("data:image/[^\"]+");')


def load_source_data(page_path: Path, graph_path: Path) -> tuple[dict[str, Any], str, dict[str, Any]]:
    page_source = page_path.read_text(encoding="utf-8")
    data_match = DATA_PATTERN.search(page_source)
    image_match = IMAGE_PATTERN.search(page_source)
    if data_match is None or image_match is None:
        raise ValueError("Redline page does not contain its expected plan data and underlay")

    redline_data = json.loads(data_match.group(1))
    underlay = json.loads(image_match.group(1))
    routing_graph = json.loads(graph_path.read_text(encoding="utf-8"))
    validate_source_data(redline_data, routing_graph)
    return redline_data, underlay, routing_graph


def validate_source_data(redline_data: dict[str, Any], routing_graph: dict[str, Any]) -> None:
    graph_zone_ids = set(routing_graph["zones"]) - {"exterior"}
    redline_zone_ids = {zone["id"] for zone in redline_data["zones"]}
    if redline_zone_ids != graph_zone_ids:
        raise ValueError("Redline zone ids do not match the current routing graph")

    graph_portals = routing_graph["portals"]
    redline_portals = {portal["id"]: portal for portal in redline_data["portals"]}
    if redline_portals.keys() != graph_portals.keys():
        raise ValueError("Redline portal ids do not match the current routing graph")

    for portal_id, portal in redline_portals.items():
        line = portal["l"]
        if len(line) != 4:
            raise ValueError(f"Invalid portal line in redline data: {portal_id}")
        midpoint = [(line[0] + line[2]) / 2, (line[1] + line[3]) / 2]
        graph_point = graph_portals[portal_id]["point"]
        if math.dist(midpoint, graph_point) > 0.1:
            raise ValueError(f"Redline portal is misaligned with routing graph: {portal_id}")


def number(value: float) -> str:
    return f"{value:g}"


def points_attribute(points: list[list[float]]) -> str:
    return " ".join(f"{number(x)},{number(y)}" for x, y in points)


def polygon_center(points: list[list[float]]) -> tuple[float, float]:
    area_twice = 0.0
    center_x = 0.0
    center_y = 0.0
    for index, point in enumerate(points):
        following = points[(index + 1) % len(points)]
        cross = point[0] * following[1] - following[0] * point[1]
        area_twice += cross
        center_x += (point[0] + following[0]) * cross
        center_y += (point[1] + following[1]) * cross
    if abs(area_twice) < 1e-9:
        return (
            sum(point[0] for point in points) / len(points),
            sum(point[1] for point in points) / len(points),
        )
    return center_x / (3 * area_twice), center_y / (3 * area_twice)


def point_in_polygon(point: tuple[float, float], polygon: list[list[float]]) -> bool:
    inside = False
    previous_index = len(polygon) - 1
    for index, current in enumerate(polygon):
        previous = polygon[previous_index]
        if (current[1] > point[1]) != (previous[1] > point[1]):
            crossing_x = (previous[0] - current[0]) * (point[1] - current[1])
            crossing_x /= previous[1] - current[1]
            if point[0] < crossing_x + current[0]:
                inside = not inside
        previous_index = index
    return inside


def build_eg_svg(
    redline_data: dict[str, Any], underlay: str, routing_graph: dict[str, Any]
) -> str:
    validate_source_data(redline_data, routing_graph)
    x, y, width, height = routing_graph["floors"]["E"]["view_box"]
    colors = {
        "vertical": "#a89a80",
        "circulation": "#d8c9a3",
        "crossable": "#ece3cf",
        "room": "#f5eedd",
    }
    output = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{number(width)}" height="{number(height)}" viewBox="{number(x)} {number(y)} {number(width)} {number(height)}" role="img" aria-labelledby="title description">',
        '<title id="title">BFW Charlottenburg, Erdgeschoss</title>',
        '<desc id="description">Zonen und Portale fuer die EG-Routendarstellung.</desc>',
        "<defs>",
        "<pattern id=\"block-hatch\" width=\"12\" height=\"12\" patternUnits=\"userSpaceOnUse\" patternTransform=\"rotate(45)\"><line x1=\"0\" y1=\"0\" x2=\"0\" y2=\"12\" stroke=\"#8a8374\" stroke-width=\"2\"/></pattern>",
        "<style>",
        ".shell{fill:none;stroke:#2f2b27;stroke-width:8;stroke-linejoin:round}.zone{stroke:#2f3fa8;stroke-width:1.6;stroke-linejoin:round}.zone--vertical{fill:#a89a80;fill-opacity:.55}.zone--circulation{fill:#d8c9a3;fill-opacity:.6}.zone--crossable{fill:#ece3cf;fill-opacity:.4}.zone--room{fill:#f5eedd;fill-opacity:.3}.zone--block{fill:#777168;fill-opacity:.55}.portal-line{fill:none;stroke:#0d6b63;stroke-width:5}.portal-line--door{stroke:#b4561f}.portal-line--exit{stroke:#b4561f;stroke-width:7}.portal-line--virtual{stroke-dasharray:10 8}.portal-point{fill:#fff;stroke:#0d6b63;stroke-width:3}.zone-label{fill:#2f2b27;font:500 10px ui-monospace,monospace;text-anchor:middle;paint-order:stroke;stroke:#fff;stroke-width:2.4;stroke-opacity:.8}</style>",
        "</defs>",
        "<g id=\"underlay\">",
        f'<image href="{underlay}" x="0" y="0" width="1790" height="1000" preserveAspectRatio="none" opacity="0.45" style="filter:grayscale(1)"/>',
        "</g>",
        "<g id=\"shell\">",
        f'<polygon class="shell" points="{points_attribute(redline_data["shell"])}"/>',
        "</g>",
        "<g id=\"zones\">",
    ]

    for zone in redline_data["zones"]:
        polygon = zone["p"]
        if len(polygon) < 3:
            raise ValueError(f"Zone has fewer than three points: {zone['id']}")
        zone_id = html.escape(zone["id"], quote=True)
        zone_kind = html.escape(zone.get("k", "room"), quote=True)
        vertical = zone_kind == "stair" or "aufzug" in zone_id
        circulation = not vertical and (
            zone_kind == "corridor" or (zone_kind == "service" and bool(zone["c"]))
        )
        category = "vertical" if vertical else "circulation" if circulation else "crossable" if zone["c"] else "room"
        classes = ["zone", f"zone--{category}"]
        if zone.get("b"):
            classes.append("zone--block")
        output.append(
            f'<polygon id="zone-{zone_id}" class="{" ".join(classes)}" data-kind="{zone_kind}" data-crossable="{1 if zone["c"] else 0}" points="{points_attribute(polygon)}"/>'
        )
        if zone.get("b"):
            output.append(
                f'<polygon class="block-overlay" points="{points_attribute(polygon)}" fill="url(#block-hatch)" pointer-events="none"/>'
            )

        xs = [point[0] for point in polygon]
        ys = [point[1] for point in polygon]
        if max(xs) - min(xs) >= 46 and max(ys) - min(ys) >= 14:
            center = polygon_center(polygon)
            if not point_in_polygon(center, polygon):
                center = (polygon[0][0], polygon[0][1])
            output.append(
                f'<text class="zone-label" x="{number(center[0])}" y="{number(center[1])}">{zone_id}</text>'
            )
    output.append("</g><g id=\"portals\">")

    for portal in redline_data["portals"]:
        portal_id = html.escape(portal["id"], quote=True)
        line = portal["l"]
        classes = ["portal-line", "portal-line--exit" if portal.get("x") else "portal-line--door"]
        if portal.get("v"):
            classes.append("portal-line--virtual")
        output.append(
            f'<line id="portal-{portal_id}" class="{" ".join(classes)}" x1="{number(line[0])}" y1="{number(line[1])}" x2="{number(line[2])}" y2="{number(line[3])}"/>'
        )
        midpoint_x = (line[0] + line[2]) / 2
        midpoint_y = (line[1] + line[3]) / 2
        output.append(
            f'<circle class="portal-point" cx="{number(midpoint_x)}" cy="{number(midpoint_y)}" r="4"/>'
        )

    output.extend(["</g>", "</svg>"])
    return "\n".join(output) + "\n"


def main() -> None:
    redline_data, underlay, routing_graph = load_source_data(REDLINE_PATH, GRAPH_PATH)
    svg = build_eg_svg(redline_data, underlay, routing_graph)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} with {len(redline_data['zones'])} zones and {len(redline_data['portals'])} portals.")


if __name__ == "__main__":
    main()