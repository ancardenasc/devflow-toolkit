"""Fill catalog tables between <!-- catalog:start --> / <!-- catalog:end --> markers."""
import re

from common import ROOT, load_catalog

TITLES = {"en": {"skill": "Skills", "agent": "Agents", "prompt": "Prompts / commands"},
          "es": {"skill": "Skills", "agent": "Agentes", "prompt": "Prompts / comandos"}}
HEAD = {"en": "| Name | Bundle | Description |", "es": "| Nombre | Bundle | Descripcion |"}


def table(cat, lang):
    key = "description" if lang == "en" else "description_es"
    out = []
    for kind, title in TITLES[lang].items():
        rows = [a for a in cat.get("assets") or [] if a["type"] == kind]
        if not rows:
            continue
        out += [f"### {title}", "", HEAD[lang], "|---|---|---|"]
        out += [f"| `{a['id']}` | {a['bundle']} | {a[key]} |" for a in rows]
        out.append("")
    return "\n".join(out).strip() or "_Coming soon._"


def main():
    cat = load_catalog()
    for fname, lang in (("README.md", "en"), ("README.es.md", "es")):
        p = ROOT / fname
        if not p.exists():
            continue
        new = re.sub(r"(<!-- catalog:start -->).*?(<!-- catalog:end -->)",
                     lambda m: f"{m.group(1)}\n{table(cat, lang)}\n{m.group(2)}",
                     p.read_text(), flags=re.S)
        p.write_text(new)


if __name__ == "__main__":
    main()
