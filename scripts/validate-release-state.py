#!/usr/bin/env python3
"""Validate repository Work Block, navigation, and closeout SSOT consistency."""
from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode

ACTIVE_STATUSES = {"draft", "planned", "in_progress", "blocked"}
FORMAL_GOVERNANCE_PROFILES = {"Managed", "Assured", "Distributed"}
CANDIDATE_STATUS = "closeout_candidate"
CANDIDATE_STATE = "assurance_pending"
CANDIDATE_EVIDENCE_TYPES = {
    "review": "review_report",
    "verification": "verification_report",
    "drift": "drift_report",
    "closeout": "closeout_report",
}
CANDIDATE_EVIDENCE_VERDICTS = {
    "review": "READY",
    "verification": "READY",
    "drift": "ALIGNED",
}
CANDIDATE_EVIDENCE_DIRECTORIES = {
    "review": "docs/reports/reviews/",
    "verification": "docs/reports/verification/",
    "drift": "docs/reports/drift/",
    "closeout": "docs/reports/closeout/",
}
COMMIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MAP_BLOCK_RE = re.compile(r"<!--\s*release-state\s*\n(?P<body>.*?)\n-->\s*", re.DOTALL)
MIGRATION_SECTION_RE = re.compile(
    r"^## Migration Work\s*\n(?P<body>.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL
)
WORK_BLOCK_FINAL_SECTION_RE = re.compile(
    r"^## (?:Final State|Closeout State)\s*\n(?P<body>.*?)(?=^##\s|\Z)",
    re.MULTILINE | re.DOTALL,
)
MARKER_RE = re.compile(
    r"^\s*[-*]\s+\*\*(?P<key>[^*]+):\*\*\s*(?P<value>.+?)\s*$", re.MULTILINE
)
MUTABLE_VCS_STATES = r"(?:draft|ready(?:\s+for\s+review)?|open|closed|merged|unmerged)"
MUTABLE_VCS_STATE_RE = re.compile(rf"^{MUTABLE_VCS_STATES}$", re.IGNORECASE)
MUTABLE_VCS_STATE_TOKEN_RE = re.compile(rf"\b{MUTABLE_VCS_STATES}\b", re.IGNORECASE)
MARKDOWN_DECORATION_RE = re.compile(r"[*_]+")
NORMALIZED_MUTABLE_VCS_STATE = rf"{MUTABLE_VCS_STATES}\b"
STRUCTURED_VCS_KEY_RE = re.compile(
    r"^(?:pr|pull_request|pullrequest|merge)_(?:status|state)$", re.IGNORECASE
)
STRUCTURED_VCS_PARENT_RE = re.compile(
    r"^(?:pr|pull_request|pullrequest|merge)$", re.IGNORECASE
)
STRUCTURED_STATE_KEY_RE = re.compile(r"^(?:status|state)$", re.IGNORECASE)
RAW_MUTABLE_CLOSEOUT_PATTERNS = (
    re.compile(r"^\s*[-*]?\s*(?:\*\*)?Merge status:(?:\*\*)?", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\bnot merged\b", re.IGNORECASE),
    re.compile(r"\bmerge commit\b", re.IGNORECASE),
    re.compile(r"\bmerged_at\b", re.IGNORECASE),
)
NORMALIZED_MUTABLE_CLOSEOUT_PATTERNS = (
    re.compile(
        rf"\b(?:PR|pull[ -]?request)\s*(?:#\s*\d+)?\s*"
        rf"(?:(?::|=)\s*|(?:is|was|remains?|became|has\s+been)\s*|"
        rf"(?:status|state)\s*(?:is|=|:)\s*){NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\b(?:PR|pull[ -]?request)\s*(?:#\s*\d+)?\s+"
        rf"{NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\*\*(?:PR|pull[ -]?request)\s*(?:#\s*\d+)?\s*:\*\*\s*"
        rf"{NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\*\*(?:PR|pull[ -]?request)\s+(?:status|state):\*\*\s*"
        rf"{NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"^\s*\|\s*(?:\*\*)?(?:PR|pull[ -]?request)\s*(?:#\s*\d+)?"
        rf"(?:\*\*)?\s*\|\s*{NORMALIZED_MUTABLE_VCS_STATE}\s*\|",
        re.IGNORECASE | re.MULTILINE,
    ),
)
STALE_MAP_PATTERNS = (
    re.compile(r"PR\s*#\d+\s+remains?\s+Draft", re.IGNORECASE),
    re.compile(r"PR\s*#\d+.*\bnot merged\b", re.IGNORECASE),
    re.compile(r"\*\*Merge status:\*\*\s*not merged", re.IGNORECASE),
)
CANONICAL_RELEASE_ASSETS = {
    "contract": "governance/release-state.md",
    "validator": "scripts/validate-release-state.py",
    "fixtures": "scripts/test-release-state-contracts.py",
    "workflow": ".github/workflows/release-state-contract.yml",
}


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


def direct_yaml_mapping_field_count(path: Path, parent_field: str, field: str) -> int:
    """Count direct nested YAML keys before safe_load can collapse duplicates."""
    try:
        document = yaml.compose(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ReleaseStateError(f"invalid {path.name}: {exc}") from exc
    if not isinstance(document, MappingNode):
        raise ReleaseStateError(f"{path.name} must contain a YAML object")
    parents = [value for key, value in document.value if isinstance(key, ScalarNode) and key.value == parent_field]
    if len(parents) != 1 or not isinstance(parents[0], MappingNode):
        raise ReleaseStateError(f"{path.name} requires one direct {parent_field} mapping")
    return sum(
        1
        for key, _ in parents[0].value
        if isinstance(key, ScalarNode) and key.value == field
    )


def parse_frontmatter(path: Path, label: str) -> tuple[dict[str, Any], str, str]:
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
    return frontmatter, body, text


def parse_frontmatter_text(text: str, label: str) -> tuple[dict[str, Any], str]:
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


def string_list(value: object, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ReleaseStateError(f"{label} must be an array of non-empty strings")
    if not allow_empty and not value:
        raise ReleaseStateError(f"{label} must not be empty")
    normalized = [item.strip().replace("\\", "/") for item in value]
    if len(normalized) != len(set(normalized)):
        raise ReleaseStateError(f"{label} contains duplicate paths")
    return normalized


def parse_markers(body: str, label: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for match in MARKER_RE.finditer(body):
        key = match.group("key").strip().lower()
        if key in result:
            raise ReleaseStateError(f"{label} contains duplicate marker: {key}")
        result[key] = match.group("value").strip()
    return result


def evaluation_verdict(value: str, label: str) -> str:
    normalized = value.strip()
    if normalized == "READY":
        return "READY"
    skipped = re.fullmatch(r"SKIPPED\s+[—–-]\s+(?P<reason>\S.*)", normalized)
    if skipped:
        return "SKIPPED"
    raise ReleaseStateError(
        f"{label} must be READY or SKIPPED with a non-empty rationale, found {normalized!r}"
    )


def extract_single_section(body: str, heading: str, label: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*\n(?P<body>.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    matches = list(pattern.finditer(body))
    if not matches:
        raise ReleaseStateError(f"{label} requires section: {heading}")
    if len(matches) != 1:
        raise ReleaseStateError(f"{label} must contain exactly one section: {heading}")
    content = matches[0].group("body").strip()
    if not content:
        raise ReleaseStateError(f"{label} section is empty: {heading}")
    return content


def parse_map_state(path: Path) -> tuple[dict[str, Any], str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReleaseStateError(f"cannot read PROJECT_MAP.md: {exc}") from exc
    matches = list(MAP_BLOCK_RE.finditer(text))
    if not matches:
        raise ReleaseStateError("PROJECT_MAP.md requires one release-state comment block")
    if len(matches) != 1:
        raise ReleaseStateError("PROJECT_MAP.md must contain exactly one release-state block")
    try:
        value = yaml.safe_load(matches[0].group("body"))
    except yaml.YAMLError as exc:
        raise ReleaseStateError(f"invalid PROJECT_MAP.md release-state block: {exc}") from exc
    if not isinstance(value, dict):
        raise ReleaseStateError("PROJECT_MAP.md release-state block must be an object")
    return value, text


def completed_work_block_markers(body: str, normalized: str) -> dict[str, str]:
    matches = list(WORK_BLOCK_FINAL_SECTION_RE.finditer(body))
    if not matches:
        raise ReleaseStateError(
            f"completed Work Block requires Final State or Closeout State section: {normalized}"
        )
    if len(matches) != 1:
        raise ReleaseStateError(
            f"completed Work Block must contain exactly one terminal state section: {normalized}"
        )
    markers = parse_markers(matches[0].group("body"), f"completed Work Block {normalized}")
    stage_keys = [key for key in ("stage state", "state") if key in markers]
    if not stage_keys:
        raise ReleaseStateError(
            f"completed Work Block requires stage state=completed: {normalized}"
        )
    for key in stage_keys:
        if markers[key] != "completed":
            raise ReleaseStateError(
                f"completed Work Block requires {key}=completed, found {markers[key]!r}: {normalized}"
            )
    required_exact = {
        "review gate": "READY",
        "verification verdict": "READY",
        "closeout mode": "success-closeout",
    }
    for key, expected in required_exact.items():
        actual = markers.get(key)
        if actual != expected:
            raise ReleaseStateError(
                f"completed Work Block requires {key}={expected}, found {actual!r}: {normalized}"
            )
    drift = markers.get("drift gate")
    if drift not in {"ALIGNED", "READY"}:
        raise ReleaseStateError(
            f"completed Work Block requires drift gate in ['ALIGNED', 'READY'], "
            f"found {drift!r}: {normalized}"
        )
    task_status = markers.get("task status")
    if task_status is not None and task_status != "completed":
        raise ReleaseStateError(
            f"completed Work Block requires task status=completed, found {task_status!r}: {normalized}"
        )
    evaluation = markers.get("evaluation verdict")
    if evaluation is not None:
        evaluation_verdict(evaluation, "completed Work Block evaluation verdict")
    return markers


def validate_completed_work_block(
    root: Path, relative: str
) -> tuple[dict[str, Any], dict[str, str]]:
    normalized, path = safe_repo_path(root, relative, "completed_work_block")
    if not normalized.startswith("docs/plans/") or not normalized.endswith(".md"):
        raise ReleaseStateError(f"completed Work Block must be under docs/plans: {normalized}")
    if not path.is_file():
        raise ReleaseStateError(f"completed Work Block is missing: {normalized}")
    frontmatter, body, _ = parse_frontmatter(path, f"completed Work Block {normalized}")
    if frontmatter.get("artifact_type") != "work_block":
        raise ReleaseStateError(f"completed path is not a Work Block: {normalized}")
    if frontmatter.get("status") != "completed":
        raise ReleaseStateError(f"completed Work Block is not status completed: {normalized}")
    work_block_id = frontmatter.get("work_block_id")
    if not isinstance(work_block_id, str) or not work_block_id.strip():
        raise ReleaseStateError(f"completed Work Block lacks work_block_id: {normalized}")
    return frontmatter, completed_work_block_markers(body, normalized)


def validate_active_work_block(root: Path, relative: str) -> dict[str, Any]:
    normalized, path = safe_repo_path(root, relative, "active_work_block")
    if not normalized.startswith("docs/plans/") or not normalized.endswith(".md"):
        raise ReleaseStateError(f"active Work Block must be under docs/plans: {normalized}")
    if not path.is_file():
        raise ReleaseStateError(f"active Work Block is missing: {normalized}")
    frontmatter, _, _ = parse_frontmatter(path, f"active Work Block {normalized}")
    if frontmatter.get("artifact_type") != "work_block":
        raise ReleaseStateError(f"active path is not a Work Block: {normalized}")
    status = frontmatter.get("status")
    if status not in ACTIVE_STATUSES:
        raise ReleaseStateError(
            f"active Work Block requires one of {sorted(ACTIVE_STATUSES)}, found {status!r}"
        )
    return frontmatter


def candidate_paths(value: object, label: str) -> list[str]:
    paths = string_list(value, label)
    for relative in paths:
        if not relative.startswith("docs/") and relative not in {
            "FILE_REGISTRY.yml",
            "PROJECT_MAP.md",
        }:
            raise ReleaseStateError(f"{label} contains unsupported candidate path: {relative}")
    return paths


def validate_pre_closeout_candidate(
    root: Path,
    migration: dict[str, Any],
    completed: list[str],
    map_state: dict[str, Any],
    map_text: str,
    active: str | None,
) -> dict[str, Any] | None:
    """Validate the one explicit local candidate declaration, if present."""
    candidate = migration.get("pre_closeout_candidate")
    map_candidate = map_state.get("pre_closeout_candidate")
    if candidate is None:
        if map_candidate is not None:
            raise ReleaseStateError(
                "PROJECT_MAP pre_closeout_candidate exists without FILE_REGISTRY declaration"
            )
        return None
    if active is not None:
        raise ReleaseStateError(
            "pre_closeout_candidate requires active_work_block to be null"
        )
    if not isinstance(candidate, dict):
        raise ReleaseStateError("pre_closeout_candidate must be an object or null")
    required_fields = {
        "work_block",
        "work_block_id",
        "predecessor_completed_work_block",
        "state",
        "required_evidence",
        "normative_manifest",
    }
    if set(candidate) != required_fields:
        raise ReleaseStateError(
            "pre_closeout_candidate must contain exactly "
            f"{sorted(required_fields)}"
        )

    work_block, work_block_path = safe_repo_path(
        root, candidate["work_block"], "pre_closeout_candidate.work_block"
    )
    if not work_block.startswith("docs/plans/") or not work_block.endswith(".md"):
        raise ReleaseStateError("pre_closeout_candidate.work_block must be under docs/plans")
    if work_block in completed:
        raise ReleaseStateError("pre_closeout_candidate.work_block must stay outside completed_work_blocks")
    if not work_block_path.is_file():
        raise ReleaseStateError("pre_closeout_candidate.work_block is missing")
    frontmatter, body, _ = parse_frontmatter(work_block_path, "pre_closeout candidate Work Block")
    if frontmatter.get("artifact_type") != "work_block":
        raise ReleaseStateError("pre_closeout_candidate.work_block is not a Work Block")
    if frontmatter.get("status") != CANDIDATE_STATUS:
        raise ReleaseStateError(
            f"pre_closeout candidate Work Block must be status {CANDIDATE_STATUS}"
        )
    if frontmatter.get("work_block_id") != candidate["work_block_id"]:
        raise ReleaseStateError("pre_closeout_candidate work_block_id does not match Work Block")
    if candidate.get("state") != CANDIDATE_STATE:
        raise ReleaseStateError(
            f"pre_closeout_candidate.state must be {CANDIDATE_STATE}"
        )

    predecessor, _ = safe_repo_path(
        root,
        candidate["predecessor_completed_work_block"],
        "pre_closeout_candidate.predecessor_completed_work_block",
    )
    if predecessor != completed[-1]:
        raise ReleaseStateError(
            "pre_closeout_candidate predecessor must be the raw latest completed Work Block"
        )

    evidence = candidate.get("required_evidence")
    if not isinstance(evidence, dict) or set(evidence) != set(CANDIDATE_EVIDENCE_TYPES):
        raise ReleaseStateError(
            "pre_closeout_candidate.required_evidence must contain exactly "
            f"{sorted(CANDIDATE_EVIDENCE_TYPES)}"
        )
    normalized_evidence: dict[str, str] = {}
    for evidence_class in CANDIDATE_EVIDENCE_TYPES:
        relative, _ = safe_repo_path(
            root,
            evidence[evidence_class],
            f"pre_closeout_candidate.required_evidence.{evidence_class}",
        )
        expected_prefix = CANDIDATE_EVIDENCE_DIRECTORIES[evidence_class]
        if not relative.startswith(expected_prefix) or not relative.endswith(".md"):
            raise ReleaseStateError(
                f"pre_closeout_candidate {evidence_class} evidence must be under {expected_prefix}"
            )
        normalized_evidence[evidence_class] = relative

    manifest = candidate_paths(
        candidate["normative_manifest"], "pre_closeout_candidate.normative_manifest"
    )
    for required_path in (work_block, "FILE_REGISTRY.yml", "PROJECT_MAP.md"):
        if required_path not in manifest:
            raise ReleaseStateError(
                f"pre_closeout_candidate.normative_manifest must include {required_path}"
            )

    current = extract_single_section(body, "Current State", "pre_closeout candidate Work Block")
    markers = parse_markers(current, "pre_closeout candidate Work Block")
    expected_markers = {
        "current stage": "Close",
        "stage state": CANDIDATE_STATE,
        "closeout mode": "candidate",
    }
    for key, expected in expected_markers.items():
        if markers.get(key) != expected:
            raise ReleaseStateError(
                f"pre_closeout candidate Work Block requires {key}={expected}, "
                f"found {markers.get(key)!r}"
            )
    for key in ("review gate", "verification verdict", "drift gate"):
        if markers.get(key) != "PENDING":
            raise ReleaseStateError(
                f"pre_closeout candidate Work Block requires {key}=PENDING, "
                f"found {markers.get(key)!r}"
            )
    if re.search(
        r"^##\s+(?:Final State|Terminal State|Closeout State)\s*$",
        body,
        re.MULTILINE | re.IGNORECASE,
    ):
        raise ReleaseStateError(
            "pre_closeout candidate Work Block must not contain a terminal state section"
        )

    if map_candidate != candidate:
        raise ReleaseStateError("PROJECT_MAP pre_closeout_candidate does not match FILE_REGISTRY")
    section = migration_section(map_text)
    if "Closeout candidate:" not in section or f"`{work_block}`" not in section:
        raise ReleaseStateError("PROJECT_MAP Migration Work section omits closeout candidate")

    return {
        "declaration": candidate,
        "work_block": work_block,
        "record": {"frontmatter": frontmatter, "markers": markers},
        "evidence": normalized_evidence,
        "manifest": manifest,
    }


def validate_candidate_evidence(root: Path, candidate: dict[str, Any]) -> str:
    """Require complete, consistently bound terminal evidence for ordinary mode."""
    subjects: set[str] = set()
    work_block_id = candidate["declaration"]["work_block_id"]
    for evidence_class, expected_type in CANDIDATE_EVIDENCE_TYPES.items():
        relative = candidate["evidence"][evidence_class]
        _, path = safe_repo_path(root, relative, f"candidate {evidence_class} evidence")
        if not path.is_file():
            raise ReleaseStateError(f"pre_closeout candidate requires {evidence_class} evidence: {relative}")
        frontmatter, body, _ = parse_frontmatter(path, f"candidate {evidence_class} evidence")
        if frontmatter.get("artifact_type") != expected_type:
            raise ReleaseStateError(
                f"candidate {evidence_class} evidence must be {expected_type}"
            )
        if frontmatter.get("status") != "approved":
            raise ReleaseStateError(f"candidate {evidence_class} evidence must be approved")
        if frontmatter.get("work_block_id") != work_block_id:
            raise ReleaseStateError(
                f"candidate {evidence_class} evidence work_block_id does not match"
            )
        expected_verdict = CANDIDATE_EVIDENCE_VERDICTS.get(evidence_class)
        if expected_verdict and frontmatter.get("verdict") != expected_verdict:
            raise ReleaseStateError(
                f"candidate {evidence_class} evidence requires verdict={expected_verdict}"
            )
        subject = frontmatter.get("subject_commit")
        if not isinstance(subject, str) or not COMMIT_SHA_RE.fullmatch(subject):
            raise ReleaseStateError(
                f"candidate {evidence_class} evidence requires a full subject_commit SHA"
            )
        subjects.add(subject)
        if evidence_class == "closeout":
            markers = parse_markers(body, "candidate closeout evidence")
            for key, expected in {
                "stage execution state": "completed",
                "review verdict": "READY",
                "verification verdict": "READY",
                "drift verdict": "ALIGNED",
                "closeout classification": "SUCCESS",
                "task status": "completed",
            }.items():
                if markers.get(key) != expected:
                    raise ReleaseStateError(
                        f"candidate closeout evidence requires {key}={expected}"
                    )
    if len(subjects) != 1:
        raise ReleaseStateError("pre_closeout candidate evidence must bind one exact subject_commit")
    return subjects.pop()


def validate_candidate_mode(root: Path, candidate: dict[str, Any]) -> None:
    for evidence_class, relative in candidate["evidence"].items():
        _, path = safe_repo_path(root, relative, f"candidate {evidence_class} evidence")
        if path.exists():
            raise ReleaseStateError(
                "pre-closeout candidate mode requires terminal evidence to be absent; "
                f"found {relative}"
            )


def git_output(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ReleaseStateError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.strip()


def candidate_from_registry_text(text: str) -> dict[str, Any]:
    try:
        registry = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ReleaseStateError(f"invalid candidate FILE_REGISTRY.yml: {exc}") from exc
    if not isinstance(registry, dict) or not isinstance(registry.get("migration_state"), dict):
        raise ReleaseStateError("candidate FILE_REGISTRY.yml requires migration_state")
    candidate = registry["migration_state"].get("pre_closeout_candidate")
    if not isinstance(candidate, dict):
        raise ReleaseStateError("candidate revision requires pre_closeout_candidate declaration")
    return candidate


def validate_evidence_persistence(
    root: Path, candidate_revision: str, evidence_revision: str
) -> dict[str, str]:
    """Prove an evidence-only revision did not mutate its assured candidate."""
    candidate_sha = git_output(root, "rev-parse", "--verify", f"{candidate_revision}^{{commit}}")
    evidence_sha = git_output(root, "rev-parse", "--verify", f"{evidence_revision}^{{commit}}")
    if candidate_sha == evidence_sha:
        raise ReleaseStateError("candidate and evidence revisions must differ")
    parent_line = git_output(root, "rev-list", "--parents", "-n", "1", evidence_sha).split()
    if len(parent_line) != 2 or parent_line[1] != candidate_sha:
        raise ReleaseStateError(
            "evidence revision must directly descend from candidate revision as its only parent"
        )
    candidate = candidate_from_registry_text(
        git_output(root, "show", f"{candidate_sha}:FILE_REGISTRY.yml")
    )
    evidence_candidate = candidate_from_registry_text(
        git_output(root, "show", f"{evidence_sha}:FILE_REGISTRY.yml")
    )
    if evidence_candidate != candidate:
        raise ReleaseStateError("evidence revision mutated pre_closeout_candidate declaration")

    evidence = candidate.get("required_evidence")
    if not isinstance(evidence, dict) or set(evidence) != set(CANDIDATE_EVIDENCE_TYPES):
        raise ReleaseStateError("candidate revision has malformed required_evidence")
    allowed_paths = set()
    for evidence_class in CANDIDATE_EVIDENCE_TYPES:
        value = evidence[evidence_class]
        if not isinstance(value, str):
            raise ReleaseStateError("candidate revision required evidence paths must be strings")
        allowed_paths.add(value)
        evidence_at_candidate = git_output(
            root, "ls-tree", "-r", "--name-only", candidate_sha, "--", value
        )
        if evidence_at_candidate:
            raise ReleaseStateError(
                "candidate revision must not already contain declared terminal evidence"
            )
    changed = set(
        filter(None, git_output(root, "diff", "--name-only", f"{candidate_sha}..{evidence_sha}").splitlines())
    )
    if changed != allowed_paths:
        raise ReleaseStateError(
            "evidence revision may change exactly the declared evidence manifest; "
            f"expected {sorted(allowed_paths)}, found {sorted(changed)}"
        )
    for evidence_class, expected_type in CANDIDATE_EVIDENCE_TYPES.items():
        relative = str(evidence[evidence_class])
        text = git_output(root, "show", f"{evidence_sha}:{relative}")
        frontmatter, _ = parse_frontmatter_text(text, f"evidence revision {relative}")
        if frontmatter.get("artifact_type") != expected_type:
            raise ReleaseStateError(f"evidence revision {relative} has wrong artifact_type")
        expected_verdict = CANDIDATE_EVIDENCE_VERDICTS.get(evidence_class)
        if expected_verdict and frontmatter.get("verdict") != expected_verdict:
            raise ReleaseStateError(
                f"evidence revision {relative} requires verdict={expected_verdict}"
            )
        if frontmatter.get("subject_commit") != candidate_sha:
            raise ReleaseStateError(
                f"evidence revision {relative} must bind candidate SHA {candidate_sha}"
            )
    return {"candidate_revision": candidate_sha, "evidence_revision": evidence_sha}


def validate_current_candidate_persistence(root: Path, candidate: dict[str, Any], reported_subject: str) -> None:
    """Find the exact evidence-only transition in current HEAD ancestry."""
    head = git_output(root, "rev-parse", "--verify", "HEAD^{commit}")
    matches: list[dict[str, str]] = []
    for evidence_revision in git_output(root, "rev-list", "--topo-order", head).splitlines():
        parent_line = git_output(root, "rev-list", "--parents", "-n", "1", evidence_revision).split()
        if len(parent_line) != 2:
            continue
        candidate_revision = parent_line[1]
        try:
            persisted_candidate = candidate_from_registry_text(
                git_output(root, "show", f"{candidate_revision}:FILE_REGISTRY.yml")
            )
        except ReleaseStateError:
            continue
        if persisted_candidate != candidate["declaration"]:
            continue
        try:
            matches.append(validate_evidence_persistence(root, candidate_revision, evidence_revision))
        except ReleaseStateError:
            continue
    if len(matches) != 1:
        raise ReleaseStateError(
            "ordinary candidate completion requires exactly one persisted evidence-only transition"
        )
    if reported_subject != matches[0]["candidate_revision"]:
        raise ReleaseStateError(
            "pre_closeout candidate evidence must bind the persisted candidate revision"
        )
    candidate_revision = matches[0]["candidate_revision"]
    for relative in candidate["manifest"]:
        candidate_blob = git_output(root, "rev-parse", f"{candidate_revision}:{relative}")
        current_blob = git_output(root, "rev-parse", f"HEAD:{relative}")
        if current_blob != candidate_blob:
            raise ReleaseStateError(
                "current HEAD differs from persisted candidate normative manifest: "
                f"{relative}"
            )


def validate_release_assets(root: Path, release_state: dict[str, Any]) -> None:
    for field, expected in CANONICAL_RELEASE_ASSETS.items():
        if release_state.get(field) != expected:
            raise ReleaseStateError(f"release_state.{field} must be {expected}")
        _, path = safe_repo_path(root, expected, f"release_state.{field}")
        if not path.is_file():
            raise ReleaseStateError(f"release-state asset is missing: {expected}")
    if release_state.get("authority") != "assurance_only":
        raise ReleaseStateError("release_state.authority must be assurance_only")


def normalized_structured_key(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def reject_structured_vcs_claims(
    value: object,
    label: str,
    path: str = "frontmatter",
    vcs_context: bool = False,
) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized_key = normalized_structured_key(key)
            current_path = f"{path}.{key}"
            child_vcs_context = vcs_context or bool(
                STRUCTURED_VCS_PARENT_RE.fullmatch(normalized_key)
            )
            is_direct_vcs_key = bool(STRUCTURED_VCS_KEY_RE.fullmatch(normalized_key))
            is_context_state_key = child_vcs_context and bool(
                STRUCTURED_STATE_KEY_RE.fullmatch(normalized_key)
            )
            if is_direct_vcs_key or is_context_state_key:
                if isinstance(child, str) and MUTABLE_VCS_STATE_RE.fullmatch(child.strip()):
                    raise ReleaseStateError(
                        f"{label} contains mutable GitHub/VCS state at {current_path}"
                    )
            reject_structured_vcs_claims(
                child,
                label,
                current_path,
                child_vcs_context,
            )
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_structured_vcs_claims(
                child,
                label,
                f"{path}[{index}]",
                vcs_context,
            )


def normalize_markdown_decoration(text: str) -> str:
    """Remove Markdown emphasis markers before semantic VCS-state matching."""
    return MARKDOWN_DECORATION_RE.sub("", text)


def reject_mutable_vcs_claims(
    text: str, label: str, structured: object | None = None
) -> None:
    if structured is not None:
        reject_structured_vcs_claims(structured, label)
    for pattern in RAW_MUTABLE_CLOSEOUT_PATTERNS:
        if pattern.search(text):
            raise ReleaseStateError(f"{label} contains mutable GitHub/VCS state: {pattern.pattern}")
    normalized_text = normalize_markdown_decoration(text)
    for pattern in NORMALIZED_MUTABLE_CLOSEOUT_PATTERNS:
        if pattern.search(normalized_text):
            raise ReleaseStateError(f"{label} contains mutable GitHub/VCS state: {pattern.pattern}")


def validate_external_vcs_boundary(value: str) -> None:
    normalized = value.strip()
    prefix = "non-normative"
    if not normalized.lower().startswith(prefix):
        raise ReleaseStateError("successful closeout must mark external VCS state non-normative")
    remainder = normalized[len(prefix) :]
    if MUTABLE_VCS_STATE_TOKEN_RE.search(remainder):
        raise ReleaseStateError(
            "external VCS state marker contains concrete mutable GitHub/VCS state"
        )


def validate_completed_closeout_reports(
    root: Path,
    completed_records: dict[str, dict[str, Any]],
    canonical_closeout: str,
) -> None:
    reports_root = root / "docs/reports/closeout"
    if not reports_root.is_dir():
        return

    completed_by_id = {
        str(record["frontmatter"]["work_block_id"]): record
        for record in completed_records.values()
    }
    seen: dict[str, str] = {}

    for path in sorted(reports_root.rglob("*.md")):
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ReleaseStateError(
                f"cannot read closeout report {path}: {exc}"
            ) from exc
        if not raw.startswith("---\n"):
            continue

        relative = path.relative_to(root).as_posix()
        label = f"completed Work Block closeout {relative}"
        frontmatter, body, _ = parse_frontmatter(path, label)
        if frontmatter.get("artifact_type") != "closeout_report":
            continue

        work_block_id = frontmatter.get("work_block_id")
        if work_block_id not in completed_by_id:
            continue
        if work_block_id in seen:
            raise ReleaseStateError(
                f"completed Work Block {work_block_id} has multiple closeout reports: "
                f"{seen[work_block_id]} and {relative}"
            )
        seen[str(work_block_id)] = relative
        if relative == canonical_closeout:
            continue

        if frontmatter.get("status") != "approved":
            raise ReleaseStateError(f"{label} must be approved")

        markers = parse_markers(body, label)
        required_exact = {
            "stage execution state": "completed",
            "review verdict": "READY",
            "verification verdict": "READY",
            "drift verdict": "ALIGNED",
            "closeout classification": "SUCCESS",
            "task status": "completed",
        }
        for key, expected in required_exact.items():
            actual = markers.get(key)
            if actual != expected:
                raise ReleaseStateError(
                    f"{label} requires {key}={expected}, found {actual!r}"
                )

        work_block_evaluation = completed_by_id[str(work_block_id)][
            "markers"
        ].get("evaluation verdict")
        closeout_evaluation = markers.get("evaluation verdict")
        if work_block_evaluation is not None:
            expected_evaluation = evaluation_verdict(
                work_block_evaluation,
                f"completed Work Block {work_block_id} evaluation verdict",
            )
            if closeout_evaluation is None:
                raise ReleaseStateError(
                    f"{label} requires evaluation verdict={expected_evaluation}"
                )
            actual_evaluation = evaluation_verdict(
                closeout_evaluation, f"{label} evaluation verdict"
            )
            if actual_evaluation != expected_evaluation:
                raise ReleaseStateError(
                    f"{label} requires evaluation verdict={expected_evaluation}, "
                    f"found {actual_evaluation!r}"
                )
        elif closeout_evaluation is not None:
            evaluation_verdict(
                closeout_evaluation, f"{label} evaluation verdict"
            )

        validate_external_vcs_boundary(markers.get("external vcs state", ""))
        extract_single_section(
            body, "Residual Risks and Limitations", label
        )
        extract_single_section(body, "Follow-Up Work", label)


def validate_closeout(
    root: Path,
    release_state: dict[str, Any],
    completed: list[str],
    completed_records: dict[str, dict[str, Any]],
) -> None:
    latest = release_state.get("latest_completed_work_block")
    closeout_value = release_state.get("closeout_report")
    if latest not in completed:
        raise ReleaseStateError(
            "release_state.latest_completed_work_block must be listed in completed_work_blocks"
        )
    if latest != completed[-1]:
        raise ReleaseStateError(
            "release_state.latest_completed_work_block must be the final completed_work_blocks entry"
        )
    latest_normalized, _ = safe_repo_path(root, latest, "latest_completed_work_block")
    closeout_normalized, closeout_path = safe_repo_path(root, closeout_value, "closeout_report")
    if not closeout_normalized.startswith("docs/reports/closeout/"):
        raise ReleaseStateError("closeout_report must be under docs/reports/closeout/")
    if not closeout_path.is_file():
        raise ReleaseStateError(f"closeout report is missing: {closeout_normalized}")
    frontmatter, body, full_text = parse_frontmatter(
        closeout_path, f"closeout report {closeout_normalized}"
    )
    if frontmatter.get("artifact_type") != "closeout_report":
        raise ReleaseStateError("release_state.closeout_report is not a closeout report")
    if frontmatter.get("status") != "approved":
        raise ReleaseStateError("release-state closeout report must be approved")

    latest_record = completed_records[latest_normalized]
    expected_work_block_id = latest_record["frontmatter"].get("work_block_id")
    if frontmatter.get("work_block_id") != expected_work_block_id:
        raise ReleaseStateError("closeout work_block_id does not exactly match latest Work Block")

    markers = parse_markers(body, "closeout")
    required_exact = {
        "stage execution state": "completed",
        "review verdict": "READY",
        "verification verdict": "READY",
        "drift verdict": "ALIGNED",
        "closeout classification": "SUCCESS",
        "task status": "completed",
    }
    for key, expected in required_exact.items():
        actual = markers.get(key)
        if actual != expected:
            raise ReleaseStateError(
                f"successful closeout requires {key}={expected}, found {actual!r}"
            )

    work_block_evaluation = latest_record["markers"].get("evaluation verdict")
    closeout_evaluation = markers.get("evaluation verdict")
    if work_block_evaluation is not None:
        expected_evaluation = evaluation_verdict(
            work_block_evaluation, "latest Work Block evaluation verdict"
        )
        if closeout_evaluation is None:
            raise ReleaseStateError(
                f"successful closeout requires evaluation verdict={expected_evaluation} "
                "because the latest Work Block declares evaluation"
            )
        actual_evaluation = evaluation_verdict(closeout_evaluation, "closeout evaluation verdict")
        if actual_evaluation != expected_evaluation:
            raise ReleaseStateError(
                f"successful closeout requires evaluation verdict={expected_evaluation}, "
                f"found {actual_evaluation!r}"
            )
    elif closeout_evaluation is not None:
        evaluation_verdict(closeout_evaluation, "closeout evaluation verdict")

    external = markers.get("external vcs state", "")
    validate_external_vcs_boundary(external)
    if release_state.get("external_vcs_state") != "non_normative":
        raise ReleaseStateError("release_state.external_vcs_state must be non_normative")

    extract_single_section(body, "Residual Risks and Limitations", "closeout")
    extract_single_section(body, "Follow-Up Work", "closeout")
    reject_mutable_vcs_claims(full_text, "closeout", frontmatter)


def top_level_frontmatter_field_count(text: str, field: str) -> int:
    """Return structural top-level occurrences of a YAML frontmatter field.

    ``safe_load`` intentionally accepts duplicate mapping keys by retaining the
    final value and resolves YAML merge keys.  The release-state binding must
    instead fail closed when a tasklist provides ``specification`` more than
    once, whether directly or through a merge key.  Compose retains both the
    mapping-node pairs and merge relationships without making physical-line
    syntax authoritative.
    """
    try:
        raw_frontmatter, _ = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ReleaseStateError("tasklist has unterminated YAML frontmatter") from exc
    try:
        document = yaml.compose(raw_frontmatter)
    except yaml.YAMLError as exc:
        raise ReleaseStateError(f"invalid tasklist frontmatter: {exc}") from exc
    if not isinstance(document, MappingNode):
        raise ReleaseStateError("tasklist frontmatter must be an object")
    def merged_field_count(node: object, ancestry: set[int]) -> int:
        """Count ``field`` declarations contributing to one mapping.

        YAML aliases share composed nodes.  Count every occurrence in the
        current merge expression, while rejecting a recursive merge graph
        rather than silently treating it as an absent binding.
        """
        if isinstance(node, MappingNode):
            node_id = id(node)
            if node_id in ancestry:
                raise ReleaseStateError("tasklist frontmatter contains recursive YAML merge")
            next_ancestry = ancestry | {node_id}
            count = 0
            for key, value in node.value:
                if not isinstance(key, ScalarNode):
                    continue
                if key.value == field:
                    count += 1
                elif key.value == "<<":
                    count += merged_field_count(value, next_ancestry)
            return count
        if isinstance(node, SequenceNode):
            return sum(merged_field_count(item, ancestry) for item in node.value)
        raise ReleaseStateError("tasklist frontmatter contains invalid YAML merge value")

    return merged_field_count(document, set())


def validate_latest_formal_specification(
    root: Path,
    latest_relative: str,
    latest_record: dict[str, Any],
    *,
    require_sibling_tasklist: bool = True,
) -> None:
    """Validate an explicit separate-specification binding for the latest formal Work Block."""
    frontmatter = latest_record["frontmatter"]
    if frontmatter.get("governance_profile") not in FORMAL_GOVERNANCE_PROFILES:
        return

    latest_normalized, _ = safe_repo_path(
        root, latest_relative, "latest_completed_work_block"
    )
    if not latest_normalized.startswith("docs/plans/") or not latest_normalized.endswith(".md"):
        raise ReleaseStateError(
            "latest completed formal Work Block must be under docs/plans"
        )
    tasklist_relative = "docs/tasklist/" + latest_normalized.removeprefix("docs/plans/")
    _, tasklist_path = safe_repo_path(
        root, tasklist_relative, "latest completed formal Work Block sibling tasklist"
    )
    if not tasklist_path.is_file():
        if not require_sibling_tasklist:
            return
        raise ReleaseStateError(
            "latest completed formal Work Block requires sibling tasklist: "
            f"{tasklist_relative}"
        )

    tasklist, _, tasklist_text = parse_frontmatter(
        tasklist_path, f"latest completed formal Work Block tasklist {tasklist_relative}"
    )
    if tasklist.get("artifact_type") != "tasklist":
        raise ReleaseStateError(
            "latest completed formal Work Block sibling is not a tasklist: "
            f"{tasklist_relative}"
        )
    if tasklist.get("work_block_id") != frontmatter.get("work_block_id"):
        raise ReleaseStateError(
            "latest completed formal Work Block tasklist work_block_id does not match"
        )

    specification_count = top_level_frontmatter_field_count(tasklist_text, "specification")
    if specification_count > 1:
        raise ReleaseStateError(
            "latest completed formal Work Block tasklist contains duplicate specification fields"
        )
    if specification_count == 0:
        return

    specification_value = tasklist.get("specification")
    specification_relative, specification_path = safe_repo_path(
        root,
        specification_value,
        "latest completed formal Work Block tasklist specification",
    )
    if not specification_relative.startswith("docs/specs/") or not specification_relative.endswith(
        ".md"
    ):
        raise ReleaseStateError(
            "latest completed formal Work Block tasklist specification must be under docs/specs"
        )
    if not specification_path.is_file():
        raise ReleaseStateError(
            "latest completed formal Work Block specification is missing: "
            f"{specification_relative}"
        )
    specification, _, _ = parse_frontmatter(
        specification_path,
        f"latest completed formal Work Block specification {specification_relative}",
    )
    if specification.get("artifact_type") != "specification":
        raise ReleaseStateError(
            "latest completed formal Work Block target is not a specification: "
            f"{specification_relative}"
        )
    if specification.get("work_block_id") != frontmatter.get("work_block_id"):
        raise ReleaseStateError(
            "latest completed formal Work Block specification work_block_id does not match"
        )
    if specification.get("status") != "approved":
        raise ReleaseStateError(
            "latest completed formal Work Block specification must be status approved"
        )


def migration_section(text: str) -> str:
    matches = list(MIGRATION_SECTION_RE.finditer(text))
    if not matches:
        raise ReleaseStateError("PROJECT_MAP.md requires one visible Migration Work section")
    if len(matches) != 1:
        raise ReleaseStateError("PROJECT_MAP.md must contain exactly one Migration Work section")
    return matches[0].group("body")


def validate_map_projection(text: str, active: str | None) -> None:
    for pattern in STALE_MAP_PATTERNS:
        if pattern.search(text):
            raise ReleaseStateError(f"PROJECT_MAP.md contains stale GitHub state: {pattern.pattern}")
    section = migration_section(text)
    no_active = "No active implementation Work Block." in section
    if active is None:
        if not no_active:
            raise ReleaseStateError(
                "PROJECT_MAP.md Migration Work section must state that no active implementation Work Block exists"
            )
    else:
        if no_active:
            raise ReleaseStateError(
                "PROJECT_MAP.md Migration Work section contradicts active Work Block state"
            )
        if f"`{active}`" not in section:
            raise ReleaseStateError(
                "PROJECT_MAP.md Migration Work section omits active Work Block"
            )


def validate_repository(root: Path, *, candidate_mode: bool = False) -> dict[str, Any]:
    root = root.resolve()
    registry_path = root / "FILE_REGISTRY.yml"
    registry = load_yaml_object(registry_path, "FILE_REGISTRY.yml")
    migration = registry.get("migration_state")
    if not isinstance(migration, dict):
        raise ReleaseStateError("FILE_REGISTRY.yml requires migration_state")
    candidate_field_count = direct_yaml_mapping_field_count(
        registry_path, "migration_state", "pre_closeout_candidate"
    )
    if candidate_field_count > 1:
        raise ReleaseStateError("FILE_REGISTRY.yml contains duplicate pre_closeout_candidate fields")
    if migration.get("pre_closeout_candidate") is not None and candidate_field_count != 1:
        raise ReleaseStateError(
            "pre_closeout_candidate must be a direct FILE_REGISTRY migration_state field"
        )
    completed = string_list(migration.get("completed_work_blocks"), "completed_work_blocks")
    completed_set = set(completed)
    completed_records: dict[str, dict[str, Any]] = {}
    work_block_ids: set[str] = set()
    for relative in completed:
        frontmatter, markers = validate_completed_work_block(root, relative)
        normalized = relative.strip().replace("\\", "/")
        work_block_id = str(frontmatter["work_block_id"])
        if work_block_id in work_block_ids:
            raise ReleaseStateError(f"duplicate completed work_block_id: {work_block_id}")
        work_block_ids.add(work_block_id)
        completed_records[normalized] = {"frontmatter": frontmatter, "markers": markers}

    active_value = migration.get("active_work_block")
    active: str | None
    if active_value is None:
        active = None
    else:
        active, _ = safe_repo_path(root, active_value, "active_work_block")
        if active in completed_set:
            raise ReleaseStateError("active Work Block cannot also be completed")
        active_frontmatter = validate_active_work_block(root, active)
        if active_frontmatter.get("work_block_id") in work_block_ids:
            raise ReleaseStateError("active Work Block ID duplicates a completed Work Block ID")

    map_state, map_text = parse_map_state(root / "PROJECT_MAP.md")
    map_completed = string_list(
        map_state.get("completed_work_blocks"), "PROJECT_MAP completed_work_blocks"
    )
    map_active = map_state.get("active_work_block")
    if map_completed != completed:
        raise ReleaseStateError("PROJECT_MAP completed Work Blocks do not match FILE_REGISTRY.yml")
    if map_active != active:
        raise ReleaseStateError("PROJECT_MAP active Work Block does not match FILE_REGISTRY.yml")
    validate_map_projection(map_text, active)

    candidate = validate_pre_closeout_candidate(
        root, migration, completed, map_state, map_text, active
    )

    release_state = registry.get("release_state")
    if not isinstance(release_state, dict):
        raise ReleaseStateError("FILE_REGISTRY.yml requires release_state")
    validate_release_assets(root, release_state)
    validate_completed_closeout_reports(
        root, completed_records, str(release_state.get("closeout_report", ""))
    )
    validate_closeout(root, release_state, completed, completed_records)
    latest = str(release_state["latest_completed_work_block"])
    validate_latest_formal_specification(root, latest, completed_records[latest])

    if candidate_mode:
        if candidate is None:
            raise ReleaseStateError("pre-closeout candidate mode requires an explicit declaration")
        validate_candidate_mode(root, candidate)
        validate_latest_formal_specification(
            root,
            candidate["work_block"],
            candidate["record"],
        )
        return {
            "completed_work_blocks": completed,
            "active_work_block": active,
            "latest_completed_work_block": release_state["latest_completed_work_block"],
            "closeout_report": release_state["closeout_report"],
            "candidate_work_block": candidate["work_block"],
            "verdict": "CANDIDATE_READY",
        }

    effective_candidate = None
    effective_completed = completed.copy()
    effective_latest = release_state["latest_completed_work_block"]
    if candidate is not None:
        effective_candidate = candidate["work_block"]
        reported_subject = validate_candidate_evidence(root, candidate)
        validate_current_candidate_persistence(root, candidate, reported_subject)
        validate_latest_formal_specification(
            root,
            effective_candidate,
            candidate["record"],
        )
        effective_completed.append(effective_candidate)
        effective_latest = effective_candidate

    return {
        "completed_work_blocks": completed,
        "active_work_block": active,
        "latest_completed_work_block": release_state["latest_completed_work_block"],
        "closeout_report": release_state["closeout_report"],
        "effective_completed_candidate": effective_candidate,
        "effective_completed_work_blocks": effective_completed,
        "effective_latest_completed_work_block": effective_latest,
        "verdict": "READY",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--pre-closeout-candidate",
        action="store_true",
        help="validate one explicit local assurance-pending candidate",
    )
    mode.add_argument(
        "--verify-evidence-persistence",
        nargs=2,
        metavar=("CANDIDATE_REV", "EVIDENCE_REV"),
        help="prove an evidence revision changes only the candidate's declared evidence files",
    )
    args = parser.parse_args()
    try:
        if args.verify_evidence_persistence:
            result = validate_evidence_persistence(
                args.root,
                args.verify_evidence_persistence[0],
                args.verify_evidence_persistence[1],
            )
            print("Evidence persistence: READY")
            print(f"Candidate revision: {result['candidate_revision']}")
            print(f"Evidence revision: {result['evidence_revision']}")
            return 0
        result = validate_repository(args.root, candidate_mode=args.pre_closeout_candidate)
    except ReleaseStateError as exc:
        print(f"RELEASE STATE BLOCKED: {exc}", file=sys.stderr)
        return 1
    print(f"Release-state contract: {result['verdict']}")
    print(f"Completed Work Blocks: {len(result['completed_work_blocks'])}")
    print(f"Active Work Block: {result['active_work_block'] or 'none'}")
    print(f"Latest completed: {result['latest_completed_work_block']}")
    if result.get("candidate_work_block"):
        print(f"Candidate Work Block: {result['candidate_work_block']}")
    if result.get("effective_completed_candidate"):
        print(f"Effective completed candidate: {result['effective_completed_candidate']}")
        print(f"Effective latest completed: {result['effective_latest_completed_work_block']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
