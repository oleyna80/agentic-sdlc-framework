#!/usr/bin/env python3
"""Focused fixtures for Codex Hard Stop approvals."""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE_TEST = ROOT / "scripts/test-codex-adapter.py"
HARD_STOP = ROOT / "template/.codex/hooks/hard_stop_policy.py"
HOOKS_CONFIG = ROOT / "template/.codex/hooks.json"

spec = importlib.util.spec_from_file_location("codex_adapter_test", BASE_TEST)
if spec is None or spec.loader is None:
    raise RuntimeError("unable to load Codex adapter fixture helpers")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def set_approvals(repo: Path, **values: bool) -> None:
    path = repo / ".agent/active-work-block.json"
    gate = json.loads(path.read_text(encoding="utf-8"))
    gate["hard_stop_approvals"].update(values)
    path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")


def set_gate_status(repo: Path, status: str) -> None:
    path = repo / ".agent/active-work-block.json"
    gate = json.loads(path.read_text(encoding="utf-8"))
    gate["write_gate"]["status"] = status
    path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")


def assert_hook_wiring() -> None:
    config = json.loads(HOOKS_CONFIG.read_text(encoding="utf-8"))
    groups = config.get("hooks", {}).get("PreToolUse", [])
    commands = [
        hook.get("command", "")
        for group in groups
        for hook in group.get("hooks", [])
        if isinstance(hook, dict)
    ]
    for required in ("hard_stop_policy.py", "pre_tool_use_policy.py"):
        if not any(required in command for command in commands):
            raise AssertionError(f"PreToolUse hook wiring missing {required}")


def main() -> int:
    assert_hook_wiring()

    with tempfile.TemporaryDirectory(prefix="codex-hard-stops-") as temp:
        repo = Path(temp)
        for path in (".agent", "src", "tests", "docs/specs", "docs/reports"):
            (repo / path).mkdir(parents=True, exist_ok=True)
        (repo / "AGENTS.md").write_text("# Fixture\n", encoding="utf-8")
        (repo / "src/app.py").write_text("value = 1\n", encoding="utf-8")
        module.git(repo, "init", "-q", "-b", "feature")
        module.git(repo, "config", "user.email", "fixture@example.com")
        module.git(repo, "config", "user.name", "Fixture")
        module.write_gate(repo, status="BLOCKED", base="0000000")
        module.git(repo, "add", ".")
        module.git(repo, "commit", "-qm", "baseline")
        module.write_gate(repo)

        push_command = "git push origin feature"
        legacy = json.loads((repo / ".agent/active-work-block.json").read_text(encoding="utf-8"))
        legacy["schema_version"] = 1
        legacy["hard_stop_approvals"]["git_push"] = True
        (repo / ".agent/active-work-block.json").write_text(
            json.dumps(legacy, indent=2) + "\n", encoding="utf-8"
        )
        module.assert_denied(
            "legacy hard-stop schema",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", push_command)),
            "schema_version=2",
        )
        module.write_gate(repo)
        module.assert_denied(
            "unapproved push",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", push_command)),
            "git_push",
        )
        set_approvals(repo, git_push=True)
        module.assert_allowed(
            "approved feature push",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", push_command)),
        )

        # A commit changes HEAD and invalidates the previous push approval window.
        module.git(repo, "commit", "--allow-empty", "-qm", "advance-head")
        module.assert_denied(
            "stale push approval after HEAD change",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", push_command)),
            "Stale approval",
        )
        module.write_gate(repo)
        set_approvals(repo, git_push=True)

        for command in (
            "git push origin main",
            "git push origin +main",
            "git push origin :main",
            "git push origin HEAD:refs/heads/main",
            "git push origin +HEAD:refs/heads/main",
        ):
            module.assert_denied(
                f"default branch push {command}",
                module.decision(HARD_STOP, repo, module.event(repo, "Bash", command)),
                "default_branch_push",
            )

        module.git(repo, "branch", "-m", "main")
        module.assert_denied(
            "standalone HEAD from default branch",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", "git push origin HEAD")),
            "default_branch_push",
        )
        module.git(repo, "branch", "-m", "feature")

        module.assert_denied(
            "secret access",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", "cat .env")),
            "credentials",
        )

        for command in (
            "rm -r src",
            "rm -rf src",
            "rm -fr src",
            "rm --recursive src",
            "sudo rm -rf src",
            "command rm -rf src",
            "echo inspected\nrm -rf src",
        ):
            module.assert_denied(
                f"destructive command {command!r}",
                module.decision(HARD_STOP, repo, module.event(repo, "Bash", command)),
                "destructive",
            )

        # Approvals are valid only inside an active, non-expired Work Block gate.
        module.write_gate(repo)
        set_approvals(repo, git_push=True)
        expired = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=1)).isoformat()
        path = repo / ".agent/active-work-block.json"
        gate = json.loads(path.read_text(encoding="utf-8"))
        gate["write_gate"]["expires_at"] = expired
        path.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")
        module.assert_denied(
            "approved push with expired approval window",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", push_command)),
            "expired",
        )

        module.write_gate(repo)
        set_approvals(repo, git_push=True)
        set_gate_status(repo, "BLOCKED")
        module.assert_denied(
            "approved push with blocked Work Block gate",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", push_command)),
            "write_gate.status=READY",
        )

    print("Codex Hard Stop fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
