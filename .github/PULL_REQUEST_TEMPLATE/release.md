<!-- markdownlint-disable MD022 -->
<!-- markdownlint-disable MD041 -->
<!-- markdownlint-disable MD003 -->

## Release

- Version (`release-prep-no-ai.yml` input `version`): X.Y.Z
- Target branch (`release-prep-no-ai.yml` input `target_branch`): develop / staging / main
- Release branch: chore/release-vX.Y.Z

- Summary (from CHANGELOG)
  -

## Workflow runs

- [ ] `Release Prep (no-AI)` workflow run linked
- [ ] `CI (pytest + coverage)` workflow run linked

## Checklist (release-prep-no-ai.yml)

- [ ] `CHANGELOG.md` moved `Unreleased` entries to `## [X.Y.Z] - YYYY-MM-DD`
- [ ] `CHANGELOG.md` keeps an empty `## [Unreleased]` section
- [ ] `paddle/config/__init__.py` updated to `__version__ = "X.Y.Z"`
- [ ] PR title follows: `version(release): prepare release vX.Y.Z`

## CI checks (ci.yml)

- [ ] `pytest paddle/frontend/tests/ --cov=frontend.views --cov-report=term-missing --cov-fail-under=90`
- [ ] `pytest paddle/americano/tests/test_americano_views.py --cov=americano.views --cov-report=term-missing --cov-fail-under=90`

## Minimum smoke test (staging/main promotions)

- [ ] Login / logout
- [ ] All rankings page loads + pagination works
- [ ] Match list loads + pagination works
- [ ] Adding a Match works and updates players' stats and rankings
- [ ] Jugadores view loads and diplays players' stats and match history
- [ ] Americano view loads
- [ ] Static assets ok (CSS/JS/images)
- [ ] New version features work as expected
