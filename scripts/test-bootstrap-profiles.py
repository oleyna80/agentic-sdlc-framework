#!/usr/bin/env python3
"""End-to-end fixtures for installation profile selection and exact scaffolds."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "bootstrap/bootstrap_project.py"
CATALOG = json.loads((ROOT / "bootstrap/profiles.json").read_text(encoding="utf-8"))
CANONICAL = {
    "core": "core",
    "codex": "codex",
    "claude-code": "claude-code",
    "opencode": "opencode",
    "multi-runtime": "multi-runtime",
    "minimal": "core",
    "full": "multi-runtime",
    "generic": "core",
}


def load_engine() -> Any:
    spec = importlib.util.spec_from_file_location("bootstrap_project", ENGINE)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to import bootstrap engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = load_engine()


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(ENGINE), *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        capture_output=True,
        text=True,
    )


def state(root: Path) -> dict:
    return json.loads(
        (root / ".agent/bootstrap-profile.json").read_text(encoding="utf-8")
    )


def skill_directories(root: Path, relative: str) -> set[str]:
    path = root / relative
    return {
        child.name
        for child in path.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }


def assert_no_placeholders(root: Path) -> None:
    suffixes = {".md", ".json", ".sh", ".yaml", ".yml", ".toml", ".py"}
    unresolved: list[str] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in suffixes:
            text = path.read_text(encoding="utf-8")
            if "{{PROJECT_" in text or "{{SOURCE_DIRS}}" in text or "{{TECH_STACK}}" in text:
                unresolved.append(str(path.relative_to(root)))
    if unresolved:
        raise AssertionError(f"unresolved placeholders: {unresolved}")


def is_ignored(root: Path, relative: str) -> bool:
    result = git(root, "check-ignore", "-q", "--no-index", "--", relative, check=False)
    if result.returncode not in {0, 1}:
        raise AssertionError(
            f"git check-ignore failed for {relative}: {result.stderr.strip()}"
        )
    return result.returncode == 0


def assert_git_boundaries(root: Path, profile_state: dict) -> None:
    git(root, "init", "-q")

    portable_common = (
        ".agent/bootstrap-profile.json",
        ".agent/ROSTER.md",
        ".agent/hooks/hard_stop_policy.py",
        ".agent/workflows/sdd-protocol.md",
        ".agent/skills/scoped-coder/SKILL.md",
    )
    for relative in portable_common:
        assert not is_ignored(root, relative), f"portable path is ignored: {relative}"

    operational_local = (
        ".agent/active-work-block.json",
        ".agent/critic-gate.md",
        ".agent/verification-gate.md",
        ".agent/project-config.md",
        "memory_bank/context.md",
        ".claude/agent-memory/verifier/MEMORY.md",
        ".codex/config.toml",
    )
    for relative in operational_local:
        assert is_ignored(root, relative), f"local path is not ignored: {relative}"

    selected = set(profile_state["components"])
    selected_portable = {
        "runtime:codex": ".codex/agents/coder.toml",
        "runtime:claude-code": ".claude/settings.json",
        "runtime:opencode": "opencode.json",
        "integration:mcp-config": ".mcp.json",
    }
    for component_id, relative in selected_portable.items():
        if component_id in selected:
            assert (root / relative).exists(), f"selected path missing: {relative}"
            assert not is_ignored(root, relative), f"selected path ignored: {relative}"


def assert_profile(requested: str, resolved: str, root: Path) -> None:
    profile_state = state(root)
    assert profile_state["requested_profile"] == requested
    assert profile_state["resolved_profile"] == resolved
    assert "does not grant" in profile_state["authority_note"]

    selected = set(profile_state["components"])
    for component_id, component in CATALOG["components"].items():
        for relative in component["paths"]:
            exists = (root / relative).exists()
            if component_id in selected and not exists:
                raise AssertionError(f"{requested}: missing selected path {relative}")
            if component_id not in selected and exists:
                raise AssertionError(f"{requested}: unexpected unselected path {relative}")

    expected_skills = set(profile_state["skills"])
    assert skill_directories(root, ".agent/skills") == expected_skills
    for mirror in profile_state["skill_mirrors"]:
        assert skill_directories(root, mirror) == expected_skills

    config = (root / ".agent/project-config.md").read_text(encoding="utf-8")
    assert f"INSTALLATION_PROFILE:** `{resolved}`" in config
    assert_no_placeholders(root)
    assert_git_boundaries(root, profile_state)


def profile_matrix() -> None:
    with tempfile.TemporaryDirectory(prefix="bootstrap-profiles-") as temp:
        base = Path(temp)
        for requested, resolved in CANONICAL.items():
            target = base / requested
            result = run(
                "--profile",
                requested,
                str(target),
                "Profile & Contract",
                f"profile-{requested}",
            )
            assert "Installation profile:" in result.stdout
            assert_profile(requested, resolved, target)


def default_profile_fixture() -> None:
    with tempfile.TemporaryDirectory(prefix="bootstrap-default-") as temp:
        target = Path(temp) / "default"
        run(str(target), "Default Profile", "default-profile")
        assert state(target)["resolved_profile"] == CATALOG["default_profile"]


def list_profiles_fixture() -> None:
    result = run("--list-profiles")
    for profile_id in CATALOG["profiles"]:
        assert profile_id in result.stdout
    for alias, target in CATALOG["aliases"].items():
        assert f"{alias} -> {target}" in result.stdout


def catalog_prevalidation_fixtures() -> None:
    missing_common = copy.deepcopy(CATALOG)
    missing_common["common_required_paths"].append("docs/definitely-missing.md")
    try:
        MODULE.validate_catalog(missing_common, ROOT)
    except MODULE.BootstrapError as exc:
        assert "common required source is missing" in str(exc)
    else:
        raise AssertionError("missing common source did not fail catalog validation")

    missing_component = copy.deepcopy(CATALOG)
    missing_component["components"]["runtime:codex"]["required_paths"].append(
        ".codex/agents/definitely-missing.toml"
    )
    try:
        MODULE.validate_catalog(missing_component, ROOT)
    except MODULE.BootstrapError as exc:
        assert "required source is missing" in str(exc)
    else:
        raise AssertionError("missing component source did not fail catalog validation")


def transactional_failure_fixtures() -> None:
    state_value = MODULE.resolve_profile_state(CATALOG, "core")
    original_copy_skills = MODULE.copy_skills

    def fail_copy_skills(*_args: object, **_kwargs: object) -> None:
        raise MODULE.BootstrapError("synthetic staged failure")

    MODULE.copy_skills = fail_copy_skills
    try:
        with tempfile.TemporaryDirectory(prefix="bootstrap-transaction-") as temp:
            base = Path(temp)
            absent = base / "absent"
            try:
                MODULE.scaffold(
                    ROOT,
                    absent,
                    "Atomic Project",
                    "atomic-project",
                    state_value,
                    CATALOG,
                )
            except MODULE.BootstrapError as exc:
                assert "synthetic staged failure" in str(exc)
            else:
                raise AssertionError("synthetic staged failure did not propagate")
            assert not absent.exists(), "failed bootstrap left a partial target"

            existing_empty = base / "existing-empty"
            existing_empty.mkdir()
            try:
                MODULE.scaffold(
                    ROOT,
                    existing_empty,
                    "Atomic Project",
                    "atomic-project",
                    state_value,
                    CATALOG,
                )
            except MODULE.BootstrapError:
                pass
            else:
                raise AssertionError("synthetic failure did not propagate for empty target")
            assert existing_empty.is_dir()
            assert not any(existing_empty.iterdir())
    finally:
        MODULE.copy_skills = original_copy_skills


def fail_closed_fixtures() -> None:
    with tempfile.TemporaryDirectory(prefix="bootstrap-fail-closed-") as temp:
        base = Path(temp)
        unknown = base / "unknown"
        result = run(
            "--profile",
            "does-not-exist",
            str(unknown),
            check=False,
        )
        assert result.returncode != 0
        assert "unknown installation profile" in result.stderr
        assert not unknown.exists()

        occupied = base / "occupied"
        occupied.mkdir()
        marker = occupied / "keep.txt"
        marker.write_text("keep\n", encoding="utf-8")
        result = run(
            "--profile",
            "core",
            str(occupied),
            check=False,
        )
        assert result.returncode != 0
        assert "not empty" in result.stderr
        assert marker.read_text(encoding="utf-8") == "keep\n"

        real = base / "real"
        real.mkdir()
        symlink = base / "symlink"
        symlink.symlink_to(real, target_is_directory=True)
        result = run(
            "--profile",
            "core",
            str(symlink),
            check=False,
        )
        assert result.returncode != 0
        assert "symbolic link" in result.stderr
        assert symlink.is_symlink()
        assert not any(real.iterdir())


def main() -> int:
    catalog_prevalidation_fixtures()
    transactional_failure_fixtures()
    profile_matrix()
    default_profile_fixture()
    list_profiles_fixture()
    fail_closed_fixtures()
    print("Bootstrap profile matrix: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
