#!/usr/bin/env python3
"""Scaffold a generated project from a validated installation profile.

Installation profiles control copied runtime surfaces and skills only. They do
not grant Work Block authority, integrations, credentials, or side-effect
permissions.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Any

SCHEMA_VERSION = 1
ALLOWED_PLACEHOLDER_SUFFIXES = {
    ".md",
    ".json",
    ".sh",
    ".yaml",
    ".yml",
    ".toml",
    ".py",
}
GENERATED_REQUIRED_PATHS = {".agent/bootstrap-profile.json"}
SPECIAL_SOURCE_PATHS = {".gitignore": "template/project.gitignore"}


class BootstrapError(RuntimeError):
    """Raised for fail-closed bootstrap validation errors."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BootstrapError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BootstrapError(f"{path} must contain a JSON object")
    return value


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def require_unique(items: list[str], label: str) -> None:
    if len(items) != len(set(items)):
        raise BootstrapError(f"{label} contains duplicate values")


def validate_relative_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BootstrapError(f"{label} must be a non-empty string")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise BootstrapError(f"{label} must be a safe relative path: {value!r}")
    return value


def source_for_common_path(framework_root: Path, relative: str) -> Path | None:
    if relative in GENERATED_REQUIRED_PATHS:
        return None
    if relative in SPECIAL_SOURCE_PATHS:
        return framework_root / SPECIAL_SOURCE_PATHS[relative]
    template_source = framework_root / "template" / relative
    if template_source.exists():
        return template_source
    framework_source = framework_root / relative
    if framework_source.exists():
        return framework_source
    return framework_source


def validate_catalog(catalog: dict[str, Any], framework_root: Path) -> None:
    if catalog.get("schema_version") != SCHEMA_VERSION:
        raise BootstrapError(
            f"profile catalog requires schema_version={SCHEMA_VERSION}"
        )

    profiles = catalog.get("profiles")
    components = catalog.get("components")
    skill_sets = catalog.get("skill_sets")
    aliases = catalog.get("aliases")
    common_required = catalog.get("common_required_paths")
    default_profile = catalog.get("default_profile")

    if not isinstance(profiles, dict) or not profiles:
        raise BootstrapError("profile catalog must define profiles")
    if not isinstance(components, dict):
        raise BootstrapError("profile catalog components must be an object")
    if not isinstance(skill_sets, dict):
        raise BootstrapError("profile catalog skill_sets must be an object")
    if not isinstance(aliases, dict):
        raise BootstrapError("profile catalog aliases must be an object")
    if not isinstance(common_required, list):
        raise BootstrapError("common_required_paths must be an array")
    if default_profile not in profiles:
        raise BootstrapError("default_profile must reference a declared profile")

    common_paths = [
        validate_relative_path(path, f"common_required_paths[{index}]")
        for index, path in enumerate(common_required)
    ]
    require_unique(common_paths, "common_required_paths")

    template_root = framework_root / "template"
    if not template_root.is_dir():
        raise BootstrapError(f"missing template directory: {template_root}")
    for relative in common_paths:
        source = source_for_common_path(framework_root, relative)
        if source is not None and not source.exists():
            raise BootstrapError(f"common required source is missing: {relative}")

    for component_id, component in components.items():
        if not isinstance(component_id, str) or not component_id:
            raise BootstrapError("component IDs must be non-empty strings")
        if not isinstance(component, dict):
            raise BootstrapError(f"component {component_id!r} must be an object")
        if component.get("kind") not in {"runtime", "integration"}:
            raise BootstrapError(
                f"component {component_id!r} kind must be runtime or integration"
            )
        for field in ("paths", "required_paths", "skill_mirrors"):
            values = component.get(field)
            if not isinstance(values, list):
                raise BootstrapError(
                    f"component {component_id!r} {field} must be an array"
                )
            validated = [
                validate_relative_path(
                    value, f"component {component_id!r} {field}[{index}]"
                )
                for index, value in enumerate(values)
            ]
            require_unique(validated, f"component {component_id!r} {field}")

        for relative in component["paths"]:
            if not (template_root / relative).exists():
                raise BootstrapError(
                    f"component {component_id!r} source path is missing: {relative}"
                )
        for relative in component["required_paths"]:
            if not (template_root / relative).exists():
                raise BootstrapError(
                    f"component {component_id!r} required source is missing: {relative}"
                )

    for set_id, skills in skill_sets.items():
        if not isinstance(skills, list):
            raise BootstrapError(f"skill set {set_id!r} must be an array")
        require_unique(skills, f"skill set {set_id!r}")
        for skill in skills:
            skill_id = validate_relative_path(skill, f"skill set {set_id!r}")
            source = framework_root / "skills" / skill_id
            if not source.is_dir() or not (source / "SKILL.md").is_file():
                raise BootstrapError(
                    f"skill set {set_id!r} references missing skill {skill_id!r}"
                )

    for profile_id, profile in profiles.items():
        if not isinstance(profile, dict):
            raise BootstrapError(f"profile {profile_id!r} must be an object")
        if not isinstance(profile.get("description"), str) or not profile["description"].strip():
            raise BootstrapError(f"profile {profile_id!r} requires description")
        profile_components = profile.get("components")
        profile_skill_sets = profile.get("skill_sets")
        if not isinstance(profile_components, list):
            raise BootstrapError(f"profile {profile_id!r} components must be an array")
        if not isinstance(profile_skill_sets, list):
            raise BootstrapError(f"profile {profile_id!r} skill_sets must be an array")
        require_unique(profile_components, f"profile {profile_id!r} components")
        require_unique(profile_skill_sets, f"profile {profile_id!r} skill_sets")
        unknown_components = [item for item in profile_components if item not in components]
        unknown_skill_sets = [item for item in profile_skill_sets if item not in skill_sets]
        if unknown_components:
            raise BootstrapError(
                f"profile {profile_id!r} has unknown components: {unknown_components}"
            )
        if unknown_skill_sets:
            raise BootstrapError(
                f"profile {profile_id!r} has unknown skill sets: {unknown_skill_sets}"
            )

    for alias, target in aliases.items():
        if not isinstance(alias, str) or not alias:
            raise BootstrapError("profile aliases must use non-empty string keys")
        if target not in profiles:
            raise BootstrapError(
                f"profile alias {alias!r} targets unknown profile {target!r}"
            )
        if alias in profiles:
            raise BootstrapError(f"profile alias {alias!r} conflicts with a profile")


