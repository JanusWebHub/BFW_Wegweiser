# Documentation guidelines

Conventions for writing commit messages, `README.md` and everything in `docs/`.

## Language

- Identifiers, structure, commit messages and docs in English; comments and
  user-facing strings in German. Node label *values* stay German, since they
  share a namespace with user-typed destination names.

## Devlog

- Entries name the prior state concretely, then the action, then the reason
  only where it is not self-evident. The reason is a fact of history or a
  constraint, never an argument for why the change was good.
- Entries are immutable, including their mistakes. Corrections are new entries
  that identify and explain the error. Never edit an existing entry.

## Commit messages and doc entries

- Every sentence carries information not recoverable from the commit diff or
  from the docs themselves. Length follows from that, never from a target word
  count.

## ADRs

- An ADR records a choice and what it beat. The model itself belongs in
  `axioms.md`, not in an ADR.
- Amendments, three tiers:
  - Decision changed → new ADR; the old one gets `Status: Superseded by ADR N`.
  - Decision abandoned → `Status: Deprecated`, with the reason.
  - Wording wrong but decision sound → correct in place, and record the
    correction in the devlog.

## Cross-references

- No relative links between documents. Refer to other docs by filename in
  backticks.
- Exception: `README.md` may link to `src/` and `web/`.

## Line endings

- CRLF in the working tree; LF in the repository. Development is on Windows,
  where CRLF is native, while LF is the Unix convention Git stores internally.
- `.gitattributes` with `* text=auto` performs the conversion on commit and
  checkout, and applies to every file in the repository, not only to docs.
- Files written by an AI assistant arrive as LF and need converting.
