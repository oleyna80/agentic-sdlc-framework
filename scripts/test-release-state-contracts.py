#!/usr/bin/env python3
"""Positive and adversarial fixtures for repository release-state reconciliation."""
from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path
import subprocess
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
TASKLIST = "docs/tasklist/wb-007-agent-evaluation-trajectory-assurance.md"
SPECIFICATION = "docs/specs/wb-007-agent-evaluation-trajectory-assurance.md"
CLOSEOUT = "docs/reports/closeout/wb-007-agent-evaluation-trajectory-assurance.md"
OLDER_CLOSEOUT = "docs/reports/closeout/wb-006-bootstrap-restore-hardening.md"
CANDIDATE = "docs/plans/wb-008-pre-closeout-candidate.md"
CANDIDATE_ID = "WB-008"
CANDIDATE_TASKLIST = "docs/tasklist/wb-008-pre-closeout-candidate.md"
CANDIDATE_SPECIFICATION = "docs/specs/wb-008-pre-closeout-candidate.md"
CANDIDATE_EVIDENCE = {
    "review": "docs/reports/reviews/wb-008-pre-closeout-candidate.md",
    "verification": "docs/reports/verification/wb-008-pre-closeout-candidate.md",
    "drift": "docs/reports/drift/wb-008-pre-closeout-candidate.md",
    "closeout": "docs/reports/closeout/wb-008-pre-closeout-candidate.md",
}


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
    governance_profile: str | None = "Managed",
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
    profile_line = (
        f"governance_profile: {governance_profile}\n" if governance_profile is not None else ""
    )
    return f"""---
schema_version: 1
artifact_type: work_block
artifact_id: {work_block_id}-fixture
status: {status}
owner_role: orchestrator
work_block_id: {work_block_id}
{profile_line}---

# {work_block_id}
{state}"""


def tasklist(
    work_block_id: str = "wb-007",
    specification: str | None = None,
    *,
    artifact_type: str = "tasklist",
    recorded_work_block_id: str | None = None,
    extra_frontmatter: str = "",
) -> str:
    specification_line = (
        f"specification: {specification}\n" if specification is not None else ""
    )
    return f"""---
schema_version: 1
artifact_type: {artifact_type}
work_block_id: {recorded_work_block_id or work_block_id}
{specification_line}{extra_frontmatter}---

# {work_block_id} tasklist
"""


def specification(
    work_block_id: str = "wb-007", *, status: str = "approved", artifact_type: str = "specification"
) -> str:
    return f"""---
schema_version: 1
artifact_type: {artifact_type}
work_block_id: {work_block_id}
status: {status}
---

# {work_block_id} specification
"""


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
    candidate: dict | None = None,
    visible_override: str | None = None,
) -> str:
    completed = completed if completed is not None else [COMPLETED]
    state = {"completed_work_blocks": completed, "active_work_block": active}
    if candidate is not None:
        state["pre_closeout_candidate"] = candidate
    block = yaml.safe_dump(state, sort_keys=False).rstrip()
    if visible_override is not None:
        visible = visible_override
    elif active is None:
        visible = "## Migration Work\n\nNo active implementation Work Block.\n"
    else:
        visible = f"## Migration Work\n\nActive:\n\n- `{active}`\n"
    return f"# Project Map\n\n<!-- release-state\n{block}\n-->\n\n{visible}"


def candidate_work_block() -> str:
    return f"""---
schema_version: 1
artifact_type: work_block
artifact_id: wb-008-pre-closeout-candidate
status: closeout_candidate
owner_role: orchestrator
work_block_id: {CANDIDATE_ID}
governance_profile: Managed
---

# {CANDIDATE_ID}

## Current State

- **Current Stage:** Close
- **Stage State:** assurance_pending
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Drift Gate:** PENDING
- **Closeout Mode:** candidate
"""


