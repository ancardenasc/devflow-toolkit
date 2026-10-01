---
name: commit
description: Create a git commit following the project's convention (Conventional Commits by default, or a custom template with the ticket id from the branch name). Reads the diff, proposes a message and asks for confirmation before committing. Single source of truth for commit format, so other skills call it in batch mode instead of duplicating the logic. Use when the user asks to commit or generate a commit message.
argument-hint: "[mode=batch; files=<list>; desc=<hint>]"
license: MIT
---

# /commit

Creates a commit following the repo convention. Never commits without explicit confirmation, except in batch mode.

## Configuration (`.devflow.yml`, all optional)

- `commit.format`: `conventional` (default) or a template such as `"[{ticket}] {summary}"`.
- `commit.language`: language of the message (default `en`).
- `commit.attribution`: `false` by default. Add attribution trailers (e.g. `Co-Authored-By`) only when this is `true`.
- `tracker.ticket_pattern`: regex to find the ticket id in the branch name (default `[A-Z]+-\d+`).

If no `.devflow.yml` exists, use the defaults above.

## Modes

- **Standalone** (`/commit`, no args): full interactive flow, with confirmation before the commit.
- **Batch** (called by another skill with `args: "mode=batch; files=<list>; desc=<optional hint>"`): use the received files without asking about staging, build the message with the same convention and commit without individual confirmation. The calling skill owns its own aggregate gate.

## Step 1: Repo and state

```
git rev-parse --show-toplevel
git status --porcelain
git branch --show-current
```

Not a git repo: STOP and ask to move into the project. No changes at all: STOP with "Nothing to commit".

## Step 2: Staging

- Batch: `git add <files>` directly.
- Standalone with staged files: use only those.
- Standalone with nothing staged: show `git status --porcelain` and ask what to stage. Never `git add -A` / `git add .` blindly.
- Never stage files that look like secrets (`.env`, `*credentials*`, `*.pem`, keys) without warning first. This applies in batch mode too.

## Step 3: Ticket

Extract the first match of `tracker.ticket_pattern` from the branch name (case-insensitive, upper-case the result). No match: ask once, "Which ticket does this belong to? (id or 'none')". With the `conventional` format the ticket is optional and goes in the footer (`Refs: ABC-123`) only if known.

## Step 4: Read the diff

`git diff --staged`. Read the real diff, not just file names, to understand the purpose of the change.

## Step 5: Propose the message

- `conventional`: `type(scope): short imperative summary`. Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore. Scope is optional.
- Custom template: fill `{ticket}` and `{summary}`; omit the ticket part when there is none.
- One line, no trailing period, imperative mood. Add a short body (bullets explaining *why*) only when the diff is large and not self-explanatory.
- Language: `commit.language`.
- The message must reflect exactly what the diff does. Never invent content.

Standalone: show the proposed message and wait for confirm / edit / cancel.

## Step 6: Commit

Pass the message through a heredoc so multi-line bodies keep their formatting:

```
git commit -F - <<'MSG'
<message>
MSG
```

- Never `--no-verify` or bypass hooks, never `--amend`, unless explicitly asked.
- No attribution trailers unless `commit.attribution: true`.
- Afterwards run `git status` and show the short hash.

## Constraints

- Do not commit without confirmation (except batch mode).
- Do not use `git add -A` / `git add .` without listing first.
- Do not invent the ticket; ask.
- Do not write a message that does not match the diff.
- One commit per invocation.
