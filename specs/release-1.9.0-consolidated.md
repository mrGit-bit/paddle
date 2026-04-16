# Release 1.9.0 Consolidated Spec

## Release

- Tag: `1.9.0`
- Date: `2026-04-11`

## Sources

- `/workspaces/paddle/specs/037-simplify-sdd-single-spec-artifact.md`
- `/workspaces/paddle/specs/038-multi-group-support-with-hall-of-fame.md`

## Shipped Scope

- Replace the duplicated spec-plus-plan SDD workflow with one compact approved active-work spec per non-trivial task.
- Keep release consolidation, but reduce it to one compact consolidated spec record per shipped release.
- Replace the single hardcoded club data model with real groups while keeping each user/player linked to exactly one group in v1.
- Preserve public browsing through an aggregated `Hall of Fame` context for anonymous users.

## Validation Summary

- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`
- `markdownlint AGENTS.md docs/PROJECT_INSTRUCTIONS.md README.md RELEASE.md CHANGELOG.md specs/TEMPLATE.md specs/037-simplify-sdd-single-spec-artifact.md .codex/commands/release.md .codex/skills/governance-markdown-auditor/SKILL.md`
- Manually confirm the only active-work template lives in `specs/TEMPLATE.md`.
- Manually confirm release docs now describe one consolidated release spec per shipped version.
- `pytest paddle/frontend/tests/test_ranking.py -q`
- `pytest paddle/frontend/tests/test_views.py -q`
- `pytest paddle/frontend/tests/test_players_pages.py -q`
- `pytest paddle/americano/tests/test_americano_views.py -q`
- `node --test paddle/frontend/tests/js/registerForm.test.js paddle/frontend/tests/js/passwordValidation.test.js`
- Manually confirm anonymous landing page shows aggregate `Hall of Fame` branding and the extra `crea un grupo` CTA.
- Manually confirm existing records appear under `club moraleja` after migration.
