#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

HOOK_DIR=".git/hooks"
mkdir -p "$HOOK_DIR"

cat > "$HOOK_DIR/post-commit" <<'EOF'
#!/usr/bin/env bash
# Auto push right after a successful commit
set -e
repo_root="$(git rev-parse --show-toplevel)"
"$repo_root/scripts/push.sh" "chore: post-commit autosave $(date -Iseconds)" || echo "[post-commit] push failed"
EOF

chmod +x "$HOOK_DIR/post-commit"
echo "Installed post-commit hook. Any future 'git commit' will auto-push."
