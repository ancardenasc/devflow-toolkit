# devflow-toolkit

> Skills, agentes y prompts reutilizables para **Claude Code** y **GitHub Copilot** que llevan una tarea de ticket a merge: iniciar, implementar con tests, revisar, documentar y entregar.

[Read in English](README.md)

Se escribe una vez en `src/` y se genera para ambas herramientas. Las convenciones del proyecto (tracker, VCS, formato de commit, comando de tests, idioma) viven en un solo `.devflow.yml`; nada queda amarrado a una empresa.

## Instalación

**Claude Code** (marketplace de plugins)
```
/plugin marketplace add ancardenasc/devflow-toolkit
/plugin install devflow-core@devflow-toolkit
```

**GitHub Copilot / manual**
```
git clone https://github.com/ancardenasc/devflow-toolkit && cd devflow-toolkit
scripts/install.sh copilot /ruta/a/tu/proyecto   # o: claude
cp .devflow.example.yml /ruta/a/tu/proyecto/.devflow.yml
```

## Contenido

<!-- catalog:start -->
### Skills

| Nombre | Bundle | Descripcion |
|---|---|---|
| `commit` | devflow-core | Commits convencionales o con prefijo de ticket a partir del diff, con confirmacion y modo batch para otros skills. |
| `case-kit` | devflow-portfolio | Genera un repo de caso de estudio de portafolio en 10 fases (brief, investigacion, PRD, diseno, pruebas, accesibilidad, caso). |

### Agentes

| Nombre | Bundle | Descripcion |
|---|---|---|
| `unit-test-writer` | devflow-core | Escribe unit tests (Jest/Vitest + Testing Library o Vue Test Utils) de comportamiento, con a11y y flujo TDD rojo/verde. |
| `code-review` | devflow-review | Revision de solo lectura de correccion, seguridad OWASP, performance, SOLID y manejo de errores sobre un PR/MR o diff local. |
| `code-clean` | devflow-review | Gate de Clean Code de solo lectura - nombres, funciones, duplicacion, codigo muerto, tests F.I.R.S.T y metricas medidas. |
| `ux-review` | devflow-review | Revision UX/accesibilidad de solo lectura en cambios frontend - WCAG 2.2 AA, heuristicas de Nielsen, diseno equitativo. |
<!-- catalog:end -->

## Configuración

Copia [`.devflow.example.yml`](.devflow.example.yml) a la raíz de tu proyecto como `.devflow.yml`. Los assets leen de ahí patrón de ticket, rama por defecto, formato de commit, comandos de test/lint/build, destino de docs, estándares de accesibilidad e idioma de salida.

## Cómo funciona

`src/` (neutral) -> `scripts/build.py` -> `plugins/` (Claude) + `dist/copilot/` (Copilot). Los skills usan el formato abierto Agent Skills que comparten ambas herramientas; agentes y prompts se traducen por herramienta. Ver [AGENTS.md](AGENTS.md).

## Seguridad

Los assets pueden controlar shell y trackers. Revísalos antes de instalar. Ver [SECURITY.md](SECURITY.md).

## Contribuir y licencia

Ver [CONTRIBUTING.md](CONTRIBUTING.md). MIT, (c) 2026 Nicolas Cardenas.
