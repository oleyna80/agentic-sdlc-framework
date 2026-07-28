#!/usr/bin/env python3
"""Validate public framework inventory, profiles, configs, tests, and privacy."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - CI installs PyYAML
    raise SystemExit("PyYAML is required for publication validation") from exc

ROOT = Path(__file__).resolve().parents[1]
FAILURES: list[str] = []
PYTHON = sys.executable
BASH = os.environ.get("BASH", "bash")

REQUIRED_FILES = [
    "README.md",
    "SETUP.md",
    "PROJECT_MAP.md",
    "FILE_REGISTRY.yml",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "PUBLICATION_CHECKLIST.md",
    "bootstrap.sh",
    "bootstrap/README.md",
    "bootstrap/profiles.json",
    "bootstrap/bootstrap_project.py",
    "governance/README.md",
    "governance/authority.md",
    "governance/lifecycle.md",
    "governance/artifacts.md",
    "governance/runtime-capabilities.md",
    "runtimes/README.md",
    "runtimes/codex/README.md",
    "runtimes/claude-code/README.md",
    "runtimes/opencode/README.md",
    "runtimes/generic/README.md",
    "integrations/README.md",
    "integrations/claude-code-codex-plugin/README.md",
    "integrations/mcp/README.md",
    "integrations/file-handoff/README.md",
    "docs/bootstrap-profiles.md",
    "docs/profiles.md",
    "docs/quickstart-minimal.md",
    "docs/session-bootstrap.md",
    "docs/mcp-tool-policy.md",
    "docs/plans/wb-005-profile-aware-bootstrap-conformance.md",
    "handoff/README.md",
    "handoff/templates/runtime-task-template.md",
    "skills/catalog.yml",
    "scripts/test-sdd-contract.sh",
    "scripts/test-bootstrap-profiles.py",
    "scripts/test-runtime-conformance.py",
    "scripts/test-integration-contracts.py",
    "scripts/test-integration-admission-evidence.py",
    "scripts/test-codex-adapter.py",
    "scripts/test-codex-hard-stops.py",
    "scripts/test-repair-lifecycle-contracts.py",
    "scripts/test-ci-contract-router.py",
    "scripts/ci-contract-router.py",
    "scripts/validate-governance.sh",
    "scripts/validate-publication.sh",
    "scripts/validate_publication.py",
    "template/project.gitignore",
    "template/AGENTS.md",
    "template/CLAUDE.md",
    "template/PROJECT_MAP.md",
    "template/FILE_REGISTRY.yml",
    "template/.agent/ROSTER.md",
    "template/.agent/active-work-block.json",
    "template/.agent/hooks/hard_stop_policy.py",
    "template/.agent/workflows/sdd-protocol.md",
    "template/scripts/bootstrap.sh",
    "template/scripts/validate-installation-profile.py",
    "template/scripts/repair-lifecycle.py",
    "template/.mcp.json",
    "template/.claude/settings.json",
    "template/.claude/hooks/work_block_gate.py",
    "template/.claude/hooks/assurance_gate.py",
    "template/.codex/hooks.json",
    "template/.codex/hooks/hard_stop_policy.py",
    "template/.codex/hooks/pre_tool_use_policy.py",
    "template/opencode.json",
    "template/.opencode/agents/architect.md",
    "template/.opencode/agents/critic.md",
    "template/.opencode/agents/coder.md",
    "template/.opencode/agents/reviewer.md",
    "template/.opencode/agents/verifier.md",
    "template/docs/templates/work-block-template.md",
    "template/docs/templates/spec-drift-report-template.md",
    "template/docs/templates/integration-admission-template.md",
    "template/docs/templates/closeout-report-template.md",
    "template/docs/templates/repair-record-template.md",
    "template/docs/templates/combined-assurance-report-template.md",
]

FORBIDDEN_PATHS = [
    "template/.gitignore",
    "template/.agent/bootstrap-profile.json",
    "template/.claude/agents/gpt-critic.md",
    "template/.claude/agents/gpt-verifier.md",
    "template/.claude/agents/codex-reviewer.md",
    "template/.claude/agent-memory/gpt-critic/MEMORY.md",
    "template/.claude/agent-memory/gpt-verifier/MEMORY.md",
    "template/.claude/agent-memory/codex-reviewer/MEMORY.md",
]

BASH_SCRIPTS = [
    "bootstrap.sh",
    "scripts/test-sdd-contract.sh",
    "scripts/validate-governance.sh",
    "scripts/validate-publication.sh",
    "template/scripts/bootstrap.sh",
    "template/.claude/hooks/critic-gate.sh",
    "template/.claude/hooks/hard-stop.sh",
    "template/.claude/hooks/typecheck.sh",
    "template/.claude/hooks/verification-gate.sh",
    "handoff/runner/cleanup.sh",
    "handoff/runner/handoff-runner.sh",
    "handoff/runner/install-systemd-user-service.sh",
    "handoff/runner/parallel-runner.sh",
    "handoff/runner/sanitize-env.sh",
    "handoff/runner/watch-queue.sh",
]

PYTHON_FILES = [
    "bootstrap/bootstrap_project.py",
    "scripts/test-bootstrap-profiles.py",
    "scripts/test-runtime-conformance.py",
    "scripts/test-codex-adapter.py",
    "scripts/test-codex-hard-stops.py",
    "scripts/test-integration-contracts.py",
    "scripts/test-integration-admission-evidence.py",
    "scripts/validate_publication.py",
    "scripts/ci-contract-router.py",
    "scripts/test-ci-contract-router.py",
    "scripts/test-repair-lifecycle-contracts.py",
    "template/scripts/validate-installation-profile.py",
    "template/scripts/repair-lifecycle.py",
    "template/.agent/hooks/hard_stop_policy.py",
    "template/.claude/hooks/work_block_gate.py",
    "template/.claude/hooks/assurance_gate.py",
    "template/.codex/hooks/hard_stop_policy.py",
    "template/.codex/hooks/pre_tool_use_policy.py",
    "template/.codex/hooks/stage0_write_gate.py",
    "template/.codex/hooks/subagent_context.py",
]

EXCLUDED_SCAN_DIRS = {
    ".git",
    "archive",
    "active",
    "done",
    "failed",
    "logs",
    "parallel",
    "queue",
    "runtime",
    "__pycache__",
}
PRIVATE_PATTERN = re.compile(
    r"azursystech|choushop|178[.]156[.]212[.]10|/home/dmitrii|/home/azur|oleyna80|home-dmitrii",
    re.I,
)
ABSOLUTE_HOME_PATTERN = re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+/")


def ok(message: str) -> None:
    print(f"OK: {message}")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    FAILURES.append(message)


def require_file(relative: str) -> None:
    if (ROOT / relative).is_file():
        ok(relative)
    else:
        fail(f"missing {relative}")


def require_absent(relative: str) -> None:
    if (ROOT / relative).exists():
        fail(f"{relative} must not exist in the publishable scaffold")
    else:
        ok(f"{relative} absent")


def file_lines(relative: str) -> list[str]:
    return (ROOT / relative).read_text(encoding="utf-8").splitlines()


def require_line(relative: str, expected: str) -> None:
    if expected in file_lines(relative):
        ok(f"{relative} contains standalone line: {expected}")
    else:
        fail(f"{relative} missing standalone line: {expected}")


def forbid_line(relative: str, forbidden: str) -> None:
    if forbidden in file_lines(relative):
        fail(f"{relative} contains forbidden blanket ignore: {forbidden}")
    else:
        ok(f"{relative} omits blanket ignore: {forbidden}")


def load_bootstrap_module() -> Any:
    path = ROOT / "bootstrap/bootstrap_project.py"
    spec = importlib.util.spec_from_file_location("bootstrap_project", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import bootstrap engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_configs() -> None:
    try:
        for relative in (
            "FILE_REGISTRY.yml",
            "template/FILE_REGISTRY.yml",
            "skills/catalog.yml",
        ):
            value = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise RuntimeError(f"{relative} must parse to a mapping")

        json_paths = (
            ".claude/settings.json",
            "bootstrap/profiles.json",
            "template/.claude/settings.json",
            "template/.mcp.json",
            "template/.agent/active-work-block.json",
            "template/.codex/hooks.json",
            "template/opencode.json",
        )
        for relative in json_paths:
            value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise RuntimeError(f"{relative} must parse to an object")

        engine = load_bootstrap_module()
        catalog = json.loads(
            (ROOT / "bootstrap/profiles.json").read_text(encoding="utf-8")
        )
        engine.validate_catalog(catalog, ROOT)
        for profile_id in catalog["profiles"]:
            state = engine.resolve_profile_state(catalog, profile_id)
            if state["resolved_profile"] != profile_id:
                raise RuntimeError(f"profile resolution drift: {profile_id}")

        referenced_skills = {
            skill
            for profile in catalog["profiles"].values()
            for set_id in profile["skill_sets"]
            for skill in catalog["skill_sets"][set_id]
        }
        missing = sorted(
            skill
            for skill in referenced_skills
            if not (ROOT / "skills" / skill / "SKILL.md").is_file()
        )
        if missing:
            raise RuntimeError(f"profile catalog references missing skills: {missing}")

        mcp = json.loads((ROOT / "template/.mcp.json").read_text(encoding="utf-8"))
        if mcp != {"mcpServers": {}}:
            raise RuntimeError("template/.mcp.json must remain empty by default")

        claude = json.loads(
            (ROOT / "template/.claude/settings.json").read_text(encoding="utf-8")
        )
        if any(key in claude for key in ("enabledMcpjsonServers", "permissions", "autoMode")):
            raise RuntimeError("template Claude settings pre-enable external integrations")
        if set(claude.get("agents", {})) != {
            "solution-architect",
            "critic",
            "reviewer",
            "scoped-coder",
            "verifier",
        }:
            raise RuntimeError("template Claude logical agent set mismatch")

        opencode = json.loads(
            (ROOT / "template/opencode.json").read_text(encoding="utf-8")
        )
        if opencode.get("mcp") != {} or opencode.get("plugin") != []:
            raise RuntimeError("template OpenCode must not enable MCP/plugins")
        if opencode.get("permission", {}).get("external_directory") != "deny":
            raise RuntimeError("template OpenCode must deny external_directory")

        skill_catalog = yaml.safe_load(
            (ROOT / "skills/catalog.yml").read_text(encoding="utf-8")
        )
        catalogued: list[str] = []
        for definition in skill_catalog.get("domains", {}).values():
            if not isinstance(definition, dict) or not isinstance(
                definition.get("skills"), list
            ):
                raise RuntimeError("invalid skill catalog domain")
            catalogued.extend(definition["skills"])
        actual = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        if set(catalogued) != actual or len(catalogued) != len(set(catalogued)):
            raise RuntimeError("skill catalog coverage mismatch")
    except Exception as exc:
        fail(f"JSON/YAML/profile configuration validation failed: {exc}")
    else:
        ok("JSON/YAML/profile configuration")


def scan_public_text() -> None:
    private_hits: list[str] = []
    home_hits: list[str] = []
    for directory, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [name for name in dirnames if name not in EXCLUDED_SCAN_DIRS]
        base = Path(directory)
        for filename in filenames:
            path = base / filename
            if path == Path(__file__).resolve():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            relative = str(path.relative_to(ROOT))
            if PRIVATE_PATTERN.search(text):
                private_hits.append(relative)
            if ABSOLUTE_HOME_PATTERN.search(text):
                home_hits.append(relative)
    if private_hits:
        fail("private project markers found in: " + ", ".join(sorted(private_hits)))
    else:
        ok("no known private project markers in public paths")
    if home_hits:
        fail("user-specific absolute home paths found in: " + ", ".join(sorted(home_hits)))
    else:
        ok("no user-specific absolute home paths in public paths")


def check_syntax() -> None:
    failed = False
    for relative in BASH_SCRIPTS:
        result = subprocess.run(
            [BASH, "-n", str(ROOT / relative)], capture_output=True, text=True
        )
        if result.returncode:
            failed = True
            fail(f"bash syntax failed: {relative}: {result.stderr.strip()}")
    for relative in PYTHON_FILES:
        try:
            compile((ROOT / relative).read_text(encoding="utf-8"), relative, "exec")
        except (OSError, SyntaxError) as exc:
            failed = True
            fail(f"Python syntax failed: {relative}: {exc}")
    if not failed:
        ok("bash and Python syntax checks")


def run_check(command: list[str], label: str) -> None:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        output = (result.stdout + "\n" + result.stderr).strip()
        fail(f"{label} failed:\n{output[-5000:]}")
    else:
        ok(label)


def smoke_profile(profile: str, expected: str) -> None:
    with tempfile.TemporaryDirectory(prefix=f"publication-{profile}-") as temp:
        target = Path(temp) / "project"
        result = subprocess.run(
            [
                BASH,
                str(ROOT / "bootstrap.sh"),
                "--profile",
                profile,
                str(target),
                "Smoke & Project",
                f"smoke-{profile}",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            fail(f"{profile} smoke bootstrap failed: {(result.stdout + result.stderr)[-5000:]}")
            return
        state = json.loads(
            (target / ".agent/bootstrap-profile.json").read_text(encoding="utf-8")
        )
        if state.get("resolved_profile") != expected:
            fail(f"{profile} smoke resolved to {state.get('resolved_profile')!r}")

        unresolved: list[str] = []
        for path in target.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "{{" in text:
                unresolved.append(str(path.relative_to(target)))
        if unresolved:
            fail(f"{profile} smoke has unresolved placeholders: {unresolved}")

        runtime_paths = (".codex", ".claude", ".opencode", "opencode.json", ".mcp.json")
        if profile == "core":
            for relative in runtime_paths:
                if (target / relative).exists():
                    fail(f"core smoke contains unselected path {relative}")
        if expected == "multi-runtime":
            for relative in runtime_paths:
                if not (target / relative).exists():
                    fail(f"multi-runtime smoke missing {relative}")
        if not unresolved:
            ok(f"{profile} smoke scaffold")


def main() -> int:
    print(f"==> Publication validation: {ROOT}")
    for relative in REQUIRED_FILES:
        require_file(relative)
    for relative in FORBIDDEN_PATHS:
        require_absent(relative)

    for relative, line in (
        (".gitignore", "archive/"),
        (".gitignore", "node_modules/"),
        (".gitignore", ".env"),
        ("template/project.gitignore", ".agent/active-work-block.json"),
        ("template/project.gitignore", ".agent/project-config.md"),
        ("template/project.gitignore", "memory_bank/"),
        ("template/project.gitignore", ".claude/agent-memory/"),
        ("template/project.gitignore", ".codex/config.toml"),
        ("template/project.gitignore", "node_modules/"),
        ("template/project.gitignore", ".env"),
    ):
        require_line(relative, line)
    forbid_line("template/project.gitignore", ".agent/")
    forbid_line("template/project.gitignore", ".codex/")

    validate_configs()

    bytecode = [
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.name == "__pycache__" or path.suffix == ".pyc"
        if "archive" not in path.parts and ".git" not in path.parts
    ]
    if bytecode:
        fail("generated Python bytecode/cache files found: " + ", ".join(bytecode))
    else:
        ok("no Python bytecode/cache files in public paths")

    scan_public_text()
    check_syntax()

    run_check([BASH, "scripts/test-sdd-contract.sh"], "SDLC contract tests")
    run_check([PYTHON, "scripts/test-bootstrap-profiles.py"], "bootstrap profile matrix")
    run_check([PYTHON, "scripts/test-runtime-conformance.py"], "runtime conformance")
    run_check([PYTHON, "scripts/test-integration-contracts.py"], "integration contracts")
    run_check(
        [PYTHON, "scripts/test-integration-admission-evidence.py"],
        "integration admission evidence",
    )
    run_check([PYTHON, "scripts/test-codex-adapter.py"], "Codex adapter contracts")
    run_check([PYTHON, "scripts/test-codex-hard-stops.py"], "Codex Hard Stop fixtures")
    run_check([PYTHON, "scripts/test-repair-lifecycle-contracts.py"], "repair lifecycle contracts")
    run_check([PYTHON, "scripts/test-ci-contract-router.py"], "CI contract router")
    run_check([BASH, "scripts/validate-governance.sh"], "governance validation")

    smoke_profile("core", "core")
    smoke_profile("multi-runtime", "multi-runtime")

    if FAILURES:
        print("==> Publication validation failed")
        return 1
    print("==> Publication validation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
