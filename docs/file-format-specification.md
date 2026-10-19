# File Format Specification

| File type                  | File Name                 | Contents                                 |
| -------------------------- | ------------------------- | ---------------------------------------- |
| Adjacency graph            | `adjacency-graph.json`    | spaces and separators                    |
| Connectivity graph         | `connectivity-graph.json` | zones, portals and movement lines        |
| Routing graph              | `routing-graph.json`      | connectivity graph plus routing config   |
| Routing config             | `routing-config.json`     | state costs, segment costs, variants     |
| Zone SVG                   | `zone.svg`                | semantic floor plan of zones and portals |
| Navigation SVG             | `navigation.svg`          | map for displaying routes                |
| Zoning file                | `zoning.json`             | the model, saved by the zoning editor    |
| Plan SVG                   | `<floor id>-plan.svg`     | vectorized equivalent of the plans       |
| Precomputed routes dataset | `precomputed-routes.json` | routes per zone pair and variant         |

## File structure

A file's `format` value is its File Name without the extension.

### Connectivity graph

JSON, top level:

- `format`: `"connectivity-graph"`
- `zoning_file_version`: timestamp of the zoning file version this file derives from, ISO 8601 UTC with milliseconds, e.g. `"2026-10-14T09:30:00.000Z"`
- `saved_at`: timestamp of when this file was saved, in the same form
- `floors`: `{ <floor id>: <floor> }`
- `zones`: `{ <zone id>: <zone> }`
- `portals`: `{ <portal id>: <portal> }`

### Routing graph

JSON, top level:

- `format`: `"routing-graph"`
- `zoning_file_version`, `saved_at`: as in the connectivity graph
- `floors`, `zones`, `portals`: as in the connectivity graph
- `segments`: `{ <zone id>: [<segment>, ...] }`
- `state_costs`, `segment_costs`, `variants`: as in the routing config

### Routing config

JSON, top level:

- `format`: `"routing-config"`
- `zoning_file_version`, `saved_at`: as in the connectivity graph
- `state_costs`: `{ <state key>: <number> }`, extra cost of the state, in the unit of `distance_m`
- `segment_costs`: `{ <segment key>: <number> }`, extra cost of the segment, in the unit of `distance_m`
- `variants`: `{ <variant id>: <variant> }`

### Plan SVG

One file per floor. SVG, root `svg`:

- `viewBox`: `x y width height`, the floor's frame
- `data-floor-id`: floor id
- `data-level`: integer, the floor's level
- `data-units-per-meter`: number
- `data-saved-at`: timestamp of when this file was saved, ISO 8601 UTC with milliseconds
- `g id="underlays"`: the underlays, optional content
- `g id="trace"`: the traced elements

Group `underlays`:

- `image`: one per underlay, in drawing order, the first at the bottom
- `href`: file name of the source image; the key for picking the image again
- `width`, `height`: size of the image
- `transform`: placement, computed from the `data-` attributes below
- `opacity`: number
- `display="none"`: only on a hidden underlay
- `data-x`, `data-y`: position
- `data-rotation`: degrees
- `data-scale`: number
- `data-flip-x`, `data-flip-y`: `"true"`, only on a flipped underlay
- `data-locked`: `"true"`, only on a locked underlay
- `data-crop`: `x y width height`, only on a cropped underlay
- `clip-path`: `url(#clip-<n>)`, only on a cropped underlay; the `clipPath id="clip-<n>"` sits in a `defs` in the group
- `data-label`, `data-brightness`, `data-contrast`: only when not the default (empty, 1, 1)

Group `trace`:

- One `g` per layer, in layer order
- `data-layer`: layer name
- `display="none"`: only on a hidden layer
- `data-locked`: `"true"`, only on a locked layer
- The traced elements sit in their layer's `g`

Traced element, every kind:

- `id`: starts with a letter, then letters, digits and `_`; unique in the file; e.g. `line1`, `poly2`, `circle3`, `path4`, `text5`, `sym6`
- `stroke`, `stroke-width`: color and thickness; not on `text`
- `fill="none"`; not on `text`
- `vector-effect="non-scaling-stroke"`; not on `text`

Traced element, by kind:

