---
name: prd-to-specs
description: Break a phased PRD into vertical-slice SDD specs for rankingdepadel.club. Use when a PRD created with $phased-prd needs to become one or more implementation specs under specs/.
---

# PRD to Specs

Use this skill to convert a durable PRD into thin, reviewable SDD specs. The
output is implementation planning only; do not start code changes through this
skill.

## Operating Rules

- Verify the current branch before writing. If it is not `develop`, warn and
  wait.
- Use `$sdd-workflow` for repository constraints, SDD gates, audit checkpoints,
  and validation expectations.
- Source material should be an on-demand PRD under `docs/prds/` created or
  maintained by `$phased-prd`. If the user provides a path, use that exact PRD.
- Explore enough current repo context to use accurate domain vocabulary,
  ownership boundaries, tests, templates, models, and existing specs.
- Create specs only after the user approves the vertical-slice breakdown.
- Phase specs remain implementation-gated until approved by the user. Do not
  implement, close, release-consolidate, or mark the source PRD as shipped.

## Workflow

1. Read the PRD and note goals, non-goals, user stories, requirements,
   implementation decisions, phase plan, testing decisions, acceptance
   scenarios, and open questions.
2. Inspect current repo surfaces that materially affect slice boundaries.
3. Draft vertical slices. Each slice should deliver a narrow complete path
   through the relevant layers, such as data, business logic, template/UI,
   operator workflow, tests, and validation.
4. Prefer many thin specs over broad horizontal specs. Avoid slices that only
   change one technical layer unless that layer is independently deployable and
   verifiable.
5. Classify each slice as:
   - `AFK`: implementation-ready after spec approval, with no unresolved
     product, UX, architecture, rollout, or data decision.
   - `HITL`: requires human decision, design review, migration approval, audit
     checkpoint, or other explicit confirmation before implementation.
6. Present the proposed breakdown as a numbered list and ask the user to
   approve or revise it before creating files.
7. After approval, create one non-release spec per slice using
   `specs/TEMPLATE.md`. Assign the next available `specs/###-short-title.md`
   numbers only when creating files.
8. Keep each spec scoped to its slice and include dependencies, allowed files,
   forbidden files, execution notes, acceptance checks, validation, and required
   audit or review checkpoints.

## Breakdown Review Shape

For each proposed slice, show:

- `Title`: short implementation-spec title.
- `Type`: `AFK` or `HITL`.
- `Blocked by`: earlier slices or unresolved decisions.
- `PRD coverage`: goals, requirements, user stories, or acceptance scenarios
  covered by the slice.
- `Validation focus`: likely tests, manual checks, or audit checkpoints.

Ask the user whether the granularity, dependencies, PRD coverage, and
`AFK`/`HITL` classifications are correct. Iterate until approved.

## Spec Content Rules

- Describe end-to-end behavior and stable execution constraints, not a
  layer-by-layer work log.
- Use file paths when they define scope, ownership, validation, or forbidden
  changes.
- Keep unresolved decisions in the spec execution notes or leave the slice as
  `HITL`; do not hide unknowns as defaults.
- Preserve PRD non-goals and exclude them explicitly when scope drift is likely.
- Cite the source PRD path in each spec summary or execution notes.
- Do not create release specs. Active PRD phase work uses only non-release
  specs with `Status: approved` and `Release tag: unreleased`.

## Validation

- Run `python scripts/validate_governance.py` if router or governance files
  changed.
- Run markdownlint on changed Markdown files when available; `MD013` is
  non-blocking.
