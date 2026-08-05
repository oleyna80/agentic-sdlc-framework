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
    for path in (
        ROOT / "governance/evaluation.md",
        ROOT / "integrations/README.md",
        ROOT / "integrations/claude-code-codex-plugin/README.md",
        ROOT / "integrations/mcp/README.md",
        ROOT / "integrations/file-handoff/README.md",
        ROOT / "handoff/templates/runtime-task-template.md",
        TEMPLATE / "docs/templates/integration-admission-template.md",
        TEMPLATE / "docs/templates/evaluation-plan-template.json",
        TEMPLATE / "docs/templates/evaluation-report-template.json",
        TEMPLATE / "docs/templates/trajectory-event-template.json",
        TEMPLATE / "scripts/validate-evaluation.py",
        TEMPLATE / ".agent/hooks/hard_stop_policy.py",
        TEMPLATE / ".claude/hooks/work_block_gate.py",
        TEMPLATE / ".claude/hooks/assurance_gate.py",
        TEMPLATE / "opencode.json",
        ROOT / "opencode.json",
    ):
        require(path)

    for role in ("architect", "critic", "coder", "reviewer", "verifier"):
        require(ROOT / f".opencode/agents/{role}.md")

    claude = load_json(TEMPLATE / ".claude/settings.json")
    present = {"enabledMcpjsonServers", "permissions", "autoMode"}.intersection(claude)
    if present:
        fail(f"Claude settings pre-enable external state: {sorted(present)}")
    expected_agents = {
        "solution-architect",
        "critic",
        "reviewer",
        "scoped-coder",
        "verifier",
    }
    if set((claude.get("agents") or {}).keys()) != expected_agents:
        fail("Claude logical agent set mismatch")
    serialized = json.dumps(claude, sort_keys=True).lower()
    for stale in ("gpt-critic", "gpt-verifier", "codex-reviewer", "mcp__codex"):
        if stale in serialized:
            fail(f"Claude settings retain provider-specific default: {stale}")
    hook_commands = json.dumps(claude.get("hooks") or {})
    for expected in (
        ".agent/hooks/hard_stop_policy.py",
        ".claude/hooks/work_block_gate.py",
        ".claude/hooks/assurance_gate.py",
    ):
        if expected not in hook_commands:
            fail(f"Claude settings missing hook: {expected}")

    if load_json(TEMPLATE / ".mcp.json") != {"mcpServers": {}}:
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
    project_read = permissions.get("read")
    if not isinstance(project_read, dict):
        fail("OpenCode project read permission map missing")
    for pattern, expected in {
        ".env": "deny",
        ".env.*": "deny",
        ".env.example": "allow",
        "secrets/**": "deny",
        "credentials/**": "deny",
        "*.pem": "deny",
        "*.key": "deny",
    }.items():
        if project_read.get(pattern) != expected:
            fail(f"OpenCode project read permission must set {pattern!r} to {expected!r}")
    if permissions.get("question") != "ask":
        fail("OpenCode question permission must require ask")
    if permissions.get("doom_loop") != "ask":
        fail("OpenCode doom_loop permission must require ask")
    if permissions.get("todowrite") != "ask":
        fail("OpenCode todowrite permission must require ask")
    if permissions.get("lsp") != "ask":
        fail("OpenCode lsp permission must require ask")
    if permissions.get("list") != "allow":
        fail("OpenCode list permission must be allow")
    if permissions.get("mcp_*") != "ask":
        fail("OpenCode MCP tools must require ask")
    bash = permissions.get("bash")
    if not isinstance(bash, dict):
        fail("OpenCode Bash permission map missing")
    for pattern in ("git commit*", "git push*", "git reset --hard*", "git clean*", "rm *"):
        if bash.get(pattern) != "deny":
            fail(f"OpenCode Bash permission must deny {pattern!r}")
    task_perm = permissions.get("task")
    if not isinstance(task_perm, dict) or task_perm.get("*") != "ask":
        fail("OpenCode task permission must be a glob map with *: ask")
    skill_perm = permissions.get("skill")
    if not isinstance(skill_perm, dict) or skill_perm.get("*") != "allow":
        fail("OpenCode skill permission must be a glob map with *: allow")
    if skill_perm.get("internal-*") != "deny":
        fail("OpenCode skill permission must deny internal-*")
    if list(skill_perm) != ["*", "internal-*"]:
        fail("OpenCode skill deny rule must follow the catch-all")
    if opencode.get("model") or opencode.get("provider"):
        fail("public OpenCode baseline must not pin provider/model routing")
    if opencode.get("default_agent") != "build":
        fail("OpenCode default_agent must be build")
    if opencode.get("subagent_depth") != 1:
        fail("OpenCode subagent_depth must be 1")
    if opencode.get("share") != "manual":
        fail("OpenCode share must be manual")
    if opencode.get("snapshot") is not True:
        fail("OpenCode snapshot must be enabled")
    for forbidden in (
        "auth",
        "enabled_providers",
        "disabled_providers",
        "experimental",
        "model",
        "provider",
        "server",
        "tools",
    ):
        if forbidden in opencode:
            fail(f"OpenCode baseline must not configure {forbidden}")

    for role in ("architect", "critic", "coder", "reviewer", "verifier"):
        data = frontmatter(TEMPLATE / f".opencode/agents/{role}.md")
        if data.get("mode") != "subagent":
            fail(f"OpenCode {role} must use mode: subagent")
        role_permissions = data.get("permission")
        if not isinstance(role_permissions, dict):
            fail(f"OpenCode {role} permission map missing")
        expected_edit = "ask" if role == "coder" else "deny"
        if role_permissions.get("edit") != expected_edit:
            fail(f"OpenCode {role} edit permission must be {expected_edit}")
        role_read = role_permissions.get("read")
        if not isinstance(role_read, dict):
            fail(f"OpenCode {role} read permission map missing")
        for pattern, expected in {
            ".env": "deny",
            ".env.*": "deny",
            ".env.example": "allow",
            "secrets/**": "deny",
            "credentials/**": "deny",
            "*.pem": "deny",
            "*.key": "deny",
        }.items():
            if role_read.get(pattern) != expected:
                fail(
                    f"OpenCode {role} read permission must set {pattern!r} to {expected!r}"
                )
        if role_permissions.get("task") != "deny":
            fail(f"OpenCode {role} nested task delegation must be denied")
        if role_permissions.get("mcp_*") != "ask":
            fail(f"OpenCode {role} MCP tools must require ask")
        skill_permissions = role_permissions.get("skill")
        if not isinstance(skill_permissions, dict):
            fail(f"OpenCode {role} skill permission map missing")
        if list(skill_permissions) != ["*", "internal-*"]:
            fail(f"OpenCode {role} skill deny rule must follow the catch-all")
        if skill_permissions.get("*") != "allow" or skill_permissions.get("internal-*") != "deny":
            fail(
                f"OpenCode {role} skill permissions must allow public and deny internal skills"
            )
        if role_permissions.get("external_directory") != "deny":
            fail(f"OpenCode {role} external_directory must be denied")
        if data.get("model"):
            fail(f"OpenCode {role} must not pin a public model")
        body = (TEMPLATE / f".opencode/agents/{role}.md").read_text(encoding="utf-8")
        if "tools:" in body or "maxSteps" in body:
            fail(f"OpenCode {role} uses deprecated agent configuration")

    for relative in (
        "opencode.json",
        ".opencode/agents/architect.md",
        ".opencode/agents/critic.md",
        ".opencode/agents/coder.md",
        ".opencode/agents/reviewer.md",
        ".opencode/agents/verifier.md",
    ):
        if (ROOT / relative).read_bytes() != (TEMPLATE / relative).read_bytes():
            fail(f"project OpenCode surface drifted from template: {relative}")

    for path in (
        TEMPLATE / ".claude/agents/gpt-critic.md",
        TEMPLATE / ".claude/agents/gpt-verifier.md",
        TEMPLATE / ".claude/agents/codex-reviewer.md",
        TEMPLATE / ".claude/agent-memory/gpt-critic/MEMORY.md",
        TEMPLATE / ".claude/agent-memory/gpt-verifier/MEMORY.md",
        TEMPLATE / ".claude/agent-memory/codex-reviewer/MEMORY.md",
    ):
        if path.exists():
            fail(f"provider-named compatibility path remains: {path.relative_to(ROOT)}")

    gate = load_json(TEMPLATE / ".agent/active-work-block.json")
    if gate.get("schema_version") != 2:
        fail("active Work Block schema_version must remain 2")
    if gate.get("integrations") != {"approved": [], "admission_records": []}:
        fail("generated integration approvals must start empty")
    assurance = gate.get("assurance")
    if not isinstance(assurance, dict) or set(assurance) != {
        "review",
        "verification",
        "evaluation",
        "drift",
    }:
        fail("active Work Block assurance functions missing")
    evaluation = assurance["evaluation"]
    if evaluation.get("required") is not False:
        fail("generated evaluation assurance must be optional by default")
    if evaluation.get("status") != "PENDING" or evaluation.get("verdict") != "PENDING":
        fail("generated evaluation assurance must start PENDING")
    if gate.get("closeout_mode") != "pending":
        fail("generated closeout_mode must start pending")

    claude_entry = (TEMPLATE / "CLAUDE.md").read_text(encoding="utf-8").lower()
    for stale in ("gpt-critic", "gpt-verifier", "codex-reviewer"):
        if stale in claude_entry:
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
    specific = data.get("hookSpecificOutput") or {}
    reason = str(data.get("reason") or specific.get("permissionDecisionReason") or "")
    denied = data.get("decision") == "block" or specific.get("permissionDecision") == "deny"
    return bool(denied), reason


