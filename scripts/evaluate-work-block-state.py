#!/usr/bin/env python3
"""Synthetic long-horizon evaluation for schema-v4 Work Block execution state.

The evaluation measures deterministic correctness and serialized UTF-8 context
bytes. It does not claim provider token savings.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "template/scripts/work-block-state.py"
STEPS = 60
NOISE_STEP = 20
SUBJECT_REPLACEMENT_STEP = 35


def load_engine() -> ModuleType:
    spec = importlib.util.spec_from_file_location("agentic_work_block_state_eval", ENGINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


STATE = load_engine()


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def init_repo(root: Path) -> str:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q", "-b", "feature")
    git(root, "config", "user.email", "fixture@example.com")
    git(root, "config", "user.name", "Fixture")
    (root / "README.md").write_text("state evaluation\n", encoding="utf-8")
    git(root, "add", "README.md")
    git(root, "commit", "-qm", "base")
    return git(root, "rev-parse", "HEAD")


def initial_state(head: str) -> dict:
    value = STATE.default_state("Managed", "evaluation")
    value["work_block_id"] = "WB-EVAL"
    value["specification"] = {"path": "docs/specs/eval.md", "revision": "spec-r1"}
    value["base_commit"] = head
    value["define_quality"] = {
        "required": True,
        "status": "READY",
        "requirements_review": "evidence://requirements",
        "traceability": "evidence://traceability",
        "consistency_analysis": "evidence://consistency",
    }
    value["critic"].update(
        status="READY",
        verdict="APPROVE",
        report="evidence://critic",
        isolation="separate_session",
    )
    value["write_gate"] = {"status": "READY", "opened_at": "2026-09-02T00:00:00+00:00"}
    value["write_set"] = ["src/**", "tests/**"]
    value["lifecycle"] = {"stage": "execute", "execution_state": "in_progress"}
    value["subject"] = {"current_revision": head, "frozen_revision": "", "generation": 1}
    value["progress"]["active_tasks"] = ["TASK-EVAL"]
    value["progress"]["next_action"] = "Continue evaluation transitions."
    STATE.validate_state(value)
    return value


def serialized_bytes(value: object) -> int:
    return len(STATE.canonical_json_bytes(value))


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="work-block-state-eval-") as temporary:
        root = Path(temporary) / "repo"
        head = init_repo(root)
        state_path = root / ".agent/active-work-block.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(initial_state(head), indent=2) + "\n", encoding="utf-8")

        history: list[dict[str, object]] = []
        state_context_total = 0
        history_context_total = 0
        state_context_max = 0
        history_context_max = 0
        correctness_failures: list[str] = []
        subject_replacement_observed = False

        for step in range(1, STEPS + 1):
            current = STATE.read_state(state_path)
            expected = current["state_version"]
            observation_ref = f"evidence://step-{step:03d}"
            observation_text = f"step={step}; operational observation"
            if step == NOISE_STEP:
                observation_text += "; raw_ci_noise=" + ("x" * 24000)

            history.append(
                {
                    "step": step,
                    "observation": observation_text,
                    "tool_result": "ok",
                }
            )

            if step == SUBJECT_REPLACEMENT_STEP:
                replacement = "d" * 40
                current = STATE.observe_revision(
                    state_path,
                    replacement,
                    observation_ref,
                    expected_version=expected,
                )
                subject_replacement_observed = (
                    current["subject"]["current_revision"] == replacement
                    and current["subject"]["generation"] == 2
                )
            else:
                current = STATE.patch_state(
                    state_path,
                    {
                        "progress.next_action": f"Execute transition {step + 1}",
                        "context.latest_observation_ref": observation_ref,
                    },
                    expected_version=expected,
                )

            compact = STATE.assemble_context(
                current,
                "procedure://sdd-protocol",
                latest_observation=observation_text if step != NOISE_STEP else observation_ref,
                selected_evidence=[observation_ref],
            )
            history_heavy = {
                "procedure_ref": "procedure://sdd-protocol",
                "state": current,
                "history": history,
                "latest_observation": observation_text,
            }
            compact_bytes = serialized_bytes(compact)
            history_bytes = serialized_bytes(history_heavy)
            state_context_total += compact_bytes
            history_context_total += history_bytes
            state_context_max = max(state_context_max, compact_bytes)
            history_context_max = max(history_context_max, history_bytes)

            if current["state_version"] != step:
                correctness_failures.append(
                    f"step {step}: state_version={current['state_version']}"
                )
            if len(current["context"]["current_evidence_refs"]) > STATE.MAX_EVIDENCE_REFS:
                correctness_failures.append(f"step {step}: evidence bound exceeded")

        final = STATE.read_state(state_path)
        stale_conflict_rejected = False
        try:
            STATE.patch_state(
                state_path,
                {"progress.next_action": "must not win"},
                expected_version=final["state_version"] - 1,
            )
        except STATE.StateError as exc:
            stale_conflict_rejected = "stale state_version" in str(exc)

        result = {
            "evaluation": "schema-v4-work-block-state",
            "steps": STEPS,
            "correctness": {
                "failures": correctness_failures,
                "subject_replacement_observed": subject_replacement_observed,
                "stale_conflict_rejected": stale_conflict_rejected,
                "final_state_version": final["state_version"],
            },
            "context_utf8_bytes": {
                "metric": "canonical serialized UTF-8 bytes; not provider tokens",
                "state_centric": {
                    "cumulative": state_context_total,
                    "max_per_step": state_context_max,
                },
                "history_heavy": {
                    "cumulative": history_context_total,
                    "max_per_step": history_context_max,
                },
                "ratio_history_to_state_cumulative": round(
                    history_context_total / state_context_total, 3
                ),
            },
            "noise": {
                "step": NOISE_STEP,
                "raw_noise_bytes": 24000,
                "default_future_state_retains_raw_noise": False,
            },
        }
        if correctness_failures or not subject_replacement_observed or not stale_conflict_rejected:
            print(json.dumps(result, indent=2, sort_keys=True))
            raise SystemExit(2)
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
