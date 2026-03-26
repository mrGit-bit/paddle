import importlib.util
import sys
from datetime import date
from pathlib import Path
import subprocess

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[3] / "scripts" / "release_orchestrator.py"
spec = importlib.util.spec_from_file_location("release_orchestrator", SCRIPT_PATH)
release_orchestrator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = release_orchestrator
spec.loader.exec_module(release_orchestrator)


def test_normalize_version_accepts_plain_and_prefixed_versions():
    assert release_orchestrator.normalize_version("1.6.0") == ("1.6.0", "v1.6.0")
    assert release_orchestrator.normalize_version("v1.6.0") == ("1.6.0", "v1.6.0")


def test_normalize_version_rejects_invalid_values():
    with pytest.raises(release_orchestrator.ReleaseError):
        release_orchestrator.normalize_version("release-1.6")


def test_validate_ssh_assets_reports_missing_config_and_keys(tmp_path):
    paths = release_orchestrator.ReleasePaths(tmp_path)

    errors = release_orchestrator.validate_ssh_assets(paths)

    assert "Missing .codex/private/release_ssh/config." in errors[0]
    assert "staging-oracle-key.pem" in errors[1]
    assert "production-oracle-key.pem" in errors[2]


def test_build_staging_checks_includes_release_specific_items():
    changelog = """## [Unreleased]

## [1.6.0] - 2026-03-16
### Changed
- Added release command automation.
- Added repo-local SSH release config.
- Added final release reporting.
"""

    checks = release_orchestrator.build_staging_checks(changelog, "1.6.0")

    assert len(checks) == 6
    assert "Validar el cambio liberado: Added release command automation." in checks


def test_build_consolidated_markdown_includes_provenance_and_snapshot(tmp_path):
    source = tmp_path / "001-example.md"
    source.write_text("# Example\n\nBody.\n", encoding="utf-8")

    output = release_orchestrator.build_consolidated_markdown(
        "spec",
        "1.6.0",
        date(2026, 3, 16),
        [source],
    )

    assert "# Release 1.6.0 Consolidated Spec" in output
    assert "`" + source.as_posix() + "`" in output
    assert "```md" in output
    assert "# Example" in output


def test_render_report_lists_step_statuses():
    context = release_orchestrator.ReleaseContext(
        repo_root=Path("/tmp/repo"),
        version="1.6.0",
        version_tag="v1.6.0",
        paths=release_orchestrator.ReleasePaths(Path("/tmp/repo")),
    )
    release_orchestrator.record_success(context, "Preflight", "All prerequisites satisfied.")
    release_orchestrator.add_step(context, "Staging Approval", "paused", "User declined production.")

    report = release_orchestrator.render_report(context)

    assert "Release report for v1.6.0" in report
    assert "- [ok] Preflight: All prerequisites satisfied." in report
    assert "- [paused] Staging Approval: User declined production." in report


def test_collect_release_sources_only_matches_current_release_version(tmp_path):
    matching = tmp_path / "022-release-slash-command.md"
    matching.write_text("Release checks for 1.6.0 and v1.6.0.\n", encoding="utf-8")
    unrelated = tmp_path / "023-future-scope.md"
    unrelated.write_text("Approved for a later release.\n", encoding="utf-8")

    selection = release_orchestrator.collect_release_sources(
        tmp_path,
        "[0-9][0-9][0-9]-*.md",
        set(),
        version="1.6.0",
        version_tag="v1.6.0",
    )

    assert selection.matched == [matching]
    assert selection.skipped == [unrelated]


def test_wait_for_workflow_run_prefers_exact_release_identifier(monkeypatch):
    started_at = release_orchestrator.datetime(2026, 3, 16, tzinfo=release_orchestrator.timezone.utc)
    runs = [
        {
            "databaseId": 10,
            "createdAt": "2026-03-16T00:00:02Z",
            "event": "workflow_dispatch",
            "headBranch": "develop",
            "displayTitle": "version(release): prepare release v1.5.9",
            "url": "https://example.test/runs/10",
        },
        {
            "databaseId": 11,
            "createdAt": "2026-03-16T00:00:03Z",
            "event": "workflow_dispatch",
            "headBranch": "develop",
            "displayTitle": "version(release): prepare release v1.6.0",
            "url": "https://example.test/runs/11",
        },
    ]

    monkeypatch.setattr(release_orchestrator, "run_json", lambda args, cwd: runs)
    monkeypatch.setattr(release_orchestrator.time, "sleep", lambda seconds: None)

    run = release_orchestrator.wait_for_workflow_run(
        "release-prep-no-ai.yml",
        started_at,
        cwd=Path("/tmp/repo"),
        expected_head_branch="develop",
        expected_identifiers=("1.6.0", "v1.6.0", "version(release): prepare release v1.6.0"),
    )

    assert run["databaseId"] == 11


def test_main_prints_partial_report_when_subprocess_fails(monkeypatch, capsys):
    context = release_orchestrator.ReleaseContext(
        repo_root=Path("/tmp/repo"),
        version="1.6.0",
        version_tag="v1.6.0",
        paths=release_orchestrator.ReleasePaths(Path("/tmp/repo")),
    )
    release_orchestrator.record_success(context, "Preflight", "All prerequisites satisfied.")

    monkeypatch.setattr(
        release_orchestrator,
        "parse_args",
        lambda argv: type("Args", (), {"version": "1.6.0"})(),
    )
    monkeypatch.setattr(release_orchestrator, "normalize_version", lambda value: ("1.6.0", "v1.6.0"))
    monkeypatch.setattr(release_orchestrator, "ReleasePaths", lambda repo_root: context.paths)

    def fail_run_release_flow(passed_context):
        release_orchestrator.record_success(passed_context, "Preflight", "All prerequisites satisfied.")
        raise subprocess.CalledProcessError(2, ["gh", "run", "watch"], stderr="gh watch failed")

    monkeypatch.setattr(release_orchestrator, "run_release_flow", fail_run_release_flow)

    exit_code = release_orchestrator.main(["1.6.0"])

    assert exit_code == 2
    stderr = capsys.readouterr().err
    assert "Release report for v1.6.0" in stderr
    assert "- [ok] Preflight: All prerequisites satisfied." in stderr
    assert "- [failed] Abort: gh watch failed" in stderr
    assert "Release automation failed: gh watch failed" in stderr
