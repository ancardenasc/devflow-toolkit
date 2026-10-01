---
name: case-kit
description: Scaffolds a portfolio case-study project with a 10-phase structure (framing, research, definition, design, validation, build, accessibility QA, launch, measurement, storytelling). Use when starting a new portfolio sample project or any project that needs a phased docs structure. Manual invocation only.
argument-hint: "[target-dir] [project-name]"
disable-model-invocation: true
license: MIT
---

# case-kit

Creates the folder structure and documents of a 10-phase portfolio case-study in a new directory.

## Usage

`/case-kit <target-dir> [project-name]`

- `target-dir`: where to create the project. Created if missing. Ask for it before writing anything if not given.
- `project-name`: inserted in the `docs/case-study.md` title and the `README.md` title. Ask if omitted.

## Steps

1. Copy the whole `template/` folder that sits next to this file (Claude Code: `${CLAUDE_SKILL_DIR}/template/`) into `target-dir`, preserving structure.
2. Make sure `src/` and `tests/` exist (keep the `.gitkeep` files; git ignores empty folders).
3. If `project-name` was given, replace `[Project name]` in `docs/case-study.md` and the first heading of `README.md` (`# Portfolio Blueprint`) with it. Leave the rest of the README: it is the phase guide.
4. In `LICENSE` replace `[Year]` with the current year (`date +%Y`, no need to ask) and `[Your Name]` with the author's name, asking only if it is unknown.
5. Never overwrite existing files in `target-dir`; list which ones were skipped.
6. Summarize what was created and remind the order: fill `docs/brief.md` (Phase 0) first, and do not advance a phase before its "Done when" criterion is met.

## Do not

- Initialize git, commit, or create remote repositories.
- Delete or overwrite existing content without asking.
