# Governance Ignore Markdown Line Length

## Context

- Current governance requires markdownlint validation and already emphasizes
  `MD022` and `MD032`, but it does not explicitly say that long lines are
  acceptable or that authors should avoid wrapping lines only for line-length
  reasons.
- The requested change is to update governance so line length is not treated as
  a blocking markdown violation and long authoritative lines remain single-line.
- Files/components read first during discovery:
  - `specs/014-governance-ignore-markdown-line-length.md`
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `AGENTS.md`

## Spec Reference

- `specs/014-governance-ignore-markdown-line-length.md`

## Objectives

- Make the Markdown governance explicit that long lines are allowed.
- Instruct authors not to wrap long lines solely to satisfy line-length linting.
- Keep `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` synchronized in wording
  and metadata.
- Preserve the existing mandatory structural Markdown rules.

## Scope

### In

- Update the Markdown-rules sections in `docs/PROJECT_INSTRUCTIONS.md` and
  `AGENTS.md`.
- Synchronize `Instruction Set Version` and `Last Updated` across both files.
- Validate the changed Markdown files after editing.

### Out

- Any product-code, test, or workflow changes.
- Changes to non-governance documentation except the required spec and plan
  files.
- Any change to mandatory `MD022` and `MD032` enforcement.

## Risks

- Risk: The new wording could be interpreted as disabling all markdownlint
  rules.
  Mitigation: State clearly that only line-length violations are non-blocking,
  while `MD022` and `MD032` remain mandatory.
- Risk: Governance files could drift out of sync.
  Mitigation: Update version/date in both files in the same patch and compare
  them before delivery.

## Files Allowed to Change

- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
- `specs/014-governance-ignore-markdown-line-length.md`
- `plans/2026-03-14_governance-ignore-markdown-line-length.md`

## Files Forbidden to Change

- `CHANGELOG.md`
- `paddle/**`
- `.github/workflows/**`
- test files
- unrelated documentation

## Proposed Changes (Step-by-Step by File)

- `docs/PROJECT_INSTRUCTIONS.md`
  - Change: Update the Markdown-rules and validation language so long lines are
    explicitly acceptable and should not be wrapped only for line-length
    reasons; synchronize version/date metadata.
  - Why: This file has higher authority and must define the intended policy.
  - Notes: Keep the file under the existing size constraints.

- `AGENTS.md`
  - Change: Mirror the same Markdown line-length policy and synchronize
    version/date metadata with `docs/PROJECT_INSTRUCTIONS.md`.
  - Why: Governance documents must stay aligned.
  - Notes: Preserve the existing SDD and output rules.

- `specs/014-governance-ignore-markdown-line-length.md`
  - Change: Keep the approved spec accurate and lint-clean.
  - Why: Required by the repository workflow.
  - Notes: Only minimal corrections if needed.

- `plans/2026-03-14_governance-ignore-markdown-line-length.md`
  - Change: Record the approved implementation plan for this governance update.
  - Why: Required before implementation.
  - Notes: No product code in plan mode.

## Plan Steps (Execution Order)

- [ ] Update `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` with aligned
  Markdown line-length policy and synchronized metadata.
- [ ] Verify the new wording preserves mandatory `MD022` and `MD032`
  requirements while making long lines non-blocking.
- [ ] Run markdownlint on the changed Markdown files and fix any structural
  issues before delivery.

## Acceptance Criteria (Testable)

- [ ] Both governance files explicitly say long lines are not treated as
  violations.
- [ ] Both governance files explicitly say not to wrap long lines into multiple
  lines solely for line-length linting.
- [ ] `Instruction Set Version` and `Last Updated` match in both governance
  files after the update.
- [ ] `MD022` and `MD032` remain mandatory in both governance files.

## Validation Commands

```bash
markdownlint docs/PROJECT_INSTRUCTIONS.md AGENTS.md \
  specs/014-governance-ignore-markdown-line-length.md \
  plans/2026-03-14_governance-ignore-markdown-line-length.md
```

## Manual Functional Checks

1. Read the Markdown rules in both governance files and confirm long lines are
   allowed without being treated as blocking violations.
2. Confirm both files state that long lines should not be wrapped into multiple
   lines only to satisfy line-length linting.
3. Confirm `MD022` and `MD032` remain mandatory in both files.
4. Confirm the version/date metadata matches exactly between the two governance
   files.

## Execution Log

- 2026-03-14 22:36 UTC — Spec created.
- 2026-03-14 22:37 UTC — Spec approved.
- 2026-03-14 22:38 UTC — Plan created.

## Post-Mortem / Improvements

- What worked well
  - The requested governance change is narrow and can stay localized.
- What caused friction
  - Existing wording already hinted at preserving authoritative long lines, but
    it did not explicitly remove line-length violations as a blocking concern.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`
  - `/AGENTS.md`
  - `/plans/TEMPLATE.md`
  - No further governance-template changes are proposed at this time.
