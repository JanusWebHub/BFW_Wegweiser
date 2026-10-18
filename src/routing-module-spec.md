# routing module specification

This specification is provisional and amendable, and the specification is authoritative for the development of the routing module. Changes to the specification require the explicit confirmation of the human participant.

## purpose

- The routing module turns the connectivity graph of the zoning module into the precomputed routes dataset.
- The optimized and finalized version of the precomputed routes dataset passes from the routing module to the navigation module.

## parts

- The routing module contains a graph compiler, a route computer and a tuning editor.
- The graph compiler produces a routing graph from the connectivity graph and the routing config.
- The route computer consumes the routing graph and produces the precomputed routes dataset.
- The tuning editor is a repurposed version of the zoning editor. It takes the connectivity graph and the zone SVG as input and contains the graph compiler and the route computer, so no separate run of either is needed.

## inputs

- The input of the routing module is the connectivity graph, as the interface between the zoning module and the routing module.

## tuning

- The tuning editor starts with an empty routing config: no costs, and `standard` with empty lists.
- The first routing graph then has distance as its only cost. It exists as data inside the tuning editor, the route computer runs on it directly, and the routes are shown on the zone SVG.
- The zoning author tunes costs and creates variants in the tuning editor and sees the changed routes there.
- Tuning changes only the routing config, which holds costs and variant restrictions.
- A variant only narrows the base graph.
- When finished, the tuning editor saves the routing config, the routing graph and the precomputed routes dataset.
