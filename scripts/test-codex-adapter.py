#!/usr/bin/env python3
"""Contract and safe fixture tests for the project-scoped Codex adapter."""
from __future__ import annotations

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
        list(args),
        cwd=cwd,
        input=json.dumps(payload) if payload is not None else None,
        text=True,
        capture_output=True,
        check=False,
        timeout=15,
    )


def git(cwd: Path, *args: str) -> str:
    result = run("git", *args, cwd=cwd)
    if result.returncode:
        fail(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout.strip()


def decision(script: Path, cwd: Path, payload: dict) -> tuple[bool, str, dict | None]:
    result = run(sys.executable, str(script), cwd=cwd, payload=payload)
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


def event(cwd: Path, tool: str, command: str | None = None, **tool_input: str) -> dict:
    value = dict(tool_input)
    if command is not None:
        value["command"] = command
    return {
        "session_id": "fixture-session",
        "turn_id": "fixture-turn",
        "cwd": str(cwd),
        "hook_event_name": "PreToolUse",
        "permission_mode": "default",
        "model": "fixture-model",
        "tool_name": tool,
        "tool_use_id": "fixture-tool",
        "tool_input": value,
    }


def patch(path: str) -> str:
    return "\n".join(
        [
            "*** Begin Patch",
            f"*** Update File: {path}",
            "@@",
            "-old",
            "+new",
            "*** End Patch",
        ]
    )


def move_patch(source: str, destination: str) -> str:
    return "\n".join(
        [
            "*** Begin Patch",
            f"*** Update File: {source}",
            f"*** Move to: {destination}",
            "@@",
            "-old",
            "+new",
            "*** End Patch",
        ]
    )


def write_gate(repo: Path, *, status: str = "READY") -> None:
    gate = {
        "schema_version": 3,
        "authority_mode": "github_capability",
        "work_block_id": "wb-fixture" if status == "READY" else "",
        "governance_profile": "Managed",
        "specification": {
            "path": "docs/specs/fixture.md" if status == "READY" else "",
            "revision": "v1" if status == "READY" else "",
        },
        "base_commit": "",
        "write_gate": {"status": status, "opened_at": "fixture" if status == "READY" else None},
        "critic": {
            "required": True,
            "status": "READY" if status == "READY" else "PENDING",
            "verdict": "APPROVE" if status == "READY" else "PENDING",
            "report": "docs/reports/critic-fixture.md" if status == "READY" else "",
            "isolation": "separate_subagent" if status == "READY" else "unknown",
            "skip_reason": "",
        },
        "write_set": ["src/**", "tests/**"] if status == "READY" else [],
        "coordination_write_set": [
            ".agent/active-work-block.json",
            ".agent/critic-gate.md",
            ".agent/verification-gate.md",
            ".codex/write-gate.md",
            "docs/plans/**",
            "docs/specs/**",
            "docs/tasklist/**",
            "docs/reports/**",
            "docs/architecture/drafts/**",
            "memory_bank/**",
        ],
        "external_hard_stops": [
            "protected_default_branch_mutation",
            "destructive",
            "live_infra",
            "live_data",
            "credentials",
            "client_communications",
            "irreversible_publish",
        ],
        "integrations": {"approved": [], "admission_records": []},
        "assurance": {},
        "closeout_mode": "pending",
    }
    (repo / ".agent/active-work-block.json").write_text(
        json.dumps(gate, indent=2) + "\n", encoding="utf-8"
    )


def assert_allowed(label: str, value: tuple[bool, str, dict | None]) -> None:
    denied, reason, _ = value
    if denied:
        fail(f"{label}: unexpectedly denied: {reason}")


def assert_denied(label: str, value: tuple[bool, str, dict | None], contains: str) -> None:
    denied, reason, _ = value
    if not denied or contains.lower() not in reason.lower():
        fail(f"{label}: expected denial containing {contains!r}, got {reason!r}")


def static_contracts() -> None:
    config = tomllib.loads(
        (TEMPLATE / ".codex/config.toml.template").read_text(encoding="utf-8")
    )
    if config.get("agents", {}).get("enabled") is not True:
        fail("[agents].enabled must be true")
    if config.get("features", {}).get("hooks") is not True:
        fail("hooks feature is not enabled")

    for name in AGENTS:
        path = TEMPLATE / f".codex/agents/{name}.toml"
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        expected = "workspace-write" if name == "coder" else "read-only"
        if data.get("sandbox_mode") != expected:
            fail(f"{path} sandbox must be {expected}")
        if "model" in data:
            fail(f"{path} must not pin a concrete model")

    hooks = json.loads((TEMPLATE / ".codex/hooks.json").read_text(encoding="utf-8"))
    text = json.dumps(hooks, sort_keys=True)
    for required in ("hard_stop_policy.py", "pre_tool_use_policy.py", "subagent_context.py"):
        if required not in text:
            fail(f"Codex hook wiring missing {required}")

    gate = json.loads(
        (TEMPLATE / ".agent/active-work-block.json").read_text(encoding="utf-8")
    )
    if gate.get("schema_version") != 3:
        fail("gate schema must be version 3")
    if gate.get("authority_mode") != "github_capability":
        fail("gate authority_mode must be github_capability")
    if "authorization" in gate or "hard_stop_approvals" in gate:
        fail("legacy signed authority fields remain in schema v3")
    if gate.get("write_gate") != {"status": "BLOCKED", "opened_at": None}:
        fail("generated gate must start BLOCKED")

    lifecycle = (TEMPLATE / ".codex/scripts/lifecycle.py").read_text(encoding="utf-8")
    doctor = (TEMPLATE / ".codex/scripts/doctor.py").read_text(encoding="utf-8")
    for legacy in ("ssh-keygen", "AGENTIC_SDLC_OWNER_SIGNERS", "allowed_signers"):
        if legacy in lifecycle or legacy in doctor:
            fail(f"legacy signing dependency remains in normal Codex control plane: {legacy}")


def hook_fixtures() -> None:
    with tempfile.TemporaryDirectory(prefix="codex-adapter-v3-") as tmp:
        repo = Path(tmp) / "repo"
        for path in (
            ".agent",
            "src",
            "tests",
            "docs/plans",
            "docs/specs",
            "docs/reports",
        ):
            (repo / path).mkdir(parents=True, exist_ok=True)
        (repo / "src/app.py").write_text("old\n", encoding="utf-8")
        (repo / "README.md").write_text("fixture\n", encoding="utf-8")
        (repo / "docs/specs/fixture.md").write_text("spec\n", encoding="utf-8")
        git(repo, "init", "-q", "-b", "feature")
        git(repo, "config", "user.email", "fixture@example.com")
        git(repo, "config", "user.name", "Fixture")
        write_gate(repo, status="BLOCKED")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "baseline")
        write_gate(repo, status="BLOCKED")

        assert_allowed(
            "read-only command",
            decision(PRE_TOOL, repo, event(repo, "Bash", "git status --short")),
        )
        assert_allowed(
            "coordination patch while blocked",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("docs/plans/wb.md"))),
        )
        assert_denied(
            "source patch while blocked",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("src/app.py"))),
            "READY",
        )

        # Coordination-only governance commits must remain possible while source
        # is BLOCKED; otherwise the local process recreates a bootstrap deadlock.
        coordination_file = repo / "docs/plans/wb.md"
        coordination_file.write_text("# Work Block\n", encoding="utf-8")
        git(repo, "add", "docs/plans/wb.md")
        assert_allowed(
            "coordination-only commit while blocked",
            decision(PRE_TOOL, repo, event(repo, "Bash", "git commit -m governance")),
        )
        git(repo, "reset", "-q", "HEAD", "--", "docs/plans/wb.md")
        coordination_file.unlink()

        write_gate(repo)
        assert_allowed(
            "in-scope patch",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("src/app.py"))),
        )
        assert_allowed(
            "in-scope Edit",
            decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
        )
        assert_allowed(
            "in-scope Write",
            decision(PRE_TOOL, repo, event(repo, "Write", path="tests/new_test.py")),
        )
        assert_denied(
            "out-of-scope patch",
            decision(PRE_TOOL, repo, event(repo, "apply_patch", patch("README.md"))),
            "outside approved scope",
        )
        assert_denied(
            "move destination outside write-set",
            decision(
                PRE_TOOL,
                repo,
                event(repo, "apply_patch", move_patch("src/app.py", "README.md")),
            ),
            "README.md",
        )
        assert_denied(
            "absolute outside repository",
            decision(PRE_TOOL, repo, event(repo, "Write", file_path="/tmp/evil.txt")),
            "outside repository",
        )
        assert_allowed(
            "simple in-scope bash write",
            decision(PRE_TOOL, repo, event(repo, "Bash", "touch src/new.py")),
        )
        assert_denied(
            "simple out-of-scope bash write",
            decision(PRE_TOOL, repo, event(repo, "Bash", "touch README.md")),
            "outside approved scope",
        )
        assert_denied(
            "complex mutating bash fails closed",
            decision(
                PRE_TOOL,
                repo,
                event(repo, "Bash", "touch src/a.py && touch README.md"),
            ),
            "Complex mutating Bash",
        )
        assert_allowed(
            "feature push passes scope guard",
            decision(PRE_TOOL, repo, event(repo, "Bash", "git push origin feature")),
        )

        (repo / "src/app.py").write_text("new\n", encoding="utf-8")
        git(repo, "add", "src/app.py")
        assert_allowed(
            "in-scope staged commit",
            decision(PRE_TOOL, repo, event(repo, "Bash", "git commit -m scoped")),
        )
        git(repo, "reset", "-q", "HEAD", "--", "src/app.py")
        (repo / "README.md").write_text("changed\n", encoding="utf-8")
        git(repo, "add", "README.md")
        assert_denied(
            "out-of-scope staged commit",
            decision(PRE_TOOL, repo, event(repo, "Bash", "git commit -m bad")),
            "Staged commit outside approved scope",
        )

        gate_path = repo / ".agent/active-work-block.json"
        gate = json.loads(gate_path.read_text(encoding="utf-8"))
        gate["schema_version"] = 2
        gate_path.write_text(json.dumps(gate), encoding="utf-8")
        assert_denied(
            "legacy schema source write",
            decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
            "schema_version=3",
        )
        write_gate(repo)
        gate = json.loads(gate_path.read_text(encoding="utf-8"))
        gate["critic"]["status"] = "PENDING"
        gate["critic"]["verdict"] = "PENDING"
        gate_path.write_text(json.dumps(gate), encoding="utf-8")
        assert_denied(
            "unresolved Critic",
            decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
            "Critic",
        )

        write_gate(repo)
        subagent_event = {
            "cwd": str(repo),
            "agent_type": "coder",
            "permission_mode": "default",
        }
        result = run(
            sys.executable,
            str(SUBAGENT),
            cwd=repo,
            payload=subagent_event,
        )
        if result.returncode:
            fail(result.stderr)
        context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
        if "github_capability" not in context or "External Hard Stops" not in context:
            fail("schema v3 capability context missing from SubagentStart")


def main() -> int:
    static_contracts()
    hook_fixtures()
    print("Codex adapter schema v3 fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
