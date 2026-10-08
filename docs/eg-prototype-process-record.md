# EG Prototype: Process Record

Date: 2026-10-07
Scope: the EG navigation prototype work in this conversation, from initial framing through branch publication and return to `local/simpler`.

This is a historical implementation record, not a design decision or specification. It distinguishes user direction, assistant implementation choices, and observed outcomes. Prototype behavior must not be read as approval of the source graph or as a finalized system contract.

## Goal and scope

The user wanted a working EG browser prototype as quickly as possible, using the current data in `claude/review` and the East Wing prototype as a practical example. The requested flow was the existing Python route computer applied to `claude/review/data/routing-graph-fixed.json`, followed by a similar static browser client. GitHub Pages was the intended way to make it accessible online.

The user prioritized a usable result over a complete implementation or another round of planning. The prototype was a navigation demonstration, not the zoning editor, not the implementation of the full zoning-to-navigation architecture, and not proof that the EG model was verified.

## Source data and initial assessment

The selected routing input was `claude/review/data/routing-graph-fixed.json`. It contains zones, portals, segments grouped by zone, state and segment cost maps, and variants. Its provenance is `unverified`.

The graph format differed from the East Wing route calculator's input:

- Segments are grouped by zone and store distance in meters as `distance_m`.
- Portal records contain a point and virtual flag, but no explicit zone-pair field. Portal endpoints are encoded in their IDs according to the graph format.
- The routing graph has crossability but no explicit navigability field. The adapter derived navigable endpoint zones from the presence of portals, excluding `exterior`.
- Segments exist only for zones that can be traversed. Non-crossable zones may still be route endpoints but cannot be transit zones.

The existing East Wing browser client expected a different precomputed database shape. It remained a useful presentation example, but the EG data required an adapter and client-side route reconstruction.

The matching floor plan was not present as a standalone SVG. The local `claude/tools/eg-redline.html` contained both an embedded JPEG underlay and polygon and portal geometry. Comparison with the selected routing graph found the same 193 interior zone IDs and all 219 portal IDs. Portal midpoint discrepancies were at most about 0.071 SVG units. This established coordinate compatibility for the prototype; it did not establish the geometry as authoritative or approved.

The supplied PDF was considered, but this workspace had no local PDF renderer installed. The embedded redline plan was therefore used as the faster available source.

## User direction and decisions

- Use the current EG routing graph from the Claude review package and adapt it to the existing route-computation flow.
- Work on a new feature branch, ultimately named `feature/eg-prototype`, based on `local/simpler`.
- Keep the prototype static and browser-based, with the route computation performed by Python.
- Use the redline page's embedded plan data to create a display SVG when its geometry was shown to match the routing graph.
- Keep the first commit focused on the deployable browser bundle. Later, add the route and SVG build sources and tests by amending that commit.
- Use a brief note in `docs/working-record.md` and keep the detailed process account in a separate file.
- The user considered whether “demo” might describe the result better than “prototype”; no naming change was made.

## Assistant implementation choices

### Route adaptation

The existing route computer in `src/calculate_routes.py` was extended to normalize the EG format while retaining its existing database support. The adapter:

- Parses portal IDs into zone pairs, relying on the graph-format rule that zone IDs contain no underscores and portal IDs join sorted zone IDs with `_`, with a numeric suffix for additional portals between a pair.
- Flattens grouped EG segments and assigns local segment IDs.
- Preserves meter distances, geometry, state costs, segment costs, and named routing variants.
- Builds zone-to-portal indexes and identifies queryable endpoints from portal connectivity.

The route search was adjusted to prohibit transit through non-crossable zones while allowing them as start or target zones. It applies directional state and segment costs, accepts a selected variant, and allows unreachable pairs in the generated table. The source graph's cost maps were empty and its `standard` variant had no additional restrictions, so those capabilities were structurally supported but not exercised by this data.

The displayed distance is in meters. Total cost is shown without a meter suffix because special costs do not necessarily have a distance unit. No special-cost behavior was demonstrated by the source data.

### Compact all-pairs output

The first full in-memory all-pairs result measured about 68,416,981 bytes when serialized as compact JSON. That was not a generated or committed file. It was the size estimate for a verbose structure containing a detailed object per route pair, including repeated IDs, sequences, states, segment references, and the graph data.

