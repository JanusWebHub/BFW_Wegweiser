---
name: wegweiser-catch-up
description: 'Catch up on Wegweiser project intent and recent work before continuing. Search Copilot session history for repository and workspace evidence, including non-repository files, decisions, approvals, corrections, and unresolved questions; compare with current files.'
argument-hint: 'Optional topic, file, branch, or time range'
---

# Wegweiser Catch-Up

Build an evidence-based orientation for the current Wegweiser workspace. This is a read-only workflow. Do not edit files unless the user separately asks.

## Procedure

1. Establish the scope from the active editor/workspace: record the workspace path, repository identity and remote if present, current branch, and worktree state. Do not assume the repository and workspace contain the same files.
2. Read the relevant current project instructions and documents. Start with [AGENTS.md](../../../AGENTS.md) and [README.md](../../../README.md); consult [working-record.md](../../../docs/working-record.md), [rulebook.md](../../../docs/rulebook.md), [system-design.md](../../../docs/system-design.md), and [implementation-plan.md](../../../docs/implementation-plan.md) according to the question. Inspect current source files to establish what is implemented.
3. Search session history in both scopes, then combine and deduplicate the results. Include the available Copilot/Chronicle session index and relevant exported conversation transcripts in the workspace, such as files under `transcripts/` or historical assistant folders. Do not imply that a Copilot-only search covers other assistants' sessions.
   - Repository scope: sessions associated with this repository, across branches unless the user narrows the request.
   - Workspace scope: sessions whose local workspace path or recorded file paths match the active workspace, including files not tracked by Git and sessions without repository metadata.
   Search user and assistant turns, not summaries alone. If workspace path metadata or file records are absent, search conversation text for the active workspace path and known workspace-only folder/file names. Start with recent sessions, then search older relevant sessions when the topic concerns a lasting decision or unresolved question. Follow the available Chronicle/session-history instructions for the active index.
4. Read enough surrounding turns to establish whether a statement was a request, an explicit decision, a provisional idea, an assistant proposal, or an unresolved question. Look for later corrections or superseding decisions. Silence is not approval. Record session dates and IDs for material conclusions.
5. Compare historical intent with the current documents and worktree. Session history is essential evidence for decisions that may never have been written into project files. Current files establish implementation state, not the complete decision history. If evidence conflicts, present the conflict with its sources and dates; do not silently reconcile it.
6. Report the sources and scopes searched and any indexing limits. In particular, cloud history may omit the local workspace path, and file-path records may be absent. If workspace-only coverage cannot be verified, say so plainly; do not present repository-only or Copilot-only results as a complete workspace/session-history search.

## Communicate Understanding

Do not presume your understanding is complete. Ask rather than silently assume when intent or relevant facts are uncertain. Give a terse, request-specific demonstration of your understanding for the user to assess. Mention conflicting sources or limitations only when they materially affect the task. Do not suggest next steps unless asked.
