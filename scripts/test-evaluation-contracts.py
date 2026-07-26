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


def expect_failure(
    label: str,
    function,
    *args,
    contains: str | None = None,
    **kwargs,
) -> None:
    try:
        function(*args, **kwargs)
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
        {"criterion_id": "deterministic-contract", "state": "pass", "evidence": "ci/run", "notes": ""}
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

    cases: list[tuple[str, object, object, str]] = []

    pending_freeze = copy.deepcopy(plan)
    pending_freeze["subject"]["frozen_revision"] = "pending-final-freeze"
    expect_failure(
        "approved-pending-freeze",
        validator.validate_plan,
        pending_freeze,
        require_approved=True,
        contains="frozen subject revision",
    )

    duplicate = copy.deepcopy(plan)
    duplicate["output_criteria"][0]["criterion_id"] = "deterministic-contract"
    cases.append(("duplicate-global-id", validator.validate_plan, duplicate, "globally unique"))

    hidden = copy.deepcopy(plan)
    hidden["trajectory_requirements"][0]["chain_of_thought"] = "capture it"
    cases.append(("hidden-reasoning", validator.validate_plan, hidden, "hidden reasoning"))

    judge_override = copy.deepcopy(plan)
    judge_override["judge_policy"]["can_override_deterministic"] = True
    cases.append(("judge-override", validator.validate_plan, judge_override, "cannot override"))

    judge_gate = copy.deepcopy(plan)
    judge_gate["judge_policy"]["can_open_authority_gates"] = True
    cases.append(("judge-gate", validator.validate_plan, judge_gate, "cannot open"))

    disabled_judge = copy.deepcopy(plan)
    disabled_judge["output_criteria"][0]["evaluator_type"] = "lm_judge"
    cases.append(("disabled-judge", validator.validate_plan, disabled_judge, "disables"))

    zero_weight = copy.deepcopy(plan)
    zero_weight["output_criteria"][0]["weight"] = 0
    cases.append(("zero-total-weight", validator.validate_plan, zero_weight, "positive total weight"))

    for label, function, value, marker in cases:
        expect_failure(label, function, value, contains=marker)

    report_cases: list[tuple[str, dict, str]] = []

    subject_mismatch = copy.deepcopy(report)
    subject_mismatch["subject_revision"] = "cafebabe"
    report_cases.append(("subject-revision-mismatch", subject_mismatch, "frozen_revision"))

    below_threshold = copy.deepcopy(report)
    below_threshold["output_results"][0]["score"] = 0.5
    report_cases.append(("below-threshold-pass", below_threshold, "below approved threshold"))

    evaluator_mismatch = copy.deepcopy(report)
    evaluator_mismatch["output_results"][0]["evaluator_type"] = "rule_based"
    report_cases.append(("evaluator-type-mismatch", evaluator_mismatch, "evaluator type"))

    missing_event = copy.deepcopy(report)
    missing_event["trajectory_results"][0]["observed_events"] = ["work_block_bound"]
    missing_event["trajectory_results"][0]["missing_events"] = ["required_checks_completed"]
    report_cases.append(("trajectory-required-event-missing", missing_event, "cannot pass"))

    false_empty_missing = copy.deepcopy(report)
    false_empty_missing["trajectory_results"][0]["observed_events"] = ["work_block_bound"]
    report_cases.append(("trajectory-false-empty-missing", false_empty_missing, "missing_events"))

    event_source_mismatch = copy.deepcopy(report)
    event_source_mismatch["trajectory_results"][0]["event_source"] = "other.jsonl"
    report_cases.append(("trajectory-event-source-mismatch", event_source_mismatch, "event source"))

    prohibited_event = copy.deepcopy(report)
    prohibited_event["trajectory_results"][0]["prohibited_events_observed"] = ["unauthorized_side_effect"]
    report_cases.append(("trajectory-prohibited", prohibited_event, "cannot pass"))

    unplanned_prohibited = copy.deepcopy(report)
    unplanned_prohibited["trajectory_results"][0]["state"] = "fail"
    unplanned_prohibited["trajectory_results"][0]["prohibited_events_observed"] = ["unknown-prohibition"]
    report_cases.append(("trajectory-unplanned-prohibited", unplanned_prohibited, "unplanned prohibited"))

    wrong_ids = copy.deepcopy(report)
    wrong_ids["output_results"][0]["criterion_id"] = "wrong"
    report_cases.append(("result-id-mismatch", wrong_ids, "exactly match"))

    ready_with_gap = copy.deepcopy(report)
    ready_with_gap["aggregate"]["inspection_gaps"] = ["missing-log"]
    report_cases.append(("ready-gap", ready_with_gap, "cannot contain"))

    blocking_not_run = copy.deepcopy(report)
    blocking_not_run["deterministic_results"][0]["state"] = "not_run"
    report_cases.append(("blocking-not-run", blocking_not_run, "requires blocking criterion pass"))

    deterministic_judge = copy.deepcopy(report)
    deterministic_judge["deterministic_results"][0]["evaluator_type"] = "lm_judge"
    report_cases.append(("deterministic-judge", deterministic_judge, "cannot rely"))

    missing_completed_at = copy.deepcopy(report)
    missing_completed_at["completed_at"] = None
    report_cases.append(("complete-report-time", missing_completed_at, "completed_at"))

    for label, candidate, marker in report_cases:
        expect_failure(label, validator.validate_report, candidate, plan, contains=marker)

    with tempfile.TemporaryDirectory(prefix="evaluation-contract-") as temp:
        root = Path(temp)
        plan_path = root / "docs/evals/eval-wb-007/plan.json"
        report_path = root / "docs/reports/evaluations/eval-wb-007.json"
        gate_path = root / ".agent/active-work-block.json"
        write(plan_path, plan)
        write(report_path, report)
        write(gate_path, active_gate())
        assert validator.validate_closeout(root)["verdict"] == "READY"

        gate_cases: list[tuple[str, dict, str]] = []

        skipped_required = active_gate()
        skipped_required["assurance"]["evaluation"].update(
            {"status": "SKIPPED", "verdict": "UNVERIFIED", "skip_reason": "not needed"}
        )
        gate_cases.append(("required-skipped", skipped_required, "cannot be SKIPPED"))

        optional_no_reason = active_gate()
        optional_no_reason["assurance"]["evaluation"].update(
            {"required": False, "status": "SKIPPED", "verdict": "UNVERIFIED", "skip_reason": ""}
        )
        gate_cases.append(("optional-skip-reason", optional_no_reason, "requires skip_reason"))

        rubric_mismatch = active_gate()
        rubric_mismatch["assurance"]["evaluation"]["rubric_revision"] = "wrong"
        gate_cases.append(("rubric-mismatch", rubric_mismatch, "rubric revision"))

        benchmark_mismatch = active_gate()
        benchmark_mismatch["assurance"]["evaluation"]["benchmark_revision"] = "wrong"
        gate_cases.append(("benchmark-mismatch", benchmark_mismatch, "benchmark revision"))

        isolation_mismatch = active_gate()
        isolation_mismatch["assurance"]["evaluation"]["isolation"] = "other"
        gate_cases.append(("isolation-mismatch", isolation_mismatch, "isolation"))

        outside_report = active_gate()
        outside_report["assurance"]["evaluation"]["report"] = "../report.json"
        gate_cases.append(("outside-report", outside_report, "escapes repository"))

        for label, gate, marker in gate_cases:
            write(gate_path, gate)
            expect_failure(label, validator.validate_closeout, root, contains=marker)

    print("Evaluation contract fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
