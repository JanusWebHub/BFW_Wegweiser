# Zoning Editor

## Purpose And Nature

The zoning editor is a visual, domain-aware modeling application: a specialized 2D CAD editor for indoor-navigation models, with a floor plan as its main working surface. Its closest practical relatives are floor-plan editors, GIS editors and lightweight CAD applications.

The zoning editor incorporates the redline workflow's mechanisms. The zoning author works directly on zones, shared boundaries, portals and movement geometry, with the plan SVG underneath.

The zoning editor is intended to become fully usable without AI assistance. Agents may assist with interpretation, proposals, authorized edits and checks, but must not be necessary to remember or execute the author's decisions.

## Domain-Aware Editing

Editing operates on building-model objects and relationships, not only graphical primitives. Moving a shared boundary differs from independently moving two polygon edges. Creating a portal establishes a crossable portion of a boundary between two zones, not merely a symbol near a wall.

The same model can be inspected spatially, topologically, semantically and historically: geometry, connections, movement permissions, and requested, changed or approved content. These are complementary views, not four separate editors.
