#!/usr/bin/env bash
set -euo pipefail

# Auto-commit and push any changes, but only if there are changes.
# Usage: ./scripts/push.sh [commit message]

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

msg=${1:-"chore: auto-save $(date -Iseconds)"}

# Ensure we have a main branch
default_branch=$(git symbolic-ref --short HEAD || echo "main")

if git diff --quiet && git diff --cached --quiet; then
  echo "Nothing to commit. Working tree clean."
  exit 0
fi

git add -A
git commit -m "$msg"

git push -u origin "$default_branch"

echo "Pushed to origin/$default_branch with message: $msg"
