# Platform notes (verified 2026-08-18)

## Supported kit environments

The kit supports:

- macOS
- Linux
- WSL
- native Windows via PowerShell

The substantive install/review logic lives in Python 3.11+ so both platform entry points use the same implementation. The `.sh` and `.ps1` files are thin launchers.

## Claude Code

Current Claude Code documentation supports macOS, Linux, WSL, and native Windows. On native Windows, Claude Code can use Git Bash when Git for Windows is installed and can also use PowerShell; current docs note that Git for Windows is recommended and PowerShell is available as the native fallback/tooling path.

The `/codex-review-*` commands use Claude's dynamic `!` command injection to execute the global review launcher before Claude sees the resulting prompt. During installation, the kit renders a Python launcher plus an absolute forward-slash runner path into those six installed command files. The resulting invocation is valid in both Git Bash and PowerShell on Windows.

The supplied original Claude command `.md` files are not converted or rewritten.

Official Claude documentation:

- https://code.claude.com/docs/en/installation
- https://code.claude.com/docs/en/tools-reference
- https://code.claude.com/docs/en/slash-commands
- https://code.claude.com/docs/en/claude-directory

## Codex

Codex supports repeatable automation through `codex exec`, and the current CLI reference exposes `--sandbox read-only` as a sandbox policy. The CLI reference also includes native-Windows sandbox functionality.

Codex user-level skills live under `<user-home>/.agents/skills`. The kit installs six explicit review skills there. Their `agents/openai.yaml` disables implicit invocation so unrelated Codex tasks are not turned into review gates.

Codex's global instruction home defaults to `<user-home>/.codex` (or `CODEX_HOME`). The kit intentionally does not install a global reviewer `AGENTS.md`.

Codex supports fallback project-instruction filenames through top-level `project_doc_fallback_filenames` in `config.toml`. For each directory, Codex checks `AGENTS.override.md`, then `AGENTS.md`, then configured fallback names. The kit globally adds `CLAUDE.md` to that fallback list while preserving existing values.

The review runner uses:

- `--ephemeral`
- `--sandbox read-only`
- `--cd <repo-root>`
- `--output-last-message <path>`

Official Codex documentation:

- https://developers.openai.com/codex/cli/
- https://developers.openai.com/codex/cli/reference
- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/guides/agents-md/

## Configuration paths

The code does not hard-code Unix path syntax. It derives the current user's home directory with Python and honors:

- `CLAUDE_CONFIG_DIR`
- `CODEX_HOME`

Defaults:

```text
macOS/Linux/WSL:
  ~/.claude
  ~/.codex
  ~/.agents/skills

native Windows:
  %USERPROFILE%\.claude
  %USERPROFILE%\.codex
  %USERPROFILE%\.agents\skills
```

## Python

Python 3.11+ is required because the kit uses the standard-library `tomllib` parser to validate Codex configuration changes.

The Unix launchers expect `python3`. The Windows PowerShell launchers try `py -3`, then `python`, then `python3`. The installer separately detects a Python 3.11+ command that can be embedded in Claude's global Codex-review command files.

## WSL distinction

WSL is treated as Linux, not native Windows. Its home directory and CLI installations are normally separate from the Windows user's native configuration. Install the kit in each environment where you actually run Claude/Codex.
