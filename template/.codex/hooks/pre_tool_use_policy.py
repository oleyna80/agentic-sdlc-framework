#!/usr/bin/env python3
"""Fail-closed Codex PreToolUse guard for Work Block scope and Hard Stops.

The hook is a project guardrail, not an OS security boundary. It reads one Codex
hook event from stdin and returns the official PreToolUse decision shape.
"""

from __future__ import annotations

import fnmatch
import json
import os
import posixpath
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

DEFAULT_COORDINATION_WRITE_SET = [
    ".agent/active-work-block.json",
    ".agent/critic-gate.md",
    ".agent/verification-gate.md",
    ".codex/write-gate.md",
    "docs/architecture/drafts/**",
    "docs/specs/**",
    "docs/plans/**",
    "docs/tasklist/**",
    "docs/reports/**",
    "memory_bank/**",
]

READ_ONLY_BASH = re.compile(
    r"^\s*(?:"
    r"pwd|ls(?:\s|$)|find(?:\s|$)|rg(?:\s|$)|grep(?:\s|$)|cat(?:\s|$)|"
    r"head(?:\s|$)|tail(?:\s|$)|wc(?:\s|$)|stat(?:\s|$)|file(?:\s|$)|"
    r"sed\s+-n(?:\s|$)|"
    r"git\s+(?:status|diff|show|log|grep|rev-parse|branch\s+--show-current)(?:\s|$)|"
    r"pytest(?:\s|$)|python(?:3)?\s+-m\s+(?:pytest|compileall)(?:\s|$)|"
    r"npm\s+(?:test|run\s+(?:test|lint|build|typecheck))(?:\s|$)|"
    r"npx\s+(?:tsc|vitest|eslint)(?:\s|$)|"
    r"bash\s+scripts/(?:test|validate)[^\s]*(?:\s|$)"
    r")",
    re.IGNORECASE,
)

OPAQUE_MUTATION = re.compile(
    r"(?:^|[;&|]\s*)(?:touch|mkdir|cp|mv|rm|install|ln|truncate|chmod|chown)\b|"
    r"\bsed\s+-i\b|\bperl\s+-pi\b|\btee\b|(?:^|[^<])>{1,2}\s*[^&]|"
    r"\bnpm\s+(?:install|ci|publish)\b|\bpnpm\s+(?:install|publish)\b|"
    r"\byarn\s+(?:install|publish)\b|\bpip\s+install\b",
    re.IGNORECASE,
)

DANGEROUS_RULES: list[tuple[str, re.Pattern[str], str]] = [
    ("git commit", re.compile(r"\bgit\s+commit\b", re.I), "git_commit"),
    ("git push", re.compile(r"\bgit\s+push\b", re.I), "git_push"),
    (
        "default branch push",
        re.compile(r"\bgit\s+push\b[^\n]*(?:\bmain\b|\bmaster\b)", re.I),
        "default_branch_push",
    ),
    (
        "destructive operation",
        re.compile(
            r"\bgit\s+reset\s+--hard\b|\bgit\s+clean\s+-[^\s]*f|"
            r"\brm\s+-[^\s]*r[^\s]*f|\bmkfs\b|\bdrop\s+(?:database|table)\b",
            re.I,
        ),
        "destructive",
    ),
    (
        "live infrastructure operation",
        re.compile(
            r"\bdocker\s+push\b|\bkubectl\s+(?:apply|delete|rollout|scale)\b|"
            r"\bterraform\s+(?:apply|destroy)\b|\bsystemctl\s+(?:restart|stop|start)\b|"
            r"\bservice\s+\S+\s+(?:restart|stop|start)\b|\bscp\b|\bssh\b",
            re.I,
        ),
        "live_infra",
    ),
    (
        "live data operation",
        re.compile(
            r"\bprisma\s+migrate\s+deploy\b|\bsequelize\s+db:migrate\b|"
            r"\b(?:psql|mysql|mongosh)\b[^\n]*(?:insert|update|delete|alter|drop|create)\b",
            re.I,
        ),
        "live_data",
    ),
    (
        "credential or secret operation",
        re.compile(
            r"\bgh\s+secret\s+(?:set|delete)\b|\bkubectl\s+create\s+secret\b|"
            r"\b(?:export|set)\s+[A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|API_KEY)\s*=",
            re.I,
        ),
        "credentials",
    ),
    (
        "client communication",
        re.compile(r"\b(?:sendmail|mailx|twilio|postmark|resend)\b", re.I),
        "client_communications",
    ),
]


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


