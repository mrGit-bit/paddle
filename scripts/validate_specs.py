#!/usr/bin/env python3
"""Validate active SDD spec metadata and required sections."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPECS_DIR = ROOT / "specs"
SPEC_NAME_RE = re.compile(r"^[0-9]{3}-[a-z0-9-]+\.md$")
SEMVER_TAG_RE = re.compile(r"^v[0-9]+\.[0-9]+\.[0-9]+$")
TRACKING_LINE_RE = re.compile(
    r"^- (?P<field>Task ID|Status|Release tag):\s*`(?P<value>[^`]+)`\s*$"
)
REQUIRED_SECTIONS = (
    "Tracking",
    "Summary",
    "Scope",
    "Files Allowed to Change",
    "Files Forbidden to Change",
    "Execution Notes",
    "Acceptance",
    "Validation",
)
VALID_STATUSES = {"approved", "implemented"}


def active_specs() -> list[Path]:
    if not SPECS_DIR.exists():
        return []
    return [
        path
        for path in sorted(SPECS_DIR.glob("*.md"))
        if path.name != "TEMPLATE.md" and not path.name.startswith("release-")
    ]


def headings(text: str) -> set[str]:
    return {
        match.group("heading").strip()
        for match in re.finditer(r"^## (?P<heading>.+?)\s*$", text, flags=re.M)
    }


def tracking_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        match = TRACKING_LINE_RE.match(line)
        if match:
            metadata[match.group("field")] = match.group("value")
    return metadata


def validate_spec(path: Path) -> list[str]:
    errors: list[str] = []
    relative = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")

    if not SPEC_NAME_RE.match(path.name):
        errors.append(f"{relative}: active spec filename must match NNN-short-title.md")

    metadata = tracking_metadata(text)
    for field in ("Task ID", "Status", "Release tag"):
        if field not in metadata:
            errors.append(f"{relative}: missing tracking field `{field}`")

    status = metadata.get("Status")
    release_tag = metadata.get("Release tag")
    if status and status not in VALID_STATUSES:
        errors.append(
            f"{relative}: Status must be one of {', '.join(sorted(VALID_STATUSES))}; "
            f"found `{status}`"
        )
    if status == "approved" and release_tag != "unreleased":
        errors.append(f"{relative}: approved specs must use Release tag `unreleased`")
    if status == "implemented" and release_tag not in {"unreleased"} and not SEMVER_TAG_RE.match(release_tag or ""):
        errors.append(
            f"{relative}: implemented specs must use Release tag `unreleased` or a version tag like `v1.2.3`"
        )

    present_headings = headings(text)
    for section in REQUIRED_SECTIONS:
        if section not in present_headings:
            errors.append(f"{relative}: missing `## {section}` section")

    return errors


def main() -> int:
    specs = active_specs()
    errors: list[str] = []
    for spec in specs:
        errors.extend(validate_spec(spec))

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"Spec validation passed: {len(specs)} active spec file(s) checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
