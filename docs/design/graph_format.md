# Graph format

- Adjacency graph: spaces and separators from the architectural plans.
- Connectivity graph: zones and portals, created from the adjacency graph alongside the simplified floor plan SVG.
- Routing graph: connectivity graph plus routing config.

This level covers the connectivity graph, the routing config and the routing graph.

## Ids

- Zone id: the room number as printed (`E.62`, `R.58`), or a designer-assigned lowercase name with `-` between words (`E.foyer`, `E.flur-tr9`). A room number printed on several floors gets the floor code in front (`E.TR9`, `1.TR9`). A space split into several zones gets `-1`, `-2`, … appended (`E.flur-tr9-1`); two spaces that would get the same name get `-a`, `-b`, …; no other word of a name is only digits. Zone ids contain no `_` and are unique across the building.
- The exterior is one zone, `exterior`, with no floor.
- Portal id: the two zone ids sorted by character code and joined by `_`, with `_2` for a second portal between the same zones: `E.62_E.flur-tr9-1`, `E.62_E.flur-tr9-1_2`.
- State key: `zone_from|portal|zone_to`, e.g. `E.flur-tr9-1|E.TR9_E.flur-tr9-1|E.TR9`.
- Segment key: `portal|zone|portal` in walking direction, e.g. `E.62_E.flur-tr9-1|E.flur-tr9-1|E.flur-tr9-1_E.flur-tr9-2`.

## Connectivity graph

Created by zoning. Floors with their SVG frame and scale, zones with floor and crossability, portals with the virtual flag and their midpoint in the floor's frame. A vertical portal joins zones on two floors (stairs, lift) and has a point on each. A portal to `exterior` lies on the floor of its other zone and may carry `emergency_exit: true` or `main_entrance: true`. Zones are drawn roughly convex, so that a straight line between two portals of a zone stays inside it.

`provenance` is `demo` for fictional data, `unverified` for data not yet checked against the plans, `verified` after that check.

```json
{
  "format": "wegweiser-connectivity-graph",
  "version": 1,
  "provenance": "demo",
  "floors": {
    "E":  { "level": 0, "svg": "web/assets/bfw-eg.svg", "view_box": [0, 0, 1580, 900], "units_per_meter": 20 },
    "1":  { "level": 1, "svg": "web/assets/bfw-og1.svg", "view_box": [0, 0, 1580, 900], "units_per_meter": 20 }
  },
  "zones": {
    "exterior":      { "crossable": false },
    "E.62":          { "floor": "E", "crossable": false },
    "E.flur-tr9-1":  { "floor": "E", "crossable": true },
    "E.flur-tr9-2":  { "floor": "E", "crossable": true },
    "E.TR9":         { "floor": "E", "crossable": true },
    "1.TR9":         { "floor": "1", "crossable": true },
    "1.flur-tr9":    { "floor": "1", "crossable": true }
  },
  "portals": {
    "E.62_E.flur-tr9-1":          { "virtual": false, "point": [453, 234] },
    "E.TR9_E.flur-tr9-1":         { "virtual": false, "point": [625, 234] },
    "E.flur-tr9-1_E.flur-tr9-2":  { "virtual": true, "point": [677, 202] },
    "E.flur-tr9-2_exterior":      { "virtual": false, "point": [1206, 180], "main_entrance": true },
    "1.TR9_E.TR9":                { "virtual": true, "vertical": true, "points": {"E": [650, 330], "1": [650, 330]} },
    "1.TR9_1.flur-tr9":           { "virtual": false, "point": [625, 234] }
  }
}
```

## Routing config

Extra costs are per direction; anything not authored is 0, so both directions cost the same unless authored otherwise. Climbing or descending a floor is a state cost on the vertical portal. A variant is a named list of zones made non-crossable in addition to the connectivity graph's own.

```json
{
  "format": "wegweiser-routing-config",
  "version": 1,
  "state_costs": {
    "E.flur-tr9-1|E.TR9_E.flur-tr9-1|E.TR9": 12.0,
    "E.TR9|1.TR9_E.TR9|1.TR9": 20.0,
    "1.TR9|1.TR9_E.TR9|E.TR9": 15.0
  },
  "segment_costs": {
    "E.62_E.flur-tr9-1|E.flur-tr9-1|E.flur-tr9-1_E.flur-tr9-2": 5.0
  },
  "variants": {
    "standard": [],
    "stufenlos": ["E.TR9", "1.TR9"]
  }
}
```