def allow(additional_context: str | None = None) -> int:
    if additional_context:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "additionalContext": additional_context,
                    }
                }
            )
        )
    return 0


def find_repo_root(cwd: Path) -> Path:
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
            if (candidate / ".git").exists() or (candidate / ".agent").exists():
                return candidate
        return current


def load_gate(root: Path) -> tuple[dict[str, Any] | None, str | None]:
    path = root / ".agent" / "active-work-block.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, f"Missing machine-readable Work Block gate: {path}"
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"Invalid machine-readable Work Block gate: {exc}"
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return None, "Unsupported or invalid active Work Block gate schema."
    return data, None


def normalize_path(raw: str) -> str | None:
    value = raw.strip().strip('"\'').replace("\\", "/")
    if value.startswith("a/") or value.startswith("b/"):
        value = value[2:]
    while value.startswith("./"):
        value = value[2:]
    if not value or value == "/dev/null" or value.startswith("/"):
        return None
    normalized = posixpath.normpath(value)
    if normalized in (".", "..") or normalized.startswith("../"):
        return None
    return normalized


def parse_patch_targets(command: str) -> list[str]:
    targets: list[str] = []
    patterns = [
        re.compile(r"^\*\*\* (?:Add|Update|Delete|Move to) File:\s*(.+?)\s*$"),
        re.compile(r"^\+\+\+\s+(?:b/)?(.+?)\s*$"),
    ]
    for line in command.splitlines():
        for pattern in patterns:
            match = pattern.match(line)
            if not match:
                continue
            path = normalize_path(match.group(1))
            if path and path not in targets:
                targets.append(path)
            break
    return targets


def path_matches(path: str, patterns: Iterable[str]) -> bool:
    for raw_pattern in patterns:
        if not isinstance(raw_pattern, str):
            continue
        pattern = raw_pattern.strip().replace("\\", "/")
        while pattern.startswith("./"):
            pattern = pattern[2:]
        if not pattern:
            continue
        if pattern.endswith("/**"):
            prefix = pattern[:-3].rstrip("/")
            if path == prefix or path.startswith(prefix + "/"):
                return True
        if fnmatch.fnmatchcase(path, pattern):
            return True
    return False


def gate_ready(gate: dict[str, Any], root: Path) -> tuple[bool, str]:
    work_block_id = str(gate.get("work_block_id") or "").strip()
    if not work_block_id or work_block_id.upper() == "TBD":
        return False, "Work Block ID is missing."

    spec = gate.get("specification")
    if not isinstance(spec, dict):
        return False, "Specification metadata is missing."
    if not str(spec.get("path") or "").strip() or not str(spec.get("revision") or "").strip():
        return False, "Specification path and revision must be recorded before source writes."

    write_gate = gate.get("write_gate")
    if not isinstance(write_gate, dict) or str(write_gate.get("status") or "").upper() != "READY":
        return False, "Write gate is not READY."

    expires_at = write_gate.get("expires_at")
    if not isinstance(expires_at, str) or not expires_at.strip():
        return False, "Write gate expiry is missing."
    try:
        expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
    except ValueError:
        return False, "Write gate expiry is invalid."
    if expiry <= datetime.now(timezone.utc):
        return False, "Write gate has expired."

    critic = gate.get("critic")
    if not isinstance(critic, dict):
        return False, "Critic state is missing."
    if bool(critic.get("required", True)):
        status = str(critic.get("status") or "").upper()
        verdict = str(critic.get("verdict") or "").upper()
        if status in {"READY", "FALLBACK"} and verdict in {"APPROVE", "SUPPLEMENT"}:
            pass
        elif status == "SKIPPED" and str(critic.get("skip_reason") or "").strip():
            pass
        else:
            return False, "Required Critic state is unresolved or blocking."

    write_set = gate.get("write_set")
    if not isinstance(write_set, list) or not any(isinstance(item, str) and item.strip() for item in write_set):
        return False, "Approved write-set is empty."

    base_commit = str(gate.get("base_commit") or "").strip()
    if base_commit:
        try:
            result = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
                timeout=3,
            )
            if result.stdout.strip() != base_commit:
                return False, "Repository HEAD no longer matches the Work Block base commit."
        except (OSError, subprocess.SubprocessError):
            return False, "Unable to verify the Work Block base commit."

    return True, "READY"


