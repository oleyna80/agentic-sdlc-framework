#!/usr/bin/env python3
"""Provider-neutral guardrail for consequential Bash operations.

This hook is deliberately cooperative. It denies obvious dangerous commands in
the normal agent channel, while the real security boundary is external GitHub,
OS, workflow, and credential capability separation.
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

RUNTIME_COMMANDS = {
    "codex": "codex-cli",
    "opencode": "opencode-cli",
    "claude": "claude-code-cli",
}

CONSEQUENTIAL = [
    (
        re.compile(
            r"\b(git\s+reset\s+--hard|git\s+clean|terraform\s+destroy|"
            r"kubectl\s+delete|DROP\s+(DATABASE|TABLE))\b",
            re.I,
        ),
        "destructive operation",
    ),
    (
        re.compile(
            r"\b(kubectl\s+(apply|patch|replace|scale|rollout|set)|"
            r"terraform\s+apply|systemctl\s+(restart|stop|start)|"
            r"service\s+\S+\s+(restart|stop|start)|scp|ssh|rsync[^\n]*:)\b",
            re.I,
        ),
        "live infrastructure operation",
    ),
    (
        re.compile(r"\bdocker\s+push\b", re.I),
        "external image publish",
    ),
    (
        re.compile(
            r"\b(psql|mysql|mongosh|redis-cli)\b[^\n]*\b"
            r"(DELETE|UPDATE|INSERT|ALTER|DROP|TRUNCATE|CREATE)\b",
            re.I,
        ),
        "direct live-data mutation",
    ),
    (
        re.compile(
            r"(^|[\s/])(\.env([.][\w.-]+)?|credentials|secrets)([\s/]|$)|"
            r"\b(rotate|revoke)\b[^\n]*(token|secret|key|credential)",
            re.I,
        ),
        "credential or secret operation",
    ),
    (
        re.compile(
            r"\b(sendmail|mailx|twilio|sendgrid|msmtp|ssmtp)\b|"
            r"\bcurl\b[^\n]*(messages|email|sms|notifications|whatsapp)[^\n]*"
            r"(-X\s*(POST|PUT|PATCH)|--data)",
            re.I,
        ),
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


def git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, check=True, capture_output=True,
            text=True, timeout=3
        )
    except (OSError, subprocess.SubprocessError) as exc:
        deny(f"Cannot inspect git state for Hard Stop policy: {exc}")
    return result.stdout.strip()


def current_branch(root: Path) -> str:
    return git(root, "branch", "--show-current")


def recursive_rm(command: str) -> bool:
    prefix = r"(?:(?:sudo|command|env)\s+)?"
    for match in re.finditer(
        rf"(?:^|[;&|\n]\s*){prefix}rm\s+([^;&|\n]+)", command, re.I
    ):
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


def force_push(command: str) -> bool:
    return bool(
        re.search(r"\bgit\s+push\b[^\n]*(?:\s-f(?:\s|$)|--force(?:-with-lease)?\b|\s\+[^\s]+)", command, re.I)
    )


def push_segments(command: str) -> list[str]:
    return [
        match.group(1).strip()
        for match in re.finditer(
            r"(?:^|[;&|\n]\s*)git\s+push\b([^;&|\n]*)", command, re.I
        )
    ]


def pushes_default_branch(command: str, root: Path) -> bool:
    branch = current_branch(root)
    for segment in push_segments(command):
        if re.search(
            r"(?:^|\s)[+:]?(?:HEAD:)?(?:refs/heads/)?(?:main|master)(?:\s|$)",
            segment,
            re.I,
        ):
            return True
        try:
            tokens = shlex.split(segment, posix=True)
        except ValueError:
            return branch in {"main", "master"}
        positional = [token for token in tokens if not token.startswith("-")]
        if branch in {"main", "master"}:
            # No explicit refspec (`git push [remote]`) pushes the current branch,
            # and explicit `HEAD` also denotes the current branch. An explicitly
            # named non-default ref such as `git push origin feature` is not a
            # direct default-branch mutation.
            if len(positional) <= 1:
                return True
            refspecs = positional[1:]
            if any(ref.upper() == "HEAD" for ref in refspecs):
                return True
    return False


def runtime_invocations(command: str) -> set[str]:
    found: set[str] = set()
    prefix = r"(?:(?:sudo|command|env)\s+)?"
    for runtime, integration_id in RUNTIME_COMMANDS.items():
        if re.search(
            rf"(?:^|[;&|\n]\s*){prefix}{re.escape(runtime)}(?:\s|$)",
            command,
            re.I,
        ):
            found.add(integration_id)
    return found


def require_integration(gate: dict, integration_id: str) -> None:
    integrations = gate.get("integrations")
    if not isinstance(integrations, dict):
        deny(f"External runtime {integration_id!r} is not admitted.")
    allowed = integrations.get("approved")
    records = integrations.get("admission_records")
    if not isinstance(allowed, list) or integration_id not in allowed:
        deny(f"External runtime invocation requires integrations.approved to contain {integration_id!r}.")
    if not isinstance(records, list) or not any(isinstance(v, str) and v.strip() for v in records):
        deny("External runtime invocation requires a concrete admission evidence path.")


def check_command(command: str, gate: dict, root: Path) -> None:
    for integration_id in runtime_invocations(command):
        require_integration(gate, integration_id)

    if recursive_rm(command):
        deny("Destructive recursive rm is outside the normal agent capability boundary.")
    if force_push(command):
        deny("Force push is outside the normal agent capability boundary.")
    if re.search(r"\bgit\s+push\b", command, re.I) and pushes_default_branch(command, root):
        deny("Direct protected/default-branch push is outside the normal agent capability boundary; use a pull request.")

    for pattern, label in CONSEQUENTIAL:
        if pattern.search(command):
            deny(f"{label} is outside the normal agent capability boundary; use an externally Owner-controlled channel.")


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
