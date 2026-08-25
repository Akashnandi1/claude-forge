#!/usr/bin/env python3
"""Safely manage CLAUDE.md in Codex project_doc_fallback_filenames."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover - Python < 3.11
    raise SystemExit("Python 3.11+ is required to update Codex TOML configuration safely.") from exc

KEY = "project_doc_fallback_filenames"
TARGET = "CLAUDE.md"
KEY_RE = re.compile(r"(?m)^[ \t]*project_doc_fallback_filenames[ \t]*=")
TABLE_RE = re.compile(r"(?m)^[ \t]*\[")


class ConfigError(RuntimeError):
    pass


def _find_assignment(text: str) -> tuple[int, int, int, int] | None:
    """Return (assignment_start, value_start, value_end, assignment_end)."""
    match = KEY_RE.search(text)
    if not match:
        return None

    # This setting is a root-level Codex config key. Refuse to edit an occurrence
    # that appears after a TOML table header because that would be table-scoped.
    first_table = TABLE_RE.search(text)
    if first_table and first_table.start() < match.start():
        raise ConfigError(
            f"Found {KEY} after a TOML table header. Move it to top level before rerunning the installer."
        )

    eq = text.find("=", match.start(), match.end() + 1)
    if eq < 0:
        raise ConfigError(f"Could not parse {KEY} assignment.")

    value_start = eq + 1
    while value_start < len(text) and text[value_start] in " \t":
        value_start += 1
    if value_start >= len(text) or text[value_start] != "[":
        raise ConfigError(f"{KEY} must be a TOML array.")

    # Find the matching closing bracket, respecting TOML strings and comments.
    depth = 0
    in_basic = False
    in_literal = False
    escape = False
    in_comment = False
    i = value_start
    close = None
    while i < len(text):
        ch = text[i]
        if in_comment:
            if ch == "\n":
                in_comment = False
            i += 1
            continue
        if in_basic:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_basic = False
            i += 1
            continue
        if in_literal:
            if ch == "'":
                in_literal = False
            i += 1
            continue
        if ch == "#":
            in_comment = True
        elif ch == '"':
            in_basic = True
        elif ch == "'":
            in_literal = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                close = i
                break
        i += 1

    if close is None:
        raise ConfigError(f"Could not find closing bracket for {KEY}.")

    # Assignment end includes the remainder of the line so trailing comments survive.
    line_end = text.find("\n", close)
    assignment_end = len(text) if line_end < 0 else line_end + 1
    return match.start(), value_start, close + 1, assignment_end


def _parse_values(text: str, value_start: int, value_end: int) -> list[str]:
    raw = text[value_start:value_end]
    try:
        parsed = tomllib.loads(f"{KEY} = {raw}\n")[KEY]
    except Exception as exc:  # tomllib raises TOMLDecodeError, kept broad for portability
        raise ConfigError(f"Could not parse {KEY}: {exc}") from exc
    if not isinstance(parsed, list) or not all(isinstance(v, str) for v in parsed):
        raise ConfigError(f"{KEY} must contain only string filenames.")
    return parsed


def _toml_array(values: list[str]) -> str:
    # JSON string escaping is compatible with TOML basic strings for these filenames.
    return "[" + ", ".join(json.dumps(v) for v in values) + "]"


def _validate_full_config(text: str) -> None:
    try:
        tomllib.loads(text)
    except Exception as exc:
        raise ConfigError(f"Resulting config.toml would be invalid TOML: {exc}") from exc


def check(path: Path) -> int:
    if not path.exists():
        print(f"MISSING {path}: {TARGET} is not configured as a Codex fallback filename")
        return 1
    text = path.read_text(encoding="utf-8")
    assignment = _find_assignment(text)
    if assignment is None:
        print(f"MISSING {KEY} in {path}")
        return 1
    _, value_start, value_end, _ = assignment
    values = _parse_values(text, value_start, value_end)
    if TARGET in values:
        print(f"OK {path}: {TARGET} is configured as a Codex fallback filename")
        return 0
    print(f"MISSING {path}: {KEY} does not include {TARGET}")
    return 1


def ensure(path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    _validate_full_config(text or "\n")
    assignment = _find_assignment(text)

    if assignment is None:
        line = f'{KEY} = ["{TARGET}"]\n'
        # Root-level keys must appear before the first table header.
        table = TABLE_RE.search(text)
        insert_at = table.start() if table else 0
        prefix = text[:insert_at]
        suffix = text[insert_at:]
        if prefix and not prefix.endswith("\n"):
            prefix += "\n"
        new_text = prefix + line
        if suffix and not new_text.endswith("\n"):
            new_text += "\n"
        new_text += suffix
        _validate_full_config(new_text)
        path.write_text(new_text, encoding="utf-8")
        return "created-key"

    start, value_start, value_end, _ = assignment
    values = _parse_values(text, value_start, value_end)
    if TARGET in values:
        return "already-present"

    values.append(TARGET)
    new_text = text[:value_start] + _toml_array(values) + text[value_end:]
    _validate_full_config(new_text)
    path.write_text(new_text, encoding="utf-8")
    return "extended-key"


def remove(path: Path, mode: str) -> str:
    if not path.exists():
        return "already-absent"
    text = path.read_text(encoding="utf-8")
    assignment = _find_assignment(text)
    if assignment is None:
        return "already-absent"
    start, value_start, value_end, assignment_end = assignment
    values = _parse_values(text, value_start, value_end)
    if TARGET not in values:
        return "already-absent"

    remaining = [v for v in values if v != TARGET]
    if mode == "created-key" and not remaining:
        new_text = text[:start] + text[assignment_end:]
    else:
        new_text = text[:value_start] + _toml_array(remaining) + text[value_end:]
    _validate_full_config(new_text or "\n")
    path.write_text(new_text, encoding="utf-8")
    return "removed"


def main(argv: list[str]) -> int:
    if len(argv) < 3 or argv[1] not in {"check", "ensure", "remove"}:
        print(
            "Usage: codex-config-fallback {check|ensure|remove} <config.toml> [created-key|extended-key]",
            file=sys.stderr,
        )
        return 2
    action = argv[1]
    path = Path(argv[2]).expanduser()
    try:
        if action == "check":
            return check(path)
        if action == "ensure":
            print(ensure(path))
            return 0
        mode = argv[3] if len(argv) >= 4 else "extended-key"
        if mode not in {"created-key", "extended-key"}:
            raise ConfigError(f"Unknown removal mode: {mode}")
        print(remove(path, mode))
        return 0
    except ConfigError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
