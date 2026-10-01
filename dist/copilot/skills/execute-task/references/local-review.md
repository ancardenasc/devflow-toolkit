# Step 7: Local reviews (pre-commit, N passes)

They run BEFORE any commit and BEFORE any push, on the local working tree, not on a pushed PR/MR. The goal is to iterate as many times as needed without producing intermediate commits or pushes; the commit plan is built only in Step 9.

Revalidate tools (preflight) before launching.

## How to get the local diff

Correct even when no commit exists yet (`git diff <base>...HEAD` compares only commits and would be empty):

```bash
cd <repo directory>                          # the session cwd may not be a git repo; run everything inside the repo
BASE=$(git merge-base <base branch> HEAD)
git status --porcelain | grep '^??'          # untracked new files: review the list
git add -N -- <new files of the task>        # intent-to-add ONLY for files that belong to the task (stages no content)
git diff $BASE                               # working tree vs base: committed + uncommitted
git diff --name-only $BASE                   # file list (to decide whether the UX review applies)
```

- **Never `git add -N .`**: it would drag in scratch files, credentials (`.env`, `*.pem`) or files foreign to the task. If an untracked file looks like a secret or foreign, exclude it and tell the user.
- Untracked files outside the selection do not enter the diff: mention them so the user confirms they are not part of the task.
- Pass in each agent's prompt: `$BASE`, the base branch and the **repo directory**. Agents only run `git diff $BASE` inside that directory (this step already did the intent-to-add).
- Before every pass, re-run this block: fixes may have created new files that need `git add -N`.

## Run the reviews in parallel

First decide whether the UX review applies (project type table + `git diff --name-only $BASE` against `frontend_globs`), then launch every applicable review **in a single message with several simultaneous agent calls**, not one after another. They are read-only and independent (same diff, none consumes another's output), so a pass takes as long as the slowest, not the sum. If one agent fails or hangs, the others still return; re-launch only the failed one (applying the agent rule of the preflight).

When pasting outputs keep the order code-review, code-clean, ux-review (correctness first, craftsmanship after) even though they ran at once.

1. **code-review** (`subagents.code_review`), local-diff mode: ticket id (for requirements) + `$BASE`, no PR/MR. Checks security (OWASP Top 10), requirements, performance, design.
2. **code-clean** (`subagents.code_clean`). Mandatory on any diff that touches code (skip only if the diff is exclusively config/docs without logic). Craftsmanship, metrics; see the agent, do not duplicate its detail here.
3. **ux-review** (`subagents.ux_review`). Mandatory if the diff touches any file matching `frontend_globs`; a single file already triggers it. Not applicable to backend projects. WCAG 2.2 AA, Nielsen, configured `a11y.standards`, equitable design.

Paste each agent's real output (findings exactly as returned). Do not summarize as "no findings" without pasting the detail.

## Findings loop

- **Critical** (any of the three): fix locally (no commit, no push), then re-run **all the applicable reviews** automatically without asking, repeat until 0 critical.
- **Cap: `review.max_auto_passes` automatic passes (default 3)** for criticals. If criticals persist after the last one: STOP, show what persists and why, and ask the user (no endless loop).
- **Important / Minor**: list them and ask: `fix` (fix + re-run all) or `leave it, continue` (accept, leave the loop with that pending, documented).
- The loop ends when: 0 critical **and** (0 important/minor pending **or** the user explicitly accepted the remaining ones).
- **No `git commit` and no `git push` happens in this block**, however many passes it takes.
- After every pass update the state: pass number and accepted important/minor findings.
