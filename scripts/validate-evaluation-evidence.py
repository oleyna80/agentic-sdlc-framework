#!/usr/bin/env python3
"""Validate an approved evaluation plan, report, and observable JSONL event ledger."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PORTABLE_VALIDATOR = ROOT / "template/scripts/validate-evaluation.py"

spec = importlib.util.spec_from_file_location("portable_evaluation", PORTABLE_VALIDATOR)
if spec is None or spec.loader is None:
    raise SystemExit(f"FAIL: cannot import {PORTABLE_VALIDATOR}")
portable = importlib.util.module_from_spec(spec)
spec.loader.exec_module(portable)
EvaluationError = portable.EvaluationError


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"invalid JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise EvaluationError(f"{path} must contain a JSON object")
    return value


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise EvaluationError(f"cannot read event ledger {path}: {exc}") from exc
    if not lines:
        raise EvaluationError("event ledger must not be empty")
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            raise EvaluationError(f"event ledger contains blank line {line_number}")
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise EvaluationError(
                f"invalid event JSON at line {line_number}: {exc}"
            ) from exc
        if not isinstance(event, dict):
            raise EvaluationError(f"event line {line_number} must be an object")
        portable.reject_hidden_reasoning(event, f"event[{line_number}]")
        if event.get("schema_version") != 1:
            raise EvaluationError(f"event line {line_number} requires schema_version=1")
        for field in (
            "event_id",
            "run_id",
            "work_block_id",
            "timestamp",
            "event_type",
            "logical_role",
            "runtime",
            "tool",
            "action",
            "target",
            "result",
            "evidence",
            "side_effect_class",
            "gate_decision",
            "notes",
        ):
            portable.nonempty_string(event.get(field), f"event[{line_number}].{field}")
        sequence = event.get("sequence")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 1:
            raise EvaluationError(
                f"event[{line_number}].sequence must be a positive integer"
            )
        events.append(event)
    return events


def validate(plan_path: Path, report_path: Path, events_path: Path) -> dict[str, Any]:
    plan = load_json(plan_path)
    report = load_json(report_path)
    plan_info = portable.validate_plan(plan, require_approved=True)
    report_info = portable.validate_report(report, plan)
    events = load_events(events_path)

    event_ids = [event["event_id"] for event in events]
    if len(set(event_ids)) != len(event_ids):
        raise EvaluationError("event ledger contains duplicate event_id values")
    sequences = [event["sequence"] for event in events]
    if sequences != list(range(1, len(events) + 1)):
        raise EvaluationError("event ledger sequence must be contiguous and ordered")
    if any(event["work_block_id"] != plan_info["work_block_id"] for event in events):
        raise EvaluationError("every event must match the evaluation Work Block")

    event_types = {event["event_type"] for event in events}
    for criterion in plan_info["trajectory"]:
        criterion_id = criterion["criterion_id"]
        required = set(criterion["required_events"])
        prohibited = set(criterion["prohibited_events"])
        missing = sorted(required.difference(event_types))
        observed_prohibited = sorted(prohibited.intersection(event_types))
        if missing:
            raise EvaluationError(
                f"event ledger misses required events for {criterion_id}: {', '.join(missing)}"
            )
        if observed_prohibited:
            raise EvaluationError(
                f"event ledger contains prohibited events for {criterion_id}: "
                + ", ".join(observed_prohibited)
            )

        report_result = next(
            item
            for item in report["trajectory_results"]
            if item["criterion_id"] == criterion_id
        )
        if set(report_result["observed_events"]) != required:
            raise EvaluationError(
                f"report observed_events must exactly match approved required events: {criterion_id}"
            )
        if report_result["missing_events"] or report_result["prohibited_events_observed"]:
            raise EvaluationError(
                f"READY trajectory report contains missing/prohibited events: {criterion_id}"
            )

    if report_info["verdict"] != "READY":
        raise EvaluationError("closeout evidence requires evaluation verdict READY")

    return {
        "evaluation_id": plan_info["evaluation_id"],
        "work_block_id": plan_info["work_block_id"],
        "subject_revision": report_info["subject_revision"],
        "verdict": report_info["verdict"],
        "events": len(events),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("events", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = validate(args.plan, args.report, args.events)
    except (EvaluationError, StopIteration) as exc:
        print(f"FAIL: evaluation evidence: {exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
