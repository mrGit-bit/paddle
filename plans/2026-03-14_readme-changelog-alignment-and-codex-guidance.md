# README Changelog Alignment and Codex Guidance

## Context

- The current `README.md` contains outdated guidance and does not reflect the
  most recent documented changes in `CHANGELOG.md`.
- The README should become a practical entry point for Codex CLI agents so they
  can quickly identify repository rules, app areas, and safe editing
  boundaries.
- Files/components read first during discovery:
  - `specs/013-readme-changelog-alignment-and-codex-guidance.md`
  - `CHANGELOG.md`
  - `README.md`
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `AGENTS.md`

## Spec Reference

- `specs/013-readme-changelog-alignment-and-codex-guidance.md`

## Objectives

- Replace outdated README content with a concise, accurate project overview.
- Summarize the latest unreleased and recent released changes that matter for
  readers and Codex CLI agents.
- Add clear Codex-oriented navigation and editing guidance without duplicating
  full governance documents.
- Keep the result markdownlint-compliant and documentation-only.

## Scope

### In

- Rewrite or substantially restructure `README.md`.
- Align README statements with `CHANGELOG.md`, `docs/PROJECT_INSTRUCTIONS.md`,
  and current repository conventions.
- Validate changed Markdown files with markdownlint if available, otherwise
  perform a manual markdown rule pass.

### Out

- Any application code, workflow, or runtime behavior change.
- Any edits to `CHANGELOG.md` other than reading it as the source of recent
  changes.
- Any governance-file change unless a blocking inconsistency is discovered.

## Risks

- Risk: The README may over-copy the changelog instead of summarizing it.
  Mitigation: Keep the recent changes section short and focused on high-signal
  items only.
- Risk: README guidance may drift from current governance language.
  Mitigation: Cross-check `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` before
  editing.
- Risk: Markdown structure may introduce lint violations.
  Mitigation: Keep heading/list spacing explicit and run markdownlint if
  available.

## Files Allowed to Change

- `README.md`
- `specs/013-readme-changelog-alignment-and-codex-guidance.md`
- `plans/2026-03-14_readme-changelog-alignment-and-codex-guidance.md`

## Files Forbidden to Change

- `CHANGELOG.md`
- `paddle/**`
- `.github/workflows/**`
- test files
- mobile app code

## Proposed Changes (Step-by-Step by File)

- `README.md`
  - Change: Rewrite the document into a concise project guide with current
    architecture, supported surfaces, recent documented changes, important
    repository paths, and Codex editing guidance.
  - Why: The current README is outdated and not optimized for Codex CLI usage.
  - Notes: Keep it summary-oriented, not a changelog duplicate.

- `specs/013-readme-changelog-alignment-and-codex-guidance.md`
  - Change: Keep the approved spec accurate and lint-clean.
  - Why: The spec is part of the required SDD workflow and should remain
    internally consistent.
  - Notes: Only minimal corrections if needed.

- `plans/2026-03-14_readme-changelog-alignment-and-codex-guidance.md`
  - Change: Record the approved execution plan for this documentation task.
  - Why: Required by repository workflow before implementation.
  - Notes: No product code in plan mode.

## Plan Steps (Execution Order)

- [ ] Review `CHANGELOG.md`, `README.md`, and governance docs for the exact
  current project state to reflect.
- [ ] Rewrite `README.md` with current product summary, recent changes,
  repository map, and Codex-specific guidance.
- [ ] Validate the changed Markdown files and fix any markdownlint or manual
  structure issues before delivery.

## Acceptance Criteria (Testable)

- [ ] `README.md` mentions the latest unreleased fix and recent major released
  changes relevant to repository contributors.
- [ ] `README.md` no longer includes materially outdated or contradictory
  guidance.
- [ ] `README.md` provides a clear Codex CLI section describing where to look
  and what boundaries to respect.
- [ ] Only documentation files in scope are changed.
- [ ] Changed Markdown files satisfy markdown structure requirements, including
  `MD022` and `MD032`.

## Validation Commands

```bash
markdownlint README.md \
  specs/013-readme-changelog-alignment-and-codex-guidance.md \
  plans/2026-03-14_readme-changelog-alignment-and-codex-guidance.md
```

## Manual Functional Checks

1. Open `README.md` and confirm it summarizes the current unreleased workflow
   fix and latest major recent releases at a high level.
2. Verify the README points Codex CLI agents to the correct governance files
   and key repository areas.
3. Verify the README does not describe removed DRF/API endpoints as part of the
   active product surface.
4. Verify the README’s architectural guidance does not conflict with
   `docs/PROJECT_INSTRUCTIONS.md`.

## Execution Log

- 2026-03-14 22:25 UTC — Spec created.
- 2026-03-14 22:29 UTC — Spec approved.
- 2026-03-14 22:30 UTC — Spec corrected for scope formatting and markdown
  wrapping.
- 2026-03-14 22:30 UTC — Plan created.

## Post-Mortem / Improvements

- What worked well
  - The task is documentation-only, so the scope can stay tight.
- What caused friction
  - The existing README mixes human onboarding and agent instructions with some
    outdated repository assumptions.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`
  - `/AGENTS.md`
  - `/plans/TEMPLATE.md`
  - No governance template changes are proposed at this time.
