# Configuración: `.devflow.yml`

Un archivo en la raíz de **tu proyecto** (no de este repo). Todas las claves son opcionales; se muestran los valores por defecto. Parte de [`.devflow.example.yml`](../../.devflow.example.yml). Hay un ejemplo completo con Jira + GitLab en [`examples/jira-gitlab/`](../../examples/jira-gitlab/).

## Referencia

| Clave | Por defecto | Significado | Lo usan |
|---|---|---|---|
| `tracker.type` | `github` | `github`, `jira`, `linear` o `none` | start-task, execute-task, review-ticket, reviewers |
| `tracker.ticket_pattern` | `[A-Z]+-\d+` | Regex que encuentra el id del ticket en el nombre de la rama | commit, start-task, execute-task |
| `tracker.site` | ninguno | Host del tracker, p. ej. `tu-equipo.atlassian.net` (Jira) | task-reviewers |
| `tracker.fields.tester` | ninguno | Campo del ticket con los testers, p. ej. un campo custom de Jira | task-reviewers, execute-task |
| `tracker.fields.sprint` | ninguno | Campo del ticket con el nombre del sprint | task-reviewers |
| `vcs.type` | inferido | `github` o `gitlab` | start-task, execute-task, reviewers |
| `vcs.default_branch` | `main` | Rama base de respaldo | start-task, execute-task, reviewers |
| `vcs.assignee` | ninguno | Assignee por defecto del PR/MR | start-task, execute-task |
| `workflow.base_from_parent` | `true` | Crear la rama desde la rama del ticket padre si existe | start-task, execute-task |
| `workflow.assign_testers` | `false` | Activa la propuesta y asignación de testers | execute-task |
| `branch.pattern` | `{ticket}-{slug}` | Plantilla del nombre de rama | start-task, execute-task |
| `branch.max_slug_length` | `50` | Largo máximo de la parte `{slug}` | start-task, execute-task |
| `commit.format` | `conventional` | `conventional` o una plantilla como `"[{ticket}] {summary}"` | commit |
| `commit.language` | `en` | Idioma de los mensajes de commit | commit |
| `commit.attribution` | `false` | Agrega líneas tipo `Co-Authored-By` | commit |
| `commands.test` | detectado | Comando de tests | start-task, execute-task, unit-test-writer |
| `commands.lint` | detectado | Comando de lint | code-clean |
| `commands.build` | ninguno | Comando de build | execute-task |
| `review.max_auto_passes` | `3` | Pasadas automáticas de corrección y re-revisión por críticos | execute-task |
| `code_style.comments` | `minimal` | `none` prohíbe comentarios en código y tests generados | execute-task |
| `frontend_globs` | `**/*.{vue,jsx,tsx,css,scss,html}` | Archivos que activan la revisión UX | ux-review, execute-task, review-ticket |
| `verify.enabled` | `false` | Verificación en navegador (opt-in) | execute-task |
| `verify.browser` | `chrome` | `chrome` o `playwright` | execute-task |
| `verify.start_command` | ninguno | Comando que levanta el stack local (se ofrece, nunca silencioso) | execute-task |
| `verify.health_checks` | `[]` | `[{name, url, expect}]` verificaciones previas a navegar | execute-task |
| `environment.services` | `[]` | `[{name, path, check}]` para llenar la tabla de entorno de testeo | execute-task |
| `docs.target` | `markdown` | `markdown`, `confluence` o `notion` | execute-task, task-summary |
| `docs.path` | `docs/` | Carpeta, o id de página/carpeta padre en confluence/notion | execute-task, task-summary |
| `a11y.standards` | `["WCAG 2.2 AA"]` | Agrega estándares extra con un archivo en `profiles/` | ux-review |
| `output_language` | `en` | Idioma de reportes, descripciones de PR y resúmenes | todos |
| `subagents.*` | nombres por defecto | Renombra `code_review`, `code_clean`, `ux_review`, `test_writer` | review-ticket, execute-task |
| `reviewers` | ninguno | Lista y subgrupos para asignar testers | task-reviewers |

## Reviewers

```yaml
reviewers:
  load_margin: 1               # entran al sorteo quienes estén a mínimo de carga + margen
  design:
    members:
      - { name: Ana Gomez, tracker_id: "<account id>", vcs_user: anagomez }
  engineering:
    groups:                    # el subgrupo se elige por una palabra clave del nombre del sprint
      - match: Alpha
        members: [{ name: Luis Perez, vcs_user: luisperez }]
```
`tracker_id` y `vcs_user` son opcionales; si faltan se resuelven en vivo y se reportan para que los agregues.

## Perfiles

Los estándares de un país o empresa viven en `profiles/`. Ejemplo: `profiles/colombia.md` agrega una columna NTC 5854 a la revisión UX cuando `a11y.standards` incluye `"NTC 5854"`.

## Dónde se lee el archivo

Los assets leen `.devflow.yml` de la raíz del repo donde trabajas. Nunca se lee nada de tu directorio personal, y los secretos no van en este archivo; guarda los tokens en la configuración de tu MCP o CLI.
