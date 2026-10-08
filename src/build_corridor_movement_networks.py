import argparse
import heapq
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONNECTIVITY = ROOT / "web" / "eg-connectivity-graph.json"
DEFAULT_SVG = ROOT / "web" / "assets" / "bfw-eg.svg"

Point = tuple[float, float]
GRID_STEP = 2.0
PORTAL_OUTLINE_TOLERANCE = 12.0
DIRECT_CENTERLINE_PORTAL_PAIRS = {
    "E.flur-tr7-1": (
        "E.flur-tr7-1_E.flur-tr7-4",
        "E.flur-tr7-1_E.flur-tr9-3",
    ),
}
CENTERLINE_PORTAL_WAYPOINTS = {
    "E.flur-tr1-3": {
        "E.flur-tr1-3_E.flur-tr2-3": (520.5, 528.5),
    },
}
MAX_CENTERLINE_SEGMENT_LENGTH = {
    "E.flur-tr3-1": 8.0,
}


def _simplify_polygon(points: list[Point]) -> list[Point]:
    simplified: list[Point] = []
    for point in points:
        if not simplified or math.dist(point, simplified[-1]) > 0.1:
            simplified.append(point)
    if len(simplified) > 2 and math.dist(simplified[0], simplified[-1]) <= 0.1:
        simplified.pop()

    changed = True
    while changed and len(simplified) > 3:
        changed = False
        for index, point in enumerate(simplified):
            previous = simplified[index - 1]
            following = simplified[(index + 1) % len(simplified)]
            first = (point[0] - previous[0], point[1] - previous[1])
            second = (following[0] - point[0], following[1] - point[1])
            cross = abs(first[0] * second[1] - first[1] * second[0])
            forward = first[0] * second[0] + first[1] * second[1] >= 0
            if cross <= 0.45 * max(1.0, math.dist(previous, following)) and forward:
                simplified.pop(index)
                changed = True
                break
    return simplified


def point_in_polygon(point: Point, polygon: list[Point]) -> bool:
    if any(
        _distance_to_segment(point, first, second) <= 1e-6
        for first, second in zip(polygon, polygon[1:] + polygon[:1])
    ):
        return True
    x, y = point
    inside = False
    for first, second in zip(polygon, polygon[1:] + polygon[:1]):
        if (first[1] > y) != (second[1] > y):
            crossing_x = (
                (second[0] - first[0]) * (y - first[1])
                / (second[1] - first[1])
                + first[0]
            )
            if x < crossing_x:
                inside = not inside
    return inside


def _distance_to_segment(point: Point, first: Point, second: Point) -> float:
    dx = second[0] - first[0]
    dy = second[1] - first[1]
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return math.dist(point, first)
    projection = max(
        0.0,
        min(
            1.0,
            (
                (point[0] - first[0]) * dx
                + (point[1] - first[1]) * dy
            )
            / length_squared,
        ),
    )
    closest = (first[0] + projection * dx, first[1] + projection * dy)
    return math.dist(point, closest)


def _distance_to_boundary(point: Point, polygon: list[Point]) -> float:
    return min(
        _distance_to_segment(point, first, second)
        for first, second in zip(polygon, polygon[1:] + polygon[:1])
    )


def _closest_boundary_point(point: Point, polygon: list[Point]) -> Point:
    candidates = []
    for first, second in zip(polygon, polygon[1:] + polygon[:1]):
        dx = second[0] - first[0]
        dy = second[1] - first[1]
        length_squared = dx * dx + dy * dy
        projection = (
            0.0
            if length_squared == 0
            else max(
                0.0,
                min(
                    1.0,
                    (
                        (point[0] - first[0]) * dx
                        + (point[1] - first[1]) * dy
                    )
                    / length_squared,
                ),
            )
        )
        boundary_point = (first[0] + projection * dx, first[1] + projection * dy)
        candidates.append((math.dist(point, boundary_point), boundary_point))
    return min(candidates)[1]


