#!/usr/bin/env python3
"""Cross-platform uninstaller for only the Codex-backed review integration."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("ERROR: Python 3.11+ is required.")

CODEX_COMMANDS = [
    "codex-review-brainstorm",
    "codex-review-requirement",
    "codex-review-design",
    "codex-review-plan",
    "codex-review-execution",
    "codex-final-review",
]


def main() -> int:
    home = Path.home()
    claude_home = Path(os.environ.get("CLAUDE_CONFIG_DIR", home / ".claude")).expanduser()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser()
    codex_config = codex_home / "config.toml"
    codex_skills_home = home / ".agents" / "skills"
    state_dir = claude_home / "review-system" / "state"
    fallback_state = state_dir / "codex-claude-fallback-added"
    installed_bin = claude_home / "review-system" / "bin"
    helper = installed_bin / "codex_config_fallback.py"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Reverse the CLAUDE.md fallback only when installation state records that this kit added it.
    if fallback_state.is_file():
        mode = fallback_state.read_text(encoding="utf-8").strip()
        if helper.is_file():
            if codex_config.is_file():
                backup = codex_config.with_name(codex_config.name + f".backup-{stamp}")
                shutil.copy2(codex_config, backup)
                print(f"Backed up before uninstall: {codex_config} -> {backup}")
            result = subprocess.run(
                [sys.executable, str(helper), "remove", str(codex_config), mode],
                text=True,
                capture_output=True,
                check=False,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode == 0:
                print(f"Codex CLAUDE.md fallback: {result.stdout.strip()}")
                fallback_state.unlink(missing_ok=True)
            else:
                sys.stderr.write(result.stderr or result.stdout)
                print(f"WARNING: leaving {codex_config} unchanged because fallback removal failed.", file=sys.stderr)
        else:
            print(f"WARNING: fallback helper is missing; leaving {codex_config} unchanged.", file=sys.stderr)
    else:
        print("Codex CLAUDE.md fallback left unchanged (it was not recorded as added by this kit).")

    # Remove only the new Codex-backed integration. Preserve original Claude commands and CLAUDE.md.
    for name in CODEX_COMMANDS:
        (claude_home / "commands" / f"{name}.md").unlink(missing_ok=True)
        shutil.rmtree(codex_skills_home / name, ignore_errors=True)

    for name in [
        "codex_feature_review.py",
        "codex_config_fallback.py",
        "codex-feature-review",
        "codex-config-fallback",
        "codex-feature-review.cmd",
        "codex-config-fallback.cmd",
        "codex-feature-review.ps1",
        "codex-config-fallback.ps1",
    ]:
        (installed_bin / name).unlink(missing_ok=True)

    for directory in (state_dir, installed_bin, claude_home / "review-system"):
        try:
            directory.rmdir()
        except OSError:
            pass

    print("Removed Codex-backed review integration. Original Claude workflow files and global CLAUDE.md were left untouched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
