# Claude Code y GitHub Copilot

Una fuente, dos salidas. Editas `src/`; `scripts/build.py` genera lo que lee cada herramienta.

## Qué se comparte y qué se genera

| Tipo de asset | Fuente | Salida Claude Code | Salida Copilot |
|---|---|---|---|
| Skill | `src/skills/<id>/SKILL.md` (+ `references/`, `assets/`) | `plugins/<bundle>/skills/<id>/` | `dist/copilot/skills/<id>/` |
| Agente | `src/agents/<id>.md` (neutral) | `plugins/<bundle>/agents/<id>.md` | `dist/copilot/agents/<id>.agent.md` |
| Prompt | `src/prompts/<id>.md` (neutral) | ninguna (el skill ya da un slash command) | `dist/copilot/prompts/<id>.prompt.md` |
| Hook | `src/hooks/<id>/` | `plugins/<bundle>/hooks/` | no soportado |

Los skills usan el formato abierto Agent Skills (`SKILL.md` con `name` y `description`), que leen ambas herramientas. Agentes y prompts difieren por herramienta, así que un archivo neutral lleva bloques `claude:` y `copilot:` que el generador traduce:

| | Claude Code | Copilot |
|---|---|---|
| Archivo de agente | `.claude/agents/x.md` | `.github/agents/x.agent.md` |
| Lista de herramientas | `tools: Read, Grep, Bash` | `tools: [read, search, execute]` |
| Modelo | `model: sonnet` | normalmente se omite (lo decide el selector) |
| Punto de entrada de prompt | slash command del skill | `.github/prompts/x.prompt.md` |

## Dónde se instalan

| Herramienta | Skills | Agentes | Prompts |
|---|---|---|---|
| Claude Code | `.claude/skills/` | `.claude/agents/` | n/a |
| Copilot | `.github/skills/` | `.github/agents/` | `.github/prompts/` |

Copilot también escanea `.claude/skills/`, así que un proyecto que ya instaló la copia de Claude obtiene los skills en ambas herramientas. Los prompts de Copilot enlazan a skills y agentes con rutas relativas (`../skills/...`), que solo resuelven al instalarse bajo `.github/` como arriba. El smoke test lo verifica.

## Diferencias conocidas

- **Los hooks son solo de Claude Code.** `session-title` no tiene equivalente en Copilot. `install.sh` no puede copiar un hook; usa el plugin, o registra el script como hook `SessionStart` en `.claude/settings.json`.
- **Herramientas de los agentes.** Los agentes publicados son de solo lectura con acceso a shell, así que funcionan con `gh` y `glab`. Los nombres de herramientas MCP dependen del producto, así que los agregas tú; ver [`examples/jira-gitlab/`](../../examples/jira-gitlab/).
- **Llamar agentes.** Claude Code los invoca con su mecanismo de agentes por nombre exacto; en Copilot seleccionas el agente personalizado. Los skills describen ambos en lenguaje neutral.
- **Modelos.** Los agentes de Claude fijan `model: sonnet`. Cámbialo en el archivo instalado si prefieres otro.
- **Sin verificar en vivo en Copilot.** La salida de Copilot sigue los formatos documentados y se valida su estructura en el CI, pero todavía no se ha corrido contra una sesión real de Copilot. Abre un issue si algún campo es rechazado.

## ¿Por qué no mantener dos copias?

Los duplicados a mano se desincronizan. El generador más el CI (`build` no debe producir diff) mantiene ambas salidas alineadas con la fuente.