def _segment_inside_polygon(
    first: Point, second: Point, polygon: list[Point], sample_step: float = 1.0
) -> bool:
    length = math.dist(first, second)
    samples = max(1, math.ceil(length / sample_step))
    return all(
        point_in_polygon(
            (
                first[0] + (second[0] - first[0]) * index / samples,
                first[1] + (second[1] - first[1]) * index / samples,
            ),
            polygon,
        )
        for index in range(samples + 1)
    )


def _grid_path(polygon: list[Point], start_point: Point, target_point: Point) -> list[Point]:
    start_boundary = (
        start_point
        if point_in_polygon(start_point, polygon)
        else _closest_boundary_point(start_point, polygon)
    )
    target_boundary = (
        target_point
        if point_in_polygon(target_point, polygon)
        else _closest_boundary_point(target_point, polygon)
    )
    if (
        math.dist(start_point, start_boundary) > PORTAL_OUTLINE_TOLERANCE
        or math.dist(target_point, target_boundary) > PORTAL_OUTLINE_TOLERANCE
    ):
        raise ValueError(
            f"Portal point is too far from corridor outline: "
            f"{start_point} to {start_boundary}, {target_point} to {target_boundary}"
        )
    min_x = min(point[0] for point in polygon)
    min_y = min(point[1] for point in polygon)
    max_x = max(point[0] for point in polygon)
    max_y = max(point[1] for point in polygon)

    cells: list[Point] = []
    x_start = math.floor(min_x / GRID_STEP) * GRID_STEP
    y_start = math.floor(min_y / GRID_STEP) * GRID_STEP
    for iy in range(math.ceil((max_y - y_start) / GRID_STEP) + 1):
        y = y_start + iy * GRID_STEP
        for ix in range(math.ceil((max_x - x_start) / GRID_STEP) + 1):
            point = (x_start + ix * GRID_STEP, y)
            if point_in_polygon(point, polygon):
                cells.append(point)
    if not cells:
        raise ValueError("Corridor polygon contains no centerline grid points")

    clearances = {
        point: _distance_to_boundary(point, polygon) for point in cells
    }
    def nearest_visible_cell(point: Point) -> Point:
        for cell in sorted(cells, key=lambda candidate: math.dist(candidate, point)):
            if _segment_inside_polygon(point, cell, polygon, sample_step=0.5):
                return cell
        raise ValueError(
            f"Point {point} cannot reach an interior centerline point"
        )

    start = nearest_visible_cell(start_boundary)
    target = nearest_visible_cell(target_boundary)

    distances = {start: 0.0}
    parents: dict[Point, Point] = {}
    queue = [(0.0, start)]
    offsets = (
        (-GRID_STEP, -GRID_STEP),
        (-GRID_STEP, 0),
        (-GRID_STEP, GRID_STEP),
        (0, -GRID_STEP),
        (0, GRID_STEP),
        (GRID_STEP, -GRID_STEP),
        (GRID_STEP, 0),
        (GRID_STEP, GRID_STEP),
    )

    while queue:
        distance, point = heapq.heappop(queue)
        if distance != distances.get(point):
            continue
        if point == target:
            break
        for dx, dy in offsets:
            neighbor = (point[0] + dx, point[1] + dy)
            if neighbor not in clearances or not _segment_inside_polygon(
                point, neighbor, polygon, sample_step=GRID_STEP / 2
            ):
                continue
            clearance = max(
                0.5, min(clearances[point], clearances[neighbor])
            )
            length = math.hypot(dx, dy)
            candidate = distance + length * (
                1 + 6 / (clearance + 0.5) ** 2
            )
            if candidate < distances.get(neighbor, math.inf):
                distances[neighbor] = candidate
                parents[neighbor] = point
                heapq.heappush(queue, (candidate, neighbor))

    if target not in distances:
        raise ValueError("Corridor portals are disconnected inside the outline")

    path = [target]
    while path[-1] != start:
        path.append(parents[path[-1]])
    path.reverse()
    full_path = [start_point]
    if math.dist(start_point, start_boundary) > 0.001:
        full_path.append(start_boundary)
    full_path.extend(path)
    if math.dist(target, target_boundary) > 0.001:
        full_path.append(target_boundary)
    full_path.append(target_point)
    return full_path


