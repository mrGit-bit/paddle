# Simplify SDD To A Single Spec Artifact

## Tracking

- Task ID: `simplify-sdd-single-spec-artifact`
- Release tag: `unreleased`

## Summary

- Replace the duplicated spec-plus-plan SDD workflow with one compact approved
  active-work spec per non-trivial task.
- Keep release consolidation, but reduce it to one compact consolidated spec
  record per shipped release.

## Scope

- In:
  - Governance updates for the active-work artifact model.
  - README and release-doc routing updates.
  - Release-orchestrator and pytest updates for single-spec consolidation.
  - Removal of legacy `plans/` release-history artifacts.
- Out:
  - Product behavior changes unrelated to repository workflow.
  - Release-content backfill beyond aligning the artifact model.

## Files Allowed to Change

- `docs/PROJECT_INSTRUCTIONS.md`
- `AGENTS.md`
- `README.md`
- `RELEASE.md`
- `CHANGELOG.md`
- `specs/`
- `plans/`
- `.codex/commands/release.md`
- `.codex/skills/governance-markdown-auditor/SKILL.md`
- `scripts/release_orchestrator.py`
- `paddle/frontend/tests/test_release_orchestrator.py`

## Files Forbidden to Change

- Product application code outside the release-orchestrator test surface.
- Deployment credentials or repo-private SSH assets.

## Implementation Plan

- [ ] Add the canonical single-spec template and document this task as an
  active-work spec.
- [ ] Update governance and repository guidance to require one approved
  active-work spec and one consolidated release spec.
- [ ] Refactor release consolidation and tests to operate only on `specs/`.
- [ ] Remove legacy `plans/` templates and consolidated release records.

## Acceptance

- [ ] Non-trivial work now requires one approved active-work spec instead of a
  separate spec and plan pair.
- [ ] Release consolidation writes only
  `specs/release-X.Y.Z-consolidated.md`.
- [ ] The release orchestrator no longer depends on `Plan:` or `Spec:`
  cross-reference metadata.
- [ ] User-facing repo guidance no longer routes contributors to `plans/`.

## Validation

- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `markdownlint AGENTS.md docs/PROJECT_INSTRUCTIONS.md README.md RELEASE.md CHANGELOG.md specs/TEMPLATE.md specs/037-simplify-sdd-single-spec-artifact.md .codex/commands/release.md .codex/skills/governance-markdown-auditor/SKILL.md`
- Manually confirm the only active-work template lives in `specs/TEMPLATE.md`.
- Manually confirm release docs now describe one consolidated release spec per
  shipped version.