def resolve_profile(
    catalog: dict[str, Any], requested_profile: str
) -> tuple[str, dict[str, Any]]:
    aliases: dict[str, str] = catalog["aliases"]
    profiles: dict[str, dict[str, Any]] = catalog["profiles"]
    resolved = aliases.get(requested_profile, requested_profile)
    profile = profiles.get(resolved)
    if profile is None:
        choices = sorted([*profiles, *aliases])
        raise BootstrapError(
            f"unknown installation profile {requested_profile!r}; "
            f"choose one of: {', '.join(choices)}"
        )
    return resolved, profile


def resolve_profile_state(
    catalog: dict[str, Any], requested_profile: str
) -> dict[str, Any]:
    resolved_profile, profile = resolve_profile(catalog, requested_profile)
    components: dict[str, dict[str, Any]] = catalog["components"]
    skill_sets: dict[str, list[str]] = catalog["skill_sets"]
    selected_components: list[str] = list(profile["components"])

    skills: list[str] = []
    for set_id in profile["skill_sets"]:
        skills.extend(skill_sets[set_id])
    skills = unique(skills)

    runtimes: list[str] = ["generic"]
    integrations: list[str] = []
    skill_mirrors: list[str] = []
    required_paths: list[str] = list(catalog["common_required_paths"])

    for component_id in selected_components:
        component = components[component_id]
        required_paths.extend(component["required_paths"])
        skill_mirrors.extend(component["skill_mirrors"])
        if component["kind"] == "runtime":
            runtimes.append(component["runtime_id"])
        else:
            integrations.append(component["integration_id"])

    required_paths.extend(f".agent/skills/{skill}/SKILL.md" for skill in skills)
    for mirror in unique(skill_mirrors):
        required_paths.extend(f"{mirror}/{skill}/SKILL.md" for skill in skills)

    forbidden_paths: list[str] = []
    for component_id, component in components.items():
        if component_id not in selected_components:
            forbidden_paths.extend(component["paths"])

    return {
        "schema_version": SCHEMA_VERSION,
        "requested_profile": requested_profile,
        "resolved_profile": resolved_profile,
        "description": profile["description"],
        "components": selected_components,
        "runtimes": unique(runtimes),
        "integrations": unique(integrations),
        "skills": skills,
        "skill_mirrors": unique(skill_mirrors),
        "required_paths": unique(required_paths),
        "forbidden_paths": unique(forbidden_paths),
        "authority_note": (
            "Installation composition does not grant Work Block authority, "
            "integration admission, credentials, or side-effect permission."
        ),
    }