- `line`: `x1`, `y1`, `x2`, `y2`
- `polyline`: `points`, `x,y` pairs separated by spaces
- `circle`: `cx`, `cy`, `r`
- `path`: `d`; `data-points`, the points the path runs through; `data-smooth`, `"true"` or `"false"`; `data-closed`, `"true"` or `"false"`
- `text`: `x`, `y`, `font-size`, `fill`; `text-anchor` and `transform`, only when set; the text is the content
- `text`, attached to an element: `data-for`, the id of that element; `data-dx`, `data-dy`, the offset
- Symbol, a `g`: `data-symbol`, one of `stairs`, `rack`, `door`, `gate`, `dock`, `column`, `pallet`, `ramp`, `elevator`; `data-cx`, `data-cy`, the center; `data-rot`, degrees; `data-width`, `data-depth`, meters; `transform`; `color`; the drawing as `path` children, in meters

## Model elements, ids and fields

### Floor

JSON:

- Id: `UG2`, `UG1`, `EG`, `OG1`, `OG2`, ...; the key in `floors`; the prefix of zone ids
- `level`: integer; `UG2` -2, `UG1` -1, `EG` 0, `OG1` 1, `OG2` 2, ...
- `svg`: string, path of the floor's plan SVG file
- `view_box`: `[x, y, width, height]`, numbers as in the SVG `viewBox` attribute; the floor's coordinate frame
- `units_per_meter`: number, SVG units per meter

### Zone

JSON:

- Id: string; the key in `zones`; unique across the building; no `_`; ASCII only
- Id, umlauts and `ß`: transliterated to `ae`, `oe`, `ue`, `ss`
- Id, numbered room: `<floor id>.<room number as printed>`, e.g. `EG.E.52`
- Id, named space: `<floor id>.<name>`, name = designer-assigned lowercase words joined by `-`, e.g. `EG.foyer`
- Id, split space: `-1`, `-2`, ... appended, e.g. `EG.flur-tr9-1`
- Id, same name for two spaces: `-a`, `-b`, ... appended
- Id, exterior: `<floor id>.exterior`
- Id: no other word of a name consists only of digits
- `floor`: floor id
- `crossable`: boolean; `false` for the exterior
- `navigable`: boolean; `true` for the exterior

SVG:

- One shape per zone, `id="<zone id>"`

### Portal

JSON:

- Id: string; the key in `portals`; `<zone id>_<zone id>`, the two zone ids sorted by character code, e.g. `EG.E.62_EG.flur-tr9-1`
- Id, further portal between the same zones: `_2`, `_3`, ... appended, e.g. `EG.E.62_EG.flur-tr9-1_2`
- `virtual`: boolean; `true` on a virtual boundary, `false` for a door or opening
- `vertical`: `true`; only on a portal between zones on two floors
- `line`: `[[x, y], [x, y]]`, start and end of the crossable section of the boundary between the two zones
- `midpoint`: `[x, y]`, the midpoint of `line`
- `points`: `{ <floor id>: [x, y] }`, one per joined floor; replaces `midpoint` and `line` on a vertical portal
- `emergency_exit`: `true`; only on portals to the exterior
- `main_entrance`: `true`; only on portals to the exterior
- Example: `"EG.hall_EG.office": { "virtual": false, "line": [[10, 20], [10, 30]], "midpoint": [10, 25] }`
- Example, vertical: `"EG.stair_OG1.stair": { "virtual": true, "vertical": true, "points": { "EG": [50, 60], "OG1": [50, 60] } }`

SVG:

- One `g`, `id="<portal id>"`, containing a `line` along the crossable section of the boundary and a `circle` at the midpoint of the `line`
- `class="portal virtual"` on a virtual portal

### State

JSON:

- Key: `zone_from | portal | zone_to`
- Example, in `state_costs`: `"EG.office|EG.hall_EG.office|EG.hall": 12.0`

### Segment

JSON, an entry in the list under its zone in `segments`:

- Key: a string of the form `entry_portal | zone | exit_portal`
- `portals`: `[entry_portal ; exit_portal]`
- `geometry`: `[[x, y], ...]`, from `entry_portal` to `exit_portal`
- `distance_m`: number; length of `geometry` divided by `units_per_meter`
- Example: `"segments": { "EG.hall": [ { "portals": ["EG.hall_EG.office", "EG.hall_EG.store"], "geometry": [[10, 25], [40, 25]], "distance_m": 1.5 } ] }`
- Example, in `segment_costs`: `"EG.hall_EG.office|EG.hall|EG.hall_EG.store": 5.0`

