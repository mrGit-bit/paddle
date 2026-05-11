# Release 1.10.3 Consolidated Spec

## Release

- Tag: `1.10.3`
- Date: `2026-05-11`

## Sources

- `/workspaces/paddle/specs/040-faster-release-orchestrator.md`

## Shipped Scope

- Move release-prep work into the local release orchestrator so normal releases no longer depend on the release-prep GitHub workflow and PR.
- Keep promotion PRs, staging deployment, manual staging approval, production deployment, and remote version/migration verification.
- Add release-completion controls so duplicate changelog headers and missing release consolidation records are caught before a completed release reports success.

## Validation Summary

- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `pytest paddle/frontend/tests/test_release_pr_body_script.py -q`
- `python scripts/validate_governance.py`
- `markdownlint` on changed Markdown files; `MD013` is non-blocking.
