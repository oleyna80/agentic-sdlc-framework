#!/usr/bin/env python3
"""Fail-closed CI routing and non-authoritative provider evidence capture."""
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
TERMINAL_JOB_RESULTS = {"success", "failure", "cancelled", "skipped"}


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


def build_provider_snapshot(
    *,
    repository: str,
    head_sha: str,
    workflow_sha: str,
    workflow_name: str,
    workflow_ref: str,
    run_id: str,
    run_attempt: str,
    event_name: str,
    job_key: str,
    job_name: str,
    job_result: str,
) -> dict[str, object]:
    identity_values = (
        repository,
        head_sha,
        workflow_sha,
        workflow_name,
        workflow_ref,
        run_id,
        run_attempt,
        event_name,
        job_key,
        job_name,
    )
    evidence_status = (
        "PARTIAL"
        if all(identity_values) and job_result in TERMINAL_JOB_RESULTS
        else "UNVERIFIED"
    )
    return {
        "schema_version": 1,
        "artifact_type": "provider_job_snapshot",
        "authority": "none",
        "temporal_semantics": "point_in_time",
        "evidence_status": evidence_status,
        "repository": repository,
        "subject": {
            "head_sha": head_sha,
            "workflow_sha": workflow_sha,
        },
        "workflow_run": {
            "name": workflow_name,
            "ref": workflow_ref,
            "run_id": run_id,
            "run_attempt": run_attempt,
            "event_name": event_name,
            "url": f"https://github.com/{repository}/actions/runs/{run_id}" if repository and run_id else None,
        },
        "job": {
            "key": job_key,
            "name": job_name,
            "result": job_result or "unknown",
            "result_source": "github-actions-needs-context",
        },
        "coverage": {
            "scope": "current_workflow_job_only",
            "complete_merge_authority": False,
        },
        "limitations": [
            "This artifact records only the current Framework Contracts job result at capture time.",
            "It does not replace or duplicate repository required checks.",
            "It is not a merge verdict and cannot block merge.",
            "It does not guarantee the absence of later reruns or provider-state changes.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    routing = sub.add_parser("route")
    routing.add_argument("paths", nargs="*")
    routing.add_argument("--paths-file", type=Path, help="NUL-delimited changed-path list")

    snapshot = sub.add_parser("snapshot")
    snapshot.add_argument("--output", type=Path, required=True)
    snapshot.add_argument("--repository", required=True)
    snapshot.add_argument("--head-sha", required=True)
    snapshot.add_argument("--workflow-sha", required=True)
    snapshot.add_argument("--workflow-name", required=True)
    snapshot.add_argument("--workflow-ref", required=True)
    snapshot.add_argument("--run-id", required=True)
    snapshot.add_argument("--run-attempt", required=True)
    snapshot.add_argument("--event-name", required=True)
    snapshot.add_argument("--job-key", required=True)
    snapshot.add_argument("--job-name", required=True)
    snapshot.add_argument("--job-result", default="")

    args = parser.parse_args()
    if args.command == "route":
        paths = args.paths
        if args.paths_file:
            paths += [path.decode("utf-8") for path in args.paths_file.read_bytes().split(b"\0") if path]
        print(json.dumps(route(paths), sort_keys=True))
        return 0

    value = build_provider_snapshot(
        repository=args.repository,
        head_sha=args.head_sha,
        workflow_sha=args.workflow_sha,
        workflow_name=args.workflow_name,
        workflow_ref=args.workflow_ref,
        run_id=args.run_id,
        run_attempt=args.run_attempt,
        event_name=args.event_name,
        job_key=args.job_key,
        job_name=args.job_name,
        job_result=args.job_result,
    )
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{value['evidence_status']}: wrote non-authoritative provider snapshot to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
