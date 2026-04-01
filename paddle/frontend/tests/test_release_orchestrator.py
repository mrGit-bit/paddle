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


def test_validate_ssh_assets_repairs_unsafe_private_key_modes(tmp_path):
    paths = release_orchestrator.ReleasePaths(tmp_path)
    paths.ssh_config.parent.mkdir(parents=True, exist_ok=True)
    paths.ssh_config.write_text("Host staging-update\n", encoding="utf-8")
    paths.staging_key.write_text("staging\n", encoding="utf-8")
    paths.prod_key.write_text("production\n", encoding="utf-8")
    paths.staging_key.chmod(0o666)
    paths.prod_key.chmod(0o640)

    errors = release_orchestrator.validate_ssh_assets(paths)

    assert errors == []
    assert paths.staging_key.stat().st_mode & 0o777 == 0o600
    assert paths.prod_key.stat().st_mode & 0o777 == 0o600


def test_validate_ssh_assets_reports_unfixable_private_key_mode(monkeypatch, tmp_path):
    paths = release_orchestrator.ReleasePaths(tmp_path)
    paths.ssh_config.parent.mkdir(parents=True, exist_ok=True)
    paths.ssh_config.write_text("Host staging-update\n", encoding="utf-8")
    paths.staging_key.write_text("staging\n", encoding="utf-8")
    paths.prod_key.write_text("production\n", encoding="utf-8")
    paths.staging_key.chmod(0o666)

    original_chmod = release_orchestrator.Path.chmod

    def fake_chmod(self, mode):
        if self == paths.staging_key:
            raise PermissionError("chmod blocked")
        return original_chmod(self, mode)

    monkeypatch.setattr(release_orchestrator.Path, "chmod", fake_chmod)

    errors = release_orchestrator.validate_ssh_assets(paths)

    assert len(errors) == 1
    assert ".codex/private/release_ssh/staging-oracle-key.pem has unsafe permissions 0666" in errors[0]
    assert "could not be set to 0600" in errors[0]


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


def test_build_staging_checks_preserves_multiline_release_items():
    changelog = """## [Unreleased]

## [1.8.1] - 2026-04-02
### Changed
- `UI/UX`: `Parejas del siglo` y `Parejas catastróficas` now require at least
  5 matches instead of 3 before a pair is eligible for the rate-based tables.
"""

    checks = release_orchestrator.build_staging_checks(changelog, "1.8.1")

    assert (
        "Validar el cambio liberado: `UI/UX`: `Parejas del siglo` y `Parejas catastróficas` "
        "now require at least 5 matches instead of 3 before a pair is eligible for the rate-based tables."
        in checks
    )


def test_read_remote_version_uses_repo_ssh_config(tmp_path, monkeypatch):
    paths = release_orchestrator.ReleasePaths(tmp_path)
    calls = []

    def fake_run_command(args, *, cwd, capture_output=True, input_text=None):
        calls.append((args, cwd, capture_output, input_text))
        return subprocess.CompletedProcess(args, 0, stdout="1.7.0\n", stderr="")

    monkeypatch.setattr(release_orchestrator, "run_command", fake_run_command)

    remote_version = release_orchestrator.read_remote_version(paths, "staging", cwd=tmp_path)

    assert remote_version == "1.7.0"
    assert calls == [
        (
            [
                "ssh",
                "-F",
                str(paths.ssh_config),
                "staging",
                "sed -n 's/^__version__ = \"\\([^\"]\\+\\)\"$/\\1/p' ~/paddle/paddle/config/__init__.py",
            ],
            tmp_path,
            True,
            None,
        )
    ]


def test_verify_remote_version_records_success(monkeypatch):
    context = release_orchestrator.ReleaseContext(
        repo_root=Path("/tmp/repo"),
        version="1.7.0",
        version_tag="v1.7.0",
        paths=release_orchestrator.ReleasePaths(Path("/tmp/repo")),
    )
    target = release_orchestrator.DeployTarget(
        deploy_alias="staging-update",
        verify_alias="staging",
        display_name="Staging",
    )

    monkeypatch.setattr(release_orchestrator, "read_remote_version", lambda *args, **kwargs: "1.7.0")

    release_orchestrator.verify_remote_version(context, target, step_name="Staging Deploy")

    assert context.steps == [
        release_orchestrator.StepResult(
            name="Staging Deploy",
            status="ok",
            detail="Executed ssh deploy via staging-update and verified staging is on 1.7.0.",
        )
    ]


