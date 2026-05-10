---
name: development-cycle-closure
description: Use for rankingdepadel.club implementation handoffs, changelog and backlog reconciliation, spec closure, commits, pushes, release consolidation, and ending a development cycle.
---

# Development Cycle Closure

Use this skill when preparing an implementation response, updating closure
metadata, committing, pushing, or reconciling shipped work.

## Implementation Response

Every implementation response must include:

- Technical Summary
- Files Modified
- Tests added or modified, with command and result summary
- Changelog Entry with the exact text added
- Human readable summary of changes
- 3-6 Manual Functional Checks
- Recommended Commit Message covering the full accumulated uncommitted change
  set since the last commit
- After the report, suggest running `/clear` to reset the context window when
  the cycle is closed; this is only a suggestion, never a required step.

## Changelog and Backlog

- Update `CHANGELOG.md` under `## [Unreleased]` for every behavior, docs,
  governance, workflow, or guidance change unless it is formatting-only.
- Prefix mixed-release bullets with stable domain categories such as `UI/UX`,
  `Governance`, `Release`, `Backend`, `Data`, `Mobile`, `Tests`, or `Docs`.
- `CHANGELOG.md` records shipped outcomes, not process narration.
- During cycle closure, reconcile completed in-scope `BACKLOG.md` items by
  removing them and ensuring the outcome is reflected in `CHANGELOG.md`.

## Closing a Development Cycle

Before any commit, push, or closure step:

- Ask whether the user wants to continue developing.
- If not, ask: `Do you want me to proceed with staging changes, committing with
  the recommended commit message, pushing to the remote branch, and closing the
  current development cycle?`
- If the user explicitly says `close cycle`, `close specification`, or gives
  equivalent direct closure authorization, treat that as approval.

When closure is authorized:

1. Update each completed in-scope loose spec from `Status: approved` to
   `Status: implemented`.
2. Reconcile in-scope backlog items.
3. Stage, commit, and push sequentially.
4. Use `git commit --no-gpg-sign`; do not try a signed commit first in this
   environment.
5. Keep processing requested-work changes until `git status --short` is clean.

Release authorization is not production authorization. If a closure request
also asks for release, proceed only through staging deployment and staging
verification, then stop for the staging manual checks. Do not create or merge
the `staging -> main` PR, deploy production, or back-merge `main` until the user
explicitly approves production promotion after those staging checks, or supplies
the documented `--staging-approved` resume command.

Keep release closure context-light. Summarize command results instead of
pasting repeated polling output, avoid full diffs unless diagnosing a failure,
and report only the decision-relevant lines from GitHub checks, SSH deploys,
and validation commands. Prefer one concise status update per release phase.

## Release Consolidation

After a successful tagged release and back-merge from `main` to `develop`,
consolidate released SDD files before starting new SDD work:

- Use the shipped production release as history.
- Consolidate only loose files marked with the shipped `vX.Y.Z`.
- Treat any loose spec with `Status: implemented` or `Status: shipped` and
  `Release tag: unreleased` as a release-blocking metadata error.
- Fold completed backlog outcomes into final release-summary wording when
  relevant.
- Keep the changelog section grouped by stable categories.
- Roll unshipped planned-version work into the next production release that
  ships it.
- Create a new loose spec for post-release follow-up instead of extending a
  shipped file.
