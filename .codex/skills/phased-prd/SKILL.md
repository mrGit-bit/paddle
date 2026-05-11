---
name: phased-prd
description: Create persistent PRDs for complex rankingdepadel.club work that should later be split into approved implementation phases. Use when a requested feature, refactor, or process change is too large for one SDD spec, needs phased delivery, or should preserve product decisions before phase planning.
---

# Phased PRD

Use this skill to turn the current conversation and repository context into a
durable PRD before implementation specs are written.

## Operating Rules

- Verify the current branch before writing. If it is not `develop`, warn and
  wait.
- Use `$sdd-workflow` for repository constraints, SDD gates, audit checkpoints,
  and validation expectations.
- Explore the repo before drafting. Use current domain vocabulary and respect
  existing architecture, specs, tests, templates, and governance.
- Ask only for decisions that materially change product behavior, scope,
  implementation boundaries, sequencing, validation, or rollout risk.
- PRDs are planning artifacts under `docs/prds/<slug>.md`.
- Phase specs remain the implementation gate under `specs/###-phase-title.md`
  and must be approved before development starts.
- Do not mark a PRD as shipped. Release closure happens through implemented
  specs and changelog reconciliation.

## Workflow

1. Ground the request in repo truth and existing SDD context.
2. Define the problem, target users, success criteria, in-scope behavior, and
   out-of-scope behavior.
3. Sketch the main modules or surfaces that may be built or changed.
4. Prefer deep modules with simple testable interfaces when the work contains
   reusable or complex behavior.
5. Confirm the module/surface breakdown with the user before writing the PRD.
6. Confirm which modules, surfaces, and workflows need explicit tests.
7. Write or update one PRD in `docs/prds/`.
8. Include a phase plan that names likely follow-up SDD specs without assigning
   final spec numbers unless those files are created in the same task.

## PRD Shape

Use this structure:

```markdown
# Title

## Problem Statement

## Goals

## Non-Goals

## Users and Use Cases

## User Stories

## Product Requirements

## Implementation Decisions

## Phase Plan

## Testing Decisions

## Acceptance Scenarios

## Open Questions

## Further Notes
```

## Content Rules

- Keep the PRD detailed enough that phase specs can be written later without
  rediscovering product intent.
- Use file paths only when they document current repo evidence or a stable
  ownership boundary. Avoid code snippets unless a prototype decision is
  clearer as a small schema, state machine, or contract.
- Keep user stories comprehensive for meaningful user and operator workflows,
  not boilerplate permutations.
- In `Phase Plan`, describe each phase by deliverable, dependencies,
  validation focus, and likely rollback or rollout concern.
- In `Testing Decisions`, prefer behavior-focused tests and cite existing test
  patterns when known.
- Leave unresolved decisions in `Open Questions`; do not hide unknowns as
  defaults.
