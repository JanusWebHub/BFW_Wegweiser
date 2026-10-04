# Operation flow

The browser uses an already built dataset and plan. Route lookup is not graph search.

```mermaid
flowchart LR
A[Navi-user enters start and destination] --> B[Resolve each to one navigable zone]
B --> C[Look up precomputed route]
C --> D[Render route on plan and give directions]
```

Input resolution may require correction or disambiguation and excludes non-navigable zones. Lookup may return an unreachable result. The guidance is static: the browser does not know or track the navi-user's current position.
