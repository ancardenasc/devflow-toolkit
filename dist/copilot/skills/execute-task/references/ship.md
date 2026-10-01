# Steps 9-13: commits, push, docs, testers, pre-merge gate, mark ready

## Step 9: Commits (PAUSE, once)

Group by semantic concern (tooling / structure / DOM / migration / test fixes / component-X ...). Each commit is independently reversible. The message convention (format, language, ticket detection) is defined by the `commit` skill, the single source of truth; do not redefine it here.

For each group build the proposal (without executing):

```
Commit #1 - [concern]
  files: <list>
  message: <per commit skill>
Commit #2 - [concern]
  ...
```

**PAUSE** by ending the turn showing the proposed commits (message + files per group). Continue when the user replies `go`, or adjust if they reply `changes: [desc]`.

After `go`, for each group in order call the `commit` skill in batch mode:
```
Skill(commit, args: "mode=batch; files=<group file list>; desc=<short description>")
```
Then verify with `git log --oneline -N`.

## Step 10: Push + sync with base + CI

Revalidate tools.

```bash
git fetch origin
git push origin <branch>
```

Verify, with real evidence for each:
- **Pending PR/MR** (Step 4 fallback): if the state says "PR pending, create in Step 10", create it now (same title with draft marking, assignee, the full Step 8 description with the testing instructions).
- **Push**: if it fails, STOP and show the error.
- **PR/MR reflects the commits**: last commit on the PR/MR = local HEAD (`gh pr view --json commits`, `glab mr view`, or the VCS tool).
- **No conflicts with the base**: mergeability fields (`gh pr view --json mergeable,mergeStateStatus`; GitLab `has_conflicts` / `detailed_merge_status`). With conflicts: STOP, propose merging or rebasing the base and ask for confirmation (never force push).
- **CI pipeline**: `gh pr checks`, `glab ci status` or the VCS tool.
  - Green: OK.
  - Running: report the state and continue with steps that do not depend on it (Step 11); re-check before the GATE.
  - Failed: STOP; read the failed job's log, diagnose, fix locally. The fix goes back through Step 7 (local reviews on the full diff), then **one single fix commit** with user confirmation + push (the only exception to "one single round of commits").
  - No pipeline: note it; it does not block.

Gate 10 (each with evidence pasted):
```
[ ] Push succeeded (output pasted)
[ ] PR/MR verified to reflect the last commit (URL + real confirmation, not assumed)
[ ] PR/MR without conflicts with the base
[ ] Pipeline: green / running (re-check before the GATE) / none
```

## Step 11: Documentation (only if the pre-start said yes) + tester proposal (only if enabled)

Two independent things that can advance together. **A** only applies if the pre-start said yes; **B** only if `workflow.assign_testers` is true.

**A. Technical documentation** (for future maintainers; different from Step 14, which is material to explain out loud). Target from `docs.target`:
- `markdown`: `<docs.path>/<TICKET>.md`.
- `confluence` / `notion`: a page titled `[<TICKET>] Description` under the parent given by `docs.path`. Search first for an existing page with that title: if it exists, update it with a version comment describing the change; otherwise create it. If the tool rejects the parent, create at the space root, tell the user to move it, and note the finding.
- Content: motivation + design decisions, affected files, phase summary, team conventions, commit history (`git log`).
- No tool to delete pages: if one is obsolete or duplicated, give the user the link so they remove it manually (never automatic).
- Fallback if the target is unavailable: `docs/<TICKET>.md`, and tell the user why.

Save the URL/path in the state; pass it to `task-summary` (Step 14) so it links it.

**B. Tester proposal** (call 1 of the `task-reviewers` agent, read-only), launched in parallel with A. See Step 12.

## Step 12: Assign testers + testing instructions on the ticket

Revalidate tools. If the tracker-write family is degraded, or `workflow.assign_testers` is false: manual assignment by the user. Show what to complete (the tester field `tracker.fields.tester`, the PR/MR reviewer, and the "Testing instructions" block pasted as text in the ticket description) and continue when they confirm.

When enabled, call the `task-reviewers` agent (call 1, no `args`) with the ticket id: it proposes testers weighted by real sprint load, never plain random, and writes nothing yet. If it was already launched in Step 11-B, **reuse that result** (the team query may consume paid API credits).

### Prepare the ticket description write (read-only, nothing is written yet)

