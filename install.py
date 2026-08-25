#!/usr/bin/env python3
"""Cross-platform installer for the Claude Code + Codex review kit."""

from __future__ import annotations

import filecmp
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("ERROR: Python 3.11+ is required.")

KIT_DIR = Path(__file__).resolve().parent
ORIGINAL_COMMANDS = [
    "brainstorm",
    "checkpoint",
    "design",
    "execute-plan",
    "final-review",
    "new-feature",
    "plan",
    "requirement",
    "review-brainstorm",
    "review-design",
    "review-execution",
    "review-plan",
    "review-requirement",
]
CODEX_COMMANDS = [
    "codex-review-brainstorm",
    "codex-review-requirement",
    "codex-review-design",
    "codex-review-plan",
    "codex-review-execution",
    "codex-final-review",
]
CODEX_SKILLS = CODEX_COMMANDS.copy()
TOKEN = "__CODEX_FEATURE_REVIEW__"


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def same_file(a: Path, b: Path) -> bool:
    return b.is_file() and filecmp.cmp(a, b, shallow=False)


def copy_file(src: Path, dst: Path, stamp: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not same_file(src, dst):
        backup = dst.with_name(dst.name + f".backup-{stamp}")
        shutil.copy2(dst, backup)
        print(f"Backed up: {dst} -> {backup}")
    shutil.copy2(src, dst)
    print(f"Installed: {dst}")


def run_helper(helper: Path, *args: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(helper), *args],
        text=True,
        capture_output=capture,
        check=False,
        encoding="utf-8",
        errors="replace",
    )


