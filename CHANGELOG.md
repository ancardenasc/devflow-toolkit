# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: [SemVer](https://semver.org/).

## [Unreleased]

## [0.2.0] - 2026-10-01

### Removed
- **devflow-portfolio** bundle and its `case-kit` skill. It moved to [ux-skills-es](https://github.com/ancardenasc/ux-skills-es), which also adds `case-study-writer`, Spanish and English templates and a corrected full MIT licence template. If you installed `devflow-portfolio`, install `case-kit` from `ux-skills-es` instead.

### Fixed
- The `case-kit` licence template in 0.1.0 shipped an abbreviated MIT text. It is gone from this repository; the full text lives in `ux-skills-es`.

## [0.1.0] - 2026-09-30

First public release.

### Added
- **devflow-core**: skills `start-task`, `execute-task` (split into `SKILL.md` + `references/`) and `commit`; agents `unit-test-writer`, `task-summary` and `task-reviewers`; hook `session-title` (Claude Code only); Copilot prompt `start-task`.
- **devflow-review**: read-only agents `code-review`, `code-clean` and `ux-review`; skill `review-ticket`; Copilot prompt `ticket-review`.
- **devflow-portfolio**: skill `case-kit`, a 10-phase case-study scaffold.
- One neutral source in `src/` generating Claude Code plugins (`plugins/`, marketplace) and GitHub Copilot output (`dist/copilot/`).
- Project configuration through a single `.devflow.yml` (tracker, VCS, commit format, commands, docs target, verification, reviewers).
- Optional profile `profiles/colombia.md` (NTC 5854) and a Jira + GitLab worked example.
- EN/ES documentation, authoring templates, install script, build/lint/smoke-test scripts and CI (validation, stale-output check, secret scan).

### Known limits
- The Copilot output follows the documented formats and is structure-checked in CI, but has not been run in a live Copilot session.
- `execute-task` and `review-ticket` have not been exercised end to end against a real tracker and pull request.
- Hooks are Claude Code only; MCP tool access for agents must be added by the user (see `examples/jira-gitlab/`).
