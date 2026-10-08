import copy
import json
import math
from pathlib import Path
import unittest

from build_routing_graph import compile_routing_graph
from calculate_routes import normalize_routing_graph, shortest_route


class RoutingGraphBuilderTests(unittest.TestCase):
    def setUp(self):
        self.connectivity = {
            "format": "wegweiser-connectivity-graph",
            "version": 1,
            "provenance": "unverified",
            "floors": {"E": {"svg": "floor.svg", "units_per_meter": 2}},
            "zones": {
                "A": {"floor": "E", "crossable": False},
                "B": {"floor": "E", "crossable": False},
                "C": {"floor": "E", "crossable": False},
                "D": {"floor": "E", "crossable": False},
                "H": {"floor": "E", "crossable": True},
                "J": {"floor": "E", "crossable": True},
                "K": {"floor": "E", "crossable": False},
                "L": {"floor": "E", "crossable": False},
            },
            "portals": {
                "A_H": {"virtual": False, "point": [0, 0]},
                "B_H": {"virtual": False, "point": [8, 4]},
                "C_H": {"virtual": False, "point": [12, 4]},
                "D_H": {"virtual": False, "point": [20, 0]},
                "J_K": {"virtual": False, "point": [0, 0]},
                "J_L": {"virtual": False, "point": [3, 4]},
            },
        }
        self.connectivity["zones"]["H"]["movement_network"] = {
            "backbone": ["A_H", "j-b-left", "j-between", "j-c-right", "D_H"],
            "junctions": {
                "j-b-left": [6, 0],
                "j-between": [10, 0],
                "j-c-right": [14, 0],
            },
            "connectors": {
                "B_H": ["j-b-left", "j-between"],
                "C_H": ["j-between", "j-c-right"],
            },
        }

    def test_compiles_authored_fishbone_path_and_uses_its_distance_for_routing(self):
        routing_graph = compile_routing_graph(self.connectivity)
        hall_segments = routing_graph["segments"]["H"]
        self.assertEqual(len(hall_segments), 6)
        segment = next(
            item for item in hall_segments if item["portals"] == ["B_H", "C_H"]
        )
        self.assertEqual(segment["geometry"], [[8.0, 4.0], [10.0, 0.0], [12.0, 4.0]])
        self.assertEqual(segment["distance_m"], 4.47)

        graph = normalize_routing_graph(routing_graph)
        forward = shortest_route(graph, "B", "C")
        reverse = shortest_route(graph, "C", "B")
        self.assertEqual(forward["distance"], 4.47)
        self.assertAlmostEqual(reverse["distance"], forward["distance"], places=3)
        self.assertEqual(forward["portal_chain"], ["B_H", "C_H"])
        self.assertEqual(reverse["portal_chain"], ["C_H", "B_H"])

    def test_compiles_curved_portal_connector_geometry(self):
        connectivity = copy.deepcopy(self.connectivity)
        network = connectivity["zones"]["H"]["movement_network"]
        network["connector_paths"] = {
            "B_H": {
                "j-b-left": [[8, 4], [7, 1], [6, 0]],
                "j-between": [[8, 4], [9, 1], [10, 0]],
            },
            "C_H": {
                "j-between": [[12, 4], [11, 1], [10, 0]],
                "j-c-right": [[12, 4], [13, 1], [14, 0]],
            },
        }

        routing_graph = compile_routing_graph(connectivity)
        segment = next(
            item
            for item in routing_graph["segments"]["H"]
            if item["portals"] == ["B_H", "C_H"]
        )
        self.assertEqual(
            segment["geometry"],
            [[8.0, 4.0], [9.0, 1.0], [10.0, 0.0], [11.0, 1.0], [12.0, 4.0]],
        )

    def test_uses_euclidean_segments_for_zones_without_authored_network(self):
        routing_graph = compile_routing_graph(self.connectivity)
        segment = routing_graph["segments"]["J"][0]
        self.assertEqual(segment["portals"], ["J_K", "J_L"])
        self.assertEqual(segment["geometry"], [[0.0, 0.0], [3.0, 4.0]])
        self.assertEqual(segment["distance_m"], 2.5)
        self.assertEqual(routing_graph["segments"]["A"], [])

    def test_rejects_authored_network_with_missing_portal_connector(self):
        connectivity = copy.deepcopy(self.connectivity)
        del connectivity["zones"]["H"]["movement_network"]["connectors"]["C_H"]
        with self.assertRaisesRegex(ValueError, "Connector coverage mismatch"):
            compile_routing_graph(connectivity)

    def test_rejects_connector_to_node_outside_backbone(self):
        connectivity = copy.deepcopy(self.connectivity)
        connectivity["zones"]["H"]["movement_network"]["connectors"]["C_H"][1] = "missing"
        with self.assertRaisesRegex(ValueError, "outside the backbone"):
            compile_routing_graph(connectivity)

    def test_rejects_movement_network_on_non_crossable_zone(self):
        connectivity = copy.deepcopy(self.connectivity)
        connectivity["zones"]["A"]["movement_network"] = {}
        with self.assertRaisesRegex(ValueError, "requires a crossable zone"):
            compile_routing_graph(connectivity)

    def test_rejects_movement_network_on_exterior(self):
        connectivity = copy.deepcopy(self.connectivity)
        connectivity["zones"]["exterior"] = {"crossable": False}
        connectivity["portals"]["A_exterior"] = {
            "virtual": False,
            "point": [0, 0],
        }
        connectivity["zones"]["exterior"]["movement_network"] = {}
        with self.assertRaisesRegex(ValueError, "exterior zone"):
            compile_routing_graph(connectivity)

    def test_rejects_non_finite_portal_coordinates(self):
        connectivity = copy.deepcopy(self.connectivity)
        connectivity["portals"]["B_H"]["point"][0] = float("nan")
        with self.assertRaisesRegex(ValueError, "finite number"):
            compile_routing_graph(connectivity)

    def test_rejects_non_finite_portal_coordinates_in_non_crossable_zone(self):
        connectivity = copy.deepcopy(self.connectivity)
        connectivity["portals"]["A_H"]["point"][0] = float("inf")
        with self.assertRaisesRegex(ValueError, "finite number"):
            compile_routing_graph(connectivity)

    def test_rejects_non_finite_movement_junction_coordinates(self):
        connectivity = copy.deepcopy(self.connectivity)
        connectivity["zones"]["H"]["movement_network"]["junctions"]["j-between"][1] = float("inf")
        with self.assertRaisesRegex(ValueError, "finite number"):
            compile_routing_graph(connectivity)

    def test_rejects_non_finite_floor_scale(self):
        connectivity = copy.deepcopy(self.connectivity)
        connectivity["floors"]["E"]["units_per_meter"] = float("nan")
        with self.assertRaisesRegex(ValueError, "finite number"):
            compile_routing_graph(connectivity)

    def test_compiles_all_target_portals_and_authored_e09_to_e20_route(self):
        root = Path(__file__).resolve().parent.parent
        source = json.loads(
            (root / "web" / "eg-connectivity-graph.json").read_text(
                encoding="utf-8"
            )
        )
        routing_graph = compile_routing_graph(source)
        self.assertNotIn("exterior", routing_graph["segments"])
        corridor_ids = {
            zone_id
            for zone_id in source["zones"]
            if zone_id.startswith("E.flur-") or zone_id == "E.durchgang"
        }
        self.assertEqual(len(corridor_ids), 37)
        for zone_id in corridor_ids:
            network = source["zones"][zone_id]["movement_network"]
            self.assertEqual(
                set(network["connector_paths"]), set(network["connectors"])
            )
            for portal_id, targets in network["connectors"].items():
                self.assertEqual(
                    set(network["connector_paths"][portal_id]), set(targets)
                )
                for target in targets:
                    path = network["connector_paths"][portal_id][target]
                    self.assertEqual(path[0], source["portals"][portal_id]["point"])
                    target_point = network["junctions"].get(
                        target, source["portals"].get(target, {})
                    )
                    if isinstance(target_point, dict):
                        target_point = target_point.get("point")
                    self.assertEqual(path[-1], target_point)

        segments = routing_graph["segments"]["E.flur-tr1-1"]
        self.assertEqual(len(segments), 300)

        portal_pair = ["E.09_E.flur-tr1-1", "E.20_E.flur-tr1-1"]
        segment = next(item for item in segments if item["portals"] == portal_pair)
        self.assertEqual(
            segment["geometry"][0],
            source["portals"][portal_pair[0]]["point"],
        )
        self.assertEqual(
            segment["geometry"][-1],
            source["portals"][portal_pair[1]]["point"],
        )
        centerline = source["zones"]["E.flur-tr1-1"]["movement_network"][
            "junctions"
        ]
        self.assertEqual(centerline["j.E.02.center"], [293.527, 116.723])
        expected_centerline = [
            centerline[f"j.E.{room_id}.center"]
            for room_id in (
                "10", "11a", "12", "11", "14", "13",
                "16", "15", "18", "17", "20",
            )
        ]
        self.assertEqual(
            [
                point
                for point in segment["geometry"]
                if point in expected_centerline
            ],
            expected_centerline,
        )
        self.assertEqual(len(segment["geometry"]), 16)
        self.assertEqual(segment["distance_m"], 20.92)

        junction_portals = [
            "E.flur-tr7-1_E.flur-tr7-4",
            "E.flur-tr7-1_E.flur-tr9-3",
        ]
        junction_segment = next(
            item
            for item in routing_graph["segments"]["E.flur-tr7-1"]
            if item["portals"] == junction_portals
        )
        self.assertEqual(
            junction_segment["geometry"],
            [
                source["portals"][junction_portals[0]]["point"],
                source["portals"][junction_portals[1]]["point"],
            ],
        )
        direct_door_portal = "E.flur-tr7-1_E.flur-tr9-3"
        routing_database = normalize_routing_graph(routing_graph)
        for start_zone, target_zone in (("E.80", "E.63"), ("E.63", "E.80")):
            route = shortest_route(routing_database, start_zone, target_zone)
            self.assertIn(direct_door_portal, route["portal_chain"])
            self.assertNotIn("E.flur-tr7-1_E.flur-tr7-5", route["portal_chain"])
            self.assertNotIn("E.flur-tr7-5_E.flur-tr9-3", route["portal_chain"])

        diagonal_corridor = source["zones"]["E.flur-tr3-1"]["movement_network"]
        diagonal_points = [
            source["portals"].get(node_id, {}).get(
                "point", diagonal_corridor["junctions"].get(node_id)
            )
            for node_id in diagonal_corridor["backbone"]
        ]
        self.assertTrue(
            all(
                math.dist(first, second) <= 8.001
                for first, second in zip(diagonal_points, diagonal_points[1:])
            )
        )
        for start_zone, target_zone in (("E.27", "E.28"), ("E.28", "E.27")):
            route = shortest_route(routing_database, start_zone, target_zone)
            self.assertEqual(
                route["portal_chain"],
                ["E.27_E.flur-tr3-1", "E.28_E.flur-tr3-1"]
                if start_zone == "E.27"
                else ["E.28_E.flur-tr3-1", "E.27_E.flur-tr3-1"],
            )
            self.assertLess(route["distance"], 3.0)

        portal_waypoint = [520.5, 528.5]
        portal_id = "E.flur-tr1-3_E.flur-tr2-3"
        corridor_network = source["zones"]["E.flur-tr1-3"]["movement_network"]
        waypoint_index = corridor_network["backbone"].index(
            next(
                junction_id
                for junction_id, point in corridor_network["junctions"].items()
                if point == portal_waypoint
            )
        )
        self.assertEqual(
            corridor_network["connectors"][portal_id],
            [
                corridor_network["backbone"][waypoint_index - 1],
                corridor_network["backbone"][waypoint_index + 1],
            ],
        )
        portal_connector_paths = corridor_network["connector_paths"][portal_id]
        self.assertEqual(len(portal_connector_paths), 2)
        self.assertNotEqual(
            *[path[-1] for path in portal_connector_paths.values()]
        )
        self.assertEqual(
            list(corridor_network["junctions"].values()).count(portal_waypoint), 1
        )
        portal_crossing_segment = next(
            item
            for item in routing_graph["segments"]["E.flur-tr1-3"]
            if portal_waypoint in item["geometry"]
        )
        self.assertEqual(
            portal_crossing_segment["geometry"].count(portal_waypoint), 1
        )

        e58_portals = ["E.58_E.58a", "E.58_E.flur-tr9-1"]
        e58_segment = next(
            item
            for item in routing_graph["segments"]["E.58"]
            if item["portals"] == e58_portals
        )
        self.assertEqual(
            e58_segment["geometry"],
            [
                source["portals"]["E.58_E.58a"]["point"],
                [1466.5, 450.0],
                [1384.9, 450.0],
                source["portals"]["E.58_E.flur-tr9-1"]["point"],
            ],
        )

        route = shortest_route(
            normalize_routing_graph(routing_graph), "E.09", "E.20"
        )
        self.assertEqual(route["portal_chain"], portal_pair)
        self.assertAlmostEqual(route["distance"], segment["distance_m"], places=3)

        e58_route = shortest_route(
            normalize_routing_graph(routing_graph), "E.flur-tr9-1", "E.58a"
        )
        self.assertEqual(
            e58_route["zone_sequence"], ["E.flur-tr9-1", "E.58", "E.58a"]
        )

        fallback_pair = sorted(
            portal_id
            for portal_id in source["portals"]
            if "E.flur-tr1-2" in portal_id
        )[:2]
        fallback_segment = next(
            item
            for item in routing_graph["segments"]["E.flur-tr1-2"]
            if item["portals"] == fallback_pair
        )
        expected_fallback_geometry = [
            source["portals"][portal_id]["point"] for portal_id in fallback_pair
        ]
        self.assertEqual(fallback_segment["geometry"][0], expected_fallback_geometry[0])
        self.assertEqual(fallback_segment["geometry"][-1], expected_fallback_geometry[-1])
        self.assertGreater(len(fallback_segment["geometry"]), 2)


if __name__ == "__main__":
    unittest.main()