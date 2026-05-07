# Release 1.10.0 Consolidated Spec

## Release

- Tag: `1.10.0`
- Date: `2026-05-06`

## Sources

- `specs/036-medallero-public-page.md`

## Shipped Scope

- Add a public `Medallero` page showing medals earned from the first page of
  each ranking scope.
- Keep medal assignment backend-owned and consistent with existing group-aware
  ranking behavior.

## Validation Summary

- `python scripts/validate_governance.py`
- `markdownlint specs/036-medallero-public-page.md` when available; `MD013` is
  non-blocking.
- Focused Django tests for medal config, medal service, and public rendering.
