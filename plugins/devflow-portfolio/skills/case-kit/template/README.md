# Portfolio Blueprint

Reusable template to build each sample project of a UX / engineering / accessibility portfolio. It turns a 10-phase process into folders and documents.

## How to use

1. Copy this directory as the base of a new project (or generate one with the `case-kit` skill).
2. Follow phases 0-9 in order, filling each file under `docs/`.
3. Do not advance a phase before meeting the "Done when" criterion of the previous one (see each template).
4. At the end, `docs/case-study.md` becomes the public case page.

## Phases and deliverables

| Phase | Folder/file | Done when |
|---|---|---|
| 0 Framing | `docs/brief.md` | Brief + success metrics + licenses listed |
| 1 Research | `docs/research/` | Script, anonymized synthesis, numbered insights |
| 2 Definition | `docs/prd.md` | Short PRD tracing insight -> requirement -> criterion |
| 3 Design | `docs/design/` | Figma/PDF with Research, Flows, Wireframes, UI, Components, A11y, Handoff |
| 4 Validation | `docs/testing/` | Usability report with findings and before/after |
| 5 Build | `src/`, `tests/`, `.github/workflows/` | Green CI, tests, deployed demo |
| 6 A11y QA | `docs/accessibility/` | WCAG matrix + conformance report |
| 7 Launch | - | Stable public URL, tag `v1.0.0` |
| 8 Measurement | `docs/case-study.md` (Results) | Real before/after numbers |
| 9 Storytelling | `docs/case-study.md` + this README | Case readable in 60 s and in 10 min |

## Cross-cutting rules

- If research data or a metric comes from a sample project (not a real client), say so explicitly. Never invent personas or numbers.
- Test participants must be real (5 is enough), with written consent.
- Only OFL, MIT, CC0 or own content for fonts, icons and images.
- No third-party personal data, no identifiable minors, no employer material.
- One ADR (`docs/decisions/NNNN-title.md`) per relevant architecture or design decision.

## Definition of Done: "portfolio ready"

- [ ] Stable, accessible public demo
- [ ] Complete README, LICENSE, green CI
- [ ] Public Figma or PDF showing the process
- [ ] Accessibility report with honest gaps (not only what went well)
- [ ] Published case study with linked evidence
- [ ] No third-party or employer material
