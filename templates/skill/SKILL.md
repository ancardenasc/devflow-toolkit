---
name: my-skill
description: One or two sentences: what it does and when to use it. Include trigger words a user would say. Max 1024 characters. Quote the value if it contains ": ".
argument-hint: "[optional-arg]"
license: MIT
---

# /my-skill

One-paragraph purpose. Answer in `output_language` from `.devflow.yml` (default: the user's language).

## Configuration (`.devflow.yml`, all optional)
List only the keys this skill reads and their defaults.

## Steps
1. Step with a clear stop condition.
2. Step that asks for confirmation before changing anything.
3. Step that pastes real evidence (command output, URL).

Move long detail to `references/<topic>.md` and reusable text to `assets/`.

## Constraints
- Never invent data that cannot be verified at the source.
- Fail loudly when an input is missing.
