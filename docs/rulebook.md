# Rulebook

This rulebook defines the project's navigation model and is its source of truth. Every project file that concerns the navigation model must conform to it.

## 1. Structural elements and topology

Defines the spaces, zones, boundaries, portals, and segment relations that structure navigation.

### 1.1

Architectural and simplified floor plans are two-dimensional representations of the building. The simplified plan is derived from the architectural, retaining only features relevant to navigation.

### 1.2

A zone is a two-dimensional space that partitions the simplified floor plan without gaps or overlaps.

A zone may be crossable or non-crossable. A non-crossable zone may be a route's start or target, but cannot be passed through.

### 1.3

A separator is a fixed, non-crossable division between two spaces in the architectural plan.

A boundary is a one-dimensional division between two zones in the simplified floor plan. It may represent a physical separator or be virtual.

### 1.4

A portal represents the crossable portion of a boundary and is drawn in the simplified floor plan as a highlighted section with its midpoint marked. In the navigation model, it is represented by that midpoint.

A portal may correspond to a physical door or other opening between distinct architectural spaces, or to a virtual opening on a virtual boundary.

A portal always joins exactly two zones. Because a boundary is a line, multiple zones may meet at a point but do not share a portal there; each pair of zones has its own shared boundary and portal.

### 1.5

A segment is a traversal through one zone, from one portal to another. It lies in the zone’s interior.

### 1.6

The exterior is a single zone surrounding the building. A route may begin or end there but never cross it.

## 2. Movement geometry and constraints

Defines walkable space, obstacles, movement zones, movement lines, and segment geometry.

### 2.1

A zone divides into a walkable part and a non-walkable part.

### 2.2

An obstacle is a fixed obstruction in the non-walkable part of a zone; routes neither end at nor pass through it.

### 2.3

The movement zone is the circulation space within the walkable part.

### 2.4

A movement line is a designer-drawn representation of the path people actually take through a movement zone.

## 3. Zoning and graph construction

Defines how the simplified floor plans are produced from the architectural plans, and how the adjacency, connectivity, and routing graphs are derived.

### 3.1

The adjacency graph is the machine-readable abstraction of the spaces and separators in the architectural plans. Its nodes are spaces and its edges are separators.

### 3.2

Zoning is the process of converting spaces and separators into zones and boundaries and creating portals, movement zones, and movement lines that form essential elements of the navigation model.

The connectivity graph is produced alongside the simplified floor plans. Its nodes are zones and its edges are portals.

Every zone must have at least one portal, and its portals must be mutually reachable without obstruction.

### 3.3

The routing graph is constructed from the connectivity graph using movement geometry and routing decisions. Its nodes are portals, and its edges are segments.

Marking additional zones as non-crossable creates a routing variant in which those zones remain reachable but cannot be passed through.

## 4. Queries and search

Defines queries, states, routes, costs, and the search for lowest-cost routes.

### 4.1

A query is a user's request for navigation from one location to another. The user specifies the start and target by room number, such as `E.62`. FLOORFOX resolves each room number to a known zone; precise positions within those zones are not represented.

### 4.2

A state is a directed transition from one zone through a portal into another zone. It is written `zone_from | portal | zone_to`. A state may be assigned special costs.

### 4.3

A segment between two consecutive states is written `portal | zone | portal`. A segment may be assigned special costs in addition to its distance cost.

### 4.4

A route is an alternating sequence of zones and portals, beginning with the start zone and ending with the target zone. It is written `zone | portal | zone | ... | portal | zone`.

Total route cost is the sum of distances and special costs from its segments and states.

### 4.5

The search is multi-source and multi-target and returns the route with the lowest total cost. The routing graph is searched from the outbound states of the start zone to the inbound states of the target zone.

### 4.6

The search produces a portal chain. The portal chain determines the zone sequence and the zone of each segment. The route is interpreted as navigation instructions and rendered on the building plan.

### 4.7

Room numbers used as user input must follow the building's printed numbering convention. The standard form is an uppercase floor or area code, a period, and one or more digits, for example `E.62`. A room number may include an additional printed suffix when the building uses one, such as `E.54a`.

Room numbers must map unambiguously to exactly one zone. Unknown or ambiguous room numbers must produce a clear correction message and must not be passed to route search. The interface must label the two inputs clearly as start room and destination room.

### 4.8

Users may also search for a named destination when a room number is not the most obvious description. A named destination may be a room title, facility, or common place, such as `Technisches Training`, `Speisesaal`, `Sporthalle`, `Cafe`, or `Toilette`. These names are aliases for one or more known zones; they do not replace the official room number as the canonical identifier.