### Variant

JSON:

- Id: string, the variant name; the key in `variants`; `standard` is the variant with nothing restricted
- `non_crossable`: `[<zone id>, ...]`, zones the variant makes non-crossable; only the exceptions
- `non_navigable`: `[<zone id>, ...]`, zones the variant makes non-navigable; only the exceptions
- Example: `"variants": { "standard": { "non_crossable": [], "non_navigable": [] } }`

### Query

- `start`: zone id, of a navigable zone
- `target`: zone id, of a navigable zone
- `variant`: variant id

### Route

- A chain of zones and portals: `zone | portal | zone | ... | portal | zone`.

## Connectivity graph example

```json
{
  "format": "connectivity-graph",
  "zoning_file_version": "2026-10-14T09:30:00.000Z",
  "saved_at": "2026-10-14T09:31:12.000Z",
  "floors": {
    "EG":  { "level": 0, "svg": "EG-plan.svg", "view_box": [0, 0, 1580, 900], "units_per_meter": 20 },
    "OG1": { "level": 1, "svg": "OG1-plan.svg", "view_box": [0, 0, 1580, 900], "units_per_meter": 20 }
  },
  "zones": {
    "EG.exterior":     { "floor": "EG",  "crossable": false, "navigable": true },
    "EG.E.62":         { "floor": "EG",  "crossable": false, "navigable": true },
    "EG.flur-tr9-1":   { "floor": "EG",  "crossable": true,  "navigable": true },
    "EG.flur-tr9-2":   { "floor": "EG",  "crossable": true,  "navigable": true },
    "EG.TR9":          { "floor": "EG",  "crossable": true,  "navigable": true },
    "OG1.TR9":         { "floor": "OG1", "crossable": true,  "navigable": true },
    "OG1.flur-tr9":    { "floor": "OG1", "crossable": true,  "navigable": true }
  },
  "portals": {
    "EG.E.62_EG.flur-tr9-1":        { "virtual": false, "midpoint": [453, 234] },
    "EG.TR9_EG.flur-tr9-1":         { "virtual": false, "midpoint": [625, 234] },
    "EG.flur-tr9-1_EG.flur-tr9-2":  { "virtual": true, "midpoint": [677, 202] },
    "EG.exterior_EG.flur-tr9-2":    { "virtual": false, "midpoint": [1206, 180], "main_entrance": true },
    "EG.TR9_OG1.TR9":               { "virtual": true, "vertical": true, "points": {"EG": [650, 330], "OG1": [650, 330]} },
    "OG1.TR9_OG1.flur-tr9":         { "virtual": false, "midpoint": [625, 234] }
  }
}
```

## Routing config example

```json
{
  "format": "routing-config",
  "zoning_file_version": "2026-10-14T09:30:00.000Z",
  "saved_at": "2026-10-14T09:45:30.000Z",
  "state_costs": {
    "EG.flur-tr9-1|EG.TR9_EG.flur-tr9-1|EG.TR9": 12.0,
    "EG.TR9|EG.TR9_OG1.TR9|OG1.TR9": 20.0,
    "OG1.TR9|EG.TR9_OG1.TR9|EG.TR9": 15.0
  },
  "segment_costs": {
    "EG.E.62_EG.flur-tr9-1|EG.flur-tr9-1|EG.flur-tr9-1_EG.flur-tr9-2": 5.0
  },
  "variants": { "standard": { "non_crossable": [], "non_navigable": [] } }
}
```

## Routing graph example