def assert_denied(label: str, value: tuple[bool, str], contains: str) -> None:
    denied, reason = value
    if not denied or contains.lower() not in reason.lower():
        fail(f"{label}: expected denial containing {contains!r}, got {reason!r}")


def assert_allowed(label: str, value: tuple[bool, str]) -> None:
    denied, reason = value
    if denied:
        fail(f"{label}: unexpectedly denied: {reason}")


def event(repo: Path, tool: str, **tool_input: str) -> dict[str, Any]:
    return {
        "cwd": str(repo),
        "hook_event_name": "PreToolUse",
        "tool_name": tool,
        "tool_input": tool_input,
        "session_id": "fixture-session",
    }


def write_gate(repo: Path, *, ready: bool = True) -> dict[str, Any]:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    gate: dict[str, Any] = {
        "schema_version": 2,
        "work_block_id": "wb-integration-fixture",
        "governance_profile": "Managed",
        "specification": {"path": "docs/specs/fixture.md", "revision": "v1"},
        "base_commit": head,
        "write_gate": {
            "status": "READY" if ready else "BLOCKED",
            "opened_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "expires_at": (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1)).isoformat(),
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
            "evaluation": {
                "required": False,
                "status": "PENDING",
                "verdict": "PENDING",
                "plan": "",
                "report": "",
                "rubric_revision": "",
                "benchmark_revision": "",
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


def persist(repo: Path, gate: dict[str, Any]) -> None:
    (repo / ".agent/active-work-block.json").write_text(
        json.dumps(gate, indent=2) + "\n", encoding="utf-8"
    )


def executable_fixtures() -> None:
    hard_stop = TEMPLATE / ".agent/hooks/hard_stop_policy.py"
    write_guard = TEMPLATE / ".claude/hooks/work_block_gate.py"
    assurance_guard = TEMPLATE / ".claude/hooks/assurance_gate.py"
    evaluation_validator = TEMPLATE / "scripts/validate-evaluation.py"

    with tempfile.TemporaryDirectory(prefix="integration-contracts-") as tmp:
        repo = Path(tmp)
        for path in (
            ".agent",
            "scripts",
            "src",
            "tests",
            "docs/specs",
            "docs/plans",
            "docs/reports",
        ):
            (repo / path).mkdir(parents=True, exist_ok=True)
        shutil.copy2(evaluation_validator, repo / "scripts/validate-evaluation.py")
        (repo / "AGENTS.md").write_text("# Fixture\n", encoding="utf-8")
        (repo / "src/app.py").write_text("value = 1\n", encoding="utf-8")
        (repo / "README.md").write_text("fixture\n", encoding="utf-8")
        (repo / "docs/specs/fixture.md").write_text("# Spec\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q", "-b", "feature"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.com"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=repo, check=True)
        (repo / ".agent/active-work-block.json").write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)

        # Integration admission is tested inside an active approval window.
        gate = write_gate(repo, ready=True)
        assert_denied(
            "external Codex CLI without admission",
            run_script(hard_stop, repo, event(repo, "Bash", command="codex review")),
            "codex-cli",
        )
        gate["integrations"] = {
            "approved": ["codex-cli"],
            "admission_records": ["docs/reports/integrations/codex-cli.md"],
        }
        persist(repo, gate)
        assert_allowed(
            "admitted external Codex CLI",
            run_script(hard_stop, repo, event(repo, "Bash", command="codex review")),
        )

        # This fixture also exercises the still-v1 Claude write guard; reset its
        # disposable gate after the schema-v2 shared Hard Stop assertions.
        gate["schema_version"] = 1
        gate["write_gate"]["status"] = "BLOCKED"
        persist(repo, gate)
        assert_allowed(
            "blocked coordination write",
            run_script(write_guard, repo, event(repo, "Write", file_path="docs/plans/wb.md")),
        )
        assert_denied(
            "blocked source write",
            run_script(write_guard, repo, event(repo, "Write", file_path="src/app.py")),
            "READY",
        )

        gate["write_gate"]["status"] = "READY"
        persist(repo, gate)
        assert_allowed(
            "in-scope Claude source write",
            run_script(write_guard, repo, event(repo, "Edit", file_path="src/app.py")),
        )
        assert_denied(
            "out-of-scope Claude source write",
            run_script(write_guard, repo, event(repo, "Edit", file_path="README.md")),
            "outside approved scope",
        )

        for name in ("review", "verification"):
            (repo / f"docs/reports/{name}.md").write_text(
                f"# {name.title()}\n", encoding="utf-8"
            )
            gate["assurance"][name].update(
                {
                    "status": "READY",
                    "verdict": "READY",
                    "report": f"docs/reports/{name}.md",
                    "isolation": "separate-session",
                }
            )
        gate["assurance"]["evaluation"].update(
            {
                "status": "SKIPPED",
                "verdict": "UNVERIFIED",
                "skip_reason": "No non-deterministic output or trajectory requirement in fixture.",
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
        persist(repo, gate)
        assert_allowed(
            "evidence-backed success closeout",
            run_script(assurance_guard, repo, {"cwd": str(repo)}),
        )

        gate["assurance"]["evaluation"]["required"] = True
        persist(repo, gate)
        assert_denied(
            "required evaluation cannot be skipped",
            run_script(assurance_guard, repo, {"cwd": str(repo)}),
            "evaluation",
        )

        gate["assurance"]["evaluation"]["required"] = False
        gate["assurance"]["verification"]["verdict"] = "BLOCKED"
        persist(repo, gate)
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
