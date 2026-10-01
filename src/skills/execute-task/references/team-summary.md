# Step 14: Team summary and final summary

Revalidate tools.

Call the `task-summary` agent (exact name), passing the ticket id, the PR/MR URL, the repo directory and base branch (for its `git log`), the **reviews summary** and, if it exists, the technical doc URL from Step 11:

```
args: "dir=<directory>; base=<base branch>; reviews=<short summary>; doc=<url>"
```

`reviews` is built by the main thread (which witnessed the reviews) in this format:

```
passes=N; CodeReview=0crit/Xmaj/Ymin; CodeClean=0crit/Xmaj/Ymin; UX=0crit/Xmaj/Ymin|n/a; accepted=<list or none>
```

Nothing is published on the PR/MR or the ticket. The agent is stateless: it rebuilds the rest from the tracker/git/PR on its own; there is no need to pass it the reasoning of the conversation.

It returns material to explain the task out loud (what was done, why, how it works with its theory, one-line pitch, anticipated questions), not deep technical documentation (Step 11 covers that when it applied). It also publishes a backup to the configured docs target.

**Evidence required**: paste the real URL or path of the page returned by the agent (or, if the docs target is degraded, the full summary in the chat).

## Final Summary

```
TASK COMPLETED
Ticket      <ID> - [Title]
Base branch [real base branch]
New branch  <branch>
Tests       N passed / 0 failed (baseline: baseline-N)
Commits     M commits (atomic)
Reviews     N local passes, 0 critical
Visual      N/M cases OK | n/a
Pipeline    [green / none]
PR/MR       [URL] (ready, not merged)
Testers     [design] / [engineering] | n/a
Doc         [URL | n/a]
Summary     [URL or path]
Time        ~ X minutes
```

`Time` = now minus the start time saved in the state (Step 0), computed with `date`, never estimated.

Gate 14, closing the task:
```
[ ] Team summary published (task-summary agent) - real URL/path pasted
[ ] Final Summary printed with real data (URLs and computed time)
[ ] Persistent state marked as completed
```