## Routing graph

Built from the connectivity graph and the routing config. Segments are computed: in every crossable zone, each pair of its portals gets one segment, a straight line between the two portal points on the zone's floor. Portals are listed in sorted order and the line runs from the first to the second; walking backwards uses the reversed line. `distance_m` is the line length divided by `units_per_meter`. Non-crossable zones get no segments.

```json
{
  "format": "wegweiser-routing-graph",
  "version": 1,
  "provenance": "demo",
  "floors": "from the connectivity graph",
  "zones": "from the connectivity graph",
  "portals": "from the connectivity graph",
  "segments": {
    "E.flur-tr9-1": [
      { "portals": ["E.62_E.flur-tr9-1", "E.TR9_E.flur-tr9-1"], "geometry": [[453, 234], [625, 234]], "distance_m": 8.6 },
      { "portals": ["E.62_E.flur-tr9-1", "E.flur-tr9-1_E.flur-tr9-2"], "geometry": [[453, 234], [677, 202]], "distance_m": 11.31 },
      { "portals": ["E.TR9_E.flur-tr9-1", "E.flur-tr9-1_E.flur-tr9-2"], "geometry": [[625, 234], [677, 202]], "distance_m": 3.05 }
    ],
    "E.flur-tr9-2": [
      { "portals": ["E.flur-tr9-1_E.flur-tr9-2", "E.flur-tr9-2_exterior"], "geometry": [[677, 202], [1206, 180]], "distance_m": 26.47 }
    ],
    "E.TR9": [
      { "portals": ["1.TR9_E.TR9", "E.TR9_E.flur-tr9-1"], "geometry": [[650, 330], [625, 234]], "distance_m": 4.96 }
    ],
    "1.TR9": [
      { "portals": ["1.TR9_1.flur-tr9", "1.TR9_E.TR9"], "geometry": [[625, 234], [650, 330]], "distance_m": 4.96 }
    ],
    "1.flur-tr9": []
  },
  "state_costs": "from the routing config",
  "segment_costs": "from the routing config",
  "variants": "from the routing config"
}
```

## Validity rules

Connectivity graph:

- Zone ids contain no `_`. Every zone except `exterior` has a `floor` that exists.
- Portal id is its two zone ids in sorted order joined by `_`, plus optional `_n`; both zones exist and differ.
- A non-vertical portal joins zones on the same floor; a vertical portal joins zones on different floors. Exception: a portal to `exterior` lies on the floor of its other zone.
- Every zone has at least one portal; every portal has `virtual`.
- `emergency_exit` and `main_entrance` appear only on portals to `exterior`.
- Every floor has `svg`, `view_box`, `units_per_meter`.
- A non-vertical portal has `point` inside its floor's view box; a vertical portal has `points` inside the view boxes of both floors.

Routing config:

- All extra costs are zero or more; every key refers to an existing state or segment; every variant zone exists.

## Search rules

- Input is a start zone, a target zone and a variant. Start and target must differ; equal zones are an invalid query.
- Route cost is the sum of segment distances, segment extra costs and state extra costs, including the first state.
- Every zone between start and target must be crossable in the chosen variant. Start and target may be non-crossable.
- If no path exists, the result is `unreachable`.

## Files

| File | Location |
| --- | --- |
| `connectivity-graph.json` | `data/` |
| `routing-config.json` | `data/` |
| `routing-graph.json` | `data/` |
| `demo-connectivity-graph.json`, `demo-routing-config.json`, `demo-routing-graph.json` | `src/fixtures/` |

## Deferred

- Adjacency graph.
- Movement lines: what a movement line is in the data (one polyline per zone, or several lines that meet), and how a portal connects to it. Movement lines replace the straight segment lines where they exist.
- Obstacles inside a zone: a straight line can pass through one.
- Walked distances: straight lines give the shortest possible distance, not the path people take.
- Rulebook addition for floors and vertical portals. The rulebook has no floors and defines a portal as the midpoint of a boundary in one plan (1.4).
- How the SVG supplies `units_per_meter`: real units in the SVG's `width`/`height`, or an attribute on the root element. Until then it is written in the connectivity graph.