def candidate_declaration() -> dict:
    return {
        "work_block": CANDIDATE,
        "work_block_id": CANDIDATE_ID,
        "predecessor_completed_work_block": COMPLETED,
        "state": "assurance_pending",
        "required_evidence": CANDIDATE_EVIDENCE.copy(),
        "normative_manifest": [CANDIDATE, "FILE_REGISTRY.yml", "PROJECT_MAP.md"],
    }


def candidate_evidence(kind: str, subject_commit: str) -> str:
    artifact_type = validator.CANDIDATE_EVIDENCE_TYPES[kind]
    if kind == "closeout":
        return closeout(
            work_block_id=CANDIDATE_ID,
            frontmatter_extra=f"subject_commit: {subject_commit}\n",
        )
    return f"""---
schema_version: 1
artifact_type: {artifact_type}
artifact_id: wb-008-{kind}
status: approved
work_block_id: {CANDIDATE_ID}
subject_commit: {subject_commit}
verdict: {validator.CANDIDATE_EVIDENCE_VERDICTS[kind]}
---

# {kind}
"""


def populate_candidate(root: Path) -> dict:
    declaration = candidate_declaration()
    candidate_registry = registry()
    candidate_registry["migration_state"]["pre_closeout_candidate"] = declaration
    candidate_map = project_map(
        candidate=declaration,
        visible_override=(
            "## Migration Work\n\nNo active implementation Work Block.\n\n"
            "Closeout candidate:\n\n"
            f"- `{CANDIDATE}`\n"
        ),
    )
    populate(root, candidate_registry, candidate_map)
    write(root / CANDIDATE, candidate_work_block())
    return declaration


def populate_formal_candidate(root: Path, *, specification_status: str = "approved") -> dict:
    declaration = populate_candidate(root)
    write(
        root / CANDIDATE_TASKLIST,
        tasklist(work_block_id=CANDIDATE_ID, specification=CANDIDATE_SPECIFICATION),
    )
    write(
        root / CANDIDATE_SPECIFICATION,
        specification(work_block_id=CANDIDATE_ID, status=specification_status),
    )
    return declaration


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args], check=True, capture_output=True, text=True
    )
    return result.stdout.strip()


def populate(root: Path, reg: dict | None = None, map_text: str | None = None) -> None:
    write(root / "FILE_REGISTRY.yml", yaml.safe_dump(reg or registry(), sort_keys=False))
    write(root / "PROJECT_MAP.md", map_text or project_map())
    write(root / "governance/release-state.md", "# contract\n")
    write(root / "scripts/validate-release-state.py", "# validator\n")
    write(root / "scripts/test-release-state-contracts.py", "# fixtures\n")
    write(root / ".github/workflows/release-state-contract.yml", "name: fixture\n")
    write(root / COMPLETED, work_block("wb-007", "completed"))
    write(root / TASKLIST, tasklist())
    write(root / CLOSEOUT, closeout())


def expect_failure(label: str, root: Path, contains: str) -> None:
    try:
        validator.validate_repository(root)
    except ReleaseStateError as exc:
        assert contains in str(exc), f"{label}: unexpected error: {exc}"
        return
    raise AssertionError(f"{label}: expected ReleaseStateError")


def assert_checkout_history(
    workflow: object, *, workflow_name: str, job_name: str
) -> None:
    """Require full history on one named ancestry-validator CI consumer."""
    if not isinstance(workflow, dict):
        raise AssertionError(f"{workflow_name} workflow must be a mapping")
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        raise AssertionError(f"{workflow_name} workflow must define jobs")
    job = jobs.get(job_name)
    if not isinstance(job, dict):
        raise AssertionError(f"{workflow_name} workflow must define the {job_name} job")
    steps = job.get("steps")
    if not isinstance(steps, list):
        raise AssertionError(f"{workflow_name}/{job_name} must define steps")
    checkout_steps = [
        step
        for step in steps
        if isinstance(step, dict) and step.get("uses") == "actions/checkout@v4"
    ]
    if len(checkout_steps) != 1:
        raise AssertionError(f"{workflow_name}/{job_name} must have exactly one checkout step")
    checkout_with = checkout_steps[0].get("with")
    if not isinstance(checkout_with, dict) or checkout_with.get("fetch-depth") != 0:
        raise AssertionError(f"{workflow_name}/{job_name} checkout must set fetch-depth: 0")


