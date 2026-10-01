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
      mkdir -p "$target/.claude/$sub"
      for p in "$root"/plugins/*/"$sub"; do [ -d "$p" ] && cp -R "$p"/. "$target/.claude/$sub/"; done
    done ;;
  copilot)
    mkdir -p "$target/.github"
    cp -R "$root/dist/copilot/." "$target/.github/" ;;
  *) echo "unknown tool: $tool" >&2; exit 1 ;;
esac
echo "installed $tool assets into $target"
echo "next: cp $root/.devflow.example.yml $target/.devflow.yml and edit it"
