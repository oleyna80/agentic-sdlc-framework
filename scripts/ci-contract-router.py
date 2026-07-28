#!/usr/bin/env python3
"""Fail-closed routing and provider-check snapshot validation for CI contracts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

ALWAYS_REQUIRED = ("sdd", "governance", "publication", "release-state")
ALLOWLISTS = {
    "ci_bootstrap_runtime_validation": (
        ".github/", "bootstrap/", "template/", "scripts/", "governance/", "docs/",
        "FILE_REGISTRY.yml", "PROJECT_MAP.md",
    ),
}


def route(paths: Iterable[str]) -> dict[str, object]:
    paths = [path for path in paths if path]
    known = bool(paths) and all(
        any(path == prefix or path.startswith(prefix) for prefix in prefixes)
        for path in paths
        for prefixes in ALLOWLISTS.values()
    )
    suite = "targeted" if known else "full"
    return {
        "suite": suite,
        "required": list(ALWAYS_REQUIRED),
        "optional": ["profile-conformance", "integration-adapters", "codex-adapter"] if suite == "full" else [],
        "paths": paths,
    }


def validate_snapshot(snapshot: dict, subject_sha: str, required_checks: Iterable[str]) -> list[str]:
    errors: list[str] = []
    if snapshot.get("subject_sha") != subject_sha:
        errors.append("snapshot subject_sha does not match the CI subject SHA")
    checks = snapshot.get("check_runs")
    if not isinstance(checks, list):
        return errors + ["snapshot check_runs must be a list"]
    by_name = {item.get("name"): item for item in checks if isinstance(item, dict)}
    for name in required_checks:
        check = by_name.get(name)
        if not check:
            errors.append(f"required provider check missing: {name}")
        elif check.get("head_sha") != subject_sha:
            errors.append(f"required provider check is not bound to subject SHA: {name}")
        elif check.get("status") != "completed" or check.get("conclusion") != "success":
            errors.append(f"required provider check is not successful: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    routing = sub.add_parser("route")
    routing.add_argument("paths", nargs="*")
    routing.add_argument("--paths-file", type=Path, help="NUL-delimited changed-path list")
    snapshot = sub.add_parser("validate-snapshot")
    snapshot.add_argument("--snapshot", type=Path, required=True)
    snapshot.add_argument("--subject-sha", required=True)
    snapshot.add_argument("--required-check", action="append", required=True)
    args = parser.parse_args()
    if args.command == "route":
        paths = args.paths
        if args.paths_file:
            paths += [path.decode("utf-8") for path in args.paths_file.read_bytes().split(b"\0") if path]
        print(json.dumps(route(paths), sort_keys=True))
        return 0
    try:
        value = json.loads(args.snapshot.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: unreadable provider snapshot: {exc}")
        return 1
    errors = validate_snapshot(value, args.subject_sha, args.required_check)
    if errors:
        print("BLOCKED: " + "; ".join(errors))
        return 1
    print("READY: provider-native snapshot matches subject SHA and required checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
