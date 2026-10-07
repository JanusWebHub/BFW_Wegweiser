import argparse
import copy
import heapq
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "claude" / "review" / "data" / "routing-graph-fixed.json"
DEFAULT_OUTPUT = ROOT / "web" / "eg-routes.json"

State = tuple[str, str, str]
EXTERIOR_ZONE_IDS = {"aussen", "exterior"}


def portal_zones(portal_id: str, zone_ids: list[str]) -> list[str]:
    parts = portal_id.split("_")
    if len(parts) == 3 and parts[2].isdigit():
        parts.pop()
    if (
        len(parts) != 2
        or parts[0] not in zone_ids
        or parts[1] not in zone_ids
        or parts[0] >= parts[1]
    ):
        raise ValueError(f"Portal id does not identify exactly one zone pair: {portal_id}")
    return parts


def normalize_routing_graph(graph: dict[str, Any]) -> dict[str, Any]:
    if graph.get("format") != "wegweiser-routing-graph":
        raise ValueError("Input is not a Wegweiser routing graph")

    source_zones = graph["zones"]
    zone_ids = sorted(source_zones)
    source_portals = graph["portals"]
    portals = {
        portal_id: {"id": portal_id, **portal, "zones": portal_zones(portal_id, zone_ids)}
        for portal_id, portal in source_portals.items()
        if not portal.get("emergency_exit") or portal.get("main_entrance")
    }
    zone_portals = {zone_id: [] for zone_id in zone_ids}
    for portal_id, portal in portals.items():
        for zone_id in portal["zones"]:
            zone_portals[zone_id].append(portal_id)

    zones = {
        zone_id: {
            "id": zone_id,
            "label": zone_id,
            "floor": source_zone.get("floor"),
            "crossable": bool(source_zone.get("crossable", False)),
            "navigable": bool(zone_portals[zone_id]),
        }
        for zone_id, source_zone in source_zones.items()
    }

    segments: dict[str, dict[str, Any]] = {}
    for zone_id, zone_segments in graph["segments"].items():
        if zone_id not in zones:
            raise ValueError(f"Segments reference unknown zone: {zone_id}")
        for index, source_segment in enumerate(zone_segments):
            segment_portals = source_segment["portals"]
            if len(segment_portals) != 2 or any(portal_id not in source_portals for portal_id in segment_portals):
                raise ValueError(f"Invalid segment portal pair in zone {zone_id}")
            if any(
                zone_id not in portal_zones(portal_id, zone_ids)
                for portal_id in segment_portals
            ):
                raise ValueError(f"Segment portal does not touch zone {zone_id}")
            if any(portal_id not in portals for portal_id in segment_portals):
                continue
            segment_id = f"segment:{zone_id}:{index}"
            segments[segment_id] = {
                "id": segment_id,
                "zone_id": zone_id,
                "portals": segment_portals,
                "geometry": source_segment["geometry"],
                "distance": float(source_segment["distance_m"]),
            }

    return {
        "meta": {
            "schema_version": graph["version"],
            "model": "Wegweiser",
            "floor": "EG",
            "svg_path": graph["floors"]["E"]["svg"],
            "provenance": graph["provenance"],
        },
        "format": graph["format"],
        "floors": graph["floors"],
        "zones": zones,
        "portals": portals,
        "segments": segments,
        "indexes": {"zone_portals": zone_portals},
        "special_state_costs": graph.get("state_costs", {}),
        "segment_costs": graph.get("segment_costs", {}),
        "variants": graph.get("variants", {"standard": []}),
    }


def state_key(state: State) -> str:
    return "|".join(state)


def far_zone(portal: dict[str, Any], near_zone: str) -> str:
    zone_a, zone_b = portal["zones"]
    if near_zone == zone_a:
        return zone_b
    if near_zone == zone_b:
        return zone_a
    raise ValueError(f"Portal {portal['id']} does not touch zone {near_zone}")


def make_segment_index(segments: dict[str, dict[str, Any]]) -> dict[tuple[str, frozenset[str]], dict[str, Any]]:
    return {
        (segment["zone_id"], frozenset(segment["portals"])): segment
        for segment in segments.values()
    }


def reconstruct_states(parents: dict[State, State | None], target_state: State) -> list[State]:
    states: list[State] = []
    current: State | None = target_state
    while current is not None:
        states.append(current)
        current = parents[current]
    states.reverse()
    return states


