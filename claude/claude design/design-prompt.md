Create the simplified floor plan and the connectivity graph for the ground floor (EG) of BFW Berlin-Brandenburg, Charlottenburg.

Attached:

- Lageplan EG (PDF scan, stored upside down)
- photos of the Flucht- und Rettungspläne B 7967_052 to B 7967_061; each plan number is in its title block
- `zoning_guidelines.md`: how to zone and how to mark up the SVG
- `graph_format.md`: the file formats; for this task only the connectivity graph applies

Outputs, updated in every step:

- `bfw-eg.svg`: the simplified floor plan, marked up as in `zoning_guidelines.md`
- `connectivity-graph.json`: floor `E` only, `provenance` set to `unverified`
- `zoning-report.md`: the report described in `zoning_guidelines.md`, with a section per step

Follow the two documents exactly. Where the sources are unclear, do not guess silently: draw your best reading and list it in the report.

## Steps

Work in the steps below. After each step, deliver the three files and stop. Do not start the next step until I approve. Do not change anything approved in an earlier step unless I ask. The checks in `zoning_guidelines.md` apply to what exists after each step; a zone may be without portals until the portal step of its wing.

1. Skeleton, whole EG: shell, wing shapes, corridor zones, Durchgang and Foyer, stairwell zones `E.TR1` to `E.TR9`, the virtual portals between these circulation zones, and `units_per_meter`.
2. Rooms, one wing per step: all remaining zones of the wing, with labels. The skeleton stays unchanged.
3. Portals, one wing per step: doors, virtual portals and exits of the wing.
4. Check, whole EG: the checks in `zoning_guidelines.md`, portals between wings, and the complete report.

Wings, in this order (step 2.1 is the rooms of wing 1, step 3.1 its portals, and so on):

1. East block: B 7967_058, B 7967_059
2. Entrance and foyer: B 7967_055, B 7967_057
3. Kitchen: B 7967_056
4. North-west wing: B 7967_060, B 7967_061
5. Long wing: B 7967_052
6. IQ + UKM wing: B 7967_053
7. Hexagon: B 7967_054
8. Middle area: Lageplan only

A room shown on plans of two wings belongs to the earlier wing in this order.

This prompt may be given to a new session at any step, with the approved files attached; continue from that step.

The east wing SVG you made earlier uses older ids and markup; do not reuse them.
