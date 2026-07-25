#!/usr/bin/env python3
"""Focused Codex PreToolUse guard for destructive Bash operations.

This complements the general write-set policy. It reads the same machine-readable
Work Block gate and does not create a second source of authority.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys

GATE_PATH = Path(".agent/active-work-block.json")
DESTRUCTIVE = re.compile(
    r"(?:^|[;&|]\s*)(?:"
    r"rm\s+(?:--recursive\b|-[A-Za-z]*r[A-Za-z]*\b)|"
    r"git\s+reset\s+--hard\b|"
    r"git\s+clean\s+-[A-Za-z]*f[A-Za-z]*\b|"
    r"terraform\s+destroy\b|"
    r"kubectl\s+delete\b|"
    r"(?:DROP|TRUNCATE)\s+(?:DATABASE|TABLE)\b"
    r")",
    re.IGNORECASE,
)


def deny(reason: str) -> int:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    return 0


def find_root(cwd: Path) -> Path:
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
            timeout=3,
        )
        return Path(result.stdout.strip()).resolve()
    except (OSError, subprocess.SubprocessError):
        current = cwd.resolve()
        for candidate in (current, *current.parents):
            if (candidate / GATE_PATH).is_file():
                return candidate
        return current


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as exc:
        return deny(f"Cannot parse destructive-command guard input: {exc}")
    if not isinstance(event, dict) or str(event.get("tool_name") or "") != "Bash":
        return 0
    tool_input = event.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str) or not DESTRUCTIVE.search(command):
        return 0

    root = find_root(Path(str(event.get("cwd") or os.getcwd())))
    try:
        gate = json.loads((root / GATE_PATH).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return deny(f"Destructive operation blocked: invalid active Work Block gate: {exc}")
    approvals = gate.get("hard_stop_approvals") if isinstance(gate, dict) else None
    if not isinstance(approvals, dict) or approvals.get("destructive") is not True:
        return deny(
            "Destructive operation requires "
            "hard_stop_approvals.destructive=true and recorded Owner approval."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
