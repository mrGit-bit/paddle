# Spec 013: README Changelog Alignment and Codex Guidance

## Functional Goal

Refresh `README.md` so it reflects the latest documented project state from
`CHANGELOG.md` and becomes a practical, high-signal reference for Codex CLI
agents working in this repository.

## Scope

### In

- Update `README.md` to reflect the current documented product state in
  `CHANGELOG.md`.
- Remove outdated or contradictory README guidance.
- Make `README.md` more useful for Codex CLI by surfacing stable repository
  context, architecture boundaries, important workflows, and safe editing
  rules.
- Keep the README focused on current supported surfaces and current project
  conventions.

### Out

- Changes to application code, tests, workflows, or runtime behavior.
- Changes to `CHANGELOG.md` content beyond using it as the source to align the
  README.
- Changes to governance files unless an inconsistency is discovered that blocks
  accurate README authoring.

## UI/UX Requirements

- Not applicable to product UI.
- The README must be easy to scan for CLI coding agents.
- Headings and lists must remain markdownlint-compliant.

## Backend/Documentation Requirements

- The README must not describe removed DRF/API surfaces as active features.
- The README must not describe outdated version-source rules that contradict
  current code or docs.
- The README should summarize the main latest released and unreleased project
  changes at a high level without duplicating the full changelog.
- The README should clearly identify where Codex CLI should look first for
  governance, architecture, and feature behavior.

## Data Rules

- `CHANGELOG.md` is the source for recent documented changes.
- `README.md` should summarize, not duplicate, changelog sections, containing
  only relevant changes for AI agents.
- Stable repository facts included in the README must match the current
  codebase and governance docs.

## Reuse Rules

- Reuse terminology and constraints already defined in
  `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` where relevant.
- Prefer concise summaries over restating large sections of governance files.
- Preserve any still-valid project-specific context already present in
  `README.md`.

## Acceptance Criteria

1. `README.md` reflects the latest main unreleased and recently released project
   changes documented in `CHANGELOG.md`.
2. `README.md` no longer contains materially outdated guidance that conflicts
   with the current changelog or repository state.
3. `README.md` includes a clearly useful section for Codex CLI agents with
   repository navigation and editing guidance.
4. The README remains concise, scannable, and markdownlint-compliant.
5. No non-documentation files are changed for this task.

## Manual Functional Checks

1. Open `README.md` and confirm the recent changes summary mentions the current
   unreleased fix and the latest major documented product/governance changes.
2. Verify the README’s architecture and workflow guidance matches
   `docs/PROJECT_INSTRUCTIONS.md` and does not describe the removed DRF/API
   surface as active.
3. Verify a Codex CLI agent could identify the main app areas, rules, and
   important files from the README without needing the full changelog first.
4. Run markdownlint on the changed Markdown files if available and confirm no
   `MD022` or `MD032` violations remain.

## Files Allowed to Change

- `README.md`
- this spec file
- the corresponding plan file

## Files Forbidden to Change

- `CHANGELOG.md`
- application code under `paddle/**`
- GitHub workflows
- test files
- mobile app code
