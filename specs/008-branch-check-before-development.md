# Spec 008: Mandatory Branch Check Before Development Work

## Functional Goal

Ensure instruction documents require Codex to verify the active git branch before implementing any requested development change, and require an explicit user branch decision when not on `develop`.

## Scope

### In

- Update project instructions in `docs/PROJECT_INSTRUCTIONS.md` to add a mandatory pre-implementation branch check rule.
- Update Codex CLI instructions in `AGENTS.md` to add the same mandatory rule.
- Rule behavior:
  - Before starting development work, check current branch.
  - If current branch is not `develop`, emit a clear warning and ask the user explicitly which branch should receive the changes.

### Out

- No product code changes.
- No workflow/script changes.
- No branching model changes.

## UI/UX Requirements

- Not applicable.

## Backend/Automation Requirements

- Rule text must be explicit and enforceable (no ambiguous wording).
- Rule must apply whenever user asks to develop/implement/change code or behavior.

## Data Rules

- Canonical expected default branch for development work: `develop`.
- Non-`develop` branch usage requires explicit user confirmation/direction.

## Reuse Rules

- Reuse existing governance sections related to workflow/branching/instructions instead of introducing unrelated sections.

## Acceptance Criteria

- AC1: `AGENTS.md` contains an explicit mandatory branch-check instruction before development work.
- AC2: `docs/PROJECT_INSTRUCTIONS.md` contains the same policy.
- AC3: Both documents clearly require warning + explicit user branch confirmation when not on `develop`.

## Manual Functional Checks

1. Start a Codex task while checked out on `develop` and confirm normal flow continues after branch check.
2. Start a Codex task while checked out on `main` and confirm Codex warns and asks which branch to use.
3. Confirm wording in both docs is consistent and unambiguous.

## Files Allowed to Change

- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`

## Files Forbidden to Change

- `.github/workflows/**`
- `paddle/**`
- `mobile/**`
- `CHANGELOG.md`
