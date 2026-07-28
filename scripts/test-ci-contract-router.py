#!/usr/bin/env python3
"""Contract fixtures for fail-closed CI routing and snapshot aggregation."""
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
good = {"subject_sha": "abc", "check_runs": [{"name": "Framework Contracts / contracts", "head_sha": "abc", "status": "completed", "conclusion": "success"}]}
assert not MODULE.validate_snapshot(good, "abc", ["Framework Contracts / contracts"])
assert MODULE.validate_snapshot(good, "def", ["Framework Contracts / contracts"])
assert MODULE.validate_snapshot({"subject_sha": "abc", "check_runs": []}, "abc", ["Framework Contracts / contracts"])
assert MODULE.validate_snapshot({"subject_sha": "abc", "check_runs": [{"name": "Framework Contracts / contracts", "status": "in_progress", "conclusion": None}]}, "abc", ["Framework Contracts / contracts"])
assert MODULE.validate_snapshot({"subject_sha": "abc", "check_runs": [{"name": "Framework Contracts / contracts", "head_sha": "wrong", "status": "completed", "conclusion": "success"}]}, "abc", ["Framework Contracts / contracts"])
print("OK: CI contract router fail-closed fixtures")
