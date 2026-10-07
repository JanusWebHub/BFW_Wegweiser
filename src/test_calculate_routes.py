import json
import pathlib
import unittest

from calculate_routes import (
    calculate_all_routes,
    compact_route_table,
    normalize_routing_graph,
    shortest_route,
)


class EgRoutingGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = pathlib.Path(__file__).resolve().parent.parent
        graph_path = root / "claude" / "review" / "data" / "routing-graph-fixed.json"
        cls.source = json.loads(graph_path.read_text(encoding="utf-8"))
        cls.graph = normalize_routing_graph(cls.source)

    def test_normalizes_routable_portals_and_segments(self):
        self.assertEqual(len(self.source["portals"]), 219)
        self.assertEqual(len(self.graph["portals"]), 206)
        self.assertEqual(len(self.graph["segments"]), 814 - sum(
            1
            for segments in self.source["segments"].values()
            for segment in segments
            if any(
                self.source["portals"][portal_id].get("emergency_exit")
                and not self.source["portals"][portal_id].get("main_entrance")
                for portal_id in segment["portals"]
            )
        ))
        self.assertEqual(self.graph["zones"]["E.01"]["navigable"], True)
        self.assertEqual(self.graph["zones"]["exterior"]["navigable"], True)
        self.assertEqual(self.graph["zones"]["exterior"]["crossable"], False)
        self.assertEqual(self.graph["indexes"]["zone_portals"]["exterior"], ["E.52_exterior"])

    def test_filters_emergency_exits_but_keeps_main_entrance(self):
        emergency_portals = {
            portal_id
            for portal_id, portal in self.source["portals"].items()
            if portal.get("emergency_exit") and not portal.get("main_entrance")
        }
        self.assertEqual(len(emergency_portals), 13)
        self.assertTrue(emergency_portals.isdisjoint(self.graph["portals"]))
        self.assertIn("E.52_exterior", self.graph["portals"])

    def test_computes_representative_eg_route_in_meters(self):
        route = shortest_route(self.graph, "E.01", "E.52")
        self.assertEqual(route["status"], "ok")
        self.assertAlmostEqual(route["distance"], 112.79, places=2)
        self.assertEqual(route["sequence"][0], "E.01")
        self.assertEqual(route["sequence"][-1], "E.52")

    def test_routes_to_and_from_exterior_use_main_entrance(self):
        from_exterior = shortest_route(self.graph, "exterior", "E.01")
        to_exterior = shortest_route(self.graph, "E.01", "exterior")

        self.assertEqual(from_exterior["status"], "ok")
        self.assertEqual(from_exterior["portal_chain"][0], "E.52_exterior")
        self.assertEqual(from_exterior["zone_sequence"][0], "exterior")
        self.assertEqual(from_exterior["zone_sequence"][-1], "E.01")
        self.assertEqual(to_exterior["status"], "ok")
        self.assertEqual(to_exterior["portal_chain"][-1], "E.52_exterior")
        self.assertEqual(to_exterior["zone_sequence"][-1], "exterior")
        self.assertNotIn("exterior", to_exterior["zone_sequence"][1:-1])

    def test_compact_route_table_includes_exterior_endpoint(self):
        graph = {
            "meta": {"provenance": "unverified"},
            "zones": {
                "A": {"crossable": True, "navigable": True},
                "B": {"crossable": False, "navigable": True},
                "exterior": {"crossable": False, "navigable": True},
            },
            "portals": {
                "A_B": {"id": "A_B", "zones": ["A", "B"]},
                "A_exterior": {"id": "A_exterior", "zones": ["A", "exterior"]},
            },
            "indexes": {
                "zone_portals": {
                    "A": ["A_B", "A_exterior"],
                    "B": ["A_B"],
                    "exterior": ["A_exterior"],
                }
            },
            "segments": {
                "A_segment": {
                    "id": "A_segment",
                    "zone_id": "A",
                    "portals": ["A_B", "A_exterior"],
                    "distance": 4,
                }
            },
            "special_state_costs": {},
            "segment_costs": {},
            "variants": {"standard": []},
        }
        routed = calculate_all_routes(graph)
        table = compact_route_table(routed)
        exterior_index = table["zones"].index("exterior")
        room_index = table["zones"].index("B")
        to_exterior = table["routes"][room_index][exterior_index]
        from_exterior = table["routes"][exterior_index][room_index]

        self.assertEqual(table["variant"], "standard")
        self.assertIsNotNone(to_exterior)
        self.assertIsNotNone(from_exterior)
        self.assertEqual(table["portals"][to_exterior[-1]], "A_exterior")
        self.assertEqual(table["portals"][from_exterior[0]], "A_exterior")

    def test_allows_non_crossable_endpoint_but_not_transit(self):
        graph = {
            "zones": {
                "A": {"crossable": False},
                "B": {"crossable": False},
                "C": {"crossable": True},
                "D": {"crossable": False},
            },
            "portals": {
                "A_B": {"id": "A_B", "zones": ["A", "B"]},
                "B_C": {"id": "B_C", "zones": ["B", "C"]},
                "C_D": {"id": "C_D", "zones": ["C", "D"]},
            },
            "indexes": {"zone_portals": {"A": ["A_B"], "B": ["A_B", "B_C"], "C": ["B_C", "C_D"], "D": ["C_D"]}},
            "segments": {
                "A_B_inside": {"id": "A_B_inside", "zone_id": "B", "portals": ["A_B", "B_C"], "distance": 1},
                "C_inside": {"id": "C_inside", "zone_id": "C", "portals": ["B_C", "C_D"], "distance": 4},
            },
            "special_state_costs": {},
            "segment_costs": {},
            "variants": {"standard": []},
        }
        self.assertEqual(shortest_route(graph, "A", "B")["status"], "ok")
        self.assertEqual(shortest_route(graph, "A", "D")["status"], "unreachable")

    def test_applies_state_and_directional_segment_costs(self):
        graph = {
            "zones": {"A": {"crossable": False}, "C": {"crossable": True}, "D": {"crossable": False}},
            "portals": {
                "A_C": {"id": "A_C", "zones": ["A", "C"]},
                "C_D": {"id": "C_D", "zones": ["C", "D"]},
            },
            "indexes": {"zone_portals": {"A": ["A_C"], "C": ["A_C", "C_D"], "D": ["C_D"]}},
            "segments": {"C_inside": {"id": "C_inside", "zone_id": "C", "portals": ["A_C", "C_D"], "distance": 4}},
            "special_state_costs": {"A|A_C|C": 1, "C|C_D|D": 2},
            "segment_costs": {"A_C|C|C_D": 3},
            "variants": {"standard": []},
        }
        route = shortest_route(graph, "A", "D")
        self.assertEqual(route["distance"], 4)
        self.assertEqual(route["special_cost"], 6)
        self.assertEqual(route["total_cost"], 10)

    def test_compact_table_encodes_portal_chains_as_indexes(self):
        database = {
            "meta": {"provenance": "unverified", "variant": "standard"},
            "portals": {"A_B": {}, "B_C": {}},
            "routes": {
                "A": {
                    "A": {"status": "ok", "portal_chain": []},
                    "C": {"status": "ok", "portal_chain": ["A_B", "B_C"]},
                },
                "C": {
                    "A": {"status": "ok", "portal_chain": ["B_C", "A_B"]},
                    "C": {"status": "ok", "portal_chain": []},
                },
            },
        }
        table = compact_route_table(database)
        self.assertEqual(table["portals"], ["A_B", "B_C"])
        self.assertEqual(table["routes"], [[[], [0, 1]], [[1, 0], []]])


if __name__ == "__main__":
    unittest.main()