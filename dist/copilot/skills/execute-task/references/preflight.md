# Step 1: Preflight of tools

Tools can die, lose authentication or be disabled for the project (in Claude Code check `claude mcp list`). This skill cannot reconnect them: it only detects, stops and asks the user to reconnect (Claude Code: `/mcp`). Detecting it here avoids discovering it at Step 12 after all the work is done.

## Families

Resolve each family to whatever the environment provides: an MCP server, a CLI (`gh`, `glab`, `jira`, `acli`), or manual input by the user.

| Family | Used in steps | Check | Critical |
|---|---|---|---|
| Ticket reading (tracker) | 2, review agents, 14 | can fetch the ticket by id (MCP tool, `gh issue view`, CLI) | Yes (unless `tracker.type: none`) |
| VCS host (PR/MR) | 4, 8, 10, 12, 13 | `gh auth status` / `glab auth status`, or the VCS MCP tools: create, update, get, list PRs/MRs, list pipelines/checks | Yes |
| Tracker writes + teams | 12 | edit issue, search, user lookup | No - degradable: Step 12 becomes manual assignment by the user |
| Docs target | 11, 14 | tool for `docs.target` (confluence/notion) | No - degradable: docs go to `<docs.path>/<TICKET>.md`, Step 14 only in chat |
| Browser (only if the pre-start enabled verification) | 8b | the browser tools named in `verify.browser`; verify only the chosen one | No - degradable: Step 8b is skipped and recorded in the state |

In Claude Code, verify MCP tools with the tool-search mechanism (a "no matching tools" result, or only authenticate tools, means disconnected or unauthenticated). A listed tool does not guarantee valid auth, so run at least one cheap live read per critical family: fetch the ticket (Step 2 does it anyway) and a read on the VCS host (`gh api user`, `glab auth status`, or a user lookup).

## Outcome

```
Critical down   -> STOP: "Missing <family>. Reconnect it and tell me 'ready'." Retry the preflight on "ready".
Degradable down -> say which step is degraded, record it in the state, continue.
All OK          -> continue.
```

## Revalidation

Repeat the check (listing only, no live smoke test) at the start of steps 4, 7, 8, 8b, 10, 12, 13 and 14, and whenever a step resumes after a long pause or a context compaction. If a tool dies mid-flow: STOP, save the state, ask to reconnect, resume exactly at that step.
