#!/usr/bin/env python3
"""Provide bounded Work Block coordination context to project-scoped Codex agents."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROLE_AUTHORITY = {
    "architect": "Read-only for source/runtime; may write only an approved draft or report artifact.",
    "critic": "Read-only; may write only the approved Critic report artifact.",
    "coder": "May write only when the local source gate is READY and only inside the approved write-set.",
    "reviewer": "Read-only for source/runtime; may write only the approved Review report artifact.",
    "verifier": "Read-only for source/runtime; may write only approved verification evidence/report artifacts.",
}
VALID_PROFILES = {"Advisory", "Controlled", "Managed", "Assured", "Distributed"}
VALID_STAGES = {"define", "execute", "assure", "close"}
VALID_EXECUTION_STATES = {"blocked", "ready", "in_progress", "completed"}
VALID_GATE_STATUSES = {"BLOCKED", "READY"}
VALID_DEFINE_STATUSES = {"PENDING", "READY", "BLOCKED"}
VALID_ASSURANCE_STATUSES = {"PENDING", "READY", "SKIPPED", "DEGRADED", "BLOCKED"}
MAX_EVIDENCE_REFS = 16


def _is_string(value: Any) -> bool:
    return isinstance(value, str)


def _is_string_list(value: Any, *, maximum: int | None = None) -> bool:
    return (
        isinstance(value, list)
        and (maximum is None or len(value) <= maximum)
        and all(_is_string(item) for item in value)
    )


def validate_v4_state(data: dict[str, Any]) -> str | None:
    """Validate the v4 envelope before exposing any state-derived context."""
    if data.get("schema_version") != 4:
        return "machine-readable Work Block gate schema_version=4 is required"
    if data.get("authority_mode") != "github_capability":
        return "machine-readable Work Block gate authority mode is unsupported"
    if (
        isinstance(data.get("state_version"), bool)
        or not isinstance(data.get("state_version"), int)
        or data["state_version"] < 0
    ):
        return "machine-readable Work Block gate state_version is invalid"
    if not _is_string(data.get("work_block_id")):
        return "machine-readable Work Block gate work_block_id is invalid"
    if data.get("governance_profile") not in VALID_PROFILES:
        return "machine-readable Work Block gate governance profile is unsupported"

    specification = data.get("specification")
    if not isinstance(specification, dict) or not all(
        _is_string(specification.get(field)) for field in ("path", "revision")
    ):
        return "machine-readable Work Block gate specification is invalid"
    if not _is_string(data.get("base_commit")):
        return "machine-readable Work Block gate base_commit is invalid"

    define_quality = data.get("define_quality")
    if not isinstance(define_quality, dict) or not isinstance(
        define_quality.get("required"), bool
    ):
        return "machine-readable Work Block gate define_quality is invalid"
    if define_quality.get("status") not in VALID_DEFINE_STATUSES or not all(
        _is_string(define_quality.get(field))
        for field in ("requirements_review", "traceability", "consistency_analysis")
    ):
        return "machine-readable Work Block gate define_quality is incomplete"

    write_gate = data.get("write_gate")
    if not isinstance(write_gate, dict) or write_gate.get("status") not in VALID_GATE_STATUSES:
        return "machine-readable Work Block gate write_gate is invalid"
    if write_gate.get("opened_at") is not None and not _is_string(write_gate.get("opened_at")):
        return "machine-readable Work Block gate write_gate timestamp is invalid"

    critic = data.get("critic")
    if not isinstance(critic, dict) or not isinstance(critic.get("required"), bool) or not all(
        _is_string(critic.get(field))
        for field in ("status", "verdict", "report", "isolation", "skip_reason")
    ):
        return "machine-readable Work Block gate critic is incomplete"

    assurance = data.get("assurance")
    if not isinstance(assurance, dict) or set(assurance) != {
        "review", "verification", "evaluation", "drift"
    }:
        return "machine-readable Work Block gate assurance is incomplete"
    for item in assurance.values():
        if not isinstance(item, dict) or not isinstance(item.get("required"), bool):
            return "machine-readable Work Block gate assurance entry is invalid"
        if item.get("status") not in VALID_ASSURANCE_STATUSES or not all(
            _is_string(item.get(field))
            for field in ("verdict", "report", "isolation", "skip_reason")
        ):
            return "machine-readable Work Block gate assurance entry is incomplete"

    if not _is_string(data.get("closeout_mode")) or not isinstance(data.get("integrations"), dict):
        return "machine-readable Work Block gate control fields are incomplete"
    integrations = data["integrations"]
    if not _is_string_list(integrations.get("approved")) or not _is_string_list(
        integrations.get("admission_records")
    ):
        return "machine-readable Work Block gate integrations are invalid"
    if not _is_string_list(data.get("write_set")) or not _is_string_list(
        data.get("coordination_write_set")
    ) or not _is_string_list(data.get("external_hard_stops")):
        return "machine-readable Work Block gate scope fields are invalid"

    lifecycle = data.get("lifecycle")
    if not isinstance(lifecycle, dict) or lifecycle.get("stage") not in VALID_STAGES or lifecycle.get(
        "execution_state"
    ) not in VALID_EXECUTION_STATES:
        return "machine-readable Work Block gate lifecycle is invalid"
    subject = data.get("subject")
    if not isinstance(subject, dict) or not all(
        _is_string(subject.get(field)) for field in ("current_revision", "frozen_revision")
    ) or (
        isinstance(subject.get("generation"), bool)
        or not isinstance(subject.get("generation"), int)
        or subject["generation"] < 0
    ):
        return "machine-readable Work Block gate subject is invalid"
    progress = data.get("progress")
    if not isinstance(progress, dict) or not all(
        _is_string_list(progress.get(field))
        for field in ("active_tasks", "blockers", "pending_decisions")
    ) or not _is_string(progress.get("next_action")):
        return "machine-readable Work Block gate progress is incomplete"
    context = data.get("context")
    if not isinstance(context, dict) or not _is_string(context.get("latest_observation_ref")) or not _is_string_list(
        context.get("current_evidence_refs"), maximum=MAX_EVIDENCE_REFS
    ) or not _is_string(context.get("handoff_snapshot_ref")):
        return "machine-readable Work Block gate context is incomplete"
    if not _is_string(data.get("lifecycle_note")):
        return "machine-readable Work Block gate lifecycle_note is invalid"
    return None


def find_repo_root(cwd: Path) -> Path:
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
            timeout=3,
        )
        return Path(result.stdout.strip()).resolve()
    except (OSError, subprocess.SubprocessError):
        current = cwd.resolve()
        for candidate in (current, *current.parents):
            if (candidate / ".git").exists() or (candidate / ".agent").exists():
                return candidate
        return current


def load_gate(root: Path) -> tuple[dict[str, Any] | None, str | None]:
    path = root / ".agent" / "active-work-block.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, "machine-readable Work Block gate is missing"
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"machine-readable Work Block gate is invalid: {exc}"
    if not isinstance(data, dict):
        return None, "machine-readable Work Block gate must be a JSON object"
    error = validate_v4_state(data)
    if error:
        return None, error
    return data, None


def compact_list(value: Any, limit: int = 20) -> str:
    if not isinstance(value, list):
        return "none"
    items = [str(item) for item in value if isinstance(item, str) and item.strip()]
    if not items:
        return "none"
    shown = items[:limit]
    suffix = f" (+{len(items) - limit} more)" if len(items) > limit else ""
    return ", ".join(shown) + suffix


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"Invalid SubagentStart input: {exc}", file=sys.stderr)
        return 1
    if not isinstance(event, dict):
        print("Invalid SubagentStart input: expected object", file=sys.stderr)
        return 1

    cwd = Path(str(event.get("cwd") or os.getcwd()))
    root = find_repo_root(cwd)
    gate, error = load_gate(root)
    agent_type = str(event.get("agent_type") or "default")
    permission_mode = str(event.get("permission_mode") or "unknown")
    role = agent_type.lower().replace("-", "_")
    authority = ROLE_AUTHORITY.get(
        role,
        "Use the authority of the logical role assigned by the parent Work Block; tool access does not expand it.",
    )

    if gate is None:
        context = (
            f"Agent type: {agent_type}. Permission mode: {permission_mode}. "
            f"Authority: {authority} The {error}; source writes are not authorized by local Work Block scope. "
            "Read AGENTS.md and request a valid active Work Block before state-changing work."
        )
    else:
        spec = gate.get("specification") if isinstance(gate.get("specification"), dict) else {}
        write_gate = gate.get("write_gate") if isinstance(gate.get("write_gate"), dict) else {}
        critic = gate.get("critic") if isinstance(gate.get("critic"), dict) else {}
        context = "\n".join(
            [
                f"Logical agent type: {agent_type}",
                f"Permission mode: {permission_mode}",
                f"Authority: {authority}",
                f"Authority mode: {gate.get('authority_mode')}",
                f"Active Work Block: {gate.get('work_block_id') or 'UNSET'}",
                f"Governance profile: {gate.get('governance_profile') or 'UNSET'}",
                f"Specification: {spec.get('path') or 'UNSET'} @ {spec.get('revision') or 'UNSET'}",
                f"Planning baseline: {gate.get('base_commit') or 'UNSET'}",
                f"Local source write gate: {str(write_gate.get('status') or 'BLOCKED').upper()}",
                f"Critic: {str(critic.get('status') or 'PENDING').upper()} / {str(critic.get('verdict') or 'PENDING').upper()}",
                f"Approved write-set: {compact_list(gate.get('write_set'))}",
                f"Coordination paths: {compact_list(gate.get('coordination_write_set'))}",
                f"External Hard Stops: {compact_list(gate.get('external_hard_stops'))}",
                "This local context is a cooperative scope guard, not production/security authority. External GitHub/OS/credential boundaries remain authoritative.",
            ]
        )

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SubagentStart",
                    "additionalContext": context,
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