The chosen output, `web/eg-routes.json`, instead stores zone and portal lookup arrays plus a matrix of portal-index chains, with `null` for unreachable pairs. The browser combines that chain with the separately loaded routing graph to recover the zone sequence, segment geometry, distance, and costs. The compact table measured about 1,176,906 bytes. The graph and display SVG remain separate assets. This avoided embedding Python or calculating paths in the browser while substantially reducing repeated route data.

### Browser client

New `web/eg.html`, `web/eg.js`, and `web/eg.css` provide start and target selectors, route swapping, route metrics, instructions, route geometry, and portal markers. The EG page reuses the East Wing stylesheet. As the graph has no display labels, selectors show zone IDs. The source graph and compact table are fetched as static JSON, and the display SVG is loaded separately. This fetch-based client requires HTTP or GitHub Pages; it does not run directly from `file://`.

Because the EG routing graph omits explicit portal zone pairs, the browser also derives them from portal IDs when reconstructing the route. The SVG builder and browser rely on the documented underscore-free zone-ID convention.

### Display SVG

`src/build_eg_svg.py` extracts the embedded plan and geometry from the redline HTML, checks that zone and portal IDs match the routing graph, and checks portal midpoint alignment before writing `web/assets/bfw-eg.svg`. The generated SVG uses the routing graph's 1790 × 1000 frame, includes the underlay, zone polygons, labels, portals, and shell, and assigns stable zone and portal IDs for route highlighting.

This generated SVG is prototype display output. It is not the finalized Navigation SVG described by the system design, and its source geometry inherits the review graph's unverified provenance.

## Problems found and corrections

- Initially the local page showed a data-load error because the route table and copied graph had not yet been generated in the expected `web/` paths. The user generated them locally; no generated data was committed until the bundle commit.
- Browser testing with mock data showed route details could render, but the first real-data load failed because graph portal records lack explicit zone pairs. The client was corrected to recover pairs from portal IDs.
- The first portal-pair parser considered every possible zone pair and made normalization slow. It was replaced with parsing based on the graph-format ID rules.
- Initial compact-table test expectations omitted the full destination row and were corrected.
- The mobile layout overflowed because the long model-status label inherited `white-space: nowrap`. It was made wrappable, and a stylesheet query version was added after the browser kept serving a cached copy.
- Route totals were initially labeled in meters. That unit was removed because total cost can include non-distance special costs.

These are implementation corrections from the prototype work, not newly established project-wide rules.

## Validation performed

- The normalized source produced 181 navigable endpoints, 219 portals, and 814 segments. All portal IDs were mapped during normalization.
- The representative route `E.01` to `E.52` computed to 112.79 m, displayed as 112.8 m, with 11 portals. The reverse route also rendered.
- The compact output contained 32,761 ordered route pairs and measured about 1.18 MB. No unreachable pairs were found in this graph.
- SVG builder tests parsed the generated SVG as XML and checked the frame, underlay, and expected zone and portal elements.
- Twelve Python tests passed. The browser JavaScript syntax check passed.
- Browser checks exercised actual route data and SVG at desktop and mobile widths, including route reversal and absence of horizontal overflow.

These checks establish prototype behavior and data compatibility only. They do not establish that the EG graph is verified, that its inferred geometry is correct against source plans, or that its distances represent walked routes.

## Branches, commits, and publishing

### JanusWebHub branch

The user created `feature/eg-prototype` from `local/simpler` at `c326569`. The first commit contained the six-file static bundle. The route calculator, SVG builder, and focused tests were subsequently staged and added by amending that commit with the message `Add EG prototype`. The resulting Janus commit is `f66181a`.

The Janus branch was pushed and is separate from `local/simpler`. The custom `.github/workflows/deploy-eg-prototype.yml` was considered, but not retained: it was not part of the prototype commit and was later deleted. The local `local/simpler` branch was not merged with the prototype branch.

### Floorfox publishing detour

The user lacked permission to change Pages settings in JanusWebHub and had authorization in FLOORFOX. A separate clone was made at `C:\projects\BFW_Wegweiser-floorfox`, based on Floorfox's existing `feature/east-wing-prototype` branch. The six static bundle files were fetched from the Janus checkout and cherry-picked, creating a Floorfox-based commit. The Floorfox README was amended to link to the EG page. The resulting Floorfox branch commit is `add4969`.