def test_verify_remote_version_raises_on_mismatch(monkeypatch):
    context = release_orchestrator.ReleaseContext(
        repo_root=Path("/tmp/repo"),
        version="1.7.0",
        version_tag="v1.7.0",
        paths=release_orchestrator.ReleasePaths(Path("/tmp/repo")),
    )
    target = release_orchestrator.DeployTarget(
        deploy_alias="prod-update",
        verify_alias="prod",
        display_name="Production",
    )

    monkeypatch.setattr(release_orchestrator, "read_remote_version", lambda *args, **kwargs: "1.6.1")

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.verify_remote_version(context, target, step_name="Production Deploy")

    assert (
        str(exc_info.value)
        == "Production deploy completed but prod reports version 1.6.1 instead of 1.7.0."
    )


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


def test_prompt_continue_raises_resume_guidance_when_not_interactive(capsys):
    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.prompt_continue(["Check one."], stdin_isatty=False)

    captured = capsys.readouterr()
    assert "Staging manual checks:" in captured.out
    assert "Check one." in captured.out
    assert "rerun `python scripts/release_orchestrator.py <version> --resume-from staging-approval" in str(
        exc_info.value
    )


def test_parse_args_accepts_resume_flags():
    args = release_orchestrator.parse_args(
        ["1.8.1", "--resume-from", "staging-approval", "--staging-approved"]
    )

    assert args.version == "1.8.1"
    assert args.resume_from == "staging-approval"
    assert args.staging_approved is True
    assert args.staging_declined is False


def test_resume_requires_staging_decision_for_resume_mode():
    args = release_orchestrator.parse_args(["1.8.1", "--resume-from", "staging-approval"])

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.resume_requires_staging_decision(args)

    assert "--resume-from staging-approval requires either --staging-approved or --staging-declined" in str(
        exc_info.value
    )


def test_resume_flags_require_resume_mode():
    args = release_orchestrator.parse_args(["1.8.1", "--staging-approved"])

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.resume_requires_staging_decision(args)

    assert "--staging-approved and --staging-declined are only valid with --resume-from staging-approval." in str(
        exc_info.value
    )


def test_parse_tracking_metadata_reads_task_and_release_fields(tmp_path):
    source = tmp_path / "022-release-slash-command.md"
    source.write_text(
        "# Example\n\n"
        "## Tracking\n\n"
        "- Task ID: `release-slash-command`\n"
        "- Plan: `plans/2026-03-16_release-slash-command.md`\n"
        "- Release tag: `v1.6.0`\n",
        encoding="utf-8",
    )

    metadata = release_orchestrator.parse_tracking_metadata(source)

    assert metadata == {
        "Task ID": "release-slash-command",
        "Plan": "plans/2026-03-16_release-slash-command.md",
        "Release tag": "v1.6.0",
    }


def test_collect_release_sources_only_includes_requested_release_tag(tmp_path):
    matching = tmp_path / "022-release-slash-command.md"
    matching.write_text(
        "# Matching\n\n"
        "## Tracking\n\n"
        "- Task ID: `release-slash-command`\n"
        "- Plan: `plans/2026-03-16_release-slash-command.md`\n"
        "- Release tag: `v1.6.0`\n",
        encoding="utf-8",
    )
    second = tmp_path / "023-future-scope.md"
    second.write_text(
        "# Other\n\n"
        "## Tracking\n\n"
        "- Task ID: `future-scope`\n"
        "- Plan: `plans/2026-03-17_future-scope.md`\n"
        "- Release tag: `v1.7.0`\n",
        encoding="utf-8",
    )
    consolidated = tmp_path / "release-1.6.0-consolidated.md"
    consolidated.write_text("# Consolidated\n", encoding="utf-8")

    explicit = tmp_path / "024-already-tagged.md"
    explicit.write_text(
        "# Explicit\n\n"
        "## Tracking\n\n"
        "- Task ID: `already-tagged`\n"
        "- Plan: `plans/2026-03-17_already-tagged.md`\n"
        "- Release tag: `v1.6.0`\n",
        encoding="utf-8",
    )

    selection = release_orchestrator.collect_release_sources(
        tmp_path,
        "[0-9][0-9][0-9]-*.md",
        set(),
        release_tag="v1.6.0",
    )

    assert selection.matched == [matching, explicit]
    assert selection.skipped == [second]


def test_collect_release_sources_excludes_named_template_files(tmp_path):
    included = tmp_path / "2026-03-17_release-fix.md"
    included.write_text(
        "# Plan\n\n"
        "## Tracking\n\n"
        "- Task ID: `release-fix`\n"
        "- Spec: `specs/099-release-fix.md`\n"
        "- Release tag: `v1.6.0`\n",
        encoding="utf-8",
    )
    template = tmp_path / "TEMPLATE.md"
    template.write_text("# Template\n", encoding="utf-8")

    selection = release_orchestrator.collect_release_sources(
        tmp_path,
        "*.md",
        {"TEMPLATE.md"},
        release_tag="v1.6.0",
    )

    assert selection.matched == [included]
    assert selection.skipped == []


