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


def main() -> int:
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

        default_push = "git push origin main"
        module.assert_denied(
            "default branch push",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", default_push)),
            "default_branch_push",
        )

        secret_read = "cat .env"
        module.assert_denied(
            "secret access",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", secret_read)),
            "credentials",
        )

        for command in ("rm -r src", "rm -rf src", "rm -fr src", "rm --recursive src"):
            module.assert_denied(
                f"destructive command {command}",
                module.decision(HARD_STOP, repo, module.event(repo, "Bash", command)),
                "destructive",
            )

        expired = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=1)).isoformat()
        module.write_gate(repo, expires=expired)
        module.assert_denied(
            "unapproved mutation remains blocked with expired gate",
            module.decision(HARD_STOP, repo, module.event(repo, "Bash", push_command)),
            "git_push",
        )

    print("Codex Hard Stop fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
