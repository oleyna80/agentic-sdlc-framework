#!/usr/bin/env python3
"""Deterministic fixtures for validate-define-traceability.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate-define-traceability.py"
TEMPLATE_VALIDATOR_PATH = ROOT / "template" / "scripts" / "validate-define-traceability.py"

spec = importlib.util.spec_from_file_location("define_traceability", VALIDATOR_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


def run_case(spec_text: str, tasks_text: str) -> dict[str, object]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        spec_path = root / "spec.md"
        tasks_path = root / "tasks.md"
        spec_path.write_text(spec_text, encoding="utf-8")
        tasks_path.write_text(tasks_text, encoding="utf-8")
        return validator.validate(spec_path, tasks_path)


def require_verdict(name: str, result: dict[str, object], expected: str) -> None:
    actual = result["verdict"]
    if actual != expected:
        raise AssertionError(f"{name}: expected {expected}, got {actual}: {result}")


def require_error(name: str, result: dict[str, object], fragment: str) -> None:
    errors = [str(value) for value in result.get("errors", [])]
    if not any(fragment.lower() in error.lower() for error in errors):
        raise AssertionError(f"{name}: missing error containing {fragment!r}: {errors}")


def require_template_parity() -> None:
    framework_source = VALIDATOR_PATH.read_text(encoding="utf-8")
    template_source = TEMPLATE_VALIDATOR_PATH.read_text(encoding="utf-8")
    if framework_source != template_source:
        raise AssertionError(
            "generated-project validate-define-traceability.py drifted from framework validator"
        )


VALID_SPEC = """# Spec
- REQ-001: Customer can create a booking.
- REQ-002: A consumed slot rejects a competing booking.
- AC-001 [req=REQ-001]: A valid booking is persisted and confirmed.
- AC-002 [req=REQ-002]: A competing booking receives a conflict result.
"""

VALID_TASKS = """# Tasks
- [ ] TASK-001 [type=enabling] [req=-] [ac=-] [paths=src/schema.py] Add booking persistence foundation.
- [ ] TASK-010 [type=requirement] [req=REQ-001] [ac=AC-001] [paths=src/booking.py,tests/test_booking.py] Implement booking creation.
- [ ] TASK-020 [type=requirement] [req=REQ-002] [ac=AC-002] [paths=src/booking.py,tests/test_booking.py] Implement slot conflict handling.
- [ ] TASK-090 [type=assurance] [req=-] [ac=-] [paths=tests/test_booking.py] Add regression checks.
"""


def main() -> int:
    require_template_parity()
    require_verdict("positive READY", run_case(VALID_SPEC, VALID_TASKS), "READY")

    orphan_requirement_tasks = VALID_TASKS.replace(
        "- [ ] TASK-020 [type=requirement] [req=REQ-002] [ac=AC-002] [paths=src/booking.py,tests/test_booking.py] Implement slot conflict handling.\n",
        "",
    )
    result = run_case(VALID_SPEC, orphan_requirement_tasks)
    require_verdict("orphan REQ", result, "BLOCKED")
    require_error("orphan REQ", result, "REQ-002 has no implementation task")

    orphan_ac_tasks = VALID_TASKS.replace(
        "[req=REQ-002] [ac=AC-002]",
        "[req=REQ-002] [ac=AC-001]",
    )
    result = run_case(VALID_SPEC, orphan_ac_tasks)
    require_verdict("orphan AC", result, "BLOCKED")
    require_error("orphan AC", result, "AC-002 has no traced implementation task")

    unknown_req_tasks = VALID_TASKS.replace("REQ-002] [ac=AC-002", "REQ-999] [ac=AC-002")
    result = run_case(VALID_SPEC, unknown_req_tasks)
    require_verdict("unknown REQ", result, "BLOCKED")
    require_error("unknown REQ", result, "unknown requirement REQ-999")

    unknown_ac_tasks = VALID_TASKS.replace("[ac=AC-002]", "[ac=AC-999]", 1)
    result = run_case(VALID_SPEC, unknown_ac_tasks)
    require_verdict("unknown AC", result, "BLOCKED")
    require_error("unknown AC", result, "unknown acceptance criterion AC-999")

    duplicate_req_spec = VALID_SPEC.replace(
        "- REQ-002: A consumed slot rejects a competing booking.\n",
        "- REQ-002: A consumed slot rejects a competing booking.\n- REQ-001: Duplicate requirement.\n",
    )
    result = run_case(duplicate_req_spec, VALID_TASKS)
    require_verdict("duplicate REQ", result, "BLOCKED")
    require_error("duplicate REQ", result, "duplicate requirement REQ-001")

    duplicate_ac_spec = VALID_SPEC + "- AC-001 [req=REQ-001]: Duplicate acceptance criterion.\n"
    result = run_case(duplicate_ac_spec, VALID_TASKS)
    require_verdict("duplicate AC", result, "BLOCKED")
    require_error("duplicate AC", result, "duplicate acceptance criterion AC-001")

    duplicate_task_tasks = VALID_TASKS + (
        "- [ ] TASK-010 [type=assurance] [req=-] [ac=-] [paths=tests/test_duplicate.py] Duplicate task id.\n"
    )
    result = run_case(VALID_SPEC, duplicate_task_tasks)
    require_verdict("duplicate TASK", result, "BLOCKED")
    require_error("duplicate TASK", result, "duplicate task TASK-010")

    malformed_requirement_task = VALID_TASKS.replace(
        "[type=requirement] [req=REQ-001] [ac=AC-001]",
        "[type=requirement] [req=-] [ac=-]",
    )
    result = run_case(VALID_SPEC, malformed_requirement_task)
    require_verdict("malformed requirement task", result, "BLOCKED")
    require_error("malformed requirement task", result, "must reference REQ and AC IDs")

    missing_paths_tasks = VALID_TASKS.replace(
        "[paths=src/booking.py,tests/test_booking.py] Implement booking creation.",
        "[paths=-] Implement booking creation.",
    )
    result = run_case(VALID_SPEC, missing_paths_tasks)
    require_verdict("missing paths", result, "BLOCKED")
    require_error("missing paths", result, "requires explicit paths/write-set")

    non_requirement_coverage_bypass = """# Tasks
