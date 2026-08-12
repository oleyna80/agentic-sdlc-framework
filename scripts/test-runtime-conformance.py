#!/usr/bin/env python3
"""Cross-runtime semantic conformance checks for bundled adapter baselines.

Runtime syntax differs. Conformance therefore compares implementation/source
write authority separately from limited report, draft, or runtime-local memory
writes.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import tomllib
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - CI installs PyYAML
    raise SystemExit("PyYAML is required for runtime conformance tests") from exc

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "template"
ROLES = ("architect", "critic", "coder", "reviewer", "verifier")
NON_IMPLEMENTATION_ROLES = {"architect", "critic", "reviewer", "verifier"}
CLAUDE_FILES = {
    "architect": "solution-architect.md",
    "critic": "critic.md",
    "coder": "scoped-coder.md",
    "reviewer": "reviewer.md",
    "verifier": "verifier.md",
}


def frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"missing YAML frontmatter: {path}")
    _, raw, body = text.split("---", 2)
    value = yaml.safe_load(raw)
    if not isinstance(value, dict):
        raise AssertionError(f"frontmatter must be an object: {path}")
    return value, body


def as_text(value: object) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, sort_keys=True)


def codex_contract() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for role in ROLES:
        path = TEMPLATE / ".codex/agents" / f"{role}.toml"
        value = tomllib.loads(path.read_text(encoding="utf-8"))
        assert value.get("name") == role
        assert "model" not in value, f"public Codex agent pins model: {path}"
        expected_sandbox = "workspace-write" if role == "coder" else "read-only"
        assert value.get("sandbox_mode") == expected_sandbox
        instructions = str(value.get("developer_instructions", ""))
        assert "AGENTS.md" in instructions
        assert re.search(rf"logical\s+{role}\s+function", instructions, re.I)
        if role == "coder":
            assert ".agent/active-work-block.json" in instructions
            assert "write-set" in instructions
        result[role] = {
            "implementation_write": role == "coder",
            "limited_artifact_write": False,
            "model_posture": "unbound",
            "authority_source": "AGENTS.md",
        }
    return result


def claude_limited_write_boundary(role: str, body: str, path: Path) -> bool:
    lower = body.lower()
    assert "read-only" in lower, f"Claude non-Coder lacks read-only declaration: {path}"
    assert re.search(
        r"do\s+not\s+(?:write|change|edit)|forbidden|any edit/write",
        lower,
    ), f"Claude non-Coder lacks explicit implementation-write prohibition: {path}"

    if role in {"architect", "critic"}:
        assert ".claude/agent-memory/" in body
        assert re.search(r"only\s+.*memory\.md|memory\.md\s+only", lower)
    elif role == "verifier":
        assert "docs/reports" in body
        assert ".claude/agent-memory/verifier/MEMORY.md" in body
        assert re.search(r"edit/write production code|change tested code", lower)
    else:
        raise AssertionError(f"unexpected limited-write role {role}: {path}")
    return True


def claude_contract() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for role, filename in CLAUDE_FILES.items():
        path = TEMPLATE / ".claude/agents" / filename
        meta, body = frontmatter(path)
        assert meta.get("model") == "inherit"
        tools = as_text(meta.get("tools", ""))
        raw_write_tool = any(token in tools for token in ("Write", "Edit", "MultiEdit"))

        if role == "coder":
            assert raw_write_tool, f"Claude Coder lacks a write-capable tool: {path}"
            assert "write-set" in body
            implementation_write = True
            limited_artifact_write = False
        else:
            implementation_write = False
            limited_artifact_write = (
                claude_limited_write_boundary(role, body, path)
                if raw_write_tool
                else False
            )
            if not raw_write_tool:
                assert "read-only" in (
                    as_text(meta.get("description", "")) + body
                ).lower()

        assert "AGENTS.md" in body or "Agentic SDLC" in body
        result[role] = {
            "implementation_write": implementation_write,
            "limited_artifact_write": limited_artifact_write,
            "model_posture": "inherit",
            "authority_source": "AGENTS.md",
        }

    settings = json.loads(
        (TEMPLATE / ".claude/settings.json").read_text(encoding="utf-8")
    )
    assert set(settings["agents"]) == {
        "solution-architect",
        "critic",
        "scoped-coder",
        "reviewer",
        "verifier",
    }
    commands = json.dumps(settings.get("hooks", {}), sort_keys=True)
    for required in (
        ".agent/hooks/hard_stop_policy.py",
        ".claude/hooks/work_block_gate.py",
        ".claude/hooks/assurance_gate.py",
    ):
        assert required in commands
    assert "enabledMcpjsonServers" not in settings
    return result


def opencode_contract() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for role in ROLES:
        path = TEMPLATE / ".opencode/agents" / f"{role}.md"
        meta, body = frontmatter(path)
        assert meta.get("mode") == "subagent"
        assert "model" not in meta
        permission = meta.get("permission")
        assert isinstance(permission, dict)
        read = permission.get("read")
        assert isinstance(read, dict)
        assert read.get("*") == "allow"
        assert read.get(".env") == "deny"
        assert read.get(".env.*") == "deny"
        assert read.get(".env.example") == "allow"
        assert read.get("secrets/**") == "deny"
        assert read.get("credentials/**") == "deny"
        assert read.get("*.pem") == "deny"
        assert read.get("*.key") == "deny"
        assert list(read) == [
            "*",
            ".env",
            ".env.*",
            ".env.example",
            "secrets/**",
            "credentials/**",
            "*.pem",
            "*.key",
        ]
        expected_edit = "ask" if role == "coder" else "deny"
        assert permission.get("edit") == expected_edit
        assert permission.get("external_directory") == "deny"
        bash = permission.get("bash")
        assert isinstance(bash, dict)
        expected_commit = "allow" if role == "coder" else "deny"
        expected_push = "ask" if role == "coder" else "deny"
        assert bash.get("git commit*") == expected_commit
        assert bash.get("git push*") == expected_push
        assert bash.get("git reset --hard*") == "deny"
        assert bash.get("git clean*") == "deny"
        assert bash.get("rm *") == "deny"
        assert permission.get("question") == "ask"
        assert permission.get("doom_loop") == "ask"
        assert permission.get("todowrite") == "ask"
        assert permission.get("lsp") == "ask"
        assert permission.get("list") == "allow"
        assert permission.get("task") == "deny"
        assert permission.get("mcp_*") == "ask"
        skill = permission.get("skill")
        assert isinstance(skill, dict)
        assert skill.get("*") == "allow"
        assert skill.get("internal-*") == "deny"
        assert list(skill) == ["*", "internal-*"]
        assert "logical" in body.lower()
        if role == "critic":
            for verdict in ("APPROVE", "APPROVE_WITH_CHANGES", "RECONSIDER", "BLOCKED"):
                assert verdict in body
            assert "SUPPLEMENT" not in body
        if role == "coder":
            assert "write-set" in body
            assert "write gate" in body.lower()
            assert "local commits are allowed" in body.lower()
        result[role] = {
            "implementation_write": role == "coder",
            "limited_artifact_write": False,
            "model_posture": "unbound",
            "authority_source": "AGENTS.md",
        }

    config = json.loads((TEMPLATE / "opencode.json").read_text(encoding="utf-8"))
    assert "AGENTS.md" in config["instructions"]
    project_read = config["permission"]["read"]
    assert isinstance(project_read, dict)
    assert project_read.get(".env") == "deny"
    assert project_read.get(".env.*") == "deny"
    assert project_read.get(".env.example") == "allow"
    assert config["permission"]["external_directory"] == "deny"
    assert config["permission"]["question"] == "ask"
    assert config["permission"]["doom_loop"] == "ask"
    assert config["permission"]["todowrite"] == "ask"
    assert config["permission"]["lsp"] == "ask"
    assert config["permission"]["list"] == "allow"
    assert config["permission"]["mcp_*"] == "ask"
    project_bash = config["permission"]["bash"]
    assert isinstance(project_bash, dict)
    assert project_bash.get("git commit*") == "allow"
    assert project_bash.get("git push*") == "ask"
    assert project_bash.get("git reset --hard*") == "deny"
    assert project_bash.get("git clean*") == "deny"
    assert project_bash.get("rm *") == "deny"
    task_perm = config["permission"]["task"]
    assert isinstance(task_perm, dict)
    assert task_perm.get("*") == "ask"
    skill_perm = config["permission"]["skill"]
    assert isinstance(skill_perm, dict)
    assert skill_perm.get("*") == "allow"
    assert skill_perm.get("internal-*") == "deny"
    assert list(skill_perm) == ["*", "internal-*"]
    assert config["mcp"] == {}
    assert config["plugin"] == []
    assert config.get("default_agent") == "build"
    assert config.get("subagent_depth") == 1
    assert config.get("share") == "manual"
    assert config.get("snapshot") is True

    runtime_paths = [
        "opencode.json",
        ".opencode/agents/architect.md",
        ".opencode/agents/critic.md",
        ".opencode/agents/coder.md",
        ".opencode/agents/reviewer.md",
        ".opencode/agents/verifier.md",
    ]
    for relative in runtime_paths:
        template_path = TEMPLATE / relative
        project_path = ROOT / relative
        assert project_path.is_file(), f"missing project OpenCode surface: {relative}"
        assert project_path.read_bytes() == template_path.read_bytes(), (
            f"project OpenCode surface drifted from template: {relative}"
        )
    return result


def shared_gate_contract() -> None:
    codex_hooks = json.loads(
        (TEMPLATE / ".codex/hooks.json").read_text(encoding="utf-8")
    )
    codex_text = json.dumps(codex_hooks, sort_keys=True)
    for required in (
        "hard_stop_policy.py",
        "pre_tool_use_policy.py",
        "subagent_context.py",
    ):
        assert required in codex_text

    for relative in (".codex/scripts/lifecycle.py", ".codex/scripts/doctor.py"):
        assert (TEMPLATE / relative).is_file(), f"missing Codex helper: {relative}"

    gate = json.loads(
        (TEMPLATE / ".agent/active-work-block.json").read_text(encoding="utf-8")
    )
    assert gate.get("schema_version") == 3
    assert gate.get("authority_mode") == "github_capability"
    assert "authorization" not in gate
    assert "hard_stop_approvals" not in gate

    shared = (TEMPLATE / ".agent/hooks/hard_stop_policy.py").read_text(
        encoding="utf-8"
    )
    for runtime_id in ("codex-cli", "claude-code-cli", "opencode-cli"):
        assert runtime_id in shared
    assert "admission_records" in shared

    mcp = json.loads((TEMPLATE / ".mcp.json").read_text(encoding="utf-8"))
    assert mcp == {"mcpServers": {}}

    generic = (ROOT / "runtimes/generic/README.md").read_text(encoding="utf-8")
    assert "Work Block" in generic
    assert re.search(r"separate\s+(documented\s+)?(pass|session)", generic, re.I)
    assert "degraded" in generic.lower()


def compare_semantics(contracts: dict[str, dict[str, dict[str, Any]]]) -> None:
    for runtime, roles in contracts.items():
        assert set(roles) == set(ROLES), f"{runtime} role set drifted"
        for role in NON_IMPLEMENTATION_ROLES:
            assert roles[role]["implementation_write"] is False, (
                f"{runtime} grants implementation write to {role}"
            )
        assert roles["coder"]["implementation_write"] is True
        assert all(value["authority_source"] == "AGENTS.md" for value in roles.values())


def main() -> int:
    contracts = {
        "codex": codex_contract(),
        "claude-code": claude_contract(),
        "opencode": opencode_contract(),
    }
    compare_semantics(contracts)
    shared_gate_contract()
    print("Cross-runtime semantic conformance: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
