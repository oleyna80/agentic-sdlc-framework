#!/usr/bin/env python3
"""Deterministic fixtures for the schema-v4 Work Block execution-state engine."""
from __future__ import annotations

import copy
import importlib.util
import json
import multiprocessing as mp
from pathlib import Path
import subprocess
import tempfile
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "template/scripts/work-block-state.py"


def load_engine() -> ModuleType:
    spec = importlib.util.spec_from_file_location("agentic_work_block_state_test", ENGINE)
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
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def init_repo(root: Path) -> str:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q", "-b", "feature")
    git(root, "config", "user.email", "fixture@example.com")
    git(root, "config", "user.name", "Fixture")
    (root / "README.md").write_text("fixture\n", encoding="utf-8")
    git(root, "add", "README.md")
    git(root, "commit", "-qm", "base")
    return git(root, "rev-parse", "HEAD")


def initialized_state(head: str, *, profile: str = "Managed") -> dict:
    value = STATE.default_state(profile, "fixture")
    value["work_block_id"] = "WB-FIXTURE"
    value["specification"] = {
        "path": "docs/specs/fixture.md",
        "revision": "spec-r1",
    }
    value["base_commit"] = head
    value["subject"] = {
        "current_revision": head,
        "frozen_revision": "",
        "generation": 1,
    }
    value["define_quality"] = {
        "required": profile in STATE.FORMAL_PROFILES,
        "status": "READY" if profile in STATE.FORMAL_PROFILES else "PENDING",
        "requirements_review": "docs/reports/requirements/review.md" if profile in STATE.FORMAL_PROFILES else "",
        "traceability": "docs/reports/requirements/traceability.md" if profile in STATE.FORMAL_PROFILES else "",
        "consistency_analysis": "docs/reports/requirements/consistency.md" if profile in STATE.FORMAL_PROFILES else "",
    }
    value["critic"].update(
        status="READY",
        verdict="APPROVE",
        report="docs/reports/reviews/critic.md",
        isolation="separate_session",
    )
    value["write_gate"] = {"status": "READY", "opened_at": "2026-09-02T00:00:00+00:00"}
    value["write_set"] = ["src/**", "tests/**"]
    value["lifecycle"] = {"stage": "execute", "execution_state": "ready"}
    STATE.validate_state(value)
    return value


