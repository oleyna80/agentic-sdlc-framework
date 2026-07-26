#!/usr/bin/env python3
"""Regression fixtures for evaluation plans, reports, and closeout binding."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "template/scripts/validate-evaluation.py"
PLAN_TEMPLATE = ROOT / "template/docs/templates/evaluation-plan-template.json"
REPORT_TEMPLATE = ROOT / "template/docs/templates/evaluation-report-template.json"

spec = importlib.util.spec_from_file_location("evaluation_validator", VALIDATOR_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
EvaluationError = validator.EvaluationError


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def expect_failure(label: str, function, *args, contains: str | None = None) -> None:
    try:
        function(*args)
    except EvaluationError as exc:
        if contains is not None:
            assert contains in str(exc), f"{label}: unexpected error: {exc}"
        return
    raise AssertionError(f"{label}: expected EvaluationError")


def approved_plan() -> dict:
    plan = load(PLAN_TEMPLATE)
    plan.update(
        {
            "evaluation_id": "eval-wb-007",
            "status": "approved",
            "work_block_id": "wb-007",
            "revision": "3",
            "benchmark_revision": "fixture-v1",
            "rubric_revision": "rubric-v2",
            "isolation_requirement": "separate-process",
        }
    )
    plan["subject"] = {
        "objective": "Validate the evaluation contract.",
        "specification_revision": "governance/evaluation.md@1",
        "frozen_revision": "deadbeef",
    }
    plan["deterministic_checks"][0].update(
        {"command": "python scripts/test-evaluation-contracts.py", "evidence": "ci/run"}
    )
    plan["output_criteria"][0].update(
        {"evaluator_type": "human", "threshold": 1.0, "weight": 1.0, "evidence": "review"}
    )
    plan["trajectory_requirements"][0].update(
        {
            "event_source": "docs/evals/eval-wb-007/events.jsonl",
            "required_events": ["work_block_bound", "required_checks_completed"],
            "prohibited_events": ["unauthorized_side_effect"],
        }
    )
    return plan


def ready_report() -> dict:
    report = load(REPORT_TEMPLATE)
    report.update(
        {
            "evaluation_id": "eval-wb-007",
            "status": "complete",
            "work_block_id": "wb-007",
            "plan_revision": "3",
            "subject_revision": "deadbeef",
            "runtime": "generic",
            "logical_role": "verifier",
            "model_class": "assurance",
            "actual_model": "not-disclosed",
            "isolation": "separate-process",
            "completed_at": "2026-07-26T00:00:00Z",
        }
    )
    report["deterministic_results"] = [
        {
            "criterion_id": "deterministic-contract",
            "state": "pass",
            "evidence": "ci/run",
            "notes": "",
        }
    ]
    report["output_results"] = [
        {
            "criterion_id": "artifact-quality",
            "state": "pass",
            "score": 1.0,
            "evaluator_type": "human",
            "evidence": "review",
            "notes": "",
        }
    ]
    report["trajectory_results"] = [
        {
            "criterion_id": "required-checks-observed",
            "state": "pass",
            "event_source": "docs/evals/eval-wb-007/events.jsonl",
            "observed_events": ["work_block_bound", "required_checks_completed"],
            "missing_events": [],
            "prohibited_events_observed": [],
            "notes": "",
        }
    ]
    report["aggregate"] = {
        "blocking_failures": [],
        "blocked_checks": [],
        "inspection_gaps": [],
        "verdict": "READY",
    }
    return report


def active_gate() -> dict:
    return {
        "schema_version": 1,
        "work_block_id": "wb-007",
        "assurance": {
            "evaluation": {
                "required": True,
                "status": "READY",
                "verdict": "READY",
                "plan": "docs/evals/eval-wb-007/plan.json",
                "report": "docs/reports/evaluations/eval-wb-007.json",
                "rubric_revision": "rubric-v2",
                "benchmark_revision": "fixture-v1",
                "isolation": "separate-process",
                "skip_reason": "",
            }
        },
        "closeout_mode": "success-closeout",
    }


def main() -> int:
    plan = approved_plan()
    report = ready_report()
    validator.validate_plan(plan, require_approved=True)
    validator.validate_report(report, plan)

    duplicate = copy.deepcopy(plan)
    duplicate["output_criteria"][0]["criterion_id"] = "deterministic-contract"
    expect_failure("duplicate-global-id", validator.validate_plan, duplicate, contains="globally unique")

    hidden = copy.deepcopy(plan)
    hidden["trajectory_requirements"][0]["chain_of_thought"] = "capture it"
    expect_failure("hidden-reasoning", validator.validate_plan, hidden, contains="hidden reasoning")

    judge_override = copy.deepcopy(plan)
    judge_override["judge_policy"]["can_override_deterministic"] = True
    expect_failure("judge-override", validator.validate_plan, judge_override, contains="cannot override")

    judge_gate = copy.deepcopy(plan)
    judge_gate["judge_policy"]["can_open_authority_gates"] = True
    expect_failure("judge-gate", validator.validate_plan, judge_gate, contains="cannot open")

    disabled_judge = copy.deepcopy(plan)
    disabled_judge["output_criteria"][0]["evaluator_type"] = "lm_judge"
    expect_failure("disabled-judge", validator.validate_plan, disabled_judge, contains="disables")

    missing_event = copy.deepcopy(report)
    missing_event["trajectory_results"][0]["missing_events"] = ["required_checks_completed"]
    expect_failure("trajectory-missing", validator.validate_report, missing_event, plan, contains="cannot pass")

    prohibited_event = copy.deepcopy(report)
    prohibited_event["trajectory_results"][0]["prohibited_events_observed"] = [
        "unauthorized_side_effect"
    ]
    expect_failure(
        "trajectory-prohibited", validator.validate_report, prohibited_event, plan, contains="cannot pass"
    )

    wrong_ids = copy.deepcopy(report)
    wrong_ids["output_results"][0]["criterion_id"] = "wrong"
    expect_failure("result-id-mismatch", validator.validate_report, wrong_ids, plan, contains="exactly match")

    ready_with_gap = copy.deepcopy(report)
    ready_with_gap["aggregate"]["inspection_gaps"] = ["missing-log"]
    expect_failure("ready-gap", validator.validate_report, ready_with_gap, plan, contains="cannot contain")

    blocking_not_run = copy.deepcopy(report)
    blocking_not_run["deterministic_results"][0]["state"] = "not_run"
    expect_failure(
        "blocking-not-run", validator.validate_report, blocking_not_run, plan, contains="requires blocking criterion pass"
    )

    deterministic_judge = copy.deepcopy(report)
    deterministic_judge["deterministic_results"][0]["evaluator_type"] = "lm_judge"
    expect_failure(
        "deterministic-judge", validator.validate_report, deterministic_judge, plan, contains="cannot rely"
    )

    with tempfile.TemporaryDirectory(prefix="evaluation-contract-") as temp:
        root = Path(temp)
        plan_path = root / "docs/evals/eval-wb-007/plan.json"
        report_path = root / "docs/reports/evaluations/eval-wb-007.json"
        gate_path = root / ".agent/active-work-block.json"
        write(plan_path, plan)
        write(report_path, report)
        write(gate_path, active_gate())
        result = validator.validate_closeout(root)
        assert result["verdict"] == "READY"

        skipped_required = active_gate()
        skipped_required["assurance"]["evaluation"].update(
            {"status": "SKIPPED", "verdict": "UNVERIFIED", "skip_reason": "not needed"}
        )
        write(gate_path, skipped_required)
        expect_failure(
            "required-skipped", validator.validate_closeout, root, contains="cannot be SKIPPED"
        )

        optional_no_reason = active_gate()
        optional_no_reason["assurance"]["evaluation"].update(
            {"required": False, "status": "SKIPPED", "verdict": "UNVERIFIED", "skip_reason": ""}
        )
        write(gate_path, optional_no_reason)
        expect_failure(
            "optional-skip-reason", validator.validate_closeout, root, contains="requires skip_reason"
        )

        rubric_mismatch = active_gate()
        rubric_mismatch["assurance"]["evaluation"]["rubric_revision"] = "wrong"
        write(gate_path, rubric_mismatch)
        expect_failure(
            "rubric-mismatch", validator.validate_closeout, root, contains="rubric revision"
        )

        benchmark_mismatch = active_gate()
        benchmark_mismatch["assurance"]["evaluation"]["benchmark_revision"] = "wrong"
        write(gate_path, benchmark_mismatch)
        expect_failure(
            "benchmark-mismatch", validator.validate_closeout, root, contains="benchmark revision"
        )

        outside_report = active_gate()
        outside_report["assurance"]["evaluation"]["report"] = "../report.json"
        write(gate_path, outside_report)
        expect_failure(
            "outside-report", validator.validate_closeout, root, contains="escapes repository"
        )

    print("Evaluation contract fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
