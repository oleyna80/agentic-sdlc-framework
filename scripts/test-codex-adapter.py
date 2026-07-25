#!/usr/bin/env python3
"""Contract and safe fixture tests for the project-scoped Codex adapter."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "template"
PRE_TOOL = TEMPLATE / ".codex/hooks/pre_tool_use_policy.py"
SUBAGENT = TEMPLATE / ".codex/hooks/subagent_context.py"
AGENTS = ("architect", "critic", "coder", "reviewer", "verifier")


def fail(message: str) -> None:
    raise AssertionError(message)


def run(*args: str, cwd: Path, payload: dict | None = None):
    return subprocess.run(
        list(args), cwd=cwd,
        input=json.dumps(payload) if payload is not None else None,
        text=True, capture_output=True, check=False, timeout=15,
    )


def git(cwd: Path, *args: str) -> str:
    result = run("git", *args, cwd=cwd)
    if result.returncode:
        fail(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout.strip()


def decision(script: Path, cwd: Path, event: dict) -> tuple[bool, str, dict | None]:
    result = run(sys.executable, str(script), cwd=cwd, payload=event)
    if result.returncode:
        fail(f"hook failed: {result.stderr}")
    if not result.stdout.strip():
        return False, "", None
    output = json.loads(result.stdout)
    specific = output.get("hookSpecificOutput", {})
    return (
        specific.get("permissionDecision") == "deny",
        str(specific.get("permissionDecisionReason") or ""),
        output,
    )


def event(cwd: Path, tool: str, command: str) -> dict:
    return {
        "session_id": "fixture-session",
        "turn_id": "fixture-turn",
        "cwd": str(cwd),
        "hook_event_name": "PreToolUse",
        "permission_mode": "default",
        "model": "fixture-model",
        "tool_name": tool,
        "tool_use_id": "fixture-tool",
        "tool_input": {"command": command},
    }


def patch(path: str) -> str:
    return "\n".join([
        "*** Begin Patch", f"*** Update File: {path}", "@@",
        "-old", "+new", "*** End Patch",
    ])


def write_gate(
    repo: Path, *, status: str = "READY", base: str | None = None,
    expires: str | None = None, critic_status: str = "READY",
    critic_verdict: str = "APPROVE",
) -> None:
    if base is None:
        base = git(repo, "rev-parse", "HEAD")
    if expires is None:
        expires = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=2)).isoformat()
    gate = {
        "schema_version": 1,
        "work_block_id": "wb-fixture",
        "governance_profile": "Managed",
        "specification": {"path": "docs/specs/fixture.md", "revision": "v1"},
        "base_commit": base,
        "write_gate": {
            "status": status,
            "opened_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "expires_at": expires,
        },
        "critic": {
            "required": True, "status": critic_status,
            "verdict": critic_verdict,
            "report": "docs/reports/critic-fixture.md", "skip_reason": "",
        },
        "write_set": ["src/**", "tests/**"],
        "coordination_write_set": [
            ".agent/active-work-block.json", ".agent/critic-gate.md",
            ".agent/verification-gate.md", ".codex/write-gate.md",
            "docs/plans/**", "docs/specs/**", "docs/tasklist/**",
            "docs/reports/**", "docs/architecture/drafts/**", "memory_bank/**",
        ],
        "hard_stop_approvals": {
            "git_commit": False, "git_push": False,
            "default_branch_push": False, "destructive": False,
            "live_infra": False, "live_data": False,
            "credentials": False, "client_communications": False,
        },
    }
    (repo / ".agent/active-work-block.json").write_text(
        json.dumps(gate, indent=2) + "\n", encoding="utf-8"
    )


def assert_allowed(label: str, value: tuple[bool, str, dict | None]) -> None:
    denied, reason, _ = value
    if denied:
        fail(f"{label}: unexpectedly denied: {reason}")


def assert_denied(
    label: str, value: tuple[bool, str, dict | None], contains: str
) -> None:
    denied, reason, _ = value
    if not denied or contains.lower() not in reason.lower():
        fail(f"{label}: expected denial containing {contains!r}, got {reason!r}")


def static_contracts() -> None:
    config = tomllib.loads(
        (TEMPLATE / ".codex/config.toml.template").read_text(encoding="utf-8")
    )
    if "multi_agent" in config:
        fail("legacy multi_agent key remains")
    if config.get("agents", {}).get("enabled") is not True:
        fail("[agents].enabled must be true")
    if config.get("agents", {}).get("max_concurrent_threads_per_session") != 6:
        fail("bounded concurrent thread count is missing")
    if config.get("features", {}).get("hooks") is not True:
        fail("hooks feature is not enabled")

    for name in AGENTS:
        path = TEMPLATE / f".codex/agents/{name}.toml"
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        for key in ("name", "description", "developer_instructions"):
            if not str(data.get(key) or "").strip():
                fail(f"{path} missing {key}")
        if data["name"] != name:
            fail(f"{path} has wrong logical role")
        expected = "workspace-write" if name == "coder" else "read-only"
        if data.get("sandbox_mode") != expected:
            fail(f"{path} sandbox must be {expected}")
        if "model" in data:
            fail(f"{path} must not pin a concrete model")

    hooks = json.loads((TEMPLATE / ".codex/hooks.json").read_text(encoding="utf-8"))
    if not hooks.get("hooks", {}).get("PreToolUse"):
        fail("PreToolUse hook missing")
    if not hooks.get("hooks", {}).get("SubagentStart"):
        fail("SubagentStart hook missing")

    gate = json.loads(
        (TEMPLATE / ".agent/active-work-block.json").read_text(encoding="utf-8")
    )
    if gate.get("schema_version") != 1:
        fail("gate schema must be version 1")
    if gate.get("write_gate", {}).get("status") != "BLOCKED":
        fail("generated gate must start BLOCKED")


def hook_fixtures() -> None:
    with tempfile.TemporaryDirectory(prefix="codex-adapter-") as tmp:
        repo = Path(tmp)
        for path in (
            ".agent", "src", "tests", "docs/plans", "docs/specs", "docs/reports"
        ):
            (repo / path).mkdir(parents=True, exist_ok=True)
        (repo / "AGENTS.md").write_text("# Fixture\n", encoding="utf-8")
        (repo / "src/app.py").write_text("value = 1\n", encoding="utf-8")
        (repo / "README.md").write_text("fixture\n", encoding="utf-8")
        git(repo, "init", "-q", "-b", "feature")
        git(repo, "config", "user.email", "fixture@example.com")
        git(repo, "config", "user.name", "Fixture")
        write_gate(repo, status="BLOCKED", base="0000000")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "baseline")
        write_gate(repo, status="BLOCKED")

        assert_allowed(
            "read-only command",
            decision(PRE_TOOL, repo, event(repo, "Bash", "git status --short")),
        )
        assert_allowed(
            "coordination patch",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("docs/plans/wb.md"))),
        )
        assert_denied(
            "blocked source patch",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("src/app.py"))),
            "READY",
        )

        write_gate(repo)
        assert_allowed(
            "in-scope patch",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("src/app.py"))),
        )
        assert_denied(
            "out-of-scope patch",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("README.md"))),
            "outside approved scope",
        )

        write_gate(
            repo,
            expires=(dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=1)).isoformat(),
        )
        assert_denied(
            "expired gate",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("src/app.py"))),
            "expired",
        )

        write_gate(repo, base="deadbee")
        assert_denied(
            "stale gate",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("src/app.py"))),
            "stale gate",
        )

        write_gate(repo, critic_status="PENDING", critic_verdict="PENDING")
        assert_denied(
            "unresolved critic",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("src/app.py"))),
            "Critic",
        )

        write_gate(repo)
        start = {
            "session_id": "fixture-session", "turn_id": "fixture-turn",
            "cwd": str(repo), "hook_event_name": "SubagentStart",
            "permission_mode": "default", "model": "fixture-model",
            "agent_id": "fixture-agent", "agent_type": "coder",
        }
        result = run(sys.executable, str(SUBAGENT), cwd=repo, payload=start)
        if result.returncode:
            fail(f"SubagentStart failed: {result.stderr}")
        context = json.loads(result.stdout).get("hookSpecificOutput", {}).get(
            "additionalContext", ""
        )
        for expected in ("wb-fixture", "coder", "Approved write-set", "src/**"):
            if expected.lower() not in str(context).lower():
                fail(f"SubagentStart context missing {expected!r}")


def main() -> int:
    static_contracts()
    hook_fixtures()
    print("Codex adapter contracts and safe fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
