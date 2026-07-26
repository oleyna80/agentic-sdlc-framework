#!/usr/bin/env python3
"""Validate repository Work Block, navigation, and closeout SSOT consistency."""
from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

import yaml

ACTIVE_STATUSES = {"draft", "planned", "in_progress", "blocked"}
MAP_BLOCK_RE = re.compile(
    r"<!--\s*release-state\s*\n(?P<body>.*?)\n-->\s*", re.DOTALL
)
MUTABLE_VCS_PATTERNS = (
    re.compile(r"^\s*[-*]?\s*\*\*Merge status:\*\*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\bnot merged\b", re.IGNORECASE),
    re.compile(r"\bremains? draft\b", re.IGNORECASE),
    re.compile(r"\bready for review\b", re.IGNORECASE),
    re.compile(r"\bmerge commit\b", re.IGNORECASE),
    re.compile(r"\bmerged_at\b", re.IGNORECASE),
)


class ReleaseStateError(RuntimeError):
    """Raised when release-state evidence is missing or contradictory."""


def load_yaml_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ReleaseStateError(f"invalid {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReleaseStateError(f"{label} must contain a YAML object")
    return value


def parse_frontmatter(path: Path, label: str) -> tuple[dict[str, Any], str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReleaseStateError(f"cannot read {label}: {exc}") from exc
    if not text.startswith("---\n"):
        raise ReleaseStateError(f"{label} requires YAML frontmatter")
    try:
        raw_frontmatter, body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ReleaseStateError(f"{label} has unterminated YAML frontmatter") from exc
    try:
        frontmatter = yaml.safe_load(raw_frontmatter)
    except yaml.YAMLError as exc:
        raise ReleaseStateError(f"invalid {label} frontmatter: {exc}") from exc
    if not isinstance(frontmatter, dict):
        raise ReleaseStateError(f"{label} frontmatter must be an object")
    return frontmatter, body


def safe_repo_path(root: Path, value: object, label: str) -> tuple[str, Path]:
    if not isinstance(value, str) or not value.strip():
        raise ReleaseStateError(f"{label} must be a non-empty repository-relative path")
    normalized = value.strip().replace("\\", "/")
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or normalized in {".", ".."} or ".." in pure.parts:
        raise ReleaseStateError(f"{label} escapes repository: {value}")
    resolved = (root / Path(*pure.parts)).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ReleaseStateError(f"{label} escapes repository: {value}") from exc
    return normalized, resolved


def string_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ReleaseStateError(f"{label} must be an array of non-empty strings")
    normalized = [item.strip().replace("\\", "/") for item in value]
    if len(normalized) != len(set(normalized)):
        raise ReleaseStateError(f"{label} contains duplicate paths")
    return normalized


def parse_map_state(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReleaseStateError(f"cannot read PROJECT_MAP.md: {exc}") from exc
    match = MAP_BLOCK_RE.search(text)
    if not match:
        raise ReleaseStateError("PROJECT_MAP.md requires one release-state comment block")
    if len(MAP_BLOCK_RE.findall(text)) != 1:
        raise ReleaseStateError("PROJECT_MAP.md must contain exactly one release-state block")
    try:
        value = yaml.safe_load(match.group("body"))
    except yaml.YAMLError as exc:
        raise ReleaseStateError(f"invalid PROJECT_MAP.md release-state block: {exc}") from exc
    if not isinstance(value, dict):
        raise ReleaseStateError("PROJECT_MAP.md release-state block must be an object")
    return value


def validate_completed_work_block(root: Path, relative: str) -> None:
    normalized, path = safe_repo_path(root, relative, "completed_work_block")
    if not normalized.startswith("docs/plans/") or not normalized.endswith(".md"):
        raise ReleaseStateError(f"completed Work Block must be under docs/plans: {normalized}")
    if not path.is_file():
        raise ReleaseStateError(f"completed Work Block is missing: {normalized}")
    frontmatter, body = parse_frontmatter(path, f"completed Work Block {normalized}")
    if frontmatter.get("artifact_type") != "work_block":
        raise ReleaseStateError(f"completed path is not a Work Block: {normalized}")
    if frontmatter.get("status") != "completed":
        raise ReleaseStateError(f"completed Work Block is not status completed: {normalized}")
    pending_markers = (
        "**Review Gate:** PENDING",
        "**Verification Verdict:** PENDING",
        "**Evaluation Verdict:** PENDING",
        "**Drift Gate:** PENDING",
        "**Closeout Mode:** pending",
    )
    found = [marker for marker in pending_markers if marker in body]
    if found:
        raise ReleaseStateError(
            f"completed Work Block retains pending lifecycle markers: {normalized}: {found}"
        )


def validate_active_work_block(root: Path, relative: str) -> None:
    normalized, path = safe_repo_path(root, relative, "active_work_block")
    if not normalized.startswith("docs/plans/") or not normalized.endswith(".md"):
        raise ReleaseStateError(f"active Work Block must be under docs/plans: {normalized}")
    if not path.is_file():
        raise ReleaseStateError(f"active Work Block is missing: {normalized}")
    frontmatter, _ = parse_frontmatter(path, f"active Work Block {normalized}")
    if frontmatter.get("artifact_type") != "work_block":
        raise ReleaseStateError(f"active path is not a Work Block: {normalized}")
    status = frontmatter.get("status")
    if status not in ACTIVE_STATUSES:
        raise ReleaseStateError(
            f"active Work Block requires one of {sorted(ACTIVE_STATUSES)}, found {status!r}"
        )


def validate_closeout(root: Path, release_state: dict[str, Any], completed: list[str]) -> None:
    latest = release_state.get("latest_completed_work_block")
    closeout_value = release_state.get("closeout_report")
    if latest not in completed:
        raise ReleaseStateError(
            "release_state.latest_completed_work_block must be listed in completed_work_blocks"
        )
    latest_normalized, _ = safe_repo_path(root, latest, "latest_completed_work_block")
    closeout_normalized, closeout_path = safe_repo_path(root, closeout_value, "closeout_report")
    if not closeout_normalized.startswith("docs/reports/closeout/"):
        raise ReleaseStateError("closeout_report must be under docs/reports/closeout/")
    if not closeout_path.is_file():
        raise ReleaseStateError(f"closeout report is missing: {closeout_normalized}")
    frontmatter, body = parse_frontmatter(closeout_path, f"closeout report {closeout_normalized}")
    if frontmatter.get("artifact_type") != "closeout_report":
        raise ReleaseStateError("release_state.closeout_report is not a closeout report")
    if frontmatter.get("status") != "approved":
        raise ReleaseStateError("release-state closeout report must be approved")
    if str(frontmatter.get("work_block_id", "")).lower() not in latest_normalized.lower():
        raise ReleaseStateError("closeout work_block_id does not match latest completed Work Block")
    required_markers = (
        "**Stage execution state:** completed",
        "**Closeout classification:** SUCCESS",
        "**Task status:** completed",
    )
    missing = [marker for marker in required_markers if marker not in body]
    if missing:
        raise ReleaseStateError(f"successful closeout is missing internal markers: {missing}")
    if "**Review verdict:** PENDING" in body or "**Verification verdict:** PENDING" in body:
        raise ReleaseStateError("successful closeout contains pending required assurance")
    if release_state.get("external_vcs_state") != "non_normative":
        raise ReleaseStateError("release_state.external_vcs_state must be non_normative")
    for pattern in MUTABLE_VCS_PATTERNS:
        if pattern.search(body):
            raise ReleaseStateError(
                f"closeout contains mutable GitHub/VCS state: {pattern.pattern}"
            )


def validate_repository(root: Path) -> dict[str, Any]:
    root = root.resolve()
    registry = load_yaml_object(root / "FILE_REGISTRY.yml", "FILE_REGISTRY.yml")
    migration = registry.get("migration_state")
    if not isinstance(migration, dict):
        raise ReleaseStateError("FILE_REGISTRY.yml requires migration_state")
    completed = string_list(migration.get("completed_work_blocks"), "completed_work_blocks")
    completed_set = set(completed)
    for relative in completed:
        validate_completed_work_block(root, relative)

    active_value = migration.get("active_work_block")
    active: str | None
    if active_value is None:
        active = None
    else:
        active, _ = safe_repo_path(root, active_value, "active_work_block")
        if active in completed_set:
            raise ReleaseStateError("active Work Block cannot also be completed")
        validate_active_work_block(root, active)

    map_state = parse_map_state(root / "PROJECT_MAP.md")
    map_completed = string_list(
        map_state.get("completed_work_blocks"),
        "PROJECT_MAP completed_work_blocks",
    )
    map_active = map_state.get("active_work_block")
    if map_completed != completed:
        raise ReleaseStateError("PROJECT_MAP completed Work Blocks do not match FILE_REGISTRY.yml")
    if map_active != active:
        raise ReleaseStateError("PROJECT_MAP active Work Block does not match FILE_REGISTRY.yml")

    release_state = registry.get("release_state")
    if not isinstance(release_state, dict):
        raise ReleaseStateError("FILE_REGISTRY.yml requires release_state")
    if release_state.get("contract") != "governance/release-state.md":
        raise ReleaseStateError("release_state.contract must reference governance/release-state.md")
    if release_state.get("validator") != "scripts/validate-release-state.py":
        raise ReleaseStateError("release_state.validator is not canonical")
    if release_state.get("fixtures") != "scripts/test-release-state-contracts.py":
        raise ReleaseStateError("release_state.fixtures is not canonical")
    validate_closeout(root, release_state, completed)

    return {
        "completed_work_blocks": completed,
        "active_work_block": active,
        "latest_completed_work_block": release_state["latest_completed_work_block"],
        "closeout_report": release_state["closeout_report"],
        "verdict": "READY",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = validate_repository(args.root)
    except ReleaseStateError as exc:
        print(f"RELEASE STATE BLOCKED: {exc}", file=sys.stderr)
        return 1
    print("Release-state contract: READY")
    print(f"Completed Work Blocks: {len(result['completed_work_blocks'])}")
    print(f"Active Work Block: {result['active_work_block'] or 'none'}")
    print(f"Latest completed: {result['latest_completed_work_block']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
