# Step 8b: Browser verification (opt-in, frontend only)

**Only if** the project is frontend/design **and** the user enabled visual verification in the pre-start **and** `verify` is configured. Otherwise skip this step without comment. **It never blocks the flow.**

## Configuration (`.devflow.yml`)

```yaml
verify:
  enabled: false           # default off; the pre-start question can turn it on per task
  browser: chrome          # chrome | playwright
  start_command: null      # command or slash command that brings the local stack up (offered, never run silently)
  health_checks: []        # list of { name, url, expect } e.g. { name: web, url: http://localhost:3000, expect: 200 }
```

## What it is for

Run the test cases of Step 8 in a real browser to (1) confirm they are reproducible before handing them to the tester, (2) leave visual evidence of the DoD and (3) catch console errors and failed requests. It does not replace the human tester: it does not judge visual quality or do exploratory testing.

## Preconditions (revalidate the chosen browser's tools, preflight)

- Run `verify.health_checks` for the services the case needs. If something does not respond: report it, offer `verify.start_command` and, if the user does not want to wait, **skip the step** and record it in the state.
- The chosen browser is connected.

## Browser choice

| | Chrome automation (default) | Playwright |
|---|---|---|
| Session | the user's real Chrome: already authenticated (SSO, VPN) | separate profile: requires login once |
| Tools | tab context (first), create tab, navigate, read page, find, computer, form input, console messages, network requests, resize, GIF recording | navigate, snapshot, click, type, screenshot, console messages, network requests, resize |
| Extra | record a GIF of the flow (descriptive name, extra frames before and after) | exact viewport, media emulation, does not touch your tabs |

Use the tool names the environment exposes for the chosen browser.

## Execution: per test case, in order

1. Apply the Preconditions and Test data exactly as written (viewport included if the case states one).
2. Follow the Steps literally, skipping none.
3. Compare against the Expected result and capture a screenshot, console errors and failed requests.
4. Classify: pass / fail (what was seen vs expected) / not verifiable (e.g. needs a session or credentials the case does not provide: **never guess credentials**).

## Rules

- Save evidence (screenshots, GIFs) in the session scratch folder, **never in the repo**.
- Do not trigger `alert/confirm/prompt` dialogs; if the flow requires them, warn the user and mark the case not verifiable. If the browser extension does not respond after 2-3 attempts, stop and ask; do not insist.
- Screenshots are not published (no tool to attach them to the ticket). They stay available to the user in the scratch folder.

## Output (paste in the chat)

```
| Case | Result | Evidence |
|------|--------|----------|
| 1 - [title] | pass / fail / not verifiable | [screenshot or GIF path; console errors if any] |
```

**If there is a fail**: show the detail and let the user decide: `fix` (local fix and **back to Step 7** to review again) or `accept` (recorded in the state). No auto-loop.

Gate 8b (only if the step ran):
```
[ ] Case | Result | Evidence table pasted with the executed cases
[ ] Every fail resolved or explicitly accepted by the user (verbatim quote)
```
