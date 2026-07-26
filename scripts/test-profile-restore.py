#!/usr/bin/env python3
"""Verify portable profile state survives Git while local operational state restores safely."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "bootstrap.sh"
BASH = os.environ.get("BASH", "bash")
MEMORY_FILES = (
    "context.md",
    "progress.md",
    "decisions.md",
    "orchestrator-log.md",
    "review-log.md",
    "external-team-log.md",
)
CANONICAL_COORDINATION_WRITE_SET = [
    ".agent/active-work-block.json",
    ".agent/critic-gate.md",
    ".agent/verification-gate.md",
    "docs/plans/**",
    "docs/specs/**",
    "docs/tasklist/**",
    "docs/reports/**",
    "docs/architecture/drafts/**",
    "memory_bank/**",
]


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
    )


def check_ignored(project: Path, relative: str) -> bool:
    result = run(
        ["git", "check-ignore", "-q", "--no-index", "--", relative],
        project,
        check=False,
    )
    if result.returncode not in {0, 1}:
        raise AssertionError(
            f"git check-ignore failed for {relative}: {result.stderr.strip()}"
        )
    return result.returncode == 0


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def assert_corrupt_coordination_restore_fails(
    project: Path, coordination_write_set: object
) -> None:
    active_path = project / ".agent/active-work-block.json"
    if active_path.exists():
        active_path.unlink()
    default_path = project / ".agent/active-work-block.default.json"
    default_gate = load_json(default_path)
    default_gate["coordination_write_set"] = coordination_write_set
    write_json(default_path, default_gate)

    result = run([BASH, "scripts/bootstrap.sh"], project, check=False)
    assert result.returncode != 0
    assert "coordination_write_set" in result.stderr
    assert not active_path.exists()


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="profile-restore-") as temp:
        project = Path(temp) / "project"
        run(
            [
                BASH,
                str(BOOTSTRAP),
                "--profile",
                "core",
                str(project),
                "Restore Contract",
                "restore-contract",
            ],
            ROOT,
        )

        portable = (
            ".agent/bootstrap-profile.json",
            ".agent/active-work-block.default.json",
            ".agent/ROSTER.md",
            ".agent/hooks/hard_stop_policy.py",
            ".agent/workflows/sdd-protocol.md",
            "scripts/bootstrap.sh",
            "scripts/validate-installation-profile.py",
        )
        for relative in portable:
            assert (project / relative).is_file(), f"missing portable path: {relative}"

        run(["git", "init", "-q"], project)
        # Ignore any runner/user global exclude file so this fixture evaluates the
        # generated project contract only.
        run(["git", "config", "core.excludesFile", "/dev/null"], project)
        for relative in portable:
            assert not check_ignored(project, relative), f"portable path ignored: {relative}"

        local_state = (
            ".agent/active-work-block.json",
            ".agent/project-config.md",
            "memory_bank/context.md",
        )
        for relative in local_state:
            assert check_ignored(project, relative), f"local path is not ignored: {relative}"

        default_gate = load_json(project / ".agent/active-work-block.default.json")
        active_gate = load_json(project / ".agent/active-work-block.json")
        assert active_gate == default_gate
        assert active_gate["write_gate"]["status"] == "BLOCKED"
        assert active_gate["integrations"]["approved"] == []
        assert (
            active_gate["coordination_write_set"]
            == CANONICAL_COORDINATION_WRITE_SET
        )
        assert active_gate["hard_stop_approvals"] == {
            "git_commit": False,
            "git_push": False,
            "default_branch_push": False,
            "destructive": False,
            "live_infra": False,
            "live_data": False,
            "credentials": False,
            "client_communications": False,
        }

        # Simulate clone/restore: ignored operational state is absent, while
        # committed portable files remain.
        (project / ".agent/active-work-block.json").unlink()
        (project / ".agent/project-config.md").unlink()
        shutil.rmtree(project / "memory_bank")

        result = run([BASH, "scripts/bootstrap.sh"], project)
        assert "RESTORED: .agent/active-work-block.json" in result.stdout
        assert "Installation profile: OK" in result.stdout
        assert "Agentic SDLC layer: OK" in result.stdout

        restored_gate = load_json(project / ".agent/active-work-block.json")
        assert restored_gate == default_gate
        assert restored_gate["write_gate"]["status"] == "BLOCKED"
        assert (
            restored_gate["coordination_write_set"]
            == CANONICAL_COORDINATION_WRITE_SET
        )

        for filename in MEMORY_FILES:
            path = project / "memory_bank" / filename
            assert path.is_file(), f"missing restored memory file: {filename}"
        assert (project / "memory_bank/snapshots/.gitkeep").is_file()
        assert (project / ".agent/project-config.md").is_file()

        # A second health check is idempotent and must not replace an active gate.
        restored_gate["work_block_id"] = "wb-local-restore-test"
        restored_gate["write_gate"]["status"] = "BLOCKED"
        (project / ".agent/active-work-block.json").write_text(
            json.dumps(restored_gate, indent=2) + "\n", encoding="utf-8"
        )
        run([BASH, "scripts/bootstrap.sh"], project)
        after_second_run = load_json(project / ".agent/active-work-block.json")
        assert after_second_run["work_block_id"] == "wb-local-restore-test"
        assert after_second_run["write_gate"]["status"] == "BLOCKED"

    with tempfile.TemporaryDirectory(prefix="profile-restore-corrupt-") as temp:
        project = Path(temp) / "project"
        run(
            [
                BASH,
                str(BOOTSTRAP),
                "--profile",
                "core",
                str(project),
                "Corrupt Restore Contract",
                "corrupt-restore-contract",
            ],
            ROOT,
        )
        (project / ".agent/active-work-block.json").unlink()
        default_path = project / ".agent/active-work-block.default.json"
        default_gate = load_json(default_path)
        default_gate["write_gate"]["status"] = "READY"
        default_gate["write_set"] = ["src/**"]
        default_gate["integrations"]["approved"] = ["codex-cli"]
        default_gate["hard_stop_approvals"]["git_push"] = True
        write_json(default_path, default_gate)

        result = run([BASH, "scripts/bootstrap.sh"], project, check=False)
        assert result.returncode != 0
        assert "write_gate.status must be BLOCKED" in result.stderr
        assert not (project / ".agent/active-work-block.json").exists()

    corrupt_coordination_cases = {
        "broad-glob": ["**"],
        "source-glob": CANONICAL_COORDINATION_WRITE_SET + ["src/**"],
        "repository-root": ["."],
        "absolute-path": ["/tmp/source.py"],
        "traversal-path": ["../source.py"],
        "missing-path": CANONICAL_COORDINATION_WRITE_SET[:-1],
        "additional-path": CANONICAL_COORDINATION_WRITE_SET + ["src/app.py"],
        "reordered-paths": list(reversed(CANONICAL_COORDINATION_WRITE_SET)),
        "non-string-path": CANONICAL_COORDINATION_WRITE_SET[:-1] + [42],
        "malformed-path": CANONICAL_COORDINATION_WRITE_SET[:-1] + [""],
    }
    with tempfile.TemporaryDirectory(prefix="profile-restore-coordination-") as temp:
        seed_project = Path(temp) / "seed"
        run(
            [
                BASH,
                str(BOOTSTRAP),
                "--profile",
                "core",
                str(seed_project),
                "Coordination Restore Contract",
                "coordination-restore-contract",
            ],
            ROOT,
        )
        for name, coordination_write_set in corrupt_coordination_cases.items():
            project = Path(temp) / name
            shutil.copytree(seed_project, project)
            assert_corrupt_coordination_restore_fails(
                project, coordination_write_set
            )

    print("Profile clone/restore contract: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