1. Read the current description **in the tracker's native rich format** (Jira: ADF, not markdown; ADF -> markdown -> ADF loses mentions, panels, tables and embedded images).
2. Back up the original as-is in the state folder (`<TICKET>.description.backup.json`) so it can be restored.
3. Decide what to do with the description:
   - Our H2 **Testing instructions** already exists: **replace** only that section (from that H2 to the next H2 or the end). The rest stays intact.
   - A **manual variant** exists (e.g. "TESTING" as a paragraph or list from an earlier task): show it at the pause and ask `replace` or `append`; never decide alone.
   - None exists: **append at the end**. Never overwrite the rest of the description.
4. Build the final document: the Step 8 block converted to the native format (bold H2/H4; list for Branch; table for the environment; bold cases with numbered lists; list for tests to run) + the rest of the original description unchanged.

### Pause

**PAUSE** by ending the turn showing, in this order:
1. The tester proposal (load table + chosen), if enabled.
2. The complete **"Testing instructions"** block to be written on the ticket and in which mode (replace / append / manual variant -> question), with the environment table highlighted: it is the part the user must review and complete (special conditions, branches of other projects, variables).

Continue when the user replies `go`, or adjust if they reply `changes: [desc]` (changes are applied to the saved block and published again on the PR/MR description too).

### After `go`

1. If enabled, call `task-reviewers` again (call 2, `args: "confirmed=true; design=<name>; engineering=<name>"` with the exact names proposed): it writes the ticket tester field (both people) and the PR/MR reviewers (**only** the engineering person). **The PR/MR assignee is not touched.**
2. Write the ticket description with the final document.
3. Re-read the description and **verify**: the "Testing instructions" section is there and all previous nodes (mentions, images, tables, panels) are intact except the replaced section. If anything was lost, restore from the backup and tell the user.
4. If the PR/MR already had the instructions (Step 8) and there were `changes`, re-read the PR/MR and confirm it matches the ticket.

**Do not comment on the ticket** (neither the PR/MR URL nor test cases): all testing content lives in the description.

**Evidence required**: paste the real confirmation of each write (tester field, PR/MR reviewer, ticket description) and the result of the step 3 verification.

Gate 12 (when applicable):
```
[ ] Testers (if enabled) and the "Testing instructions" block approved by the user (`go`)
[ ] Ticket tester field with both people - real confirmation pasted (or the user's textual confirmation if manual)
[ ] PR/MR reviewer = engineering person only, assignee intact - confirmation pasted (or the user's if manual)
[ ] Ticket description with "Testing instructions" - re-read, other nodes intact (or pasted as text for the user to publish if degraded)
[ ] Backup of the original description saved in the state folder
```

## GATE: pre-merge verification (blocking, do not skip)

You cannot advance to Step 13 without explicitly ticking this checklist (everything already happened in earlier steps; here it is only verified):

```
[ ] code-review ran locally (Step 7) -> 0 critical, output pasted
[ ] code-clean ran locally (Step 7) -> 0 critical, output pasted
[ ] ux-review ran locally (Step 7) if applicable -> 0 critical, output pasted
[ ] Final tests with 0 failures (Step 6)
[ ] Full description + real Testing instructions on the PR/MR (Step 8)
[ ] Browser verification (Step 8b): executed with all fails resolved/accepted, or skipped (opt-in off or environment unavailable)
[ ] Push done, PR/MR reflects the last commit, no conflicts (Step 10)
[ ] Pipeline green (re-check now if it was "running") or none
[ ] Testers assigned + Testing instructions on the ticket (Step 12), or manual completion confirmed
```

If any item is unticked: **STOP**, run the missing step now, do not continue. "I'll check later" or assuming it was done is not accepted: verify each item explicitly before Step 13.

## Step 13: Mark ready + final summary

**Never merge. Merging is done by someone or something else, outside this flow.**

Revalidate tools. Mark the PR/MR ready:
- GitHub: `gh pr ready <n>`.
- GitLab: read the real title with `get_merge_request`/`glab mr view`, then remove only the draft prefix (`Draft:`, `[Draft]`, `(Draft)`, `WIP:`) without altering the rest; or `glab mr update <id> --ready`.
- Do NOT execute a merge under any circumstance.

**Evidence required**: paste the resulting title/state and verify the PR/MR no longer shows as a draft (`isDraft: false` / `draft: false` / title without prefix).

The Final Summary is printed at the end of Step 14 (it needs the team-summary URL and the total time).
