import argparse
import json
import math
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "database.json"
SVG_PATH = "web/assets/bfw-eg-ost.svg"


ROOMS: dict[str, dict[str, Any]] = {
    "circulation": {"label": "Flur und Atrium", "zone_ids": ["flur_west", "atrium", "flur_ost", "anschluss"]},
    "E.61": {"label": "Werkstatt", "zone_ids": ["E.61"]},
    "E.59b": {"label": "Büro", "zone_ids": ["E.59b"]},
    "E.59a": {"label": "Büro", "zone_ids": ["E.59a"]},
    "E.59": {"label": "Besprechungsraum", "zone_ids": ["E.59"]},
    "elt": {"label": "Elektroverteilung", "zone_ids": ["elt"]},
    "E.52": {"label": "Eingangsbereich / Rezeption", "zone_ids": ["E.52"]},
    "wachdienst": {"label": "Wachdienst", "zone_ids": ["wachdienst"]},
    "E.63": {"label": "Unterricht", "zone_ids": ["E.63"]},
    "E.62": {"label": "Unterricht", "zone_ids": ["E.62"]},
    "vr_h": {"label": "Vorraum WC Herren", "zone_ids": ["vr_h"]},
    "vr_d": {"label": "Vorraum WC Damen", "zone_ids": ["vr_d"]},
    "E.54b": {"label": "WC Herren", "zone_ids": ["E.54b"]},
    "E.54a": {"label": "WC Damen", "zone_ids": ["E.54a"]},
    "E.58a": {"label": "Technik", "zone_ids": ["E.58a"]},
    "TR9": {"label": "Treppenhaus", "zone_ids": ["TR9"]},
    "R.58": {"label": "Konferenzraum", "zone_ids": ["R.58"]},
    "E.57": {"label": "Unterricht", "zone_ids": ["E.57"]},
    "E.56c": {"label": "Unterricht", "zone_ids": ["E.56c"]},
    "E.56b": {"label": "Unbekannt", "zone_ids": ["E.56b"]},
    "aussen": {"label": "Außenbereich", "zone_ids": ["aussen"]},
}


ZONE_ROWS = [
    ("aussen", "exterior", "Außenbereich", None),
    ("E.61", "room", "Werkstatt", [370, 95]),
    ("E.59b", "room", "Büro", [550, 90]),
    ("E.59a", "room", "Büro", [700, 90]),
    ("E.59", "room", "Besprechungsraum", [860, 90]),
    ("elt", "service", "Elektroverteilung", [947, 205]),
    ("E.52", "hall", "Eingangsbereich / Rezeption", [1160, 185]),
    ("wachdienst", "room", "Wachdienst", [1360, 170]),
    ("E.63", "room", "Unterricht", [220, 285]),
    ("E.62", "room", "Unterricht", [400, 285]),
    ("flur_west", "corridor", "Flur West", [560, 205]),
    ("atrium", "hall", "Flur Mitte / Atrium", [820, 285]),
    ("flur_ost", "corridor", "Flur Ost", [1160, 288]),
    ("vr_h", "service", "Vorraum WC Herren", [500, 255]),
    ("vr_d", "service", "Vorraum WC Damen", [600, 255]),
    ("E.54b", "service", "WC Herren", [495, 305]),
    ("E.54a", "service", "WC Damen", [600, 305]),
    ("E.58a", "service", "Technik", [582, 430]),
    ("TR9", "stairs", "Treppenhaus", [650, 330]),
    ("R.58", "room", "Konferenzraum", [700, 470]),
    ("E.57", "room", "Unterricht", [1050, 420]),
    ("E.56c", "room", "Unterricht", [1290, 410]),
    ("E.56b", "room", "Unbekannt", [1370, 390]),
    ("anschluss", "corridor", "Anschluss übriges Erdgeschoss", [1460, 288]),
]


