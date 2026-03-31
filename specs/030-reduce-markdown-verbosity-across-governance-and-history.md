# Reduce Markdown Verbosity Across Governance and History

## Tracking

- Task ID: `reduce-markdown-verbosity-across-governance-and-history`
- Plan: `plans/2026-03-27_reduce-markdown-verbosity-across-governance-and-history.md`
- Release tag: `unreleased`

## Goal

- Make repository Markdown lighter and more schematic by default.
- Apply that rule to governance docs, `CHANGELOG.md`, active specs/plans, and
  consolidated release files.

## Scope

- In:
  - add an explicit low-verbosity Markdown rule to governance
  - shorten current changelog/spec/plan/release-history wording
  - update the governance audit to record the new rule
- Out:
  - product code changes
  - workflow changes
  - dropping shipped facts or traceability

## Files

- Allowed:
  - `specs/030-reduce-markdown-verbosity-across-governance-and-history.md`
  - `plans/2026-03-27_reduce-markdown-verbosity-across-governance-and-history.md`
  - `AGENTS.md`
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `README.md`
  - `RELEASE.md`
  - `CHANGELOG.md`
  - `plans/TEMPLATE.md`
  - `specs/*.md`
  - `plans/*.md`
  - `.codex/audits/*.md`
- Forbidden:
  - `paddle/**`
  - `.github/workflows/**`
  - `.codex/private/**`

## Acceptance

- [ ] Governance explicitly prefers light schematic Markdown.
- [ ] `CHANGELOG.md` is shorter and more outcome-focused.
- [ ] Active specs/plans and the template keep only execution-value detail.
- [ ] Consolidated release files are compact provenance records.
- [ ] The governance audit records the new rule.

## Checks

- Read `AGENTS.md` and `docs/PROJECT_INSTRUCTIONS.md` and confirm the rule is
  explicit.
- Compare the affected `CHANGELOG.md` section before/after and confirm it is
  shorter without losing facts.
- Open one active spec/plan and one consolidated release file and confirm they
  are schematic.
- Confirm the audit report records the verbosity fix.
