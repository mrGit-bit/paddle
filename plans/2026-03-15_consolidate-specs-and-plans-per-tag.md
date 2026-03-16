# Post-Release Consolidation of SDD Specs and Plans

## Context

- The approved spec is
  `specs/017-consolidate-specs-and-plans-per-tag.md`.
- The repository currently follows one spec file and one plan file per SDD
  during active work, which should remain unchanged.
- The requested adjustment is to consolidate those already-approved per-SDD
  files only after a tagged release has been completed and successfully
  back-merged from `main` to `develop`.
- The goal is to keep the current execution flow intact while reducing
  long-term repository fragmentation for completed deployments.
- Files/components read first during discovery:
  - `specs/017-consolidate-specs-and-plans-per-tag.md`
  - `specs/*.md`
  - `plans/*.md`
  - `README.md`
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `AGENTS.md`
  - `CHANGELOG.md`

## Spec Reference

- `specs/017-consolidate-specs-and-plans-per-tag.md`

## Objectives

- Preserve the current one-spec-per-SDD and one-plan-per-SDD workflow during
  active development.
- Define and document a post-release consolidation convention that runs after a
  successful tagged release and back-merge from `main` to `develop`.
- Consolidate the set of SDD markdown artifacts that supported a released
  deployment into one canonical spec file and one canonical plan file for that
  deployment.
- Ensure already-consolidated released deployments do not leave behind released
  per-SDD spec or plan files outside the applicable release-level consolidated
  files.
- Keep historical decision context readable after consolidation.

## Scope

### In

- Document that active work continues to create one spec and one plan per SDD.
- Define the release/back-merge checkpoint that triggers consolidation.
- Review existing `specs/` and `plans/` files and group them by released
  deployment.
- Choose canonical filenames and consolidation strategy for each released
  deployment.
- Merge grouped spec content into one canonical deployment-level spec file.
- Merge grouped plan content into one canonical deployment-level plan file.
- Fold any remaining released per-SDD files, such as the `1.4.0` audit-skill
  and generated-Markdown governance artifacts, into the applicable latest
  consolidated release files.
- Update workflow/governance documentation where the release-cycle rule or
  repository structure must change.
- Update `CHANGELOG.md` if the documentation/governance change is behaviorally
  meaningful under project rules.

### Out

- Product code, tests, templates, models, views, or deployment workflows.
- Changes to the actual release tags or release note content.
- Reopening or changing technical decisions unrelated to consolidation.

## Risks

- Risk: Mapping released deployments to the exact set of contributing SDD files
  may be ambiguous for older work.
  Mitigation: Use `CHANGELOG.md`, release chronology, and existing spec/plan
  content to make the grouping explicit before merging files.
- Risk: Removing split files could erase approval or execution history.
  Mitigation: Preserve history inside the consolidated canonical files and keep
  any necessary provenance notes.
- Risk: A deployment may appear consolidated while still leaving released
  per-SDD files behind.
  Mitigation: Add an explicit no-loose-ends governance rule and verify the
  remaining released files are folded into the latest applicable release-level
  consolidated files.
- Risk: Governance updates could accidentally imply that consolidation happens
  before release or during active SDD execution.
  Mitigation: State explicitly that consolidation is a post-release activity
  performed only after successful back-merge to `develop`.
- Risk: Markdown restructuring could introduce lint failures.
  Mitigation: Run markdownlint on every changed Markdown file and fix structural
  issues in the same pass.

## Files Allowed to Change

- `specs/*.md`
- `plans/*.md`
- `plans/TEMPLATE.md`
- `README.md`
- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
- `CHANGELOG.md`

## Files Forbidden to Change

- application code under `paddle/**`
- `.github/workflows/**`
- test files
- static assets

## Proposed Changes (Step-by-Step by File)

- `specs/*.md`
  - Change: Audit the current per-SDD spec inventory, identify which files
    belong to each released deployment, and merge them into one canonical
    deployment-level spec file after release.
  - Why: The user request is to preserve the current per-SDD workflow but
    consolidate completed release batches afterward.
  - Notes: Preserve scope, acceptance criteria, and decision history from the
    source files.

- `plans/*.md`
  - Change: Audit the current per-SDD plan inventory, identify which files
    belong to each released deployment, and merge them into one canonical
    deployment-level plan file after release.
  - Why: The user request is to preserve the current per-SDD workflow but
    consolidate completed release batches afterward.
  - Notes: Preserve execution steps, validation commands, and execution-log
    context from the source files.

- `plans/TEMPLATE.md`
  - Change: Update the template only if needed so it keeps the current per-SDD
    behavior while documenting any post-release consolidation metadata that
    future plans should carry.
  - Why: The template must support the unchanged active workflow and the new
    release-cycle maintenance rule without changing Plan Mode expectations.
  - Notes: Keep changes minimal and markdownlint-compliant.

- `docs/PROJECT_INSTRUCTIONS.md`
  - Change: Update the SDD wording so it explicitly preserves one spec and one
    plan per SDD during development, and adds the post-release consolidation
    rule after successful tagged release back-merge, including the no-loose-
    ends requirement for already-consolidated released deployments.
  - Why: Higher-priority governance must describe the actual workflow.
  - Notes: Keep version/date synchronized with `AGENTS.md`.

- `AGENTS.md`
  - Change: Mirror the same active-workflow and post-release consolidation
    updates made in `docs/PROJECT_INSTRUCTIONS.md`, including the no-loose-ends
    rule.
  - Why: Governance documents must stay aligned.
  - Notes: Keep wording localized and synchronized.

