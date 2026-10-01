---
name: review-ticket
description: Review an already implemented ticket - verify its Definition of Done against the tracker, run the code-review, code-clean and ux-review agents on the PR/MR, consolidate one report, and optionally publish it as inline PR/MR comments and a ticket comment. Read-only plus comments, it never edits code, commits or merges. Use to review or audit a finished ticket/PR, not to execute a new task.
argument-hint: "[ticket-id] [pr-or-mr]"
license: MIT
---

# /review-ticket

Senior reviewer: verifies the DoD and runs three review agents on a ticket/PR that is already implemented. No implementation, no commits, no merge. Answer in `output_language` (default: the user's language).

It orchestrates three existing agents through the agent/subagent mechanism of the tool (never as free text), always from the main thread and never nested: `code-review`, `code-clean`, `ux-review`. Names come from `subagents.*` in `.devflow.yml`. This skill does not reimplement their logic; it verifies the DoD, calls them and consolidates.

## Configuration (`.devflow.yml`, optional)
`tracker.type`, `vcs.type`, `vcs.default_branch`, `frontend_globs` (decides if UX review applies), `subagents.*`.

## Input

```
? Ticket id: [input]
? PR/MR (optional, auto-detected from the ticket id or branch if omitted): [input]
? Publish findings at the end (PR/MR + ticket) (y/n): [input]
```

## Step 0: Checklist

Create a task list with one item per step (1 to 5), using the task tool the environment provides.

**Evidence rule**: mark an item complete ONLY with verifiable evidence pasted (real tool output, never an assumption or a generic summary).

## Step 1: Ticket and PR/MR

Fetch title, description, status, assignee, parent and acceptance criteria / DoD (tracker MCP, `gh issue view`, CLI, or pasted text). On error: STOP.

Find the PR/MR: `gh pr list --search "<id>"` / `glab mr list --search "<id>"` (or VCS tools). One match: use it. Several: list and ask. None: ask for the PR/MR or branch.

Take the DoD exactly as written in the ticket. If the ticket has no explicit DoD, say so; never invent criteria.

Gate 1:
```
[ ] Ticket fetched (including parent) - output pasted
[ ] PR/MR identified - real URL pasted
```

## Step 2: Diff and DoD verification

Get the changed files (+/- lines) and existing discussions (`gh pr diff <n>`, `glab mr diff <id>`).

| Criterion (exact ticket text) | Status | Evidence (file:line) |
|---|---|---|
| ... | OK / partial / missing | ... |

Never mark OK without pointing to the file and line that satisfies it.

Gate 2:
```
[ ] Diff fetched - output pasted
[ ] DoD table complete, one row per real ticket criterion
```

## Step 3: Reviews (existing agents, scope unchanged)

Run in parallel (same message, no dependency between them):

1. **code-review**: security (OWASP Top 10), performance, SOLID, error handling, tests.
2. **code-clean**: Clean Code craftsmanship: naming, functions, duplication, dead code, F.I.R.S.T tests.
3. **ux-review**: only if `git diff --name-only <base>...<mr-branch>` touches files matching `frontend_globs` (verify, do not assume). WCAG 2.2 AA, Nielsen, plus any configured `a11y.standards`.

**Evidence required for each**: paste the agent's real output as returned. Do not summarize as "no critical findings" without pasting the full detail.

Gate 3:
```
[ ] code-review executed - output pasted
[ ] code-clean executed - output pasted
[ ] ux-review executed, or explicitly "not applicable" (no frontend files in the diff)
```

## Step 4: Consolidated report

```markdown
# Review: [TICKET] - [Title]

## Summary
| PR/MR | [title](url) |
| Changes | N files (+M/-Z lines) |
| Verdict | OK / Minor changes / Changes required |

## DoD
[table from Step 2]

## Consolidated findings
(merge the three agents; if two flag the same thing, dedupe and cite both; tag each finding with its origin [code-review]/[code-clean]/[ux-review])

### Critical
#### [C-1] Title - [origin]
- File: path:line
- Problem: ...
- Proposed fix: ...
### Important   (same format)
### Minor       (same format)

## Verdict
2 sentences: real state + recommended action.
```

**Critical gate**: if there is any critical finding, show the full report and **end the turn**, asking for confirmation before Step 5. With no critical findings, continue directly if the user already asked to publish.

## Step 5: Publish (if requested, or after confirmation at the critical gate)

**PR/MR**: for each finding with an identifiable file and line, create an inline review comment (`gh api` review comments / `gh pr review`, `glab mr note`, or the VCS tool) with `[severity] problem + proposed fix`.

**Ticket**: one comment with the full Step 4 report, through the tracker tool.

**Evidence required**: paste the real confirmation of each publication (comment ids/URLs). Do not assume it was posted.

Gate 5:
```
[ ] Inline PR/MR comments posted (or "no findings with an exact line")
[ ] Ticket comment posted - real id/URL pasted
```

## Constraints

- Never edit code, commit or merge; this skill is read-only plus comments.
- Never invent DoD criteria.
- Never summarize an agent's findings before pasting its real output.
- Dedupe findings across agents (code-review does not repeat naming/dead-code from code-clean, by design).
- Never publish after a critical finding without confirmation.
- UX review is conditional on file patterns, verified with `git diff --name-only`.
