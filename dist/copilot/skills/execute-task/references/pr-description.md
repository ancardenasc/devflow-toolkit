# Step 8: Full PR/MR description + testing instructions

Revalidate tools (preflight). With the final implementation and the reviews closed, rewrite the **whole** description (not only the testing instructions): What / Why (adjust if it changed) / **Changes** (file/module -> specific change, from the real diff) / **Verification** (concrete steps) / **Testing instructions**.

This step does **not** publish anything to the tracker (that happens in Step 12, with the user's approval) and does **not** publish review notes anywhere: review results only travel to `task-summary` through `args` (Step 14).

## Writing style (What / Why / Changes / Verification / intro of Testing instructions)

Write as the developer would in a real PR, not as an AI-generated report. An AI "slop grenade" is a long, formulaic answer pasted where one sentence would do: the reader loses time hunting for the real fact, and a wall of text invites no reply.

Target tone, as an example:
> Includes the initial work plus the adjustments after the local review (card accessibility, passive wheel listener, sub-pixel tolerance and a layout without double scroll on short viewports). Tests: 234 suites / 5568 tests green. **Could not be verified in a real browser** (the app needs a backend), so cases 1 to 4 and 7 are the ones that confirm the visual DoD.

Direct, natural sentences, limits admitted plainly ("could not verify X because Y"), no padding.

**Avoid** (typical AI patterns):
- Filler: "This change implements...", "It is important to note that...", "In summary...", "As can be seen..."
- Lists where one sentence is enough (a one-item list is not a list)
- Redundancy: repeating in "Why" what "What" already says
- Needless formality and empty hedging ("could potentially...", "to some extent")

**Do**: short sentences, one idea each; name the concrete thing (file, component, behavior) instead of generalizing; admit naturally what could not be done or verified.

**Does not apply** to the mechanical test-case fields (Preconditions / Test data / Steps / Expected result) nor to the environment table: those stay literal and unambiguous by design. The human style is for free prose, not for the structured fields a tester executes to the letter.

## Testing instructions: one source for the PR/MR and the ticket

Generate them **once**, save the draft in the state folder as `<TICKET>.testing.md`, and publish them identically in the PR/MR description (now) and in the ticket description (Step 12).

**Shortcut for trivial tasks**: if the diff is only text/copy, config, or a one-line fix without new logic, use the short version:

```markdown
## **Testing instructions**
- **Branch:** `<branch>`
- [one sentence: what to test and how, e.g. "Only verify the button label changed to 'Save changes' under Settings > Profile"]
```

Never force an environment table, structured cases or a test list for such a change. When unsure whether it is trivial, ask the user at the Step 12 pause instead of deciding alone.

If it is **not** trivial, the full fixed structure:

```markdown
## **Testing instructions**
- **Branch:** `<branch>`

#### **Environment setup**
| Project | Branch | Description |
|---|---|---|
| <service> | <branch> | - |
| <service> | <branch> | [special condition: points to staging, variable X, ...] |

#### **Test cases**
**Case 1: [Title - action + goal]**
**Preconditions**: ...
**Test data**: ...
**Steps**:
1. ...
**Expected result**: ...

#### **Tests to run**
- `<test command> <spec path>`
- When finished, run the full suite: `<full test command>`
```

- The H2 and the three H4 are bold. Branch is the task branch the tester must check out.
- Cases are bold lines (`**Case N: ...**`), not H3, to keep the hierarchy under an H4.

### Environment setup (detected from real state, never invented)

Only when `environment.services` is configured: a list of `{name, path, check}` (path of the repo, an HTTP/command health check). Read-only:

```bash
git -C <path> branch --show-current                                   # current branch
git -C <path> status --porcelain | grep -E '\.env|settings|docker-compose|config/'   # unversioned local config
<check>                                                               # e.g. curl -s -o /dev/null -w '%{http_code}' <url>
```

How to build the table:
- Rows are the services that are **up**. The task's repo always appears, with the task branch.
- **Group in one row** the services that share the same branch.
- **Description**: `-` when there is no special condition. Complete it from the Plan's "technical dependencies" and from "local config modified: <files>" marks (so the user can describe them at the Step 12 pause).
- Other services list the branch the developer had while testing (never assume the default branch).
- VPN is not reliably observable: mention it as a precondition only if the Plan says so.
- If nothing responds (stack down): list only the task's repo and branch with the description `- (environment not verified)`.
- Without `environment.services`: list only the task's repo and branch and leave the description for the user.

### Test cases

Goal: whoever tests the task (QA, another dev, the same user) can reproduce the change without reading code or knowing the feature. **One test case per observable behavior** introduced in the phases (UI, endpoint, flow, validation), not one generic case for the whole PR/MR.

Mandatory structure of each case:

```markdown
**Case N: [Title - action + goal, e.g. "Search a document from the home page"]**
**Preconditions**: [exact prior state, e.g. "Signed in as a standard user", "At least 1 document uploaded"]
**Test data**: [exact values, never generic, e.g. email: user@example.com, password: <test password>, search text: "contract"]
**Steps**:
1. Go to [exact path, e.g. Home > Documents > Search]
2. [Action verb] [exact element]
3. ...
**Expected result**: [what the system shows, verifiable, e.g. "A list with 3 results appears in under 2 seconds"]
```

Wording rules, no exceptions:
- No ambiguous words ("fast", "nice", "works well"); use a metric or verifiable state ("load time under 2 seconds", "a green button with the text 'Saved' appears").
- One action per step, action verb first ("Click", "Enter", "Select", "Go to").
- Always the exact path; never assume the tester knows the menu ("Go to Settings > Profile > Save", not "go to the profile").
- Test data as literal values, not descriptions ("email: user@example.com", not "a valid email"). Never real credentials.
- Same format from case to case within the block.

### Tests to run

Mandatory tests of the ticket (in case the tester does not want to run everything), derived from the diff:

```bash
git diff --name-only $BASE | grep -E '\.(spec|test)\.(js|ts|jsx|tsx|py)$'     # specs created or modified in the ticket
```
- One item per file: `` `<test command> <spec path>` ``.
- **Always the last line**: `When finished, run the full suite: <full test command>` (all tests must pass before the task is considered tested).
- No specs in the diff: only the full-suite line.

## Publishing on the PR/MR

Update the description with the complete text (`gh pr edit <n> --body-file <file>`, `glab mr update <id> --description "<text>"`, or the VCS tool).

**Evidence required**: paste the final "Testing instructions" block and the real confirmation of the update (or re-read the PR/MR and paste the section). If the PR/MR does not exist yet (Step 4 fallback), paste the prepared content and record in the state that it is published in Step 10.
