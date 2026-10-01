---
name: my-prompt
description: Short description shown in the slash-command picker.
targets: [copilot]
copilot:
  agent: agent
  tools: [read, search, execute]
---

Follow the instructions of the [my-skill skill](../skills/my-skill/SKILL.md).

Ask the user for any missing input before doing anything else, and confirm each step before executing it.