def assert_canonical_ancestry_consumer_history() -> None:
    """Prove each known direct CI consumer rejects shallow checkout history."""
    consumers = (
        ("release-state-contract", ".github/workflows/release-state-contract.yml", "release-state"),
        ("framework-contracts", ".github/workflows/framework-contracts.yml", "contracts"),
    )
    for workflow_name, relative_path, job_name in consumers:
        workflow = yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))
        assert_checkout_history(workflow, workflow_name=workflow_name, job_name=job_name)

        def checkout_step(candidate: dict) -> dict:
            steps = candidate["jobs"][job_name]["steps"]
            return next(step for step in steps if step.get("uses") == "actions/checkout@v4")

        absent = deepcopy(workflow)
        checkout_step(absent)["with"].pop("fetch-depth")

        shallow = deepcopy(workflow)
        checkout_step(shallow)["with"]["fetch-depth"] = 1

        misplaced = deepcopy(workflow)
        checkout_step(misplaced)["with"].pop("fetch-depth")
        setup = next(
            step
            for step in misplaced["jobs"][job_name]["steps"]
            if step.get("uses") == "actions/setup-python@v5"
        )
        setup.setdefault("with", {})["fetch-depth"] = 0

        for label, candidate in (
            ("absent", absent),
            ("shallow", shallow),
            ("misplaced", misplaced),
        ):
            try:
                assert_checkout_history(
                    candidate, workflow_name=workflow_name, job_name=job_name
                )
            except AssertionError:
                continue
            raise AssertionError(
                f"{workflow_name}/{job_name} accepted {label} checkout depth"
            )


