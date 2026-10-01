---
name: start-task
description: Start a development task end to end - fetch the ticket, pick the base branch, create a well-named branch, run baseline tests, push it and open a draft pull/merge request. Use when the user asks to start or kick off a task, optionally with a ticket id. Confirms before each step.
argument-hint: "[ticket-id]"
license: MIT
---

# /start-task

Sets up a task: ticket, branch, baseline tests, draft PR/MR. Ask for explicit confirmation before each step. Answer in `output_language` (default: the user's language).

## Configuration (`.devflow.yml`, all optional)

- `tracker.type` (`github` | `jira` | `linear` | `none`) and `tracker.ticket_pattern` (default `[A-Z]+-\d+`)
- `vcs.type` (`github` | `gitlab`), `vcs.default_branch` (default `main`), `vcs.assignee`
- `workflow.base_from_parent` (default `true`): branch from the parent ticket's branch when it exists
- `branch.pattern` (default `{ticket}-{slug}`), `branch.max_slug_length` (default `50`)
- `commands.test` (baseline test command)

Without the file: infer `vcs.type` from `git remote get-url origin`, assume `main`, and ask when unsure.

## Before starting (confirm)

```
? Ticket id (matches tracker.ticket_pattern, or "none"): [input]
? Project folder (only if the workspace has several repos; list the root folders as numbered options): [input]
```
Assignee comes from `vcs.assignee`; do not ask. Show the choices and wait for OK.

## Step 1: Ticket and base branch

Fetch the ticket (title, acceptance criteria, **parent** link) using the tracker tool available: MCP, `gh issue view <n> --json title,body,labels`, a CLI, or text pasted by the user. If it fails: STOP with "Could not fetch <id>: <error>. Check the id and your permissions."

Always check the parent (not just the epic) before choosing the base branch. Branch search uses plain git, because many VCS tool integrations cannot list branches:

```
IF workflow.base_from_parent AND the ticket has a parent (ID-Y):
  git fetch origin
  git branch -r | grep -i "<id-y lowercase>"
  1 match  -> base branch, then: git checkout <it> && git pull
  >1       -> list and ask which one
  0        -> tell the user the parent branch does not exist; ask (default branch or another)
ELSE:
  base = vcs.default_branch -> git checkout <base> && git pull
```

## Step 2: Branch name

Build it from `branch.pattern`: `{ticket}` lower-case, `{slug}` an English, semantic, kebab-case summary of the ticket title, at most `branch.max_slug_length` characters (the ticket prefix does not count). Example: `abc-1234-user-auth-flow`. Without a ticket: slug only.

Show it and ask to confirm. If rejected, ask for the user's name, validate kebab-case and length, confirm again.

## Step 3: Baseline tests

```bash
git checkout <base> && git pull
<commands.test>            # if unset: detect from package.json / Makefile / pyproject, or ask; skip only if the project has no tests
```
- All pass: record the count as baseline and continue.
- Failures: show the errors and STOP. Fix existing debt before starting new work.

## Step 4: Create the branch

```bash
git switch -c <branch-name>
```

## Step 5: Publish the branch

```bash
git push -u origin <branch-name>
```
If it fails: STOP and show the error (permissions, branch already exists remotely). Do not continue until the user resolves it. A VCS integration (GitHub/GitLab MCP) may be used instead of the CLI when available.

## Step 6: Open the draft PR/MR

First check whether an open PR/MR already exists for this source branch; if so, reuse it and show its URL.

- Title: `[<TICKET>] <Title Case summary>` (no ticket: just the summary). Always a draft.
- Body: fill `assets/pr-description.md` (next to this file; Claude Code: `${CLAUDE_SKILL_DIR}/assets/pr-description.md`) with concrete content, not generic text.
- Target: the base branch from Step 1. Assignee: `vcs.assignee` if set.

```bash
# GitHub
gh pr create --draft --base <base> --title "<title>" --body-file <file> [--assignee <user>]
# GitLab (title prefix "Draft: " marks a draft)
glab mr create --title "Draft: <title>" --description "<body>" --source-branch <branch> --target-branch <base> --remove-source-branch [--assignee <user>]
```

## Final summary

```
TASK STARTED
Ticket      <ID> - <title>
Base branch <branch>
New branch  <branch>
Tests       N passed / 0 failed
PR/MR       <url>
```
Next: start editing files, or run the `execute-task` skill for the full flow.

## Constraints

- Explicit confirmation before each step; the pause is simply ending the turn.
- Any failure: STOP and show the error.
- Baseline tests must pass first.
- Branch name validated before pushing.
- Never assume the default branch before checking the parent ticket (when `workflow.base_from_parent`).
- The PR/MR description follows the fixed template in `assets/pr-description.md`.
