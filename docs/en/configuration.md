# Configuration: `.devflow.yml`

One file at the root of **your project** (not this repo). Every key is optional; defaults are shown. Start from [`.devflow.example.yml`](../../.devflow.example.yml). A worked Jira + GitLab file is in [`examples/jira-gitlab/`](../../examples/jira-gitlab/).

## Reference

| Key | Default | Meaning | Used by |
|---|---|---|---|
| `tracker.type` | `github` | `github`, `jira`, `linear` or `none` | start-task, execute-task, review-ticket, reviewers |
| `tracker.ticket_pattern` | `[A-Z]+-\d+` | Regex that finds the ticket id in branch names | commit, start-task, execute-task |
| `tracker.site` | none | Tracker host, e.g. `your-team.atlassian.net` (Jira) | task-reviewers |
| `tracker.fields.tester` | none | Ticket field holding the testers, e.g. a Jira custom field | task-reviewers, execute-task |
| `tracker.fields.sprint` | none | Ticket field holding the sprint name | task-reviewers |
| `vcs.type` | inferred | `github` or `gitlab` | start-task, execute-task, reviewers |
| `vcs.default_branch` | `main` | Fallback base branch | start-task, execute-task, reviewers |
| `vcs.assignee` | none | Default PR/MR assignee | start-task, execute-task |
| `workflow.base_from_parent` | `true` | Branch from the parent ticket's branch when it exists | start-task, execute-task |
| `workflow.assign_testers` | `false` | Enable the tester proposal and assignment step | execute-task |
| `branch.pattern` | `{ticket}-{slug}` | Branch name template | start-task, execute-task |
| `branch.max_slug_length` | `50` | Max length of the `{slug}` part | start-task, execute-task |
| `commit.format` | `conventional` | `conventional` or a template such as `"[{ticket}] {summary}"` | commit |
| `commit.language` | `en` | Language of commit messages | commit |
| `commit.attribution` | `false` | Add `Co-Authored-By` style trailers | commit |
| `commands.test` | detected | Test command | start-task, execute-task, unit-test-writer |
| `commands.lint` | detected | Lint command | code-clean |
| `commands.build` | none | Build command | execute-task |
| `review.max_auto_passes` | `3` | Automatic fix-and-re-review passes for critical findings | execute-task |
| `code_style.comments` | `minimal` | `none` forbids comments in generated code and tests | execute-task |
| `frontend_globs` | `**/*.{vue,jsx,tsx,css,scss,html}` | Files that make the UX review apply | ux-review, execute-task, review-ticket |
| `verify.enabled` | `false` | Browser verification (opt-in) | execute-task |
| `verify.browser` | `chrome` | `chrome` or `playwright` | execute-task |
| `verify.start_command` | none | Command that brings the local stack up (offered, never silent) | execute-task |
| `verify.health_checks` | `[]` | `[{name, url, expect}]` checks before browsing | execute-task |
| `environment.services` | `[]` | `[{name, path, check}]` used to fill the testing-environment table | execute-task |
| `docs.target` | `markdown` | `markdown`, `confluence` or `notion` | execute-task, task-summary |
| `docs.path` | `docs/` | Folder, or parent page/folder id for confluence/notion | execute-task, task-summary |
| `a11y.standards` | `["WCAG 2.2 AA"]` | Add extra standards via a file in `profiles/` | ux-review |
| `output_language` | `en` | Language of reports, PR descriptions and summaries | all |
| `subagents.*` | default names | Rename `code_review`, `code_clean`, `ux_review`, `test_writer` | review-ticket, execute-task |
| `reviewers` | none | Roster and subgroups for tester assignment | task-reviewers |

## Reviewers

```yaml
reviewers:
  load_margin: 1               # candidates within min load + margin enter the draw
  design:
    members:
      - { name: Ana Gomez, tracker_id: "<account id>", vcs_user: anagomez }
  engineering:
    groups:                    # subgroup picked by a keyword found in the sprint name
      - match: Alpha
        members: [{ name: Luis Perez, vcs_user: luisperez }]
```
`tracker_id` and `vcs_user` are optional; when missing they are resolved live and reported so you can add them.

## Profiles

Country or company standards live in `profiles/`. Example: `profiles/colombia.md` adds an NTC 5854 column to the UX review when `a11y.standards` includes `"NTC 5854"`.

## Where the file is read

Assets read `.devflow.yml` from the project root of the repo you are working in. Nothing is ever read from your home directory, and secrets never belong in this file; keep tokens in your MCP or CLI configuration.
