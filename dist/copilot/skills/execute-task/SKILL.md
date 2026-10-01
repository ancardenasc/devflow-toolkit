---
name: execute-task
description: Execute a development task end to end - preflight, plan, TDD implementation, local reviews (code review, clean code, UX), minimal commits, PR/MR with testing instructions, optional browser verification, optional tester assignment, docs and a team summary, leaving the PR/MR ready but never merged. Use when the user asks to execute or complete a whole task for a ticket. Runs in the main thread so it can pause for confirmation at each gate.
argument-hint: "[ticket-id]"
license: MIT
---

# /execute-task

Senior engineer: plan, implement, review locally, leave the PR/MR ready (never merged). Explicit pauses and confirmations at every gate. Answer in `output_language` (default: the user's language).

This skill orchestrates agents for bounded, isolable tasks: `code-review`, `code-clean`, `ux-review`, `unit-test-writer`, `task-summary` and, optionally, `task-reviewers`. Call them through the tool's agent mechanism with the exact agent name (never as free text), always from the main thread and never nested, so the evidence rule can paste each agent's real output. Names come from `subagents.*` in `.devflow.yml`. Commits go through the `commit` skill in batch mode (single source of truth for message format; do not duplicate it here). Everything else runs in this thread because it must pause and wait for the user turn by turn.

Detail for each step lives in `references/`, next to this file (Claude Code: `${CLAUDE_SKILL_DIR}/references/`). Read the reference of a step when you reach it.

## Configuration (`.devflow.yml`, all optional)

See `.devflow.example.yml` in the toolkit. Keys this skill uses: `tracker.*`, `vcs.*`, `workflow.base_from_parent`, `branch.*`, `commands.{test,lint,build}`, `frontend_globs`, `docs.*`, `output_language`, `subagents.*`, `review.max_auto_passes` (default 3), `code_style.comments` (`none` | `minimal`, default `minimal`), `verify.*` (browser verification, off by default), `environment.services` (for the testing-environment table), `workflow.assign_testers` (default `false`), `tracker.fields.tester`.

## Step map

```
0   Checklist + persistent state
1   Preflight of tools                      -> references/preflight.md
2   Ticket + base branch                    -> same logic as the start-task skill, steps 1-2
3   Branch name (propose only)
    PAUSE  Plan (read-only)
4   Branch + baseline + draft PR/MR
5   Execute phases (TDD)                    -> references/tdd-phases.md
6   Final tests
7   Local reviews (N passes; PAUSE on important/minor)   -> references/local-review.md
8   Full PR/MR description + testing instructions        -> references/pr-description.md
8b  Browser verification (opt-in)                        -> references/browser-verification.md
9   Commits (PAUSE, once)                   -> references/ship.md
10  Push + sync with base + CI              -> references/ship.md
11  Documentation (if chosen) + tester proposal (if enabled)   -> references/ship.md
12  Assign testers + testing instructions on the ticket (PAUSE) -> references/ship.md
    GATE   Pre-merge
13  Mark ready + final summary              -> references/ship.md
14  Team summary                            -> references/team-summary.md
```

## Before starting

**Ticket id**: before asking, check whether the current session name (e.g. set with `/rename`) contains a match of `tracker.ticket_pattern`. If so, propose it for confirmation instead of assuming silently.

```
? Ticket id: [input or confirmation of the detected one]
? Project type: [1: frontend/design] [2: backend] [3: other]
? Documentation at the end (y/n): [input]
? (frontend only, if verify is configured) Browser verification (y/n, default n): [input]
```

**Resume**: as soon as the ticket id is known, look for the state file (Step 0). If it exists and the user chooses to resume, load project, docs choice, directory and test command from it and do not repeat the other questions.

**The project type defines the flow** (store it in the state):

| Type | Tests (TDD) | UX review |
|---|---|---|
| frontend / design | `unit-test-writer` agent + `commands.test` | if the diff touches `frontend_globs` |
| backend / other | detected runner; tests written by the main thread with the same red -> green cycle | not applicable |

**Repo directory**: if the session cwd is a git repo (`git rev-parse --show-toplevel`), use it and confirm. If not (a folder grouping several repos), list the subfolders containing `.git` and ask which one. Store it: all git, test and build commands run inside it, and it is passed to every agent in its prompt.

**Test command**: `commands.test`; if unset, the `test` script of `package.json` or the project's runner; if not detectable, ask once and store it.

**PR/MR assignee**: `vcs.assignee` if set; do not ask.

## Step 0: Checklist + persistent state

Create a task list with one item per step of the map (1 to 14, including the Plan, the pre-merge gate and the pauses), then one item per phase once the plan exists. If no task tool is available, the checklist lives in the state file as markdown checkboxes with the same rules.

**Evidence rule**: mark an item complete ONLY with verifiable evidence pasted (real command output, a real URL returned by a tool, a real review result). Never by assumption, generic summary ("should be fine", "tests passed") or because "it was done before".

**Persistent state**: file `<repo>/.git/devflow/<TICKET>.md` (inside `.git`, so it is never committed and survives context compaction, session crashes and tool disconnects).
- Exists: show it and ask `resume from step N` or `start over`.
- Does not exist: create the folder and the file with ticket, project type, start time (`date -u +%FT%TZ`), directory, test command, flags from the pre-start.
- Update it at every gate: current step, base branch, new branch, baseline N, PR/MR URL/id, completed phases, review pass number, accepted important/minor findings, docs URL, chosen testers.
- At the end of Step 14 mark it `status: completed` (do not delete).

## Step 1: Preflight

Verify tool access before doing work; discovering a dead tool at Step 12 wastes everything before it. Details and the degradation table: `references/preflight.md`. Critical families must be available (ticket reading, VCS); degradable ones (tracker writes, docs, browser) only degrade a named step. Revalidate at the start of steps 4, 7, 8, 8b, 10, 12, 13 and 14, and after any long pause or compaction.

**Rule for agents**: if an agent reports it could not read the ticket or the diff, that review **does not count as executed**; never treat it as "no findings". Treat it as a preflight failure and re-launch it.

Gate 1:
```
[ ] Critical families verified - output pasted
[ ] Degradable families: state recorded (OK / degraded + affected step)
```

## Step 2: Ticket + base branch

Apply steps 1-2 of the `start-task` skill: fetch the ticket **requesting the parent field explicitly** (a missing field in the response means it was never requested, not that there is no parent), check the parent before choosing the base branch, and find branches with plain `git` (`git fetch origin; git branch -r | grep -i <parent-id>`), never with an integration that may lack branch listing.

Before any `git checkout`, run `git status --porcelain` in the repo. Uncommitted or untracked files: STOP, show them and ask (stash with `-u`, commit separately, or discard by explicit user decision). Never check out or pull on top of unsaved work.

Gate 2 (each with evidence pasted):
```
[ ] Ticket fetched with the parent requested explicitly (no error)
[ ] Parent value actually read from the response (id or null), not assumed
[ ] Base branch determined (output of checkout + pull pasted)
```

## Step 3: Branch name

Propose a name per `branch.pattern` (English, semantic, kebab-case, `branch.max_slug_length`) and confirm. Only propose; the branch is created once, in Step 4, after the Plan.

## PAUSE: Plan (READ-ONLY)

No file changes, no state-changing git, no tests. Explore locally (Read/Glob/grep on the cloned repo, not through the VCS API): key affected files, related specs, technical dependencies, risks (mass changes, dynamic classes, naming). Then write the plan:

```markdown
## Execution plan
### Phase 0 - Pre-flight        (blocking debt, if any)
### Phase 1 - [Name]            Files / Risk / Dependencies
### Phase N - Cleanup / tests
Estimated time: [X minutes]
```

**PAUSE** by ending the turn with the plan. Continue when the user replies `go`, or adjust if they reply `changes: [description]`.

## Step 4: Branch + baseline + draft PR/MR

Revalidate tools. The base branch is already up to date from Step 2.

```bash
git switch -c <branch>                 # the only creation of the branch
<test command> 2>&1 | tail -4          # baseline; save N in the state. Baseline must pass.
git push -u origin <branch>
```

Check for an existing PR/MR for the branch and reuse it. Otherwise create a **draft** with the fixed description template (`start-task/assets/pr-description.md`): only **What** and **Why** can be filled with certainty now (they come from the ticket); the rest stays as a placeholder rewritten in Step 8. Title `[<TICKET>] <summary>`, assignee `vcs.assignee`, delete source branch on merge. On GitLab the draft state is the `Draft: ` title prefix (do not use a `draft` API parameter that may not exist).

**Evidence**: paste the real URL returned. Never report "PR created" without it.

**Fallback**: the branch has no commits over the base yet and the host may refuse the PR/MR for that reason. Do not force anything: record `PR pending, create in Step 10` in the state, continue without it, and create it in Step 10 right after the push with the full description prepared in Step 8.

Gate 4:
```
[ ] New branch created (output pasted)
[ ] Baseline tests run, N saved (output pasted, not summarized)
[ ] Draft PR/MR created or reused - real URL pasted (or the real refusal error + "PR pending" in the state)
```

## Step 5: Execute phases (TDD)

Per phase: test first, it must fail (red), minimal implementation, it passes (green). Paste real red and green output per phase. Nothing is committed or pushed here. Details and who writes the test: `references/tdd-phases.md`.

## Step 6: Final tests

Run the full test command. Classify each failure before touching anything: outdated spec due to an intentional change (update the spec), real regression (fix the code), flaky test (fix the test; never ignore or skip it). Repeat until 0 failures; two consecutive failures with the same cause: propose an alternative to the user. **STOP if it does not reach 0 failures.**

Gate 6: `[ ] Final tests with 0 failures (output pasted, not summarized)`

## Step 7: Local reviews (pre-commit, N passes)

They run BEFORE any commit or push, on the local working tree. Run the three review agents in parallel, in local-diff mode, and loop on findings (max `review.max_auto_passes` automatic passes for criticals; important/minor are listed and the user chooses `fix` or `leave it, continue`). No commit or push happens inside this block. Diff mechanics, the loop and the empty-diff rule: `references/local-review.md`.

Gate 7:
```
[ ] code-review, code-clean, ux-review (if applicable) run in local-diff mode with a NON-empty diff, 0 critical - last-pass output pasted
[ ] Pending important/minor, if any, explicitly accepted by the user (verbatim quote)
```

## Step 8: Full PR/MR description + testing instructions

Rewrite the **whole** description with the final implementation: What / Why / Changes / Verification / Testing instructions. One single source for the PR/MR and the ticket. Writing style (human, not AI boilerplate), the short version for trivial changes, the environment table and the test-case format: `references/pr-description.md`. This step publishes nothing to the tracker (that is Step 12) and publishes no review notes anywhere: review results travel only to `task-summary` via `args` (Step 14).

Gate 8:
```
[ ] Full description updated (real Changes/Verification/Testing instructions, no placeholders) - confirmation pasted
[ ] Testing instructions complete, or the short version for a trivial diff (state which and why)
[ ] Draft saved in the state folder as <TICKET>.testing.md
```

## Step 8b: Browser verification (opt-in)

Only for frontend projects when the user enabled it in the pre-start and `verify.*` is configured. Never blocks the flow. Otherwise skip without comment. Details: `references/browser-verification.md`.

## Steps 9-13: ship

Commits (one pause, via the `commit` skill in batch mode), push + conflict check + CI, optional docs and tester proposal, optional ticket update, pre-merge gate, mark ready. Details and gates: `references/ship.md`.

## Step 14: Team summary

Call `task-summary` and print the final summary. Details: `references/team-summary.md`.

## Constraints (invariants; detail lives in each step)

- Mandatory checklist from Step 0; an item is `completed` only with pasted evidence, never by assumption.
- Every gate (including the pre-merge gate) is blocking and verified explicitly.
- Pauses (`go` / `changes`) are end-of-turn; the user confirms in their next message.
- Failure anywhere: STOP and diagnose. A dead tool: STOP, save state, ask the user to reconnect; an agent review without access to its tools never counts as "no findings".
- Reviews only locally and before the first commit/push; zero commits/pushes inside the fix loop; max `review.max_auto_passes` automatic passes per critical; the local diff is never empty.
- Commits: one round (Step 9), atomic (one concern each), messages only through the `commit` skill. Only exception: one fix commit if CI fails (Step 10), after re-passing Step 7 and with confirmation.
- `git add -N` only for task files, never `git add -N .` / `git add -A`; never `git checkout` over an unsaved working tree.
- TDD mandatory per phase (test first, red then green); in frontend projects the specs always go through `unit-test-writer`, never inline.
- Generated code and tests follow `code_style.comments`: with `none`, no comments at all (inline, block or docstring); existing comments are not required to be removed unless the user asks.
- 0 failures in the final tests (non-negotiable); baseline must pass before starting.
- Testing instructions: one single source (Step 8), published identically on the PR/MR and in the ticket description; never as a ticket comment.
- Human writing style in free prose written to the PR/MR or ticket; mechanical test-case fields stay literal by design.
- Trivial tasks: short testing instructions, never forcing the full structure, and never overwriting the rest of a ticket description (read in its native format, back up, replace or append only the section, re-read and verify).
- No review notes are published on the PR/MR or ticket.
- Testers (when enabled): the ticket tester field gets both people; the PR/MR reviewer gets only the engineering one; the PR/MR assignee is never touched.
- The parent ticket is ALWAYS checked before fixing the base branch (never assume the default branch).
- PR/MR stays a draft until Step 13; assignee, delete-source-branch and the fixed description template as in Step 4.
- Never delete documentation pages automatically; if one is obsolete or duplicated, tell the user.
- Never force push; conflicts with the base are resolved with user confirmation.
- NEVER merge the PR/MR (not even with confirmation); merging is done by someone or something else, outside this flow.
