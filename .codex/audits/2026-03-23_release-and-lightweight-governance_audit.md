# Release And Lightweight Governance Audit

## Summary

- Scope: Targeted governance review for the lightweight simple-change exception
  and release-auth documentation updates.
- Audited target: `docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`, `README.md`,
  `RELEASE.md`, and `CHANGELOG.md`.
- Audit date: 2026-03-23
- Reviewer: Codex via `governance-markdown-auditor`

## Governance Findings

### Finding GF-001

- Status: solved
- Type: Suggestion
- Severity: minor
- Category: boundary
- Evidence: The repository needed one narrow exception to the standard SDD
  workflow for small, low-risk documentation and governance edits, while
  keeping release-auth setup owned by `RELEASE.md` instead of spreading those
  operational details across higher-level governance files.
- Why it matters: Without a scoped exception, trivial governance/doc fixes
  create unnecessary spec/plan overhead. Without a clear owner, release-auth
  setup would drift across multiple markdown files.
- Recommended minimal fix: Add the exception only to the governance files that
  define workflow expectations, and keep the operational `gh` setup in
  `RELEASE.md`.
- Discard explanation:

## Ownership Map

- File: `docs/PROJECT_INSTRUCTIONS.md`
  - Current role: Compact repository constraints and minimum SDD gates,
    including the narrow simple-change exception.
  - Recommended role: Keep as the compact authority file for workflow gates and
    repository constraints.
- File: `AGENTS.md`
  - Current role: Codex execution behavior and workflow mechanics, including
    how the simple-change exception is triggered.
  - Recommended role: Keep as the execution-behavior owner.
- File: `README.md`
  - Current role: Orientation and routing note that points to the active-work
    lookup rule and mentions the narrow exception.
  - Recommended role: Keep as a routing document only.
- File: `RELEASE.md`
  - Current role: Owner of release prerequisites and local release setup,
    including Codespaces `gh` authentication guidance.
  - Recommended role: Keep all release-auth operational detail here.
- File: `CHANGELOG.md`
  - Current role: Record of the governance and release-guidance changes.
  - Recommended role: Keep as release history and unreleased change tracking.

## Coordination Gaps

- Gap: None for the reviewed scope after the current changes.

## Rewrite Plan

- Step: No further rewrite needed for this scope.
  - Goal: Keep the simple-change exception narrow and avoid leaking release
    authentication setup into broader governance files.
  - Files primarily affected: `docs/PROJECT_INSTRUCTIONS.md`, `AGENTS.md`,
    `README.md`, `RELEASE.md`

## Open Questions

- None.