PORTAL_ROWS = [
    ("p01", "E.63", "flur_west", 354, 211, False),
    ("p02", "E.61", "flur_west", 440, 170, False),
    ("p03", "E.59b", "flur_west", 533, 170, False),
    ("p04", "E.62", "flur_west", 453, 234, False),
    ("p05", "vr_h", "flur_west", 500, 234, False),
    ("p06", "vr_d", "flur_west", 600, 234, False),
    ("p07", "TR9", "flur_west", 625, 234, False),
    ("p08", "flur_west", "atrium", 677, 202, True),
    ("p09", "E.59a", "atrium", 688, 170, False),
    ("p11", "E.59", "atrium", 855, 170, False),
    ("p13", "R.58", "atrium", 828, 396, False),
    ("p14", "elt", "atrium", 947, 240, False),
    ("p15", "atrium", "flur_ost", 936, 288, True),
    ("p16", "E.52", "flur_ost", 1107, 240, False),
    ("p18", "E.57", "flur_ost", 1096, 336, False),
    ("p19", "E.56c", "flur_ost", 1277, 336, False),
    ("p20", "E.56b", "flur_ost", 1373, 336, False),
    ("p21", "flur_ost", "anschluss", 1424, 288, True),
    ("p22", "wachdienst", "E.52", 1381, 196, False),
    ("p24", "vr_h", "E.54b", 495, 278, False),
    ("p25", "vr_d", "E.54a", 600, 278, False),
    ("p26", "E.58a", "R.58", 582, 396, False),
    ("p23", "aussen", "E.52", 1206, 0, False),
    ("p27", "aussen", "E.61", 435, 0, False),
    ("p28", "aussen", "E.63", 120, 186, False),
]


WALL_ROWS = [
    ("w01", "E.61", "circulation", "p02"),
    ("w02", "E.59b", "circulation", "p03"),
    ("w03", "E.59a", "circulation", "p09"),
    ("w04", "E.59", "circulation", "p11"),
    ("w05", "elt", "circulation", "p14"),
    ("w06", "E.52", "circulation", "p16"),
    ("w07", "wachdienst", "E.52", "p22"),
    ("w08", "E.63", "circulation", "p01"),
    ("w09", "E.62", "circulation", "p04"),
    ("w10", "vr_h", "circulation", "p05"),
    ("w11", "vr_d", "circulation", "p06"),
    ("w12", "TR9", "circulation", "p07"),
    ("w13", "R.58", "circulation", "p13"),
    ("w14", "E.57", "circulation", "p18"),
    ("w15", "E.56c", "circulation", "p19"),
    ("w16", "E.56b", "circulation", "p20"),
    ("w17", "vr_h", "E.54b", "p24"),
    ("w18", "vr_d", "E.54a", "p25"),
    ("w19", "E.58a", "R.58", "p26"),
    ("w20", "E.61", "E.59b", None),
    ("w21", "E.59b", "E.59a", None),
    ("w22", "E.59a", "E.59", None),
    ("w23", "E.57", "E.56c", None),
    ("w24", "E.56c", "E.56b", None),
    ("w25", "aussen", "E.52", "p23"),
    ("w26", "aussen", "E.61", "p27"),
    ("w27", "aussen", "E.63", "p28"),
]


SPECIAL_STATE_COSTS = {
    "flur_west|p07|TR9": 12.0,
    "TR9|p07|flur_west": 12.0,
}


def make_zones() -> dict[str, dict[str, Any]]:
    return {
        zone_id: {
            "id": zone_id,
            "kind": kind,
            "label": label,
            "svg_id": f"zone-{zone_id}",
            "movement_center": center,
        }
        for zone_id, kind, label, center in ZONE_ROWS
    }


def make_portals() -> dict[str, dict[str, Any]]:
    return {
        portal_id: {
            "id": portal_id,
            "zones": [zone_a, zone_b],
            "point": [x, y],
            "virtual": virtual,
            "svg_id": f"portal-{portal_id}",
        }
        for portal_id, zone_a, zone_b, x, y, virtual in PORTAL_ROWS
    }


def make_walls() -> dict[str, dict[str, Any]]:
    return {
        wall_id: {
            "id": wall_id,
            "rooms": [room_a, room_b],
            "portal_id": portal_id,
        }
        for wall_id, room_a, room_b, portal_id in WALL_ROWS
    }


def distance(point_a: list[float], point_b: list[float]) -> float:
    return math.hypot(point_b[0] - point_a[0], point_b[1] - point_a[1])


def derive_zone_index(
    zones: dict[str, dict[str, Any]], portals: dict[str, dict[str, Any]]
) -> dict[str, list[str]]:
    zone_index = {zone_id: [] for zone_id in zones}
    for portal_id, portal in portals.items():
        for zone_id in portal["zones"]:
            zone_index[zone_id].append(portal_id)
    return {zone_id: sorted(portal_ids) for zone_id, portal_ids in zone_index.items()}


def segment_geometry(
    zone: dict[str, Any], portal_a: dict[str, Any], portal_b: dict[str, Any]
) -> list[list[float]]:
    point_a = portal_a["point"]
    point_b = portal_b["point"]
    center = zone["movement_center"]
    if center is None or zone["kind"] in {"room", "service", "stairs"}:
        return [point_a, point_b]
    if point_a == center or point_b == center:
        return [point_a, point_b]
    return [point_a, center, point_b]