def write_state(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def assert_blocked(callable_, contains: str) -> None:
    try:
        callable_()
    except STATE.StateError as exc:
        assert contains in str(exc), str(exc)
    else:
        raise AssertionError(f"expected StateError containing {contains!r}")


def concurrent_patch(engine_path: str, state_path: str, version: int, marker: str, queue) -> None:
    spec = importlib.util.spec_from_file_location(f"state_worker_{marker}", engine_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        result = module.patch_state(
            Path(state_path),
            {"progress.next_action": marker},
            version,
            timeout=3.0,
        )
        queue.put(("ok", result["state_version"], result["progress"]["next_action"]))
    except module.StateError as exc:
        queue.put(("blocked", str(exc)))


def test_defaults_and_validation() -> None:
    controlled = STATE.default_state()
    managed = STATE.default_state("Managed")
    assert controlled["schema_version"] == 4
    assert controlled["state_version"] == 0
    assert controlled["write_gate"] == {"status": "BLOCKED", "opened_at": None}
    assert controlled["define_quality"]["required"] is False
    assert managed["define_quality"]["required"] is True
    assert managed["lifecycle"] == {"stage": "define", "execution_state": "blocked"}
    STATE.validate_state(controlled)
    STATE.validate_state(managed)


def test_patch_cas_and_authority_protection(root: Path, head: str) -> None:
    state_path = root / ".agent/active-work-block.json"
    write_state(state_path, initialized_state(head))
    first = STATE.patch_state(
        state_path,
        {"progress.next_action": "first"},
        expected_version=0,
    )
    assert first["state_version"] == 1
    assert first["progress"]["next_action"] == "first"
    assert_blocked(
        lambda: STATE.patch_state(
            state_path,
            {"progress.next_action": "stale"},
            expected_version=0,
        ),
        "stale state_version",
    )
    assert_blocked(
        lambda: STATE.patch_state(
            state_path,
            {"write_gate.status": "BLOCKED"},
            expected_version=1,
        ),
        "protected/unknown",
    )
    assert STATE.read_state(state_path)["progress"]["next_action"] == "first"


def test_real_concurrent_cas(root: Path, head: str) -> None:
    state_path = root / ".agent/active-work-block.json"
    write_state(state_path, initialized_state(head))
    ctx = mp.get_context("spawn")
    queue = ctx.Queue()
    workers = [
        ctx.Process(
            target=concurrent_patch,
            args=(str(ENGINE), str(state_path), 0, marker, queue),
        )
        for marker in ("worker-a", "worker-b")
    ]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(10)
        assert worker.exitcode == 0
    results = [queue.get(timeout=2) for _ in workers]
    assert sum(item[0] == "ok" for item in results) == 1, results
    assert sum(item[0] == "blocked" for item in results) == 1, results
    assert any("stale state_version" in str(item) for item in results if item[0] == "blocked")
    final = STATE.read_state(state_path)
    assert final["state_version"] == 1
    assert final["progress"]["next_action"] in {"worker-a", "worker-b"}


def test_subject_reconciliation_invalidates_assurance(root: Path, head: str) -> None:
    state_path = root / ".agent/active-work-block.json"
    value = initialized_state(head)
    value["write_gate"] = {"status": "BLOCKED", "opened_at": None}
    value["subject"]["frozen_revision"] = head
    value["assurance"]["review"].update(
        status="READY",
        verdict="READY",
        report="docs/reports/reviews/review.md",
    )
    value["assurance"]["verification"].update(
        status="READY",
        verdict="READY",
        report="docs/reports/verification/verification.md",
    )
    write_state(state_path, value)
    changed = "f" * 40
    result = STATE.observe_revision(
        state_path,
        changed,
        "evidence://remote-head-changed",
        expected_version=0,
    )
    assert result["subject"]["current_revision"] == changed
    assert result["subject"]["frozen_revision"] == ""
    assert result["subject"]["generation"] == 2
    assert result["assurance"]["review"]["status"] == "BLOCKED"
    assert result["assurance"]["review"]["verdict"] == "UNVERIFIED"
    assert result["assurance"]["verification"]["status"] == "BLOCKED"
    assert "evidence://remote-head-changed" in result["context"]["current_evidence_refs"]


def test_handoff_is_authority_attenuating(root: Path, head: str) -> None:
    source_path = root / ".agent/source.json"
    target_path = root / ".agent/target.json"
    snapshot_path = root / ".agent/handoff.json"
    source = initialized_state(head)
    source["progress"]["active_tasks"] = ["TASK-005"]
    source["progress"]["next_action"] = "Run adapter migration"
    source["context"]["current_evidence_refs"] = ["evidence://source"]
    source["integrations"] = {
        "approved": ["codex-cloud"],
        "admission_records": ["docs/reports/integrations/codex-cloud.md"],
    }
    write_state(source_path, source)
    snapshot = STATE.export_handoff(source_path, root, snapshot_path)
    assert snapshot["source"]["repository_revision"] == head
    assert "write_gate" not in snapshot["operational"]
    assert "integrations" not in snapshot["operational"]

    target = initialized_state(head)
    target["write_gate"] = {"status": "BLOCKED", "opened_at": None}
    target["integrations"] = {"approved": [], "admission_records": []}
    target["assurance"]["review"].update(
        status="READY",
        verdict="READY",
        report="docs/reports/reviews/target.md",
    )
    write_state(target_path, target)
    imported = STATE.import_handoff(
        target_path,
        root,
        snapshot_path,
        "evidence://handoff",
        expected_version=0,
    )
    assert imported["write_gate"] == {"status": "BLOCKED", "opened_at": None}
    assert imported["integrations"] == {"approved": [], "admission_records": []}
    assert imported["progress"]["active_tasks"] == ["TASK-005"]
    assert imported["context"]["handoff_snapshot_ref"] == "evidence://handoff"


def legacy_v3(head: str) -> dict:
    current = initialized_state(head)
    legacy = copy.deepcopy(current)
    legacy.pop("state_version", None)
    legacy.pop("lifecycle", None)
    legacy.pop("subject", None)
    legacy.pop("progress", None)
    legacy.pop("context", None)
    legacy["schema_version"] = 3
    legacy["write_gate"] = {"status": "READY", "opened_at": "2026-09-02T00:00:00+00:00"}
    legacy["integrations"] = {
        "approved": ["codex-cli"],
        "admission_records": ["docs/reports/integrations/codex-cli.md"],
    }
    legacy["assurance"]["review"].update(
        status="READY",
        verdict="READY",
        report="docs/reports/reviews/legacy.md",
    )
    return legacy


def test_v3_migration_fails_closed(root: Path, head: str) -> None:
    state_path = root / ".agent/active-work-block.json"
    write_state(state_path, legacy_v3(head))
    migrated = STATE.migrate_v3(state_path)
    assert migrated["schema_version"] == 4
    assert migrated["state_version"] == 0
    assert migrated["write_gate"] == {"status": "BLOCKED", "opened_at": None}
    assert migrated["integrations"] == {"approved": [], "admission_records": []}
    assert migrated["lifecycle"] == {"stage": "define", "execution_state": "blocked"}
    assert migrated["assurance"]["review"]["status"] == "BLOCKED"
    assert migrated["assurance"]["review"]["verdict"] == "UNVERIFIED"
    assert "Revalidate migrated" in migrated["progress"]["next_action"]


def test_context_metric(head: str) -> None:
    value = initialized_state(head)
    assembled = STATE.assemble_context(
        value,
        "procedure://sdd",
        latest_observation="latest observation",
        selected_evidence=["evidence://1"],
    )
    size = len(STATE.canonical_json_bytes(assembled))
    assert size > 0
    assert "history" not in assembled
    assert set(assembled) == {
        "procedure_ref",
        "state",
        "latest_observation",
        "selected_evidence",
    }


def main() -> None:
    test_defaults_and_validation()
    with tempfile.TemporaryDirectory(prefix="work-block-state-v4-") as temporary:
        root = Path(temporary) / "repo"
        head = init_repo(root)
        test_patch_cas_and_authority_protection(root, head)
        test_real_concurrent_cas(root, head)
        test_subject_reconciliation_invalidates_assurance(root, head)
        test_handoff_is_authority_attenuating(root, head)
        test_v3_migration_fails_closed(root, head)
        test_context_metric(head)
    print("Schema-v4 Work Block execution-state fixtures: OK")


if __name__ == "__main__":
    main()
