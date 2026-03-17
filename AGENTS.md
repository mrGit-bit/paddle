# AGENTS.md — Codex Execution Rules

Instruction Set Version: 2.2.20  
Last Updated: 2026-03-17

## 1. Authority and File Roles

Authority:

1. Explicit task brief
2. `/docs/PROJECT_INSTRUCTIONS.md`
3. `AGENTS.md`

Document roles:

- `docs/PROJECT_INSTRUCTIONS.md`: compact repository constraints and minimum
  SDD gates.
- `AGENTS.md`: Codex execution behavior, workflow mechanics, and handoff rules.
- `README.md`: repository orientation, architecture context, and owner-doc
  pointers.

If version/date mismatch exists between `PROJECT_INSTRUCTIONS.md` and
`AGENTS.md`, stop and align them first.

## 2. Tool Roles

- Codex CLI is the default tool for spec drafting, planning, implementation,
  tests, and repository changes.
- ChatGPT is not required when Codex CLI can cover the task end to end.
- Use ChatGPT only for pre-spec clarification of ambiguous work, project
  technology or design questions, governance decisions, development-concept
  clarification, or screenshot review.

## 3. Execution Workflow

Follow the SDD flow defined in `docs/PROJECT_INSTRUCTIONS.md`.

Execution rules:

1. Verify the current branch before development or implementation work.
2. Use the latest approved non-release spec and plan for the current task as
   the active-work artifacts.
3. Treat `specs/release-*.md` and `plans/release-*.md` as historical release
   records only.
4. Do not implement before both current active-work artifacts are approved.
5. Keep implementation aligned with the approved scope; no scope expansion.

Quality checkpoints:

- `/review` is a fast targeted review checkpoint on the relevant draft, diff, or
  scoped change set.
- `audit` is for deeper governance, security, reuse, and maintainability
  inspection.
- Use either when useful, prefer `/review` first when both make sense, and fix
  accepted findings before moving past the relevant gate or closing the work.

Post-release:

- After a successful tagged release and back-merge from `main` to `develop`,
  perform any pending spec/plan consolidation for that release before starting
  new SDD work.

## 4. Handoff Requirements

Every implementation response must include:

- Technical Summary
- Files Modified
- Tests added or modified, with command and result summary
- Changelog Entry with the exact text added
- Human readable summary of changes
- 3-6 Manual Functional Checks
- Recommended Commit Message covering the full accumulated uncommitted change
  set since the last commit

Before any commit, push, or closure step:

- Ask whether the user wants to continue developing.
- If not, ask: `Do you want me to proceed with staging changes, committing with
  the recommended commit message, pushing to the remote branch, and closing the
  current development cycle?`

If the user confirms closure:

- Stage, commit, and push in the same flow.
- Reconcile any completed backlog items in `BACKLOG.md` that belong to the
  requested scope by removing them from backlog and ensuring the implemented
  outcome is reflected in `CHANGELOG.md`.
- Keep processing remaining requested-work changes until `git status --short`
  is clean.
- After closure, suggest next steps if relevant.

## 5. Markdown Handling

For changed Markdown files:

- Do not add `markdownlint-disable` directives unless explicitly requested.
- Keep `MD022` and `MD032` compliant.
- Treat `MD013` as non-blocking.
- `CHANGELOG.md` may keep an `MD024` disable because repeated Keep a Changelog
  category headings are intentional there.
- Preserve authoritative generated text unless a structural correction is
  required.
- Run markdownlint on changed Markdown files when available and fix violations
  in the same change set except `MD013`.
