#!/usr/bin/env python3
"""Build release PR body from template and CHANGELOG section."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def extract_release_section(changelog_text: str, version: str) -> str:
    pattern = rf"^## \[{re.escape(version)}\] - .*?\n(?P<body>.*?)(?=^## \[|\Z)"
    match = re.search(pattern, changelog_text, flags=re.M | re.S)
    if not match:
        raise ValueError(f"No section found for version {version} in CHANGELOG.md")
    body = match.group("body").strip("\n")
    if not body.strip():
        return "- (no notable changes)"
    return body


def render_release_pr_body(
    template_text: str, changelog_text: str, version: str, target_branch: str
) -> str:
    summary = extract_release_section(changelog_text, version)
    summary_block = "\n".join(f"  {line}" if line else "" for line in summary.splitlines())

    body = template_text
    body = body.replace("X.Y.Z", version)
    body = body.replace("develop / staging / main", target_branch)
    body = body.replace("chore/release-vX.Y.Z", f"chore/release-v{version}")
    body = body.replace("- Summary (from CHANGELOG)\n  -", f"- Summary (from CHANGELOG)\n{summary_block}")
    return body


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--target-branch", required=True)
    parser.add_argument(
        "--template-path",
        default=".github/PULL_REQUEST_TEMPLATE/release.md",
    )
    parser.add_argument("--changelog-path", default="CHANGELOG.md")
    parser.add_argument("--output-path", required=True)
    args = parser.parse_args()

    template_path = Path(args.template_path)
    changelog_path = Path(args.changelog_path)
    output_path = Path(args.output_path)

    template_text = template_path.read_text(encoding="utf-8")
    changelog_text = changelog_path.read_text(encoding="utf-8")

    body = render_release_pr_body(
        template_text=template_text,
        changelog_text=changelog_text,
        version=args.version,
        target_branch=args.target_branch,
    )
    output_path.write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
