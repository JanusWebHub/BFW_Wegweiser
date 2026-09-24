import argparse
import copy
import heapq
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "database.json"
DEFAULT_OUTPUT = ROOT / "database_with_routes.json"

State = tuple[str, str, str]


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
) -> dict[str, Any]:
    sequence: list[str] = [states[0][0]]
    for _, portal_id, zone_to in states:
        sequence.extend([portal_id, zone_to])

    segment_ids: list[str] = []
    segment_zones: list[str] = []
    distance = 0.0
    for previous, current in zip(states, states[1:]):
        traversed_zone = previous[2]
        segment = segment_index[(traversed_zone, frozenset([previous[1], current[1]]))]
        segment_ids.append(segment["id"])
        segment_zones.append(traversed_zone)
        distance += segment["distance"]

    segment_roles = [
        "access" if index == 0 or index == len(segment_ids) - 1 else "transit"
        for index in range(len(segment_ids))
    ]
    state_special_cost = sum(special_costs.get(state_key(state), 0.0) for state in states)
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
        "special_cost": round(state_special_cost, 3),
        "total_cost": round(distance + state_special_cost, 3),
    }


def shortest_route(database: dict[str, Any], start_zone: str, target_zone: str) -> dict[str, Any]:
    zones = database["zones"]
    portals = database["portals"]
    zone_index = database["indexes"]["zone_portals"]
    special_costs = database.get("special_state_costs", {})
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
                reconstruct_states(parents, current), segment_index, special_costs
            )
        if entered_zone == "aussen":
            continue

        for next_portal_id in zone_index[entered_zone]:
            if next_portal_id == current_portal_id:
                continue
            next_zone = far_zone(portals[next_portal_id], entered_zone)
            if next_zone == "aussen" and target_zone != "aussen":
                continue
            next_state = (entered_zone, next_portal_id, next_zone)
            segment = segment_index[(entered_zone, frozenset([current_portal_id, next_portal_id]))]
            next_cost = (
                current_cost
                + float(segment["distance"])
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


def calculate_all_routes(database: dict[str, Any]) -> dict[str, Any]:
    routed_database = copy.deepcopy(database)
    zone_ids = sorted(database["zones"])
    routes: dict[str, dict[str, dict[str, Any]]] = {}
    for start_zone in zone_ids:
        routes[start_zone] = {}
        for target_zone in zone_ids:
            routes[start_zone][target_zone] = shortest_route(
                database, start_zone, target_zone
            )
    routed_database["routes"] = routes
    routed_database["meta"]["route_count"] = len(zone_ids) ** 2
    routed_database["meta"]["routing_algorithm"] = "multi-source multi-target Dijkstra over directed portal states"
    return routed_database


def validate_routes(database: dict[str, Any]) -> None:
    zone_ids = set(database["zones"])
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
            if route["status"] != "ok":
                raise ValueError(f"Prototype route is unreachable: {start_zone} -> {target_zone}")
            sequence = route["sequence"]
            if not sequence or sequence[0] != start_zone or sequence[-1] != target_zone:
                raise ValueError(f"Invalid route endpoints: {start_zone} -> {target_zone}")
            if len(sequence) % 2 != 1:
                raise ValueError(f"Route does not alternate: {start_zone} -> {target_zone}")
            if len(route["segment_ids"]) != max(0, len(route["portal_chain"]) - 1):
                raise ValueError(f"Segment count mismatch: {start_zone} -> {target_zone}")
            if any(zone == "aussen" for zone in route["zone_sequence"][1:-1]):
                raise ValueError(f"Exterior used as an intermediate: {start_zone} -> {target_zone}")
            for index in range(0, len(sequence) - 2, 2):
                zone_from, portal_id, zone_to = sequence[index : index + 3]
                if set(portals[portal_id]["zones"]) != {zone_from, zone_to}:
                    raise ValueError(
                        f"Portal {portal_id} does not join {zone_from} and {zone_to}"
                    )
            expected_total = route["distance"] + route["special_cost"]
            if not math.isclose(route["total_cost"], expected_total, abs_tol=0.002):
                raise ValueError(f"Cost mismatch: {start_zone} -> {target_zone}")


def calculate_routes(input_path: Path, output_path: Path) -> Path:
    database = json.loads(input_path.read_text(encoding="utf-8"))
    routed_database = calculate_all_routes(database)
    validate_routes(routed_database)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(routed_database, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate all east-wing routes")
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = calculate_routes(args.input, args.output)
    database = json.loads(output_path.read_text(encoding="utf-8"))
    route_count = database["meta"]["route_count"]
    unreachable = sum(
        route["status"] == "unreachable"
        for targets in database["routes"].values()
        for route in targets.values()
    )
    print(f"Wrote {output_path} with {route_count} routes ({unreachable} unreachable).")


if __name__ == "__main__":
    main()