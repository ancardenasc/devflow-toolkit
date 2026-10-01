"""Shared helpers: frontmatter parsing and catalog loading."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FM = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)


def split_frontmatter(text):
    m = FM.match(text)
    if not m:
        raise ValueError("missing frontmatter")
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)


def dump_frontmatter(meta, body):
    head = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=10_000).strip()
    return f"---\n{head}\n---\n{body.lstrip(chr(10))}"


def load_catalog():
    return yaml.safe_load((ROOT / "catalog.yml").read_text())
