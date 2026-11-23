#!/usr/bin/env bash
# Install the OCA skills for Claude Code.
#   scripts/install.sh                  -> ~/.claude/skills (all your projects)
#   scripts/install.sh --project DIR    -> DIR/.claude/skills (one project)
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="$HOME/.claude/skills"
if [[ "${1:-}" == "--project" ]]; then
  [[ -n "${2:-}" ]] || { echo "usage: $0 [--project DIR]" >&2; exit 2; }
  target="$2/.claude/skills"
fi

mkdir -p "$target"
for dir in "$here"/skills/*/; do
  name="$(basename "$dir")"
  rm -rf "${target:?}/$name"
  cp -r "$dir" "$target/$name"
  echo "installed $name -> $target/$name"
done
echo "Restart Claude Code (or open a new session) to load the skills."
