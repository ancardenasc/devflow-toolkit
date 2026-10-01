"""Install into throwaway projects and verify the result, for both tools."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

from common import ROOT, load_catalog, split_frontmatter

LINK = re.compile(r"\]\((\.{1,2}/[^)#]+)")
errors = []


def check_tree(root, expected):
    for rel in expected:
        if not (root / rel).exists():
            errors.append(f"missing after install: {rel}")
    for f in root.rglob("*.md"):
        text = f.read_text()
        if text.startswith("---\n") and "template" not in f.relative_to(root).parts:
            try:
                meta, _ = split_frontmatter(text)
            except (ValueError, yaml.YAMLError) as e:
                errors.append(f"{f.relative_to(root)}: bad frontmatter ({e})")
                continue
            if not meta.get("description"):
                errors.append(f"{f.relative_to(root)}: no description")
        for m in LINK.finditer(text):
            if not (f.parent / m.group(1)).resolve().exists():
                errors.append(f"{f.relative_to(root)}: broken link {m.group(1)}")


def main():
    assets = load_catalog()["assets"]
    for tool in ("claude", "copilot"):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([str(ROOT / "scripts" / "install.sh"), tool, d], check=True, capture_output=True)
            base = Path(d) / (".claude" if tool == "claude" else ".github")
            expected = []
            for a in assets:
                i, kind = a["id"], a["type"]
                if kind == "skill":
                    expected.append(f"skills/{i}/SKILL.md")
                elif kind == "agent":
                    expected.append(f"agents/{i}.md" if tool == "claude" else f"agents/{i}.agent.md")
                elif kind == "prompt" and tool == "copilot":
                    expected.append(f"prompts/{i}.prompt.md")
            check_tree(base, expected)
            print(f"{tool}: {len(expected)} expected files checked")
    for e in errors:
        print("ERROR", e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
