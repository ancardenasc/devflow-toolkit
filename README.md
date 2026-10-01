# devflow-toolkit

[![validate](https://github.com/ancardenasc/devflow-toolkit/actions/workflows/validate.yml/badge.svg)](https://github.com/ancardenasc/devflow-toolkit/actions/workflows/validate.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![assets](https://img.shields.io/badge/assets-14-blue)
![tools](https://img.shields.io/badge/Claude%20Code%20%2B%20Copilot-supported-8A63D2)
![docs](https://img.shields.io/badge/docs-EN%20%7C%20ES-lightgrey)

**Skills, agents and prompts for Claude Code and GitHub Copilot that take a task from ticket to merge:** start it, implement it with tests, review it, document it and hand it over, without ever merging for you.

[Leer en español](README.es.md)

Write once in `src/`, generate for both tools. Your conventions (tracker, VCS, commit format, test command, language) live in one `.devflow.yml`, so nothing is hardcoded to a company.

```mermaid
flowchart LR
  T([Ticket]) --> S[start-task] --> P{{Plan}} --> D[TDD] --> R[3 local reviews]
  R --> C[commit] --> PR[PR/MR + CI] --> TS[task-summary] --> M([Ready, not merged])
```

## Why this exists

AI assistants write code fast and review it lightly. These assets add the discipline around that speed:

- **Gates with evidence.** A step is done only with pasted real output, never "should be fine".
- **Reviews before commits.** Correctness/security, Clean Code and UX/accessibility run on the local diff, as many passes as needed, before history is written.
- **Human decisions stay human.** Plan, commit plan and testers pause for your `go`. Reviewers are read-only. Nothing merges.
- **Portable.** No company conventions inside the assets; everything comes from `.devflow.yml`.

## Install

**Claude Code** (plugin marketplace)
```
/plugin marketplace add ancardenasc/devflow-toolkit
/plugin install devflow-core@devflow-toolkit
/plugin install devflow-review@devflow-toolkit
```

**GitHub Copilot, or manual**
```
git clone https://github.com/ancardenasc/devflow-toolkit && cd devflow-toolkit
scripts/install.sh copilot /path/to/your/project     # or: claude
cp .devflow.example.yml /path/to/your/project/.devflow.yml
```

Then run `/start-task` or `/execute-task`. Full walkthrough: [getting started](docs/en/getting-started.md).

## What's inside

<!-- catalog:start -->
### Skills

| Name | Bundle | Description |
|---|---|---|
| `commit` | devflow-core | Conventional or ticket-prefixed commits from the staged diff, with confirmation and a batch mode for other skills. |
| `case-kit` | devflow-portfolio | Scaffolds a 10-phase portfolio case-study repo (brief, research, PRD, design, testing, accessibility, case study). |
| `start-task` | devflow-core | Starts a task - ticket lookup, base branch from the parent ticket, named branch, baseline tests and a draft PR/MR. |
| `review-ticket` | devflow-review | Reviews a finished ticket - DoD check plus code-review, code-clean and ux-review agents, one consolidated report, optional publishing. |
| `execute-task` | devflow-core | Runs a whole task end to end - plan, TDD, local reviews, minimal commits, PR/MR with testing instructions, optional browser check and tester assignment; never merges. |

### Agents

| Name | Bundle | Description |
|---|---|---|
| `unit-test-writer` | devflow-core | Writes unit tests (Jest/Vitest + Testing Library or Vue Test Utils) for behavior, with a11y checks and a red/green TDD flow. |
| `code-review` | devflow-review | Read-only review of correctness, OWASP security, performance, SOLID and error handling on a PR/MR or local diff. |
| `code-clean` | devflow-review | Read-only Clean Code gate - naming, functions, duplication, dead code, F.I.R.S.T tests and measured metrics. |
| `ux-review` | devflow-review | Read-only UX/accessibility review on frontend changes - WCAG 2.2 AA, Nielsen heuristics, equitable design. |
| `task-summary` | devflow-core | Prepares you to explain a finished task out loud - what, why, how it works, one-line pitch and likely questions; saves a backup page. |
| `task-reviewers` | devflow-core | Proposes balanced testers by real sprint load (one design, one engineering) and, after confirmation, writes the ticket and PR/MR reviewers; never touches the assignee. |

### Prompts / commands

| Name | Bundle | Description |
|---|---|---|
| `start-task` | devflow-core | Copilot slash command that runs the start-task skill. |
| `ticket-review` | devflow-review | Copilot slash command for a full ticket review with an executive summary. |

### Hooks (Claude Code only)

| Name | Bundle | Description |
|---|---|---|
| `session-title` | devflow-core | Names each new Claude Code session after the git branch (Claude Code only). |
<!-- catalog:end -->

Bundles: **devflow-core** (workflow), **devflow-review** (read-only reviewers), **devflow-portfolio** (case-study scaffold). Install only what you need.

## Configuration

Copy [`.devflow.example.yml`](.devflow.example.yml) to your project root as `.devflow.yml`. Every key is optional. Minimal GitHub setup:

```yaml
tracker: { type: github }
vcs: { type: github, default_branch: main }
commands: { test: "npm test" }
```

Reference: [configuration](docs/en/configuration.md). Jira + GitLab with MCP servers: [`examples/jira-gitlab/`](examples/jira-gitlab/).

## One source, two tools

`src/` (neutral) -> `scripts/build.py` -> `plugins/` (Claude Code) and `dist/copilot/` (Copilot). Skills use the open Agent Skills format both tools read; agents and prompts are translated per tool. CI keeps generated files in step with the source. Details and known differences: [cross-tool](docs/en/cross-tool.md).

## Repository layout

```
src/            neutral sources (skills, agents, prompts, hooks)
plugins/        generated Claude Code plugins + marketplace
dist/copilot/   generated Copilot agents, prompts, skills
profiles/       optional country/company standards (e.g. NTC 5854)
examples/       worked setups (Jira + GitLab)
templates/      starting points for new assets
scripts/        build, lint, install, smoke test
docs/{en,es}/   documentation
catalog.yml     asset catalog; README tables are generated from it
```

## Documentation

[Getting started](docs/en/getting-started.md) · [Workflow](docs/en/workflow.md) · [Configuration](docs/en/configuration.md) · [Cross-tool](docs/en/cross-tool.md) · [Authoring](docs/en/authoring.md)

## Status and limits

Version 0.1. Structure, frontmatter and links are checked in CI and the Claude plugins load in a live session. The Copilot output follows the documented formats but has not been run in a live Copilot session yet, and the long flows (`execute-task`, `review-ticket`) have not been exercised against a real tracker and PR. Issues and feedback are welcome.

## Security

Assets can drive shell, git and tracker tools. Read an asset before installing it, and keep tokens in your own MCP/CLI configuration, never in this repo. See [SECURITY.md](SECURITY.md).

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). MIT, (c) 2026 Nicolas Cardenas.
