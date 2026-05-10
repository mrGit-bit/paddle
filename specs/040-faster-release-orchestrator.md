# Faster Release Orchestrator

Use for active SDD work only.

## Tracking

- Task ID: `faster-release-orchestrator`
- Status: `implemented`
- Release tag: `unreleased`

## Summary

- Move release-prep work into the local release orchestrator so normal
  releases no longer depend on the release-prep GitHub workflow and PR.
- Keep promotion PRs, staging deployment, manual staging approval, production
  deployment, and remote version/migration verification.
- Add release-completion controls so duplicate changelog headers and missing
  release consolidation records are caught before a completed release reports
  success.

## Scope

- In:
  - Local changelog and version release-prep commit inside
    `scripts/release_orchestrator.py`.
  - Optional `--next-patch` version derivation.
  - Explicit `--skip-local-validation` rerun escape hatch.
  - Deterministic promotion PR check handling when no checks are reported.
  - Mandatory consolidation validation after production and back-merge.
  - Repair of the duplicated `1.10.2` changelog header and missing `1.10.1`
    and `1.10.2` consolidation records.
  - Release documentation and tests for the changed workflow.
- Out:
  - Removing the fallback release-prep GitHub workflow.
  - Removing staging or production promotion PRs.
  - Automatic production promotion without explicit approval.
  - Remote deploy script changes.

## Acceptance

- [x] A normal release prepares `CHANGELOG.md` and `paddle/config/__init__.py`
      locally, commits the release-prep change, and pushes `develop`.
- [x] Duplicate target release headers fail before staging promotion.
- [x] Empty `Unreleased` fails unless a future explicit no-op mode is added.
- [x] Promotion PRs still require required or visible checks, and no-check
      promotion PRs fail quickly with an actionable diagnostic.
- [x] `--skip-local-validation` skips only local pytest validation and only
      when explicitly supplied.
- [x] `--next-patch` derives the next patch from the configured version.
- [x] Production resume works without manual branch restoration.
- [x] Completed but unreleased specs remain loose with
      `Release tag: unreleased` until they are selected for a future release.
- [x] Matching shipped specs are consolidated into
      `specs/release-X.Y.Z-consolidated.md` and removed from loose specs.
- [x] `CHANGELOG.md` has exactly one `1.10.2` header after repair.
- [x] Consolidated release records exist for `1.10.1` and `1.10.2`.

## Validation

- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `pytest paddle/frontend/tests/test_release_pr_body_script.py -q`
- `python scripts/validate_governance.py`
- `markdownlint` on changed Markdown files; `MD013` is non-blocking.