def check_patch(command: str, gate: dict[str, Any] | None, gate_error: str | None, root: Path) -> int:
    targets = parse_patch_targets(command)
    if not targets:
        return deny("Unable to determine apply_patch target paths; use an explicit standard patch.")

    coordination = DEFAULT_COORDINATION_WRITE_SET
    if gate and isinstance(gate.get("coordination_write_set"), list):
        coordination = list(gate["coordination_write_set"])

    source_targets = [path for path in targets if not path_matches(path, coordination)]
    if not source_targets:
        return allow("Coordination-only patch allowed while the source gate remains independent.")

    if gate is None:
        return deny(gate_error or "Active Work Block gate is unavailable.")
    ready, reason = gate_ready(gate, root)
    if not ready:
        return deny(reason)

    write_set = gate.get("write_set", [])
    outside = [path for path in source_targets if not path_matches(path, write_set)]
    if outside:
        return deny("Patch targets outside the approved write-set: " + ", ".join(outside))
    return allow()


def hard_stop_approval(gate: dict[str, Any] | None, key: str) -> bool:
    approvals = gate.get("hard_stop_approvals") if isinstance(gate, dict) else None
    return bool(isinstance(approvals, dict) and approvals.get(key) is True)


def check_bash(command: str, gate: dict[str, Any] | None, gate_error: str | None, root: Path) -> int:
    stripped = command.strip()
    if not stripped:
        return allow()
    if READ_ONLY_BASH.match(stripped) and not OPAQUE_MUTATION.search(stripped):
        return allow()

    matched_rules: list[tuple[str, str]] = []
    for label, pattern, approval_key in DANGEROUS_RULES:
        if pattern.search(stripped):
            matched_rules.append((label, approval_key))
    for label, approval_key in matched_rules:
        if not hard_stop_approval(gate, approval_key):
            return deny(f"{label} requires explicit Owner approval recorded as {approval_key}.")

    if matched_rules:
        if gate is None:
            return deny(gate_error or "Active Work Block gate is unavailable.")
        ready, reason = gate_ready(gate, root)
        return allow() if ready else deny(reason)

    if re.match(r"^\s*git\s+add\b", stripped, re.I):
        if gate is None:
            return deny(gate_error or "Active Work Block gate is unavailable.")
        ready, reason = gate_ready(gate, root)
        if not ready:
            return deny(reason)
        try:
            tokens = shlex.split(stripped)
        except ValueError:
            return deny("Unable to parse git add command safely.")
        paths = [normalize_path(token) for token in tokens[2:] if not token.startswith("-")]
        paths = [path for path in paths if path]
        if not paths:
            return deny("Use explicit scoped paths with git add; broad staging is blocked.")
        outside = [path for path in paths if not path_matches(path, gate.get("write_set", []))]
        if outside:
            return deny("git add targets outside the approved write-set: " + ", ".join(outside))
        return allow()

    if OPAQUE_MUTATION.search(stripped):
        return deny(
            "Opaque mutating Bash is blocked because target scope cannot be verified. "
            "Use apply_patch or a simpler explicit command covered by the Work Block gate."
        )

    # Unknown commands are allowed only when they are not recognized as writes or Hard Stops.
    # Hooks are guardrails, so sandbox/approval policy still applies independently.
    return allow()


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"Invalid hook input: {exc}", file=sys.stderr)
        return 2
    if not isinstance(event, dict):
        print("Invalid hook input: expected object", file=sys.stderr)
        return 2

    cwd = Path(str(event.get("cwd") or os.getcwd()))
    root = find_repo_root(cwd)
    gate, gate_error = load_gate(root)
    tool_name = str(event.get("tool_name") or "")
    tool_input = event.get("tool_input")
    command = str(tool_input.get("command") or "") if isinstance(tool_input, dict) else ""

    if tool_name in {"apply_patch", "Edit", "Write"}:
        return check_patch(command, gate, gate_error, root)
    if tool_name == "Bash":
        return check_bash(command, gate, gate_error, root)
    return allow()


if __name__ == "__main__":
    raise SystemExit(main())
