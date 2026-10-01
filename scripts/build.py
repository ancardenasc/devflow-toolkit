"""Generate tool-specific outputs from the neutral sources in src/.

src/skills/<id>/SKILL.md          -> plugins/<bundle>/skills/<id>/ and dist/copilot/skills/<id>/
src/agents/<id>.md  (neutral)     -> plugins/<bundle>/agents/<id>.md  and dist/copilot/agents/<id>.agent.md
src/hooks/<id>/{hooks.json,*.sh}  -> plugins/<bundle>/hooks/ (Claude only; hooks.json merged per bundle)
src/prompts/<id>.md (neutral)     -> plugins/<bundle>/commands/<id>.md and dist/copilot/prompts/<id>.prompt.md
catalog.yml                       -> .claude-plugin/marketplace.json and plugins/<bundle>/.claude-plugin/plugin.json

Neutral agent frontmatter:  name, description, bundle?, claude: {tools, model, color}, copilot: {title, tools, model}
Neutral prompt frontmatter: name, description, targets? (default both; skills already give Claude a slash command), copilot: {agent, tools}, claude: {allowed-tools, argument-hint}
"""
import json
import shutil

from common import ROOT, dump_frontmatter, load_catalog, split_frontmatter


def reset(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def main():
    cat = load_catalog()
    by_id = {(a["type"], a["id"]): a for a in cat.get("assets") or []}
    for d in (ROOT / "plugins", ROOT / "dist" / "copilot"):
        reset(d)

    hooks_by_bundle = {}

    for a in by_id.values():
        i, kind, b = a["id"], a["type"], a["bundle"]
        plug = ROOT / "plugins" / b
        cop = ROOT / "dist" / "copilot"
        if kind == "skill":
            src = ROOT / "src" / "skills" / i
            for dest in (plug / "skills" / i, cop / "skills" / i):
                shutil.copytree(src, dest)
        elif kind == "agent":
            meta, body = split_frontmatter((ROOT / "src" / "agents" / f"{i}.md").read_text())
            c, g = meta.get("claude", {}), meta.get("copilot", {})
            cm = {"name": meta["name"], "description": meta["description"], **c}
            gm = {"name": g.get("title", meta["name"]), "description": meta["description"]}
            gm.update({k: v for k, v in g.items() if k != "title"})
            (plug / "agents").mkdir(parents=True, exist_ok=True)
            (cop / "agents").mkdir(parents=True, exist_ok=True)
            (plug / "agents" / f"{i}.md").write_text(dump_frontmatter(cm, body))
            (cop / "agents" / f"{i}.agent.md").write_text(dump_frontmatter(gm, body))
        elif kind == "prompt":
            meta, body = split_frontmatter((ROOT / "src" / "prompts" / f"{i}.md").read_text())
            targets = meta.get("targets", ["claude", "copilot"])
            cm = {"description": meta["description"], **meta.get("claude", {})}
            gm = {"description": meta["description"], **meta.get("copilot", {})}
            (cop / "prompts").mkdir(parents=True, exist_ok=True)
            if "claude" in targets:
                (plug / "commands").mkdir(parents=True, exist_ok=True)
                (plug / "commands" / f"{i}.md").write_text(dump_frontmatter(cm, body))
            (cop / "prompts" / f"{i}.prompt.md").write_text(dump_frontmatter(gm, body))
        elif kind == "hook":
            src = ROOT / "src" / "hooks" / i
            (plug / "hooks").mkdir(parents=True, exist_ok=True)
            for f in src.iterdir():
                if f.name != "hooks.json":
                    shutil.copy2(f, plug / "hooks" / f.name)
            merged = hooks_by_bundle.setdefault(b, {})
            for event, entries in json.loads((src / "hooks.json").read_text())["hooks"].items():
                merged.setdefault(event, []).extend(entries)
        else:
            raise SystemExit(f"unknown type {kind!r} for {i}")

    for b, merged in hooks_by_bundle.items():
        (ROOT / "plugins" / b / "hooks" / "hooks.json").write_text(json.dumps({"hooks": merged}, indent=2) + "\n")

    used = sorted({a["bundle"] for a in by_id.values()})
    for b in used:
        pj = ROOT / "plugins" / b / ".claude-plugin"
        pj.mkdir(parents=True, exist_ok=True)
        (pj / "plugin.json").write_text(json.dumps({
            "name": b,
            "version": cat["version"],
            "description": cat["bundles"][b]["description"],
            "author": {"name": cat["author"]["name"], "url": cat["author"]["url"]},
            "license": cat["license"],
        }, indent=2) + "\n")
    (ROOT / ".claude-plugin" / "marketplace.json").write_text(json.dumps({
        "name": "devflow-toolkit",
        "owner": {"name": cat["author"]["name"]},
        "description": cat["description"],
        "plugins": [{"name": b, "source": f"./plugins/{b}", "description": cat["bundles"][b]["description"]} for b in used],
    }, indent=2) + "\n")
    print(f"built {len(by_id)} assets, {len(used)} bundles")


if __name__ == "__main__":
    main()
