#!/usr/bin/env python3
"""Deterministic fixtures for validate-define-traceability.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate-define-traceability.py"

spec = importlib.util.spec_from_file_location("define_traceability", VALIDATOR_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
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
    require_verdict("valid", run_case(VALID_SPEC, VALID_TASKS), "READY")

    orphan_requirement_tasks = VALID_TASKS.replace(
        "- [ ] TASK-020 [type=requirement] [req=REQ-002] [ac=AC-002] [paths=src/booking.py,tests/test_booking.py] Implement slot conflict handling.\n",
        "",
    )
    require_verdict(
        "orphan requirement/task",
        run_case(VALID_SPEC, orphan_requirement_tasks),
        "BLOCKED",
    )

    unknown_ref_tasks = VALID_TASKS.replace("REQ-002] [ac=AC-002", "REQ-999] [ac=AC-002")
    require_verdict("unknown requirement", run_case(VALID_SPEC, unknown_ref_tasks), "BLOCKED")

    malformed_requirement_task = VALID_TASKS.replace(
        "[type=requirement] [req=REQ-001] [ac=AC-001]",
        "[type=requirement] [req=-] [ac=-]",
    )
    require_verdict(
        "missing requirement trace",
        run_case(VALID_SPEC, malformed_requirement_task),
        "BLOCKED",
    )

    enabling_without_fake_requirement = VALID_TASKS.replace(
        "[type=enabling] [req=-] [ac=-]",
        "[type=documentation] [req=-] [ac=-]",
    )
    require_verdict(
        "non-requirement task",
        run_case(VALID_SPEC, enabling_without_fake_requirement),
        "READY",
    )

    print("define traceability fixtures: READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
