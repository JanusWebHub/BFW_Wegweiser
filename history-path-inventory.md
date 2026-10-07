# History Path Inventory

Discovered 2026-10-07 through read-only inspection of paths, filenames and workspace metadata. Conversation substance and database contents were not analyzed. Counts are a discovery-time snapshot, not counts of distinct conversations.

## Workspace Roots

- Current: `C:\projects\wegweiser`
- Former: `C:\Users\deniz\OneDrive\Documents\Projects\BT-IT\P\BT\projekte\wegweiser` (retained empty directory)

## VS Code / Copilot Chat

Base: `C:\Users\deniz\AppData\Roaming\Code\User\workspaceStorage`

| Workspace | Directory under base | Chat files | Debug session directories |
| --- | --- | ---: | ---: |
| Current root | `5793e55528b102434d4f07afba66aafc` | 8 | 8 |
| Former root | `230c63ca2969ecd6ac4b62b269018a21` | 36 | 20 |
| Former root's sibling `wegweiser-denizmertmercan` | `af1cb05df54d72f33992bfec95d5192f` | 4 | 0 |
| Former root's sibling `wegweiser-old-workspace` | `be210c7478d91f74f77d5ac202d49b6f` | 1 | 0 |
| Former root's sibling `wegweiser-east-wing-prototype` | `ce0b3948c7fd57c5b74f1fcf34fb437d` | 5 | 2 |
| `C:\Users\deniz\OneDrive\projects\wegweiser` | `d4a69bab976d1d26273a15e71142ccd1` | 3 | 0 |

Paths relative to each workspace storage directory:

- `workspace.json`: confirmed workspace mapping.
- `chatSessions\<session-id>.jsonl`: session-named chat files, 57 across the six stores.
- `GitHub.copilot-chat\debug-logs\<session-id>\main.jsonl` and `models.json`: where debug records exist.
- `chatEditingSessions\`: editing-session records.
- `state.vscdb` and `state.vscdb.backup`: workspace state databases.

Global base: `C:\Users\deniz\AppData\Roaming\Code\User\globalStorage`

- `github.copilot-chat\session-store.db`, `session-store.db-wal`, `session-store.db-shm`: local session index files.
- `github.copilot-chat\cloudSessions.json` and `copilot.cli.oldGlobalSessions.json`: additional session-related records, contents unexamined.
- `github.copilot-chat\memory-tool\memories\`: Copilot collaboration and writing-preference notes.
- `anthropic.claude-code\session-bookmarks\` and `session-permission-modes\`: Claude extension records, including known Wegweiser session IDs.

## Claude Code

Base: `C:\Users\deniz\.claude\projects`

| Directory under base | Raw JSONL sessions | Adjacent Markdown exports |
| --- | ---: | ---: |
| `c--projects-wegweiser` | 4 | 4 |
| `c--Users-deniz-OneDrive-Documents-Projects-BT-IT-P-BT-projekte-wegweiser` | 12 | 0 |

Both stores contain `memory\`. The former-workspace store also contains session-specific `custom-title.json` and `tool-results\` records.

- `C:\Users\deniz\.claude\file-history\<session-id>\`: 162 snapshot files matched by ID to 9 Wegweiser sessions.
- `C:\Users\deniz\.claude\plans\`: 2 plan files; project association unverified.
- `C:\Users\deniz\.claude.json` and `C:\Users\deniz\.claude\backups\`: global configuration and 5 backups; contents unexamined.

## Copilot CLI

Confirmed former-workspace session base: `C:\Users\deniz\.copilot\session-state\778e3c56-bf61-4f15-b4e1-d494983fe517`

- `workspace.yaml`: metadata identifies the former root, `JanusWebHub/BFW_Wegweiser`, and branch `main`.
- `events.jsonl`, `checkpoints\index.md`, `rewind-file-snapshots\tracking.json`: associated session records.
- `C:\Users\deniz\.copilot\session-store.db` with WAL/SHM companions: separate CLI index, contents unexamined.

## Exports And Other Traces

- `C:\projects\utilities\transcripter\outputs\`: 5 web transcript exports (Markdown and JSON variants).
- `C:\projects\utilities\transcripter\claude\local\code\extract-claude-transcript.ps1`: extractor; documented default writes Markdown beside the source JSONL, with optional project output under `transcripts\`.
- `C:\Users\deniz\AppData\Roaming\Code\User\History\<id>\entries.json`: 81 Wegweiser-associated editor-history records referencing 633 saved versions (48 former-root records, 31 current, 2 other paths).
- `C:\Users\deniz\AppData\Roaming\Code\logs\<run>\window1\exthost\GitHub.copilot-chat\GitHub Copilot Chat.log`: Wegweiser references confirmed in run `20261007T062751`.
- `C:\Users\deniz\AppData\Roaming\Code\logs\<run>\window1\exthost\Anthropic.claude-code\Claude VSCode.log`: Wegweiser references confirmed in runs `20261006T181604` and `20261007T062751`.
- The same log roots contain Git and other diagnostic logs with Wegweiser references; these are not established conversation stores.

## Unverified Or Empty Locations

- `C:\Users\deniz\AppData\Roaming\Code\User\globalStorage\emptyWindowChatSessions\`: 22 files; Wegweiser relevance unverified.
- `C:\Users\deniz\AppData\Roaming\Code\User\profiles\`: state databases in profiles `478f307d`, `5a6fa903`, `5c095cc5`, `5d50aba6` and `builtin\agents`; relevance unverified.
- `C:\Users\deniz\.copilot\sidebar-sessions-state\`: one JSON file; relevance unverified.
- `C:\Users\deniz\AppData\Local\copilot\` and `C:\Users\deniz\.vscode\`: inspected top-level names; no project conversation store established.
- Claude `debug\`, `sessions\` and `session-env\`, and VS Code `Backups\`: no files found.
- `C:\Users\deniz\AppData\Roaming\Code - Insiders` and `VSCodium`: not found.
