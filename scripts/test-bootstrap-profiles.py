#!/usr/bin/env python3
"""End-to-end fixtures for installation profile selection and exact scaffolds."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile

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


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(ENGINE), *args],
        cwd=ROOT,
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


def main() -> int:
    profile_matrix()
    default_profile_fixture()
    list_profiles_fixture()
    fail_closed_fixtures()
    print("Bootstrap profile matrix: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