def test_collect_release_sources_skips_unreleased_files(tmp_path):
    source = tmp_path / "031-example.md"
    source.write_text(
        "# Example\n\n"
        "## Tracking\n\n"
        "- Task ID: `example`\n"
        "- Plan: `plans/2026-03-27_example.md`\n"
        "- Release tag: `unreleased`\n",
        encoding="utf-8",
    )

    selection = release_orchestrator.collect_release_sources(
        tmp_path,
        "[0-9][0-9][0-9]-*.md",
        set(),
        release_tag="v1.7.0",
    )

    assert selection.matched == []
    assert selection.skipped == [source]


def test_run_command_retries_gh_without_invalid_env_tokens(monkeypatch):
    calls = []

    def fake_run(args, **kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise subprocess.CalledProcessError(
                1,
                args,
                stderr=(
                    "Failed to log in to github.com using token (GH_TOKEN)\n"
                    "The token in GH_TOKEN is invalid."
                ),
            )
        return subprocess.CompletedProcess(args, 0, stdout="ok\n", stderr="")

    monkeypatch.setenv("GH_TOKEN", "invalid")
    monkeypatch.setattr(release_orchestrator.subprocess, "run", fake_run)

    completed = release_orchestrator.run_command(["gh", "auth", "status"], cwd=Path("/tmp/repo"))

    assert completed.stdout == "ok\n"
    assert calls[0]["env"] is None
    assert "GH_TOKEN" not in calls[1]["env"]


def test_run_command_raises_when_gh_auth_retry_still_fails(monkeypatch):
    calls = []

    def fake_run(args, **kwargs):
        calls.append(kwargs)
        if len(calls) == 1:
            raise subprocess.CalledProcessError(
                1,
                args,
                stderr=(
                    "Failed to log in to github.com using token (GH_TOKEN)\n"
                    "The token in GH_TOKEN is invalid."
                ),
            )
        raise subprocess.CalledProcessError(
            1,
            args,
            stderr=(
                "Failed to log in to github.com account mrcorreoweb\n"
                "The token in /home/codespace/.config/gh/hosts.yml is invalid."
            ),
        )

    monkeypatch.setenv("GH_TOKEN", "invalid")
    monkeypatch.setattr(release_orchestrator.subprocess, "run", fake_run)

    with pytest.raises(subprocess.CalledProcessError):
        release_orchestrator.run_command(["gh", "auth", "status"], cwd=Path("/tmp/repo"))

    assert len(calls) == 2


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
        expected_identifiers=("1.6.0", "v1.6.0", "version(release): prepare release v1.6.0"),
    )

    assert run["databaseId"] == 11


def test_wait_for_workflow_run_accepts_single_dispatch_candidate_without_branch_match(monkeypatch):
    started_at = release_orchestrator.datetime(2026, 3, 26, 18, 32, 55, tzinfo=release_orchestrator.timezone.utc)
    runs = [
        {
            "databaseId": 23611535777,
            "createdAt": "2026-03-26T18:32:57Z",
            "event": "workflow_dispatch",
            "headBranch": "main",
            "displayTitle": "Release Prep (no-AI)",
            "url": "https://example.test/runs/23611535777",
        }
    ]

    monkeypatch.setattr(release_orchestrator, "run_json", lambda args, cwd: runs)
    monkeypatch.setattr(release_orchestrator.time, "sleep", lambda seconds: None)

    run = release_orchestrator.wait_for_workflow_run(
        "release-prep-no-ai.yml",
        started_at,
        cwd=Path("/tmp/repo"),
        expected_identifiers=("1.6.0", "v1.6.0", "version(release): prepare release v1.6.0"),
    )

    assert run["databaseId"] == 23611535777


def test_wait_for_required_checks_ignores_no_checks_reported(monkeypatch):
    def fake_run_command(args, *, cwd, capture_output=True, input_text=None):
        raise subprocess.CalledProcessError(
            1,
            args,
            output="no checks reported on the 'chore/release-v1.6.0' branch\n",
        )

    monkeypatch.setattr(release_orchestrator, "run_command", fake_run_command)

    release_orchestrator.wait_for_required_checks(83, cwd=Path("/tmp/repo"))


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

    def fail_run_release_flow(passed_context, passed_args):
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
