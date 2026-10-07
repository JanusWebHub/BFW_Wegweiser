import pathlib
import unittest
from xml.etree import ElementTree

from build_eg_svg import build_eg_svg, load_source_data


class EgSvgBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = pathlib.Path(__file__).resolve().parent.parent
        cls.redline_data, cls.underlay, cls.routing_graph = load_source_data(
            root / "claude" / "tools" / "eg-redline.html",
            root / "claude" / "review" / "data" / "routing-graph-fixed.json",
        )

    def test_source_matches_current_routing_graph(self):
        self.assertEqual(len(self.redline_data["zones"]), 193)
        self.assertEqual(len(self.redline_data["portals"]), 219)
        self.assertTrue(self.underlay.startswith("data:image/jpeg;base64,"))

    def test_builds_full_frame_svg_with_routing_ids(self):
        svg = build_eg_svg(self.redline_data, self.underlay, self.routing_graph)
        root = ElementTree.fromstring(svg)
        namespace = "{http://www.w3.org/2000/svg}"
        self.assertEqual(root.attrib["viewBox"], "0 0 1790 1000")
        self.assertIsNotNone(root.find(f'.//*[@id="zone-E.01"]'))
        self.assertIsNotNone(root.find(f'.//*[@id="portal-E.01_E.vr-e01_2"]'))
        self.assertEqual(len(root.findall(f".//{namespace}circle[@class='portal-point']")), 219)
        self.assertIsNotNone(root.find(f".//{namespace}image"))


if __name__ == "__main__":
    unittest.main()