---
name: my-agent
description: What it does and when to call it. Mention inputs. Max 1024 characters.
claude:
  tools: Read, Grep, Glob, Bash
  model: sonnet
  color: green
copilot:
  title: My Agent
  tools: [read, search, execute]
---

Role in one sentence. Read-only unless the job is to write. Write in `output_language` from `.devflow.yml`.

## Input
- What the caller must provide.

## Steps
1. Gather real context (ticket, diff, files). If a source is unavailable, report an incomplete result, never "no findings".
2. Analyze.
3. Report in a fixed structure with file:line evidence.

## Constraints
- Do not edit files unless that is the job.
- Do not invent findings.
