#!/usr/bin/env python3
"""Fixture-test the project-scoped Codex agents, hooks, and Work Block gate."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import tomllib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "template"
PRE_TOOL = TEMPLATE / ".codex" / "hooks" / "pre_tool_use_policy.py"
SUBAGENT = TEMPLATE / ".codex" / "hooks" / "subagent_context.py"
AGENT_DIR = TEMPLATE / ".codex" / "agents"


def fail(message: str) -> None:
    raise AssertionError(message)


def syntax_check(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    compile(source, str(path), "exec")


def run_hook(script: Path, cwd: Path, event: dict[str, Any]) -> tuple[int, dict[str, Any] | None, str]:
    result = subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(event),
        text=True,
        capture_output=True,
        cwd=cwd,
        timeout=10,
        env={**dict(__import__("os").environ), "PYTHONDONTWRITEBYTECODE": "1"},
    )
    output = result.stdout.strip()
    parsed = json.loads(output) if output else None
    return result.returncode, parsed, result.stderr.strip()


def decision(payload: dict[str, Any] | None) -> str:
    if not payload:
        return "allow"
    specific = payload.get("hookSpecificOutput")
    return str(specific.get("permissionDecision") or "allow") if isinstance(specific, dict) else "unknown"


def reason(payload: dict[str, Any] | None) -> str:
    if not payload:
        return ""
    specific = payload.get("hookSpecificOutput")
    return str(specific.get("permissionDecisionReason") or "") if isinstance(specific, dict) else ""


def assert_allowed(label: str, result: tuple[int, dict[str, Any] | None, str]) -> None:
    code, payload, stderr = result
    if code != 0 or decision(payload) == "deny":
        fail(f"{label}: expected allow, code={code}, payload={payload}, stderr={stderr}")


def assert_denied(label: str, result: tuple[int, dict[str, Any] | None, str], contains: str = "") -> None:
    code, payload, stderr = result
    if code != 0 or decision(payload) != "deny":
        fail(f"{label}: expected deny, code={code}, payload={payload}, stderr={stderr}")
    if contains and contains.lower() not in reason(payload).lower():
        fail(f"{label}: denial reason did not contain {contains!r}: {reason(payload)!r}")


def future_iso(hours: int = 2) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


def ready_gate() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "work_block_id": "wb-fixture",
        "governance_profile": "Assured",
        "specification": {"path": "docs/specs/fixture.md", "revision": "spec-fixture-v1"},
        "base_commit": "",
        "write_gate": {
            "status": "READY",
            "opened_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": future_iso(),
        },
        "critic": {
            "required": True,
            "status": "READY",
            "verdict": "APPROVE",
            "report": "docs/reports/critic-wb-fixture.md",
            "skip_reason": "",
        },
        "write_set": ["src/**", "tests/**"],
        "coordination_write_set": [
            ".agent/**",
            ".codex/write-gate.md",
            "docs/specs/**",
            "docs/plans/**",
            "docs/reports/**",
            "memory_bank/**",
        ],
        "hard_stop_approvals": {
            "git_commit": False,
            "git_push": False,
            "default_branch_push": False,
            "destructive": False,
            "live_infra": False,
            "live_data": False,
            "credentials": False,
            "client_communications": False,
        },
    }


def write_gate(root: Path, gate: dict[str, Any]) -> None:
    path = root / ".agent" / "active-work-block.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(gate, indent=2), encoding="utf-8")


def event(tool_name: str, command: str, cwd: Path) -> dict[str, Any]:
    return {
        "session_id": "fixture-session",
        "turn_id": "fixture-turn",
        "cwd": str(cwd),
        "hook_event_name": "PreToolUse",
        "permission_mode": "default",
        "tool_name": tool_name,
        "tool_use_id": "fixture-tool",
        "tool_input": {"command": command},
    }


def patch(path: str) -> str:
    return "\n".join(
        ["*** Begin Patch", f"*** Update File: {path}", "@@", "-old", "+new", "*** End Patch"]
    )


def validate_static_files() -> None:
    for script in (PRE_TOOL, SUBAGENT):
        if not script.is_file():
            fail(f"missing hook script: {script}")
        syntax_check(script)

    hooks = json.loads((TEMPLATE / ".codex" / "hooks.json").read_text(encoding="utf-8"))
    if set(hooks.get("hooks", {})) != {"PreToolUse", "SubagentStart"}:
        fail("hooks.json must register exactly PreToolUse and SubagentStart")

    config = tomllib.loads((TEMPLATE / ".codex" / "config.toml.template").read_text(encoding="utf-8"))
    if config.get("agents", {}).get("enabled") is not True:
        fail("Codex [agents].enabled must be true")
    if "multi_agent" in config:
        fail("legacy top-level multi_agent must not be present")

    expected = {"architect", "critic", "coder", "reviewer", "verifier"}
    actual: set[str] = set()
    for path in sorted(AGENT_DIR.glob("*.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        for key in ("name", "description", "developer_instructions"):
            if not str(data.get(key) or "").strip():
                fail(f"{path} missing required key {key}")
        actual.add(str(data["name"]))
        expected_sandbox = "workspace-write" if data["name"] == "coder" else "read-only"
        if data.get("sandbox_mode") != expected_sandbox:
            fail(f"{data['name']} must default to {expected_sandbox}")
    if actual != expected:
        fail(f"custom agent set mismatch: expected={sorted(expected)} actual={sorted(actual)}")

    gate = json.loads((TEMPLATE / ".agent" / "active-work-block.json").read_text(encoding="utf-8"))
    if gate.get("schema_version") != 1 or gate.get("write_gate", {}).get("status") != "BLOCKED":
        fail("default active Work Block gate must be schema v1 and BLOCKED")


def validate_pre_tool_fixtures() -> None:
    with tempfile.TemporaryDirectory(prefix="codex-adapter-") as tmp:
        root = Path(tmp)
        (root / ".git").mkdir()
        gate = ready_gate()
        write_gate(root, gate)

        assert_allowed("read-only Bash", run_hook(PRE_TOOL, root, event("Bash", "git status --short", root)))
        assert_allowed("in-scope patch", run_hook(PRE_TOOL, root, event("apply_patch", patch("src/app.py"), root)))
        assert_denied("out-of-scope patch", run_hook(PRE_TOOL, root, event("apply_patch", patch("config/prod.yml"), root)), "outside")
        assert_allowed("explicit scoped git add", run_hook(PRE_TOOL, root, event("Bash", "git add src/app.py", root)))
        assert_denied("broad git add", run_hook(PRE_TOOL, root, event("Bash", "git add -A", root)), "explicit")
        assert_denied("opaque mutation", run_hook(PRE_TOOL, root, event("Bash", "mkdir -p src/new", root)), "opaque")
        assert_denied("git push hard stop", run_hook(PRE_TOOL, root, event("Bash", "git push origin feature", root)), "git_push")
        assert_denied("destructive hard stop", run_hook(PRE_TOOL, root, event("Bash", "rm -rf src", root)), "destructive")

        approved = copy.deepcopy(gate)
        approved["hard_stop_approvals"]["git_push"] = True
        write_gate(root, approved)
        assert_allowed("approved feature push", run_hook(PRE_TOOL, root, event("Bash", "git push origin feature", root)))

        blocked = copy.deepcopy(gate)
        blocked["write_gate"]["status"] = "BLOCKED"
        write_gate(root, blocked)
        assert_denied("blocked source patch", run_hook(PRE_TOOL, root, event("apply_patch", patch("src/app.py"), root)), "not READY")
        assert_allowed("blocked coordination patch", run_hook(PRE_TOOL, root, event("apply_patch", patch("docs/specs/fixture.md"), root)))

        expired = copy.deepcopy(gate)
        expired["write_gate"]["expires_at"] = (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()
        write_gate(root, expired)
        assert_denied("expired gate", run_hook(PRE_TOOL, root, event("apply_patch", patch("src/app.py"), root)), "expired")

        missing_spec = copy.deepcopy(gate)
        missing_spec["specification"]["revision"] = ""
        write_gate(root, missing_spec)
        assert_denied("missing specification", run_hook(PRE_TOOL, root, event("apply_patch", patch("src/app.py"), root)), "Specification")

        unresolved_critic = copy.deepcopy(gate)
        unresolved_critic["critic"]["status"] = "PENDING"
        unresolved_critic["critic"]["verdict"] = "PENDING"
        write_gate(root, unresolved_critic)
        assert_denied("unresolved critic", run_hook(PRE_TOOL, root, event("apply_patch", patch("src/app.py"), root)), "Critic")


def validate_subagent_context() -> None:
    with tempfile.TemporaryDirectory(prefix="codex-subagent-") as tmp:
        root = Path(tmp)
        (root / ".git").mkdir()
        write_gate(root, ready_gate())
        start_event = {
            "session_id": "fixture-session",
            "turn_id": "fixture-turn",
            "cwd": str(root),
            "hook_event_name": "SubagentStart",
            "permission_mode": "default",
            "agent_id": "fixture-agent",
            "agent_type": "coder",
        }
        code, payload, stderr = run_hook(SUBAGENT, root, start_event)
        if code != 0 or not payload:
            fail(f"SubagentStart failed: code={code} payload={payload} stderr={stderr}")
        specific = payload.get("hookSpecificOutput", {})
        if specific.get("hookEventName") != "SubagentStart":
            fail("SubagentStart output has wrong event name")
        context = str(specific.get("additionalContext") or "")
        for expected in ("wb-fixture", "src/**", "Coder", "READY"):
            if expected.lower() not in context.lower():
                fail(f"SubagentStart context missing {expected!r}: {context}")


def main() -> int:
    syntax_check(Path(__file__))
    validate_static_files()
    validate_pre_tool_fixtures()
    validate_subagent_context()
    print("OK: Codex adapter agents, hooks, and Work Block gate fixtures passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
