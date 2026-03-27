# Reduce Markdown Verbosity Across Governance and History Plan

## Tracking

- Task ID: `reduce-markdown-verbosity-across-governance-and-history`
- Spec: `specs/030-reduce-markdown-verbosity-across-governance-and-history.md`
- Release tag: `v1.6.2`

## Summary

- Governance defined Markdown lint rules but not a low-verbosity writing rule.
- `CHANGELOG.md`, active specs/plans, and consolidated release files had grown
  too narrative.

## Scope

- In:
  - add the low-verbosity rule to governance
  - run a focused Markdown review/audit
  - shorten the affected changelog/spec/plan/release-history files
- Out:
  - product code
  - workflow changes
  - removal of shipped facts

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

## Plan

- [ ] Add the low-verbosity Markdown rule to governance.
- [ ] Audit the highest-friction Markdown files.
- [ ] Shorten the affected active and historical artifacts.
- [ ] Validate Markdown and update the audit record.

## Acceptance

- [ ] Governance states the low-verbosity rule.
- [ ] `CHANGELOG.md` is materially shorter in the touched area.
- [ ] Active specs/plans and the template are more execution-focused.
- [ ] Consolidated release files keep provenance with less bulk.
- [ ] The audit report records the solved verbosity finding.

## Validation

- `markdownlint-cli2 --config /tmp/markdownlint-no-md013.json AGENTS.md docs/PROJECT_INSTRUCTIONS.md README.md RELEASE.md CHANGELOG.md plans/*.md specs/*.md .codex/audits/*.md`
- Manual checks:
  - Compare one changelog area before/after.
  - Open one active spec/plan and one consolidated release file.
  - Confirm the audit report records the new rule.
