---
name: sdd-workflow
description: Use for rankingdepadel.club product/code work, active SDD specs, Codex planning, repository constraints, and deciding whether review or audit checkpoints apply.
---

# SDD Workflow

Use this skill for product behavior, code changes, non-trivial planning, active
specs, and repository constraints.

## Repository Constraints

- Product: padel rankings, matches, player profiles, and Americano tournaments.
- Backend: Django. Frontend: Django templates and Bootstrap 5.
- Mobile: Capacitor WebView wrapper around the web product.
- Python: 3.10.12.
- Development DB: SQLite. Staging/production DB: Oracle Autonomous Database
  over TCPS.
- Use vanilla JavaScript only when necessary.
- DRF/API endpoints are deprecated and must not be extended.
- Backend owns business logic; templates render only.
- No frontend ranking logic.
- Reuse existing presentation classes/components before adding parallel styles.
- Treat user-edited UI text, labels, class names, and style choices as product
  intent. Do not normalize, rename, or "clean up" them while making adjacent
  changes unless the user explicitly asks.
- If a requested change touches user-written text or styles and the intended
  outcome is ambiguous, ask before editing that surface.
- For CSS/template fixes, trace the rendered template and actual selector or
  component path before editing styles; verify the selector changed is present
  on the affected surface.
- Before reusing a shared CSS class for a new component state, check whether
  later base selectors reset the same custom properties or declarations.
- When a shared state class must override a component base class, account for
  CSS cascade order with a colocated combined selector after the base selector.
- UI text is Spanish. Code, comments, docs, and specs are English.
- Apply DRY, KISS, SRP, YAGNI, and Explicit > Implicit.
- Avoid speculative refactors, renames, moves, and unrelated formatting.
- Verify current official behavior before relying on external tools,
  integration discovery, authentication, configuration paths, or versioned
  capabilities.

## SDD Gate

Before non-trivial implementation:

1. Check the current git branch.
2. If it is not `develop`, warn and wait for confirmation before editing.
3. Find or create the latest approved non-release spec for the task under
   `specs/###-short-title.md`.
4. Start implementation only after the active-work spec is approved.

If the active-work spec is missing or incomplete, notify the user and wait
for further instructions before proceeding.

Simple-change exception:

- Small, low-risk documentation, governance, or repository-guidance edits may
  skip a new active-work spec.
- If the task grows beyond that narrow scope, return to the standard SDD gate.

Spec lifecycle:

- Active work uses non-release specs only.
- Specs created from `$prd-to-specs` follow the same active-work gate:
  implement only one approved non-release spec at a time unless the user
  explicitly widens scope.
- `specs/release-*.md` files are historical release records.
- Loose non-release specs use `Status: approved|implemented` and
  `Release tag: unreleased`.
- Move a spec to `implemented` only when the scoped work is complete and the
  development cycle is being closed.

## Planning Behavior

- In planning workflows, explore the repo before asking questions.
- Ask preference-locking questions for non-trivial work when product, UX, or
  implementation tradeoffs remain.
- Treat `docs/pre-specs/` files as scratch input only. Do not stage, commit,
  release-consolidate, or describe them as shipped artifacts.
- ChatGPT pre-specs are starting points for Codex `/plan`, not active specs.
- Active specs should capture only scope, constraints, stable execution notes,
  acceptance checks, and validation needed to execute safely.

## Quality Checkpoints

Evaluate the relevant checkpoint before advancing non-trivial work:

- `/review`: fast targeted review of a draft, diff, or scoped change set.
- `$audit`: Django view behavior, architecture, security, reuse, and ORM
  performance.
- `$template-presentation-audit`: one-template CSS cascade, computed-style, and
  responsive presentation review.
- `$governance-markdown-auditor`: governance markdown, ownership, duplication,
  and process overhead.

If no checkpoint fits, say why. Surface only medium/high-severity findings.
Ask the user whether to address or discard each finding before fixing it.

## Model and Schema Changes

When Django model/schema changes are introduced, generate and apply migrations
in development before treating the task as complete.
