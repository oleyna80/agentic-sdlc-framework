#!/usr/bin/env python3
"""Positive and adversarial fixtures for repository release-state reconciliation."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate-release-state.py"

spec = importlib.util.spec_from_file_location("release_state_validator", VALIDATOR)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
ReleaseStateError = validator.ReleaseStateError

COMPLETED = "docs/plans/wb-007-agent-evaluation-trajectory-assurance.md"
ACTIVE = "docs/plans/wb-008-post-merge-ssot-release-gate.md"
CLOSEOUT = "docs/reports/closeout/wb-007-agent-evaluation-trajectory-assurance.md"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def work_block(work_block_id: str, status: str, pending: bool = False) -> str:
    current = ""
    if pending:
        current = "\n## Current State\n\n- **Review Gate:** PENDING\n- **Closeout Mode:** pending\n"
    return f"""---
schema_version: 1
artifact_type: work_block
artifact_id: {work_block_id}-fixture
status: {status}
owner_role: orchestrator
work_block_id: {work_block_id}
---

# {work_block_id}
{current}"""


def closeout(extra: str = "") -> str:
    return f"""---
schema_version: 1
artifact_type: closeout_report
artifact_id: wb-007-closeout
status: approved
owner_role: orchestrator
work_block_id: wb-007
---

# Closeout

- **Stage execution state:** completed
- **Review verdict:** READY
- **Verification verdict:** READY
- **Evaluation verdict:** READY
- **Drift verdict:** ALIGNED
- **Closeout classification:** SUCCESS
- **Task status:** completed

External GitHub pull-request state is non-normative and is read from GitHub when needed.
{extra}
"""


def registry(completed: list[str] | None = None, active: str | None = None) -> dict:
    completed = completed if completed is not None else [COMPLETED]
    return {
        "version": 11,
        "migration_state": {
            "completed_work_blocks": completed,
            "active_work_block": active,
            "planned": [],
        },
        "release_state": {
            "contract": "governance/release-state.md",
            "validator": "scripts/validate-release-state.py",
            "fixtures": "scripts/test-release-state-contracts.py",
            "latest_completed_work_block": COMPLETED,
            "closeout_report": CLOSEOUT,
            "external_vcs_state": "non_normative",
        },
    }


def project_map(completed: list[str] | None = None, active: str | None = None) -> str:
    value = {
        "completed_work_blocks": completed if completed is not None else [COMPLETED],
        "active_work_block": active,
    }
    block = yaml.safe_dump(value, sort_keys=False).rstrip()
    return f"# Project Map\n\n<!-- release-state\n{block}\n-->\n"


def populate(root: Path, reg: dict | None = None, map_text: str | None = None) -> None:
    reg = reg or registry()
    write(root / "FILE_REGISTRY.yml", yaml.safe_dump(reg, sort_keys=False))
    write(root / "PROJECT_MAP.md", map_text or project_map())
    write(root / "governance/release-state.md", "# contract\n")
    write(root / COMPLETED, work_block("wb-007", "completed"))
    write(root / CLOSEOUT, closeout())


def expect_failure(label: str, root: Path, contains: str) -> None:
    try:
        validator.validate_repository(root)
    except ReleaseStateError as exc:
        assert contains in str(exc), f"{label}: unexpected error: {exc}"
        return
    raise AssertionError(f"{label}: expected ReleaseStateError")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="release-state-valid-") as temp:
        root = Path(temp)
        populate(root)
        result = validator.validate_repository(root)
        assert result["verdict"] == "READY"
        assert result["active_work_block"] is None

    with tempfile.TemporaryDirectory(prefix="release-state-active-") as temp:
        root = Path(temp)
        populate(root, registry(active=ACTIVE), project_map(active=ACTIVE))
        write(root / ACTIVE, work_block("wb-008", "in_progress", pending=True))
        result = validator.validate_repository(root)
        assert result["active_work_block"] == ACTIVE

    with tempfile.TemporaryDirectory(prefix="release-state-fixtures-") as temp:
        root = Path(temp)
        populate(root)

        missing = copy.deepcopy(registry())
        missing["migration_state"]["completed_work_blocks"] = ["docs/plans/missing.md"]
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(missing, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map(["docs/plans/missing.md"]))
        expect_failure("missing-completed", root, "is missing")

        populate(root)
        write(root / COMPLETED, work_block("wb-007", "in_progress", pending=True))
        expect_failure("completed-status", root, "not status completed")

        populate(root)
        overlap = registry(active=COMPLETED)
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(overlap, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map(active=COMPLETED))
        expect_failure("active-completed-overlap", root, "cannot also be completed")

        populate(root)
        active_missing = registry(active=ACTIVE)
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(active_missing, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map(active=ACTIVE))
        expect_failure("active-missing", root, "active Work Block is missing")

        populate(root)
        active_completed = registry(active=ACTIVE)
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(active_completed, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map(active=ACTIVE))
        write(root / ACTIVE, work_block("wb-008", "completed"))
        expect_failure("active-completed-status", root, "requires one of")

        populate(root)
        write(root / "PROJECT_MAP.md", project_map([], None))
        expect_failure("map-completed-drift", root, "completed Work Blocks do not match")

        populate(root)
        write(root / "PROJECT_MAP.md", project_map([COMPLETED], ACTIVE))
        expect_failure("map-active-drift", root, "active Work Block does not match")

        populate(root)
        write(root / CLOSEOUT, closeout("\n- **Merge status:** not merged\n"))
        expect_failure("mutable-vcs-state", root, "mutable GitHub/VCS state")

        populate(root)
        write(
            root / CLOSEOUT,
            closeout().replace("**Verification verdict:** READY", "**Verification verdict:** PENDING"),
        )
        expect_failure("pending-closeout", root, "pending required assurance")

        populate(root)
        traversal = registry(completed=["../outside.md"])
        traversal["release_state"]["latest_completed_work_block"] = "../outside.md"
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(traversal, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map(["../outside.md"]))
        expect_failure("path-traversal", root, "escapes repository")

        populate(root)
        duplicate = registry(completed=[COMPLETED, COMPLETED])
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(duplicate, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map([COMPLETED, COMPLETED]))
        expect_failure("duplicate-completed", root, "duplicate paths")

        populate(root)
        write(root / "PROJECT_MAP.md", "# Project Map\n")
        expect_failure("missing-map-block", root, "requires one release-state comment block")

        populate(root)
        wrong_closeout = registry()
        wrong_closeout["release_state"]["external_vcs_state"] = "tracked_in_closeout"
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(wrong_closeout, sort_keys=False))
        expect_failure("vcs-boundary", root, "must be non_normative")

    print("Release-state contract fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
