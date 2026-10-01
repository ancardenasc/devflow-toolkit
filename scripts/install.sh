#!/usr/bin/env bash
# Manual installer. Usage: scripts/install.sh <claude|copilot> [target-dir]
#   claude  -> copies plugin skills/agents/commands into <target>/.claude (default: current dir)
#   copilot -> copies dist/copilot into <target>/.github (default: current dir)
set -euo pipefail
tool="${1:?usage: install.sh <claude|copilot> [target-dir]}"
target="${2:-.}"
root="$(cd "$(dirname "$0")/.." && pwd)"
case "$tool" in
  claude)
    for sub in skills agents commands; do
      for p in "$root"/plugins/*/"$sub"; do
        [ -d "$p" ] || continue
        mkdir -p "$target/.claude/$sub"
        cp -R "$p"/. "$target/.claude/$sub/"
      done
    done
    echo "note: hooks cannot be copied. To enable session-title, use the plugin marketplace" \
         "or register plugins/devflow-core/hooks/session-title.sh as a SessionStart hook in .claude/settings.json" ;;
  copilot)
    mkdir -p "$target/.github"
    cp -R "$root/dist/copilot/." "$target/.github/" ;;
  *) echo "unknown tool: $tool" >&2; exit 1 ;;
esac
echo "installed $tool assets into $target"
echo "next: cp $root/.devflow.example.yml $target/.devflow.yml and edit it"