Floorfox Pages was configured to deploy from `feature/eg-prototype` at the repository root. The Pages deployment completed successfully, and both the EG page and README link were verified online. A 404 screenshot preceded the successful deployment. The Floorfox clone is a separate repository/worktree and was not merged into the Janus branch.

## Continuation point

After the publishing and recordkeeping discussion, the user returned the active checkout to `local/simpler` at `c326569`. This file holds the detailed process history; `docs/working-record.md` retains a brief implementation note with the branch, sources, and provenance caveat. The prototype branch and its build sources remain separate; no merge into `local/simpler` was made in this conversation.

At the time of writing this record, `docs/working-record.md` is modified on `local/simpler`; `.github/`, `AGENTS.md`, and `history-path-inventory.md` are untracked workspace items and were not included in the prototype commit. No content from `history-path-inventory.md` was read or used.

## Movement-network prototype follow-up (2026-10-08)

### Design reasoning

The work began with how one long corridor path should serve its many room portals. The user chose a shared backbone between the corridor-end portals, with a door connector toward each end; the next portal determines which connector is used. For E.09 and E.20, the user specified equal 45-degree connectors: project the door onto the backbone, then place attachment points the same perpendicular distance to either side. E.21 and E.24 use the TR1-3 endpoint on the short side because their symmetric attachment would lie beyond the zone.

The connectors and intervening backbone form one segment between a portal pair; junctions do not add route transitions. Authored geometry must determine both displayed path and route distance, so the route search can choose using the distance people would follow. The display-only alternative was set aside because it would leave Euclidean costs in route selection. The scope was incremental: author `E.flur-tr1-1`, retain Euclidean segments for zones without movement data, and reject an incomplete network in an authored zone.

### Prototype implementation

The user supplied `web/eg-connectivity-graph.json` as a copy of the review connectivity graph, leaving the original review files unchanged. The user designed and authored the movement layout. I calculated the junction coordinates from existing portal points with a one-off PowerShell command, then added the resulting network data to the copy; no reusable coordinate-generation script was created. The prototype representation uses an ordered backbone, named junction points, and two connector references for each room portal. It was not established as a project-wide format.

`src/build_routing_graph.py` reads that copy and rebuilds the routing graph. The user chose a full rebuild so its output could be compared with the existing browser graph before replacement, rather than silently patching the derived graph. The compiler finds one shortest authored path per target-zone portal pair and sums its length for `distance_m`; other crossable zones retain Euclidean segments. The browser's portal-chain route table, `web/eg-routes.json`, was semantically unchanged. The compiler output was directed to the canonical `web/eg-routing-graph.json`; the original review files were left untouched. The `docs/data/graph_format.md` edit made during development was reverted, so the prototype format remains local to these files.

The user requested a readable comparison because the raw graph diff was unwieldy. `src/compare_routing_graphs.py` generates a local HTML report grouped by graph path and portal pair, with independent filters for target-zone segments and the zone's movement property. Before replacement, the report showed 298 changed portal-pair segments plus the new movement property, with no differences elsewhere; two of the 300 target pairs were unchanged. After the new graph replaced the old one, a fresh comparison showed no differences. The user then deleted the temporary candidate graph and report.

`web/movement-lines-tr1-1.svg` visualizes the full corridor and the E.09-to-E.20 route as two connectors plus the intervening backbone. It references the existing `web/assets/bfw-eg.svg` through an SVG viewBox window. A small HTML preview was added because VS Code's direct SVG view did not consistently show that linked background.

### Validation and limits

The first compiler output included an empty `segments.exterior` entry. The user identified the rule violation; the compiler now omits exterior segments and tests that behavior. It also validates finite numeric input and network references, and rejects movement data on exterior or non-crossable zones. Focused compiler tests and the full Python suite passed. The rebuilt graph contains 300 target-zone portal-pair segments; the E.09-to-E.20 segment is 20.23 m.

The prototype does not verify that authored paths stay inside zone boundaries or avoid obstacles; its connectivity input does not contain zone polygons for that check. It also defaults missing routing costs and variants to empty cost maps and `standard: []`. That matches the current prototype data, but future non-default settings stored only in the routing graph would need an explicit configuration source or preservation step. The source graph remains unverified, and a full navigation-app route interaction after graph replacement was not recorded.
