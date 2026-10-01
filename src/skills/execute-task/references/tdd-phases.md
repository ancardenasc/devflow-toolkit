# Steps 5-6: TDD per phase and final tests

## Who writes the test

| Project type | Test author |
|---|---|
| frontend / design | the `unit-test-writer` agent (agent mechanism, exact name from `subagents.test_writer`). Pass it the file to test and the expected behavior of the phase from the Plan. It writes or adjusts the spec BEFORE any production code, applying stable selectors, AAA and a11y checks for interactive components. Never write the spec inline to skip it. |
| backend / other | the main thread, with the project's runner, before the code |

## Cycle per phase

1. Test author writes/adjusts the test for the phase's behavior.
2. The test must **FAIL (red)**. If it already passes without changes, it does not cover the real case: fix the test, never skip this step.
3. Make the changes from the plan: the minimum implementation that passes.
4. Build if applicable (`commands.build`).
5. Run the partial tests: the same spec as step 1 plus any others that apply (the project's single-file test invocation).
6. Pass (green): next phase.
7. Fail: fix and re-run. Two failures in a row: propose an alternative to the user.

**Evidence required per phase**: paste the real red output (step 2) and the real green output (step 6). Do not summarize as "test created and passes" without both.

Nothing is committed or pushed in this step. Update the state with the completed phase.

## Final tests (Step 6)

```bash
<commands.test full suite> 2>&1 | tail -5
```

```
N passed (baseline: baseline-N)  -> continue
Failures -> classify each before touching anything:
  - spec outdated by an intentional change (selector, text, class, name) -> update the spec
  - real regression in production code -> fix the code
  - fragile or flaky test (order, time or network dependent) -> fix the test; never ignore or skip it
  -> re-run; repeat until 0 failures (two in a row with the same cause: propose an alternative)
```

**STOP if it does not reach 0 failures.**
