#!/usr/bin/env python3
"""Validate portable evaluation plans, reports, and Work Block closeout state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import sys
from typing import Any

SCHEMA_VERSION = 1
RESULT_STATES = {"pass", "fail", "blocked", "not_run", "not_applicable"}
EVALUATION_VERDICTS = {"READY", "BLOCKED", "UNVERIFIED"}
ASSURANCE_STATUSES = {"PENDING", "READY", "SKIPPED", "DEGRADED", "BLOCKED"}
EVALUATOR_TYPES = {"deterministic", "human", "rule_based", "lm_judge"}
FORBIDDEN_REASONING_KEYS = {
    "chain_of_thought",
    "chain-of-thought",
    "hidden_reasoning",
    "private_reasoning",
    "scratchpad",
    "internal_deliberation",
}


class EvaluationError(RuntimeError):
    pass


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"invalid {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise EvaluationError(f"{label} must contain a JSON object")
    return value


def nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationError(f"{label} must be a non-empty string")
    return value.strip()


def string_list(value: object, label: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise EvaluationError(f"{label} must be an array of non-empty strings")
    if not allow_empty and not value:
        raise EvaluationError(f"{label} must not be empty")
    return [item.strip() for item in value]


def bool_value(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise EvaluationError(f"{label} must be boolean")
    return value


def reject_hidden_reasoning(value: object, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower().replace(" ", "_")
            if normalized in FORBIDDEN_REASONING_KEYS:
                raise EvaluationError(
                    f"{path}.{key} requests hidden reasoning; only observable events are allowed"
                )
            reject_hidden_reasoning(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_hidden_reasoning(child, f"{path}[{index}]")


def unique_criterion_ids(items: object, label: str) -> list[dict[str, Any]]:
    if not isinstance(items, list):
        raise EvaluationError(f"{label} must be an array")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise EvaluationError(f"{label}[{index}] must be an object")
        criterion_id = nonempty_string(item.get("criterion_id"), f"{label}[{index}].criterion_id")
        if criterion_id in seen:
            raise EvaluationError(f"duplicate criterion_id in {label}: {criterion_id}")
        seen.add(criterion_id)
        result.append(item)
    return result


def validate_plan(plan: dict[str, Any], *, require_approved: bool = False) -> dict[str, Any]:
    reject_hidden_reasoning(plan)
    if plan.get("schema_version") != SCHEMA_VERSION:
        raise EvaluationError(f"evaluation plan requires schema_version={SCHEMA_VERSION}")
    if plan.get("artifact_type") != "evaluation_plan":
        raise EvaluationError("artifact_type must be evaluation_plan")

    evaluation_id = nonempty_string(plan.get("evaluation_id"), "evaluation_id")
    work_block_id = nonempty_string(plan.get("work_block_id"), "work_block_id")
    revision = nonempty_string(plan.get("revision"), "revision")
    status = nonempty_string(plan.get("status"), "status")
    if status not in {"draft", "review", "approved", "superseded", "blocked"}:
        raise EvaluationError(f"unsupported evaluation plan status: {status}")
    if require_approved and status != "approved":
        raise EvaluationError("closeout evaluation plan must be approved")

    subject = plan.get("subject")
    if not isinstance(subject, dict):
        raise EvaluationError("subject must be an object")
    for field in ("objective", "specification_revision", "frozen_revision"):
        nonempty_string(subject.get(field), f"subject.{field}")

    deterministic = unique_criterion_ids(plan.get("deterministic_checks"), "deterministic_checks")
    output = unique_criterion_ids(plan.get("output_criteria"), "output_criteria")
    trajectory = unique_criterion_ids(
        plan.get("trajectory_requirements"), "trajectory_requirements"
    )
    if not deterministic and not output and not trajectory:
        raise EvaluationError("evaluation plan must define at least one criterion")

    all_ids: set[str] = set()
    for label, items in (
        ("deterministic_checks", deterministic),
        ("output_criteria", output),
        ("trajectory_requirements", trajectory),
    ):
        for index, item in enumerate(items):
            criterion_id = nonempty_string(item.get("criterion_id"), f"{label}[{index}].criterion_id")
            if criterion_id in all_ids:
                raise EvaluationError(f"criterion_id must be globally unique: {criterion_id}")
            all_ids.add(criterion_id)
            nonempty_string(item.get("description"), f"{label}[{index}].description")
            bool_value(item.get("blocking"), f"{label}[{index}].blocking")

    for index, item in enumerate(deterministic):
        nonempty_string(item.get("command"), f"deterministic_checks[{index}].command")
        nonempty_string(item.get("evidence"), f"deterministic_checks[{index}].evidence")

    for index, item in enumerate(output):
        evaluator_type = nonempty_string(
            item.get("evaluator_type"), f"output_criteria[{index}].evaluator_type"
        )
        if evaluator_type not in EVALUATOR_TYPES:
            raise EvaluationError(
                f"output_criteria[{index}].evaluator_type is unsupported: {evaluator_type}"
            )
        threshold = item.get("threshold")
        if not isinstance(threshold, (int, float)) or isinstance(threshold, bool):
            raise EvaluationError(f"output_criteria[{index}].threshold must be numeric")
        weight = item.get("weight")
        if not isinstance(weight, (int, float)) or isinstance(weight, bool) or weight < 0:
            raise EvaluationError(f"output_criteria[{index}].weight must be non-negative")
        nonempty_string(item.get("evidence"), f"output_criteria[{index}].evidence")

    for index, item in enumerate(trajectory):
        nonempty_string(
            item.get("event_source"), f"trajectory_requirements[{index}].event_source"
        )
        string_list(
            item.get("required_events"),
            f"trajectory_requirements[{index}].required_events",
            allow_empty=False,
        )
        string_list(
            item.get("prohibited_events", []),
            f"trajectory_requirements[{index}].prohibited_events",
        )

    nonempty_string(plan.get("benchmark_revision"), "benchmark_revision")
    nonempty_string(plan.get("rubric_revision"), "rubric_revision")
    nonempty_string(plan.get("isolation_requirement"), "isolation_requirement")
    if plan.get("aggregate_verdict_rule") != "all_blocking_pass":
        raise EvaluationError("aggregate_verdict_rule must be all_blocking_pass")

    judge = plan.get("judge_policy")
    if not isinstance(judge, dict):
        raise EvaluationError("judge_policy must be an object")
    lm_allowed = bool_value(judge.get("lm_judge_allowed"), "judge_policy.lm_judge_allowed")
    if bool_value(
        judge.get("can_override_deterministic"),
        "judge_policy.can_override_deterministic",
    ):
        raise EvaluationError("LM judges cannot override deterministic evidence")
    if bool_value(
        judge.get("can_open_authority_gates"),
        "judge_policy.can_open_authority_gates",
    ):
        raise EvaluationError("LM judges cannot open authority gates")
    judge_identity = nonempty_string(judge.get("judge_identity"), "judge_policy.judge_identity")
    prompt_revision = nonempty_string(
        judge.get("judge_prompt_revision"), "judge_policy.judge_prompt_revision"
    )
    if lm_allowed and (
        judge_identity == "not-applicable" or prompt_revision == "not-applicable"
    ):
        raise EvaluationError("enabled LM judge requires concrete identity and prompt revision")
    if not lm_allowed and any(
        item.get("evaluator_type") == "lm_judge" for item in output
    ):
        raise EvaluationError("output criterion uses lm_judge while judge policy disables it")

    return {
        "evaluation_id": evaluation_id,
        "work_block_id": work_block_id,
        "revision": revision,
        "status": status,
        "deterministic": deterministic,
        "output": output,
        "trajectory": trajectory,
        "rubric_revision": plan["rubric_revision"],
        "benchmark_revision": plan["benchmark_revision"],
    }


def result_map(items: object, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(unique_criterion_ids(items, label)):
        criterion_id = nonempty_string(item.get("criterion_id"), f"{label}[{index}].criterion_id")
        state = nonempty_string(item.get("state"), f"{label}[{index}].state")
        if state not in RESULT_STATES:
            raise EvaluationError(f"{label}[{index}].state is unsupported: {state}")
        result[criterion_id] = item
    return result


def validate_report(
    report: dict[str, Any], plan: dict[str, Any] | None = None
) -> dict[str, Any]:
    reject_hidden_reasoning(report)
    if report.get("schema_version") != SCHEMA_VERSION:
        raise EvaluationError(f"evaluation report requires schema_version={SCHEMA_VERSION}")
    if report.get("artifact_type") != "evaluation_report":
        raise EvaluationError("artifact_type must be evaluation_report")

    evaluation_id = nonempty_string(report.get("evaluation_id"), "evaluation_id")
    work_block_id = nonempty_string(report.get("work_block_id"), "work_block_id")
    plan_revision = nonempty_string(report.get("plan_revision"), "plan_revision")
    nonempty_string(report.get("subject_revision"), "subject_revision")
    status = nonempty_string(report.get("status"), "status")
    if status not in {"draft", "review", "complete", "blocked"}:
        raise EvaluationError(f"unsupported evaluation report status: {status}")
    for field in ("runtime", "logical_role", "model_class", "isolation"):
        value = nonempty_string(report.get(field), field)
        if status == "complete" and value in {"replace-me", "unknown"}:
            raise EvaluationError(f"complete report requires concrete {field}")

    deterministic = result_map(report.get("deterministic_results"), "deterministic_results")
    output = result_map(report.get("output_results"), "output_results")
    trajectory = result_map(report.get("trajectory_results"), "trajectory_results")

    for criterion_id, item in deterministic.items():
        state = item["state"]
        if state == "pass":
            nonempty_string(item.get("evidence"), f"deterministic_results[{criterion_id}].evidence")

    for criterion_id, item in output.items():
        evaluator_type = nonempty_string(
            item.get("evaluator_type"), f"output_results[{criterion_id}].evaluator_type"
        )
        if evaluator_type not in EVALUATOR_TYPES:
            raise EvaluationError(
                f"output_results[{criterion_id}].evaluator_type is unsupported"
            )
        if item["state"] == "pass":
            score = item.get("score")
            if not isinstance(score, (int, float)) or isinstance(score, bool):
                raise EvaluationError(f"output_results[{criterion_id}].score must be numeric")
            nonempty_string(item.get("evidence"), f"output_results[{criterion_id}].evidence")

    for criterion_id, item in trajectory.items():
        nonempty_string(
            item.get("event_source"), f"trajectory_results[{criterion_id}].event_source"
        )
        observed = string_list(
            item.get("observed_events"),
            f"trajectory_results[{criterion_id}].observed_events",
        )
        missing = string_list(
            item.get("missing_events"),
            f"trajectory_results[{criterion_id}].missing_events",
        )
        prohibited = string_list(
            item.get("prohibited_events_observed"),
            f"trajectory_results[{criterion_id}].prohibited_events_observed",
        )
        if item["state"] == "pass" and (not observed or missing or prohibited):
            raise EvaluationError(
                f"trajectory result {criterion_id} cannot pass with missing/prohibited/empty observable events"
            )

    judge_evidence = report.get("judge_evidence")
    if not isinstance(judge_evidence, list) or any(
        not isinstance(item, dict) for item in judge_evidence
    ):
        raise EvaluationError("judge_evidence must be an array of objects")

    aggregate = report.get("aggregate")
    if not isinstance(aggregate, dict):
        raise EvaluationError("aggregate must be an object")
    blocking_failures = string_list(
        aggregate.get("blocking_failures"), "aggregate.blocking_failures"
    )
    blocked_checks = string_list(aggregate.get("blocked_checks"), "aggregate.blocked_checks")
    inspection_gaps = string_list(
        aggregate.get("inspection_gaps"), "aggregate.inspection_gaps"
    )
    verdict = nonempty_string(aggregate.get("verdict"), "aggregate.verdict")
    if verdict not in EVALUATION_VERDICTS:
        raise EvaluationError(f"unsupported evaluation verdict: {verdict}")

    plan_info: dict[str, Any] | None = None
    if plan is not None:
        plan_info = validate_plan(plan, require_approved=status == "complete")
        if evaluation_id != plan_info["evaluation_id"]:
            raise EvaluationError("report evaluation_id does not match plan")
        if work_block_id != plan_info["work_block_id"]:
            raise EvaluationError("report work_block_id does not match plan")
        if plan_revision != plan_info["revision"]:
            raise EvaluationError("report plan_revision does not match plan revision")

        result_groups = {
            "deterministic": deterministic,
            "output": output,
            "trajectory": trajectory,
        }
        for group_name, planned in (
            ("deterministic", plan_info["deterministic"]),
            ("output", plan_info["output"]),
            ("trajectory", plan_info["trajectory"]),
        ):
            planned_ids = {item["criterion_id"] for item in planned}
            result_ids = set(result_groups[group_name])
            if planned_ids != result_ids:
                raise EvaluationError(
                    f"{group_name} result IDs do not exactly match the approved plan"
                )

        if verdict == "READY":
            if status != "complete":
                raise EvaluationError("READY verdict requires complete report status")
            if blocking_failures or blocked_checks or inspection_gaps:
                raise EvaluationError("READY verdict cannot contain blocking failures or gaps")
            for group_name, planned in (
                ("deterministic", plan_info["deterministic"]),
                ("output", plan_info["output"]),
                ("trajectory", plan_info["trajectory"]),
            ):
                for criterion in planned:
                    if criterion["blocking"] and result_groups[group_name][criterion["criterion_id"]]["state"] != "pass":
                        raise EvaluationError(
                            f"READY verdict requires blocking criterion pass: {criterion['criterion_id']}"
                        )
            for criterion in plan_info["deterministic"]:
                result = deterministic[criterion["criterion_id"]]
                if result.get("evaluator_type") == "lm_judge":
                    raise EvaluationError("deterministic result cannot rely on an LM judge")

    if verdict == "READY" and (blocking_failures or blocked_checks or inspection_gaps):
        raise EvaluationError("READY verdict cannot contain blocking failures or gaps")

    return {
        "evaluation_id": evaluation_id,
        "work_block_id": work_block_id,
        "plan_revision": plan_revision,
        "status": status,
        "verdict": verdict,
        "plan": plan_info,
    }


def repo_relative_file(root: Path, raw: object, label: str, prefix: str) -> Path:
    value = nonempty_string(raw, label).strip("\"'")
    path = Path(value)
    if path.is_absolute():
        try:
            path = path.resolve().relative_to(root)
        except (OSError, ValueError) as exc:
            raise EvaluationError(f"{label} is outside repository: {value}") from exc
    pure = PurePosixPath(path.as_posix())
    if ".." in pure.parts:
        raise EvaluationError(f"{label} escapes repository: {value}")
    normalized = pure.as_posix().lstrip("./")
    if not normalized.startswith(prefix):
        raise EvaluationError(f"{label} must be under {prefix}: {normalized}")
    full = root / normalized
    if not full.is_file() or full.stat().st_size == 0:
        raise EvaluationError(f"{label} does not exist or is empty: {normalized}")
    return full


def validate_closeout(root: Path) -> dict[str, Any]:
    gate_path = root / ".agent/active-work-block.json"
    gate = load_json_object(gate_path, str(gate_path))
    if gate.get("schema_version") != SCHEMA_VERSION:
        raise EvaluationError("unsupported active Work Block schema_version")
    work_block_id = nonempty_string(gate.get("work_block_id"), "work_block_id")
    assurance = gate.get("assurance")
    if not isinstance(assurance, dict):
        raise EvaluationError("active Work Block requires assurance object")
    state = assurance.get("evaluation")
    if not isinstance(state, dict):
        raise EvaluationError("active Work Block requires assurance.evaluation state")

    required = state.get("required") is True
    status = nonempty_string(state.get("status"), "assurance.evaluation.status")
    verdict = nonempty_string(state.get("verdict"), "assurance.evaluation.verdict")
    skip_reason = str(state.get("skip_reason") or "").strip()
    if status not in ASSURANCE_STATUSES:
        raise EvaluationError(f"unsupported evaluation assurance status: {status}")
    if required and status == "SKIPPED":
        raise EvaluationError("required evaluation cannot be SKIPPED")
    if not required and status == "SKIPPED":
        if not skip_reason:
            raise EvaluationError("skipped optional evaluation requires skip_reason")
        return {"required": required, "status": status, "verdict": verdict}
    if status == "PENDING":
        raise EvaluationError("evaluation assurance is still PENDING")
    if verdict not in EVALUATION_VERDICTS:
        raise EvaluationError(f"evaluation verdict is unresolved or invalid: {verdict}")

    plan_path = repo_relative_file(
        root, state.get("plan"), "assurance.evaluation.plan", "docs/evals/"
    )
    report_path = repo_relative_file(
        root, state.get("report"), "assurance.evaluation.report", "docs/reports/"
    )
    isolation = nonempty_string(state.get("isolation"), "assurance.evaluation.isolation")
    if isolation == "unknown":
        raise EvaluationError("evaluation isolation must record the actual boundary")
    rubric_revision = nonempty_string(
        state.get("rubric_revision"), "assurance.evaluation.rubric_revision"
    )
    benchmark_revision = nonempty_string(
        state.get("benchmark_revision"), "assurance.evaluation.benchmark_revision"
    )

    plan = load_json_object(plan_path, str(plan_path))
    report = load_json_object(report_path, str(report_path))
    plan_info = validate_plan(plan, require_approved=True)
    report_info = validate_report(report, plan)
    if plan_info["work_block_id"] != work_block_id:
        raise EvaluationError("evaluation plan Work Block does not match active Work Block")
    if rubric_revision != plan_info["rubric_revision"]:
        raise EvaluationError("active Work Block rubric revision does not match plan")
    if benchmark_revision != plan_info["benchmark_revision"]:
        raise EvaluationError("active Work Block benchmark revision does not match plan")
    if verdict != report_info["verdict"]:
        raise EvaluationError("active Work Block evaluation verdict does not match report")

    mode = str(gate.get("closeout_mode") or "")
    if mode == "success-closeout":
        if required and (status != "READY" or verdict != "READY"):
            raise EvaluationError(
                "success-closeout requires required evaluation status/verdict READY"
            )
        if status == "READY" and verdict != "READY":
            raise EvaluationError("evaluation READY status requires READY verdict")
    elif mode != "reporting-only":
        raise EvaluationError(
            "closeout_mode must be success-closeout or reporting-only for evaluation closeout"
        )

    return {
        "required": required,
        "status": status,
        "verdict": verdict,
        "plan": plan_path.as_posix(),
        "report": report_path.as_posix(),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("path", type=Path)
    plan_parser.add_argument("--require-approved", action="store_true")

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("report", type=Path)
    report_parser.add_argument("plan", type=Path)

    closeout_parser = subparsers.add_parser("closeout")
    closeout_parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(argv or sys.argv[1:]))
    try:
        if args.command == "plan":
            info = validate_plan(
                load_json_object(args.path, str(args.path)),
                require_approved=args.require_approved,
            )
        elif args.command == "report":
            plan = load_json_object(args.plan, str(args.plan))
            report = load_json_object(args.report, str(args.report))
            info = validate_report(report, plan)
        else:
            info = validate_closeout(args.root.resolve())
    except EvaluationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(info, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
