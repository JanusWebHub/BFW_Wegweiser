---
name: wegweiser-history-review
description: 'One-time review of historical Wegweiser Copilot and Claude conversations across current and former workspace associations. Produce a proposed, source-linked record of project direction, confirmed decisions, corrections, and unresolved questions.'
user-invocable: true
disable-model-invocation: true
---

# Wegweiser History Review

All investigation must be read-only. Git commands that only inspect history and repository state are allowed, including `log`, `show`, `diff`, `branch --list`, and `for-each-ref`. Use `git --no-optional-locks` for inspection to avoid optional writes such as index refreshes. Do not modify the worktree, index, refs, configuration, or Git objects; fetch, pull, checkout/switch, reset, and other state-changing operations are prohibited. Do not reindex or synchronize histories, or run commands that write files.

The sole permitted write is the review file at the project root, `history-review.md`, through an edit tool. If it already exists, obtain explicit approval before replacing it. Do not create, edit, remove, or move any other files. Permission mode does not expand this authorization.

This is a temporary, explicitly invoked workflow for a one-time review, not routine catch-up. Keep it available for user-directed revisions until the user considers the review complete. Do not automatically repeat the review or remove this skill.

History-location discovery is complete and the review purpose is agreed. Use [history-path-inventory.md](../../../history-path-inventory.md) to locate relevant project history across current and former workspace associations, including workspace-only work.

Review the substantive project history in local Copilot and Claude conversation stores and existing exports, not merely recent sessions or existing summaries. Examine the full locally available Git history across all branches. Use supplied commits as anchors, not an exhaustive list; begin with commit summaries and changed-file lists, inspecting substantive diffs where needed. Indexes help locate conversations; logs and snapshots are supplementary only when needed. Account for duplicate conversations, continuations, merges, and replayed commits. Other discovered workspace names remain candidates until their project relevance is established.

Create a proposed distilled, source-linked review at the project root as `history-review.md`, not a comprehensive conversation archive. If that file already exists, ask before replacing it. Reconstruct the project's purpose, conceptual model, reasoning, major breakthroughs, turning points, and distinct phases, including what changes of direction superseded. Organize the synthesis around project substance and evolution, not recent activity or an inventory of open items.

The user's latest explicit confirmation or correction governs each subject; newer assistant proposals do not override earlier confirmed decisions. Recent confirmations govern interpretation, not historical coverage. Git records changes; conversations establish intent and approval. Distinguish confirmed and superseded decisions, provisional ideas, and assistant recommendations. Treat the EG prototype as a bounded exception, mentioning it only where necessary to prevent confusion about the enduring direction.

Retain source paths, session IDs, dates, and selected excerpts where needed to make conclusions checkable. Do not silently resolve conflicting or incomplete evidence; ask when relevant intent or facts remain uncertain. Record material coverage limitations in the review.

Leave source histories untouched. The review is a proposal for the user's assessment, not authoritative project guidance. Do not update project documents, agent instructions, or skills, or implement recovered proposals without separate approval.

Keep the chat brief; put the substantive review in the file.
