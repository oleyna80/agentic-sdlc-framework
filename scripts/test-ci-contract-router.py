#!/usr/bin/env python3
"""Contract fixtures for fail-closed CI routing and provider snapshot semantics."""
from __future__ import annotations

import importlib.util
from pathlib import Path

PATH = Path(__file__).with_name("ci-contract-router.py")
SPEC = importlib.util.spec_from_file_location("ci_contract_router", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

assert MODULE.route(["template/scripts/repair-lifecycle.py"])["suite"] == "targeted"
assert MODULE.route(["product/app.py"])["suite"] == "full"
assert MODULE.route([])["suite"] == "full"
assert MODULE.route(["template/a path.py"])["suite"] == "targeted"
assert MODULE.route(["scripts/test-sdd-contract.sh"])["required"] == ["sdd", "governance", "publication", "release-state"]

base = {
    "repository": "example/framework",
    "head_sha": "head123",
    "workflow_sha": "merge456",
    "workflow_name": "Framework Contracts",
    "workflow_ref": "example/framework/.github/workflows/framework-contracts.yml@refs/pull/9/merge",
    "run_id": "30377306228",
    "run_attempt": "2",
    "event_name": "pull_request",
    "job_key": "contracts",
    "job_name": "contracts",
    "job_result": "success",
}
partial = MODULE.build_provider_snapshot(**base)
assert partial["evidence_status"] == "PARTIAL"
assert partial["authority"] == "none"
assert partial["temporal_semantics"] == "point_in_time"
assert partial["subject"] == {"head_sha": "head123", "workflow_sha": "merge456"}
assert partial["job"]["key"] == "contracts"
assert partial["job"]["result"] == "success"
assert partial["job"]["result_source"] == "github-actions-needs-context"
assert partial["coverage"]["scope"] == "current_workflow_job_only"
assert partial["coverage"]["complete_merge_authority"] is False
assert any("not a merge verdict" in item for item in partial["limitations"])

failed = MODULE.build_provider_snapshot(**{**base, "job_result": "failure"})
assert failed["evidence_status"] == "PARTIAL"
assert failed["job"]["result"] == "failure"

unverified_result = MODULE.build_provider_snapshot(**{**base, "job_result": ""})
assert unverified_result["evidence_status"] == "UNVERIFIED"
assert unverified_result["job"]["result"] == "unknown"

unverified_identity = MODULE.build_provider_snapshot(**{**base, "head_sha": ""})
assert unverified_identity["evidence_status"] == "UNVERIFIED"

print("OK: CI route and provider snapshot temporal-semantics fixtures")
