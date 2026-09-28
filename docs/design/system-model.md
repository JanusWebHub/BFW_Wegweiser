# System model

This is a relationship view, not a sequence of processing steps. The [rulebook](../rulebook.md) defines these terms and their constraints.

```mermaid
flowchart LR
Z[Zones] -->|joined by| P[Portals]
P -->|paired within a zone| S[Segments]
P -->|crossed in a direction| T[States]
S --> R[Route]
T --> R
```

A route alternates zones and portals. Its directed states describe crossings; its segments describe travel between successive portals within a zone. The search finds a lowest-cost route between start and target zones.
