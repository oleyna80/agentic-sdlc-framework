#!/usr/bin/env python3
"""Fail-closed Codex guard for explicit Owner-approved Hard Stops.

This hook is intentionally separate from write-set enforcement. It controls
irreversible or externally consequential Bash operations and does not attempt
to authorize ordinary source edits.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

GATE_PATH = Path(".agent/active-work-block.json")

SIMPLE_PATTERNS = [
    (re.compile(r"\bgit\s+commit\b", re.I), "git_commit", "git commit"),
    (re.compile(r"\bgit\s+push\b", re.I), "git_push", "git push"),
    (
        re.compile(
            r"\b(git\s+reset\s+--hard|git\s+clean|terraform\s+destroy|"
            r"kubectl\s+delete|DROP\s+(DATABASE|TABLE))\b",
            re.I,
        ),
        "destructive",
        "destructive operation",
    ),
    (
        re.compile(
            r"\b(docker\s+push|kubectl\s+(apply|patch|replace|scale|rollout|set)|"
            r"terraform\s+apply|systemctl\s+(restart|stop|start)|"
            r"service\s+\S+\s+(restart|stop|start)|scp|rsync[^\n]*:)\b",
            re.I,
        ),
        "live_infra",
        "live infrastructure operation",
    ),
    (
        re.compile(
            r"\b(psql|mysql|mongosh|redis-cli)\b[^\n]*\b"
            r"(DELETE|UPDATE|INSERT|ALTER|DROP|TRUNCATE|CREATE)\b",
            re.I,
        ),
        "live_data",
        "direct data mutation",
    ),
    (
        re.compile(
            r"(^|[\s/])(\.env([.][\w.-]+)?|credentials|secrets)([\s/]|$)|"
            r"\b(rotate|revoke)\b[^\n]*(token|secret|key|credential)",
            re.I,
        ),
        "credentials",
        "credential or secret access/mutation",
    ),
    (
        re.compile(
            r"\b(sendmail|mailx|twilio|sendgrid)\b|"
            r"\bcurl\b[^\n]*(messages|email|sms|notifications)[^\n]*"
            r"(-X\s*(POST|PUT|PATCH)|--data)",
            re.I,
        ),
        "client_communications",
        "client-facing communication",
    ),
]


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            },
            ensure_ascii=False,
        )
    )
    raise SystemExit(0)


def read_event() -> dict:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as exc:
        deny(f"Cannot parse PreToolUse input: {exc}")
    if not isinstance(event, dict):
        deny("PreToolUse input must be a JSON object.")
    return event


def root_from(cwd: object) -> Path:
    start = Path(str(cwd or os.getcwd())).resolve()
    for root in (start, *start.parents):
        if (root / GATE_PATH).is_file():
            return root
    deny(f"Cannot find {GATE_PATH.as_posix()} from {start}.")


def load_gate(root: Path) -> dict:
    try:
        gate = json.loads((root / GATE_PATH).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        deny(f"Invalid {GATE_PATH.as_posix()}: {exc}")
    if not isinstance(gate, dict):
        deny("Active Work Block gate must be a JSON object.")
    return gate


def approved(gate: dict, key: str) -> bool:
    approvals = gate.get("hard_stop_approvals")
    return isinstance(approvals, dict) and approvals.get(key) is True


def current_branch(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            timeout=3,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        deny(f"Cannot inspect git branch for push policy: {exc}")
    return result.stdout.strip()


def recursive_rm(command: str) -> bool:
    """Detect rm recursive flags including -r, -rf, -fr and --recursive."""
    for match in re.finditer(r"(?:^|[;&|]\s*)rm\s+([^;&|\n]+)", command, re.I):
        try:
            tokens = shlex.split(match.group(1), posix=True)
        except ValueError:
            return True
        for token in tokens:
            if token == "--":
                break
            if token == "--recursive":
                return True
            if token.startswith("-") and not token.startswith("--") and "r" in token[1:].lower():
                return True
    return False


def require_approval(gate: dict, key: str, label: str) -> None:
    if not approved(gate, key):
        deny(
            f"{label} requires hard_stop_approvals.{key}=true and "
            "recorded Owner approval."
        )


def check_command(command: str, gate: dict, root: Path) -> None:
    if recursive_rm(command):
        require_approval(gate, "destructive", "destructive recursive rm")

    found: set[str] = set()
    for pattern, key, label in SIMPLE_PATTERNS:
        if pattern.search(command):
            found.add(key)
            require_approval(gate, key, label)

    if "git_push" in found:
        explicit_default = re.search(
            r"\bgit\s+push\b[^\n]*(\bmain\b|\bmaster\b|\bHEAD:(main|master)\b)",
            command,
            re.I,
        )
        explicit_ref = re.search(r"\bgit\s+push\b\s+\S+\s+\S+", command, re.I)
        implicit_default = not explicit_ref and current_branch(root) in {"main", "master"}
        if explicit_default or implicit_default:
            require_approval(
                gate,
                "default_branch_push",
                "default-branch push",
            )


def main() -> None:
    event = read_event()
    if str(event.get("tool_name") or "") != "Bash":
        return
    value = event.get("tool_input")
    command = value.get("command") if isinstance(value, dict) else None
    if not isinstance(command, str):
        deny("Bash input is missing tool_input.command.")
    root = root_from(event.get("cwd"))
    gate = load_gate(root)
    check_command(command, gate, root)


if __name__ == "__main__":
    main()
