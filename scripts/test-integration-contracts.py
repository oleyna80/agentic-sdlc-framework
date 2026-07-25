#!/usr/bin/env python3
"""Static and executable fixtures for runtime/integration adapter contracts."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "template"


def fail(message: str) -> None:
    raise AssertionError(message)


def require(path: Path) -> None:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")


def load_json(path: Path) -> dict[str, Any]:
    require(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must parse to an object")
    return value


def frontmatter(path: Path) -> dict[str, Any]:
    require(path)
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        fail(f"{path.relative_to(ROOT)} has unterminated YAML frontmatter")
    value = yaml.safe_load(text[4:end])
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} frontmatter must be a mapping")
    return value


def static_contracts() -> None:
    required = [
        ROOT / "integrations/README.md",
        ROOT / "integrations/claude-code-codex-plugin/README.md",
        ROOT / "integrations/mcp/README.md",
        ROOT / "integrations/file-handoff/README.md",
        ROOT / "handoff/templates/runtime-task-template.md",
        TEMPLATE / "docs/templates/integration-admission-template.md",
        TEMPLATE / ".agent/hooks/hard_stop_policy.py",
        TEMPLATE / ".claude/hooks/work_block_gate.py",
        TEMPLATE / ".claude/hooks/assurance_gate.py",
        TEMPLATE / "opencode.json",
    ]
    for path in required:
        require(path)

    claude = load_json(TEMPLATE / ".claude/settings.json")
    forbidden_top_level = {"enabledMcpjsonServers", "permissions", "autoMode"}
    present = forbidden_top_level.intersection(claude)
    if present:
        fail(f"Claude settings pre-enable external integration state: {sorted(present)}")
    expected_agents = {
        "solution-architect",
        "critic",
        "reviewer",
        "scoped-coder",
        "verifier",
    }
    actual_agents = set((claude.get("agents") or {}).keys())
    if actual_agents != expected_agents:
        fail(f"Claude logical agent set mismatch: {sorted(actual_agents)}")
    serialized_claude = json.dumps(claude, sort_keys=True).lower()
    for stale in ("gpt-critic", "gpt-verifier", "codex-reviewer", "mcp__codex"):
        if stale in serialized_claude:
            fail(f"Claude settings retain provider-specific default: {stale}")
    hook_commands = json.dumps(claude.get("hooks") or {})
    for expected in (
        ".agent/hooks/hard_stop_policy.py",
        ".claude/hooks/work_block_gate.py",
        ".claude/hooks/assurance_gate.py",
    ):
        if expected not in hook_commands:
            fail(f"Claude settings missing hook: {expected}")

    mcp = load_json(TEMPLATE / ".mcp.json")
    if mcp != {"mcpServers": {}}:
        fail("generated .mcp.json must be an empty opt-in registry")

    opencode = load_json(TEMPLATE / "opencode.json")
    if opencode.get("mcp") != {} or opencode.get("plugin") != []:
        fail("OpenCode must not enable MCP servers or plugins by default")
    permissions = opencode.get("permission")
    if not isinstance(permissions, dict):
        fail("OpenCode permission object missing")
    if permissions.get("external_directory") != "deny":
        fail("OpenCode external_directory must be denied")
    if permissions.get("edit") != "ask":
        fail("OpenCode project edit permission must require ask")
    bash = permissions.get("bash")
    if not isinstance(bash, dict):
        fail("OpenCode Bash permission map missing")
    for pattern in ("git commit*", "git push*", "git reset --hard*", "git clean*", "rm *"):
        if bash.get(pattern) != "deny":
            fail(f"OpenCode Bash permission must deny {pattern!r}")
    if opencode.get("model") or opencode.get("provider"):
        fail("public OpenCode baseline must not pin provider/model routing")

    for role in ("architect", "critic", "coder", "reviewer", "verifier"):
        data = frontmatter(TEMPLATE / f".opencode/agents/{role}.md")
        if data.get("mode") != "subagent":
            fail(f"OpenCode {role} must use mode: subagent")
        agent_permissions = data.get("permission")
        if not isinstance(agent_permissions, dict):
            fail(f"OpenCode {role} permission map missing")
        expected_edit = "ask" if role == "coder" else "deny"
        if agent_permissions.get("edit") != expected_edit:
            fail(f"OpenCode {role} edit permission must be {expected_edit}")
        if agent_permissions.get("task") != "deny":
            fail(f"OpenCode {role} nested task delegation must be denied")
        if agent_permissions.get("external_directory") != "deny":
            fail(f"OpenCode {role} external_directory must be denied")
        if data.get("model"):
            fail(f"OpenCode {role} must not pin a public model")

    removed = [
        TEMPLATE / ".claude/agents/gpt-critic.md",
        TEMPLATE / ".claude/agents/gpt-verifier.md",
        TEMPLATE / ".claude/agents/codex-reviewer.md",
        TEMPLATE / ".claude/agent-memory/gpt-critic/MEMORY.md",
        TEMPLATE / ".claude/agent-memory/gpt-verifier/MEMORY.md",
        TEMPLATE / ".claude/agent-memory/codex-reviewer/MEMORY.md",
    ]
    for path in removed:
        if path.exists():
            fail(f"provider-named compatibility path remains: {path.relative_to(ROOT)}")

    gate = load_json(TEMPLATE / ".agent/active-work-block.json")
    if gate.get("schema_version") != 1:
        fail("active Work Block schema_version must remain 1")
    integrations = gate.get("integrations")
    if integrations != {"approved": [], "admission_records": []}:
        fail("generated Work Block integration approvals must start empty")
    assurance = gate.get("assurance")
    if not isinstance(assurance, dict) or set(assurance) != {
        "review",
        "verification",
        "drift",
    }:
        fail("active Work Block assurance functions missing")
    if gate.get("closeout_mode") != "pending":
        fail("generated closeout_mode must start pending")

    claude_entry = (TEMPLATE / "CLAUDE.md").read_text(encoding="utf-8")
    for stale in ("gpt-critic", "gpt-verifier", "codex-reviewer"):
        if stale in claude_entry.lower():
            fail(f"CLAUDE.md retains provider-authoritative agent: {stale}")

    handoff = frontmatter(ROOT / "handoff/templates/runtime-task-template.md")
    for key in (
        "task_id",
        "work_block_id",
        "from_runtime",
        "to_runtime",
        "logical_function",
        "source_revision",
        "authority",
        "allowed_scope",
        "forbidden_scope",
    ):
        if key not in handoff:
            fail(f"runtime task envelope missing {key}")


def run_script(path: Path, cwd: Path, payload: dict[str, Any]) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=cwd,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )
    if result.returncode:
        fail(f"{path.name} crashed: {result.stderr}")
    output = result.stdout.strip()
    if not output:
        return False, ""
    data = json.loads(output)
    reason = str(
        data.get("reason")
        or (data.get("hookSpecificOutput") or {}).get("permissionDecisionReason")
        or ""
    )
    denied = data.get("decision") == "block" or (
        data.get("hookSpecificOutput") or {}
    ).get("permissionDecision") == "deny"
    return bool(denied), reason


def assert_denied(label: str, value: tuple[bool, str], contains: str) -> None:
    denied, reason = value
    if not denied or contains.lower() not in reason.lower():
        fail(f"{label}: expected denial containing {contains!r}, got {reason!r}")


def assert_allowed(label: str, value: tuple[bool, str]) -> None:
    denied, reason = value
    if denied:
        fail(f"{label}: unexpectedly denied: {reason}")


def write_gate(repo: Path, *, ready: bool = True) -> dict[str, Any]:
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()
    gate: dict[str, Any] = {
        "schema_version": 1,
        "work_block_id": "wb-integration-fixture",
        "governance_profile": "Managed",
        "specification": {"path": "docs/specs/fixture.md", "revision": "v1"},
        "base_commit": head,
        "write_gate": {
            "status": "READY" if ready else "BLOCKED",
            "opened_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "expires_at": (
                dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1)
            ).isoformat(),
        },
        "critic": {
            "required": True,
            "status": "READY",
            "verdict": "APPROVE",
            "report": "docs/reports/critic.md",
            "isolation": "separate-session",
            "skip_reason": "",
        },
        "assurance": {
            "review": {
                "required": True,
                "status": "PENDING",
                "verdict": "PENDING",
                "report": "",
                "isolation": "unknown",
                "skip_reason": "",
            },
            "verification": {
                "required": True,
                "status": "PENDING",
                "verdict": "PENDING",
                "report": "",
                "isolation": "unknown",
                "skip_reason": "",
            },
            "drift": {
                "required": False,
                "status": "PENDING",
                "verdict": "PENDING",
                "report": "",
                "isolation": "unknown",
                "skip_reason": "",
            },
        },
        "closeout_mode": "pending",
        "integrations": {"approved": [], "admission_records": []},
        "write_set": ["src/**", "tests/**"],
        "coordination_write_set": [
            ".agent/active-work-block.json",
            "docs/plans/**",
            "docs/specs/**",
            "docs/reports/**",
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
    (repo / ".agent/active-work-block.json").write_text(
        json.dumps(gate, indent=2) + "\n", encoding="utf-8"
    )
    return gate


def event(repo: Path, tool: str, **tool_input: str) -> dict[str, Any]:
    return {
        "cwd": str(repo),
        "hook_event_name": "PreToolUse",
        "tool_name": tool,
        "tool_input": tool_input,
        "session_id": "fixture-session",
    }


def executable_fixtures() -> None:
    shared_hard_stop = TEMPLATE / ".agent/hooks/hard_stop_policy.py"
    write_guard = TEMPLATE / ".claude/hooks/work_block_gate.py"
    assurance_guard = TEMPLATE / ".claude/hooks/assurance_gate.py"

    with tempfile.TemporaryDirectory(prefix="integration-contracts-") as tmp:
        repo = Path(tmp)
        for path in (
            ".agent",
            "src",
            "tests",
            "docs/specs",
            "docs/plans",
            "docs/reports",
        ):
            (repo / path).mkdir(parents=True, exist_ok=True)
        (repo / "AGENTS.md").write_text("# Fixture\n", encoding="utf-8")
        (repo / "src/app.py").write_text("value = 1\n", encoding="utf-8")
        (repo / "README.md").write_text("fixture\n", encoding="utf-8")
        (repo / "docs/specs/fixture.md").write_text("# Spec\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q", "-b", "feature"], cwd=repo, check=True)
        subprocess.run(
            ["git", "config", "user.email", "fixture@example.com"],
            cwd=repo,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture"], cwd=repo, check=True
        )
        (repo / ".agent/active-work-block.json").write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)
        gate = write_gate(repo, ready=False)

        assert_denied(
            "external Codex CLI without admission",
            run_script(
                shared_hard_stop,
                repo,
                event(repo, "Bash", command="codex review"),
            ),
            "codex-cli",
        )

        gate["write_gate"]["status"] = "READY"
        gate["integrations"] = {
            "approved": ["codex-cli"],
            "admission_records": ["docs/reports/integrations/codex-cli.md"],
        }
        (repo / ".agent/active-work-block.json").write_text(
            json.dumps(gate, indent=2) + "\n", encoding="utf-8"
        )
        assert_allowed(
            "admitted external Codex CLI",
            run_script(
                shared_hard_stop,
                repo,
                event(repo, "Bash", command="codex review"),
            ),
        )

        gate["write_gate"]["status"] = "BLOCKED"
        (repo / ".agent/active-work-block.json").write_text(
            json.dumps(gate, indent=2) + "\n", encoding="utf-8"
        )
        assert_allowed(
            "blocked coordination write",
            run_script(
                write_guard,
                repo,
                event(repo, "Write", file_path="docs/plans/wb.md"),
            ),
        )
        assert_denied(
            "blocked source write",
            run_script(
                write_guard,
                repo,
                event(repo, "Write", file_path="src/app.py"),
            ),
            "READY",
        )

        gate["write_gate"]["status"] = "READY"
        (repo / ".agent/active-work-block.json").write_text(
            json.dumps(gate, indent=2) + "\n", encoding="utf-8"
        )
        assert_allowed(
            "in-scope Claude source write",
            run_script(
                write_guard,
                repo,
                event(repo, "Edit", file_path="src/app.py"),
            ),
        )
        assert_denied(
            "out-of-scope Claude source write",
            run_script(
                write_guard,
                repo,
                event(repo, "Edit", file_path="README.md"),
            ),
            "outside approved scope",
        )

        for name in ("review", "verification"):
            report = repo / f"docs/reports/{name}.md"
            report.write_text(f"# {name.title()}\n", encoding="utf-8")
            gate["assurance"][name].update(
                {
                    "status": "READY",
                    "verdict": "READY",
                    "report": f"docs/reports/{name}.md",
                    "isolation": "separate-session",
                }
            )
        gate["assurance"]["drift"].update(
            {
                "status": "SKIPPED",
                "verdict": "PENDING",
                "skip_reason": "No behavior or contract change in fixture.",
            }
        )
        gate["closeout_mode"] = "success-closeout"
        (repo / ".agent/active-work-block.json").write_text(
            json.dumps(gate, indent=2) + "\n", encoding="utf-8"
        )
        assert_allowed(
            "evidence-backed success closeout",
            run_script(assurance_guard, repo, {"cwd": str(repo)}),
        )

        gate["assurance"]["verification"]["verdict"] = "BLOCKED"
        (repo / ".agent/active-work-block.json").write_text(
            json.dumps(gate, indent=2) + "\n", encoding="utf-8"
        )
        assert_denied(
            "blocked verification cannot success-closeout",
            run_script(assurance_guard, repo, {"cwd": str(repo)}),
            "Verification",
        )



def main() -> int:
    static_contracts()
    executable_fixtures()
    print("Integration adapter contracts and fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