def _point_to_segment_projection(point: Point, first: Point, second: Point) -> Point:
    dx = second[0] - first[0]
    dy = second[1] - first[1]
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return first
    projection = max(
        0.0,
        min(
            1.0,
            (
                (point[0] - first[0]) * dx
                + (point[1] - first[1]) * dy
            )
            / length_squared,
        ),
    )
    return (first[0] + projection * dx, first[1] + projection * dy)


def _simplify_path(
    path: list[Point],
    polygon: list[Point],
    protected_points: set[Point] | None = None,
) -> list[Point]:
    protected_points = protected_points or set()
    path = [
        point
        for index, point in enumerate(path)
        if index == 0 or math.dist(point, path[index - 1]) > 0.001
    ]
    if len(path) < 3:
        return path

    keep = {0, len(path) - 1}
    protected_indices = {
        index for index, point in enumerate(path) if point in protected_points
    }
    keep.update(protected_indices)
    anchors = sorted(keep)
    stack = list(zip(anchors, anchors[1:]))
    while stack:
        start, end = stack.pop()
        if end - start < 2:
            continue
        furthest_index = max(
            range(start + 1, end),
            key=lambda index: _distance_to_segment(
                path[index], path[start], path[end]
            ),
        )
        if (
            _distance_to_segment(path[furthest_index], path[start], path[end]) > 3
            or not _segment_inside_polygon(path[start], path[end], polygon)
        ):
            keep.add(furthest_index)
            stack.extend(((start, furthest_index), (furthest_index, end)))
    return [path[index] for index in sorted(keep)]


def _densify_path(path: list[Point], max_segment_length: float) -> list[Point]:
    dense_path = [path[0]]
    for first, second in zip(path, path[1:]):
        segment_count = max(
            1, math.ceil(math.dist(first, second) / max_segment_length)
        )
        dense_path.extend(
            (
                first[0] + (second[0] - first[0]) * index / segment_count,
                first[1] + (second[1] - first[1]) * index / segment_count,
            )
            for index in range(1, segment_count + 1)
        )
    return dense_path


