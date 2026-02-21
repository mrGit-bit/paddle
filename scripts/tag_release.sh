#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: ./scripts/tag_release.sh <version> \"<summary>\"" >&2
}

if [[ $# -ne 2 ]]; then
  usage
  exit 1
fi

VERSION="$1"
SUMMARY="$2"
TAG="v${VERSION}"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "[ERROR] Working tree is not clean. Commit/stash changes before tagging." >&2
  exit 1
fi

echo "[INFO] Fetching latest refs and tags from origin..."
git fetch --tags origin

echo "[INFO] Checking out main..."
git checkout main

echo "[INFO] Pulling main with fast-forward only..."
git pull --ff-only origin main

if git rev-parse -q --verify "refs/tags/${TAG}" >/dev/null; then
  echo "[ERROR] Tag ${TAG} already exists locally." >&2
  exit 1
fi

if git ls-remote --exit-code --tags origin "refs/tags/${TAG}" >/dev/null 2>&1; then
  echo "[ERROR] Tag ${TAG} already exists on origin." >&2
  exit 1
fi

echo "[INFO] Creating annotated tag ${TAG}..."
git tag -a "${TAG}" -m "${SUMMARY}"

echo "[INFO] Pushing tag ${TAG} to origin..."
git push origin "${TAG}"

echo "[OK] Release tag ${TAG} created and pushed successfully."
