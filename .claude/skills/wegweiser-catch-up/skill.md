---
name: wegweiser-catch-up
description: 'Catch up on Wegweiser project intent and current implementation before continuing. Use at the start of complex, stale, or unclear work in the Wegweiser repository, or when the user says "catch up", "get oriented", or "what state is this in". Reads the project documents and source files to build an evidence-based orientation.'
argument-hint: 'Optional topic, file, or branch'
---

# Wegweiser Catch-Up

Build an evidence-based orientation for the current Wegweiser workspace. This is a read-only workflow. Do not edit files unless the user separately asks.

## Procedure

1. Establish the scope: record the workspace path, repository identity and remote if present, current branch, and worktree state. Use read-only git commands only (`git status`, `git branch --show-current`, `git remote -v`, `git log`, `git worktree list`). Do not assume the repository and workspace contain the same files.
2. Read the current project instructions and documents. Start with [AGENTS.md](../../../AGENTS.md) and [README.md](../../../README.md). Consult [working-record.md](../../../docs/working-record.md), [rulebook.md](../../../docs/rulebook.md), [system-design.md](../../../docs/system-design.md), and [implementation-plan.md](../../../docs/implementation-plan.md) according to the question. Inspect current source files to establish what is implemented.
3. Distinguish documented intent, confirmed and provisional agreements, planned work, and implemented behavior. Current files may not fully capture the project author's intent, which may exist only in transcripts or session history; consult relevant records when needed to clarify the task. Raise conflicts or uncertainties when they materially affect the task. Check the paths that AGENTS.md names against the files that exist, since the pipeline description may be out of date.

## Communicate Understanding

Do not presume your understanding is complete. Ask rather than silently assume when intent or relevant facts are uncertain. Give a terse, request-specific demonstration of your understanding for the user to assess. Mention conflicting sources or limitations only when they materially affect the task. Do not suggest next steps unless asked.
