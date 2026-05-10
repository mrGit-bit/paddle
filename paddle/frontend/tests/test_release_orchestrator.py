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


def test_next_patch_version_increments_patch_component():
    assert release_orchestrator.next_patch_version("1.10.2") == "1.10.3"


def test_move_unreleased_to_version_strict_rejects_duplicate_header():
    changelog = "## [Unreleased]\n\n- Added change.\n\n## [1.10.3] - 2026-05-10\n\n- Existing.\n"

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.move_unreleased_to_version_strict(
            changelog,
            "1.10.3",
            date(2026, 5, 10),
        )

    assert "already contains a release header for 1.10.3" in str(exc_info.value)


def test_move_unreleased_to_version_strict_rejects_empty_unreleased():
    changelog = "## [Unreleased]\n\n## [1.10.2] - 2026-05-10\n\n- Existing.\n"

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.move_unreleased_to_version_strict(
            changelog,
            "1.10.3",
            date(2026, 5, 10),
        )

    assert "Unreleased section is empty" in str(exc_info.value)


def test_prepare_local_release_commits_and_pushes_release_files(monkeypatch, tmp_path):
    repo_root = tmp_path
    (repo_root / "paddle" / "config").mkdir(parents=True)
    (repo_root / "CHANGELOG.md").write_text("## [Unreleased]\n\n- Added faster release.\n", encoding="utf-8")
    (repo_root / "paddle" / "config" / "__init__.py").write_text('__version__ = "1.10.2"\n', encoding="utf-8")
    commands = []

    def fake_run_command(args, *, cwd, capture_output=True, input_text=None):
        commands.append(args)
        if args[:3] == ["git", "diff", "--cached"]:
            return subprocess.CompletedProcess(args, 0, stdout="CHANGELOG.md\npaddle/config/__init__.py\n", stderr="")
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    monkeypatch.setattr(release_orchestrator, "run_command", fake_run_command)
    monkeypatch.setattr(release_orchestrator, "date", type("FakeDate", (), {"today": staticmethod(lambda: date(2026, 5, 10))}))
    context = release_orchestrator.ReleaseContext(
        repo_root=repo_root,
        version="1.10.3",
        version_tag="v1.10.3",
        paths=release_orchestrator.ReleasePaths(repo_root),
    )

    release_orchestrator.prepare_local_release(context)

    assert "## [1.10.3] - 2026-05-10" in (repo_root / "CHANGELOG.md").read_text(encoding="utf-8")
    assert (repo_root / "paddle" / "config" / "__init__.py").read_text(encoding="utf-8") == '__version__ = "1.10.3"\n'
    assert ["git", "commit", "--no-gpg-sign", "-m", "version(release): prepare release v1.10.3"] in commands
    assert ["git", "push", "origin", "develop"] in commands
    assert context.steps[-1].name == "Local Release Prep"


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


def test_build_develop_checks_includes_release_specific_items():
    changelog = """## [Unreleased]

## [1.6.0] - 2026-03-16
### Changed
- Added release command automation.
- Added repo-local SSH release config.
- Added final release reporting.
"""

    checks = release_orchestrator.build_develop_checks(changelog, "1.6.0")

    assert len(checks) == 5
    assert "Validar la logica del cambio liberado: Added release command automation." in checks


def test_build_staging_checks_preserves_multiline_release_items():
    changelog = """## [Unreleased]

## [1.8.1] - 2026-04-02
### Changed
- `UI/UX`: `Parejas del siglo` y `Parejas catastróficas` now require at least
  5 matches instead of 3 before a pair is eligible for the rate-based tables.
"""

    checks = release_orchestrator.build_staging_checks(changelog, "1.8.1")

    assert (
        "Validar en UI el cambio liberado: `UI/UX`: `Parejas del siglo` y `Parejas catastróficas` "
        "now require at least 5 matches instead of 3 before a pair is eligible for the rate-based tables."
        in checks
    )


def test_build_staging_checks_are_ui_oriented():
    checks = release_orchestrator.build_staging_checks("## [Unreleased]\n", "1.9.0")

    assert checks[0] == "Iniciar sesion y cerrar sesion sin errores visibles de interfaz."
    assert "render visual" in checks[1]


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


