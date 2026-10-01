# devflow-toolkit

[![validate](https://github.com/ancardenasc/devflow-toolkit/actions/workflows/validate.yml/badge.svg)](https://github.com/ancardenasc/devflow-toolkit/actions/workflows/validate.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![assets](https://img.shields.io/badge/assets-13-blue)
![tools](https://img.shields.io/badge/Claude%20Code%20%2B%20Copilot-soportado-8A63D2)
![docs](https://img.shields.io/badge/docs-EN%20%7C%20ES-lightgrey)

**Skills, agentes y prompts para Claude Code y GitHub Copilot que llevan una tarea de ticket a merge:** iniciarla, implementarla con tests, revisarla, documentarla y entregarla, sin hacer merge por ti.

[Read in English](README.md)

Se escribe una vez en `src/` y se genera para ambas herramientas. Tus convenciones (tracker, VCS, formato de commit, comando de tests, idioma) viven en un solo `.devflow.yml`; nada queda amarrado a una empresa.

```mermaid
flowchart LR
  T([Ticket]) --> S[start-task] --> P{{Plan}} --> D[TDD] --> R[3 revisiones locales]
  R --> C[commit] --> PR[PR/MR + CI] --> TS[task-summary] --> M([Listo, sin merge])
```

## Por qué existe

Los asistentes de IA escriben código rápido y lo revisan poco. Estos assets ponen disciplina alrededor de esa velocidad:

- **Gates con evidencia.** Un paso está hecho solo con salida real pegada, nunca con "debería estar bien".
- **Revisiones antes de commits.** Correctitud/seguridad, Clean Code y UX/accesibilidad corren sobre el diff local, las pasadas que hagan falta, antes de escribir el historial.
- **Las decisiones humanas siguen siendo humanas.** Plan, plan de commits y testers esperan tu `go`. Los revisores son de solo lectura. Nada se mergea.
- **Portable.** Ninguna convención de empresa dentro de los assets; todo sale de `.devflow.yml`.

## Instalación

**Claude Code** (marketplace de plugins)
```
/plugin marketplace add ancardenasc/devflow-toolkit
/plugin install devflow-core@devflow-toolkit
/plugin install devflow-review@devflow-toolkit
```

**GitHub Copilot, o manual**
```
git clone https://github.com/ancardenasc/devflow-toolkit && cd devflow-toolkit
scripts/install.sh copilot /ruta/a/tu/proyecto     # o: claude
cp .devflow.example.yml /ruta/a/tu/proyecto/.devflow.yml
```

Luego ejecuta `/start-task` o `/execute-task`. Guía completa: [primeros pasos](docs/es/getting-started.md).

## Contenido

<!-- catalog:start -->
### Skills

| Nombre | Bundle | Descripción |
|---|---|---|
| `commit` | devflow-core | Commits convencionales o con prefijo de ticket a partir del diff, con confirmación y modo batch para otros skills. |
| `start-task` | devflow-core | Inicia una tarea: consulta el ticket, rama base desde el ticket padre, rama con nombre, tests base y PR/MR en borrador. |
| `review-ticket` | devflow-review | Revisa un ticket terminado: verifica el DoD y corre los agentes code-review, code-clean y ux-review; un reporte consolidado y publicación opcional. |
| `execute-task` | devflow-core | Ejecuta una tarea completa: plan, TDD, revisiones locales, commits mínimos, PR/MR con instrucciones de testeo, verificación en navegador y testers opcionales; nunca hace merge. |

### Agentes

| Nombre | Bundle | Descripción |
|---|---|---|
| `unit-test-writer` | devflow-core | Escribe unit tests (Jest/Vitest + Testing Library o Vue Test Utils) de comportamiento, con a11y y flujo TDD rojo/verde. |
| `code-review` | devflow-review | Revisión de solo lectura de correctitud, seguridad OWASP, performance, SOLID y manejo de errores sobre un PR/MR o diff local. |
| `code-clean` | devflow-review | Gate de Clean Code de solo lectura: nombres, funciones, duplicación, código muerto, tests F.I.R.S.T y métricas medidas. |
| `ux-review` | devflow-review | Revisión UX/accesibilidad de solo lectura en cambios frontend: WCAG 2.2 AA, heurísticas de Nielsen, diseño equitativo. |
| `task-summary` | devflow-core | Te prepara para explicar una tarea terminada en voz alta: qué, por qué, cómo funciona, frase corta y preguntas probables; guarda un respaldo. |
| `task-reviewers` | devflow-core | Propone testers balanceados por carga real del sprint (uno de diseño, uno de ingeniería) y, tras confirmar, escribe el ticket y los reviewers del PR/MR; nunca toca el assignee. |

### Prompts / comandos

| Nombre | Bundle | Descripción |
|---|---|---|
| `start-task` | devflow-core | Comando slash de Copilot que ejecuta el skill start-task. |
| `ticket-review` | devflow-review | Comando slash de Copilot para una revisión completa de ticket con resumen ejecutivo. |

### Hooks (solo Claude Code)

| Nombre | Bundle | Descripción |
|---|---|---|
| `session-title` | devflow-core | Nombra cada sesión nueva de Claude Code con la rama git (solo Claude Code). |
<!-- catalog:end -->

Bundles: **devflow-core** (flujo), **devflow-review** (revisores de solo lectura). Instala solo lo que necesites.

> El skill `case-kit` (estructura de casos de estudio de portafolio) se movió a [ux-skills-es](https://github.com/ancardenasc/ux-skills-es), junto con `case-study-writer`, en español e inglés.

## Configuración

Copia [`.devflow.example.yml`](.devflow.example.yml) a la raíz de tu proyecto como `.devflow.yml`. Todas las claves son opcionales. Configuración mínima con GitHub:

```yaml
tracker: { type: github }
vcs: { type: github, default_branch: main }
commands: { test: "npm test" }
```

Referencia: [configuración](docs/es/configuration.md). Jira + GitLab con servidores MCP: [`examples/jira-gitlab/`](examples/jira-gitlab/).

## Una fuente, dos herramientas

`src/` (neutral) -> `scripts/build.py` -> `plugins/` (Claude Code) y `dist/copilot/` (Copilot). Los skills usan el formato abierto Agent Skills que leen ambas herramientas; agentes y prompts se traducen por herramienta. El CI mantiene lo generado alineado con la fuente. Detalles y diferencias conocidas: [cross-tool](docs/es/cross-tool.md).

## Estructura del repositorio

```
src/            fuentes neutrales (skills, agentes, prompts, hooks)
plugins/        plugins de Claude Code generados + marketplace
dist/copilot/   agentes, prompts y skills de Copilot generados
profiles/       estándares opcionales por país/empresa (p. ej. NTC 5854)
examples/       configuraciones de ejemplo (Jira + GitLab)
templates/      puntos de partida para assets nuevos
scripts/        build, lint, instalación, smoke test
docs/{en,es}/   documentación
catalog.yml     catálogo de assets; las tablas del README se generan de aquí
```

## Documentación

[Primeros pasos](docs/es/getting-started.md) · [Flujo](docs/es/workflow.md) · [Configuración](docs/es/configuration.md) · [Cross-tool](docs/es/cross-tool.md) · [Autoría](docs/es/authoring.md)

## Estado y límites

Versión 0.1. La estructura, el frontmatter y los links se validan en el CI y los plugins de Claude cargan en una sesión real. La salida de Copilot sigue los formatos documentados pero todavía no se ha corrido en una sesión real de Copilot, y los flujos largos (`execute-task`, `review-ticket`) no se han ejercitado contra un tracker y un PR reales. Los issues y comentarios son bienvenidos.

## Seguridad

Los assets pueden controlar shell, git y trackers. Lee un asset antes de instalarlo y guarda los tokens en tu propia configuración de MCP/CLI, nunca en este repo. Ver [SECURITY.md](SECURITY.md).

## Contribuir y licencia

Ver [CONTRIBUTING.md](CONTRIBUTING.md) y [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). MIT, (c) 2026 Nicolas Cardenas.
