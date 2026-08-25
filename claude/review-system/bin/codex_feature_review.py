#!/usr/bin/env python3
"""Cross-platform Codex review launcher used by Claude Code review commands."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

FEATURE_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def fail(message: str, code: int = 1) -> "NoReturn":
    print(f"Codex review launcher error: {message}", file=sys.stderr)
    raise SystemExit(code)


def usage() -> "NoReturn":
    print(
        "Usage:\n"
        "  codex-feature-review brainstorm <feature>\n"
        "  codex-feature-review requirement <feature>\n"
        "  codex-feature-review design <feature>\n"
        "  codex-feature-review plan <feature>\n"
        "  codex-feature-review execution <phase-number> <feature>\n"
        "  codex-feature-review final <feature>",
        file=sys.stderr,
    )
    raise SystemExit(2)


def command_for(executable: str, args: list[str]) -> list[str]:
    """Return an argv that can execute native binaries or Windows .cmd/.bat shims."""
    path = Path(executable)
    if os.name == "nt" and path.suffix.lower() in {".cmd", ".bat"}:
        comspec = os.environ.get("COMSPEC") or shutil.which("cmd.exe") or "cmd.exe"
        command_line = subprocess.list2cmdline([executable, *args])
        return [comspec, "/d", "/s", "/c", command_line]
    return [executable, *args]


def run_text(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
        encoding="utf-8",
        errors="replace",
    )


def main(argv: list[str]) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if len(argv) < 3:
        usage()

    stage = argv[1]
    if stage in {"brainstorm", "requirement", "design", "plan", "final"}:
        if len(argv) != 3:
            usage()
        phase = None
        feature = argv[2]
    elif stage == "execution":
        if len(argv) != 4:
            usage()
        phase = argv[2]
        feature = argv[3]
        if not phase.isdigit() or int(phase) <= 0:
            fail("phase number must be a positive integer")
    else:
        usage()

    if not FEATURE_RE.fullmatch(feature):
        fail("feature name may contain only letters, digits, dot, underscore, and hyphen")

    git = shutil.which("git")
    codex = shutil.which("codex")
    if not git:
        fail("git is not installed or not on PATH")
    if not codex:
        fail("codex CLI is not installed or not on PATH")

    git_result = run_text(command_for(git, ["rev-parse", "--show-toplevel"]))
    if git_result.returncode != 0:
        fail("run this command from inside a Git repository")
    repo_root = Path(git_result.stdout.strip()).resolve()

    feature_dir = repo_root / "claude-features" / feature
    if not feature_dir.is_dir():
        fail(f"feature directory not found: claude-features/{feature}")

    stage_meta = {
        "brainstorm": ("codex-review-brainstorm", "brainstorm"),
        "requirement": ("codex-review-requirement", "requirement"),
        "design": ("codex-review-design", "design"),
        "plan": ("codex-review-plan", "plan"),
        "final": ("codex-final-review", "final"),
    }
    if stage == "execution":
        skill = "codex-review-execution"
        label = f"execution-phase-{phase}"
    else:
        skill, label = stage_meta[stage]

    report_dir = feature_dir / "reviews" / "codex"
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report = report_dir / f"{label}-{timestamp}.md"

    if stage == "execution":
        task = (
            f"Use ${skill} explicitly. Review phase {phase} of feature {feature}. "
            "Treat the phase file and repository artifacts as the contract. "
            "Return only the required review report."
        )
    else:
        task = (
            f"Use ${skill} explicitly. Review feature {feature}. "
            "Treat repository artifacts as authoritative. Return only the required review report."
        )

    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix="codex-review-", suffix=".md", delete=False) as handle:
            tmp_path = Path(handle.name)

        codex_args = [
            "exec",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--cd",
            str(repo_root),
            "--output-last-message",
            str(tmp_path),
        ]
        model = os.environ.get("CODEX_REVIEW_MODEL")
        if model:
            codex_args.extend(["--model", model])
        codex_args.append(task)

        result = run_text(command_for(codex, codex_args), cwd=repo_root)
        if result.returncode != 0:
            print("# Codex Review - BLOCKED\n", file=sys.stderr)
            print("Codex CLI failed before producing a usable review.\n", file=sys.stderr)
            if result.stdout:
                print(result.stdout, file=sys.stderr, end="" if result.stdout.endswith("\n") else "\n")
            if result.stderr:
                print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")
            return 1

        if not tmp_path.is_file() or tmp_path.stat().st_size == 0:
            fail("Codex completed without a final review message")

        content = tmp_path.read_text(encoding="utf-8", errors="replace")
        report.write_text(content, encoding="utf-8", newline="\n")
        print(f'<codex-review-report path="{report}">')
        print(content, end="" if content.endswith("\n") else "\n")
        print("</codex-review-report>")
        return 0
    finally:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
