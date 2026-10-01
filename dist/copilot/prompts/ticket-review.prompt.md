---
description: Full review of a ticket - DoD check, code review, clean-code review and UX review of the PR/MR, with an executive summary
agent: agent
tools:
- read
- search
- execute
---
Follow the instructions of the [review-ticket skill](../skills/review-ticket/SKILL.md).

Ask the user which workspace root folder to work in (list the folders as numbered options) and which PR/MR or branch to review. If the folder is not part of the workspace, say so and wait for a valid choice.

Run the review agents [code-review](../agents/code-review.agent.md), [code-clean](../agents/code-clean.agent.md) and [ux-review](../agents/ux-review.agent.md) (UX only when the diff touches frontend files). If a step cannot be completed (no access to the PR/MR, an agent or the files), stop, explain the blocker and wait for instructions.

Finish with an executive summary, each section ordered by descending severity:
1. **Top 3 critical findings** across code review and clean code
2. **Top 3 critical UX findings** (omit if the UX review did not apply)
3. **Final recommendation**: ready to merge, or changes required