The start and destination controls must be free-text search fields, not dropdown menus containing every room. The normal workflow is to type a room number such as `E.62`. The same field must also accept a named destination. While the user types, it may show a short list of relevant matches, limited to the entered text and never presented as the complete room inventory. Suggestions should show the official room number together with the name, for example `E.62 - Technisches Training`.

The interface may provide a small `Popular destinations` chooser for important places that users are likely to recognise by name, such as `Cafe`, `Speisesaal`, `Sporthalle`, and `Toilette`. On a large screen this may be a short row of buttons; on a small screen it may be a compact menu containing only these curated destinations. It must remain short and must not become a second room directory. Selecting a destination that refers to multiple zones, such as `Toilette`, must open a second small choice showing distinguishable locations, for example by floor or nearby room, before route search begins. Every typed search or quick choice must resolve to exactly one zone before route search begins.

## 5. Usage analytics and user feedback

FLOORFOX must collect enough anonymous usage data to improve navigation while respecting the privacy of the people using it. Analytics are stored in a database and are evaluated in aggregate; they must not be used to identify or profile individual users.

### 5.1

Each navigation attempt may record:

- the date and time bucket of the request, not an exact timestamp when that is unnecessary;
- the start zone and target zone;
- the resulting route as a sequence of zones and portals;
- whether a route was generated and displayed successfully;
- whether no route could be generated or displayed;
- an optional anonymous session identifier that expires after a short, defined period and cannot be used to identify a person.

The database must not store names, email addresses, exact device identifiers, precise location data, or other information that can identify a user.

FLOORFOX must not claim to know whether a user followed a displayed route, reached the destination, abandoned the route after it was displayed, or encountered a problem while walking. No walking trace or continuous location tracking is part of the system.

### 5.2

After a route has been displayed, FLOORFOX may quietly offer feedback in the existing result view, for example as a small non-blocking prompt below the map and instructions: `Was FLOORFOX useful? Rate 1-5` with a nearby `Report an issue` link. The issue link may expand a short inline text field only after the user selects it. The prompt must not open a modal, take focus, cover the route, or prevent the user from leaving. It must be easy to dismiss and must never interrupt, obscure, delay, or repeatedly prompt the user during navigation. It should be shown at most occasionally according to a defined frequency limit.

- `1` = not useful;
- `2` = slightly useful;
- `3` = partly useful;
- `4` = useful;
- `5` = very useful.

The user may select one rating from 1 to 5 with one simple action. The `Report an issue` action must provide a short optional text field with a clear `Send` and `Cancel` or `Skip` choice. The text field must have a defined length limit suitable for a short message. The rating, issue report, and any comment must be optional and must not block navigation. Text reports must be reviewed and stored subject to the project's privacy and retention rules.

### 5.3

Feedback must be associated with the relevant navigation attempt and, where possible, with its start zone, target zone, route, and route segments. This makes it possible to detect whether self-reported low ratings or issue reports cluster around a particular path, portal, zone, or destination without identifying the person who submitted the feedback. A rating or issue report is the user's report of their experience, not proof that the route was followed or that a specific location caused the problem.

### 5.4

The analytics database must support these aggregate statistics:

- number of navigation requests over time;
- most frequently requested start and target zones;
- most frequently used routes, portals, and zone transitions;
- route generation and display success rates;
- requests for which no route could be generated or displayed;
- average usefulness rating and rating distribution;
- usefulness rating by route, route segment, portal, start zone, and target zone;
- locations with repeated low ratings, repeated route-generation failures, or unusually high request counts.

Statistics must be based on a sufficiently large group of requests before they are shown, so that individual feedback cannot be inferred.

### 5.5

The collected data must be available to authorised project maintainers through a separate, access-controlled analytics dashboard. It must not be exposed in the public FLOORFOX navigation view. The dashboard must visualise the collected data with at least:

- a time-series chart for requests, route generation, and route display success or failure;
- a ranked bar chart for the most used routes and zone transitions;
- a floor-plan heatmap for frequently used or problematic areas;
- a rating distribution chart and average rating by route;
- a filtered table for detailed route, portal, and feedback investigation.

Charts must show the selected time period, sample size, and relevant filters. Visualisations must distinguish missing data from a low rating and must not suggest conclusions unsupported by the available sample.

The dashboard must allow maintainers to filter ratings and comments by time period, start zone, target zone, route, route segment, and portal. It must show the number of responses alongside every rating summary and must hide or aggregate results below the minimum privacy threshold. Raw comments must be visible only to authorised reviewers and must not be presented as proof of what happened after the route was displayed.

### 5.6

Analytics are used to identify navigation problems and guide improvements to zones, portals, movement lines, route costs, and instructions. A low rating or route-generation failure is a signal for investigation, not proof that a particular user followed a route or that a particular route was the cause. Changes based on analytics must be validated with a later comparison of usage and explicitly submitted feedback.
