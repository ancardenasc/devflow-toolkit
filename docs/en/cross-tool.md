# Claude Code and GitHub Copilot

One source, two outputs. You edit `src/`; `scripts/build.py` generates what each tool reads.

## What is shared and what is generated

| Asset type | Source | Claude Code output | Copilot output |
|---|---|---|---|
| Skill | `src/skills/<id>/SKILL.md` (+ `references/`, `assets/`) | `plugins/<bundle>/skills/<id>/` | `dist/copilot/skills/<id>/` |
| Agent | `src/agents/<id>.md` (neutral) | `plugins/<bundle>/agents/<id>.md` | `dist/copilot/agents/<id>.agent.md` |
| Prompt | `src/prompts/<id>.md` (neutral) | none (the skill already gives a slash command) | `dist/copilot/prompts/<id>.prompt.md` |
| Hook | `src/hooks/<id>/` | `plugins/<bundle>/hooks/` | not supported |

Skills use the open Agent Skills format (`SKILL.md` with `name` and `description`), which both tools read. Agents and prompts differ per tool, so a neutral file carries `claude:` and `copilot:` blocks that the generator translates:

| | Claude Code | Copilot |
|---|---|---|
| Agent file | `.claude/agents/x.md` | `.github/agents/x.agent.md` |
| Tool list | `tools: Read, Grep, Bash` | `tools: [read, search, execute]` |
| Model | `model: sonnet` | usually omitted (picker decides) |
| Prompt entry point | skill slash command | `.github/prompts/x.prompt.md` |

## Install locations

| Tool | Skills | Agents | Prompts |
|---|---|---|---|
| Claude Code | `.claude/skills/` | `.claude/agents/` | n/a |
| Copilot | `.github/skills/` | `.github/agents/` | `.github/prompts/` |

Copilot also scans `.claude/skills/`, so a project that already installed the Claude copy gets the skills in both tools. Copilot prompt files link to skills and agents with relative paths (`../skills/...`), which only resolve when installed under `.github/` as above. The smoke test checks this.

## Known differences

- **Hooks are Claude Code only.** `session-title` has no Copilot equivalent. `install.sh` cannot copy a hook; use the plugin, or register the script as a `SessionStart` hook in `.claude/settings.json`.
- **Agent tools.** The shipped agents are read-only with shell access, so they work with `gh` and `glab`. MCP tool names are product- and tool-specific, so you add them yourself; see [`examples/jira-gitlab/`](../../examples/jira-gitlab/).
- **Calling agents.** Claude Code calls them with its agent mechanism by exact name; in Copilot you select the custom agent. The skills describe both in neutral wording.
- **Models.** Claude agents pin `model: sonnet`. Change it in the installed file if you prefer another.
- **Not verified live in Copilot.** The Copilot output follows the documented formats and is structure-checked in CI, but it has not been run against a live Copilot session yet. Please open an issue if a field is rejected.

## Why not maintain two copies?

Hand-maintained duplicates drift. The generator plus CI (`build` must produce no diff) keeps both outputs in step with the source.
