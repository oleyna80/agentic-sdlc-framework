#!/usr/bin/env python3
"""Focused fixtures for schema v3 external Hard Stop guardrails."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HARD_STOP = ROOT / "template/.codex/hooks/hard_stop_policy.py"
HOOKS_CONFIG = ROOT / "template/.codex/hooks.json"


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


def git(repo: Path, *args: str) -> str:
    result = run("git", *args, cwd=repo)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def event(repo: Path, command: str) -> dict:
    return {
        "cwd": str(repo),
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }


def decision(repo: Path, command: str) -> tuple[bool, str]:
    result = run(sys.executable, str(HARD_STOP), cwd=repo, payload=event(repo, command))
    assert result.returncode == 0, result.stderr
    if not result.stdout.strip():
        return False, ""
    output = json.loads(result.stdout)
    specific = output.get("hookSpecificOutput", {})
    return specific.get("permissionDecision") == "deny", str(
        specific.get("permissionDecisionReason") or ""
    )


def allowed(repo: Path, command: str) -> None:
    denied, reason = decision(repo, command)
    assert not denied, f"{command!r} unexpectedly denied: {reason}"


def denied(repo: Path, command: str, contains: str) -> None:
    is_denied, reason = decision(repo, command)
    assert is_denied, f"{command!r} unexpectedly allowed"
    assert contains.lower() in reason.lower(), (command, reason)


def gate(repo: Path, *, integrations: dict | None = None) -> None:
    value = {
        "schema_version": 3,
        "authority_mode": "github_capability",
        "work_block_id": "WB-FIXTURE",
        "write_gate": {"status": "READY", "opened_at": "fixture"},
        "integrations": integrations or {"approved": [], "admission_records": []},
    }
    (repo / ".agent/active-work-block.json").write_text(
        json.dumps(value, indent=2) + "\n", encoding="utf-8"
    )


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
        assert any(required in command for command in commands), required


def main() -> int:
    assert_hook_wiring()
    with tempfile.TemporaryDirectory(prefix="codex-hard-stops-v3-") as temp:
        repo = Path(temp)
        (repo / ".agent").mkdir()
        (repo / "src").mkdir()
        (repo / "src/app.py").write_text("value = 1\n", encoding="utf-8")
        git(repo, "init", "-q", "-b", "feature")
        git(repo, "config", "user.email", "fixture@example.com")
        git(repo, "config", "user.name", "Fixture")
        gate(repo)
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "baseline")

        # Normal reversible Git operations are not Owner Hard Stops.
        allowed(repo, "git commit -m normal-feature-commit")
        allowed(repo, "git push origin feature")
        allowed(repo, "git status --short")

        # Protected/default branch and history-rewriting pushes remain denied locally,
        # and GitHub rules provide the external framework boundary.
        for command in (
            "git push origin main",
            "git push origin master",
            "git push origin HEAD:refs/heads/main",
        ):
            denied(repo, command, "default-branch")
        for command in (
            "git push -f origin feature",
            "git push --force origin feature",
            "git push --force-with-lease origin feature",
            "git push origin +feature",
        ):
            denied(repo, command, "Force push")

        git(repo, "branch", "-m", "main")
        denied(repo, "git push origin HEAD", "default-branch")
        git(repo, "branch", "-m", "feature")

        for command in (
            "rm -r src",
            "rm -rf src",
            "sudo rm -rf src",
            "command rm --recursive src",
            "git reset --hard HEAD~1",
            "git clean -fd",
        ):
            denied(repo, command, "destructive")

        for command in (
            "ssh deploy@example.invalid uptime",
            "scp file deploy@example.invalid:/tmp/file",
            "kubectl apply -f deployment.yml",
            "terraform apply plan.tfplan",
            "systemctl restart app",
        ):
            denied(repo, command, "live infrastructure")

        denied(repo, "docker push ghcr.io/example/app:sha-123", "external image publish")
        denied(repo, "psql db -c 'UPDATE users SET x=1'", "live-data")
        denied(repo, "cat .env", "credential")
        denied(repo, "sendmail client@example.invalid", "client-facing")

        denied(repo, "codex exec review", "integrations.approved")
        gate(
            repo,
            integrations={
                "approved": ["codex-cli"],
                "admission_records": ["docs/reports/codex-admission.md"],
            },
        )
        allowed(repo, "codex exec review")

    print("Codex external Hard Stop fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
