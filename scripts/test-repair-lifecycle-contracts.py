#!/usr/bin/env python3
"""Adversarial fixtures for NDR record and template contracts."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
import yaml

ROOT = Path(__file__).parents[1]
PATH = ROOT / "template/scripts/repair-lifecycle.py"
SPEC = importlib.util.spec_from_file_location("repair_lifecycle", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

domains = {domain: False for domain in MODULE.PROHIBITED_DOMAINS}
base = {
    "mode": "NDR", "risk": "low", "deterministic": True, "reversible": True,
    "architecture_decision_required": False, "prohibited_domains": domains,
    "implementation_passes": 1, "correction_rounds": 1,
    "allowlist": ["scripts/example.py"], "problem": "p", "root_cause": "r",
    "verification_commands": ["python scripts/example.py"], "stop_condition": "owner",
    "integration_stabilization": {"items": ["one", "two", "three"], "correction_rounds": 2},
}
assert not MODULE.validate(base, ["scripts/example.py"])
for key, value in (("risk", "high"), ("deterministic", False), ("reversible", False), ("architecture_decision_required", True), ("implementation_passes", 2), ("correction_rounds", 2)):
    assert MODULE.validate({**base, key: value}), key
assert MODULE.validate({**base, "prohibited_domains": {**domains, "deploy": True}})
assert MODULE.validate({**base, "allowlist": ["src/product.py"]})
assert MODULE.validate({**base, "integration_stabilization": {"items": [1, 2, 3, 4], "correction_rounds": 0}})
assert MODULE.validate({**base, "integration_stabilization": {"items": [], "correction_rounds": 3}})
assert MODULE.validate(base, ["scripts/other.py"])
assert MODULE.validate(base, None)
assert MODULE.validate(base, [])
assert not MODULE.validate(base, ["scripts/example.py"])
assert MODULE.validate(base, ["src/product.py"])
assert MODULE.validate(base, ["scripts/example.py", "src/product.py"])
for bypass in ("./scripts/example.py", "scripts//example.py", "scripts/../example.py", "scripts/./example.py", "scripts\\example.py", "/scripts/example.py"):
    assert MODULE.validate(base, [bypass]), bypass
for bypass in ("./scripts/example.py", "scripts//example.py", "scripts/../example.py", "scripts/./example.py"):
    assert MODULE.validate({**base, "allowlist": [bypass]}, [bypass]), bypass

template = ROOT / "template/docs/templates/repair-record-template.md"
assert not MODULE.validate(MODULE.load_record(template), ["scripts/example.py"])
registry = yaml.safe_load((ROOT / "template/FILE_REGISTRY.yml").read_text(encoding="utf-8"))
assert registry["evaluation_assurance"]["contract"] == "governance/evaluation.md"
assert registry["repair_assurance"]["validator"] == "scripts/repair-lifecycle.py"
with tempfile.TemporaryDirectory() as temp:
    record = Path(temp) / "record.md"
    record.write_text("# record\n```json\n" + json.dumps(base) + "\n```\n", encoding="utf-8")
    assert MODULE.load_record(record) == base
print("OK: NDR repair lifecycle, Markdown record, and registry-root contracts")
