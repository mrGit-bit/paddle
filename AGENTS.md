# AGENTS.md — Codex Execution Rules

Instruction Set Version: 2.2.23  
Last Updated: 2026-03-27

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
- For external-tool or integration features that depend on current support,
  discovery rules, authentication behavior, configuration paths, or versioned
  capabilities, verify the live tool behavior or current official
  documentation before relying on them in specs, plans, automation, or user
  guidance.
- This applies to Codex CLI, GitHub CLI, GitHub Actions behavior, SSH tooling,
  Codespaces integration, MCP wiring, and any similar dependency needed to
  complete the requested work.
- Do not assume a discovery path, config path, auth flow, or checked-in
  integration file works just because it appears in a draft spec or repository
  file. Validate the active tool version and the current environment first.

## 3. Execution Workflow

Follow the SDD flow defined in `docs/PROJECT_INSTRUCTIONS.md`.

Execution rules:

1. Verify the current branch before development or implementation work.
2. Use the latest approved non-release spec and plan for the current task as
   the active-work artifacts.
3. Pair loose specs and plans by shared `Task ID` tracking metadata and
   explicit `Plan` / `Spec` references instead of filename similarity alone.
4. Treat `specs/release-*.md` and `plans/release-*.md` as historical release
   records only.
5. Do not implement before both current active-work artifacts are approved.
6. Keep implementation aligned with the approved scope; no scope expansion.
7. Loose non-release specs and plans must carry explicit `Release tag`
   tracking metadata. Post-release consolidation normally uses the matching
   shipped production release tag. If a planned release never reaches
   production, do not keep a standalone release record for it; roll its
   unshipped loose files and changelog notes into the next production release
   that actually ships them.

Simple-change exception:

- For small, low-risk changes with narrow scope, such as straightforward
  documentation, governance, or repository-guidance edits, Codex CLI may skip
  creating spec and plan files.
- Codex must first ask a confirmation question and receive approval for that
  reduced-process path before editing files.
- If the task grows beyond that narrow change set, stop using the exception and
  return to the normal approved spec and plan workflow.

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
  new SDD work. Use the shipped production release as the historical record:
  when a planned version never entered production, its unshipped loose
  spec/plan files and notes must be absorbed into the next production release
  that actually shipped them instead of being archived under the non-shipped
  version.

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
- Backlog reconciliation is owned by development-cycle closure, not by release
  automation unless a release workflow explicitly says otherwise.
- Keep processing remaining requested-work changes until `git status --short`
  is clean.
- After closure, suggest next steps if relevant.

## 5. Markdown Handling

For changed Markdown files:

- Keep new or rewritten Markdown light and schematic by default.
- Prefer short sections, direct bullets, compact summaries, and no duplicate
  restatement.
- `CHANGELOG.md` should record shipped outcomes, not process narration.
- Loose specs/plans should capture only the scope, constraints, and checks
  needed to execute the task.
- Consolidated release files should be compact provenance records, not embedded
  copies of prior source files.
- Do not add `markdownlint-disable` directives unless explicitly requested.
- Keep `MD022` and `MD032` compliant.
- Treat `MD013` as non-blocking.
- `CHANGELOG.md` may keep an `MD024` disable because repeated Keep a Changelog
  category headings are intentional there.
- Preserve authoritative generated text unless a structural correction is
  required.
- Run markdownlint on changed Markdown files when available and fix violations
  in the same change set except `MD013`.
