# System design

The rulebook defines the model theoretically, covering its terms and their relationships. This document specifies the current system design by making the system-level design decisions that conform strictly to the model, using tools such as clarifying and exemplifying rulebook terms and resolving what the rulebook deliberately leaves open.

## 1. Modeling pipeline

The system implements a human-in-the-loop, computer-assisted modeling pipeline with two complementary representation types:

- visual representations: architectural plans, simplified floor plans, spatial routing plans, and graph visualizations
- machine-readable symbolic representations: serialized graph models containing nodes, edges, and attributes

1. Architectural plans are interpreted into a machine-readable adjacency graph.
2. The plans and adjacency graph are used in zoning to produce simplified floor plans and a connectivity graph.
3. The routing graph is constructed from the connectivity graph and serialized.
4. Routes are computed by searching the routing graph and serialized for the browser client.
5. The browser renders routes on the building plan.

## 2. Costs

A special cost is any factor beyond distance that makes a state or segment harder or easier for a person, for example a turn, a door, or a floor change. These factors and their weights are a tuning decision, made when the routing graph is constructed from the connectivity graph.
