# Spec 016: Changelog Backfill and Governance Clarification

## Functional Goal

Backfill `CHANGELOG.md` so `## [Unreleased]` documents the recent README and
governance changes already committed, and clarify governance so future
documentation/governance changes are not incorrectly treated as changelog-
exempt unless they are truly formatting-only.

## Scope

### In

- Update `CHANGELOG.md` under `## [Unreleased]` with the missing recent
  documentation/governance changes.
- Update `docs/PROJECT_INSTRUCTIONS.md` to clarify changelog expectations for
  documentation and governance changes.
- Update `AGENTS.md` with matching changelog-clarification language.
- Keep governance metadata synchronized across `docs/PROJECT_INSTRUCTIONS.md`
  and `AGENTS.md`.

### Out

- Changes to product code, tests, workflows, or runtime behavior.
- Rewriting older released changelog sections.
- Broader governance changes unrelated to changelog expectations.

## UI/UX Requirements

- Not applicable to product UI.

## Backend/Documentation Requirements

- `CHANGELOG.md` must describe the recent README refresh and governance updates
  in the `Unreleased` section.
- Governance must clearly distinguish `formatting-only` changes from
  documentation/governance changes that still require changelog entries.
- Governance wording in `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` must
  remain aligned.

## Data Rules

- The new changelog entry must match the already committed behavior/process
  changes.
- Governance metadata (`Instruction Set Version` and `Last Updated`) must match
  between `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md`.

## Reuse Rules

- Reuse the existing changelog-discipline language instead of adding a separate
  duplicate policy section.
- Keep edits minimal and localized to the missing changelog entry and the
  governance wording needed to prevent the same misclassification.

## Acceptance Criteria

1. `CHANGELOG.md` `## [Unreleased]` includes the recent README and governance
   changes from the last documentation/governance cycle.
2. `docs/PROJECT_INSTRUCTIONS.md` clarifies that documentation/governance
   changes still require changelog updates unless they are truly
   formatting-only.
3. `AGENTS.md` contains the same clarification.
4. Governance metadata remains synchronized between the two governance files.

## Manual Functional Checks

1. Read `CHANGELOG.md` `## [Unreleased]` and confirm it now mentions the README
   refresh plus the recent governance rule changes.
2. Read the changelog-discipline rule in both governance files and confirm they
   now explicitly exclude only truly formatting-only changes.
3. Confirm the wording makes documentation/governance changes changelog-worthy
   unless they are formatting-only.
4. Confirm governance version/date metadata matches exactly between the two
   files.

## Files Allowed to Change

- `CHANGELOG.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
- this spec file
- the corresponding plan file

## Files Forbidden to Change

- `README.md`
- application code under `paddle/**`
- GitHub workflows
- test files
