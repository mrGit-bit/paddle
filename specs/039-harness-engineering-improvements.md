# Harness Engineering Improvements

Use for active SDD work only.

## Tracking

- Task ID: `harness-engineering-improvements`
- Status: `implemented`
- Release tag: `unreleased`

`approved` stays in place until the scoped work is finished and the
development cycle for this spec is being closed. Only then move the spec to
`implemented`.

## Summary

- Make repository harness checks easier to run locally and harder to bypass in
  CI.
- Document the harness map so humans and agents can find the right source of
  truth quickly.

## Scope

- In:
  - Add a local harness validation command.
  - Add spec validation.
  - Add release dry-run validation.
  - Add governance validation and Markdown linting to CI.
  - Add concise harness documentation.
- Out:
  - Product behavior changes.
  - Release publishing changes.
  - Broad rewrites of existing governance or release workflows.

## Files Allowed to Change

- `.github/workflows/ci.yml`
- `CHANGELOG.md`
- `docs/HARNESS.md`
- `scripts/check_harness.sh`
- `scripts/release_orchestrator.py`
- `scripts/validate_specs.py`
- `specs/039-harness-engineering-improvements.md`

## Files Forbidden to Change

- Product code under `paddle/`
- Mobile app code under `mobile/`
- Existing release records under `specs/release-*.md`

## Execution Notes

- [x] Keep new checks deterministic and local-friendly.
- [x] Keep Markdown concise.
- [x] Do not require network access for local harness validation.

## Acceptance

- [x] A single local command validates the repository harness.
- [x] CI enforces governance validation.
- [x] CI enforces Markdown linting with line length omitted.
- [x] A harness map document explains source-of-truth files and commands.
- [x] Active specs can be validated mechanically.
- [x] Release orchestration exposes a non-destructive check mode.

## Validation

- `python scripts/validate_governance.py`
- `python scripts/validate_specs.py`
- `python scripts/release_orchestrator.py --check`
- `bash scripts/check_harness.sh`