def main() -> int:
    assert_canonical_ancestry_consumer_history()

    with tempfile.TemporaryDirectory(prefix="release-state-valid-") as temp:
        root = Path(temp)
        populate(root)
        assert validator.validate_repository(root)["verdict"] == "READY"

    with tempfile.TemporaryDirectory(prefix="release-state-formal-spec-approved-") as temp:
        root = Path(temp)
        populate(root)
        write(root / TASKLIST, tasklist(specification=SPECIFICATION))
        write(root / SPECIFICATION, specification())
        assert validator.validate_repository(root)["verdict"] == "READY"

    with tempfile.TemporaryDirectory(prefix="release-state-formal-spec-fixtures-") as temp:
        root = Path(temp)

        populate(root)
        (root / TASKLIST).unlink()
        expect_failure("formal-spec-missing-tasklist", root, "requires sibling tasklist")

        populate(root)
        write(root / TASKLIST, tasklist(specification=SPECIFICATION))
        write(root / SPECIFICATION, specification(status="draft"))
        expect_failure("formal-spec-draft", root, "must be status approved")

        populate(root)
        write(
            root / TASKLIST,
            f"""---
{{schema_version: 1, artifact_type: tasklist, work_block_id: wb-007, specification: {SPECIFICATION}}}
---

# wb-007 tasklist
""",
        )
        write(root / SPECIFICATION, specification(status="draft"))
        expect_failure("formal-spec-flow-map-binding", root, "must be status approved")

        populate(root)
        write(
            root / TASKLIST,
            f"""---
schema_version: 1
artifact_type: tasklist
work_block_id: wb-007
? specification
: {SPECIFICATION}
---

# wb-007 tasklist
""",
        )
        write(root / SPECIFICATION, specification(status="draft"))
        expect_failure("formal-spec-explicit-key-binding", root, "must be status approved")

        populate(root)
        write(root / TASKLIST, tasklist(specification="../outside.md"))
        expect_failure("formal-spec-path-traversal", root, "escapes repository")

        populate(root)
        write(root / TASKLIST, tasklist(specification=""))
        expect_failure("formal-spec-empty", root, "must be a non-empty")

        populate(root)
        write(
            root / TASKLIST,
            tasklist(extra_frontmatter="specification:\n  - docs/specs/example.md\n"),
        )
        expect_failure("formal-spec-malformed", root, "must be a non-empty")

        populate(root)
        write(
            root / TASKLIST,
            tasklist(specification=SPECIFICATION, artifact_type="specification"),
        )
        expect_failure("formal-spec-tasklist-type", root, "sibling is not a tasklist")

        populate(root)
        write(
            root / TASKLIST,
            tasklist(specification=SPECIFICATION, recorded_work_block_id="wb-else"),
        )
        expect_failure("formal-spec-tasklist-id", root, "tasklist work_block_id does not match")

        populate(root)
        write(root / TASKLIST, tasklist(specification="docs/specs/missing.md"))
        expect_failure("formal-spec-missing-target", root, "specification is missing")

        populate(root)
        write(root / TASKLIST, tasklist(specification=SPECIFICATION))
        write(root / SPECIFICATION, specification(artifact_type="work_block"))
        expect_failure("formal-spec-wrong-type", root, "target is not a specification")

        populate(root)
        write(root / TASKLIST, tasklist(specification=SPECIFICATION))
        write(root / SPECIFICATION, specification(work_block_id="wb-else"))
        expect_failure("formal-spec-wrong-id", root, "work_block_id does not match")

        populate(root)
        write(
            root / TASKLIST,
            tasklist(
                specification=SPECIFICATION,
                extra_frontmatter=f"specification: {SPECIFICATION}\n",
            ),
        )
        expect_failure("formal-spec-duplicate-field", root, "duplicate specification fields")

        populate(root)
        write(
            root / TASKLIST,
            f"""---
{{schema_version: 1, artifact_type: tasklist, work_block_id: wb-007, specification: {SPECIFICATION}, specification: {SPECIFICATION}}}
---

# wb-007 tasklist
""",
        )
        expect_failure(
            "formal-spec-flow-map-duplicate-field",
            root,
            "duplicate specification fields",
        )

        populate(root)
        write(
            root / TASKLIST,
            f"""---
schema_version: 1
artifact_type: tasklist
work_block_id: wb-007
? specification
: {SPECIFICATION}
? specification
: {SPECIFICATION}
---

# wb-007 tasklist
""",
        )
        expect_failure(
            "formal-spec-explicit-key-duplicate-field",
            root,
            "duplicate specification fields",
        )

        populate(root)
        write(
            root / TASKLIST,
            f"""---
schema_version: 1
artifact_type: tasklist
work_block_id: wb-007
<<: {{specification: {SPECIFICATION}}}
---

# wb-007 tasklist
""",
        )
        write(root / SPECIFICATION, specification(status="draft"))
        expect_failure("formal-spec-merge-key-binding", root, "must be status approved")

        populate(root)
        write(
            root / TASKLIST,
            f"""---
schema_version: 1
artifact_type: tasklist
work_block_id: wb-007
<<: {{specification: {SPECIFICATION}}}
specification: {SPECIFICATION}
---

# wb-007 tasklist
""",
        )
        expect_failure(
            "formal-spec-direct-and-merge-duplicate-field",
            root,
            "duplicate specification fields",
        )

        populate(root)
        write(
            root / TASKLIST,
            f"""---
schema_version: 1
artifact_type: tasklist
work_block_id: wb-007
<<:
  - {{specification: {SPECIFICATION}}}
  - {{specification: {SPECIFICATION}}}
---

# wb-007 tasklist
""",
        )
        expect_failure(
            "formal-spec-multiple-merge-duplicate-field",
            root,
            "duplicate specification fields",
        )

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
            ("mutable-merge-status-open", "- **Merge status:** open"),
            ("mutable-merge-status-plain-open", "- Merge status: open"),
            ("mutable-merged-at", "merged_at: 2026-07-27T19:45:39Z"),
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
        duplicate_closeout = "docs/reports/closeout/wb-007-duplicate.md"
        write(root / duplicate_closeout, closeout())
        expect_failure(
            "canonical-plus-additional-closeout",
            root,
            "multiple closeout reports",
        )
        (root / duplicate_closeout).unlink()

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

    with tempfile.TemporaryDirectory(prefix="release-state-candidate-") as temp:
        root = Path(temp)
        declaration = populate_candidate(root)
        result = validator.validate_repository(root, candidate_mode=True)
        assert result["verdict"] == "CANDIDATE_READY"
        assert result["candidate_work_block"] == CANDIDATE
        cli = subprocess.run(
            ["python3", str(VALIDATOR), "--root", str(root), "--pre-closeout-candidate"],
            check=False,
            capture_output=True,
            text=True,
        )
        assert cli.returncode == 0 and "Release-state contract: CANDIDATE_READY" in cli.stdout
        expect_failure("candidate-default-missing-evidence", root, "requires review evidence")

        malformed = registry()
        malformed["migration_state"]["pre_closeout_candidate"] = []
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(malformed, sort_keys=False))
        expect_failure("candidate-malformed", root, "must be an object or null")

        declaration = populate_candidate(root)
        registry_text = (root / "FILE_REGISTRY.yml").read_text(encoding="utf-8")
        write(
            root / "FILE_REGISTRY.yml",
            registry_text.replace(
                "  pre_closeout_candidate:",
                "  pre_closeout_candidate: null\n  pre_closeout_candidate:",
                1,
            ),
        )
        expect_failure("candidate-duplicate", root, "duplicate pre_closeout_candidate")

        declaration = populate_candidate(root)
        declaration["predecessor_completed_work_block"] = OLDER
        candidate_registry = registry()
        candidate_registry["migration_state"]["pre_closeout_candidate"] = declaration
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(candidate_registry, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map(candidate=declaration, visible_override=(
            "## Migration Work\n\nNo active implementation Work Block.\n\n"
            f"Closeout candidate:\n\n- `{CANDIDATE}`\n"
        )))
        expect_failure("candidate-wrong-predecessor", root, "must be the raw latest")

        declaration = populate_candidate(root)
        write(root / "PROJECT_MAP.md", project_map())
        expect_failure("candidate-map-disagreement", root, "does not match FILE_REGISTRY")

        declaration = populate_candidate(root)
        write(root / CANDIDATE, candidate_work_block().replace("**Review Gate:** PENDING", "**Review Gate:** READY"))
        expect_failure("candidate-prohibited-ready", root, "requires review gate=PENDING")

        declaration = populate_candidate(root)
        write(
            root / CANDIDATE,
            candidate_work_block().replace(
                "**Verification Verdict:** PENDING",
                "**Verification Verdict:** READY — wrapped final claim",
            ),
        )
        expect_failure("candidate-prohibited-ready-suffix", root, "requires verification verdict=PENDING")

        declaration = populate_candidate(root)
        write(root / CANDIDATE, candidate_work_block() + "\n## Final State\n\n- **Review Gate:** READY\n")
        expect_failure("candidate-terminal-state-section", root, "must not contain a terminal state section")

        declaration = populate_candidate(root)
        declaration["required_evidence"]["review"] = "docs/reports/reviews/not-markdown.txt"
        candidate_registry = registry()
        candidate_registry["migration_state"]["pre_closeout_candidate"] = declaration
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(candidate_registry, sort_keys=False))
        write(root / "PROJECT_MAP.md", project_map(candidate=declaration, visible_override=(
            "## Migration Work\n\nNo active implementation Work Block.\n\n"
            f"Closeout candidate:\n\n- `{CANDIDATE}`\n"
        )))
        expect_failure("candidate-bad-evidence-path", root, "must be under")

        declaration = populate_candidate(root)
        candidate_registry = registry(active=ACTIVE)
        candidate_registry["migration_state"]["pre_closeout_candidate"] = declaration
        write(root / "FILE_REGISTRY.yml", yaml.safe_dump(candidate_registry, sort_keys=False))
        write(
            root / "PROJECT_MAP.md",
            project_map(
                active=ACTIVE,
                candidate=declaration,
                visible_override=(
                    "## Migration Work\n\nActive:\n\n"
                    f"- `{ACTIVE}`\n\n"
                    "Closeout candidate:\n\n"
                    f"- `{CANDIDATE}`\n"
                ),
            ),
        )
        write(root / ACTIVE, work_block("wb-009", "in_progress"))
        expect_failure(
            "candidate-active-ordinary",
            root,
            "pre_closeout_candidate requires active_work_block to be null",
        )
        try:
            validator.validate_repository(root, candidate_mode=True)
        except ReleaseStateError as exc:
            assert "pre_closeout_candidate requires active_work_block to be null" in str(exc)
        else:
            raise AssertionError("candidate mode accepted an active work block")

    with tempfile.TemporaryDirectory(prefix="release-state-evidence-persistence-") as temp:
        root = Path(temp)
        populate_candidate(root)
        git(root, "init", "-q")
        git(root, "config", "user.email", "fixtures@example.test")
        git(root, "config", "user.name", "Fixture")
        primary_branch = git(root, "branch", "--show-current")
        git(root, "add", ".")
        git(root, "commit", "-qm", "candidate")
        candidate_sha = git(root, "rev-parse", "HEAD")
        for evidence_class, relative in CANDIDATE_EVIDENCE.items():
            write(root / relative, candidate_evidence(evidence_class, candidate_sha))
        git(root, "add", ".")
        git(root, "commit", "-qm", "evidence")
        evidence_sha = git(root, "rev-parse", "HEAD")
        result = validator.validate_evidence_persistence(root, candidate_sha, evidence_sha)
        assert result["candidate_revision"] == candidate_sha
        ordinary_result = validator.validate_repository(root)
        assert ordinary_result["effective_completed_candidate"] == CANDIDATE
        assert ordinary_result["effective_completed_work_blocks"] == [COMPLETED, CANDIDATE]
        assert ordinary_result["effective_latest_completed_work_block"] == CANDIDATE

        git(root, "checkout", "-qb", "merge-integration", candidate_sha)
        write(root / "integration.md", "integration parent\n")
        git(root, "add", ".")
        git(root, "commit", "-qm", "integration parent")
        git(root, "merge", "--no-ff", primary_branch, "-m", "merge evidence")
        merged_result = validator.validate_repository(root)
        assert merged_result["effective_latest_completed_work_block"] == CANDIDATE
        git(root, "checkout", "-q", primary_branch)

        git(root, "checkout", "-qb", "post-evidence-normative-mutation", evidence_sha)
        write(root / CANDIDATE, candidate_work_block() + "\nPost-evidence mutation.\n")
        git(root, "add", ".")
        git(root, "commit", "-qm", "post-evidence normative mutation")
        expect_failure(
            "post-evidence-normative-mutation",
            root,
            "current HEAD differs from persisted candidate normative manifest",
        )
        git(root, "checkout", "-q", primary_branch)

        git(root, "checkout", "-qb", "post-evidence-normative-side", evidence_sha)
        write(root / CANDIDATE, candidate_work_block() + "\nMerge-side mutation.\n")
        git(root, "add", ".")
        git(root, "commit", "-qm", "merge-side normative mutation")
        git(root, "checkout", "-qb", "post-evidence-normative-merge", evidence_sha)
        write(root / "integration.md", "integration parent\n")
        git(root, "add", ".")
        git(root, "commit", "-qm", "integration parent")
        git(root, "merge", "--no-ff", "post-evidence-normative-side", "-m", "merge normative mutation")
        expect_failure(
            "post-evidence-normative-merge",
            root,
            "current HEAD differs from persisted candidate normative manifest",
        )
        git(root, "checkout", "-q", primary_branch)

        git(root, "checkout", "-qb", "negative-verdict", candidate_sha)
        for evidence_class, relative in CANDIDATE_EVIDENCE.items():
            evidence = candidate_evidence(evidence_class, candidate_sha)
            if evidence_class == "review":
                evidence = evidence.replace("verdict: READY", "verdict: CHANGES_REQUIRED")
            write(root / relative, evidence)
        git(root, "add", ".")
        git(root, "commit", "-qm", "negative review evidence")
        expect_failure("candidate-negative-review-verdict", root, "requires verdict=READY")
        git(root, "checkout", "-q", primary_branch)

        git(root, "checkout", "-qb", "wrong-subject", candidate_sha)
        wrong_subject = "f" * 40
        for evidence_class, relative in CANDIDATE_EVIDENCE.items():
            write(root / relative, candidate_evidence(evidence_class, wrong_subject))
        git(root, "add", ".")
        git(root, "commit", "-qm", "wrong subject evidence")
        expect_failure(
            "candidate-wrong-subject-evidence",
            root,
            "requires exactly one persisted evidence-only transition",
        )
        git(root, "checkout", "-q", primary_branch)

        unrelated_tree = git(root, "rev-parse", f"{evidence_sha}^{{tree}}")
        unrelated_sha = git(root, "commit-tree", unrelated_tree, "-m", "unrelated evidence tree")
        try:
            validator.validate_evidence_persistence(root, candidate_sha, unrelated_sha)
        except ReleaseStateError as exc:
            assert "must directly descend from candidate revision" in str(exc)
        else:
            raise AssertionError("candidate persistence accepted a non-descendant evidence revision")

        git(root, "checkout", "-qb", "normative-mutation", candidate_sha)
        for evidence_class, relative in CANDIDATE_EVIDENCE.items():
            write(root / relative, candidate_evidence(evidence_class, candidate_sha))
        write(root / CANDIDATE, candidate_work_block() + "\nCandidate mutation.\n")
        git(root, "add", ".")
        git(root, "commit", "-qm", "forbidden normative change")
        mutated_sha = git(root, "rev-parse", "HEAD")
        try:
            validator.validate_evidence_persistence(root, candidate_sha, mutated_sha)
        except ReleaseStateError as exc:
            assert "exactly the declared evidence manifest" in str(exc)
        else:
            raise AssertionError("candidate persistence accepted a normative mutation")

    with tempfile.TemporaryDirectory(prefix="release-state-effective-candidate-formal-spec-") as temp:
        root = Path(temp)
        populate_formal_candidate(root)
        git(root, "init", "-q")
        git(root, "config", "user.email", "fixtures@example.test")
        git(root, "config", "user.name", "Fixture")
        git(root, "add", ".")
        git(root, "commit", "-qm", "formal candidate")
        candidate_sha = git(root, "rev-parse", "HEAD")
        candidate_result = validator.validate_repository(root, candidate_mode=True)
        assert candidate_result["verdict"] == "CANDIDATE_READY"
        write(
            root / CANDIDATE_SPECIFICATION,
            specification(work_block_id=CANDIDATE_ID, status="draft"),
        )
        try:
            validator.validate_repository(root, candidate_mode=True)
        except ReleaseStateError as exc:
            assert "specification must be status approved" in str(exc)
        else:
            raise AssertionError("candidate mode accepted a draft formal specification")
        write(
            root / CANDIDATE_SPECIFICATION,
            specification(work_block_id=CANDIDATE_ID, status="approved"),
        )
        for evidence_class, relative in CANDIDATE_EVIDENCE.items():
            write(root / relative, candidate_evidence(evidence_class, candidate_sha))
        git(root, "add", ".")
        git(root, "commit", "-qm", "candidate evidence")
        ready_result = validator.validate_repository(root)
        assert ready_result["effective_latest_completed_work_block"] == CANDIDATE
        write(
            root / CANDIDATE_SPECIFICATION,
            specification(work_block_id=CANDIDATE_ID, status="draft"),
        )
        git(root, "add", ".")
        git(root, "commit", "-qm", "candidate formal specification regresses")
        expect_failure(
            "effective-candidate-formal-spec-draft",
            root,
            "specification must be status approved",
        )

    print("Release-state contract fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