- [ ] TASK-001 [type=assurance] [req=REQ-001] [ac=AC-001] [paths=tests/test_booking.py] Verify booking creation.
- [ ] TASK-002 [type=documentation] [req=REQ-002] [ac=AC-002] [paths=docs/booking.md] Document slot conflict handling.
"""
    result = run_case(VALID_SPEC, non_requirement_coverage_bypass)
    require_verdict("non-requirement coverage bypass", result, "BLOCKED")
    require_error("non-requirement coverage bypass", result, "REQ-001 has no implementation task")
    require_error("non-requirement coverage bypass", result, "AC-002 has no traced implementation task")

    unknown_ref_on_non_requirement = VALID_TASKS.replace(
        "[type=assurance] [req=-] [ac=-]",
        "[type=assurance] [req=REQ-999] [ac=AC-999]",
    )
    result = run_case(VALID_SPEC, unknown_ref_on_non_requirement)
    require_verdict("unknown references on non-requirement task", result, "BLOCKED")
    require_error("unknown references on non-requirement task", result, "unknown requirement REQ-999")
    require_error("unknown references on non-requirement task", result, "unknown acceptance criterion AC-999")

    non_requirement_without_fake_requirement = VALID_TASKS.replace(
        "[type=enabling] [req=-] [ac=-]",
        "[type=documentation] [req=-] [ac=-]",
    )
    require_verdict(
        "non-requirement task without fake IDs",
        run_case(VALID_SPEC, non_requirement_without_fake_requirement),
        "READY",
    )

    print("define traceability fixtures: READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
