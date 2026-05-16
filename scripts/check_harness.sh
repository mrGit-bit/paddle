#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== Governance =="
python scripts/validate_governance.py

echo
echo "== Specs =="
python scripts/validate_specs.py

echo
echo "== Release Dry Run =="
python scripts/release_orchestrator.py --check

echo
echo "== Markdown =="
markdown_globs=(
  "AGENTS.md"
  "README.md"
  "RELEASE.md"
  "CHANGELOG.md"
  "docs/*.md"
  "specs/*.md"
  ".codex/skills/**/*.md"
  ".github/PULL_REQUEST_TEMPLATE/*.md"
)
if command -v markdownlint-cli2 >/dev/null 2>&1; then
  markdownlint-cli2 "${markdown_globs[@]}"
elif command -v markdownlint >/dev/null 2>&1; then
  markdownlint "${markdown_globs[@]}"
else
  echo "markdownlint or markdownlint-cli2 is required for Markdown validation." >&2
  exit 1
fi

echo
echo "Harness validation passed."