def route_from_states(
    states: list[State],
    segment_index: dict[tuple[str, frozenset[str]], dict[str, Any]],
    special_costs: dict[str, float],
    segment_costs: dict[str, float],
) -> dict[str, Any]:
    sequence: list[str] = [states[0][0]]
    for _, portal_id, zone_to in states:
        sequence.extend([portal_id, zone_to])

    segment_ids: list[str] = []
    segment_zones: list[str] = []
    distance = 0.0
    segment_special_cost = 0.0
    for previous, current in zip(states, states[1:]):
        traversed_zone = previous[2]
        segment = segment_index[(traversed_zone, frozenset([previous[1], current[1]]))]
        segment_ids.append(segment["id"])
        segment_zones.append(traversed_zone)
        distance += segment["distance"]
        segment_special_cost += float(
            segment_costs.get(f"{previous[1]}|{traversed_zone}|{current[1]}", 0.0)
        )

    segment_roles = [
        "access" if index == 0 or index == len(segment_ids) - 1 else "transit"
        for index in range(len(segment_ids))
    ]
    state_special_cost = sum(float(special_costs.get(state_key(state), 0.0)) for state in states)
    special_cost = state_special_cost + segment_special_cost
    return {
        "status": "ok",
        "sequence": sequence,
        "portal_chain": [state[1] for state in states],
        "zone_sequence": sequence[::2],
        "state_chain": [
            {"zone_from": zone_from, "portal_id": portal_id, "zone_to": zone_to}
            for zone_from, portal_id, zone_to in states
        ],
        "segment_ids": segment_ids,
        "segment_zones": segment_zones,
        "segment_roles": segment_roles,
        "distance": round(distance, 3),
        "special_cost": round(special_cost, 3),
        "total_cost": round(distance + special_cost, 3),
    }


def shortest_route(
    database: dict[str, Any],
    start_zone: str,
    target_zone: str,
    variant: str = "standard",
) -> dict[str, Any]:
    zones = database["zones"]
    portals = database["portals"]
    zone_index = database["indexes"]["zone_portals"]
    special_costs = database.get("special_state_costs", {})
    segment_costs = database.get("segment_costs", {})
    variants = database.get("variants", {})
    if variants and variant not in variants:
        raise ValueError(f"Unknown routing variant: {variant}")
    additionally_non_crossable = set(variants.get(variant, []))
    segment_index = make_segment_index(database["segments"])

    if start_zone not in zones or target_zone not in zones:
        raise KeyError(f"Unknown route endpoint: {start_zone} -> {target_zone}")
    if start_zone == target_zone:
        return {
            "status": "ok",
            "sequence": [start_zone],
            "portal_chain": [],
            "zone_sequence": [start_zone],
            "state_chain": [],
            "segment_ids": [],
            "segment_zones": [],
            "segment_roles": [],
            "distance": 0.0,
            "special_cost": 0.0,
            "total_cost": 0.0,
        }

    distances: dict[State, float] = {}
    parents: dict[State, State | None] = {}
    queue: list[tuple[float, State]] = []

    for portal_id in zone_index[start_zone]:
        state = (start_zone, portal_id, far_zone(portals[portal_id], start_zone))
        initial_cost = float(special_costs.get(state_key(state), 0.0))
        if initial_cost < distances.get(state, math_inf()):
            distances[state] = initial_cost
            parents[state] = None
            heapq.heappush(queue, (initial_cost, state))

    while queue:
        current_cost, current = heapq.heappop(queue)
        if current_cost != distances.get(current):
            continue

        _, current_portal_id, entered_zone = current
        if entered_zone == target_zone:
            return route_from_states(
                reconstruct_states(parents, current), segment_index, special_costs, segment_costs
            )
        if (
            entered_zone in EXTERIOR_ZONE_IDS
            or not zones[entered_zone].get("crossable", True)
            or entered_zone in additionally_non_crossable
        ):
            continue

        for next_portal_id in zone_index[entered_zone]:
            if next_portal_id == current_portal_id:
                continue
            next_zone = far_zone(portals[next_portal_id], entered_zone)
            if next_zone in EXTERIOR_ZONE_IDS and target_zone != next_zone:
                continue
            next_state = (entered_zone, next_portal_id, next_zone)
            segment = segment_index.get(
                (entered_zone, frozenset([current_portal_id, next_portal_id]))
            )
            if segment is None:
                continue
            next_cost = (
                current_cost
                + float(segment["distance"])
                + float(segment_costs.get(f"{current_portal_id}|{entered_zone}|{next_portal_id}", 0.0))
                + float(special_costs.get(state_key(next_state), 0.0))
            )
            if next_cost < distances.get(next_state, math_inf()):
                distances[next_state] = next_cost
                parents[next_state] = current
                heapq.heappush(queue, (next_cost, next_state))

    return {
        "status": "unreachable",
        "sequence": [],
        "portal_chain": [],
        "zone_sequence": [],
        "state_chain": [],
        "segment_ids": [],
        "segment_zones": [],
        "segment_roles": [],
        "distance": None,
        "special_cost": None,
        "total_cost": None,
    }


def math_inf() -> float:
    return float("inf")


