"""Lint sources and generated output. Exit 1 on any problem."""
import re
import sys

import yaml

from common import ROOT, load_catalog, split_frontmatter

NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Company/personal terms that must never reach a public repo.
FORBIDDEN = re.compile(r"tirant|BDD-|c06e3789|\bncardenas\b|customfield_\d+|/Users/", re.I)
SKIP_FORBIDDEN = {"scripts/lint.py", "catalog.yml"}  # catalog authored by owner; lint lists the terms
errors = []


def err(msg):
    errors.append(msg)


def main():
    cat = load_catalog()
    ids = set()
    for a in cat.get("assets") or []:
        i, kind = a["id"], a["type"]
        ids.add((kind, i))
        if not NAME.match(i) or len(i) > 64:
            err(f"{i}: name must be kebab-case, <=64 chars")
        if a["bundle"] not in cat["bundles"]:
            err(f"{i}: unknown bundle {a['bundle']}")
        for k in ("description", "description_es"):
            if not a.get(k):
                err(f"{i}: catalog missing {k}")
        path = {
            "skill": ROOT / "src/skills" / i / "SKILL.md",
            "agent": ROOT / "src/agents" / f"{i}.md",
            "prompt": ROOT / "src/prompts" / f"{i}.md",
            "hook": ROOT / "src/hooks" / i / "hooks.json",
        }[kind]
        if not path.exists():
            err(f"{i}: missing {path.relative_to(ROOT)}")
            continue
        if kind == "hook":
            continue
        text = path.read_text()
        try:
            meta, _ = split_frontmatter(text)
        except (ValueError, yaml.YAMLError) as e:
            err(f"{path.relative_to(ROOT)}: invalid frontmatter ({str(e).splitlines()[0]})")
            continue
        if kind != "prompt" and meta.get("name") != i:
            err(f"{path.relative_to(ROOT)}: frontmatter name != {i}")
        if not meta.get("description") or len(str(meta["description"])) > 1024:
            err(f"{path.relative_to(ROOT)}: description missing or >1024 chars")
        if kind == "skill" and text.count("\n") > 500:
            err(f"{path.relative_to(ROOT)}: SKILL.md over 500 lines; move detail to references/")
    # forbidden terms in everything publishable
    for f in ROOT.rglob("*"):
        rel = f.relative_to(ROOT).as_posix()
        if (not f.is_file() or rel.startswith((".git/", ".venv/")) or rel in SKIP_FORBIDDEN
                or f.suffix in {".png", ".jpg", ".gif"}):
            continue
        try:
            for n, line in enumerate(f.read_text().splitlines(), 1):
                if FORBIDDEN.search(line):
                    err(f"{rel}:{n}: forbidden term: {line.strip()[:80]}")
        except UnicodeDecodeError:
            pass
    # relative markdown links inside generated Copilot output must resolve
    link = re.compile(r"\]\((\.{1,2}/[^)#]+)")
    for f in (ROOT / "dist" / "copilot").rglob("*.md"):
        for m in link.finditer(f.read_text()):
            if not (f.parent / m.group(1)).resolve().exists():
                err(f"{f.relative_to(ROOT).as_posix()}: broken relative link {m.group(1)}")
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} problem(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
