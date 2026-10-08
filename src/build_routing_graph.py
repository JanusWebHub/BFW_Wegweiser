import argparse
import heapq
import json
import math
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "web" / "eg-connectivity-graph.json"
DEFAULT_OUTPUT = ROOT / "web" / "eg-routing-graph.json"

Point = tuple[float, float]


def finite_number(value: Any, description: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{description} must be a finite number")
    try:
        number = float(value)
    except (OverflowError, ValueError) as error:
        raise ValueError(f"{description} must be a finite number") from error
    if not math.isfinite(number):
        raise ValueError(f"{description} must be a finite number")
    return number


def validate_finite_values(value: Any, path: str = "input") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"Non-finite number at {path}")
    if isinstance(value, dict):
        for key, child in value.items():
            validate_finite_values(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_finite_values(child, f"{path}[{index}]")


def portal_zones(portal_id: str, zone_ids: set[str]) -> tuple[str, str]:
    parts = portal_id.split("_")
    if len(parts) == 3 and parts[2].isdigit():
        parts.pop()
    if (
        len(parts) != 2
        or parts[0] not in zone_ids
        or parts[1] not in zone_ids
        or parts[0] >= parts[1]
    ):
        raise ValueError(f"Portal ID does not identify one sorted zone pair: {portal_id}")
    return parts[0], parts[1]


def portal_point(portal_id: str, portal: dict[str, Any], floor_id: str) -> Point:
    point = portal.get("point")
    if point is None:
        point = portal.get("points", {}).get(floor_id)
    if not isinstance(point, list) or len(point) != 2:
        raise ValueError(f"Portal has no point on floor {floor_id}: {portal_id}")
    return (
        finite_number(point[0], f"Portal {portal_id} x coordinate"),
        finite_number(point[1], f"Portal {portal_id} y coordinate"),
    )


def point_distance(first: Point, second: Point) -> float:
    distance = math.dist(first, second)
    if not math.isfinite(distance):
        raise ValueError("Geometry produces a non-finite distance")
    return distance


def _shortest_path(
    adjacency: dict[str, list[tuple[str, str]]],
    edge_points: dict[str, tuple[str, str, list[Point]]],
    start: str,
    target: str,
) -> tuple[list[Point], float]:
    distances = {start: 0.0}
    parents: dict[str, tuple[str, str]] = {}
    queue = [(0.0, start)]

    while queue:
        distance, node = heapq.heappop(queue)
        if distance != distances.get(node):
            continue
        if node == target:
            break
        for neighbor, edge_id in adjacency[node]:
            edge_start, edge_end, geometry = edge_points[edge_id]
            edge_length = sum(
                point_distance(first, second)
                for first, second in zip(geometry, geometry[1:])
            )
            candidate = distance + edge_length
            if candidate < distances.get(neighbor, math.inf):
                distances[neighbor] = candidate
                parents[neighbor] = (node, edge_id)
                heapq.heappush(queue, (candidate, neighbor))

    if target not in distances:
        raise ValueError(f"Movement network has no path between {start} and {target}")

    traversals: list[tuple[str, str, str]] = []
    node = target
    while node != start:
        previous, edge_id = parents[node]
        traversals.append((previous, node, edge_id))
        node = previous
    traversals.reverse()

    geometry: list[Point] = []
    for previous, following, edge_id in traversals:
        edge_start, edge_end, edge_geometry = edge_points[edge_id]
        oriented = edge_geometry if (previous, following) == (edge_start, edge_end) else list(reversed(edge_geometry))
        geometry.extend(oriented if not geometry else oriented[1:])

    return geometry, distances[target]


def _movement_segments(
    zone_id: str,
    zone_portals: list[str],
    portals: dict[str, dict[str, Any]],
    floor_id: str,
    movement_network: dict[str, Any],
    units_per_meter: float,
) -> list[dict[str, Any]]:
    junctions = movement_network.get("junctions", {})
    connectors = movement_network.get("connectors", {})
    connector_paths = movement_network.get("connector_paths")
    backbone = movement_network.get("backbone", [])
    if len(backbone) < 2 or len(backbone) != len(set(backbone)):
        raise ValueError(f"Invalid backbone node sequence in zone {zone_id}")

    endpoints = {backbone[0], backbone[-1]}
    if not endpoints.issubset(zone_portals):
        raise ValueError(f"Backbone endpoints must be portals in zone {zone_id}")
    if set(junctions) != set(backbone) - endpoints:
        raise ValueError(f"Backbone junction definitions do not match its node sequence in zone {zone_id}")
    expected_connectors = set(zone_portals) - endpoints
    if set(connectors) != expected_connectors:
        missing = sorted(expected_connectors - set(connectors))
        extra = sorted(set(connectors) - expected_connectors)
        raise ValueError(f"Connector coverage mismatch in {zone_id}: missing={missing}, extra={extra}")
    if connector_paths is not None:
        if not isinstance(connector_paths, dict) or set(connector_paths) != expected_connectors:
            raise ValueError(f"Connector path coverage mismatch in {zone_id}")

    if set(junctions) & set(portals):
        raise ValueError(f"Movement junction ID collides with a portal ID in zone {zone_id}")

    node_points: dict[str, Point] = {
        portal_id: portal_point(portal_id, portals[portal_id], floor_id)
        for portal_id in zone_portals
    }
    for junction_id, raw_point in junctions.items():
        if not isinstance(raw_point, list) or len(raw_point) != 2:
            raise ValueError(f"Invalid movement junction point: {junction_id}")
        point = (
            finite_number(raw_point[0], f"Movement junction {junction_id} x coordinate"),
            finite_number(raw_point[1], f"Movement junction {junction_id} y coordinate"),
        )
        node_points[junction_id] = point

    if any(node_id not in node_points for node_id in backbone):
        raise ValueError(f"Backbone references an unknown node in zone {zone_id}")

    adjacency: dict[str, list[tuple[str, str]]] = {node_id: [] for node_id in node_points}
    edge_points: dict[str, tuple[str, str, list[Point]]] = {}

    def add_edge(
        edge_id: str,
        first: str,
        second: str,
        geometry: list[Point] | None = None,
    ) -> None:
        if first == second or first not in node_points or second not in node_points:
            raise ValueError(f"Invalid movement edge {edge_id} in zone {zone_id}")
        if geometry is None:
            geometry = [node_points[first], node_points[second]]
        if len(geometry) < 2:
            raise ValueError(f"Movement edge has invalid geometry: {edge_id}")
        if (
            point_distance(geometry[0], node_points[first]) > 0.001
            or point_distance(geometry[-1], node_points[second]) > 0.001
        ):
            raise ValueError(f"Movement edge geometry endpoints do not match: {edge_id}")
        if sum(
            point_distance(start, end)
            for start, end in zip(geometry, geometry[1:])
        ) <= 0:
            raise ValueError(f"Movement edge has zero length: {edge_id}")
        edge_points[edge_id] = (first, second, geometry)
        adjacency[first].append((second, edge_id))
        adjacency[second].append((first, edge_id))

    for index, (first, second) in enumerate(zip(backbone, backbone[1:])):
        add_edge(f"backbone:{index}", first, second)

    for portal_id in sorted(connectors):
        targets = connectors[portal_id]
        if not isinstance(targets, list) or len(targets) != 2 or targets[0] == targets[1]:
            raise ValueError(f"Portal connector must name two distinct backbone nodes: {portal_id}")
        if any(node_id not in backbone for node_id in targets):
            raise ValueError(f"Portal connector references a node outside the backbone: {portal_id}")
        portal_paths = None
        if connector_paths is not None:
            portal_paths = connector_paths[portal_id]
            if not isinstance(portal_paths, dict) or set(portal_paths) != set(targets):
                raise ValueError(f"Connector target coverage mismatch: {portal_id}")
        for direction, target_node in enumerate(targets):
            geometry = None
            if portal_paths is not None:
                raw_geometry = portal_paths[target_node]
                if not isinstance(raw_geometry, list) or len(raw_geometry) < 2:
                    raise ValueError(f"Invalid connector path: {portal_id}")
                geometry = [
                    (
                        finite_number(point[0], f"Connector {portal_id} x coordinate"),
                        finite_number(point[1], f"Connector {portal_id} y coordinate"),
                    )
                    for point in raw_geometry
                    if isinstance(point, list) and len(point) == 2
                ]
                if len(geometry) != len(raw_geometry):
                    raise ValueError(f"Invalid connector path point: {portal_id}")
            add_edge(
                f"connector:{portal_id}:{direction}",
                portal_id,
                target_node,
                geometry,
            )

    for neighbors in adjacency.values():
        neighbors.sort()

    segments = []
    for first_portal, second_portal in combinations(sorted(zone_portals), 2):
        geometry, length = _shortest_path(
            adjacency, edge_points, first_portal, second_portal
        )
        segments.append(
            {
                "portals": [first_portal, second_portal],
                "geometry": [[x, y] for x, y in geometry],
                "distance_m": round(length / units_per_meter, 2),
            }
        )
    return segments


def compile_routing_graph(connectivity_graph: dict[str, Any]) -> dict[str, Any]:
    if connectivity_graph.get("format") != "wegweiser-connectivity-graph":
        raise ValueError("Input is not a Wegweiser connectivity graph")
    validate_finite_values(connectivity_graph)

    zones = connectivity_graph.get("zones", {})
    portals = connectivity_graph.get("portals", {})
    zone_ids = set(zones)
    floors = connectivity_graph.get("floors", {})
    portals_by_zone = {zone_id: [] for zone_id in zones}

    for portal_id, portal in portals.items():
        first_zone, second_zone = portal_zones(portal_id, zone_ids)
        portals_by_zone[first_zone].append(portal_id)
        portals_by_zone[second_zone].append(portal_id)
        if "virtual" not in portal:
            raise ValueError(f"Portal is missing its virtual flag: {portal_id}")
        for zone_id in (first_zone, second_zone):
            if zone_id == "exterior":
                continue
            floor_id = zones[zone_id].get("floor")
            if floor_id not in floors:
                raise ValueError(f"Portal touches a zone with no valid floor: {portal_id}")
            portal_point(portal_id, portal, floor_id)

    segments: dict[str, list[dict[str, Any]]] = {}
    for zone_id, zone in zones.items():
        movement_network = zone.get("movement_network")
        if movement_network is not None:
            if zone_id == "exterior":
                raise ValueError("The exterior zone cannot have a movement network")
            if not zone.get("crossable", False):
                raise ValueError(f"Movement network requires a crossable zone: {zone_id}")
            if len(portals_by_zone[zone_id]) < 2:
                raise ValueError(f"Movement network requires at least two portals: {zone_id}")
        if zone_id == "exterior":
            continue
        zone_portals = sorted(portals_by_zone[zone_id])
        if not zone_portals:
            continue
        segments[zone_id] = []
        if not zone.get("crossable", False) or len(zone_portals) < 2:
            continue
        floor_id = zone.get("floor")
        if floor_id not in floors:
            raise ValueError(f"Crossable zone has no valid floor: {zone_id}")
        units_per_meter = finite_number(
            floors[floor_id].get("units_per_meter"),
            f"units_per_meter for floor {floor_id}",
        )
        if units_per_meter <= 0:
            raise ValueError(f"Invalid units_per_meter for floor {floor_id}")

        if movement_network is not None:
            segments[zone_id] = _movement_segments(
                zone_id,
                zone_portals,
                portals,
                floor_id,
                movement_network,
                units_per_meter,
            )
            continue

        zone_segments = []
        for first_portal, second_portal in combinations(zone_portals, 2):
            first_point = portal_point(first_portal, portals[first_portal], floor_id)
            second_point = portal_point(second_portal, portals[second_portal], floor_id)
            zone_segments.append(
                {
                    "portals": [first_portal, second_portal],
                    "geometry": [list(first_point), list(second_point)],
                    "distance_m": round(
                        point_distance(first_point, second_point) / units_per_meter,
                        2,
                    ),
                }
            )
        segments[zone_id] = zone_segments

    return {
        "format": "wegweiser-routing-graph",
        "version": connectivity_graph["version"],
        "provenance": connectivity_graph.get("provenance", "unverified"),
        "floors": floors,
        "zones": zones,
        "portals": portals,
        "segments": segments,
        "state_costs": connectivity_graph.get("state_costs", {}),
        "segment_costs": connectivity_graph.get("segment_costs", {}),
        "variants": connectivity_graph.get("variants", {"standard": []}),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a routing graph from connectivity data")
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    connectivity_graph = json.loads(args.input.read_text(encoding="utf-8"))
    routing_graph = compile_routing_graph(connectivity_graph)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(routing_graph, ensure_ascii=False, indent=1, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote routing graph to {args.output}.")


if __name__ == "__main__":
    main()