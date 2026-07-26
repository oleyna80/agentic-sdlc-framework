#!/usr/bin/env python3
"""Validate publishable evaluation governance, templates, and generated scaffold."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "governance/evaluation.md",
    "docs/plans/wb-007-agent-evaluation-trajectory-assurance.md",
    "scripts/test-evaluation-contracts.py",
    "scripts/validate_evaluation_publication.py",
    "template/scripts/validate-evaluation.py",
    "template/docs/evals/README.md",
    "template/docs/reports/evaluations/README.md",
    "template/docs/templates/evaluation-plan-template.json",
    "template/docs/templates/evaluation-report-template.json",
    "template/docs/templates/trajectory-event-template.json",
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: evaluation publication: {message}")


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must parse to an object")
    return value


def load_bootstrap_module():
    path = ROOT / "bootstrap/bootstrap_project.py"
    spec = importlib.util.spec_from_file_location("bootstrap_project", path)
    if spec is None or spec.loader is None:
        fail("cannot import bootstrap engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(f"missing {relative}")

    for relative in (
        "scripts/test-evaluation-contracts.py",
        "scripts/validate_evaluation_publication.py",
        "template/scripts/validate-evaluation.py",
        "template/.claude/hooks/assurance_gate.py",
    ):
        path = ROOT / relative
        try:
            compile(path.read_text(encoding="utf-8"), relative, "exec")
        except (OSError, SyntaxError) as exc:
            fail(f"Python syntax failed for {relative}: {exc}")

    plan = load_json(ROOT / "template/docs/templates/evaluation-plan-template.json")
    report = load_json(ROOT / "template/docs/templates/evaluation-report-template.json")
    event = load_json(ROOT / "template/docs/templates/trajectory-event-template.json")
    if plan.get("artifact_type") != "evaluation_plan":
        fail("evaluation plan template artifact_type mismatch")
    if report.get("artifact_type") != "evaluation_report":
        fail("evaluation report template artifact_type mismatch")
    if event.get("event_type") != "tool_call":
        fail("trajectory event template event_type mismatch")
    serialized = json.dumps([plan, report, event], sort_keys=True).lower()
    for forbidden in (
        '"chain_of_thought"',
        '"hidden_reasoning"',
        '"private_reasoning"',
        '"scratchpad"',
    ):
        if forbidden in serialized:
            fail(f"evaluation templates expose forbidden reasoning field {forbidden}")

    catalog = load_json(ROOT / "bootstrap/profiles.json")
    required = set(catalog.get("common_required_paths") or [])
    for relative in (
        "governance/evaluation.md",
        "docs/evals/README.md",
        "docs/reports/evaluations/README.md",
        "docs/templates/evaluation-plan-template.json",
        "docs/templates/evaluation-report-template.json",
        "docs/templates/trajectory-event-template.json",
        "scripts/validate-evaluation.py",
    ):
        if relative not in required:
            fail(f"bootstrap profile catalog omits {relative}")

    engine = load_bootstrap_module()
    engine.validate_catalog(catalog, ROOT)

    result = subprocess.run(
        [sys.executable, "scripts/test-evaluation-contracts.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        fail((result.stdout + "\n" + result.stderr).strip()[-5000:])

    with tempfile.TemporaryDirectory(prefix="evaluation-publication-") as temp:
        target = Path(temp) / "project"
        result = subprocess.run(
            [
                "bash",
                str(ROOT / "bootstrap.sh"),
                "--profile",
                "core",
                str(target),
                "Evaluation Publication Smoke",
                "evaluation-publication-smoke",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            fail((result.stdout + "\n" + result.stderr).strip()[-5000:])
        for relative in (
            "governance/evaluation.md",
            "scripts/validate-evaluation.py",
            "docs/evals/README.md",
            "docs/reports/evaluations/README.md",
            "docs/templates/evaluation-plan-template.json",
            "docs/templates/evaluation-report-template.json",
            "docs/templates/trajectory-event-template.json",
        ):
            if not (target / relative).is_file():
                fail(f"core generated scaffold missing {relative}")
        gate = load_json(target / ".agent/active-work-block.default.json")
        expected = {
            "required": False,
            "status": "PENDING",
            "verdict": "PENDING",
            "plan": "",
            "report": "",
            "rubric_revision": "",
            "benchmark_revision": "",
            "isolation": "unknown",
            "skip_reason": "",
        }
        if gate.get("assurance", {}).get("evaluation") != expected:
            fail("generated blocked default evaluation state is not canonical")

    print("Evaluation publication validation: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
