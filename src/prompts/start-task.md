---
name: start-task
description: Start a new task - fetch the ticket, create the branch, run baseline tests and open a draft PR/MR
targets: [copilot]
copilot:
  agent: agent
  tools: [execute, read, search]
---

Follow the instructions of the [start-task skill](../skills/start-task/SKILL.md) from the first step.

Ask the user for the ticket id (and, if the workspace has several repositories, which root folder to work in) before doing anything else. Read `.devflow.yml` from the project root if it exists. Confirm each step before executing it.
