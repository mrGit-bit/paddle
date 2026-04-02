# AGENTS.md — Codex Execution Rules

Instruction Set Version: 2.3.4  
Last Updated: 2026-04-02

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
- Keep `docs/PROJECT_INSTRUCTIONS.md` compact enough for ChatGPT Project
  instructions: target under 7000 characters and never above 7800.
- If a governance addition would exceed that budget, keep only the portable
  rule in `docs/PROJECT_INSTRUCTIONS.md` and move the detail here or to another
  owner doc instead of expanding the project-instructions file further.

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
  documentation before relying on them in specs, automation, or user
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
2. Use the latest approved non-release spec for the current task as the
   active-work artifact.
3. Treat `specs/release-*.md` as historical release records only.
4. Do not implement before the current active-work spec is approved.
5. Keep implementation aligned with the approved scope; no scope expansion.
6. Loose non-release specs must carry explicit tracking metadata:
   `Status: approved|implemented` and `Release tag: unreleased`.
   Use `Status: approved` for approved work that has not yet completed its
   development cycle closure. Move a loose spec from `approved` to
   `implemented` only when the scoped work is done and that spec's
   development cycle is being closed. Use `Status: implemented` for work whose
   development cycle was closed on `develop` but is not yet shipped. Reserve
   `Release tag` for shipment tracking only. Before release
   consolidation, mark only the actually shipped loose files with the target
   `vX.Y.Z` and update them to `Status: shipped`. During consolidation,
   `python scripts/release_orchestrator.py <version>` folds only those
   exact-match files into the shipped release record, reviews the changelog
   section for that release, and keeps that section as a light summary of
   shipped changes. If a planned release never reaches production, do not keep
   a standalone release record for it; roll its unshipped loose files and
   changelog notes into the next production release that actually ships them.
   A loose task must not stay loose once any scoped behavior from that task has
   reached production; consolidate the shipped file for that release, and if
   more work is needed afterward, create a new loose spec for the follow-up
   instead of reopening or extending the shipped file.

Simple-change exception:

- For small, low-risk changes with narrow scope, such as straightforward
  documentation, governance, or repository-guidance edits, Codex CLI may skip
  creating an active-work spec.
- If the requested change is clearly minor and fits that reduced-process path,
  Codex may proceed directly without an extra confirmation turn.
- If the task grows beyond that narrow change set, stop using the exception and
  return to the normal approved-spec workflow.

Planning behavior:

- In `/plan` or any planning-only workflow, explore first, then bias toward a
  question-heavy planning loop before finalizing the plan.
- Do not jump straight from exploration to a completed plan when meaningful
  product, UX, or implementation preferences could still be confirmed with the
  user.
- After exploration, summarize the discovered context and ask follow-up
  questions that lock preferences or tradeoffs even when a reasonable default
  seems likely.
- Prefer at least one round of preference-locking questions for non-trivial
  planning work and a second round when implementation choices would otherwise
  be left to inference.
- Only skip those extra planning questions when the remaining decisions are
  truly mechanical or already explicitly settled by the user or repository
  governance.

Quality checkpoints:

- `/review` is a fast targeted review checkpoint on the relevant draft, diff, or
  scoped change set.
- `audit` is for deeper governance, security, reuse, and maintainability
  inspection.
- Evaluate whether `/review` or `audit` should be used for each non-trivial spec
  or implementation task, especially when the target flow already exists.
- Prefer `/review` first when both checkpoints could fit the scope.
- If neither checkpoint is used, say so explicitly in the working response and
  give a brief reason for skipping it or discarding it for that scope.
- Only surface findings that are medium or high severity; do not raise low
  severity findings as active review/audit findings.
- Before continuing past the relevant gate, explicitly ask the user whether
  each surfaced finding should be addressed or discarded, then update the
  review/audit record accordingly.
- Do not fix findings directly just because they were found; implement fixes
  only after the user chooses to address them.
- When Django model/schema changes are introduced, generate and apply the
  required migrations in development before treating the task as complete.

Post-release:

- After a successful tagged release and back-merge from `main` to `develop`,
  perform any pending spec consolidation for that release before starting new
  SDD work. Use the shipped production release as the historical record: only
  loose files explicitly marked with the shipped `vX.Y.Z` are consolidated for
  that release. Review the changelog section for that release in the same step
  and rewrite it as a simple, light summary when needed. When a planned
  version never entered production, its unshipped loose spec files and notes
  must be absorbed into the next production release that actually shipped them
  instead of being archived under the non-shipped version. Post-release
  reconciliation is not complete while any loose non-release file still
  describes behavior already in production; retag those files to the shipped
  version if needed, consolidate them immediately, and delete the superseded
  loose files before new SDD work begins.

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
- Exception: if the user explicitly says `close cycle`, `close specification`,
  or gives equivalent direct closure authorization, treat that as approval to
  stage, commit, and push without asking the extra confirmation question.

If the user confirms closure:

- Stage, commit, and push in the same flow.
- Run closure git operations sequentially, never in parallel; `git add`,
  `git commit`, and `git push` must each finish before the next one starts.
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
- Keep `CHANGELOG.md` entries scannable by prefixing bullets with stable domain
  categories when a release mixes different kinds of work, for example
  `UI/UX`, `Governance`, `Release`, `Backend`, `Data`, `Mobile`, `Tests`, or
  `Docs`.
- Active-work specs should capture only the scope, constraints, and checks
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
