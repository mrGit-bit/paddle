#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: ./scripts/backmerge_main_to_develop.sh <version>" >&2
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

VERSION="$1"
MERGE_MSG="merge(release): backmerge main into develop after v${VERSION}"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "[ERROR] Working tree is not clean. Commit/stash changes before backmerging." >&2
  exit 1
fi

echo "[INFO] Fetching latest refs from origin..."
git fetch origin

echo "[INFO] Checking out develop..."
git checkout develop

echo "[INFO] Pulling develop with fast-forward only..."
git pull --ff-only origin develop

echo "[INFO] Merging origin/main into develop..."
if ! git merge --no-ff -m "${MERGE_MSG}" origin/main; then
  if git diff --name-only --diff-filter=U | grep -q .; then
    echo "[ERROR] Merge conflicts detected. Resolve conflicts manually, then run:"
    echo "        git add <resolved-files>"
    echo "        git commit"
    echo "        git push origin develop"
    echo "        (or abort with: git merge --abort)"
    exit 1
  fi

  echo "[ERROR] Merge failed for a non-conflict reason. Please inspect git output." >&2
  exit 1
fi

echo "[INFO] Pushing develop to origin..."
git push origin develop

echo "[OK] Backmerge from origin/main to develop completed and pushed."
