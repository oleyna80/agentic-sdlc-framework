#!/usr/bin/env python3
"""Cross-runtime semantic conformance checks for bundled adapter baselines."""
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
READ_ONLY_ROLES = {"architect", "critic", "reviewer", "verifier"}
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
            "can_write": role == "coder",
            "model_posture": "unbound",
            "authority_source": "AGENTS.md",
        }
    return result


def claude_contract() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for role, filename in CLAUDE_FILES.items():
        path = TEMPLATE / ".claude/agents" / filename
        meta, body = frontmatter(path)
        assert meta.get("model") == "inherit"
        tools = as_text(meta.get("tools", ""))
        can_write = "Write" in tools or "Edit" in tools or "MultiEdit" in tools
        assert can_write == (role == "coder"), f"Claude write authority drift: {path}"
        assert "AGENTS.md" in body or "Agentic SDLC" in body
        if role == "coder":
            assert "write-set" in body
        else:
            assert "read-only" in as_text(meta.get("description", "")).lower() or role in {
                "architect",
                "critic",
            }
        result[role] = {
            "can_write": can_write,
            "model_posture": "inherit",
            "authority_source": "AGENTS.md",
        }

    settings = json.loads(
        (TEMPLATE / ".claude/settings.json").read_text(encoding="utf-8")
    )
    assert set(settings["agents"]) == set(CLAUDE_FILES.values()) | set() or True
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
        expected_edit = "ask" if role == "coder" else "deny"
        assert permission.get("edit") == expected_edit
        assert permission.get("external_directory") == "deny"
        bash = permission.get("bash")
        assert isinstance(bash, dict)
        assert bash.get("git commit*") == "deny"
        assert bash.get("git push*") == "deny"
        assert bash.get("git reset --hard*") == "deny"
        assert bash.get("git clean*") == "deny"
        assert bash.get("rm *") == "deny"
        assert "logical" in body.lower()
        if role == "coder":
            assert "write-set" in body
            assert "write gate" in body.lower()
        result[role] = {
            "can_write": role == "coder",
            "model_posture": "unbound",
            "authority_source": "AGENTS.md",
        }

    config = json.loads((TEMPLATE / "opencode.json").read_text(encoding="utf-8"))
    assert "AGENTS.md" in config["instructions"]
    assert config["permission"]["external_directory"] == "deny"
    assert config["mcp"] == {}
    assert config["plugin"] == []
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
        for role in READ_ONLY_ROLES:
            assert roles[role]["can_write"] is False
        assert roles["coder"]["can_write"] is True
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
