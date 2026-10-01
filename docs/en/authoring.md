# Authoring: adding or changing an asset

## Setup

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

## Workflow

1. Write the source under `src/` (templates in [`templates/`](../../templates/)).
2. Add an entry to `catalog.yml` with `id`, `type`, `bundle`, `description` and `description_es`.
3. Generate and check:
   ```
   .venv/bin/python scripts/build.py
   .venv/bin/python scripts/gen_readme.py
   .venv/bin/python scripts/lint.py
   .venv/bin/python scripts/smoke_install.py
   claude plugin validate . --strict
   ```
4. Commit the source **and** the generated output together. CI fails if they disagree.

Only edit `src/` and `catalog.yml`. `plugins/`, `dist/` and the README catalog tables are generated.

## Formats

**Skill** (`src/skills/<id>/SKILL.md`)
```yaml
---
name: my-skill            # equals the folder name, kebab-case, max 64
description: What it does and when to use it. Max 1024 characters.
argument-hint: "[arg]"    # optional
license: MIT
---
```
Keep `SKILL.md` under 500 lines and move step detail to `references/` (one level deep). Put reusable text in `assets/`.

**Agent** (`src/agents/<id>.md`)
```yaml
---
name: my-agent
description: What it does and when to call it.
claude:  { tools: "Read, Grep, Bash", model: sonnet, color: green }
copilot: { title: My Agent, tools: [read, search, execute] }
---
```

**Prompt** (`src/prompts/<id>.md`), usually Copilot only
```yaml
---
name: my-prompt
description: ...
targets: [copilot]
copilot: { agent: agent, tools: [read, search] }
---
```
Link to skills and agents with relative paths as installed (`../skills/<id>/SKILL.md`, `../agents/<id>.agent.md`).

**Hook** (`src/hooks/<id>/hooks.json` + script). Claude Code only. Quote `${CLAUDE_PLUGIN_ROOT}` in the command.

## Rules for generic content

- **No company or personal data**: no company names, ticket prefixes, tenant ids, field ids, people, internal URLs, absolute paths. The linter blocks known terms.
- **Values come from `.devflow.yml`**, never from the asset. Add a key to `.devflow.example.yml` and to the reference table when you need a new one.
- **Vendor-neutral wording**: say "the tracker tool" and give CLI examples (`gh`, `glab`); keep MCP tool names out of agent frontmatter.
- **Read-only unless the job is to write.** Reviewers get `Read, Grep, Glob, Bash`.
- **Fail loudly.** If an input is missing (ticket, diff), report an incomplete result, never "no findings".
- **Evidence over claims.** Require pasted output for completed steps.
- **English assets**, with Spanish only in `description_es` and `docs/es`.
- **YAML descriptions** containing `: ` must be quoted. The linter catches invalid frontmatter.

## What CI checks

Frontmatter and names, description length, `SKILL.md` size, forbidden terms, relative links in generated Copilot output, stale generated files, `claude plugin validate`, the install smoke test and a secret scan.

## Versioning

SemVer in `catalog.yml` (`version`), a `CHANGELOG.md` entry per release, a git tag `vX.Y.Z`. Users on the plugin marketplace update when the version changes.
