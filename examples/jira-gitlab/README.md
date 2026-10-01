# Example: Jira + GitLab setup

A worked configuration for a team that tracks work in Jira and hosts code in GitLab, using MCP servers
instead of CLIs. All ids below are placeholders; replace them with your own.

## 1. MCP servers

- Atlassian (Jira + Confluence), e.g. the official remote connector: tool prefix `mcp__claude_ai_Atlassian_Rovo__`.
- GitLab, e.g. `@zereight/mcp-gitlab`: tool prefix `mcp__GitLab-MCP__`.

Check them with `claude mcp list` and reconnect with `/mcp`. Keep tokens in your own MCP configuration; never commit them.

## 2. Project configuration

Copy [`devflow.yml`](devflow.yml) to your project root as `.devflow.yml` and fill in your values.

## 3. Give the agents access to the MCP tools

The generated agents ship with `Read, Grep, Glob, Bash` so they are read-only and work with `gh`/`glab`.
To let them use the MCP servers, extend the `tools:` line of the installed agent file
(`.claude/agents/<name>.md`, or the plugin copy):

| Agent | Add to `tools:` |
|---|---|
| `code-review`, `ux-review` | `mcp__claude_ai_Atlassian_Rovo__getJiraIssue, mcp__GitLab-MCP__list_merge_requests, mcp__GitLab-MCP__get_merge_request, mcp__GitLab-MCP__get_merge_request_diffs, mcp__GitLab-MCP__mr_discussions` |
| `code-clean` | `mcp__GitLab-MCP__list_merge_requests, mcp__GitLab-MCP__get_merge_request_diffs` |
| `task-summary` | the review set above plus `mcp__claude_ai_Atlassian_Rovo__searchConfluenceUsingCql, mcp__claude_ai_Atlassian_Rovo__getConfluenceSpaces, mcp__claude_ai_Atlassian_Rovo__createConfluencePage, mcp__claude_ai_Atlassian_Rovo__updateConfluencePage` |
| `task-reviewers` | `mcp__claude_ai_Atlassian_Rovo__getJiraIssue, mcp__claude_ai_Atlassian_Rovo__searchJiraIssuesUsingJql, mcp__claude_ai_Atlassian_Rovo__lookupJiraAccountId, mcp__claude_ai_Atlassian_Rovo__getTeamworkGraphContext, mcp__claude_ai_Atlassian_Rovo__editJiraIssue, mcp__GitLab-MCP__list_merge_requests, mcp__GitLab-MCP__get_merge_request, mcp__GitLab-MCP__list_project_members, mcp__GitLab-MCP__get_users, mcp__GitLab-MCP__update_merge_request` |

## Notes learned the hard way

- **Ask Jira for the parent field explicitly.** A default `getJiraIssue` call omits `parent`; a missing field means it was never requested, not that the ticket has no parent.
- **Some GitLab MCP servers cannot list branches.** The skills find branches with plain `git` (`git branch -r`).
- **GitLab marks drafts with a `Draft:` title prefix.** Do not rely on a `draft` API parameter.
- **Edit Jira descriptions in ADF**, not markdown: a markdown round trip loses mentions, panels, tables and images. Read, back up, replace only the target section, re-read, verify.
- **Check the tester field format on the first real run.** A multi-user picker is written as `[{"accountId": "..."}]`; confirm it for your instance.
- **Some Atlassian team queries consume paid credits.** Reuse the tester proposal instead of asking twice.
