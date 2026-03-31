#!/usr/bin/env python3
"""Automate the documented repository release flow."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


VERSION_PATTERN = re.compile(r"^v?(?P<version>\d+\.\d+\.\d+)$")
CHECKLIST_ITEM_RE = re.compile(r"^-\s+(.*\S)\s*$", re.MULTILINE)
NO_CHECKS_REPORTED_RE = re.compile(r"no checks reported on the .+ branch", re.IGNORECASE)
TRACKING_LINE_RE = re.compile(r"^- (?P<field>Task ID|Plan|Spec|Release tag):\s*`(?P<value>[^`]+)`\s*$")
SAFE_PRIVATE_KEY_GROUP_OR_WORLD_MASK = 0o077
DEFAULT_PRIVATE_KEY_MODE = 0o600
class ReleaseError(RuntimeError):
    """Raised when the automated release flow cannot continue."""


@dataclass
class StepResult:
    name: str
    status: str
    detail: str


@dataclass
class ReleasePaths:
    repo_root: Path
    ssh_config: Path = field(init=False)
    staging_key: Path = field(init=False)
    prod_key: Path = field(init=False)
    specs_dir: Path = field(init=False)
    plans_dir: Path = field(init=False)
    changelog: Path = field(init=False)
    backmerge_script: Path = field(init=False)

    def __post_init__(self) -> None:
        private_dir = self.repo_root / ".codex" / "private" / "release_ssh"
        self.ssh_config = private_dir / "config"
        self.staging_key = private_dir / "staging-oracle-key.pem"
        self.prod_key = private_dir / "production-oracle-key.pem"
        self.specs_dir = self.repo_root / "specs"
        self.plans_dir = self.repo_root / "plans"
        self.changelog = self.repo_root / "CHANGELOG.md"
        self.backmerge_script = self.repo_root / "scripts" / "backmerge_main_to_develop.sh"


@dataclass
class ReleaseContext:
    repo_root: Path
    version: str
    version_tag: str
    paths: ReleasePaths
    steps: list[StepResult] = field(default_factory=list)

    @property
    def release_branch(self) -> str:
        return f"chore/release-{self.version_tag}"

    @property
    def prep_pr_title(self) -> str:
        return f"version(release): prepare release {self.version_tag}"


@dataclass
class ReleaseSourceSelection:
    matched: list[Path]
    skipped: list[Path]


def normalize_version(value: str) -> tuple[str, str]:
    match = VERSION_PATTERN.fullmatch(value.strip())
    if not match:
        raise ReleaseError(
            "Version must be in X.Y.Z or vX.Y.Z format, for example 1.6.0 or v1.6.0."
        )
    version = match.group("version")
    return version, f"v{version}"


def run_command(
    args: list[str],
    *,
    cwd: Path,
    capture_output: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    if args and args[0] == "gh":
        return run_gh_command(
            args,
            cwd=cwd,
            capture_output=capture_output,
            input_text=input_text,
        )
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=capture_output,
        input=input_text,
    )


def run_subprocess(
    args: list[str],
    *,
    cwd: Path,
    capture_output: bool,
    input_text: str | None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=capture_output,
        input=input_text,
        env=env,
    )


def command_output(stdout: str | None, stderr: str | None) -> str:
    parts = [part.strip() for part in (stdout, stderr) if part and part.strip()]
    return "\n".join(parts)


def command_error_output(exc: subprocess.CalledProcessError) -> str:
    return command_output(exc.stdout, exc.stderr) or "Command failed."


def build_env_without_gh_token_overrides() -> dict[str, str] | None:
    env = os.environ.copy()
    removed = False
    for name in ("GH_TOKEN", "GITHUB_TOKEN"):
        if name in env:
            env.pop(name, None)
            removed = True
    return env if removed else None


def should_retry_gh_without_env_tokens(exc: subprocess.CalledProcessError) -> bool:
    output = command_error_output(exc)
    return bool(
        re.search(r"Failed to log in to github\.com using token \((GH_TOKEN|GITHUB_TOKEN)\)", output)
        and re.search(r"The token in (GH_TOKEN|GITHUB_TOKEN) is invalid\.", output)
    )


def replay_output(completed: subprocess.CompletedProcess[str]) -> None:
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)


def run_gh_command(
    args: list[str],
    *,
    cwd: Path,
    capture_output: bool,
    input_text: str | None,
) -> subprocess.CompletedProcess[str]:
    effective_capture = True if not capture_output else capture_output
    try:
        completed = run_subprocess(
            args,
            cwd=cwd,
            capture_output=effective_capture,
            input_text=input_text,
        )
    except subprocess.CalledProcessError as exc:
        retry_env = build_env_without_gh_token_overrides()
        if retry_env is None or not should_retry_gh_without_env_tokens(exc):
            raise
        completed = run_subprocess(
            args,
            cwd=cwd,
            capture_output=effective_capture,
            input_text=input_text,
            env=retry_env,
        )
    if not capture_output:
        replay_output(completed)
    return completed


def run_json(args: list[str], *, cwd: Path) -> object:
    completed = run_command(args, cwd=cwd)
    output = completed.stdout.strip()
    return json.loads(output) if output else None


def add_step(context: ReleaseContext, name: str, status: str, detail: str) -> None:
    context.steps.append(StepResult(name=name, status=status, detail=detail))


def record_success(context: ReleaseContext, name: str, detail: str) -> None:
    add_step(context, name, "ok", detail)


def record_failure(context: ReleaseContext, name: str, detail: str) -> None:
    add_step(context, name, "failed", detail)


def ensure_command_available(command: str, *, cwd: Path) -> None:
    run_command(["bash", "-lc", f"command -v {command} >/dev/null"], cwd=cwd)


def ensure_gh_authenticated(*, cwd: Path) -> None:
    run_command(["gh", "auth", "status"], cwd=cwd)


def ensure_clean_synced_develop(context: ReleaseContext) -> None:
    cwd = context.repo_root
    branch = run_command(["git", "branch", "--show-current"], cwd=cwd).stdout.strip()
    if branch != "develop":
        raise ReleaseError(
            f"Release automation must start from develop, but the current branch is {branch}."
        )

    status = run_command(["git", "status", "--short"], cwd=cwd).stdout.strip()
    if status:
        raise ReleaseError(
            "Working tree is not clean. Stage, commit, or discard pending changes before /prompts:release."
        )

    run_command(["git", "fetch", "origin"], cwd=cwd)
    counts = run_command(
        ["git", "rev-list", "--left-right", "--count", "origin/develop...develop"],
        cwd=cwd,
    ).stdout.strip()
    behind, ahead = [int(part) for part in counts.split()]
    if behind or ahead:
        raise ReleaseError(
            "Local develop is not synchronized with origin/develop. Pull or push pending commits before /prompts:release."
        )


def display_path(path: Path, *, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def private_key_mode_is_safe(mode: int) -> bool:
    return bool(mode & 0o400) and not bool(mode & SAFE_PRIVATE_KEY_GROUP_OR_WORLD_MASK)


def normalize_private_key_permissions(path: Path, *, repo_root: Path) -> str | None:
    current_mode = path.stat().st_mode & 0o777
    if private_key_mode_is_safe(current_mode):
        return None

    try:
        path.chmod(DEFAULT_PRIVATE_KEY_MODE)
    except OSError as exc:
        return (
            f"{display_path(path, repo_root=repo_root)} has unsafe permissions "
            f"{current_mode:04o} and could not be set to {DEFAULT_PRIVATE_KEY_MODE:04o}: {exc}"
        )

    repaired_mode = path.stat().st_mode & 0o777
    if private_key_mode_is_safe(repaired_mode):
        return None

    return (
        f"{display_path(path, repo_root=repo_root)} has unsafe permissions "
        f"{current_mode:04o}; expected owner-only private-key permissions such as "
        f"{DEFAULT_PRIVATE_KEY_MODE:04o}, but the mode is still {repaired_mode:04o}."
    )


def validate_ssh_assets(paths: ReleasePaths) -> list[str]:
    errors: list[str] = []
    if not paths.ssh_config.exists():
        errors.append(
            "Missing .codex/private/release_ssh/config. Copy .codex/templates/release_ssh_config.example first."
        )
    if not paths.staging_key.exists():
        errors.append("Missing .codex/private/release_ssh/staging-oracle-key.pem.")
    if not paths.prod_key.exists():
        errors.append("Missing .codex/private/release_ssh/production-oracle-key.pem.")
    for key_path in (paths.staging_key, paths.prod_key):
        if key_path.exists():
            permission_error = normalize_private_key_permissions(key_path, repo_root=paths.repo_root)
            if permission_error:
                errors.append(permission_error)
    return errors


def parse_changelog_section(changelog_text: str, version: str) -> list[str]:
    pattern = rf"^## \[{re.escape(version)}\] - .*?\n(?P<body>.*?)(?=^## \[|\Z)"
    match = re.search(pattern, changelog_text, flags=re.M | re.S)
    if not match:
        return []
    body = match.group("body")
    return CHECKLIST_ITEM_RE.findall(body)


def build_staging_checks(changelog_text: str, version: str) -> list[str]:
    checks = [
        "Iniciar sesion y cerrar sesion sin errores.",
        "Abrir rankings y confirmar que la paginacion funciona.",
        "Abrir la lista de partidos y confirmar que la paginacion funciona.",
        "Crear un partido y confirmar que ranking y estadisticas se actualizan.",
        "Abrir Americano y confirmar que la vista carga correctamente.",
    ]
    release_items = parse_changelog_section(changelog_text, version)[:3]
    for item in release_items:
        checks.append(f"Validar el cambio liberado: {item}")
    return checks[:6]


def matches_workflow_run(
    run: dict[str, object],
    *,
    started_at: datetime,
    expected_identifiers: tuple[str, ...],
) -> bool:
    created_at = datetime.fromisoformat(str(run["createdAt"]).replace("Z", "+00:00"))
    if created_at < started_at - timedelta(seconds=5):
        return False
    if str(run.get("event", "")) != "workflow_dispatch":
        return False
    display_title = str(run.get("displayTitle", ""))
    return any(identifier and identifier in display_title for identifier in expected_identifiers)


def wait_for_workflow_run(
    workflow_file: str,
    started_at: datetime,
    *,
    cwd: Path,
    expected_identifiers: tuple[str, ...],
) -> dict[str, object]:
    for _ in range(60):
        runs = run_json(
            [
                "gh",
                "run",
                "list",
                "--workflow",
                workflow_file,
                "--limit",
                "20",
                "--json",
                "databaseId,createdAt,status,conclusion,url,displayTitle,event,headBranch",
            ],
            cwd=cwd,
        )
        assert isinstance(runs, list)
        dispatch_candidates = [
            run
            for run in runs
            if str(run.get("event", "")) == "workflow_dispatch"
            and datetime.fromisoformat(str(run["createdAt"]).replace("Z", "+00:00"))
            >= started_at - timedelta(seconds=5)
        ]
        exact_matches = [
            run
            for run in dispatch_candidates
            if matches_workflow_run(
                run,
                started_at=started_at,
                expected_identifiers=expected_identifiers,
            )
        ]
        if len(exact_matches) == 1:
            return exact_matches[0]
        if len(exact_matches) > 1:
            raise ReleaseError(
                f"Found multiple workflow runs for {workflow_file} matching the dispatched release identifiers."
            )
        if len(dispatch_candidates) == 1:
            return dispatch_candidates[0]
        if len(dispatch_candidates) > 1:
            raise ReleaseError(
                f"Found multiple workflow runs for {workflow_file} after dispatch and could not match one to this release."
            )
        time.sleep(5)
    raise ReleaseError(f"Could not find a workflow run for {workflow_file} after dispatch.")


def wait_for_run_completion(run_id: int, *, cwd: Path) -> None:
    run_command(["gh", "run", "watch", str(run_id), "--exit-status"], cwd=cwd, capture_output=False)


def find_pr(base: str, head: str, title: str, *, cwd: Path) -> dict[str, object] | None:
    prs = run_json(
        [
            "gh",
            "pr",
            "list",
            "--base",
            base,
            "--head",
            head,
            "--state",
            "open",
            "--json",
            "number,title,url",
        ],
        cwd=cwd,
    )
    assert isinstance(prs, list)
    for pr in prs:
        if str(pr["title"]) == title:
            return pr
    return None


def wait_for_pr(base: str, head: str, title: str, *, cwd: Path) -> dict[str, object]:
    for _ in range(60):
        pr = find_pr(base, head, title, cwd=cwd)
        if pr:
            return pr
        time.sleep(5)
    raise ReleaseError(f"Could not find PR '{title}' ({head} -> {base}).")


def create_or_reuse_promotion_pr(base: str, head: str, version_tag: str, *, cwd: Path) -> dict[str, object]:
    title = f"release: promote {head} to {base} for {version_tag}"
    existing = find_pr(base, head, title, cwd=cwd)
    if existing:
        return existing

    body = (
        f"Automated release promotion for {version_tag}.\n\n"
        f"- Base: {base}\n"
        f"- Head: {head}\n"
        f"- Gate: wait for CI before merge\n"
    )
    run_command(
        [
            "gh",
            "pr",
            "create",
            "--base",
            base,
            "--head",
            head,
            "--title",
            title,
            "--body",
            body,
        ],
        cwd=cwd,
    )
    return wait_for_pr(base, head, title, cwd=cwd)


def wait_for_required_checks(pr_number: int, *, cwd: Path) -> None:
    try:
        run_command(
            ["gh", "pr", "checks", str(pr_number), "--watch", "--required"],
            cwd=cwd,
            capture_output=False,
        )
    except subprocess.CalledProcessError as exc:
        if NO_CHECKS_REPORTED_RE.search(command_error_output(exc)):
            return
        raise


def merge_pr(pr_number: int, strategy: str, *, cwd: Path, delete_branch: bool) -> None:
    args = ["gh", "pr", "merge", str(pr_number), strategy]
    if delete_branch:
        args.append("--delete-branch")
    run_command(args, cwd=cwd, capture_output=False)


def deploy_environment(paths: ReleasePaths, host_alias: str, *, cwd: Path) -> None:
    run_command(["ssh", "-F", str(paths.ssh_config), host_alias], cwd=cwd, capture_output=False)


def prompt_continue(checks: list[str]) -> bool:
    print("\nStaging manual checks:")
    for index, check in enumerate(checks, start=1):
        print(f"{index}. {check}")
    response = input("\nContinue to production after these checks? [y/N]: ").strip().lower()
    return response in {"y", "yes"}


def parse_tracking_metadata(source: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in source.read_text(encoding="utf-8").splitlines():
        match = TRACKING_LINE_RE.match(line)
        if match:
            metadata[match.group("field")] = match.group("value")
    return metadata


def collect_release_sources(
    directory: Path,
    pattern: str,
    excluded_names: set[str],
    *,
    release_tag: str,
) -> ReleaseSourceSelection:
    matched: list[Path] = []
    skipped: list[Path] = []
    for path in sorted(directory.glob(pattern)):
        if path.name in excluded_names:
            continue
        if path.name.startswith("release-"):
            continue
        metadata = parse_tracking_metadata(path)
        source_release_tag = metadata.get("Release tag")
        if source_release_tag == release_tag:
            matched.append(path)
        else:
            skipped.append(path)
    return ReleaseSourceSelection(matched=matched, skipped=skipped)


def build_consolidated_markdown(kind: str, version: str, release_date: date, sources: list[Path]) -> str:
    title = f"# Release {version} Consolidated {kind.title()}\n"
    lines = [
        title,
        "",
        "## Release",
        "",
        f"- Release tag: `{version}`",
        f"- Release date: `{release_date.isoformat()}`",
        "- Consolidation status: post-release back-merge complete",
        "",
        "## Source Provenance",
        "",
    ]
    for source in sources:
        lines.append(f"- `{source.as_posix()}`")

    lines.extend(
        [
            "",
            "## Source Snapshots",
            "",
            "The following approved source files were consolidated for this release.",
            "",
        ]
    )

    for source in sources:
        lines.extend(
            [
                f"### `{source.as_posix()}`",
                "",
                "```md",
                source.read_text(encoding="utf-8").rstrip(),
                "```",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def commit_consolidation(
    context: ReleaseContext,
    spec_selection: ReleaseSourceSelection,
    plan_selection: ReleaseSourceSelection,
) -> None:
    spec_sources = spec_selection.matched
    plan_sources = plan_selection.matched
    if not spec_sources and not plan_sources:
        skipped_sources = spec_selection.skipped + plan_selection.skipped
        if skipped_sources:
            skipped_names = ", ".join(source.name for source in skipped_sources)
            record_success(
                context,
                "Consolidation",
                f"No loose spec or plan files were tagged for {context.version_tag}; left other loose files untouched ({skipped_names}).",
            )
            return
        record_success(context, "Consolidation", "No loose spec or plan files required consolidation.")
        return

    release_date = date.today()
    spec_target = context.paths.specs_dir / f"release-{context.version}-consolidated.md"
    plan_target = context.paths.plans_dir / f"release-{context.version}-consolidated.md"

    if spec_sources:
        spec_target.write_text(
            build_consolidated_markdown("spec", context.version, release_date, spec_sources),
            encoding="utf-8",
        )
    if plan_sources:
        plan_target.write_text(
            build_consolidated_markdown("plan", context.version, release_date, plan_sources),
            encoding="utf-8",
        )

    for source in spec_sources + plan_sources:
        source.unlink()

    add_targets: list[str] = []
    if spec_sources:
        add_targets.append(str(spec_target))
    if plan_sources:
        add_targets.append(str(plan_target))
    if add_targets:
        run_command(["git", "add", *add_targets], cwd=context.repo_root)
    for source in spec_sources + plan_sources:
        run_command(["git", "add", "-u", str(source)], cwd=context.repo_root)

    diff = run_command(["git", "diff", "--cached", "--name-only"], cwd=context.repo_root).stdout.strip()
    if not diff:
        record_success(context, "Consolidation", "No consolidation file changes were staged.")
        return

    run_command(
        ["git", "commit", "-m", f"docs(release): consolidate specs and plans for {context.version_tag}"],
        cwd=context.repo_root,
        capture_output=False,
    )
    run_command(["git", "push", "origin", "develop"], cwd=context.repo_root, capture_output=False)
    skipped_sources = spec_selection.skipped + plan_selection.skipped
    skipped_detail = ""
    if skipped_sources:
        skipped_names = ", ".join(source.name for source in skipped_sources)
        skipped_detail = f" Left unrelated loose files untouched: {skipped_names}."
    record_success(
        context,
        "Consolidation",
        f"Created consolidated release artifacts and pushed the develop update for {context.version_tag}.{skipped_detail}",
    )


def close_backmerge_prs(*, cwd: Path) -> None:
    prs = run_json(
        [
            "gh",
            "pr",
            "list",
            "--base",
            "develop",
            "--head",
            "main",
            "--state",
            "open",
            "--json",
            "number",
        ],
        cwd=cwd,
    )
    assert isinstance(prs, list)
    for pr in prs:
        run_command(
            [
                "gh",
                "pr",
                "close",
                str(pr["number"]),
                "--comment",
                "Closing because the release automation already back-merged origin/main into develop locally.",
            ],
            cwd=cwd,
            capture_output=False,
        )


def render_report(context: ReleaseContext) -> str:
    lines = [
        f"Release report for {context.version_tag}",
        "",
    ]
    for step in context.steps:
        lines.append(f"- [{step.status}] {step.name}: {step.detail}")
    return "\n".join(lines)


def run_release_flow(context: ReleaseContext) -> None:
    ensure_command_available("gh", cwd=context.repo_root)
    ensure_command_available("ssh", cwd=context.repo_root)
    ensure_gh_authenticated(cwd=context.repo_root)
    ensure_clean_synced_develop(context)
    ssh_errors = validate_ssh_assets(context.paths)
    if ssh_errors:
        raise ReleaseError(" ".join(ssh_errors))
    record_success(
        context,
        "Preflight",
        "Validated develop branch, clean synced git state, GitHub auth, and repo-local SSH assets.",
    )

    started_at = datetime.now(timezone.utc)
    run_command(
        [
            "gh",
            "workflow",
            "run",
            ".github/workflows/release-prep-no-ai.yml",
            "-f",
            f"version={context.version}",
            "-f",
            "target_branch=develop",
        ],
        cwd=context.repo_root,
    )
    workflow_run = wait_for_workflow_run(
        "release-prep-no-ai.yml",
        started_at,
        cwd=context.repo_root,
        expected_identifiers=(context.version, context.version_tag, context.prep_pr_title, context.release_branch),
    )
    wait_for_run_completion(int(workflow_run["databaseId"]), cwd=context.repo_root)
    record_success(
        context,
        "Release Prep Workflow",
        f"Completed successfully: {workflow_run['url']}",
    )

    prep_pr = wait_for_pr("develop", context.release_branch, context.prep_pr_title, cwd=context.repo_root)
    wait_for_required_checks(int(prep_pr["number"]), cwd=context.repo_root)
    merge_pr(int(prep_pr["number"]), "--squash", cwd=context.repo_root, delete_branch=True)
    record_success(
        context,
        "Release Prep PR",
        f"Squash-merged PR #{prep_pr['number']} and deleted {context.release_branch}.",
    )

    run_command(["git", "pull", "--ff-only", "origin", "develop"], cwd=context.repo_root)
    staging_pr = create_or_reuse_promotion_pr("staging", "develop", context.version_tag, cwd=context.repo_root)
    wait_for_required_checks(int(staging_pr["number"]), cwd=context.repo_root)
    merge_pr(int(staging_pr["number"]), "--merge", cwd=context.repo_root, delete_branch=False)
    record_success(
        context,
        "Develop to Staging PR",
        f"Merged PR #{staging_pr['number']} after required CI checks.",
    )

    deploy_environment(context.paths, "staging-update", cwd=context.repo_root)
    record_success(context, "Staging Deploy", "Executed ssh -F repo-local-config staging-update.")

    changelog_text = context.paths.changelog.read_text(encoding="utf-8")
    checks = build_staging_checks(changelog_text, context.version)
    if not prompt_continue(checks):
        add_step(context, "Staging Approval", "paused", "User declined production promotion after staging.")
        print(render_report(context))
        return

    record_success(context, "Staging Approval", "User approved promotion after staging validation.")
    prod_pr = create_or_reuse_promotion_pr("main", "staging", context.version_tag, cwd=context.repo_root)
    wait_for_required_checks(int(prod_pr["number"]), cwd=context.repo_root)
    merge_pr(int(prod_pr["number"]), "--merge", cwd=context.repo_root, delete_branch=False)
    record_success(
        context,
        "Staging to Main PR",
        f"Merged PR #{prod_pr['number']} after required CI checks.",
    )

    deploy_environment(context.paths, "prod-update", cwd=context.repo_root)
    record_success(context, "Production Deploy", "Executed ssh -F repo-local-config prod-update.")

    run_command([str(context.paths.backmerge_script), context.version], cwd=context.repo_root, capture_output=False)
    close_backmerge_prs(cwd=context.repo_root)
    record_success(context, "Back-merge", "Merged origin/main into local develop and pushed origin/develop.")

    spec_sources = collect_release_sources(
        context.paths.specs_dir,
        "[0-9][0-9][0-9]-*.md",
        set(),
        release_tag=context.version_tag,
    )
    plan_sources = collect_release_sources(
        context.paths.plans_dir,
        "20[0-9][0-9]-*.md",
        {"TEMPLATE.md"},
        release_tag=context.version_tag,
    )
    commit_consolidation(context, spec_sources, plan_sources)
    print(render_report(context))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="Release version in X.Y.Z or vX.Y.Z format.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path(__file__).resolve().parents[1]
    context: ReleaseContext | None = None
    try:
        version, version_tag = normalize_version(args.version)
        context = ReleaseContext(
            repo_root=repo_root,
            version=version,
            version_tag=version_tag,
            paths=ReleasePaths(repo_root),
        )
        run_release_flow(context)
        return 0
    except ReleaseError as exc:
        if context is not None:
            add_step(context, "Abort", "failed", str(exc))
            print(render_report(context), file=sys.stderr)
        print(f"Release automation failed: {exc}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else "Command failed."
        if context is not None:
            add_step(context, "Abort", "failed", stderr)
            print(render_report(context), file=sys.stderr)
        print(f"Release automation failed: {stderr}", file=sys.stderr)
        return exc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
