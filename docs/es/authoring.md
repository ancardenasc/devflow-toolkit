# Autoría: agregar o cambiar un asset

## Preparación

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

## Flujo

1. Escribe la fuente en `src/` (plantillas en [`templates/`](../../templates/)).
2. Agrega una entrada en `catalog.yml` con `id`, `type`, `bundle`, `description` y `description_es`.
3. Genera y verifica:
   ```
   .venv/bin/python scripts/build.py
   .venv/bin/python scripts/gen_readme.py
   .venv/bin/python scripts/lint.py
   .venv/bin/python scripts/smoke_install.py
   claude plugin validate . --strict
   ```
4. Haz commit de la fuente **y** de lo generado juntos. El CI falla si no coinciden.

Edita solo `src/` y `catalog.yml`. `plugins/`, `dist/` y las tablas del catálogo en los README son generados.

## Formatos

**Skill** (`src/skills/<id>/SKILL.md`)
```yaml
---
name: my-skill            # igual al nombre de la carpeta, kebab-case, máx. 64
description: Qué hace y cuándo usarlo. Máx. 1024 caracteres.
argument-hint: "[arg]"    # opcional
license: MIT
---
```
Mantén `SKILL.md` bajo 500 líneas y mueve el detalle de pasos a `references/` (un nivel de profundidad). El texto reutilizable va en `assets/`.

**Agente** (`src/agents/<id>.md`)
```yaml
---
name: my-agent
description: Qué hace y cuándo llamarlo.
claude:  { tools: "Read, Grep, Bash", model: sonnet, color: green }
copilot: { title: My Agent, tools: [read, search, execute] }
---
```

**Prompt** (`src/prompts/<id>.md`), normalmente solo Copilot
```yaml
---
name: my-prompt
description: ...
targets: [copilot]
copilot: { agent: agent, tools: [read, search] }
---
```
Enlaza a skills y agentes con rutas relativas tal como quedan instalados (`../skills/<id>/SKILL.md`, `../agents/<id>.agent.md`).

**Hook** (`src/hooks/<id>/hooks.json` + script). Solo Claude Code. Pon entre comillas `${CLAUDE_PLUGIN_ROOT}` en el comando.

## Reglas para contenido genérico

- **Sin datos de empresa ni personales**: nada de nombres de empresa, prefijos de ticket, ids de tenant o de campo, personas, URLs internas, rutas absolutas. El linter bloquea términos conocidos.
- **Los valores vienen de `.devflow.yml`**, nunca del asset. Agrega una clave a `.devflow.example.yml` y a la tabla de referencia cuando necesites una nueva.
- **Redacción neutral al proveedor**: di "la herramienta del tracker" y da ejemplos con CLI (`gh`, `glab`); deja los nombres de herramientas MCP fuera del frontmatter de los agentes.
- **Solo lectura salvo que el trabajo sea escribir.** Los revisores reciben `Read, Grep, Glob, Bash`.
- **Fallar en voz alta.** Si falta un insumo (ticket, diff), reporta un resultado incompleto, nunca "sin hallazgos".
- **Evidencia antes que afirmaciones.** Exige salida pegada para los pasos completados.
- **Assets en inglés**, con español solo en `description_es` y `docs/es`.
- **Las descripciones YAML** que contengan `: ` deben ir entre comillas. El linter detecta frontmatter inválido.

## Qué revisa el CI

Frontmatter y nombres, largo de la descripción, tamaño de `SKILL.md`, términos prohibidos, links relativos en la salida de Copilot, archivos generados desactualizados, `claude plugin validate`, el smoke test de instalación y un escaneo de secretos.

## Versionado

SemVer en `catalog.yml` (`version`), una entrada de `CHANGELOG.md` por release, un tag git `vX.Y.Z`. Quienes usan el marketplace de plugins se actualizan cuando cambia la versión.
