# Development lifecycle

Development creates the tools, assets, and client. Its order need not match the order in which a finished system builds data.

```mermaid
flowchart LR
A[Model and design] --> B[Shared data contracts]
B --> C[Implement tools and browser]
B --> D[Author plans and configuration]
C --> E[Test with fixtures and verified building data]
D --> E
E --> F[Integrate and release]
F --> G[Maintain and extend]
G --> B
```

Controlled fixtures test changes before and after real plans are available, including when adding buildings or maintaining the program. Verified building data is needed before offering building guidance; fictional fixtures remain test data, not public navigation data.
