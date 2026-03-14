# Governance README Consultation and Maintenance

## Context

- Current governance defines the authority order but does not explicitly tell
  agents to consult `README.md` when repository context or navigation guidance
  would help.
- Current governance also does not explicitly say to keep `README.md` updated
  when repository guidance or other README-covered context changes.
- The requested change is to add both rules while preserving the existing
  authority order.
- Files/components read first during discovery:
  - `specs/015-governance-check-readme-when-necessary.md`
  - `docs/PROJECT_INSTRUCTIONS.md`
  - `AGENTS.md`
  - `README.md`

## Spec Reference

- `specs/015-governance-check-readme-when-necessary.md`

## Objectives

- Add a governance rule to consult `README.md` when necessary for repository
  context, architecture orientation, or safe navigation.
- Add a governance rule to keep `README.md` updated when its covered guidance
  or repository context changes.
- Preserve the current authority order and synchronize governance metadata.
- Validate the changed Markdown files after editing.

## Scope

### In

- Update authority/governance wording in `docs/PROJECT_INSTRUCTIONS.md`.
- Update matching authority/governance wording in `AGENTS.md`.
- Synchronize `Instruction Set Version` and `Last Updated` across both files.
- Validate changed Markdown files with current governance expectations.

### Out

- Changes to `README.md` content itself for this task.
- Product code, tests, workflows, or runtime behavior changes.
- Changes to the spec/plan workflow beyond the README consultation and
  maintenance rules.

## Risks

- Risk: The new wording could accidentally imply `README.md` is a higher
  authority source.
  Mitigation: State clearly that `README.md` is supporting context only.
- Risk: The wording could be too vague about when README updates are required.
  Mitigation: Tie the requirement to README-covered repository context or
  guidance changes.
- Risk: Governance files could drift out of sync.
  Mitigation: Update both files in the same patch and verify matching metadata.

## Files Allowed to Change

- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
- `specs/015-governance-check-readme-when-necessary.md`
- `plans/2026-03-14_governance-readme-consultation-and-maintenance.md`

## Files Forbidden to Change

- `README.md`
- `CHANGELOG.md`
- `paddle/**`
- `.github/workflows/**`
- test files

## Proposed Changes (Step-by-Step by File)

- `docs/PROJECT_INSTRUCTIONS.md`
  - Change: Add authority/governance wording to consult `README.md` when
    necessary and to keep `README.md` updated when README-covered context or
    guidance changes; synchronize version/date metadata.
  - Why: This file has higher authority and must define the policy clearly.
  - Notes: Do not imply that `README.md` overrides governance.

- `AGENTS.md`
  - Change: Mirror the same README consultation and maintenance policy;
    synchronize version/date metadata with `docs/PROJECT_INSTRUCTIONS.md`.
  - Why: Governance documents must stay aligned.
  - Notes: Keep the change localized.

- `specs/015-governance-check-readme-when-necessary.md`
  - Change: Keep the approved spec accurate and lint-clean.
  - Why: Required by repository workflow.
  - Notes: Only minimal corrections if needed.

- `plans/2026-03-14_governance-readme-consultation-and-maintenance.md`
  - Change: Record the approved execution plan for this governance update.
  - Why: Required before implementation.
  - Notes: No product code in plan mode.

## Plan Steps (Execution Order)

- [ ] Update `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` with aligned README
  consultation and README maintenance rules plus synchronized metadata.
- [ ] Verify the wording keeps `README.md` as supporting context rather than a
  higher-authority instruction source.
- [ ] Run markdownlint on the changed Markdown files using the current
  governance policy and fix any structural issues before delivery.

## Acceptance Criteria (Testable)

- [ ] Both governance files say to check `README.md` when necessary for
  repository context or navigation.
- [ ] Both governance files say to keep `README.md` updated when README-covered
  guidance or repository context changes.
- [ ] The authority order remains unchanged in both governance files.
- [ ] `Instruction Set Version` and `Last Updated` match in both governance
  files after the update.

## Validation Commands

```bash
markdownlint --disable MD013 -- docs/PROJECT_INSTRUCTIONS.md AGENTS.md \
  specs/015-governance-check-readme-when-necessary.md \
  plans/2026-03-14_governance-readme-consultation-and-maintenance.md
```

## Manual Functional Checks

1. Read the governance section in both files and confirm they instruct agents
   to check `README.md` when necessary.
2. Confirm both files also instruct contributors to keep `README.md` updated
   when README-covered guidance or repository context changes.
3. Confirm the wording does not place `README.md` above the explicit task brief
   or `docs/PROJECT_INSTRUCTIONS.md`.
4. Confirm the version/date metadata matches exactly in both governance files.

## Execution Log

- 2026-03-14 22:44 UTC — Spec created.
- 2026-03-14 22:46 UTC — Spec refined to include README maintenance guidance.
- 2026-03-14 22:46 UTC — Spec approved.
- 2026-03-14 22:47 UTC — Plan created.

## Post-Mortem / Improvements

- What worked well
  - The requested governance change is narrow and fits the existing authority
    section cleanly.
- What caused friction
  - The original request expanded during spec review to include both README
    consultation and maintenance expectations.
- Suggested updates to:
  - `/docs/PROJECT_INSTRUCTIONS.md`
  - `/AGENTS.md`
  - `/plans/TEMPLATE.md`
  - No further governance-template changes are proposed at this time.
