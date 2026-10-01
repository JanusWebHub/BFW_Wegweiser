# Spec proposals

Proposed additions, approved in review but not yet in `docs/data`. Each names the file and section it would change.

## 1. Zone kind `block` (inaccessible space)

`zoning_guidelines.md`, section "Zones" (new bullets) and "Portals" (exemption); `graph_format.md`, section "Validity rules".

A `block` is space that is drawn but nobody can enter: a shaft, a wall mass, a column or fixed obstacle, ventilation, fixed seating, a counter.

- A block is a zone like any other: it has an id, takes part in the no-gap, no-overlap coverage, and shares its boundary exactly with its neighbours.
- A block is never crossable and never a route start or target.
- A block needs no portal. It is exempt from "every zone has at least one portal" and from reachability checks. A block with a portal is invalid.
- Connectivity JSON (not yet emitted by the working graph, so blocks currently export as plain non-crossable zones): `"kind": "block"` on the zone (default `"kind": "room"` stays implicit). `crossable` must be `false`.
- SVG: class `zone block`, neutral colour, hatched.
- A space that is merely closed to the public (storage, technical room) is not a block; it is a normal non-crossable zone with a door.
- A seating area or hall someone can walk to stays a normal zone, even if it is not a through route.

Validator: block ⇒ `crossable: false` ∧ no portal; every non-block, non-`exterior` zone has a portal.

## 2. Nested rooms

`zoning_guidelines.md`, section "Zones", replaces the bullet "A room enclosed by another room is cut out of the outer zone as a hole."

A room inside another room (for example a disabled toilet inside a WC anteroom) is cut out of the host zone, as a notch where it touches the host's outline, otherwise as a hole.

- The host zone and the nested room share a boundary. The door between them is a normal portal.
- The host is crossable only when it is the only access to the nested room, under the existing rule "A room that is the only access to another room is crossable". This is the same rule, not an exception, and the report lists the host.
- A nested room that is also reachable another way does not make its host crossable.
- A nested room is not a block. It has a portal to its host (or to another zone) and is a valid destination.
- Zones with holes are exported as polygon with `holes` rings in the SVG path (`fill-rule="evenodd"`); the graph itself does not change.

Validator: coverage check counts holes as covered by their nested zones; a hole not filled by a zone is a gap.

## Rule ordering note

Doors always lie on the shared boundary of their two zones (within 0.6 units). If a drawn door and a drawn wall disagree, the drawn door wins up to about 4.5 units and the wall moves; larger differences snap the door to the wall.
