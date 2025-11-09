#!/usr/bin/env bash
set -euo pipefail

# Polling-based watcher: commits and pushes when there are changes.
# No external dependencies required.
#
# Usage:
#   ./scripts/auto-push-loop.sh [interval-seconds]
#
# Stop with Ctrl+C. Consider running under tmux/screen/systemd for persistence.

INTERVAL=${1:-20}
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

echo "[auto-push] Watching $REPO_DIR every ${INTERVAL}s..."

while true; do
  if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "[auto-push] Changes detected at $(date -Iseconds). Pushing..."
    ./scripts/push.sh "chore: autosave $(date -Iseconds)"
  fi
  sleep "$INTERVAL"
done
