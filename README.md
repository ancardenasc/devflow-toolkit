# devflow-toolkit

> Reusable skills, agents and prompts for **Claude Code** and **GitHub Copilot** that take a task from ticket to merge: start, implement with tests, review, document, ship.

[Leer en español](README.es.md)

Write once in `src/`, generate for both tools. Project conventions (tracker, VCS, commit format, test command, language) live in one `.devflow.yml`, so nothing is hardcoded to a company.

## Install

**Claude Code** (plugin marketplace)
```
/plugin marketplace add ancardenasc/devflow-toolkit
/plugin install devflow-core@devflow-toolkit
```

**GitHub Copilot / manual**
```
git clone https://github.com/ancardenasc/devflow-toolkit && cd devflow-toolkit
scripts/install.sh copilot /path/to/your/project   # or: claude
cp .devflow.example.yml /path/to/your/project/.devflow.yml
```

## What's inside

<!-- catalog:start -->
### Skills

| Name | Bundle | Description |
|---|---|---|
| `commit` | devflow-core | Conventional or ticket-prefixed commits from the staged diff, with confirmation and a batch mode for other skills. |
| `case-kit` | devflow-portfolio | Scaffolds a 10-phase portfolio case-study repo (brief, research, PRD, design, testing, accessibility, case study). |

### Agents

| Name | Bundle | Description |
|---|---|---|
| `unit-test-writer` | devflow-core | Writes unit tests (Jest/Vitest + Testing Library or Vue Test Utils) for behavior, with a11y checks and a red/green TDD flow. |
| `code-review` | devflow-review | Read-only review of correctness, OWASP security, performance, SOLID and error handling on a PR/MR or local diff. |
| `code-clean` | devflow-review | Read-only Clean Code gate - naming, functions, duplication, dead code, F.I.R.S.T tests and measured metrics. |
| `ux-review` | devflow-review | Read-only UX/accessibility review on frontend changes - WCAG 2.2 AA, Nielsen heuristics, equitable design. |
<!-- catalog:end -->

## Configuration

Copy [`.devflow.example.yml`](.devflow.example.yml) to your project root as `.devflow.yml`. Assets read it for ticket pattern, default branch, commit format, test/lint/build commands, docs target, accessibility standards and output language.

## How it works

`src/` (neutral) -> `scripts/build.py` -> `plugins/` (Claude) + `dist/copilot/` (Copilot). Skills use the open Agent Skills format shared by both tools; agents and prompts are translated per tool. See [AGENTS.md](AGENTS.md).

## Security

Assets can drive shell and tracker tools. Review before installing. See [SECURITY.md](SECURITY.md).

## Contributing & license

See [CONTRIBUTING.md](CONTRIBUTING.md). MIT, (c) 2026 Nicolas Cardenas.
