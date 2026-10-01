# AGENTS.md

Repository of reusable AI-assistant assets (Claude Code + GitHub Copilot).

- Edit only `src/` and `catalog.yml`. `plugins/`, `dist/` and the README tables are generated.
- After any change run: `.venv/bin/python scripts/build.py && .venv/bin/python scripts/lint.py`.
- Assets must stay generic: no company names, ticket prefixes, tenant ids, personal names or absolute paths. Project-specific values belong in `.devflow.yml`.
- Asset names are English kebab-case and equal the file/folder name.
- Skills follow the Agent Skills spec (`name`, `description`, SKILL.md under 500 lines; details in `references/`).
