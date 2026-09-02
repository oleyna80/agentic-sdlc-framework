#!/usr/bin/env python3
"""Provider-neutral schema-v4 Work Block execution-state engine.

The local state and lock are cooperative process controls, not a security boundary.
Consequential authority remains outside the mutable project wherever practical.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from typing import Any, Callable, Iterator

SCHEMA_VERSION = 4
SNAPSHOT_SCHEMA_VERSION = 1
AUTHORITY_MODE = "github_capability"
FORMAL_PROFILES = {"Managed", "Assured", "Distributed"}
VALID_PROFILES = {"Advisory", "Controlled", "Managed", "Assured", "Distributed"}
VALID_STAGES = {"define", "execute", "assure", "close"}
VALID_EXECUTION_STATES = {"blocked", "ready", "in_progress", "completed"}
VALID_DEFINE_STATUSES = {"PENDING", "READY", "BLOCKED"}
VALID_ASSURANCE_STATUSES = {"PENDING", "READY", "SKIPPED", "DEGRADED", "BLOCKED"}
VALID_ASSURANCE_VERDICTS = {
    "review": {"PENDING", "READY", "CHANGES_REQUIRED", "BLOCKED", "UNVERIFIED"},
    "verification": {"PENDING", "READY", "BLOCKED", "UNVERIFIED"},
    "evaluation": {"PENDING", "READY", "BLOCKED", "UNVERIFIED"},
    "drift": {"PENDING", "ALIGNED", "ALIGNMENT_REQUIRED", "BLOCKED", "UNVERIFIED"},
}
MAX_EVIDENCE_REFS = 16
MAX_CURRENT_ITEMS = 32
MAX_ITEM_CHARS = 4096
DEFAULT_LOCK_TIMEOUT = 5.0
DEFAULT_COORDINATION = [
    ".agent/active-work-block.json",
    ".agent/critic-gate.md",
    ".agent/verification-gate.md",
    ".codex/write-gate.md",
    "docs/plans/**",
    "docs/specs/**",
    "docs/tasklist/**",
    "docs/reports/**",
    "docs/architecture/drafts/**",
    "memory_bank/**",
]
EXTERNAL_HARD_STOPS = [
    "protected_default_branch_mutation",
    "destructive",
    "live_infra",
    "live_data",
    "credentials",
    "client_communications",
    "irreversible_publish",
]
PATCHABLE_PATHS = {
    "progress.active_tasks",
    "progress.blockers",
    "progress.pending_decisions",
    "progress.next_action",
    "context.latest_observation_ref",
    "context.current_evidence_refs",
}


class StateError(RuntimeError):
    """Fail-closed state contract violation."""


def _string(value: object, label: str, *, allow_empty: bool = True) -> str:
    if not isinstance(value, str):
        raise StateError(f"{label} must be a string")
    if not allow_empty and not value.strip():
        raise StateError(f"{label} must be non-empty")
    if len(value) > MAX_ITEM_CHARS:
        raise StateError(f"{label} exceeds {MAX_ITEM_CHARS} characters")
    return value


def _int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise StateError(f"{label} must be a non-negative integer")
    return value


def _string_list(
    value: object,
    label: str,
    *,
    maximum: int = MAX_CURRENT_ITEMS,
    allow_empty_items: bool = False,
) -> list[str]:
    if not isinstance(value, list):
        raise StateError(f"{label} must be an array")
    if len(value) > maximum:
        raise StateError(f"{label} exceeds maximum item count {maximum}")
    result: list[str] = []
    for index, item in enumerate(value):
        text = _string(item, f"{label}[{index}]", allow_empty=allow_empty_items)
        if not allow_empty_items and not text.strip():
            raise StateError(f"{label}[{index}] must be non-empty")
        result.append(text)
    if len(set(result)) != len(result):
        raise StateError(f"{label} contains duplicate entries")
    return result


def default_define_quality(profile: str = "Controlled") -> dict[str, Any]:
    return {
        "required": profile in FORMAL_PROFILES,
        "status": "PENDING",
        "requirements_review": "",
        "traceability": "",
        "consistency_analysis": "",
    }


def _assurance_entry(*, evaluation: bool = False) -> dict[str, Any]:
    value: dict[str, Any] = {
        "required": False if evaluation else True,
        "status": "PENDING",
        "verdict": "PENDING",
    }
    if evaluation:
        value.update(
            plan="",
            report="",
            rubric_revision="",
            benchmark_revision="",
            isolation="unknown",
            skip_reason="",
        )
    else:
        value.update(report="", isolation="unknown", skip_reason="")
    return value


def default_state(profile: str = "Controlled", reason: str = "coordination") -> dict[str, Any]:
    if profile not in VALID_PROFILES:
        raise StateError(f"unknown governance profile: {profile}")
    review = _assurance_entry()
    verification = _assurance_entry()
    evaluation = _assurance_entry(evaluation=True)
    drift = _assurance_entry(evaluation=True)
    drift.pop("plan", None)
    drift.pop("rubric_revision", None)
    drift.pop("benchmark_revision", None)
    return {
        "schema_version": SCHEMA_VERSION,
        "state_version": 0,
        "authority_mode": AUTHORITY_MODE,
        "work_block_id": "",
        "governance_profile": profile,
        "specification": {"path": "", "revision": ""},
        "base_commit": "",
        "define_quality": default_define_quality(profile),
        "write_gate": {"status": "BLOCKED", "opened_at": None},
        "critic": {
            "required": True,
            "status": "PENDING",
            "verdict": "PENDING",
            "report": "",
            "isolation": "unknown",
            "skip_reason": "",
        },
        "assurance": {
            "review": review,
            "verification": verification,
            "evaluation": evaluation,
            "drift": drift,
        },
        "closeout_mode": "pending",
        "integrations": {"approved": [], "admission_records": []},
        "write_set": [],
        "coordination_write_set": DEFAULT_COORDINATION.copy(),
        "external_hard_stops": EXTERNAL_HARD_STOPS.copy(),
        "lifecycle": {"stage": "define", "execution_state": "blocked"},
        "subject": {"current_revision": "", "frozen_revision": "", "generation": 0},
        "progress": {
            "active_tasks": [],
            "blockers": [],
            "pending_decisions": [],
            "next_action": "",
        },
        "context": {
            "latest_observation_ref": "",
            "current_evidence_refs": [],
            "handoff_snapshot_ref": "",
        },
        "lifecycle_note": reason,
    }


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def read_state(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StateError(f"invalid state {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise StateError("state must be a JSON object")
    return value


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False
        ) as out:
            json.dump(value, out, ensure_ascii=False, indent=2)
            out.write("\n")
            out.flush()
            os.fsync(out.fileno())
            temporary = Path(out.name)
        os.replace(temporary, path)
        temporary = None
        if os.name == "posix" and hasattr(os, "O_DIRECTORY"):
            try:
                directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            except OSError:
                pass
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass


@contextmanager
def state_lock(state_path: Path, timeout: float = DEFAULT_LOCK_TIMEOUT) -> Iterator[None]:
    if timeout <= 0:
        raise StateError("lock timeout must be positive")
    lock_path = state_path.with_name(state_path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("a+b")
    deadline = time.monotonic() + timeout
    acquired = False
    try:
        if os.name == "posix":
            import fcntl

            while True:
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise StateError("state lock timeout")
                    time.sleep(0.05)
        elif os.name == "nt":
            import msvcrt

            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"\0")
                handle.flush()
            while True:
                try:
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    acquired = True
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        raise StateError("state lock timeout")
                    time.sleep(0.05)
        else:
            raise StateError(f"unsupported state-lock platform: {os.name}")
        yield
    finally:
        if acquired:
            try:
                if os.name == "posix":
                    import fcntl

                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
                elif os.name == "nt":
                    import msvcrt

                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            except OSError:
                pass
        handle.close()


def _validate_define_quality(value: object, profile: str) -> None:
    if not isinstance(value, dict):
        raise StateError("define_quality must be an object")
    required = value.get("required")
    if not isinstance(required, bool):
        raise StateError("define_quality.required must be boolean")
    if profile in FORMAL_PROFILES and required is not True:
        raise StateError(f"{profile} requires define_quality.required=true")
    status = value.get("status")
    if status not in VALID_DEFINE_STATUSES:
        raise StateError("define_quality.status must be PENDING, READY, or BLOCKED")
    for field in ("requirements_review", "traceability", "consistency_analysis"):
        _string(value.get(field), f"define_quality.{field}")
    if required and status == "READY":
        for field in ("requirements_review", "traceability", "consistency_analysis"):
            if not str(value.get(field) or "").strip():
                raise StateError(f"READY define_quality requires {field} evidence")


def _validate_assurance(value: object) -> None:
    if not isinstance(value, dict):
        raise StateError("assurance must be an object")
    if set(value) != {"review", "verification", "evaluation", "drift"}:
        raise StateError("assurance must contain review, verification, evaluation, and drift")
    for name in ("review", "verification", "evaluation", "drift"):
        item = value.get(name)
        if not isinstance(item, dict):
            raise StateError(f"assurance.{name} must be an object")
        if not isinstance(item.get("required"), bool):
            raise StateError(f"assurance.{name}.required must be boolean")
        if item.get("status") not in VALID_ASSURANCE_STATUSES:
            raise StateError(f"assurance.{name}.status is invalid")
        if item.get("verdict") not in VALID_ASSURANCE_VERDICTS[name]:
            raise StateError(f"assurance.{name}.verdict is invalid")
        for field in ("report", "isolation", "skip_reason"):
            _string(item.get(field), f"assurance.{name}.{field}")
        if name == "evaluation":
            for field in ("plan", "rubric_revision", "benchmark_revision"):
                _string(item.get(field), f"assurance.evaluation.{field}")


def validate_state(value: dict[str, Any]) -> None:
    if value.get("schema_version") != SCHEMA_VERSION:
        raise StateError(f"state requires schema_version={SCHEMA_VERSION}")
    _int(value.get("state_version"), "state_version")
    if value.get("authority_mode") != AUTHORITY_MODE:
        raise StateError(f"state requires authority_mode={AUTHORITY_MODE}")
    _string(value.get("work_block_id"), "work_block_id")
    profile = _string(value.get("governance_profile"), "governance_profile", allow_empty=False)
    if profile not in VALID_PROFILES:
        raise StateError(f"unknown governance_profile: {profile}")
    specification = value.get("specification")
    if not isinstance(specification, dict):
        raise StateError("specification must be an object")
    _string(specification.get("path"), "specification.path")
    _string(specification.get("revision"), "specification.revision")
    _string(value.get("base_commit"), "base_commit")
    _validate_define_quality(value.get("define_quality"), profile)

    write_gate = value.get("write_gate")
    if not isinstance(write_gate, dict) or write_gate.get("status") not in {"BLOCKED", "READY"}:
        raise StateError("write_gate must be BLOCKED or READY")
    opened_at = write_gate.get("opened_at")
    if opened_at is not None:
        _string(opened_at, "write_gate.opened_at", allow_empty=False)

    critic = value.get("critic")
    if not isinstance(critic, dict):
        raise StateError("critic must be an object")
    if not isinstance(critic.get("required"), bool):
        raise StateError("critic.required must be boolean")
    for field in ("status", "verdict", "report", "isolation", "skip_reason"):
        _string(critic.get(field), f"critic.{field}")

    _validate_assurance(value.get("assurance"))
    _string(value.get("closeout_mode"), "closeout_mode", allow_empty=False)

    integrations = value.get("integrations")
    if not isinstance(integrations, dict):
        raise StateError("integrations must be an object")
    _string_list(integrations.get("approved"), "integrations.approved")
    _string_list(integrations.get("admission_records"), "integrations.admission_records")
    _string_list(value.get("write_set"), "write_set", maximum=512)
    _string_list(value.get("coordination_write_set"), "coordination_write_set", maximum=512)
    _string_list(value.get("external_hard_stops"), "external_hard_stops", maximum=128)

    lifecycle = value.get("lifecycle")
    if not isinstance(lifecycle, dict):
        raise StateError("lifecycle must be an object")
    if lifecycle.get("stage") not in VALID_STAGES:
        raise StateError("lifecycle.stage is invalid")
    if lifecycle.get("execution_state") not in VALID_EXECUTION_STATES:
        raise StateError("lifecycle.execution_state is invalid")

    subject = value.get("subject")
    if not isinstance(subject, dict):
        raise StateError("subject must be an object")
    _string(subject.get("current_revision"), "subject.current_revision")
    _string(subject.get("frozen_revision"), "subject.frozen_revision")
    _int(subject.get("generation"), "subject.generation")

    progress = value.get("progress")
    if not isinstance(progress, dict):
        raise StateError("progress must be an object")
    _string_list(progress.get("active_tasks"), "progress.active_tasks")
    _string_list(progress.get("blockers"), "progress.blockers")
    _string_list(progress.get("pending_decisions"), "progress.pending_decisions")
    _string(progress.get("next_action"), "progress.next_action")

    context = value.get("context")
    if not isinstance(context, dict):
        raise StateError("context must be an object")
    _string(context.get("latest_observation_ref"), "context.latest_observation_ref")
    _string_list(
        context.get("current_evidence_refs"),
        "context.current_evidence_refs",
        maximum=MAX_EVIDENCE_REFS,
    )
    _string(context.get("handoff_snapshot_ref"), "context.handoff_snapshot_ref")
    _string(value.get("lifecycle_note", ""), "lifecycle_note")


def git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
        timeout=5,
    )
    if result.returncode != 0:
        raise StateError("cannot resolve git HEAD")
    return result.stdout.strip()


def git_branch(root: Path) -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
        timeout=5,
    )
    if result.returncode != 0:
        raise StateError("cannot resolve git branch")
    branch = result.stdout.strip()
    return branch or "DETACHED"


def _append_evidence(state: dict[str, Any], evidence_ref: str) -> None:
    evidence_ref = _string(evidence_ref, "evidence_ref", allow_empty=False).strip()
    refs = list(state["context"]["current_evidence_refs"])
    if evidence_ref not in refs:
        refs.append(evidence_ref)
    if len(refs) > MAX_EVIDENCE_REFS:
        raise StateError(
            f"current evidence exceeds maximum {MAX_EVIDENCE_REFS}; retire a current pointer first"
        )
    state["context"]["current_evidence_refs"] = refs


def _unbind_assurance(state: dict[str, Any]) -> None:
    for name, item in state["assurance"].items():
        if item.get("status") == "READY":
            item["status"] = "BLOCKED"
            item["verdict"] = "UNVERIFIED"
            item["skip_reason"] = ""


def _set_subject_revision(
    state: dict[str, Any], revision: str, evidence_ref: str
) -> None:
    revision = _string(revision, "revision", allow_empty=False).strip()
    subject = state["subject"]
    old_current = subject["current_revision"]
    old_frozen = subject["frozen_revision"]
    if revision != old_current:
        subject["current_revision"] = revision
        subject["generation"] += 1
        if old_frozen and old_frozen != revision:
            subject["frozen_revision"] = ""
        _unbind_assurance(state)
        state["progress"]["next_action"] = (
            "Reconcile/freeze the current subject and rerun assurance required for the new subject."
        )
    state["context"]["latest_observation_ref"] = evidence_ref
    _append_evidence(state, evidence_ref)


def transaction(
    state_path: Path,
    mutator: Callable[[dict[str, Any]], None],
    *,
    expected_version: int | None = None,
    timeout: float = DEFAULT_LOCK_TIMEOUT,
) -> dict[str, Any]:
    with state_lock(state_path, timeout):
        current = read_state(state_path)
        validate_state(current)
        current_version = current["state_version"]
        if expected_version is not None and current_version != expected_version:
            raise StateError(
                f"stale state_version: expected {expected_version}, current {current_version}"
            )
        candidate = copy.deepcopy(current)
        mutator(candidate)
        if candidate.get("state_version") != current_version:
            raise StateError("state_version is reducer-owned")
        candidate["state_version"] = current_version + 1
        validate_state(candidate)
        atomic_write(state_path, candidate)
        return candidate


def patch_state(
    state_path: Path,
    changes: dict[str, Any],
    expected_version: int,
    *,
    timeout: float = DEFAULT_LOCK_TIMEOUT,
) -> dict[str, Any]:
    if not isinstance(changes, dict) or not changes:
        raise StateError("patch requires a non-empty JSON object")
    unknown = sorted(set(changes).difference(PATCHABLE_PATHS))
    if unknown:
        raise StateError("generic patch contains protected/unknown paths: " + ", ".join(unknown))

    def mutate(state: dict[str, Any]) -> None:
        for path, value in changes.items():
            section, field = path.split(".", 1)
            state[section][field] = copy.deepcopy(value)

    return transaction(
        state_path, mutate, expected_version=expected_version, timeout=timeout
    )


def observe_revision(
    state_path: Path,
    revision: str,
    evidence_ref: str,
    expected_version: int,
    *,
    timeout: float = DEFAULT_LOCK_TIMEOUT,
) -> dict[str, Any]:
    def mutate(state: dict[str, Any]) -> None:
        _set_subject_revision(state, revision, evidence_ref)

    return transaction(
        state_path, mutate, expected_version=expected_version, timeout=timeout
    )


def freeze_subject(
    state_path: Path,
    root: Path,
    evidence_ref: str,
    expected_version: int,
    *,
    timeout: float = DEFAULT_LOCK_TIMEOUT,
) -> dict[str, Any]:
    revision = git_head(root)

    def mutate(state: dict[str, Any]) -> None:
        previous_frozen = state["subject"]["frozen_revision"]
        _set_subject_revision(state, revision, evidence_ref)
        if previous_frozen and previous_frozen != revision:
            _unbind_assurance(state)
        state["subject"]["frozen_revision"] = revision
        state["write_gate"] = {"status": "BLOCKED", "opened_at": None}
        state["lifecycle"] = {"stage": "assure", "execution_state": "ready"}
        state["lifecycle_note"] = "subject frozen for assurance"

    return transaction(
        state_path, mutate, expected_version=expected_version, timeout=timeout
    )


def _snapshot_without_digest(snapshot: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(snapshot)
    value.pop("snapshot_digest", None)
    return value


def validate_snapshot(snapshot: dict[str, Any]) -> None:
    if set(snapshot) != {
        "snapshot_schema_version",
        "status",
        "source",
        "operational",
        "snapshot_digest",
    }:
        raise StateError("snapshot contains missing or unexpected top-level fields")
    if snapshot.get("snapshot_schema_version") != SNAPSHOT_SCHEMA_VERSION:
        raise StateError("unsupported snapshot schema version")
    if snapshot.get("status") != "handoff":
        raise StateError("snapshot status must be handoff")
    source = snapshot.get("source")
    if not isinstance(source, dict) or set(source) != {
        "work_block_id",
        "state_version",
        "state_digest",
        "repository_revision",
        "branch",
        "specification",
    }:
        raise StateError("snapshot source shape is invalid")
    _string(source.get("work_block_id"), "snapshot.source.work_block_id", allow_empty=False)
    _int(source.get("state_version"), "snapshot.source.state_version")
    _string(source.get("state_digest"), "snapshot.source.state_digest", allow_empty=False)
    _string(source.get("repository_revision"), "snapshot.source.repository_revision", allow_empty=False)
    _string(source.get("branch"), "snapshot.source.branch", allow_empty=False)
    specification = source.get("specification")
    if not isinstance(specification, dict) or set(specification) != {"path", "revision"}:
        raise StateError("snapshot specification shape is invalid")
    _string(specification.get("path"), "snapshot.source.specification.path", allow_empty=False)
    _string(specification.get("revision"), "snapshot.source.specification.revision", allow_empty=False)

    operational = snapshot.get("operational")
    if not isinstance(operational, dict) or set(operational) != {"subject", "progress", "context"}:
        raise StateError("snapshot operational payload is invalid")
    subject = operational.get("subject")
    if not isinstance(subject, dict) or set(subject) != {
        "current_revision",
        "frozen_revision",
        "generation",
    }:
        raise StateError("snapshot subject shape is invalid")
    _string(subject.get("current_revision"), "snapshot.subject.current_revision")
    _string(subject.get("frozen_revision"), "snapshot.subject.frozen_revision")
    _int(subject.get("generation"), "snapshot.subject.generation")
    progress = operational.get("progress")
    if not isinstance(progress, dict) or set(progress) != {
        "active_tasks",
        "blockers",
        "pending_decisions",
        "next_action",
    }:
        raise StateError("snapshot progress shape is invalid")
    _string_list(progress.get("active_tasks"), "snapshot.progress.active_tasks")
    _string_list(progress.get("blockers"), "snapshot.progress.blockers")
    _string_list(progress.get("pending_decisions"), "snapshot.progress.pending_decisions")
    _string(progress.get("next_action"), "snapshot.progress.next_action")
    context = operational.get("context")
    if not isinstance(context, dict) or set(context) != {
        "latest_observation_ref",
        "current_evidence_refs",
        "handoff_snapshot_ref",
    }:
        raise StateError("snapshot context shape is invalid")
    _string(context.get("latest_observation_ref"), "snapshot.context.latest_observation_ref")
    _string_list(
        context.get("current_evidence_refs"),
        "snapshot.context.current_evidence_refs",
        maximum=MAX_EVIDENCE_REFS,
    )
    _string(context.get("handoff_snapshot_ref"), "snapshot.context.handoff_snapshot_ref")

    expected = canonical_digest(_snapshot_without_digest(snapshot))
    if snapshot.get("snapshot_digest") != expected:
        raise StateError("snapshot digest mismatch")


def export_handoff(
    state_path: Path,
    root: Path,
    output: Path,
    *,
    timeout: float = DEFAULT_LOCK_TIMEOUT,
) -> dict[str, Any]:
    with state_lock(state_path, timeout):
        state = read_state(state_path)
        validate_state(state)
        if not state["work_block_id"].strip():
            raise StateError("cannot export handoff from uninitialized Work Block state")
        if not state["specification"]["path"].strip() or not state["specification"]["revision"].strip():
            raise StateError("cannot export handoff without specification identity")
        context = copy.deepcopy(state["context"])
        context["handoff_snapshot_ref"] = ""
        snapshot: dict[str, Any] = {
            "snapshot_schema_version": SNAPSHOT_SCHEMA_VERSION,
            "status": "handoff",
            "source": {
                "work_block_id": state["work_block_id"],
                "state_version": state["state_version"],
                "state_digest": canonical_digest(state),
                "repository_revision": git_head(root),
                "branch": git_branch(root),
                "specification": copy.deepcopy(state["specification"]),
            },
            "operational": {
                "subject": copy.deepcopy(state["subject"]),
                "progress": copy.deepcopy(state["progress"]),
                "context": context,
            },
        }
        snapshot["snapshot_digest"] = canonical_digest(snapshot)
        validate_snapshot(snapshot)
        atomic_write(output, snapshot)
        return snapshot


def read_snapshot(path: Path) -> dict[str, Any]:
    try:
        snapshot = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StateError(f"invalid snapshot {path}: {exc}") from exc
    if not isinstance(snapshot, dict):
        raise StateError("snapshot must be a JSON object")
    validate_snapshot(snapshot)
    return snapshot


def import_handoff(
    state_path: Path,
    root: Path,
    snapshot_path: Path,
    evidence_ref: str,
    expected_version: int,
    *,
    timeout: float = DEFAULT_LOCK_TIMEOUT,
) -> dict[str, Any]:
    snapshot = read_snapshot(snapshot_path)
    source = snapshot["source"]
    operational = snapshot["operational"]

    def mutate(state: dict[str, Any]) -> None:
        if not state["work_block_id"].strip():
            raise StateError("handoff import requires an initialized target Work Block")
        if state["work_block_id"] != source["work_block_id"]:
            raise StateError("handoff Work Block identity mismatch")
        if state["specification"] != source["specification"]:
            raise StateError("handoff specification identity mismatch")
        if state["write_gate"]["status"] != "BLOCKED":
            raise StateError("handoff import requires target write_gate=BLOCKED")
        current_head = git_head(root)
        if current_head != source["repository_revision"]:
            raise StateError(
                "handoff repository revision mismatch: "
                f"snapshot={source['repository_revision']} target={current_head}"
            )
        incoming_subject = operational["subject"]
        incoming_revision = incoming_subject["current_revision"]
        if incoming_revision and incoming_revision != source["repository_revision"]:
            raise StateError("handoff subject revision is not bound to source repository revision")
        old_subject = copy.deepcopy(state["subject"])
        if incoming_revision and incoming_revision != old_subject["current_revision"]:
            state["subject"]["current_revision"] = incoming_revision
            state["subject"]["frozen_revision"] = incoming_subject["frozen_revision"]
            state["subject"]["generation"] = max(
                old_subject["generation"], incoming_subject["generation"]
            ) + 1
            _unbind_assurance(state)
        elif incoming_revision:
            state["subject"]["frozen_revision"] = incoming_subject["frozen_revision"]
            state["subject"]["generation"] = max(
                old_subject["generation"], incoming_subject["generation"]
            )
        state["progress"] = copy.deepcopy(operational["progress"])
        state["context"]["latest_observation_ref"] = operational["context"][
            "latest_observation_ref"
        ]
        state["context"]["current_evidence_refs"] = copy.deepcopy(
            operational["context"]["current_evidence_refs"]
        )
        state["context"]["handoff_snapshot_ref"] = evidence_ref
        _append_evidence(state, evidence_ref)
        state["lifecycle_note"] = "operational context imported from validated handoff"

    return transaction(
        state_path, mutate, expected_version=expected_version, timeout=timeout
    )


def _known_v3(value: dict[str, Any]) -> None:
    if value.get("schema_version") != 3:
        raise StateError("migrate-v3 requires schema_version=3")
    if value.get("authority_mode") != AUTHORITY_MODE:
        raise StateError("unknown v3 authority_mode")
    if not isinstance(value.get("work_block_id"), str):
        raise StateError("malformed v3 work_block_id")
    profile = value.get("governance_profile")
    if profile not in VALID_PROFILES:
        raise StateError("malformed v3 governance_profile")
    for field in ("specification", "write_gate", "critic", "assurance"):
        if not isinstance(value.get(field), dict):
            raise StateError(f"malformed v3 {field}")
    for field in ("write_set", "coordination_write_set", "external_hard_stops"):
        if not isinstance(value.get(field), list):
            raise StateError(f"malformed v3 {field}")
    integrations = value.get("integrations", {"approved": [], "admission_records": []})
    if not isinstance(integrations, dict):
        raise StateError("malformed v3 integrations")


def migrate_v3(
    state_path: Path, *, timeout: float = DEFAULT_LOCK_TIMEOUT
) -> dict[str, Any]:
    with state_lock(state_path, timeout):
        legacy = read_state(state_path)
        _known_v3(legacy)
        profile = legacy["governance_profile"]
        migrated = default_state(profile, "migrated from schema v3; revalidation required")
        migrated["work_block_id"] = legacy.get("work_block_id", "")
        migrated["specification"] = copy.deepcopy(legacy.get("specification", migrated["specification"]))
        migrated["base_commit"] = str(legacy.get("base_commit") or "")
        define_quality = legacy.get("define_quality")
        if isinstance(define_quality, dict):
            migrated["define_quality"] = copy.deepcopy(define_quality)
        else:
            migrated["define_quality"] = default_define_quality(profile)
        migrated["write_gate"] = {"status": "BLOCKED", "opened_at": None}
        migrated["critic"] = copy.deepcopy(legacy.get("critic", migrated["critic"]))

        legacy_assurance = legacy.get("assurance", {})
        for name in ("review", "verification", "evaluation", "drift"):
            old = legacy_assurance.get(name)
            if isinstance(old, dict):
                normalized = copy.deepcopy(migrated["assurance"][name])
                normalized.update(copy.deepcopy(old))
                if normalized.get("status") == "READY":
                    normalized["status"] = "BLOCKED"
                    normalized["verdict"] = "UNVERIFIED"
                    normalized["skip_reason"] = ""
                migrated["assurance"][name] = normalized
        migrated["closeout_mode"] = str(legacy.get("closeout_mode") or "pending")
        migrated["integrations"] = {"approved": [], "admission_records": []}
        migrated["write_set"] = copy.deepcopy(legacy.get("write_set", []))
        migrated["coordination_write_set"] = copy.deepcopy(
            legacy.get("coordination_write_set", DEFAULT_COORDINATION)
        )
        migrated["external_hard_stops"] = copy.deepcopy(
            legacy.get("external_hard_stops", EXTERNAL_HARD_STOPS)
        )
        migrated["lifecycle"] = {"stage": "define", "execution_state": "blocked"}
        migrated["progress"]["next_action"] = (
            "Revalidate migrated schema-v4 Work Block before reopening source writes."
        )
        migrated["state_version"] = 0
        validate_state(migrated)
        atomic_write(state_path, migrated)
        return migrated


def assemble_context(
    state: dict[str, Any],
    procedure_ref: str,
    latest_observation: str = "",
    selected_evidence: list[str] | None = None,
) -> dict[str, Any]:
    validate_state(state)
    return {
        "procedure_ref": _string(procedure_ref, "procedure_ref", allow_empty=False),
        "state": copy.deepcopy(state),
        "latest_observation": _string(latest_observation, "latest_observation"),
        "selected_evidence": _string_list(
            selected_evidence or [], "selected_evidence", maximum=MAX_EVIDENCE_REFS
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--state", type=Path, default=Path(".agent/active-work-block.json")
    )
    parser.add_argument("--lock-timeout", type=float, default=DEFAULT_LOCK_TIMEOUT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    commands.add_parser("validate")

    patch = commands.add_parser("patch")
    patch.add_argument("--expected-version", type=int, required=True)
    patch.add_argument("--set-json", required=True)

    observe_local = commands.add_parser("observe-local")
    observe_local.add_argument("--expected-version", type=int, required=True)
    observe_local.add_argument("--evidence-ref", required=True)

    observe_external = commands.add_parser("observe-external")
    observe_external.add_argument("--expected-version", type=int, required=True)
    observe_external.add_argument("--revision", required=True)
    observe_external.add_argument("--evidence-ref", required=True)

    freeze = commands.add_parser("freeze-subject")
    freeze.add_argument("--expected-version", type=int, required=True)
    freeze.add_argument("--evidence-ref", required=True)

    export = commands.add_parser("export-handoff")
    export.add_argument("--output", type=Path, required=True)

    import_cmd = commands.add_parser("import-handoff")
    import_cmd.add_argument("--snapshot", type=Path, required=True)
    import_cmd.add_argument("--expected-version", type=int, required=True)
    import_cmd.add_argument("--evidence-ref", required=True)

    commands.add_parser("migrate-v3")

    context = commands.add_parser("context")
    context.add_argument("--procedure-ref", required=True)
    context.add_argument("--latest-observation", default="")
    context.add_argument("--evidence", action="append", default=[])

    args = parser.parse_args()
    root = args.root.resolve()
    state_path = args.state if args.state.is_absolute() else root / args.state

    if args.command in {"status", "validate", "context"}:
        value = read_state(state_path)
        validate_state(value)
        if args.command == "context":
            assembled = assemble_context(
                value,
                args.procedure_ref,
                args.latest_observation,
                args.evidence,
            )
            print(
                json.dumps(
                    {
                        "context": assembled,
                        "utf8_bytes": len(canonical_json_bytes(assembled)),
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
        else:
            print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        return 0

    if args.command == "patch":
        try:
            changes = json.loads(args.set_json)
        except json.JSONDecodeError as exc:
            raise StateError(f"invalid --set-json: {exc}") from exc
        if not isinstance(changes, dict):
            raise StateError("--set-json must decode to an object")
        result = patch_state(
            state_path,
            changes,
            args.expected_version,
            timeout=args.lock_timeout,
        )
    elif args.command == "observe-local":
        result = observe_revision(
            state_path,
            git_head(root),
            args.evidence_ref,
            args.expected_version,
            timeout=args.lock_timeout,
        )
    elif args.command == "observe-external":
        result = observe_revision(
            state_path,
            args.revision,
            args.evidence_ref,
            args.expected_version,
            timeout=args.lock_timeout,
        )
    elif args.command == "freeze-subject":
        result = freeze_subject(
            state_path,
            root,
            args.evidence_ref,
            args.expected_version,
            timeout=args.lock_timeout,
        )
    elif args.command == "export-handoff":
        output = args.output if args.output.is_absolute() else root / args.output
        result = export_handoff(
            state_path, root, output, timeout=args.lock_timeout
        )
    elif args.command == "import-handoff":
        snapshot = args.snapshot if args.snapshot.is_absolute() else root / args.snapshot
        result = import_handoff(
            state_path,
            root,
            snapshot,
            args.evidence_ref,
            args.expected_version,
            timeout=args.lock_timeout,
        )
    else:
        result = migrate_v3(state_path, timeout=args.lock_timeout)

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StateError as exc:
        print(f"BLOCKED: {exc}")
        raise SystemExit(2)
