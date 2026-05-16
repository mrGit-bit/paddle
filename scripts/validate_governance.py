#!/usr/bin/env python3
"""Validate repository governance metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "docs" / "PROJECT_INSTRUCTIONS.md"
AGENTS = ROOT / "AGENTS.md"
BACKLOG = ROOT / "BACKLOG.md"
PROJECT_MAX_CHARS = 3200
PROJECT_TARGET_CHARS = 2600
AGENTS_MAX_CHARS = 2200
AGENTS_TARGET_CHARS = 1800


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def metadata(text: str, path: Path) -> tuple[str, str]:
    version = re.search(r"^Instruction Set Version: (.+)$", text, re.M)
    date = re.search(r"^Last Updated: (.+)$", text, re.M)
    if not version or not date:
        raise ValueError(f"{path}: missing instruction version or date header")
    return version.group(1).strip(), date.group(1).strip()


def routed_skills(agents_text: str) -> list[Path]:
    skill_names = sorted(set(re.findall(r"\$([a-z0-9-]+)", agents_text)))
    return [
        ROOT / ".codex" / "skills" / name / "SKILL.md"
        for name in skill_names
    ]


def backlog_errors(backlog_text: str) -> list[str]:
    errors: list[str] = []
    match = re.search(
        r"^## Pending Tasks$(?P<section>.*?)(?=^## |\Z)",
        backlog_text,
        re.M | re.S,
    )
    if not match:
        return [f"{BACKLOG.relative_to(ROOT)}: missing Pending Tasks section"]

    lines = match.group("section").splitlines()
    header_index = next(
        (
            index
            for index, line in enumerate(lines)
            if line.strip() == "| Requirement | IMP. | SIMP. | PRI. |"
        ),
        None,
    )
    if header_index is None:
        return [f"{BACKLOG.relative_to(ROOT)}: missing pending task table"]
    if (
        header_index + 1 >= len(lines)
        or lines[header_index + 1].strip() != "| --- | --- | --- | --- |"
    ):
        errors.append(
            f"{BACKLOG.relative_to(ROOT)}: malformed pending task table header"
        )

    task_rows: list[tuple[int, int, int, int]] = []
    previous_row_line: int | None = None
    blank_after_row = False
    for offset, line in enumerate(lines[header_index + 2 :], start=header_index + 3):
        stripped = line.strip()
        if not stripped:
            if previous_row_line is not None:
                blank_after_row = True
            continue
        if not stripped.startswith("|"):
            continue
        if blank_after_row:
            errors.append(
                f"{BACKLOG.relative_to(ROOT)}: blank line splits pending task table "
                f"before section line {offset}"
            )
            blank_after_row = False
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 4:
            errors.append(
                f"{BACKLOG.relative_to(ROOT)}: pending task row on section line "
                f"{offset} has {len(cells)} columns"
            )
            continue
        try:
            importance, simplicity, priority = (
                int(cells[1]),
                int(cells[2]),
                int(cells[3]),
            )
        except ValueError:
            errors.append(
                f"{BACKLOG.relative_to(ROOT)}: pending task row on section line "
                f"{offset} has non-numeric scoring columns"
            )
            continue
        expected_priority = importance * simplicity
        if priority != expected_priority:
            errors.append(
                f"{BACKLOG.relative_to(ROOT)}: pending task row on section line "
                f"{offset} has PRI {priority}; expected {expected_priority}"
            )
        task_rows.append((offset, importance, simplicity, priority))
        previous_row_line = offset

    for current, following in zip(task_rows, task_rows[1:]):
        if (current[3], current[2]) < (following[3], following[2]):
            errors.append(
                f"{BACKLOG.relative_to(ROOT)}: pending task row on section line "
                f"{following[0]} is out of priority order"
            )
            break

    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    project_text = read(PROJECT)
    agents_text = read(AGENTS)
    backlog_text = read(BACKLOG)

    project_meta = metadata(project_text, PROJECT)
    agents_meta = metadata(agents_text, AGENTS)
    if project_meta != agents_meta:
        errors.append(
            "Instruction headers differ: "
            f"{PROJECT.relative_to(ROOT)} has {project_meta}, "
            f"{AGENTS.relative_to(ROOT)} has {agents_meta}"
        )

    project_chars = len(project_text)
    if project_chars > PROJECT_MAX_CHARS:
        errors.append(
            f"{PROJECT.relative_to(ROOT)} is {project_chars} characters; "
            f"maximum is {PROJECT_MAX_CHARS}"
        )
    elif project_chars > PROJECT_TARGET_CHARS:
        warnings.append(
            f"{PROJECT.relative_to(ROOT)} is {project_chars} characters; "
            f"target is under {PROJECT_TARGET_CHARS}"
        )

    agents_chars = len(agents_text)
    if agents_chars > AGENTS_MAX_CHARS:
        errors.append(
            f"{AGENTS.relative_to(ROOT)} is {agents_chars} characters; "
            f"maximum is {AGENTS_MAX_CHARS}"
        )
    elif agents_chars > AGENTS_TARGET_CHARS:
        warnings.append(
            f"{AGENTS.relative_to(ROOT)} is {agents_chars} characters; "
            f"target is under {AGENTS_TARGET_CHARS}"
        )

    for skill in routed_skills(agents_text):
        if not skill.exists():
            errors.append(f"Missing required routed skill: {skill.relative_to(ROOT)}")

    errors.extend(backlog_errors(backlog_text))

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(
        "Governance validation passed: headers match and "
        f"{PROJECT.relative_to(ROOT)} is {project_chars} characters "
        "for ChatGPT project-instruction use; "
        f"{AGENTS.relative_to(ROOT)} is {agents_chars} characters "
        "for Codex router use; routed skills and backlog scoring are valid."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
