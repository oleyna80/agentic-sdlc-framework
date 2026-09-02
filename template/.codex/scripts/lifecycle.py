#!/usr/bin/env python3
"""Schema-v4 local Work Block lifecycle helper.

The helper is a Codex compatibility adapter over the provider-neutral execution
state engine. It manages cooperative project-local state; it does not create
external security authority.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any


def load_state_tool() -> ModuleType:
    path = Path(__file__).resolve().parents[2] / "scripts/work-block-state.py"
    spec = importlib.util.spec_from_file_location("agentic_work_block_state", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load execution state engine: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


STATE = load_state_tool()
SCHEMA_VERSION = STATE.SCHEMA_VERSION
AUTHORITY_MODE = STATE.AUTHORITY_MODE
FORMAL_PROFILES = STATE.FORMAL_PROFILES
VALID_PROFILES = STATE.VALID_PROFILES
ASSURANCE_STATUSES = STATE.VALID_ASSURANCE_STATUSES
ASSURANCE_VERDICTS = STATE.VALID_ASSURANCE_VERDICTS


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def validate_open(args: argparse.Namespace) -> None:
    if not args.work_block_id.strip():
        raise STATE.StateError("open requires a non-empty --work-block-id")
    if args.governance_profile not in VALID_PROFILES:
        raise STATE.StateError("open requires a known --governance-profile")
    if args.governance_profile == "Advisory":
        raise STATE.StateError("Advisory profile cannot open source writes")
    if not args.specification_path.strip():
        raise STATE.StateError("open requires --specification-path")
    if not args.specification_revision.strip():
        raise STATE.StateError("open requires --specification-revision")
    writes = [value.strip() for value in args.write if value.strip()]
    if not writes:
        raise STATE.StateError("open requires at least one --write path")
    if args.critic_status not in {"READY", "DEGRADED", "FALLBACK", "SKIPPED"}:
        raise STATE.StateError("open requires a resolved Critic status")
    if args.governance_profile in FORMAL_PROFILES and args.critic_status == "SKIPPED":
        raise STATE.StateError(f"{args.governance_profile} cannot skip the Critic gate")
    if args.critic_status == "SKIPPED":
        if not args.critic_skip_reason.strip():
            raise STATE.StateError("SKIPPED Critic requires --critic-skip-reason")
    elif args.critic_verdict not in {"APPROVE", "SUPPLEMENT"}:
        raise STATE.StateError("resolved Critic requires APPROVE or SUPPLEMENT verdict")
    if args.critic_status != "SKIPPED" and not args.critic_report.strip():
        raise STATE.StateError("resolved Critic requires --critic-report")

    quality_refs = [
        args.requirements_review.strip(),
        args.traceability.strip(),
        args.consistency_analysis.strip(),
    ]
    if args.governance_profile in FORMAL_PROFILES and not all(quality_refs):
        raise STATE.StateError(
            f"{args.governance_profile} open requires requirements-review, traceability, and consistency evidence"
        )
    if any(quality_refs) and not all(quality_refs):
        raise STATE.StateError("Define-quality evidence must be supplied as a complete set")


def open_replacement(root: Path, args: argparse.Namespace, current: dict[str, Any]) -> dict[str, Any]:
    validate_open(args)
    value = STATE.default_state(
        args.governance_profile, "source work opened by Work Block coordination"
    )
    value["work_block_id"] = args.work_block_id.strip()
    value["governance_profile"] = args.governance_profile
    value["specification"] = {
        "path": args.specification_path.strip(),
        "revision": args.specification_revision.strip(),
    }
    revision = STATE.git_head(root)
    value["base_commit"] = revision
    value["subject"] = {
        "current_revision": revision,
        "frozen_revision": "",
        "generation": 1,
    }
    value["write_gate"] = {"status": "READY", "opened_at": now()}
    value["write_set"] = list(dict.fromkeys(v.strip() for v in args.write if v.strip()))
    value["critic"] = {
        "required": True,
        "status": args.critic_status,
        "verdict": args.critic_verdict if args.critic_status != "SKIPPED" else "SKIPPED",
        "report": args.critic_report.strip(),
        "isolation": args.critic_isolation,
        "skip_reason": args.critic_skip_reason.strip(),
    }
    refs = [
        args.requirements_review.strip(),
        args.traceability.strip(),
        args.consistency_analysis.strip(),
    ]
    if all(refs):
        value["define_quality"] = {
            "required": args.governance_profile in FORMAL_PROFILES,
            "status": "READY",
            "requirements_review": refs[0],
            "traceability": refs[1],
            "consistency_analysis": refs[2],
        }
    value["assurance"]["evaluation"]["required"] = args.evaluation_required
    value["assurance"]["drift"]["required"] = args.drift_required
    value["lifecycle"] = {"stage": "execute", "execution_state": "ready"}
    value["progress"]["next_action"] = "Execute the approved write-set and freeze the exact subject for assurance."
    if isinstance(current.get("integrations"), dict):
        value["integrations"] = copy.deepcopy(current["integrations"])
    if isinstance(current.get("coordination_write_set"), list):
        value["coordination_write_set"] = list(current["coordination_write_set"])
    return value


def validate_closeout_state(current: dict[str, Any], mode: str) -> None:
    STATE.validate_state(current)
    assurance = current["assurance"]
    normalized: dict[str, tuple[bool, str, str]] = {}
    for name in ("review", "verification", "evaluation", "drift"):
        item = assurance[name]
        required = item["required"] is True
        status = str(item["status"])
        verdict = str(item["verdict"])
        skip_reason = str(item.get("skip_reason") or "").strip()
        if status not in ASSURANCE_STATUSES:
            raise STATE.StateError(f"assurance.{name}.status is invalid or missing")
        if status == "PENDING":
            raise STATE.StateError(f"assurance.{name} is still PENDING")
        if status == "SKIPPED":
            if required:
                raise STATE.StateError(f"required assurance.{name} cannot be SKIPPED")
            if not skip_reason:
                raise STATE.StateError(f"skipped assurance.{name} requires skip_reason")
        elif verdict not in ASSURANCE_VERDICTS[name]:
            raise STATE.StateError(f"assurance.{name}.verdict is unresolved or invalid")
        normalized[name] = (required, status, verdict)

    if mode != "success-closeout":
        return
    required_review, review_status, review_verdict = normalized["review"]
    required_verification, verification_status, verification_verdict = normalized[
        "verification"
    ]
    required_evaluation, evaluation_status, evaluation_verdict = normalized["evaluation"]
    required_drift, drift_status, drift_verdict = normalized["drift"]
    if required_review and (review_status != "READY" or review_verdict != "READY"):
        raise STATE.StateError("success-closeout requires assurance.review READY/READY")
    if required_verification and (
        verification_status != "READY" or verification_verdict != "READY"
    ):
        raise STATE.StateError("success-closeout requires assurance.verification READY/READY")
    if required_evaluation and (
        evaluation_status != "READY" or evaluation_verdict != "READY"
    ):
        raise STATE.StateError("success-closeout requires assurance.evaluation READY/READY")
    if required_drift and (drift_status != "READY" or drift_verdict != "ALIGNED"):
        raise STATE.StateError("success-closeout requires assurance.drift READY/ALIGNED")


def prepare_state(state_path: Path, reason: str, timeout: float) -> dict[str, Any]:
    with STATE.state_lock(state_path, timeout):
        if state_path.exists():
            current = STATE.read_state(state_path)
            if current.get("schema_version") == 3:
                raise STATE.StateError("schema-v3 state requires migrate-v3 before prepare")
            STATE.validate_state(current)
            version = current["state_version"] + 1
        else:
            version = 0
        value = STATE.default_state("Controlled", reason)
        value["state_version"] = version
        STATE.validate_state(value)
        STATE.atomic_write(state_path, value)
        return value


def record_assurance(state_path: Path, args: argparse.Namespace, timeout: float) -> dict[str, Any]:
    def mutate(state: dict[str, Any]) -> None:
        item = state["assurance"][args.name]
        if args.status == "SKIPPED" and item["required"]:
            raise STATE.StateError(f"required assurance.{args.name} cannot be SKIPPED")
        if args.status == "SKIPPED" and not args.skip_reason.strip():
            raise STATE.StateError("SKIPPED assurance requires --skip-reason")
        if args.status == "READY" and not args.report.strip():
            raise STATE.StateError("READY assurance requires --report")
        item["status"] = args.status
        item["verdict"] = args.verdict
        item["report"] = args.report.strip()
        item["isolation"] = args.isolation
        item["skip_reason"] = args.skip_reason.strip()
        if args.name == "evaluation":
            if args.plan is not None:
                item["plan"] = args.plan.strip()
            if args.rubric_revision is not None:
                item["rubric_revision"] = args.rubric_revision.strip()
            if args.benchmark_revision is not None:
                item["benchmark_revision"] = args.benchmark_revision.strip()
        state["lifecycle_note"] = f"assurance.{args.name} recorded"

    return STATE.transaction(
        state_path,
        mutate,
        expected_version=args.expected_version,
        timeout=timeout,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--state", type=Path, default=Path(".agent/active-work-block.json")
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--lock-timeout", type=float, default=STATE.DEFAULT_LOCK_TIMEOUT)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status")

    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--reason", default="coordination")

    opening = subparsers.add_parser("open")
    opening.add_argument("--expected-version", type=int, required=True)
    opening.add_argument("--work-block-id", required=True)
    opening.add_argument("--specification-path", required=True)
    opening.add_argument("--specification-revision", required=True)
    opening.add_argument("--write", action="append", default=[])
    opening.add_argument("--governance-profile", default="Controlled")
    opening.add_argument("--requirements-review", default="")
    opening.add_argument("--traceability", default="")
    opening.add_argument("--consistency-analysis", default="")
    opening.add_argument("--critic-status", default="READY")
    opening.add_argument("--critic-verdict", default="APPROVE")
    opening.add_argument("--critic-report", default="")
    opening.add_argument("--critic-isolation", default="same_context")
    opening.add_argument("--critic-skip-reason", default="")
    opening.add_argument("--evaluation-required", action="store_true")
    opening.add_argument("--drift-required", action="store_true")

    freeze = subparsers.add_parser("freeze")
    freeze.add_argument("--expected-version", type=int, required=True)
    freeze.add_argument("--reason", required=True)
    freeze.add_argument("--evidence-ref", required=True)

    assurance = subparsers.add_parser("assurance")
    assurance.add_argument("--expected-version", type=int, required=True)
    assurance.add_argument("--name", choices=("review", "verification", "evaluation", "drift"), required=True)
    assurance.add_argument("--status", choices=tuple(sorted(ASSURANCE_STATUSES)), required=True)
    assurance.add_argument("--verdict", required=True)
    assurance.add_argument("--report", default="")
    assurance.add_argument("--isolation", default="unknown")
    assurance.add_argument("--skip-reason", default="")
    assurance.add_argument("--plan")
    assurance.add_argument("--rubric-revision")
    assurance.add_argument("--benchmark-revision")

    close = subparsers.add_parser("close")
    close.add_argument("--expected-version", type=int, required=True)
    close.add_argument("--reason", required=True)
    close.add_argument(
        "--mode", choices=("success-closeout", "reporting-only"), required=True
    )

    subparsers.add_parser("migrate-v3")

    args = parser.parse_args()
    root = args.root.resolve()
    state_path = args.state if args.state.is_absolute() else root / args.state

    if args.command == "status":
        value = STATE.read_state(state_path)
        STATE.validate_state(value)
        print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        return 0
    if args.command == "prepare":
        value = prepare_state(state_path, args.reason, args.lock_timeout)
    elif args.command == "migrate-v3":
        value = STATE.migrate_v3(state_path, timeout=args.lock_timeout)
    elif args.command == "open":
        validate_open(args)

        def mutate(current: dict[str, Any]) -> None:
            replacement = open_replacement(root, args, current)
            version = current["state_version"]
            current.clear()
            current.update(replacement)
            current["state_version"] = version

        value = STATE.transaction(
            state_path,
            mutate,
            expected_version=args.expected_version,
            timeout=args.lock_timeout,
        )
    elif args.command == "freeze":
        revision = STATE.git_head(root)

        def mutate(current: dict[str, Any]) -> None:
            previous_frozen = current["subject"]["frozen_revision"]
            STATE._set_subject_revision(current, revision, args.evidence_ref)
            if previous_frozen and previous_frozen != revision:
                STATE._unbind_assurance(current)
            current["subject"]["frozen_revision"] = revision
            current["write_gate"] = {"status": "BLOCKED", "opened_at": None}
            current["lifecycle"] = {"stage": "assure", "execution_state": "ready"}
            current["lifecycle_note"] = args.reason

        value = STATE.transaction(
            state_path,
            mutate,
            expected_version=args.expected_version,
            timeout=args.lock_timeout,
        )
    elif args.command == "assurance":
        if args.verdict not in ASSURANCE_VERDICTS[args.name] and not (
            args.status == "SKIPPED" and args.verdict == "PENDING"
        ):
            raise STATE.StateError(f"invalid verdict for assurance.{args.name}")
        value = record_assurance(state_path, args, args.lock_timeout)
    else:
        current = STATE.read_state(state_path)
        STATE.validate_state(current)
        if current["state_version"] != args.expected_version:
            raise STATE.StateError(
                f"stale state_version: expected {args.expected_version}, current {current['state_version']}"
            )
        validate_closeout_state(current, args.mode)

        def mutate(current_state: dict[str, Any]) -> None:
            validate_closeout_state(current_state, args.mode)
            current_state["write_gate"] = {"status": "BLOCKED", "opened_at": None}
            current_state["closeout_mode"] = args.mode
            current_state["lifecycle"] = {"stage": "close", "execution_state": "completed"}
            current_state["lifecycle_note"] = args.reason

        value = STATE.transaction(
            state_path,
            mutate,
            expected_version=args.expected_version,
            timeout=args.lock_timeout,
        )

    print(json.dumps(value, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except STATE.StateError as exc:
        print(f"BLOCKED: {exc}")
        raise SystemExit(2)
