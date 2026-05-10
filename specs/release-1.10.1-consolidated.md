# Release 1.10.1 Consolidated Spec

## Release

- Tag: `1.10.1`
- Date: `2026-05-07`

## Sources

- `specs/037-release-orchestrator-check-fallback.md`

## Shipped Scope

- Keep release automation moving when GitHub reports no required checks but
  visible PR checks are present.
- Avoid release back-merge failures caused by local GPG signing configuration.

## Validation Summary

- `python scripts/validate_governance.py`
- `markdownlint` on changed Markdown files; `MD013` is non-blocking.
- `pytest paddle/frontend/tests/test_release_orchestrator.py`
- `pytest paddle/frontend/tests/test_release_pr_body_script.py`