def ensure_target_is_empty(target: Path) -> None:
    if target.is_symlink():
        raise BootstrapError(f"target must not be a symbolic link: {target}")
    if target.exists() and not target.is_dir():
        raise BootstrapError(f"target exists and is not a directory: {target}")
    if target.is_dir() and any(target.iterdir()):
        raise BootstrapError(f"target exists and is not empty: {target}")


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def clean_skill_root(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for child in path.iterdir():
        if child.name == "README.md":
            continue
        remove_path(child)


def copy_skills(framework_root: Path, target: Path, state: dict[str, Any]) -> None:
    destinations = [target / ".agent/skills"]
    destinations.extend(target / mirror for mirror in state["skill_mirrors"])
    for destination in destinations:
        clean_skill_root(destination)

    for skill in state["skills"]:
        source = framework_root / "skills" / skill
        for destination in destinations:
            shutil.copytree(source, destination / skill)


def replace_placeholders(
    tree_root: Path,
    final_project_root: Path,
    project_name: str,
    project_slug: str,
) -> None:
    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROJECT_SLUG}}": project_slug,
        "{{PROJECT_ROOT}}": str(final_project_root),
        "{{SOURCE_DIRS}}": "src/*, app/*",
        "{{TECH_STACK}}": "to be defined",
    }
    for path in tree_root.rglob("*"):
        if not path.is_file() or path.suffix not in ALLOWED_PLACEHOLDER_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        updated = text
        for placeholder, value in replacements.items():
            updated = updated.replace(placeholder, value)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def make_executable(path: Path) -> None:
    if not path.is_file():
        return
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def build_project_tree(
    framework_root: Path,
    tree_root: Path,
    final_target: Path,
    project_name: str,
    project_slug: str,
    state: dict[str, Any],
    catalog: dict[str, Any],
) -> None:
    shutil.copytree(framework_root / "template", tree_root)
    project_gitignore = tree_root / "project.gitignore"
    if project_gitignore.is_file():
        project_gitignore.replace(tree_root / ".gitignore")

    for directory in ("governance", "runtimes", "integrations"):
        shutil.copytree(
            framework_root / directory,
            tree_root / directory,
            dirs_exist_ok=True,
        )

    selected = set(state["components"])
    for component_id, component in catalog["components"].items():
        if component_id in selected:
            continue
        for relative in component["paths"]:
            remove_path(tree_root / relative)

    copy_skills(framework_root, tree_root, state)

    state_path = tree_root / ".agent/bootstrap-profile.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    replace_placeholders(tree_root, final_target, project_name, project_slug)

    executable_patterns = (
        ".agent/hooks/*.py",
        ".claude/hooks/*.sh",
        ".claude/hooks/*.py",
        ".codex/hooks/*.py",
        "scripts/*.sh",
        "scripts/*.py",
    )
    for pattern in executable_patterns:
        for path in tree_root.glob(pattern):
            make_executable(path)

    health_check = tree_root / "scripts/bootstrap.sh"
    if health_check.is_file():
        subprocess.run(["bash", str(health_check)], cwd=tree_root, check=True)


def scaffold(
    framework_root: Path,
    target: Path,
    project_name: str,
    project_slug: str,
    state: dict[str, Any],
    catalog: dict[str, Any],
) -> None:
    ensure_target_is_empty(target)
    target.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(
        prefix=f".{target.name or 'project'}.bootstrap-",
        dir=target.parent,
    ) as temp:
        staging_root = Path(temp) / "project"
        build_project_tree(
            framework_root,
            staging_root,
            target,
            project_name,
            project_slug,
            state,
            catalog,
        )
        if target.exists():
            target.rmdir()
        staging_root.replace(target)


def list_profiles(catalog: dict[str, Any]) -> None:
    default_profile = catalog["default_profile"]
    aliases: dict[str, str] = catalog["aliases"]
    for profile_id, profile in catalog["profiles"].items():
        suffix = " (default)" if profile_id == default_profile else ""
        print(f"{profile_id}{suffix}: {profile['description']}")
    if aliases:
        print("aliases:")
        for alias, target in sorted(aliases.items()):
            print(f"  {alias} -> {target}")


def parse_args(catalog: dict[str, Any]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold an Agentic SDLC project installation profile."
    )
    parser.add_argument(
        "--profile",
        default=os.environ.get("AGENTIC_SDLC_PROFILE", catalog["default_profile"]),
        help="installation profile ID or alias",
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="list installation profiles and exit",
    )
    parser.add_argument("target_dir", nargs="?")
    parser.add_argument("project_name", nargs="?", default="My Project")
    parser.add_argument("project_slug", nargs="?")
    args = parser.parse_args()
    if not args.list_profiles and not args.target_dir:
        parser.error("target_dir is required unless --list-profiles is used")
    return args


def main() -> int:
    framework_root = Path(__file__).resolve().parents[1]
    catalog_path = framework_root / "bootstrap/profiles.json"
    try:
        catalog = load_json(catalog_path)
        validate_catalog(catalog, framework_root)
        args = parse_args(catalog)
        if args.list_profiles:
            list_profiles(catalog)
            return 0

        requested_profile = str(args.profile).strip()
        state = resolve_profile_state(catalog, requested_profile)
        target = Path(str(args.target_dir)).expanduser().resolve()
        project_name = str(args.project_name)
        project_slug = str(
            args.project_slug
            or "-".join(project_name.lower().split())
            or "project"
        )

        print(
            f"==> Scaffolding: {project_name} ({project_slug})\n"
            f"    Target: {target}\n"
            f"    Installation profile: {requested_profile} "
            f"-> {state['resolved_profile']}"
        )
        scaffold(
            framework_root,
            target,
            project_name,
            project_slug,
            state,
            catalog,
        )
    except (BootstrapError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"\n==> Done. Project scaffolded at {target}")
    print("\nNext steps:")
    print(f"  cd {target}")
    print("  git init && git add -A && git commit -m 'Initial scaffold from Agentic SDLC Framework'")
    print("\nThen:")
    print("  1. Read AGENTS.md and .agent/bootstrap-profile.json")
    print("  2. Select governance/runtime/integration profiles in the first Work Block")
    print("  3. Smoke-test installed runtime surfaces before relying on them")
    print("  4. Keep external integrations disabled until admitted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
