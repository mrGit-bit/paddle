# Spec 017: Post-Release Consolidation of SDD Specs and Plans

## Tracking

- Task ID: `consolidate-specs-and-plans-per-tag`
- Plan: `plans/2026-03-15_consolidate-specs-and-plans-per-tag.md`
- Release tag: `v1.5.0`

## Functional Goal

Keep the current SDD workflow unchanged during active development, with one spec
file and one plan file created per SDD as usual, and add a post-release
consolidation rule so that after each successful tagged release and back-merge
from `main` to `develop`, all specs and plans that supported that released
deployment are consolidated into one canonical spec file and one canonical plan
file for the deployment.

## Scope

### In

- Preserve the current workflow of creating one spec file and one plan file per
  SDD during development.
- Define a post-release rule that consolidates all SDD specs and plans included
  in a released deployment after the tagged release has been back-merged from
  `main` to `develop`.
- Define a canonical mapping rule between a release tag and its consolidated
  spec/plan documents.
- Update repository guidance so the consolidation happens only after a
  successful tagged release and back-merge, not during normal SDD execution.
- Preserve decision history and approval traceability after consolidation.

### Out

- Product code, templates, models, views, workflows, or runtime behavior.
- Rewriting accepted technical decisions beyond what is needed to merge the
  markdown history.
- Changing release tags, release automation, or changelog version structure.

## UI/UX Requirements

- Not applicable to product UI.

## Backend/Documentation Requirements

- The repository must keep the current per-SDD spec/plan creation flow for
  active work.
- The repository must also define a documented post-release process for
  identifying which SDD specs and plans belong to a released deployment and how
  they are consolidated.
- The repository must not leave released per-SDD spec or plan files behind once
  a deployment has been consolidated, except when a released artifact cannot be
  traced confidently and governance explicitly allows deferring that specific
  migration.
- Consolidated files must preserve the decision history, approval context, and
  acceptance criteria from the merged source files.
- Superseded per-SDD files must either be removed or replaced with a clearly
  documented provenance strategy decided in implementation.
- `README.md`, `AGENTS.md`, and `docs/PROJECT_INSTRUCTIONS.md` must stay aligned
  if any of them describe the SDD workflow, release cycle, or repository
  structure.

## Data Rules

- No release tag metadata may be altered as part of this work.
- Historical per-SDD content must remain traceable after consolidation.
- Consolidation must occur only for deployments that were actually released and
  successfully back-merged to `develop`.
- If a released deployment has already been consolidated, later governance work
  must not leave additional released per-SDD files outside the latest
  applicable consolidated release files.
- Governance metadata (`Instruction Set Version` and `Last Updated`) must remain
  synchronized between `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` if either
  file changes.

## Reuse Rules

- Reuse the existing SDD workflow instead of replacing it.
- Reuse the current per-SDD creation pattern during active work.
- Reuse the current plan template unless implementation shows a minimal update is
  required to support the post-release consolidation rule.
- Prefer merging existing markdown content over rewriting it from scratch.

## Acceptance Criteria

1. Repository guidance states that active development continues to use one spec
   file and one plan file per SDD.
2. Repository guidance states that after each successful tagged release and
   back-merge from `main` to `develop`, all SDD specs for that released
   deployment are consolidated into one canonical spec file.
3. Repository guidance states that after each successful tagged release and
   back-merge from `main` to `develop`, all SDD plans for that released
   deployment are consolidated into one canonical plan file.
4. Once a released deployment is consolidated, no leftover released per-SDD
   spec or plan files remain outside the applicable consolidated release files.
5. Consolidated files preserve readable historical intent, approval context,
   and acceptance criteria from the merged source files.
6. Repository guidance reflects the new post-release consolidation convention
   wherever the SDD or repository structure is described.

## Manual Functional Checks

1. Read the updated governance guidance and confirm it still requires one spec
   file and one plan file per SDD during active development.
2. Confirm the updated guidance also states that consolidation happens only
   after a successful tagged release and back-merge from `main` to `develop`.
3. Inspect the defined post-release convention and confirm it results in one
   canonical consolidated spec file and one canonical consolidated plan file
   per released deployment.
4. Confirm there are no leftover released per-SDD spec/plan files outside the
   applicable consolidated release files for already-consolidated deployments.
5. Open one consolidated spec and one consolidated plan and confirm they still
   preserve the merged scope, criteria, approval context, and history.
6. Verify `README.md`, `AGENTS.md`, and `docs/PROJECT_INSTRUCTIONS.md` do not
   contradict each other if they reference the SDD workflow or repository
   structure.

## Files Allowed to Change

- `specs/*.md`
- `plans/*.md`
- `plans/TEMPLATE.md`
- `README.md`
- `AGENTS.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `CHANGELOG.md`
- this spec file

## Files Forbidden to Change

- application code under `paddle/**`
- GitHub workflows under `.github/workflows/**`
- tests
- static assets
