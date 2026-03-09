import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[3] / ".github" / "scripts" / "release_pr_body.py"
spec = importlib.util.spec_from_file_location("release_pr_body", SCRIPT_PATH)
release_pr_body = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(release_pr_body)


def test_render_release_pr_body_populates_summary_and_metadata():
    template = """## Release

- Version (`release-prep-no-ai.yml` input `version`): X.Y.Z
- Target branch (`release-prep-no-ai.yml` input `target_branch`): develop / staging / main
- Release branch: chore/release-vX.Y.Z

- Summary (from CHANGELOG)
  -
"""
    changelog = """## [Unreleased]

## [1.4.0] - 2026-03-07
### Changed
- Added release summary extraction.
- Uses template-driven PR body.
"""

    body = release_pr_body.render_release_pr_body(
        template_text=template,
        changelog_text=changelog,
        version="1.4.0",
        target_branch="staging",
    )

    assert "X.Y.Z" not in body
    assert "develop / staging / main" not in body
    assert "chore/release-vX.Y.Z" not in body
    assert "1.4.0" in body
    assert "staging" in body
    assert "chore/release-v1.4.0" in body
    assert "  ### Changed" in body
    assert "  - Added release summary extraction." in body
    assert "  - Uses template-driven PR body." in body


def test_extract_release_section_raises_for_missing_version():
    changelog = """## [Unreleased]

## [1.3.1] - 2026-02-20
- Existing changes.
"""

    try:
        release_pr_body.extract_release_section(changelog, "1.4.0")
        assert False, "Expected ValueError when version section is missing"
    except ValueError as exc:
        assert "1.4.0" in str(exc)
