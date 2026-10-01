# Primeros pasos

Cinco minutos desde cero hasta tu primera tarea asistida.

## 1. Instalar

**Claude Code** (marketplace de plugins, recomendado)
```
/plugin marketplace add ancardenasc/devflow-toolkit
/plugin install devflow-core@devflow-toolkit
/plugin install devflow-review@devflow-toolkit
```
Agrega `devflow-portfolio@devflow-toolkit` si quieres la estructura de caso de estudio.

**GitHub Copilot, o Claude Code sin plugins**
```
git clone https://github.com/ancardenasc/devflow-toolkit
cd devflow-toolkit
scripts/install.sh copilot /ruta/a/tu/proyecto     # escribe .github/{agents,prompts,skills}
scripts/install.sh claude  /ruta/a/tu/proyecto     # escribe .claude/{agents,skills}
```

Más opciones y salvedades: [cross-tool](cross-tool.md).

## 2. Configurar tu proyecto

Copia el archivo de ejemplo a la raíz del proyecto donde trabajas y edita los pocos valores que difieran de los predeterminados:

```
cp .devflow.example.yml /ruta/a/tu/proyecto/.devflow.yml
```

Todas las claves son opcionales. Sin archivo, los assets infieren el VCS de `git remote get-url origin`, asumen `main` y preguntan si hay dudas. Referencia completa: [configuración](configuration.md).

Configuración mínima con GitHub:
```yaml
tracker: { type: github }
vcs: { type: github, default_branch: main }
commands: { test: "npm test" }
```

## 3. Usarlo

| Quieres | Ejecuta | Bundle |
|---|---|---|
| Iniciar una tarea: rama, tests base, PR en borrador | `/start-task` | devflow-core |
| Ejecutar una tarea completa (plan, TDD, revisiones, PR) | `/execute-task` | devflow-core |
| Crear un commit con el mensaje correcto | `/commit` | devflow-core |
| Revisar un ticket/PR terminado | `/review-ticket` | devflow-review |
| Generar un repo de caso de estudio | `/case-kit <dir> <nombre>` | devflow-portfolio |

En Claude Code el plugin les pone namespace (`/devflow-core:start-task`); si copias los archivos tienen el nombre corto. En Copilot Chat los prompts `/start-task` y `/ticket-review` llaman a los mismos skills.

Los agentes de revisión y apoyo (`code-review`, `code-clean`, `ux-review`, `unit-test-writer`, `task-summary`, `task-reviewers`) los invocan los skills, y también puedes llamarlos directamente.

## 4. Qué esperar

- Cada skill **confirma antes de actuar** y **pega evidencia real** (salida de comandos, URLs) en vez de afirmar que terminó.
- Los revisores son de **solo lectura**; nada se hace merge por ti, nunca.
- Todo lo específico de tu empresa (prefijo de ticket, formato de commit, lista de testers, espacio de docs) va en `.devflow.yml`, nunca dentro de los assets.

Siguiente: [cómo encaja el flujo](workflow.md).
