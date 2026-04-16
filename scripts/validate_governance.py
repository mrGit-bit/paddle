#!/usr/bin/env python3
"""Validate repository governance metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "docs" / "PROJECT_INSTRUCTIONS.md"
AGENTS = ROOT / "AGENTS.md"
PROJECT_MAX_CHARS = 7800
PROJECT_TARGET_CHARS = 7000


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def metadata(text: str, path: Path) -> tuple[str, str]:
    version = re.search(r"^Instruction Set Version: (.+)$", text, re.M)
    date = re.search(r"^Last Updated: (.+)$", text, re.M)
    if not version or not date:
        raise ValueError(f"{path}: missing instruction version or date header")
    return version.group(1).strip(), date.group(1).strip()


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    project_text = read(PROJECT)
    agents_text = read(AGENTS)

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

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(
        "Governance validation passed: headers match and "
        f"{PROJECT.relative_to(ROOT)} is {project_chars} characters."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