```json
{
  "format": "routing-graph",
  "zoning_file_version": "2026-10-14T09:30:00.000Z",
  "saved_at": "2026-10-14T09:46:05.000Z",
  "floors": {
    "EG":  { "level": 0, "svg": "EG-plan.svg", "view_box": [0, 0, 1580, 900], "units_per_meter": 20 },
    "OG1": { "level": 1, "svg": "OG1-plan.svg", "view_box": [0, 0, 1580, 900], "units_per_meter": 20 }
  },
  "zones": {
    "EG.exterior":     { "floor": "EG",  "crossable": false, "navigable": true },
    "EG.E.62":         { "floor": "EG",  "crossable": false, "navigable": true },
    "EG.flur-tr9-1":   { "floor": "EG",  "crossable": true,  "navigable": true },
    "EG.flur-tr9-2":   { "floor": "EG",  "crossable": true,  "navigable": true },
    "EG.TR9":          { "floor": "EG",  "crossable": true,  "navigable": true },
    "OG1.TR9":         { "floor": "OG1", "crossable": true,  "navigable": true },
    "OG1.flur-tr9":    { "floor": "OG1", "crossable": true,  "navigable": true }
  },
  "portals": {
    "EG.E.62_EG.flur-tr9-1":        { "virtual": false, "midpoint": [453, 234] },
    "EG.TR9_EG.flur-tr9-1":         { "virtual": false, "midpoint": [625, 234] },
    "EG.flur-tr9-1_EG.flur-tr9-2":  { "virtual": true, "midpoint": [677, 202] },
    "EG.exterior_EG.flur-tr9-2":    { "virtual": false, "midpoint": [1206, 180], "main_entrance": true },
    "EG.TR9_OG1.TR9":               { "virtual": true, "vertical": true, "points": {"EG": [650, 330], "OG1": [650, 330]} },
    "OG1.TR9_OG1.flur-tr9":         { "virtual": false, "midpoint": [625, 234] }
  },
  "segments": {
    "EG.flur-tr9-1": [
      { "portals": ["EG.E.62_EG.flur-tr9-1", "EG.TR9_EG.flur-tr9-1"], "geometry": [[453, 234], [625, 234]], "distance_m": 8.6 },
      { "portals": ["EG.TR9_EG.flur-tr9-1", "EG.E.62_EG.flur-tr9-1"], "geometry": [[625, 234], [453, 234]], "distance_m": 8.6 },
      { "portals": ["EG.E.62_EG.flur-tr9-1", "EG.flur-tr9-1_EG.flur-tr9-2"], "geometry": [[453, 234], [677, 202]], "distance_m": 11.31 },
      { "portals": ["EG.flur-tr9-1_EG.flur-tr9-2", "EG.E.62_EG.flur-tr9-1"], "geometry": [[677, 202], [453, 234]], "distance_m": 11.31 },
      { "portals": ["EG.TR9_EG.flur-tr9-1", "EG.flur-tr9-1_EG.flur-tr9-2"], "geometry": [[625, 234], [677, 202]], "distance_m": 3.05 },
      { "portals": ["EG.flur-tr9-1_EG.flur-tr9-2", "EG.TR9_EG.flur-tr9-1"], "geometry": [[677, 202], [625, 234]], "distance_m": 3.05 }
    ],
    "EG.flur-tr9-2": [
      { "portals": ["EG.exterior_EG.flur-tr9-2", "EG.flur-tr9-1_EG.flur-tr9-2"], "geometry": [[1206, 180], [677, 202]], "distance_m": 26.47 },
      { "portals": ["EG.flur-tr9-1_EG.flur-tr9-2", "EG.exterior_EG.flur-tr9-2"], "geometry": [[677, 202], [1206, 180]], "distance_m": 26.47 }
    ],
    "EG.TR9": [
      { "portals": ["EG.TR9_EG.flur-tr9-1", "EG.TR9_OG1.TR9"], "geometry": [[625, 234], [650, 330]], "distance_m": 4.96 },
      { "portals": ["EG.TR9_OG1.TR9", "EG.TR9_EG.flur-tr9-1"], "geometry": [[650, 330], [625, 234]], "distance_m": 4.96 }
    ],
    "OG1.TR9": [
      { "portals": ["EG.TR9_OG1.TR9", "OG1.TR9_OG1.flur-tr9"], "geometry": [[650, 330], [625, 234]], "distance_m": 4.96 },
      { "portals": ["OG1.TR9_OG1.flur-tr9", "EG.TR9_OG1.TR9"], "geometry": [[625, 234], [650, 330]], "distance_m": 4.96 }
    ],
    "OG1.flur-tr9": []
  },
  "state_costs": {
    "EG.flur-tr9-1|EG.TR9_EG.flur-tr9-1|EG.TR9": 12.0,
    "EG.TR9|EG.TR9_OG1.TR9|OG1.TR9": 20.0,
    "OG1.TR9|EG.TR9_OG1.TR9|EG.TR9": 15.0
  },
  "segment_costs": {
    "EG.E.62_EG.flur-tr9-1|EG.flur-tr9-1|EG.flur-tr9-1_EG.flur-tr9-2": 5.0
  },
  "variants": { "standard": { "non_crossable": [], "non_navigable": [] } }
}
```