def python_launcher() -> str:
    """Return a launcher expression valid in both native Windows shells used by Claude Code."""
    candidates: list[list[str]]
    if os.name == "nt":
        candidates = [["py", "-3"], ["python"], ["python3"]]
    else:
        candidates = [["python3"], ["python"]]

    for candidate in candidates:
        executable = shutil.which(candidate[0])
        if not executable:
            continue
        result = subprocess.run(
            [*candidate, "-c", "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0:
            return " ".join(candidate)
    raise SystemExit(
        "ERROR: could not find a Python 3.11+ launcher on PATH. "
        "Install Python 3.11+ and ensure python3/python (macOS/Linux/WSL) or py/python (Windows) is available."
    )


def shell_path(path: Path) -> str:
    # Forward slashes are accepted by Windows Python and PowerShell, and are native on POSIX.
    return path.resolve().as_posix()


def render_codex_command(template: Path, runner: Path, launcher: str) -> str:
    text = template.read_text(encoding="utf-8")
    if TOKEN not in text:
        raise SystemExit(f"ERROR: Codex command template is missing {TOKEN}: {template}")
    invocation = f'{launcher} "{shell_path(runner)}"'
    return text.replace(TOKEN, invocation)


def install_rendered_command(template: Path, dst: Path, runner: Path, launcher: str, stamp: str) -> None:
    rendered = render_codex_command(template, runner, launcher)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        existing = dst.read_text(encoding="utf-8", errors="replace")
        if existing != rendered:
            backup = dst.with_name(dst.name + f".backup-{stamp}")
            shutil.copy2(dst, backup)
            print(f"Backed up: {dst} -> {backup}")
    dst.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"Installed: {dst}")


def main() -> int:
    stamp = timestamp()
    home = Path.home()
    claude_home = Path(os.environ.get("CLAUDE_CONFIG_DIR", home / ".claude")).expanduser()
    codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser()
    codex_config = codex_home / "config.toml"
    codex_skills_home = home / ".agents" / "skills"
    state_dir = claude_home / "review-system" / "state"
    fallback_state = state_dir / "codex-claude-fallback-added"
    installed_bin = claude_home / "review-system" / "bin"

    for directory in (claude_home / "commands", installed_bin, state_dir, codex_skills_home, codex_home):
        directory.mkdir(parents=True, exist_ok=True)

    launcher = python_launcher()

    # Preserve the user's existing global CLAUDE.md unless absent or already identical.
    src_claude = KIT_DIR / "claude" / "CLAUDE.md"
    dst_claude = claude_home / "CLAUDE.md"
    if not dst_claude.exists():
        copy_file(src_claude, dst_claude, stamp)
    elif same_file(src_claude, dst_claude):
        print(f"Already current: {dst_claude}")
    else:
        candidate = claude_home / "CLAUDE.review-kit.md"
        copy_file(src_claude, candidate, stamp)
        print(f"Preserved existing global CLAUDE.md. Review/merge candidate written to: {candidate}")

    # Original Claude workflow remains the Claude-only path.
    for name in ORIGINAL_COMMANDS:
        copy_file(KIT_DIR / "claude" / "commands" / f"{name}.md", claude_home / "commands" / f"{name}.md", stamp)

    # Shared cross-platform Python cores plus optional convenience wrappers.
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
        src = KIT_DIR / "claude" / "review-system" / "bin" / name
        if src.exists():
            copy_file(src, installed_bin / name, stamp)

    # POSIX wrappers should be executable when the host supports POSIX mode bits.
    if os.name != "nt":
        for name in ("codex-feature-review", "codex-config-fallback"):
            path = installed_bin / name
            if path.exists():
                path.chmod(path.stat().st_mode | 0o111)

    runner = installed_bin / "codex_feature_review.py"
    helper = installed_bin / "codex_config_fallback.py"

    # New Codex-backed Claude commands are rendered with the Python launcher detected at install time.
    for name in CODEX_COMMANDS:
        template = KIT_DIR / "claude" / "codex-commands" / f"{name}.md"
        install_rendered_command(template, claude_home / "commands" / f"{name}.md", runner, launcher, stamp)

    # Make existing project CLAUDE.md files visible to Codex without per-project AGENTS.md files.
    check = run_helper(helper, "check", str(codex_config), capture=True)
    if check.returncode == 0:
        print(f"Already configured: Codex treats CLAUDE.md as a project instruction fallback ({codex_config})")
    elif check.returncode == 1:
        if codex_config.is_file():
            backup = codex_config.with_name(codex_config.name + f".backup-{stamp}")
            shutil.copy2(codex_config, backup)
            print(f"Backed up: {codex_config} -> {backup}")
        ensured = run_helper(helper, "ensure", str(codex_config), capture=True)
        if ensured.returncode != 0:
            sys.stderr.write(ensured.stderr or ensured.stdout)
            raise SystemExit(f"ERROR: could not safely update {codex_config}")
        result = ensured.stdout.strip()
        if result in {"created-key", "extended-key"}:
            fallback_state.write_text(result + "\n", encoding="utf-8")
        elif result != "already-present":
            raise SystemExit(f"ERROR: unexpected Codex fallback configuration result: {result}")
        print(f"Configured: {codex_config} includes CLAUDE.md in project_doc_fallback_filenames")
    else:
        sys.stderr.write(check.stderr or check.stdout)
        raise SystemExit(f"ERROR: could not safely inspect {codex_config}. No Codex config changes were made.")

    # Codex-native global skills.
    skills_src = KIT_DIR / "codex" / "skills"
    for name in CODEX_SKILLS:
        src = skills_src / name
        dst = codex_skills_home / name
        if dst.exists():
            backup = codex_skills_home / f"{name}.backup-{stamp}"
            if backup.exists():
                shutil.rmtree(backup)
            shutil.move(str(dst), str(backup))
            print(f"Backed up: {dst} -> {backup}")
        shutil.copytree(src, dst)
        print(f"Installed Codex skill: {dst}")

    print("\nInstallation complete.")
    print(f"Platform: {'Windows' if os.name == 'nt' else 'POSIX/WSL'}")
    print(f"Claude global config: {claude_home}")
    print(f"Codex global skills: {codex_skills_home}")
    print(f"Codex config: {codex_config} (CLAUDE.md fallback enabled)")
    print(f"Review command Python launcher: {launcher}")
    print("\nRun the platform verifier, then start a new Claude Code/Codex session so discovery uses the updated global configuration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
