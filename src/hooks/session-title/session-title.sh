#!/bin/bash
# Names a new Claude Code session after the current git branch (or the folder name).
# Needs: jq. Resumed sessions are left alone so a name you set is not overwritten.
command -v jq >/dev/null 2>&1 || exit 0
input=$(cat)
source=$(echo "$input" | jq -r '.source')
[[ "$source" == "startup" || "$source" == "clear" ]] || exit 0

name=$(git branch --show-current 2>/dev/null)
[[ -n "$name" ]] || name=$(basename "$PWD")

jq -n --arg title "$name" '{hookSpecificOutput: {hookEventName: "SessionStart", sessionTitle: $title}}'
