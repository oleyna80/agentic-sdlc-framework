#!/usr/bin/env python3
"""Positive and adversarial fixtures for repository release-state reconciliation."""
from __future__ import annotations

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
OLDER = "docs/plans/wb-006-bootstrap-restore-hardening.md"
ACTIVE = "docs/plans/wb-008-post-merge-ssot-release-gate.md"
CLOSEOUT = "docs/reports/closeout/wb-007-agent-evaluation-trajectory-assurance.md"
OLDER_CLOSEOUT = "docs/reports/closeout/wb-006-bootstrap-restore-hardening.md"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def work_block(
    work_block_id: str,
    status: str,
    *,
    stage: str = "completed",
    review: str = "READY",
    verification: str = "READY",
    evaluation: str | None = "READY",
    drift: str = "ALIGNED",
    closeout_mode: str = "success-closeout",
    task_status: str = "completed",
    include_terminal_section: bool = True,
) -> str:
    if status == "completed" and include_terminal_section:
        evaluation_line = (
            f"- **Evaluation Verdict:** {evaluation}\n" if evaluation is not None else ""
        )
        state = (
            "\n## Final State\n\n"
            f"- **Stage State:** {stage}\n"
            f"- **Review Gate:** {review}\n"
            f"- **Verification Verdict:** {verification}\n"
            f"{evaluation_line}"
            f"- **Drift Gate:** {drift}\n"
            f"- **Closeout Mode:** {closeout_mode}\n"
            f"- **Task Status:** {task_status}\n"
        )
    elif status == "completed":
        state = ""
    else:
        state = (
            "\n## Current State\n\n"
            "- **Stage State:** in_progress\n"
            "- **Review Gate:** PENDING\n"
            "- **Closeout Mode:** pending\n"
        )
    return f"""---
schema_version: 1
artifact_type: work_block
artifact_id: {work_block_id}-fixture
status: {status}
owner_role: orchestrator
work_block_id: {work_block_id}
---

# {work_block_id}
{state}"""


