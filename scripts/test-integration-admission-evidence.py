#!/usr/bin/env python3
"""Regression fixture: integration ID alone is not sufficient admission."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "template/.agent/hooks/hard_stop_policy.py"


def run(repo: Path, command: str) -> tuple[bool, str]:
    payload = {
        "cwd": str(repo),
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
    }
    result = subprocess.run(
        [sys.executable, str(POLICY)],
        cwd=repo,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )
    if result.returncode:
        raise AssertionError(result.stderr)
    if not result.stdout.strip():
        return False, ""
    data = json.loads(result.stdout)
    specific = data.get("hookSpecificOutput") or {}
    return (
        specific.get("permissionDecision") == "deny",
        str(specific.get("permissionDecisionReason") or ""),
    )


def write_gate(repo: Path, records: list[str]) -> None:
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True
    ).strip()
    gate = {
        "schema_version": 3,
        "authority_mode": "github_capability",
        "work_block_id": "wb-integration-admission-fixture",
        "base_commit": head,
        "write_gate": {"status": "READY", "opened_at": "fixture"},
        "integrations": {
            "approved": ["codex-cli"],
            "admission_records": records,
        },
    }
    (repo / ".agent/active-work-block.json").write_text(
        json.dumps(gate, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="integration-admission-") as tmp:
        repo = Path(tmp)
        (repo / ".agent").mkdir(parents=True)
        (repo / "README.md").write_text("fixture\n", encoding="utf-8")
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

        write_gate(repo, [])
        denied, reason = run(repo, "codex review")
        if not denied or "admission evidence" not in reason:
            raise AssertionError(
                "approved integration ID without admission evidence must be denied; "
                f"got {reason!r}"
            )

        write_gate(repo, ["docs/reports/integrations/codex-cli.md"])
        denied, reason = run(repo, "codex review")
        if denied:
            raise AssertionError(
                f"integration with ID and admission evidence was denied: {reason}"
            )

    print("Integration admission evidence fixture: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
