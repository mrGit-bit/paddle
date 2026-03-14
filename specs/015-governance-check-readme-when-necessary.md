# Spec 015: Governance Check README When Necessary

## Functional Goal

Update the governance documents so agents are explicitly instructed to consult
`README.md` when it is necessary for current repository context, architecture
orientation, or safe repository navigation, and so contributors are instructed
to keep `README.md` updated when README-covered repository context or guidance
changes.

## Scope

### In

- Update governance wording in `docs/PROJECT_INSTRUCTIONS.md`.
- Update matching governance wording in `AGENTS.md`.
- Add governance wording that `README.md` should be kept updated when it
  contains repository context or guidance affected by a change.
- Keep version/date metadata synchronized across both governance files in the
  same change set.
- Keep the new README consultation rule subordinate to the existing authority
  order where the explicit task brief and `docs/PROJECT_INSTRUCTIONS.md` remain
  higher authority than `README.md`.

### Out

- Changes to product code, tests, workflows, or runtime behavior.
- Changes to `README.md` content itself for this task.
- Changes to spec/plan workflow beyond adding README consultation guidance.

## UI/UX Requirements

- Not applicable to product UI.

## Backend/Documentation Requirements

- Governance must clearly state when consulting `README.md` is expected or
  useful.
- Governance must clearly state that `README.md` should be updated when
  repository guidance, architecture orientation, or other README-covered
  context becomes outdated because of a change.
- The wording must not elevate `README.md` above the existing authority order.
- The wording in `docs/PROJECT_INSTRUCTIONS.md` and `AGENTS.md` must remain
  aligned.
- The new rule should help agents use `README.md` as a practical repository
  map, not as a replacement for higher-authority governance.

## Data Rules

- Authority order remains:
  1. Explicit task brief
  2. `docs/PROJECT_INSTRUCTIONS.md`
  3. `AGENTS.md`
- `README.md` is supporting repository context, not a higher-authority source.
- `Instruction Set Version` and `Last Updated` must match across the two
  governance files after the change.

## Reuse Rules

- Reuse the existing authority/governance sections instead of creating
  disconnected new policy sections.
- Keep edits minimal and localized to governance wording and synchronized
  metadata.

## Acceptance Criteria

1. `docs/PROJECT_INSTRUCTIONS.md` explicitly instructs agents to check
   `README.md` when necessary for repository context or navigation.
2. `AGENTS.md` contains the same README consultation guidance.
3. Both governance files instruct contributors to keep `README.md` updated when
   covered repository context or guidance changes.
4. The new wording does not change the current authority order.
5. `Instruction Set Version` and `Last Updated` remain synchronized between the
   two governance files.

## Manual Functional Checks

1. Read the authority/governance section in both files and confirm they mention
   checking `README.md` when necessary.
2. Confirm the wording does not place `README.md` above the explicit task brief
   or `docs/PROJECT_INSTRUCTIONS.md`.
3. Confirm both governance files also say to keep `README.md` updated when
   README-covered repository context changes.
4. Confirm both governance files use materially matching wording for the README
   consultation and maintenance rules.
5. Confirm version/date metadata matches exactly in both governance files.

## Files Allowed to Change

- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
- this spec file
- the corresponding plan file

## Files Forbidden to Change

- `README.md`
- `CHANGELOG.md`
- application code under `paddle/**`
- GitHub workflows
- test files