def closeout(
    extra: str = "",
    *,
    work_block_id: str = "wb-007",
    stage: str = "completed",
    review: str = "READY",
    verification: str = "READY",
    evaluation: str | None = "READY",
    drift: str = "ALIGNED",
    classification: str = "SUCCESS",
    task_status: str = "completed",
    external: str = "non-normative; read from the hosting platform when needed",
    include_residual: bool = True,
    include_follow_up: bool = True,
    frontmatter_extra: str = "",
) -> str:
    evaluation_line = (
        f"- **Evaluation verdict:** {evaluation}\n" if evaluation is not None else ""
    )
    residual = (
        "\n## Residual Risks and Limitations\n\n"
        "- Runtime and OS isolation remain outside this fixture.\n"
        if include_residual
        else ""
    )
    follow_up = (
        "\n## Follow-Up Work\n\n"
        "1. Run target-environment smoke when live runtimes are admitted.\n"
        if include_follow_up
        else ""
    )
    return f"""---
schema_version: 1
artifact_type: closeout_report
artifact_id: wb-007-closeout
status: approved
owner_role: orchestrator
work_block_id: {work_block_id}
{frontmatter_extra}---

# Closeout

- **Stage execution state:** {stage}
- **Review verdict:** {review}
- **Verification verdict:** {verification}
{evaluation_line}- **Drift verdict:** {drift}
- **Closeout classification:** {classification}
- **Task status:** {task_status}
- **External VCS state:** {external}

External GitHub pull-request state is non-normative and is read from GitHub when needed.
{extra}{residual}{follow_up}
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
            "workflow": ".github/workflows/release-state-contract.yml",
            "latest_completed_work_block": completed[-1],
            "closeout_report": CLOSEOUT,
            "external_vcs_state": "non_normative",
            "authority": "assurance_only",
        },
    }


def project_map(
    completed: list[str] | None = None,
    active: str | None = None,
    *,
    visible_override: str | None = None,
) -> str:
    completed = completed if completed is not None else [COMPLETED]
    block = yaml.safe_dump(
        {"completed_work_blocks": completed, "active_work_block": active},
        sort_keys=False,
    ).rstrip()
    if visible_override is not None:
        visible = visible_override
    elif active is None:
        visible = "## Migration Work\n\nNo active implementation Work Block.\n"
    else:
        visible = f"## Migration Work\n\nActive:\n\n- `{active}`\n"
    return f"# Project Map\n\n<!-- release-state\n{block}\n-->\n\n{visible}"


def populate(root: Path, reg: dict | None = None, map_text: str | None = None) -> None:
    write(root / "FILE_REGISTRY.yml", yaml.safe_dump(reg or registry(), sort_keys=False))
    write(root / "PROJECT_MAP.md", map_text or project_map())
    write(root / "governance/release-state.md", "# contract\n")
    write(root / "scripts/validate-release-state.py", "# validator\n")
    write(root / "scripts/test-release-state-contracts.py", "# fixtures\n")
    write(root / ".github/workflows/release-state-contract.yml", "name: fixture\n")
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
        assert validator.validate_repository(root)["verdict"] == "READY"

    with tempfile.TemporaryDirectory(prefix="release-state-clean-boundary-") as temp:
        root = Path(temp)
        populate(root)
        write(
            root / CLOSEOUT,
            closeout(external="non-normative; ownership boundary only"),
        )
        assert validator.validate_repository(root)["verdict"] == "READY"

    with tempfile.TemporaryDirectory(prefix="release-state-pr-reference-") as temp:
        root = Path(temp)
        populate(root)
        write(
            root / CLOSEOUT,
            closeout("\nPR #9 review evidence is repository-owned.\n"),
        )
        assert validator.validate_repository(root)["verdict"] == "READY"

    with tempfile.TemporaryDirectory(prefix="release-state-markdown-non-state-") as temp:
        root = Path(temp)
        populate(root)
        write(
            root / CLOSEOUT,
            closeout("\nPR #9: *review evidence* is repository-owned.\n"),
        )
        assert validator.validate_repository(root)["verdict"] == "READY"

    with tempfile.TemporaryDirectory(prefix="release-state-historical-closeout-") as temp:
        root = Path(temp)
        completed = [OLDER, COMPLETED]
        populate(root, registry(completed), project_map(completed))
        write(root / OLDER, work_block("wb-006", "completed", evaluation=None))
        write(root / OLDER_CLOSEOUT, closeout(work_block_id="wb-006", evaluation=None))
        assert validator.validate_repository(root)["verdict"] == "READY"

    with tempfile.TemporaryDirectory(prefix="release-state-skipped-") as temp:
        root = Path(temp)
        populate(root)
        write(root / COMPLETED, work_block("wb-007", "completed", evaluation="SKIPPED — deterministic"))
        write(root / CLOSEOUT, closeout(evaluation="SKIPPED — deterministic"))
        assert validator.validate_repository(root)["verdict"] == "READY"

    with tempfile.TemporaryDirectory(prefix="release-state-legacy-drift-") as temp:
        root = Path(temp)
        completed = [OLDER, COMPLETED]
        populate(root, registry(completed), project_map(completed))
        write(root / OLDER, work_block("wb-006", "completed", evaluation=None, drift="READY"))
        assert validator.validate_repository(root)["verdict"] == "READY"

    with tempfile.TemporaryDirectory(prefix="release-state-active-") as temp:
        root = Path(temp)
        populate(root, registry(active=ACTIVE), project_map(active=ACTIVE))
        write(root / ACTIVE, work_block("wb-008", "in_progress"))
        assert validator.validate_repository(root)["active_work_block"] == ACTIVE

    with tempfile.TemporaryDirectory(prefix="release-state-fixtures-") as temp:
        root = Path(temp)

        populate(root)
        missing = registry(["docs/plans/missing.md"])
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(missing, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map(["docs/plans/missing.md"]))
        expect_failure("missing-completed", root, "is missing")

        populate(root)
        write(root / COMPLETED, work_block("wb-007", "in_progress"))
        expect_failure("completed-status", root, "not status completed")

        populate(root)
        write(root / COMPLETED, work_block("wb-007", "completed", include_terminal_section=False))
        expect_failure("missing-terminal-section", root, "requires Final State or Closeout State")

        for label, kwargs, expected in (
            ("completed-pending-stage", {"stage": "in_progress"}, "stage state=completed"),
            ("completed-blocked-review", {"review": "BLOCKED"}, "review gate=READY"),
            ("completed-review-suffix", {"review": "READY — BLOCKED"}, "review gate=READY"),
            ("completed-unverified-verification", {"verification": "UNVERIFIED"}, "verification verdict=READY"),
            ("completed-drift-suffix", {"drift": "ALIGNED — MISALIGNED"}, "drift gate"),
            ("completed-misaligned-drift", {"drift": "MISALIGNED"}, "drift gate"),
            ("completed-bad-closeout", {"closeout_mode": "pending"}, "closeout mode=success-closeout"),
            ("completed-bad-task", {"task_status": "blocked"}, "task status=completed"),
            ("completed-ready-eval-suffix", {"evaluation": "READY — BLOCKED"}, "evaluation verdict"),
            ("completed-empty-skip", {"evaluation": "SKIPPED — "}, "evaluation verdict"),
        ):
            populate(root)
            write(root / COMPLETED, work_block("wb-007", "completed", **kwargs))
            expect_failure(label, root, expected)

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
        duplicate_id = registry(active=ACTIVE)
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(duplicate_id, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map(active=ACTIVE))
        write(root / ACTIVE, work_block("wb-007", "in_progress"))
        expect_failure("active-duplicate-id", root, "duplicates a completed Work Block ID")

        populate(root)
        write(root / "PROJECT_MAP.md", project_map([OLDER], None))
        expect_failure("map-completed-drift", root, "completed Work Blocks do not match")

        populate(root)
        write(root / "PROJECT_MAP.md", project_map([COMPLETED], ACTIVE))
        expect_failure("map-active-drift", root, "active Work Block does not match")

        populate(root)
        active_registry = registry(active=ACTIVE)
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(active_registry, sort_keys=False))
        write(root / ACTIVE, work_block("wb-008", "in_progress"))
        write(root / "PROJECT_MAP.md", project_map(active=ACTIVE, visible_override="## Migration Work\n\nNo active implementation Work Block.\n"))
        expect_failure("visible-active-contradiction", root, "contradicts active Work Block state")

        populate(root)
        active_registry = registry(active=ACTIVE)
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(active_registry, sort_keys=False))
        write(root / ACTIVE, work_block("wb-008", "in_progress"))
        write(
            root / "PROJECT_MAP.md",
            project_map(
                active=ACTIVE,
                visible_override=(
                    "## Migration Work\n\nNo active implementation Work Block.\n\n"
                    "## Key Paths\n\n"
                    f"- `{ACTIVE}`\n"
                ),
            ),
        )
        expect_failure("active-path-outside-migration-section", root, "contradicts active Work Block state")

        populate(root)
        write(root / "PROJECT_MAP.md", project_map(visible_override="## Migration Work\n\nCompleted only.\n"))
        expect_failure("visible-none-missing", root, "must state that no active")

        populate(root)
        write(
            root / "PROJECT_MAP.md",
            project_map(visible_override="## Migration Work\n\nPR #7 remains Draft.\nNo active implementation Work Block.\n"),
        )
        expect_failure("stale-map-pr", root, "contains stale GitHub state")

        populate(root)
        write(root / CLOSEOUT, closeout("\n- **Merge status:** not merged\n"))
        expect_failure("mutable-vcs-marker", root, "mutable GitHub/VCS state")

        for label, assertion in (
            ("mutable-pr-open", "PR #9 is open."),
            ("mutable-pr-draft", "PR #9 is Draft."),
            ("mutable-pr-merged", "PR #9 was merged."),
            ("mutable-pr-bare-open", "PR #9 open."),
            ("mutable-pr-bare-draft", "PR #9 Draft."),
            ("mutable-pr-bare-merged", "PR #9 merged."),
            ("mutable-pr-bare-ready", "PR #9 ready for review."),
            ("mutable-pull-request-bare-closed", "Pull request #9 closed."),
            ("mutable-pr-colon-open", "PR #9: open."),
            ("mutable-pr-colon-draft", "PR #9: Draft."),
            ("mutable-pr-colon-merged", "PR #9: merged."),
            ("mutable-pr-bold-colon", "**PR #9:** merged"),
            ("mutable-pr-bold-state", "**PR #9:** **merged**"),
            ("mutable-pr-italic-state", "PR #9: *merged*"),
            ("mutable-pr-combined-state", "**PR #9:** ***merged***"),
            ("mutable-pr-underscore-state", "PR #9: _open_"),
            ("mutable-pull-request-combined-underscore", "Pull request #9: ___closed___"),
            ("mutable-pr-table-bold-state", "| **PR #9** | **open** |"),
            ("mutable-pr-table", "| PR #9 | merged |"),
            ("mutable-pr-bold-table", "| **PR #9** | open |"),
        ):
            populate(root)
            write(root / CLOSEOUT, closeout(f"\n{assertion}\n"))
            expect_failure(label, root, "mutable GitHub/VCS state")

        for label, frontmatter_extra in (
            ("mutable-pr-frontmatter-prose", 'release_note: "PR #9 is merged"\n'),
            ("mutable-pr-frontmatter-key", "pr_status: merged\n"),
            ("mutable-pull-request-frontmatter-key", "pull_request_state: open\n"),
            (
                "mutable-nested-frontmatter-key",
                "hosting:\n  pull-request-status: Draft\n",
            ),
            (
                "mutable-pr-parent-status",
                "pr: {status: merged}\n",
            ),
            (
                "mutable-pull-request-parent-state",
                "pull_request: {state: open}\n",
            ),
        ):
            populate(root)
            write(root / CLOSEOUT, closeout(frontmatter_extra=frontmatter_extra))
            expect_failure(label, root, "mutable GitHub/VCS state")

        for label, kwargs, expected in (
            ("closeout-review-suffix", {"review": "READY — BLOCKED"}, "review verdict=READY"),
            ("closeout-verification-suffix", {"verification": "READY — BLOCKED"}, "verification verdict=READY"),
            ("closeout-drift-suffix", {"drift": "ALIGNED — MISALIGNED"}, "drift verdict=ALIGNED"),
            ("closeout-classification-suffix", {"classification": "SUCCESS — FAILED"}, "closeout classification=SUCCESS"),
            ("closeout-task-suffix", {"task_status": "completed — blocked"}, "task status=completed"),
            ("closeout-ready-eval-suffix", {"evaluation": "READY — BLOCKED"}, "closeout evaluation verdict"),
        ):
            populate(root)
            write(root / CLOSEOUT, closeout(**kwargs))
            expect_failure(label, root, expected)

        populate(root)
        write(root / CLOSEOUT, closeout("\n- **Verification verdict:** PENDING\n"))
        expect_failure("duplicate-closeout-marker", root, "duplicate marker: verification verdict")

        populate(root)
        write(root / CLOSEOUT, closeout(evaluation=None))
        expect_failure("required-evaluation-missing", root, "requires evaluation verdict=READY")

        populate(root)
        write(root / CLOSEOUT, closeout(evaluation="UNVERIFIED"))
        expect_failure("unverified-evaluation", root, "closeout evaluation verdict")

        populate(root)
        write(root / CLOSEOUT, closeout(external="tracked in closeout"))
        expect_failure("missing-external-boundary", root, "mark external VCS state non-normative")

        populate(root)
        write(
            root / CLOSEOUT,
            closeout(external="non-normative; current state is merged"),
        )
        expect_failure(
            "mutable-state-in-external-boundary",
            root,
            "external VCS state marker contains concrete mutable",
        )

        populate(root, registry([OLDER, COMPLETED]), project_map([OLDER, COMPLETED]))
        write(root / OLDER, work_block("wb-006", "completed", evaluation=None))
        write(
            root / OLDER_CLOSEOUT,
            closeout(work_block_id="wb-006", evaluation=None, review="BLOCKED"),
        )
        expect_failure(
            "historical-closeout-blocked-review",
            root,
            "review verdict=READY",
        )
        (root / OLDER_CLOSEOUT).unlink()

        populate(root)
        write(root / CLOSEOUT, closeout(include_residual=False))
        expect_failure("missing-residual-risks", root, "requires section: Residual Risks and Limitations")

        populate(root)
        write(root / CLOSEOUT, closeout(include_follow_up=False))
        expect_failure("missing-follow-up", root, "requires section: Follow-Up Work")

        populate(root)
        write(root / CLOSEOUT, closeout(work_block_id="wb-00"))
        expect_failure("closeout-id-substring", root, "does not exactly match")

        populate(root)
        two = registry([OLDER, COMPLETED])
        two["release_state"]["latest_completed_work_block"] = OLDER
        write(root / OLDER, work_block("wb-006", "completed", evaluation=None))
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(two, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map([OLDER, COMPLETED]))
        expect_failure("latest-not-final", root, "must be the final")

        populate(root)
        traversal = registry(["../outside.md"])
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(traversal, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map(["../outside.md"]))
        expect_failure("path-traversal", root, "escapes repository")

        populate(root)
        duplicate = registry([COMPLETED, COMPLETED])
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(duplicate, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map([COMPLETED, COMPLETED]))
        expect_failure("duplicate-completed", root, "duplicate paths")

        populate(root)
        write(root / "PROJECT_MAP.md", "# Project Map\n")
        expect_failure("missing-map-block", root, "requires one release-state comment block")

        populate(root)
        wrong_vcs = registry()
        wrong_vcs["release_state"]["external_vcs_state"] = "tracked_in_closeout"
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(wrong_vcs, sort_keys=False))
        expect_failure("vcs-boundary", root, "must be non_normative")

        populate(root)
        wrong_authority = registry()
        wrong_authority["release_state"]["authority"] = "merge_authority"
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(wrong_authority, sort_keys=False))
        expect_failure("authority-boundary", root, "must be assurance_only")

        populate(root)
        wrong_workflow = registry()
        wrong_workflow["release_state"]["workflow"] = ".github/workflows/other.yml"
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(wrong_workflow, sort_keys=False))
        expect_failure("wrong-workflow", root, "release_state.workflow must be")

        populate(root)
        (root / ".github/workflows/release-state-contract.yml").unlink()
        expect_failure("missing-workflow", root, "release-state asset is missing")

    print("Release-state contract fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
