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
DEFAULT_DEFINE_QUALITY = {
    "required": False,
    "status": "PENDING",
    "requirements_review": "",
    "traceability": "",
    "consistency_analysis": "",
}
READY_DEFINE_QUALITY = {
    "required": True,
    "status": "READY",
    "requirements_review": "docs/reports/requirements-quality.md",
    "traceability": "docs/reports/traceability.json",
    "consistency_analysis": "docs/reports/define-consistency.md",
}


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


def write_gate(repo: Path, *, status: str = "READY", profile: str = "Managed") -> dict:
    define_quality = dict(READY_DEFINE_QUALITY)
    if profile == "Controlled":
        define_quality = dict(DEFAULT_DEFINE_QUALITY)
    gate = {
        "schema_version": 3,
        "authority_mode": "github_capability",
        "work_block_id": "wb-fixture",
        "governance_profile": profile,
        "specification": {
            "path": "docs/specs/fixture.md",
            "revision": "v1",
        },
        "base_commit": "",
        "define_quality": define_quality,
        "write_gate": {"status": status, "opened_at": "fixture" if status == "READY" else None},
        "critic": {
            "required": True,
            "status": "READY",
            "verdict": "APPROVE",
            "report": "docs/reports/critic-fixture.md",
            "isolation": "separate_subagent",
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
    return gate


def persist_gate(repo: Path, gate: dict) -> None:
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
    if gate.get("define_quality") != DEFAULT_DEFINE_QUALITY:
        fail("generated gate must start with canonical Controlled Define-quality default")
    if "authorization" in gate or "hard_stop_approvals" in gate:
        fail("legacy signed authority fields remain in schema v3")
    if gate.get("write_gate") != {"status": "BLOCKED", "opened_at": None}:
        fail("generated gate must start BLOCKED")

    guard = PRE_TOOL.read_text(encoding="utf-8")
    for marker in (
        "validate_define_quality",
        "validate_governance_profile",
        "VALID_GOVERNANCE_PROFILES",
        "FORMAL_DEFINE_PROFILES",
        "requirements_review",
        "traceability",
        "consistency_analysis",
    ):
        if marker not in guard:
            fail(f"Codex source guard missing Define-quality marker: {marker}")

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
            "write_gate.status=READY",
        )

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

        gate = write_gate(repo)
        gate.pop("governance_profile")
        persist_gate(repo, gate)
        assert_denied(
            "missing governance profile",
            decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
            "governance_profile",
        )

        for label, invalid_profile in (
            ("empty governance profile", ""),
            ("whitespace governance profile", "   "),
            ("unknown governance profile", "Manged"),
            ("non-string governance profile", 42),
        ):
            gate = write_gate(repo)
            gate["governance_profile"] = invalid_profile
            persist_gate(repo, gate)
            assert_denied(
                label,
                decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
                "governance_profile",
            )

        gate = write_gate(repo, profile="Advisory")
        persist_gate(repo, gate)
        assert_denied(
            "Advisory source write",
            decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
            "Advisory",
        )

        write_gate(repo, profile="Controlled")
        assert_allowed(
            "Controlled non-applicable Define-quality remains proportional",
            decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
        )

        for profile in ("Managed", "Assured", "Distributed"):
            gate = write_gate(repo, profile=profile)
            gate["define_quality"]["required"] = False
            persist_gate(repo, gate)
            assert_denied(
                f"{profile} required=false cannot bypass",
                decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
                "required=false",
            )

        gate = write_gate(repo)
        gate.pop("define_quality")
        persist_gate(repo, gate)
        assert_denied(
            "Managed missing Define-quality",
            decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
            "define_quality",
        )

        gate = write_gate(repo)
        gate["define_quality"]["status"] = "PENDING"
        persist_gate(repo, gate)
        assert_denied(
            "Managed Define-quality pending",
            decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
            "status=READY",
        )

        gate = write_gate(repo)
        gate["define_quality"]["requirements_review"] = "   "
        persist_gate(repo, gate)
        assert_denied(
            "Managed blank Define-quality evidence",
            decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
            "requirements_review",
        )

        write_gate(repo)
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
        gate = write_gate(repo)
        gate["schema_version"] = 2
        persist_gate(repo, gate)
        assert_denied(
            "legacy schema source write",
            decision(PRE_TOOL, repo, event(repo, "Edit", file_path="src/app.py")),
            "schema_version=3",
        )
        gate = write_gate(repo)
        gate["critic"]["status"] = "PENDING"
        gate["critic"]["verdict"] = "PENDING"
        persist_gate(repo, gate)
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