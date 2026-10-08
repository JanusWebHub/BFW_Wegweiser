import copy
import json
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
        self.assertEqual(len(segment["geometry"]), 22)
        self.assertEqual(segment["distance_m"], 20.23)

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
        self.assertEqual(fallback_segment["geometry"], expected_fallback_geometry)


if __name__ == "__main__":
    unittest.main()