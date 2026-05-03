---
name: sdd-grill-me
description: Use for rankingdepadel.club SDD planning interviews, "grill me" prompts, plan pressure-tests, unresolved product or architecture decisions, and pre-implementation planning that should end in a decision-complete proposed plan.
---

# SDD Grill Me

Use this skill when the user wants a rigorous planning interview before specs,
implementation, or architectural commitment.

## Operating Rules

- Stay in planning mode for this workflow; do not implement.
- Verify the current branch before planning. If it is not `develop`, warn and
  wait for confirmation before any later implementation work.
- Use `$sdd-workflow` as governing context for repository constraints, active
  specs, audit gates, and validation expectations.
- Explore the repo before asking questions. Do not ask for facts that can be
  discovered through files, schemas, tests, specs, or current behavior.
- Ask only questions that materially change scope, product behavior, UX,
  architecture, data flow, validation, or rollout risk.
- Ask one question at a time unless the tool surface requires batching. Include
  a recommended answer and concrete tradeoff choices.
- Push back on contradictions, hidden assumptions, risky defaults, and vague
  success criteria.
- Track resolved decisions, open dependencies, assumptions, blockers, and the
  next decision to resolve.

## Interview Flow

1. Ground the task in repo truth: branch, relevant specs, current code paths,
   tests, templates, models, routes, and governance constraints.
2. Clarify intent until goal, audience, success criteria, in-scope behavior,
   out-of-scope behavior, and constraints are explicit.
3. Resolve implementation decisions: interfaces, data flow, edge cases,
   failure modes, compatibility, validation, and review or audit checkpoints.
4. Stop when the plan is decision-complete enough for another engineer or
   agent to implement without choosing defaults.

## Final Output

When the decision tree is resolved, output exactly one `<proposed_plan>` block.
Keep it concise and include:

- Clear title.
- Brief summary.
- Key implementation changes or public interfaces.
- Test cases and acceptance scenarios.
- Explicit assumptions and defaults.

Do not ask whether to proceed in the final plan.
