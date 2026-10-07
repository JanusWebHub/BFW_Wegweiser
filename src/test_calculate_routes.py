import json
import pathlib
import unittest

from calculate_routes import (
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

    def test_normalizes_all_portals_and_segments(self):
        self.assertEqual(len(self.graph["portals"]), 219)
        self.assertEqual(len(self.graph["segments"]), 814)
        self.assertEqual(self.graph["zones"]["E.01"]["navigable"], True)
        self.assertEqual(self.graph["zones"]["exterior"]["navigable"], False)

    def test_computes_representative_eg_route_in_meters(self):
        route = shortest_route(self.graph, "E.01", "E.52")
        self.assertEqual(route["status"], "ok")
        self.assertAlmostEqual(route["distance"], 112.79, places=2)
        self.assertEqual(route["sequence"][0], "E.01")
        self.assertEqual(route["sequence"][-1], "E.52")

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