def calculate_all_routes(database: dict[str, Any], variant: str = "standard") -> dict[str, Any]:
    routed_database = copy.deepcopy(database)
    zone_ids = sorted(
        zone_id
        for zone_id, zone in database["zones"].items()
        if zone.get("navigable", True)
    )
    routes: dict[str, dict[str, dict[str, Any]]] = {}
    for start_zone in zone_ids:
        routes[start_zone] = {}
        for target_zone in zone_ids:
            routes[start_zone][target_zone] = shortest_route(
                database, start_zone, target_zone, variant
            )
    routed_database["routes"] = routes
    routed_database["meta"]["route_count"] = sum(map(len, routes.values()))
    routed_database["meta"]["variant"] = variant
    routed_database["meta"]["routing_algorithm"] = "multi-source multi-target Dijkstra over directed portal states"
    return routed_database


def validate_routes(database: dict[str, Any]) -> None:
    zone_ids = set(database["routes"])
    portals = database["portals"]
    expected_route_count = len(zone_ids) ** 2
    actual_route_count = sum(len(targets) for targets in database["routes"].values())
    if actual_route_count != expected_route_count:
        raise ValueError(
            f"Expected {expected_route_count} ordered routes, found {actual_route_count}"
        )

    for start_zone, targets in database["routes"].items():
        if set(targets) != zone_ids:
            raise ValueError(f"Route targets are incomplete for {start_zone}")
        for target_zone, route in targets.items():
            if route["status"] == "unreachable":
                continue
            if route["status"] != "ok":
                raise ValueError(f"Invalid route status: {start_zone} -> {target_zone}")
            sequence = route["sequence"]
            if not sequence or sequence[0] != start_zone or sequence[-1] != target_zone:
                raise ValueError(f"Invalid route endpoints: {start_zone} -> {target_zone}")
            if len(sequence) % 2 != 1:
                raise ValueError(f"Route does not alternate: {start_zone} -> {target_zone}")
            if len(route["segment_ids"]) != max(0, len(route["portal_chain"]) - 1):
                raise ValueError(f"Segment count mismatch: {start_zone} -> {target_zone}")
            if any(
                zone in EXTERIOR_ZONE_IDS or not database["zones"][zone].get("crossable", True)
                for zone in route["zone_sequence"][1:-1]
            ):
                raise ValueError(f"Non-crossable zone used as an intermediate: {start_zone} -> {target_zone}")
            for index in range(0, len(sequence) - 2, 2):
                zone_from, portal_id, zone_to = sequence[index : index + 3]
                if set(portals[portal_id]["zones"]) != {zone_from, zone_to}:
                    raise ValueError(
                        f"Portal {portal_id} does not join {zone_from} and {zone_to}"
                    )
            expected_total = route["distance"] + route["special_cost"]
            if not math.isclose(route["total_cost"], expected_total, abs_tol=0.002):
                raise ValueError(f"Cost mismatch: {start_zone} -> {target_zone}")


def compact_route_table(database: dict[str, Any]) -> dict[str, Any]:
    zone_ids = sorted(database["routes"])
    portal_ids = sorted(database["portals"])
    portal_indexes = {portal_id: index for index, portal_id in enumerate(portal_ids)}
    return {
        "format": "wegweiser-route-table",
        "version": 1,
        "provenance": database["meta"].get("provenance", "unverified"),
        "variant": database["meta"].get("variant", "standard"),
        "zones": zone_ids,
        "portals": portal_ids,
        "routes": [
            [
                None
                if database["routes"][start_zone][target_zone]["status"] == "unreachable"
                else [
                    portal_indexes[portal_id]
                    for portal_id in database["routes"][start_zone][target_zone]["portal_chain"]
                ]
                for target_zone in zone_ids
            ]
            for start_zone in zone_ids
        ],
    }


def calculate_routes(input_path: Path, output_path: Path, variant: str = "standard") -> Path:
    source = json.loads(input_path.read_text(encoding="utf-8"))
    is_routing_graph = source.get("format") == "wegweiser-routing-graph"
    database = normalize_routing_graph(source) if is_routing_graph else source
    routed_database = calculate_all_routes(database, variant)
    validate_routes(routed_database)
    output_data = compact_route_table(routed_database) if is_routing_graph else routed_database
    output_path.parent.mkdir(parents=True, exist_ok=True)
    serialization_options = {"separators": (",", ":")} if is_routing_graph else {"indent": 2}
    output_path.write_text(
        json.dumps(output_data, ensure_ascii=False, **serialization_options) + "\n",
        encoding="utf-8",
    )
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate routes from a Wegweiser routing graph")
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--variant", default="standard")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = calculate_routes(args.input, args.output, args.variant)
    database = json.loads(output_path.read_text(encoding="utf-8"))
    if database.get("format") == "wegweiser-route-table":
        route_count = len(database["zones"]) ** 2
        unreachable = sum(path is None for row in database["routes"] for path in row)
    else:
        route_count = database["meta"]["route_count"]
        unreachable = sum(
            route["status"] == "unreachable"
            for targets in database["routes"].values()
            for route in targets.values()
        )
    print(f"Wrote {output_path} with {route_count} routes ({unreachable} unreachable).")


if __name__ == "__main__":
    main()