# Informe de error (OpenPlanter Desktop)

## Resumen
El error `run_shell` que ves (`[WinError 3] El sistema no puede encontrar la ruta especificada`) se produce porque el runtime intenta lanzar un *shell POSIX* por defecto (`/bin/sh`) con argumentos `-c` **en un entorno Windows**, donde normalmente **no existe** `/bin/sh`.

Además, los fallos de `web_search`/`fetch_url` (`EXA_API_KEY not configured`) se deben a que no hay una clave de API configurada para Exa.

## Evidencia (del código en este repo)

### 1) `run_shell` intenta ejecutar el binario configurado en `config.shell`
- Archivo: `crates/op-core/src/tools/shell.rs`
- Evidencia: `Command::new(shell).args(["-c", command]).current_dir(root)...spawn()`

Esto significa que el proceso a ejecutar es literalmente el valor de `shell` (p.ej. `/bin/sh`) y se invoca con `-c <comando>`.

### 2) El valor por defecto de `shell` es `/bin/sh`
- Archivo: `crates/op-core/src/config.rs`
- Evidencia: en `impl Default for AgentConfig` → `shell: "/bin/sh".into(),`
- Evidencia adicional: en `from_env()` → `shell: env_or("OPENPLANTER_SHELL", "/bin/sh"),`

En Windows, `/bin/sh` no existe salvo que uses MSYS2/Git Bash/WSL y apuntes explícitamente al ejecutable.

### 3) Síntoma observado
Cuando se llama a `run_shell` desde el agente (por ejemplo `pwd && ls -la`), el tool devuelve:
`[failed to start: [WinError 3] El sistema no puede encontrar la ruta especificada]`

Ese mensaje coincide con el error típico de Windows cuando `CreateProcess` no encuentra el ejecutable (`/bin/sh`) o cuando la ruta de `current_dir` no es válida. Dado que el workspace sí parece accesible (porque `list_files` funciona), la causa más probable es el ejecutable del shell.

## Causa raíz
**Configuración por defecto no compatible con Windows:**
- Se asume un shell tipo Unix (`/bin/sh` + `-c`).
- En Windows, el shell estándar sería `cmd.exe` (con `/C`) o `powershell.exe` (con `-Command`).

## Cómo solucionarlo
### Opción A (sin tocar código): configurar `OPENPLANTER_SHELL`
Configura la variable de entorno `OPENPLANTER_SHELL` a un shell real disponible en tu máquina, por ejemplo:
- Git Bash: `C:\Program Files\Git\bin\bash.exe` (y seguir usando `-c` funciona)
- MSYS2 bash
- WSL: apuntar a `wsl.exe` (pero entonces cambian los comandos/rutas)

### Opción B (con cambios de código): detectar Windows y usar el shell/args correctos
Implementar lógica tipo:
- Windows → `cmd.exe /C <command>` o `powershell.exe -Command <command>`
- Unix → `/bin/sh -c <command>`

## Nota aparte: `web_search` / `fetch_url`
Los mensajes `EXA_API_KEY not configured` indican que no existe `EXA_API_KEY` o `OPENPLANTER_EXA_API_KEY` en el entorno. Para usar Exa, debes definirla.