def test_read_remote_pending_migrations_uses_repo_ssh_config(tmp_path, monkeypatch):
    paths = release_orchestrator.ReleasePaths(tmp_path)
    calls = []

    def fake_run_command(args, *, cwd, capture_output=True, input_text=None):
        calls.append((args, cwd, capture_output, input_text))
        return subprocess.CompletedProcess(
            args,
            0,
            stdout="games\n [X] 0001_initial\n [ ] 0006_group_remove_player_unique_lower_name_and_more\n",
            stderr="",
        )

    monkeypatch.setattr(release_orchestrator, "run_command", fake_run_command)

    pending = release_orchestrator.read_remote_pending_migrations(paths, "staging", cwd=tmp_path)

    assert pending == ["0006_group_remove_player_unique_lower_name_and_more"]
    assert calls == [
        (
            [
                "ssh",
                "-F",
                str(paths.ssh_config),
                "staging",
                "cd ~/paddle/paddle && source ~/venv/bin/activate && python manage.py showmigrations --settings=config.settings.prod",
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

    migrations_applied = []
    monkeypatch.setattr(
        release_orchestrator,
        "apply_remote_migrations",
        lambda paths, host_alias, *, cwd: migrations_applied.append((paths, host_alias, cwd)),
    )
    monkeypatch.setattr(release_orchestrator, "read_remote_pending_migrations", lambda *args, **kwargs: [])
    monkeypatch.setattr(release_orchestrator, "read_remote_version", lambda *args, **kwargs: "1.7.0")

    release_orchestrator.verify_remote_version(context, target, step_name="Staging Deploy")

    assert migrations_applied == [(context.paths, "staging", Path("/tmp/repo"))]
    assert context.steps == [
        release_orchestrator.StepResult(
            name="Staging Deploy",
            status="ok",
            detail=(
                "Executed ssh deploy via staging-update, applied remote migrations, and verified "
                "staging is on 1.7.0 with no pending migrations."
            ),
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

    monkeypatch.setattr(release_orchestrator, "apply_remote_migrations", lambda *args, **kwargs: None)
    monkeypatch.setattr(release_orchestrator, "read_remote_pending_migrations", lambda *args, **kwargs: [])
    monkeypatch.setattr(release_orchestrator, "read_remote_version", lambda *args, **kwargs: "1.6.1")

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.verify_remote_version(context, target, step_name="Production Deploy")

    assert (
        str(exc_info.value)
        == "Production deploy completed but prod reports version 1.6.1 instead of 1.7.0."
    )


def test_verify_remote_version_raises_on_pending_migrations(monkeypatch):
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

    monkeypatch.setattr(release_orchestrator, "apply_remote_migrations", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        release_orchestrator,
        "read_remote_pending_migrations",
        lambda *args, **kwargs: ["0006_group_remove_player_unique_lower_name_and_more"],
    )

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.verify_remote_version(context, target, step_name="Staging Deploy")

    assert (
        str(exc_info.value)
        == "Staging deploy completed but staging still has pending migrations: "
        "0006_group_remove_player_unique_lower_name_and_more."
    )


def test_build_consolidated_markdown_builds_compact_summary_sections(tmp_path):
    source = tmp_path / "001-example.md"
    source.write_text(
        "# Example\n\n"
        "## Tracking\n\n"
        "- Task ID: `example`\n"
        "- Release tag: `v1.6.0`\n\n"
        "## Summary\n\n"
        "- Added the simplified SDD workflow.\n"
        "- Removed duplicate release-plan history.\n\n"
        "## Validation\n\n"
        "- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`\n"
        "- Manual review of release docs.\n",
        encoding="utf-8",
    )

    output = release_orchestrator.build_consolidated_markdown(
        "1.6.0",
        date(2026, 3, 16),
        [source],
    )

    assert "# Release 1.6.0 Consolidated Spec" in output
    assert "`" + source.as_posix() + "`" in output
    assert "## Shipped Scope" in output
    assert "- Added the simplified SDD workflow." in output
    assert "## Validation Summary" in output
    assert "- `pytest paddle/frontend/tests/test_release_orchestrator.py -q`" in output


def test_build_changelog_consolidation_review_flags_repeated_categories():
    changelog = """## [Unreleased]

## [1.9.1] - 2026-04-16

- `UI/UX`: First player detail change.
- `UI/UX`: Second player detail change.
- `UI/UX`: Third player detail change.
- `UI/UX`: Fourth player detail change.
- `Governance`: One governance change.
"""
    consolidated = """# Release 1.9.1 Consolidated Spec

## Shipped Scope

- Reworked player detail statistics.
- Cleaned ranking sort icons.
"""
    backlog = """| Requirement | IMP. | SIMP. | PRI. |
| --- | --- | --- | --- |
| Improve player detail statistics | 2 | 2 | 4 |
"""

    review = release_orchestrator.build_changelog_consolidation_review(
        "1.9.1",
        changelog,
        consolidated,
        backlog,
    )

    assert review == [
        "Changelog consolidation review for 1.9.1:",
        "- Release notes: 5 bullets; categories: UI/UX 4, Governance 1.",
        "- Consolidated shipped scope: 2 bullets available as source material.",
        "- Backlog requirements available for comparison: 1.",
        (
            "- Action: compress repetitive same-category bullets into grouped outcome summaries: "
            "UI/UX (4)."
        ),
    ]


def test_build_changelog_consolidation_review_accepts_compact_grouped_section():
    changelog = """## [Unreleased]

## [1.9.0] - 2026-04-07

- `Data`: Added group ownership.
- `UI/UX`: Scoped authenticated browsing.
- `Release`: Hardened release automation.
"""

    review = release_orchestrator.build_changelog_consolidation_review("1.9.0", changelog)

    assert review[-1] == "- Action: confirm the release notes are already compact and grouped by category."


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


def test_parse_args_accepts_next_patch_without_version():
    args = release_orchestrator.parse_args(["--next-patch"])

    assert args.version is None
    assert args.next_patch is True


def test_resolve_requested_version_derives_next_patch(tmp_path):
    paths = release_orchestrator.ReleasePaths(tmp_path)
    paths.version_file.parent.mkdir(parents=True)
    paths.version_file.write_text('__version__ = "1.10.2"\n', encoding="utf-8")
    args = release_orchestrator.parse_args(["--next-patch"])

    assert release_orchestrator.resolve_requested_version(args, paths) == ("1.10.3", "v1.10.3")


def test_resolve_requested_version_rejects_version_with_next_patch(tmp_path):
    paths = release_orchestrator.ReleasePaths(tmp_path)
    args = release_orchestrator.parse_args(["1.10.3", "--next-patch"])

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.resolve_requested_version(args, paths)

    assert "Use either an explicit version or --next-patch" in str(exc_info.value)


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
        "- Status: `implemented`\n"
        "- Release tag: `v1.6.0`\n",
        encoding="utf-8",
    )

    metadata = release_orchestrator.parse_tracking_metadata(source)

    assert metadata == {
        "Task ID": "release-slash-command",
        "Status": "implemented",
        "Release tag": "v1.6.0",
    }


def test_collect_release_sources_only_includes_requested_release_tag(tmp_path):
    matching = tmp_path / "022-release-slash-command.md"
    matching.write_text(
        "# Matching\n\n"
        "## Tracking\n\n"
        "- Task ID: `release-slash-command`\n"
        "- Status: `implemented`\n"
        "- Release tag: `v1.6.0`\n",
        encoding="utf-8",
    )
    second = tmp_path / "023-future-scope.md"
    second.write_text(
        "# Other\n\n"
        "## Tracking\n\n"
        "- Task ID: `future-scope`\n"
        "- Status: `implemented`\n"
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
        "- Status: `shipped`\n"
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
        "# Spec\n\n"
        "## Tracking\n\n"
        "- Task ID: `release-fix`\n"
        "- Status: `implemented`\n"
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
        "- Status: `approved`\n"
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
    assert selection.suspicious_unreleased == []


def test_collect_release_sources_flags_implemented_unreleased_specs(tmp_path):
    source = tmp_path / "031-example.md"
    source.write_text(
        "# Example\n\n"
        "## Tracking\n\n"
        "- Task ID: `example`\n"
        "- Status: `implemented`\n"
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
    assert selection.suspicious_unreleased == [source]


def test_collect_release_sources_skips_tagged_specs_until_cycle_is_closed(tmp_path):
    source = tmp_path / "032-approved-but-tagged.md"
    source.write_text(
        "# Example\n\n"
        "## Tracking\n\n"
        "- Task ID: `example`\n"
        "- Status: `approved`\n"
        "- Release tag: `v1.7.0`\n",
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


def test_commit_consolidation_writes_single_release_spec(monkeypatch, tmp_path, capsys):
    repo_root = tmp_path
    specs_dir = repo_root / "specs"
    specs_dir.mkdir()
    (repo_root / "CHANGELOG.md").write_text(
        "## [Unreleased]\n\n"
        "## [1.6.0] - 2026-03-16\n\n"
        "- `Governance`: Added one approved spec file per task.\n",
        encoding="utf-8",
    )
    (repo_root / "BACKLOG.md").write_text(
        "| Requirement | IMP. | SIMP. | PRI. |\n"
        "| --- | --- | --- | --- |\n"
        "| Simplify SDD release records | 2 | 2 | 4 |\n",
        encoding="utf-8",
    )
    source = specs_dir / "037-example.md"
    source.write_text(
        "# Example\n\n"
        "## Tracking\n\n"
        "- Task ID: `example`\n"
        "- Status: `implemented`\n"
        "- Release tag: `v1.6.0`\n\n"
        "## Summary\n\n"
        "- Added one approved spec file per task.\n\n"
        "## Validation\n\n"
        "- `pytest -q`\n",
        encoding="utf-8",
    )

    commands = []

    def fake_run_command(args, *, cwd, capture_output=True, input_text=None):
        commands.append(args)
        if args[:3] == ["git", "diff", "--cached"]:
            return subprocess.CompletedProcess(args, 0, stdout="specs/release-1.6.0-consolidated.md\n", stderr="")
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    monkeypatch.setattr(release_orchestrator, "run_command", fake_run_command)
    monkeypatch.setattr(release_orchestrator, "date", type("FakeDate", (), {"today": staticmethod(lambda: date(2026, 3, 16))}))

    context = release_orchestrator.ReleaseContext(
        repo_root=repo_root,
        version="1.6.0",
        version_tag="v1.6.0",
        paths=release_orchestrator.ReleasePaths(repo_root),
    )
    selection = release_orchestrator.ReleaseSourceSelection(matched=[source], skipped=[])

    release_orchestrator.commit_consolidation(context, selection)

    target = specs_dir / "release-1.6.0-consolidated.md"
    assert target.exists()
    assert not source.exists()
    assert target.read_text(encoding="utf-8").startswith("# Release 1.6.0 Consolidated Spec")
    assert ["git", "add", str(target)] in commands
    assert ["git", "commit", "-m", "docs(release): consolidate specs for v1.6.0"] in commands
    captured = capsys.readouterr()
    assert "Changelog consolidation review for 1.6.0:" in captured.out
    assert "- Backlog requirements available for comparison: 1." in captured.out


def test_commit_consolidation_fails_on_implemented_unreleased_specs(tmp_path):
    repo_root = tmp_path
    specs_dir = repo_root / "specs"
    specs_dir.mkdir()
    source = specs_dir / "037-example.md"
    source.write_text("# Example\n", encoding="utf-8")
    context = release_orchestrator.ReleaseContext(
        repo_root=repo_root,
        version="1.10.2",
        version_tag="v1.10.2",
        paths=release_orchestrator.ReleasePaths(repo_root),
    )
    selection = release_orchestrator.ReleaseSourceSelection(
        matched=[],
        skipped=[source],
        suspicious_unreleased=[source],
    )

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.commit_consolidation(context, selection)

    assert "037-example.md" in str(exc_info.value)
    assert "Release tag: unreleased" in str(exc_info.value)


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


def test_wait_for_pr_checks_uses_required_checks_when_configured(monkeypatch):
    calls = []

    def fake_run_command(args, *, cwd, capture_output=True, input_text=None):
        calls.append(args)
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    monkeypatch.setattr(release_orchestrator, "run_command", fake_run_command)
    monkeypatch.setattr(release_orchestrator.time, "sleep", lambda seconds: None)

    release_orchestrator.wait_for_pr_checks(83, cwd=Path("/tmp/repo"))

    assert len(calls) == 1
    assert calls[0][-1] == "--required"


def test_wait_for_pr_checks_uses_visible_checks_when_required_checks_are_not_configured(
    monkeypatch,
):
    calls = []

    def fake_run_command(args, *, cwd, capture_output=True, input_text=None):
        calls.append(args)
        if "--required" in args:
            raise subprocess.CalledProcessError(
                1,
                args,
                output="no required checks reported on the 'staging' branch\n",
            )
        return subprocess.CompletedProcess(args, 0, stdout="", stderr="")

    monkeypatch.setattr(release_orchestrator, "run_command", fake_run_command)
    monkeypatch.setattr(release_orchestrator.time, "sleep", lambda seconds: None)

    release_orchestrator.wait_for_pr_checks(83, cwd=Path("/tmp/repo"))

    assert calls == [
        ["gh", "pr", "checks", "83", "--watch", "--required"],
        ["gh", "pr", "checks", "83", "--watch"],
    ]


def test_wait_for_pr_checks_raises_when_checks_never_appear(monkeypatch):
    def fake_run_command(args, *, cwd, capture_output=True, input_text=None):
        raise subprocess.CalledProcessError(
            1,
            args,
            output="no checks reported on the 'chore/release-v1.6.0' branch\n",
        )

    monkeypatch.setattr(release_orchestrator, "run_command", fake_run_command)
    monkeypatch.setattr(release_orchestrator.time, "sleep", lambda seconds: None)

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.wait_for_pr_checks(83, cwd=Path("/tmp/repo"), base="staging", head="develop")

    assert str(exc_info.value) == (
        "No checks were reported for PR #83 (develop -> staging). "
        "Inspect with `gh pr checks 83` before continuing the release."
    )


def test_run_release_validation_suite_records_success(monkeypatch):
    commands = []
    changelog = "## [Unreleased]\n\n## [1.9.0] - 2026-04-07\n### Changed\n- Added release validation.\n"
    context = release_orchestrator.ReleaseContext(
        repo_root=Path("/tmp/repo"),
        version="1.9.0",
        version_tag="v1.9.0",
        paths=release_orchestrator.ReleasePaths(Path("/tmp/repo")),
    )
    context.paths.changelog.parent.mkdir(parents=True, exist_ok=True)
    context.paths.changelog.write_text(changelog, encoding="utf-8")

    def fake_run_subprocess(args, *, cwd, capture_output, input_text, env=None):
        commands.append((args, cwd, capture_output, input_text, env))
        return subprocess.CompletedProcess(args, 0, stdout="ok\n", stderr="")

    monkeypatch.setattr(release_orchestrator, "run_subprocess", fake_run_subprocess)

    release_orchestrator.run_release_validation_suite(context)

    assert [call[0] for call in commands] == [
        list(release_orchestrator.LOCAL_RELEASE_VALIDATION_COMMANDS[0]),
        list(release_orchestrator.LOCAL_RELEASE_VALIDATION_COMMANDS[1]),
    ]
    assert context.steps[-1] == release_orchestrator.StepResult(
        name="Local Release Validation",
        status="ok",
        detail="Passed the local CI-equivalent pytest and coverage commands on develop before staging promotion.",
    )


def test_run_release_validation_suite_raises_on_failure(monkeypatch):
    changelog = "## [Unreleased]\n\n## [1.9.0] - 2026-04-07\n### Changed\n- Added release validation.\n"
    context = release_orchestrator.ReleaseContext(
        repo_root=Path("/tmp/repo"),
        version="1.9.0",
        version_tag="v1.9.0",
        paths=release_orchestrator.ReleasePaths(Path("/tmp/repo")),
    )
    context.paths.changelog.parent.mkdir(parents=True, exist_ok=True)
    context.paths.changelog.write_text(changelog, encoding="utf-8")

    def fake_run_subprocess(args, *, cwd, capture_output, input_text, env=None):
        raise subprocess.CalledProcessError(1, args, output="", stderr="2 failed")

    monkeypatch.setattr(release_orchestrator, "run_subprocess", fake_run_subprocess)

    with pytest.raises(release_orchestrator.ReleaseError) as exc_info:
        release_orchestrator.run_release_validation_suite(context)

    assert "Local release validation failed before staging promotion on command" in str(exc_info.value)
    assert "2 failed" in str(exc_info.value)


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