def build_movement_network(
    zone_id: str,
    polygon_points: list[Point],
    portals: list[tuple[str, Point]],
    centerline_portals: tuple[str, str] | None = None,
    centerline_waypoints: dict[str, Point] | None = None,
) -> dict[str, Any]:
    if len(portals) < 2:
        raise ValueError(f"Corridor must have at least two portals: {zone_id}")
    polygon = _simplify_polygon(polygon_points)
    ordered_portals = sorted(portals)
    centerline_waypoints = centerline_waypoints or {}
    portal_indices = {
        portal_id: index for index, (portal_id, _) in enumerate(ordered_portals)
    }
    if any(portal_id not in portal_indices for portal_id in centerline_waypoints):
        raise ValueError(f"Centerline waypoint portal is missing in {zone_id}")
    if centerline_portals is None:
        start_index, end_index = max(
            (
                (first, second)
                for first in range(len(ordered_portals))
                for second in range(first + 1, len(ordered_portals))
            ),
            key=lambda pair: math.dist(
                ordered_portals[pair[0]][1], ordered_portals[pair[1]][1]
            ),
        )
    else:
        indices = {
            portal_id: index
            for index, (portal_id, _) in enumerate(ordered_portals)
        }
        if any(portal_id not in indices for portal_id in centerline_portals):
            raise ValueError(
                f"Centerline portal pair is missing from corridor {zone_id}"
            )
        start_index, end_index = (
            indices[portal_id] for portal_id in centerline_portals
        )
    centerline_start = ordered_portals[start_index][1]
    centerline_end = ordered_portals[end_index][1]
    if centerline_portals is None:
        if centerline_waypoints:
            dx = centerline_end[0] - centerline_start[0]
            dy = centerline_end[1] - centerline_start[1]
            length_squared = dx * dx + dy * dy
            waypoints = sorted(
                centerline_waypoints.values(),
                key=lambda point: (
                    (point[0] - centerline_start[0]) * dx
                    + (point[1] - centerline_start[1]) * dy
                )
                / length_squared,
            )
            path = []
            current = centerline_start
            for waypoint in [*waypoints, centerline_end]:
                leg = _grid_path(polygon, current, waypoint)
                if not path:
                    path.extend(leg)
                else:
                    overlap = 0
                    while (
                        overlap < len(path) - 1
                        and overlap < len(leg) - 1
                        and math.dist(
                            path[-2 - overlap], leg[1 + overlap]
                        )
                        <= 0.01
                    ):
                        overlap += 1
                    path.extend(leg[1 + overlap :])
                current = waypoint
            path = _simplify_path(path, polygon, set(waypoints[:-1]))
        else:
            path = _simplify_path(
                _grid_path(polygon, centerline_start, centerline_end), polygon
            )
    else:
        sample_count = max(2, math.ceil(math.dist(centerline_start, centerline_end) / 0.5))
        if not all(
            point_in_polygon(
                (
                    centerline_start[0]
                    + (centerline_end[0] - centerline_start[0]) * index / sample_count,
                    centerline_start[1]
                    + (centerline_end[1] - centerline_start[1]) * index / sample_count,
                ),
                polygon,
            )
            for index in range(1, sample_count)
        ):
            raise ValueError(f"Direct corridor centerline leaves zone {zone_id}")
        path = [centerline_start, centerline_end]
    if zone_id in MAX_CENTERLINE_SEGMENT_LENGTH:
        path = _densify_path(path, MAX_CENTERLINE_SEGMENT_LENGTH[zone_id])
    start_portal = ordered_portals[start_index][0]
    end_portal = ordered_portals[end_index][0]

    junctions: dict[str, list[float]] = {}
    backbone = [start_portal]
    start_point = ordered_portals[start_index][1]
    end_point = ordered_portals[end_index][1]
    previous_point = start_point
    for point in path[1:-1]:
        if math.dist(point, previous_point) < 0.01 or math.dist(point, end_point) < 0.01:
            continue
        junction_id = f"j.{zone_id}.center-{len(junctions) + 1:03d}"
        junctions[junction_id] = [round(point[0], 3), round(point[1], 3)]
        backbone.append(junction_id)
        previous_point = point
    backbone.append(end_portal)

    node_points: dict[str, Point] = {
        start_portal: ordered_portals[start_index][1],
        end_portal: ordered_portals[end_index][1],
        **{node_id: tuple(point) for node_id, point in junctions.items()},
    }
    connectors: dict[str, list[str]] = {}
    for portal_id, portal_point in ordered_portals:
        if portal_id in (start_portal, end_portal):
            continue
        if portal_id in centerline_waypoints:
            waypoint_index = next(
                (
                    index
                    for index, node_id in enumerate(backbone)
                    if node_id in junctions
                    and math.dist(
                        tuple(junctions[node_id]), centerline_waypoints[portal_id]
                    )
                    <= 0.001
                ),
                None,
            )
            if waypoint_index is None or waypoint_index == 0 or waypoint_index == len(backbone) - 1:
                raise ValueError(
                    f"Centerline waypoint is not internal to the backbone: {portal_id}"
                )
            connectors[portal_id] = [
                backbone[waypoint_index - 1],
                backbone[waypoint_index + 1],
            ]
            continue
        best_segment = min(
            range(len(backbone) - 1),
            key=lambda index: math.dist(
                portal_point,
                _point_to_segment_projection(
                    portal_point,
                    node_points[backbone[index]],
                    node_points[backbone[index + 1]],
                ),
            ),
        )
        connectors[portal_id] = [
            backbone[best_segment],
            backbone[best_segment + 1],
        ]

    return {
        "backbone": backbone,
        "junctions": junctions,
        "connectors": connectors,
    }


