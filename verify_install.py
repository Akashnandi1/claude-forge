#!/usr/bin/env python3
"""Cross-platform installation verifier for the Claude Code + Codex review kit."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
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
CLAUDE_REVIEW_COMMANDS = [
    "review-brainstorm",
    "review-requirement",
    "review-design",
    "review-plan",
    "review-execution",
    "final-review",
]


def main() -> int:
    home = Path.home()
    claude_home = Path(os.environ.get("CLAUDE_CONFIG_DIR", home / ".claude")).expanduser()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser()
    codex_config = codex_home / "config.toml"
    codex_skills_home = home / ".agents" / "skills"
    installed_bin = claude_home / "review-system" / "bin"
    helper = installed_bin / "codex_config_fallback.py"

    failed = False

    def ok(message: str) -> None:
        print(f"OK   {message}")

    def miss(message: str) -> None:
        nonlocal failed
        print(f"MISS {message}")
        failed = True

    def check_file(path: Path) -> None:
        ok(str(path)) if path.is_file() else miss(str(path))

    print("CLI/runtime checks")
    claude = shutil.which("claude")
    codex = shutil.which("codex")
    ok(f"claude: {claude}") if claude else miss("claude CLI")
    ok(f"codex:  {codex}") if codex else miss("codex CLI")
    ok(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

    print("\nClaude command checks")
    for name in [*CLAUDE_REVIEW_COMMANDS, *CODEX_COMMANDS]:
        check_file(claude_home / "commands" / f"{name}.md")
    for name in [
        "codex_feature_review.py",
        "codex_config_fallback.py",
    ]:
        check_file(installed_bin / name)

    print("\nCodex project-instruction fallback check")
    if helper.is_file():
        result = subprocess.run(
            [sys.executable, str(helper), "check", str(codex_config)],
            text=True,
            capture_output=True,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
        output = (result.stdout or result.stderr).strip()
        print(output)
        if result.returncode != 0:
            failed = True
    else:
        miss("fallback configuration helper")

    print("\nCodex skill checks")
    for name in CODEX_COMMANDS:
        check_file(codex_skills_home / name / "SKILL.md")

    if failed:
        print("\nVerification found missing or incomplete components.", file=sys.stderr)
        return 1
    print("\nAll expected files and global Codex fallback configuration are installed. Start a new Claude Code/Codex session if these were just installed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
