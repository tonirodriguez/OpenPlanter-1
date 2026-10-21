# Estado de corrección — error_report.md

## Pregunta
¿Ya está corregido el error reportado en `error_report.md`?

## Respuesta (basada en evidencia del repo)
**No.** El comportamiento que causa el error sigue presente en el código:

- El **shell por defecto** continúa siendo `"/bin/sh"` (no compatible con Windows si no existe un entorno POSIX).
  - Evidencia: `crates/op-core/src/config.rs` en `impl Default for AgentConfig` mantiene `shell: "/bin/sh".into(),`.

- La ejecución de comandos sigue asumiendo el patrón **Unix** `shell -c <command>`.
  - Evidencia: `crates/op-core/src/tools/shell.rs` usa `Command::new(shell).args(["-c", command])...spawn()`.

- No hay evidencia en el repositorio de una rama específica para Windows (por ejemplo `cfg!(windows)`, `cmd.exe /C`, `powershell -Command`) dentro del tool de shell.
  - Evidencia: búsquedas en el árbol `crates/**` no encontraron `cmd.exe`, `powershell`, ni `cfg!(windows)` asociadas al tool.

## Implicación
Si ejecutas OpenPlanter Desktop en Windows **sin configurar** un shell válido (p.ej. Git Bash), `run_shell` seguirá fallando con un error de “no se puede encontrar la ruta/ejecutable”, tal como se describe en `error_report.md`.

## Qué faltaría para considerarlo “corregido”
1) **Fix de código**: detectar Windows y usar `cmd.exe /C` o `powershell.exe -Command` (y ajustar quoting), o
2) **Fix de configuración/documentación**: asegurar que el instalador/app configure `OPENPLANTER_SHELL` a un ejecutable existente.
