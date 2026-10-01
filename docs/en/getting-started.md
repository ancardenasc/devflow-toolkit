# Getting started

Five minutes from zero to your first assisted task.

## 1. Install

**Claude Code** (plugin marketplace, recommended)
```
/plugin marketplace add ancardenasc/devflow-toolkit
/plugin install devflow-core@devflow-toolkit
/plugin install devflow-review@devflow-toolkit
```

**GitHub Copilot, or Claude Code without plugins**
```
git clone https://github.com/ancardenasc/devflow-toolkit
cd devflow-toolkit
scripts/install.sh copilot /path/to/your/project     # writes .github/{agents,prompts,skills}
scripts/install.sh claude  /path/to/your/project     # writes .claude/{agents,skills}
```

More options and caveats: [cross-tool](cross-tool.md).

## 2. Configure your project

Copy the example file to the root of the project you work on and edit the few values that differ from the defaults:

```
cp .devflow.example.yml /path/to/your/project/.devflow.yml
```

Every key is optional. With no file, the assets infer the VCS from `git remote get-url origin`, assume `main`, and ask when unsure. Full reference: [configuration](configuration.md).

Minimal GitHub setup:
```yaml
tracker: { type: github }
vcs: { type: github, default_branch: main }
commands: { test: "npm test" }
```

## 3. Use it

| You want to | Run | Bundle |
|---|---|---|
| Start a task: branch, baseline tests, draft PR | `/start-task` | devflow-core |
| Run a whole task end to end (plan, TDD, reviews, PR) | `/execute-task` | devflow-core |
| Create a commit with the right message | `/commit` | devflow-core |
| Review a finished ticket/PR | `/review-ticket` | devflow-review |

In Claude Code the plugin namespaces them (`/devflow-core:start-task`); copied files give the short names. In Copilot Chat the prompts `/start-task` and `/ticket-review` call the same skills.

The review and helper agents (`code-review`, `code-clean`, `ux-review`, `unit-test-writer`, `task-summary`, `task-reviewers`) are called by the skills, and you can invoke them directly as well.

## 4. What to expect

- Every skill **confirms before acting** and **pastes real evidence** (command output, URLs) instead of claiming success.
- Reviewers are **read-only**; nothing is merged for you, ever.
- Anything specific to your company (ticket prefix, commit format, tester roster, docs space) belongs in `.devflow.yml`, never inside the assets.

Next: [how the workflow fits together](workflow.md).