def derive_segments(
    zones: dict[str, dict[str, Any]],
    portals: dict[str, dict[str, Any]],
    zone_index: dict[str, list[str]],
) -> dict[str, dict[str, Any]]:
    segments: dict[str, dict[str, Any]] = {}
    for zone_id, portal_ids in zone_index.items():
        if zones[zone_id]["kind"] == "exterior":
            continue
        for portal_a_id, portal_b_id in combinations(portal_ids, 2):
            geometry = segment_geometry(
                zones[zone_id], portals[portal_a_id], portals[portal_b_id]
            )
            length = sum(distance(a, b) for a, b in zip(geometry, geometry[1:]))
            segment_id = f"segment:{zone_id}:{portal_a_id}:{portal_b_id}"
            segments[segment_id] = {
                "id": segment_id,
                "zone_id": zone_id,
                "portals": [portal_a_id, portal_b_id],
                "distance": round(length, 3),
                "geometry": geometry,
            }
    return segments


def validate_source(
    rooms: dict[str, dict[str, Any]],
    zones: dict[str, dict[str, Any]],
    portals: dict[str, dict[str, Any]],
    walls: dict[str, dict[str, Any]],
    zone_index: dict[str, list[str]],
) -> None:
    mapped_zones = [zone_id for room in rooms.values() for zone_id in room["zone_ids"]]
    if set(mapped_zones) != set(zones) or len(mapped_zones) != len(set(mapped_zones)):
        raise ValueError("Every zone must map to exactly one architectural room")

    for portal_id, portal in portals.items():
        portal_zones = portal["zones"]
        if len(portal_zones) != 2 or len(set(portal_zones)) != 2:
            raise ValueError(f"Portal {portal_id} must join exactly two distinct zones")
        missing = set(portal_zones) - set(zones)
        if missing:
            raise ValueError(f"Portal {portal_id} references missing zones: {missing}")

    empty_zones = [zone_id for zone_id, portal_ids in zone_index.items() if not portal_ids]
    if empty_zones:
        raise ValueError(f"Every zone must have a portal: {empty_zones}")

    for wall_id, wall in walls.items():
        if len(wall["rooms"]) != 2 or len(set(wall["rooms"])) != 2:
            raise ValueError(f"Wall {wall_id} must separate two distinct rooms")
        if not set(wall["rooms"]).issubset(rooms):
            raise ValueError(f"Wall {wall_id} references an unknown room")
        if wall["portal_id"] is not None and wall["portal_id"] not in portals:
            raise ValueError(f"Wall {wall_id} references an unknown portal")


def build_database() -> dict[str, Any]:
    rooms = {
        room_id: {"id": room_id, **room}
        for room_id, room in ROOMS.items()
    }
    zones = make_zones()
    portals = make_portals()
    walls = make_walls()
    zone_index = derive_zone_index(zones, portals)
    validate_source(rooms, zones, portals, walls, zone_index)
    segments = derive_segments(zones, portals, zone_index)

    connectivity_edges = {
        f"boundary:{portal_id}": {
            "id": f"boundary:{portal_id}",
            "zones": portal["zones"],
            "portal_id": portal_id,
        }
        for portal_id, portal in portals.items()
    }
    routing_edges = {
        segment_id: {
            "id": segment_id,
            "portals": segment["portals"],
            "zone_id": segment["zone_id"],
            "distance": segment["distance"],
        }
        for segment_id, segment in segments.items()
    }

    return {
        "meta": {
            "schema_version": 1,
            "model": "Wegweiser",
            "floor": "EG Ost",
            "coordinate_system": {"view_box": [0, 0, 1580, 900], "unit": "svg-unit"},
            "svg_path": SVG_PATH,
            "rulebook": "docs/rulebook_sorted.md",
            "cost_formula": "segment.distance + destination_state.special_cost",
        },
        "rooms": rooms,
        "zones": zones,
        "portals": portals,
        "segments": segments,
        "special_state_costs": SPECIAL_STATE_COSTS,
        "indexes": {"zone_portals": zone_index},
        "graphs": {
            "adjacency": {"nodes": sorted(rooms), "edges": walls},
            "connectivity": {"nodes": sorted(zones), "edges": connectivity_edges},
            "routing": {"nodes": sorted(portals), "edges": routing_edges},
        },
    }


def write_database(output_path: Path) -> Path:
    database = build_database()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(database, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Wegweiser east-wing database")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    output_path = write_database(parse_args().output)
    database = json.loads(output_path.read_text(encoding="utf-8"))
    print(
        f"Wrote {output_path} with "
        f"{len(database['rooms'])} rooms, {len(database['zones'])} zones, "
        f"{len(database['portals'])} portals, and {len(database['segments'])} segments."
    )


if __name__ == "__main__":
    main()