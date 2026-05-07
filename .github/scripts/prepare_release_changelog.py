#!/usr/bin/env python3
"""Move CHANGELOG Unreleased notes into a dated release section."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


def move_unreleased_to_version(
    changelog_text: str,
    version: str,
    release_date: date,
) -> str:
    match = re.search(
        r"^## \[Unreleased\]\s*\n(?P<body>.*?)(?=^## \[|\Z)",
        changelog_text,
        flags=re.M | re.S,
    )
    if not match:
        raise ValueError("No '## [Unreleased]' section found in CHANGELOG.md")

    body = match.group("body").strip("\n")
    if not body.strip():
        body = "- (no notable changes)"

    unreleased_replacement = "## [Unreleased]\n\n"
    new_section = f"## [{version}] - {release_date.isoformat()}\n\n{body.strip()}\n\n"
    new_text = re.sub(
        r"^## \[Unreleased\]\s*\n.*?(?=^## \[|\Z)",
        unreleased_replacement,
        changelog_text,
        flags=re.M | re.S,
    )
    new_text = new_text.replace(
        unreleased_replacement,
        unreleased_replacement + new_section,
        1,
    )
    return re.sub(
        r"(?m)^## \[Unreleased\]\n+(?=## \[)",
        unreleased_replacement,
        new_text,
        count=1,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--changelog-path", default="CHANGELOG.md")
    args = parser.parse_args()

    path = Path(args.changelog_path)
    if not path.exists():
        raise SystemExit("CHANGELOG.md not found at repo root")

    today = date.today()
    new_text = move_unreleased_to_version(
        path.read_text(encoding="utf-8"),
        args.version,
        today,
    )
    path.write_text(new_text, encoding="utf-8")
    print(f"Updated CHANGELOG.md: created ## [{args.version}] - {today.isoformat()}")


if __name__ == "__main__":
    main()
