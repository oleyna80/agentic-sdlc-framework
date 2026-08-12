#!/usr/bin/env python3
"""Offline fixtures for the schema v3 GitHub-capability lifecycle helper."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LIFE = ROOT / "template/.codex/scripts/lifecycle.py"


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def call(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(LIFE),
            "--root",
            str(repo),
            "--state",
            str(repo / ".agent/active-work-block.json"),
            *args,
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def blocked(repo: Path, *args: str, contains: str = "BLOCKED:") -> None:
    result = call(repo, *args)
    assert result.returncode == 2, result.stdout + result.stderr
    assert contains in result.stdout, result.stdout


def state(repo: Path) -> dict:
    return json.loads(
        (repo / ".agent/active-work-block.json").read_text(encoding="utf-8")
    )


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="codex-control-plane-v3-") as temporary:
        repo = Path(temporary) / "repo"
        repo.mkdir()
        (repo / ".agent").mkdir()
        (repo / "docs/specs").mkdir(parents=True)
        (repo / "src").mkdir()
        (repo / "tests").mkdir()
        (repo / "docs/specs/fixture.md").write_text("# Fixture\n", encoding="utf-8")
        (repo / "src/app.py").write_text("value = 1\n", encoding="utf-8")
        git(repo, "init", "-q", "-b", "feature")
        git(repo, "config", "user.email", "fixture@example.com")
        git(repo, "config", "user.name", "Fixture")
        git(repo, "add", ".")
        git(repo, "commit", "-qm", "base")
        h0 = git(repo, "rev-parse", "HEAD")

        prepared = call(repo, "prepare", "--reason", "stage-0")
        assert prepared.returncode == 0, prepared.stdout + prepared.stderr
        value = state(repo)
        assert value["schema_version"] == 3
        assert value["authority_mode"] == "github_capability"
        assert value["write_gate"] == {"status": "BLOCKED", "opened_at": None}
        assert "authorization" not in value
        assert "hard_stop_approvals" not in value

        # No signer environment, private key, detached signature, or authorization record is required.
        opened = call(
            repo,
            "open",
            "--work-block-id",
            "WB-FIXTURE",
            "--specification-path",
            "docs/specs/fixture.md",
            "--specification-revision",
            h0,
            "--write",
            "src/**",
            "--write",
            "tests/**",
            "--critic-status",
            "READY",
            "--critic-verdict",
            "APPROVE",
            "--critic-report",
            "docs/reports/critic-fixture.md",
            "--critic-isolation",
            "separate_subagent",
        )
        assert opened.returncode == 0, opened.stdout + opened.stderr
        value = state(repo)
        assert value["schema_version"] == 3
        assert value["authority_mode"] == "github_capability"
        assert value["work_block_id"] == "WB-FIXTURE"
        assert value["base_commit"] == h0
        assert value["write_gate"]["status"] == "READY"
        assert value["write_set"] == ["src/**", "tests/**"]
        assert value["critic"]["verdict"] == "APPROVE"
        assert not list(repo.glob(".agent/authorizations/*.sig"))

        # A normal source commit changes HEAD without requiring a cryptographic renew cycle.
        (repo / "src/app.py").write_text("value = 2\n", encoding="utf-8")
        git(repo, "add", "src/app.py")
        git(repo, "commit", "-qm", "normal feature commit")
        h1 = git(repo, "rev-parse", "HEAD")
        assert h1 != h0
        status = call(repo, "status")
        assert status.returncode == 0, status.stdout + status.stderr
        assert state(repo)["write_gate"]["status"] == "READY"
        assert state(repo)["base_commit"] == h0

        # Invalid scope/Critic states fail closed.
        call(repo, "prepare", "--reason", "retry")
        blocked(
            repo,
            "open",
            "--work-block-id",
            "WB-NO-WRITE",
            "--specification-path",
            "docs/specs/fixture.md",
            "--specification-revision",
            h1,
        )
        blocked(
            repo,
            "open",
            "--work-block-id",
            "WB-BAD-CRITIC",
            "--specification-path",
            "docs/specs/fixture.md",
            "--specification-revision",
            h1,
            "--write",
            "src/**",
            "--critic-status",
            "PENDING",
        )
        blocked(
            repo,
            "open",
            "--work-block-id",
            "WB-SKIPPED",
            "--specification-path",
            "docs/specs/fixture.md",
            "--specification-revision",
            h1,
            "--write",
            "src/**",
            "--critic-status",
            "SKIPPED",
        )

        opened = call(
            repo,
            "open",
            "--work-block-id",
            "WB-SKIPPED",
            "--specification-path",
            "docs/specs/fixture.md",
            "--specification-revision",
            h1,
            "--write",
            "src/**",
            "--critic-status",
            "SKIPPED",
            "--critic-skip-reason",
            "Owner selected documented degraded path",
        )
        assert opened.returncode == 0, opened.stdout + opened.stderr

        # Freeze and close preserve evidence while blocking further source work.
        current = state(repo)
        current["assurance"]["review"].update(
            status="READY",
            verdict="READY",
            report="docs/reports/review.md",
            isolation="separate_session",
        )
        current["assurance"]["verification"].update(
            status="READY",
            verdict="READY",
            report="docs/reports/verification.md",
            isolation="separate_session",
        )
        current["assurance"]["evaluation"].update(
            status="SKIPPED",
            verdict="PENDING",
            skip_reason="not required",
        )
        current["assurance"]["drift"].update(
            status="SKIPPED",
            verdict="PENDING",
            skip_reason="not required",
        )
        (repo / ".agent/active-work-block.json").write_text(
            json.dumps(current, indent=2) + "\n", encoding="utf-8"
        )
        frozen = call(repo, "freeze", "--reason", "assurance")
        assert frozen.returncode == 0, frozen.stdout + frozen.stderr
        frozen_state = state(repo)
        assert frozen_state["write_gate"]["status"] == "BLOCKED"
        assert frozen_state["assurance"]["review"]["verdict"] == "READY"

        closed = call(
            repo,
            "close",
            "--reason",
            "verified",
            "--mode",
            "success-closeout",
        )
        assert closed.returncode == 0, closed.stdout + closed.stderr
        closed_state = state(repo)
        assert closed_state["write_gate"]["status"] == "BLOCKED"
        assert closed_state["closeout_mode"] == "success-closeout"
        assert closed_state["assurance"]["verification"]["verdict"] == "READY"

    print("GitHub-capability lifecycle fixtures: OK")


if __name__ == "__main__":
    main()