def add_connector_paths(
    zone_id: str,
    network: dict[str, Any],
    polygon_points: list[Point],
    portals: list[tuple[str, Point]],
) -> None:
    polygon = _simplify_polygon(polygon_points)
    portal_points = dict(portals)
    node_points: dict[str, Point] = {
        portal_id: point for portal_id, point in portals
    }
    node_points.update(
        {node_id: tuple(point) for node_id, point in network["junctions"].items()}
    )
    connector_paths = {}
    for portal_id, targets in network.get("connectors", {}).items():
        connector_paths[portal_id] = {}
        for target in targets:
            if portal_id in CENTERLINE_PORTAL_WAYPOINTS.get(zone_id, {}):
                path = [portal_points[portal_id], node_points[target]]
            else:
                path = _grid_path(
                    polygon, portal_points[portal_id], node_points[target]
                )
                path = _simplify_path(path, polygon)
            connector_paths[portal_id][target] = [
                [x, y] for x, y in path
            ]
    network["connector_paths"] = connector_paths


def _portal_zone_ids(portal_id: str) -> tuple[str, str]:
    parts = portal_id.split("_")
    if len(parts) == 3 and parts[2].isdigit():
        parts.pop()
    if len(parts) != 2:
        raise ValueError(f"Invalid portal ID: {portal_id}")
    return parts[0], parts[1]


def build_missing_corridor_networks(
    connectivity: dict[str, Any], svg_path: Path
) -> list[str]:
    svg = ET.parse(svg_path).getroot()
    svg_zones = {
        element.get("id", "")[5:]: element
        for element in svg.iter()
        if element.get("id", "").startswith("zone-")
        and element.get("data-kind") == "corridor"
    }
    portal_map: dict[str, list[tuple[str, Point]]] = {}
    for zone_id in svg_zones:
        portal_map[zone_id] = []
    for portal_id, portal in connectivity.get("portals", {}).items():
        for zone_id in _portal_zone_ids(portal_id):
            if zone_id in portal_map:
                point = portal.get("point")
                if not isinstance(point, list) or len(point) != 2:
                    raise ValueError(f"Portal has no point: {portal_id}")
                portal_map[zone_id].append(
                    (portal_id, (float(point[0]), float(point[1])))
                )

    added = []
    for zone_id, element in sorted(svg_zones.items()):
        zone = connectivity["zones"].get(zone_id)
        if zone is None:
            raise ValueError(f"SVG corridor is missing from connectivity graph: {zone_id}")
        raw_points = element.get("points", "").split()
        polygon = [
            tuple(float(value) for value in pair.split(","))
            for pair in raw_points
        ]
        centerline_portals = DIRECT_CENTERLINE_PORTAL_PAIRS.get(zone_id)
        centerline_waypoints = CENTERLINE_PORTAL_WAYPOINTS.get(zone_id, {})
        if (
            zone.get("movement_network") is None
            or centerline_portals is not None
            or centerline_waypoints
            or zone_id in MAX_CENTERLINE_SEGMENT_LENGTH
        ):
            zone["movement_network"] = build_movement_network(
                zone_id,
                polygon,
                portal_map[zone_id],
                centerline_portals,
                centerline_waypoints,
            )
            added.append(zone_id)
        add_connector_paths(
            zone_id, zone["movement_network"], polygon, portal_map[zone_id]
        )
    return added


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add centered movement networks to unmapped corridor zones"
    )
    parser.add_argument("connectivity", nargs="?", type=Path, default=DEFAULT_CONNECTIVITY)
    parser.add_argument("svg", nargs="?", type=Path, default=DEFAULT_SVG)
    args = parser.parse_args()

    connectivity = json.loads(args.connectivity.read_text(encoding="utf-8"))
    added = build_missing_corridor_networks(connectivity, args.svg)
    args.connectivity.write_text(
        json.dumps(connectivity, indent=1) + "\n", encoding="utf-8"
    )
    print(f"Updated centered movement networks for {len(added)} corridors.")
    for zone_id in added:
        print(f"  {zone_id}")


if __name__ == "__main__":
    main()