- `README.md`
  - Change: Update repository-structure guidance only if it needs to clarify
    the difference between active per-SDD files and post-release consolidated
    deployment files, including the requirement not to leave released
    per-SDD files behind after consolidation.
  - Why: README should not contradict governance or on-disk structure.
  - Notes: Keep it summary-oriented.

- `CHANGELOG.md`
  - Change: Add an `Unreleased` entry if the governance/documentation
    consolidation changes repository workflow behavior beyond formatting.
  - Why: Project rules require changelog updates for documentation/governance
    changes unless they are truly formatting-only.
  - Notes: Match the real behavior change precisely.

## Plan Steps (Execution Order)

- [ ] Update governance/template wording so active development still uses one
  spec file and one plan file per SDD, and so consolidation is explicitly a
  post-release activity after successful back-merge from `main` to `develop`,
  with no leftover released per-SDD files for already-consolidated
  deployments.
- [ ] Build an explicit mapping of existing spec files and plan files to the
  released deployment each one supports, using `CHANGELOG.md` and file content
  where needed.
- [ ] Choose the canonical consolidated filename format for one deployment-level
  spec and one deployment-level plan per released deployment.
- [ ] Merge grouped spec files into one canonical deployment-level spec file
  while preserving scope, acceptance criteria, and traceable history.
- [ ] Merge grouped plan files into one canonical deployment-level plan file
  while preserving execution details, validation commands, and approval history.
- [ ] Fold the remaining released `1.4.0` per-SDD spec and plan files into the
  `release-1.4.0-consolidated.md` artifacts and remove the superseded
  individual files.
- [ ] Remove or replace superseded per-SDD files according to the chosen
  provenance strategy and update any repository guidance that references them.
- [ ] Run markdownlint on every changed Markdown file and fix all blocking
  structural issues before delivery.

## Acceptance Criteria (Testable)

- [ ] Governance and template documentation state clearly that active
  development still uses one spec file and one plan file per SDD.
- [ ] Governance and template documentation state clearly that consolidation
  happens only after a successful tagged release and back-merge from `main` to
  `develop`.
- [ ] Governance and repository guidance state clearly that already-
  consolidated released deployments must not leave released per-SDD files
  outside the applicable release-level consolidated files.
- [ ] The repository contains only one canonical deployment-level spec file for
  each consolidated released deployment.
- [ ] The repository contains only one canonical deployment-level plan file for
  each consolidated released deployment, excluding `plans/TEMPLATE.md`.
- [ ] Consolidated files preserve the merged scope, criteria, and historical
  context from the source files.
- [ ] Changed Markdown files satisfy required Markdown structure rules,
  including `MD022` and `MD032`.

## Validation Commands

```bash
markdownlint --disable MD013 -- README.md CHANGELOG.md AGENTS.md \
  docs/PROJECT_INSTRUCTIONS.md specs/*.md plans/*.md
```

## Manual Functional Checks

1. Read the updated governance/template wording and confirm active development
   still uses one spec file and one plan file per SDD.
2. Confirm the updated wording states that consolidation happens only after a
   successful tagged release and back-merge from `main` to `develop`.
3. Inspect `specs/` after implementation and confirm each consolidated released
   deployment has only one canonical deployment-level spec file.
4. Inspect `plans/` after implementation and confirm each consolidated released
   deployment has only one canonical deployment-level plan file plus
   `plans/TEMPLATE.md`.
5. Confirm `specs/010-django-view-audit-skill.md`,
   `specs/011-governance-markdown-authoritative-output.md`,
   `plans/2026-03-10_django-view-audit-skill.md`, and
   `plans/2026-03-10_governance-markdown-authoritative-output.md` no longer
   remain as loose released files outside `1.4.0` consolidation.
6. Open one consolidated spec file and one consolidated plan file and confirm
   the merged history, acceptance criteria, and execution details remain
   traceable.

## Execution Log

- 2026-03-15 00:00 UTC — Spec approved.
- 2026-03-15 00:10 UTC — Existing spec/plan inventory reviewed for release-batch
  consolidation planning.
- 2026-03-15 00:15 UTC — Plan created.
- 2026-03-15 00:25 UTC — Plan revised to preserve one spec and one plan per
  active SDD and move consolidation to the post-release back-merge step.
- 2026-03-15 00:35 UTC — Revised plan approved.
- 2026-03-15 00:40 UTC — Implementation started.
- 2026-03-15 01:05 UTC — Markdown validation executed on changed files.
- 2026-03-15 01:10 UTC — Governance and release-level consolidation updates
  completed.
- 2026-03-15 01:20 UTC — Plan revised to prohibit loose released per-SDD files
  after consolidation and to fold remaining `1.4.0` artifacts into the release
  consolidated files.

## Post-Mortem / Improvements

- What worked well
  - The approved spec now preserves the current per-SDD workflow while defining
    the release-cycle cleanup step.
- What caused friction
  - Existing filenames do not naturally encode the released deployment they
    support, so the migration needs an explicit grouping step.
  - Partial consolidation left released `1.4.0` artifacts outside the
    deployment-level release files, so governance needs an explicit
    no-loose-ends rule.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`
  - `/AGENTS.md`
  - `/plans/TEMPLATE.md`
  - Adjust only as much as needed to make the post-release consolidation rule
    explicit and durable.
