# Contributing

1. Add the asset under `src/` (templates in `templates/`) and an entry in `catalog.yml`.
2. `python -m venv .venv && .venv/bin/pip install -r requirements.txt`
3. `.venv/bin/python scripts/build.py && .venv/bin/python scripts/lint.py`
4. Commit generated output together with the source. CI fails on stale output.
Keep assets generic and vendor-neutral; see AGENTS.md.
