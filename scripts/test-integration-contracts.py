#!/usr/bin/env python3
"""Static and executable fixtures for runtime/integration adapter contracts."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "template"
DEFAULT_DEFINE_QUALITY = {
    "required": False,
    "status": "PENDING",
    "requirements_review": "",
    "traceability": "",
    "consistency_analysis": "",
}
READY_DEFINE_QUALITY = {
    "required": True,
    "status": "READY",
    "requirements_review": "docs/reports/requirements-quality.md",
    "traceability": "docs/reports/traceability.json",
    "consistency_analysis": "docs/reports/define-consistency.md",
}
GRAPH_ACTIVATION_TOKENS = ("repository-graph", "repository_graph", "graph-provider")


def fail(message: str) -> None:
    raise AssertionError(message)


def is_graph_activation(value: object) -> bool:
    return isinstance(value, str) and any(
        token in value.lower() for token in GRAPH_ACTIVATION_TOKENS
    )


def require(path: Path) -> None:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")


def load_json(path: Path) -> dict[str, Any]:
    require(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must parse to an object")
    return value


def frontmatter(path: Path) -> dict[str, Any]:
    require(path)
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        fail(f"{path.relative_to(ROOT)} has unterminated YAML frontmatter")
    value = yaml.safe_load(text[4:end])
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} frontmatter must be a mapping")
    return value


def static_contracts() -> None:
    for path in (
        ROOT / "governance/evaluation.md",
        ROOT / "integrations/README.md",
        ROOT / "integrations/claude-code-codex-plugin/README.md",
        ROOT / "integrations/mcp/README.md",
        ROOT / "integrations/file-handoff/README.md",
        ROOT / "handoff/templates/runtime-task-template.md",
        TEMPLATE / "docs/templates/integration-admission-template.md",
        TEMPLATE / "docs/templates/evaluation-plan-template.json",
        TEMPLATE / "docs/templates/evaluation-report-template.json",
        TEMPLATE / "docs/templates/trajectory-event-template.json",
        TEMPLATE / "scripts/validate-evaluation.py",
        TEMPLATE / ".agent/hooks/hard_stop_policy.py",
        TEMPLATE / ".claude/hooks/work_block_gate.py",
        TEMPLATE / ".claude/hooks/assurance_gate.py",
        TEMPLATE / "opencode.json",
        ROOT / "opencode.json",
        ROOT / "docs/specs/repository-graph-provider-contract.md",
        ROOT / "docs/architecture/decisions/2026-08-11-repository-graph-provider-boundary.md",
        ROOT / "docs/plans/wb-repository-graph-001-optional-local-provider.md",
        ROOT / "integrations/repository-graph/README.md",
        TEMPLATE / "docs/templates/repository-graph-opt-in-template.md",
    ):
        require(path)

    def normalized(path: Path) -> str:
        return " ".join(path.read_text(encoding="utf-8").lower().split())

    graph_boundary_paths = {
        "contract": ROOT / "docs/specs/repository-graph-provider-contract.md",
        "ADR": ROOT / "docs/architecture/decisions/2026-08-11-repository-graph-provider-boundary.md",
        "guide": ROOT / "integrations/repository-graph/README.md",
        "opt-in template": TEMPLATE / "docs/templates/repository-graph-opt-in-template.md",
    }
    graph_boundary_text = {label: normalized(path) for label, path in graph_boundary_paths.items()}
    required_clauses = {
        "contract": (
            "local, derived, rebuildable, and non-authoritative",
            "not published by default",
            "cannot grant authority, a write-set, an approval, an assurance verdict, or a canonical or durable-memory effect",
            "cannot be the sole basis for a change",
            "important findings require direct confirmation against canonical repository source",
            "does not install, configure, invoke, start, index, query, or admit a provider",
            "does not enable mcp, apis, hooks, runtime configuration, embeddings, uploads, credentials, or keys",
            ".git/info/exclude",
            "operator-managed global exclusion",
            "do not add a generic graph directory or committed ignore rule",
        ),
        "ADR": (
            "local, derived, rebuildable, non-authoritative, and not published by default",
            "cannot grant authority, a write-set, approval, assurance verdict, or canonical/durable-memory effect",
            "cannot be the sole basis for a change",
            "material findings require direct canonical repository-source confirmation",
            "owns no provider installation, configuration, process, index, query, mcp/api surface, hook, runtime configuration, embedding, upload, credential, or key",
            "never a committed generic graph ignore rule",
        ),
        "guide": (
            "local, derived, rebuildable, non-authoritative, and not published by default",
            "cannot grant authority, a write-set, approval, assurance verdict, canonical/durable-memory effect, or be the sole basis for a change",
            "confirm important findings directly against canonical repository source",
            "no provider is selected, configured, started, indexed, queried, or invoked by this framework",
            "installation/configuration, mcp/api access, hooks, runtime configuration, embeddings/uploads, credentials, and provider invocation are future, owner-approved project work",
            "do not add a generic graph directory or a committed ignore rule",
        ),
        "opt-in template": (
            "local, derived, rebuildable, non-authoritative, and not published by default",
            "grants no authority, write-set, approval, assurance verdict, canonical/durable-memory effect, and cannot be the sole basis for a change",
            "confirm important findings directly against canonical repository source",
            "does not select, install, configure, or invoke a provider",
            "do not record credentials, api keys, embeddings, uploads, or provider-local content here",
            "provider installation/configuration, indexing/querying, mcp/api, hooks, runtime configuration, and invocation require their own owner-approved scope",
        ),
    }
    for label, clauses in required_clauses.items():
        for clause in clauses:
            if clause not in graph_boundary_text[label]:
                fail(f"Repository Graph Provider {label} missing required boundary: {clause}")

    navigation_clauses = {
        ROOT / "integrations/README.md": (
            "unadmitted, provider-neutral optional local derived-state capability",
            "not an adapter installation or provider admission",
        ),
        ROOT / "README.md": (
            "no external integration is enabled by bootstrap",
        ),
        ROOT / "SETUP.md": (
            "docs/templates/repository-graph-opt-in-template.md",
        ),
        ROOT / "PROJECT_MAP.md": (
            "repository graph provider. it does not install, configure, or invoke a provider",
        ),
        TEMPLATE / "PROJECT_MAP.md": (
            "provider-neutral local derived state; unadmitted and uninstalled",
        ),
    }
    for path, clauses in navigation_clauses.items():
        text = normalized(path)
        for clause in clauses:
            if clause not in text:
                fail(f"Repository Graph Provider navigation missing boundary in {path.relative_to(ROOT)}: {clause}")

    root_registry = yaml.safe_load((ROOT / "FILE_REGISTRY.yml").read_text(encoding="utf-8"))
    template_registry = yaml.safe_load((TEMPLATE / "FILE_REGISTRY.yml").read_text(encoding="utf-8"))
    for label, registry in (("root", root_registry), ("template", template_registry)):
        entry = registry.get("entries", {}).get("integrations/repository-graph/README.md", {})
        if entry.get("role") != "optional_provider_neutral_repository_graph_capability_boundary":
            fail(f"Repository Graph Provider {label} registry role drifted")
        if entry.get("status") != "normative":
            fail(f"Repository Graph Provider {label} registry must be normative, not an adapter")
        if entry.get("authority") != "none_without_separate_owner_approved_admission":
            fail(f"Repository Graph Provider {label} registry authority boundary drifted")

    all_boundary_text = " ".join(graph_boundary_text.values())
    for forbidden in (
        "gitnexus",
        "sourcegraph",
        "codescene",
        "npm install",
        "pip install",
        "--index-only",
        "mcpservers",
        "api_key",
        "default provider",
    ):
        if forbidden in all_boundary_text:
            fail(f"Repository Graph Provider boundary must not prescribe: {forbidden}")

    catalog = load_json(ROOT / "bootstrap/profiles.json")
    graph_documentation_paths = {
        "integrations/repository-graph/README.md",
        "docs/templates/repository-graph-opt-in-template.md",
    }
    common_required_paths = set(catalog.get("common_required_paths") or [])
    if not graph_documentation_paths.issubset(common_required_paths):
        fail("Repository Graph Provider documentation must be required for every bootstrap profile")
    for component_id, component in (catalog.get("components") or {}).items():
        if is_graph_activation(component_id) or is_graph_activation(component.get("integration_id")):
            fail(f"Repository Graph Provider must not declare activation component {component_id}")
        component_paths = set(component.get("paths") or []) | set(component.get("required_paths") or [])
        if graph_documentation_paths.intersection(component_paths):
            fail(f"Repository Graph Provider documentation must not activate component {component_id}")
    for profile_id, profile_definition in (catalog.get("profiles") or {}).items():
        for component_id in profile_definition.get("components") or []:
            if is_graph_activation(component_id):
                fail(f"Repository Graph Provider must not activate component in profile {profile_id}")

    generic_graph_ignore_entries = {
        "graph/",
        "graphs/",
        ".graph/",
        ".repository-graph/",
        "repository-graph/",
        ".repository_graph/",
        "repository_graph/",
    }
    for path in (ROOT / ".gitignore", TEMPLATE / "project.gitignore"):
        entries = {
            line.strip().lower()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        prohibited = entries.intersection(generic_graph_ignore_entries)
        if prohibited:
            fail(f"Repository Graph Provider must not add generic committed ignore entries in {path.relative_to(ROOT)}: {sorted(prohibited)}")

    work_block = ROOT / "docs/plans/wb-repository-graph-001-optional-local-provider.md"
    work_block_data = frontmatter(work_block)
    if work_block_data.get("status") != "completed":
        fail("Repository Graph Provider Work Block must be completed at Close")
    if work_block_data.get("base_revision") != "13c9f8fbb1659db8224cc0173d9e811abcf790af":
        fail("Repository Graph Provider Work Block base revision drifted")
    work_block_text = " ".join(work_block.read_text(encoding="utf-8").split())
    for required in (
        "APPROVE_WITH_CHANGES",
        "Review / Verification / Drift",
        "no provider evaluation",
        "provider installation/configuration/index/query",
        "Repository Graph Evaluation Brief.md",
    ):
        if required not in work_block_text:
            fail(f"Repository Graph Provider Work Block missing: {required}")

    graph_work_block = "docs/plans/wb-repository-graph-001-optional-local-provider.md"
    graph_closeout = "docs/reports/closeout/wb-repository-graph-001-optional-local-provider.md"
    migration_state = root_registry.get("migration_state", {})
    if migration_state.get("active_work_block") is not None:
        fail("Repository Graph Provider Close must leave no active Work Block")
    if graph_work_block not in migration_state.get("completed_work_blocks", []):
        fail("Repository Graph Provider Work Block missing from completed release state")
    closeout = ROOT / graph_closeout
    require(closeout)
    if frontmatter(closeout).get("status") != "approved":
        fail("Repository Graph Provider Closeout must remain approved")


def repository_graph_bootstrap_fixture() -> None:
    """Every profile receives docs only; this fixture never invokes a provider."""
    catalog = load_json(ROOT / "bootstrap/profiles.json")
    profiles = sorted(set(catalog["profiles"]) | set(catalog["aliases"]))
    engine = ROOT / "bootstrap/bootstrap_project.py"
    with tempfile.TemporaryDirectory(prefix="repository-graph-bootstrap-") as temp:
        base = Path(temp)
        for profile in profiles:
            target = base / profile
            result = subprocess.run(
                [sys.executable, str(engine), "--profile", profile, str(target), "Graph Fixture", profile],
                cwd=ROOT,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            if result.returncode:
                fail(f"Repository Graph Provider bootstrap failed for {profile}: {result.stderr.strip()}")
            for relative in (
                "docs/templates/repository-graph-opt-in-template.md",
                "integrations/repository-graph/README.md",
                "PROJECT_MAP.md",
                "FILE_REGISTRY.yml",
            ):
                require(target / relative)
            state = load_json(target / ".agent/bootstrap-profile.json")
            required_paths = set(state.get("required_paths") or [])
            for field in ("components", "integrations"):
                activated = [
                    value for value in (state.get(field) or []) if is_graph_activation(value)
                ]
                if activated:
                    fail(f"Repository Graph Provider must not activate {field} for {profile}: {activated}")
            for relative in (
                "docs/templates/repository-graph-opt-in-template.md",
                "integrations/repository-graph/README.md",
            ):
                if relative not in required_paths:
                    fail(f"Repository Graph Provider documentation missing from required_paths for {profile}: {relative}")
                documentation = target / relative
                contents = documentation.read_bytes()
                documentation.unlink()
                validation = subprocess.run(
                    [sys.executable, "scripts/validate-installation-profile.py", "."],
                    cwd=target,
                    capture_output=True,
                    text=True,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                if validation.returncode == 0 or relative not in validation.stderr:
                    fail(f"Repository Graph Provider validator did not detect missing required path for {profile}: {relative}")
                documentation.write_bytes(contents)
            opt_in = " ".join(
                (target / "docs/templates/repository-graph-opt-in-template.md")
                .read_text(encoding="utf-8")
                .split()
            )
            if "This template does not select, install, configure, or invoke a provider." not in opt_in:
                fail(f"Repository Graph Provider opt-in template drifted for {profile}")

    for role in ("architect", "critic", "coder", "reviewer", "verifier"):
        require(ROOT / f".opencode/agents/{role}.md")

    claude = load_json(TEMPLATE / ".claude/settings.json")
    present = {"enabledMcpjsonServers", "permissions", "autoMode"}.intersection(claude)
    if present:
        fail(f"Claude settings pre-enable external state: {sorted(present)}")
    expected_agents = {
        "solution-architect",
        "critic",
        "reviewer",
        "scoped-coder",
        "verifier",
    }
    if set((claude.get("agents") or {}).keys()) != expected_agents:
        fail("Claude logical agent set mismatch")
    serialized = json.dumps(claude, sort_keys=True).lower()
    for stale in ("gpt-critic", "gpt-verifier", "codex-reviewer", "mcp__codex"):
        if stale in serialized:
            fail(f"Claude settings retain provider-specific default: {stale}")
    hook_commands = json.dumps(claude.get("hooks") or {})
    for expected in (
        ".agent/hooks/hard_stop_policy.py",
        ".claude/hooks/work_block_gate.py",
        ".claude/hooks/assurance_gate.py",
    ):
        if expected not in hook_commands:
            fail(f"Claude settings missing hook: {expected}")

    if load_json(TEMPLATE / ".mcp.json") != {"mcpServers": {}}:
        fail("generated .mcp.json must be an empty opt-in registry")

    opencode = load_json(TEMPLATE / "opencode.json")
    if opencode.get("mcp") != {} or opencode.get("plugin") != []:
        fail("OpenCode must not enable MCP servers or plugins by default")
    permissions = opencode.get("permission")
    if not isinstance(permissions, dict):
        fail("OpenCode permission object missing")
    if permissions.get("external_directory") != "deny":
        fail("OpenCode external_directory must be denied")
    if permissions.get("edit") != "ask":
        fail("OpenCode project edit permission must require ask")
    project_read = permissions.get("read")
    if not isinstance(project_read, dict):
        fail("OpenCode project read permission map missing")
    for pattern, expected in {
        ".env": "deny",
        ".env.*": "deny",
        ".env.example": "allow",
        "secrets/**": "deny",
        "credentials/**": "deny",
        "*.pem": "deny",
        "*.key": "deny",
    }.items():
        if project_read.get(pattern) != expected:
            fail(f"OpenCode project read permission must set {pattern!r} to {expected!r}")
    if permissions.get("question") != "ask":
        fail("OpenCode question permission must require ask")
    if permissions.get("doom_loop") != "ask":
        fail("OpenCode doom_loop permission must require ask")
    if permissions.get("todowrite") != "ask":
        fail("OpenCode todowrite permission must require ask")
    if permissions.get("lsp") != "ask":
        fail("OpenCode lsp permission must require ask")
    if permissions.get("list") != "allow":
        fail("OpenCode list permission must be allow")
    if permissions.get("mcp_*") != "ask":
        fail("OpenCode MCP tools must require ask")
    bash = permissions.get("bash")
    if not isinstance(bash, dict):
        fail("OpenCode Bash permission map missing")
    if bash.get("git commit*") != "allow":
        fail("OpenCode normal local commit must be allowed")
    if bash.get("git push*") != "ask":
        fail("OpenCode push must require a runtime prompt, not SSH authorization")
    for pattern in ("git reset --hard*", "git clean*", "rm *"):
        if bash.get(pattern) != "deny":
            fail(f"OpenCode Bash permission must deny {pattern!r}")
    task_perm = permissions.get("task")
    if not isinstance(task_perm, dict) or task_perm.get("*") != "ask":
        fail("OpenCode task permission must be a glob map with *: ask")
    skill_perm = permissions.get("skill")
    if not isinstance(skill_perm, dict) or skill_perm.get("*") != "allow":
        fail("OpenCode skill permission must be a glob map with *: allow")
    if skill_perm.get("internal-*") != "deny":
        fail("OpenCode skill permission must deny internal-*")
    if list(skill_perm) != ["*", "internal-*"]:
        fail("OpenCode skill deny rule must follow the catch-all")
    if opencode.get("model") or opencode.get("provider"):
        fail("public OpenCode baseline must not pin provider/model routing")
    if opencode.get("default_agent") != "build":
        fail("OpenCode default_agent must be build")
    if opencode.get("subagent_depth") != 1:
        fail("OpenCode subagent_depth must be 1")
    if opencode.get("share") != "manual":
        fail("OpenCode share must be manual")
    if opencode.get("snapshot") is not True:
        fail("OpenCode snapshot must be enabled")
    for forbidden in (
        "auth",
        "enabled_providers",
        "disabled_providers",
        "experimental",
        "model",
        "provider",
        "server",
        "tools",
    ):
        if forbidden in opencode:
            fail(f"OpenCode baseline must not configure {forbidden}")

    bridge_skill_paths = (
        ".opencode/skills/critic-review/SKILL.md",
        ".opencode/skills/reviewer/SKILL.md",
        ".opencode/skills/scoped-coder/SKILL.md",
        ".opencode/skills/ssot-sync-closeout/SKILL.md",
        ".opencode/skills/subagent-mission-brief/SKILL.md",
        ".opencode/skills/task-decomposition/SKILL.md",
        ".opencode/skills/verifier/SKILL.md",
    )
    root_opencode = load_json(ROOT / "opencode.json")
    template_skill_paths = (opencode.get("skills") or {}).get("paths")
    root_skill_paths = (root_opencode.get("skills") or {}).get("paths")
    if template_skill_paths != ["skills"] or root_skill_paths != template_skill_paths:
        fail("root/template OpenCode skills.paths must have exact historical parity")
    for relative in bridge_skill_paths:
        root_bridge = ROOT / relative
        require(root_bridge)

    for role in ("architect", "critic", "coder", "reviewer", "verifier"):
        data = frontmatter(TEMPLATE / f".opencode/agents/{role}.md")
        if data.get("mode") != "subagent":
            fail(f"OpenCode {role} must use mode: subagent")
        role_permissions = data.get("permission")
        if not isinstance(role_permissions, dict):
            fail(f"OpenCode {role} permission map missing")
        expected_edit = "ask" if role == "coder" else "deny"
        if role_permissions.get("edit") != expected_edit:
            fail(f"OpenCode {role} edit permission must be {expected_edit}")
        role_read = role_permissions.get("read")
        if not isinstance(role_read, dict):
            fail(f"OpenCode {role} read permission map missing")
        for pattern, expected in {
            ".env": "deny",
            ".env.*": "deny",
            ".env.example": "allow",
            "secrets/**": "deny",
            "credentials/**": "deny",
            "*.pem": "deny",
            "*.key": "deny",
        }.items():
            if role_read.get(pattern) != expected:
                fail(
                    f"OpenCode {role} read permission must set {pattern!r} to {expected!r}"
                )
        role_bash = role_permissions.get("bash")
        if not isinstance(role_bash, dict):
            fail(f"OpenCode {role} Bash permission map missing")
        expected_commit = "allow" if role == "coder" else "deny"
        expected_push = "ask" if role == "coder" else "deny"
        if role_bash.get("git commit*") != expected_commit:
            fail(f"OpenCode {role} git commit permission must be {expected_commit}")
        if role_bash.get("git push*") != expected_push:
            fail(f"OpenCode {role} git push permission must be {expected_push}")
        for pattern in ("git reset --hard*", "git clean*", "rm *"):
            if role_bash.get(pattern) != "deny":
                fail(f"OpenCode {role} Bash permission must deny {pattern!r}")
        if role_permissions.get("task") != "deny":
            fail(f"OpenCode {role} nested task delegation must be denied")
        if role_permissions.get("mcp_*") != "ask":
            fail(f"OpenCode {role} MCP tools must require ask")
        skill_permissions = role_permissions.get("skill")
        if not isinstance(skill_permissions, dict):
            fail(f"OpenCode {role} skill permission map missing")
        if list(skill_permissions) != ["*", "internal-*"]:
            fail(f"OpenCode {role} skill deny rule must follow the catch-all")
        if skill_permissions.get("*") != "allow" or skill_permissions.get("internal-*") != "deny":
            fail(
                f"OpenCode {role} skill permissions must allow public and deny internal skills"
            )
        if role_permissions.get("external_directory") != "deny":
            fail(f"OpenCode {role} external_directory must be denied")
        if data.get("model"):
            fail(f"OpenCode {role} must not pin a public model")
        body = (TEMPLATE / f".opencode/agents/{role}.md").read_text(encoding="utf-8")
        if "tools:" in body or "maxSteps" in body:
            fail(f"OpenCode {role} uses deprecated agent configuration")

    for relative in (
        "opencode.json",
        ".opencode/agents/architect.md",
        ".opencode/agents/critic.md",
        ".opencode/agents/coder.md",
        ".opencode/agents/reviewer.md",
        ".opencode/agents/verifier.md",
    ):
        if (ROOT / relative).read_bytes() != (TEMPLATE / relative).read_bytes():
            fail(f"project OpenCode surface drifted from template: {relative}")

    for path in (
        TEMPLATE / ".claude/agents/gpt-critic.md",
        TEMPLATE / ".claude/agents/gpt-verifier.md",
        TEMPLATE / ".claude/agents/codex-reviewer.md",
        TEMPLATE / ".claude/agent-memory/gpt-critic/MEMORY.md",
        TEMPLATE / ".claude/agent-memory/gpt-verifier/MEMORY.md",
        TEMPLATE / ".claude/agent-memory/codex-reviewer/MEMORY.md",
    ):
        if path.exists():
            fail(f"provider-named compatibility path remains: {path.relative_to(ROOT)}")

    gate = load_json(TEMPLATE / ".agent/active-work-block.json")
    if gate.get("schema_version") != 4:
        fail("active Work Block schema_version must be 4")
    if gate.get("authority_mode") != "github_capability":
        fail("active Work Block authority_mode must be github_capability")
    if gate.get("governance_profile") != "Controlled":
        fail("generated Work Block default profile must remain Controlled")
    if gate.get("define_quality") != DEFAULT_DEFINE_QUALITY:
        fail("generated Work Block must contain canonical Define-quality default")
    if "authorization" in gate or "hard_stop_approvals" in gate:
        fail("legacy signed authority fields must be absent from schema v4")
    if gate.get("integrations") != {"approved": [], "admission_records": []}:
        fail("generated integration approvals must start empty")
    assurance = gate.get("assurance")
    if not isinstance(assurance, dict) or set(assurance) != {
        "review",
        "verification",
        "evaluation",
        "drift",
    }:
        fail("active Work Block assurance functions missing")
    evaluation = assurance["evaluation"]
    if evaluation.get("required") is not False:
        fail("generated evaluation assurance must be optional by default")
    if evaluation.get("status") != "PENDING" or evaluation.get("verdict") != "PENDING":
        fail("generated evaluation assurance must start PENDING")
    if gate.get("closeout_mode") != "pending":
        fail("generated closeout_mode must start pending")

    claude_guard = (TEMPLATE / ".claude/hooks/work_block_gate.py").read_text(encoding="utf-8")
    for marker in (
        "validate_define_quality",
        "validate_governance_profile",
        "VALID_GOVERNANCE_PROFILES",
        "FORMAL_DEFINE_PROFILES",
        "requirements_review",
        "traceability",
        "consistency_analysis",
    ):
        if marker not in claude_guard:
            fail(f"Claude Work Block guard missing Define-quality marker: {marker}")

    claude_entry = (TEMPLATE / "CLAUDE.md").read_text(encoding="utf-8").lower()
    for stale in ("gpt-critic", "gpt-verifier", "codex-reviewer"):
        if stale in claude_entry:
            fail(f"CLAUDE.md retains provider-authoritative agent: {stale}")

    handoff = frontmatter(ROOT / "handoff/templates/runtime-task-template.md")
    for key in (
        "task_id",
        "work_block_id",
        "from_runtime",
        "to_runtime",
        "logical_function",
        "source_revision",
        "authority",
        "allowed_scope",
        "forbidden_scope",
    ):
        if key not in handoff:
            fail(f"runtime task envelope missing {key}")


def run_script(path: Path, cwd: Path, payload: dict[str, Any]) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=cwd,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )
    if result.returncode:
        fail(f"{path.name} crashed: {result.stderr}")
    output = result.stdout.strip()
    if not output:
        return False, ""
    data = json.loads(output)
    specific = data.get("hookSpecificOutput") or {}
    reason = str(data.get("reason") or specific.get("permissionDecisionReason") or "")
    denied = data.get("decision") == "block" or specific.get("permissionDecision") == "deny"
    return bool(denied), reason


def assert_denied(label: str, value: tuple[bool, str], contains: str) -> None:
    denied, reason = value
    if not denied or contains.lower() not in reason.lower():
        fail(f"{label}: expected denial containing {contains!r}, got {reason!r}")


def assert_allowed(label: str, value: tuple[bool, str]) -> None:
    denied, reason = value
    if denied:
        fail(f"{label}: unexpectedly denied: {reason}")


def event(repo: Path, tool: str, **tool_input: str) -> dict[str, Any]:
    return {
        "cwd": str(repo),
        "hook_event_name": "PreToolUse",
        "tool_name": tool,
        "tool_input": tool_input,
        "session_id": "fixture-session",
    }


def write_gate(
    repo: Path, *, ready: bool = True, profile: str = "Managed"
) -> dict[str, Any]:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    define_quality = dict(READY_DEFINE_QUALITY)
    if profile == "Controlled":
        define_quality = dict(DEFAULT_DEFINE_QUALITY)
    gate: dict[str, Any] = {
        "schema_version": 4,
        "authority_mode": "github_capability",
        "work_block_id": "wb-integration-fixture",
        "governance_profile": profile,
        "specification": {"path": "docs/specs/fixture.md", "revision": "v1"},
        "base_commit": head,
        "define_quality": define_quality,
        "write_gate": {
            "status": "READY" if ready else "BLOCKED",
            "opened_at": "fixture" if ready else None,
        },
        "critic": {
            "required": True,
            "status": "READY",
            "verdict": "APPROVE",
            "report": "docs/reports/critic.md",
            "isolation": "separate-session",
            "skip_reason": "",
        },
        "assurance": {
            "review": {
                "required": True,
                "status": "PENDING",
                "verdict": "PENDING",
                "report": "",
                "isolation": "unknown",
                "skip_reason": "",
            },
            "verification": {
                "required": True,
                "status": "PENDING",
                "verdict": "PENDING",
                "report": "",
                "isolation": "unknown",
                "skip_reason": "",
            },
            "evaluation": {
                "required": False,
                "status": "PENDING",
                "verdict": "PENDING",
                "plan": "",
                "report": "",
                "rubric_revision": "",
                "benchmark_revision": "",
                "isolation": "unknown",
                "skip_reason": "",
            },
            "drift": {
                "required": False,
                "status": "PENDING",
                "verdict": "PENDING",
                "report": "",
                "isolation": "unknown",
                "skip_reason": "",
            },
        },
        "closeout_mode": "pending",
        "integrations": {"approved": [], "admission_records": []},
        "write_set": ["src/**", "tests/**"],
        "coordination_write_set": [
            ".agent/active-work-block.json",
            ".agent/critic-gate.md",
            ".agent/verification-gate.md",
            ".codex/write-gate.md",
            "docs/plans/**",
            "docs/specs/**",
            "docs/tasklist/**",
            "docs/reports/**",
            "docs/architecture/drafts/**",
            "memory_bank/**",
        ],
        "external_hard_stops": [
            "protected_default_branch_mutation",
            "destructive",
            "live_infra",
            "live_data",
            "credentials",
            "client_communications",
            "irreversible_publish",
        ],
    }
    (repo / ".agent/active-work-block.json").write_text(
        json.dumps(gate, indent=2) + "\n", encoding="utf-8"
    )
    return gate


def persist(repo: Path, gate: dict[str, Any]) -> None:
    (repo / ".agent/active-work-block.json").write_text(
        json.dumps(gate, indent=2) + "\n", encoding="utf-8"
    )


def executable_fixtures() -> None:
    hard_stop = TEMPLATE / ".agent/hooks/hard_stop_policy.py"
    write_guard = TEMPLATE / ".claude/hooks/work_block_gate.py"
    assurance_guard = TEMPLATE / ".claude/hooks/assurance_gate.py"
    evaluation_validator = TEMPLATE / "scripts/validate-evaluation.py"

    with tempfile.TemporaryDirectory(prefix="integration-contracts-") as tmp:
        repo = Path(tmp)
        for path in (
            ".agent",
            "scripts",
            "src",
            "tests",
            "docs/specs",
            "docs/plans",
            "docs/reports",
        ):
            (repo / path).mkdir(parents=True, exist_ok=True)
        shutil.copy2(evaluation_validator, repo / "scripts/validate-evaluation.py")
        (repo / "AGENTS.md").write_text("# Fixture\n", encoding="utf-8")
        (repo / "src/app.py").write_text("value = 1\n", encoding="utf-8")
        (repo / "README.md").write_text("fixture\n", encoding="utf-8")
        (repo / "docs/specs/fixture.md").write_text("# Spec\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q", "-b", "feature"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.com"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=repo, check=True)
        (repo / ".agent/active-work-block.json").write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)

        gate = write_gate(repo, ready=True)
        assert_denied(
            "external Codex CLI without admission",
            run_script(hard_stop, repo, event(repo, "Bash", command="codex review")),
            "codex-cli",
        )
        gate["integrations"] = {
            "approved": ["codex-cli"],
            "admission_records": ["docs/reports/integrations/codex-cli.md"],
        }
        persist(repo, gate)
        assert_allowed(
            "admitted external Codex CLI",
            run_script(hard_stop, repo, event(repo, "Bash", command="codex review")),
        )

        gate["write_gate"]["status"] = "BLOCKED"
        gate["write_gate"]["opened_at"] = None
        persist(repo, gate)
        assert_allowed(
            "blocked coordination write",
            run_script(write_guard, repo, event(repo, "Write", file_path="docs/plans/wb.md")),
        )
        assert_denied(
            "blocked source write",
            run_script(write_guard, repo, event(repo, "Write", file_path="src/app.py")),
            "write_gate.status=READY",
        )

        gate["write_gate"]["status"] = "READY"
        gate["write_gate"]["opened_at"] = "fixture"
        persist(repo, gate)
        assert_allowed(
            "in-scope Claude source write",
            run_script(write_guard, repo, event(repo, "Edit", file_path="src/app.py")),
        )
        assert_denied(
            "out-of-scope Claude source write",
            run_script(write_guard, repo, event(repo, "Edit", file_path="README.md")),
            "outside approved scope",
        )

        gate = write_gate(repo, ready=True)
        gate.pop("governance_profile")
        persist(repo, gate)
        assert_denied(
            "Claude missing governance profile",
            run_script(write_guard, repo, event(repo, "Edit", file_path="src/app.py")),
            "governance_profile",
        )

        for label, invalid_profile in (
            ("Claude empty governance profile", ""),
            ("Claude whitespace governance profile", "   "),
            ("Claude unknown governance profile", "Manged"),
            ("Claude non-string governance profile", 42),
        ):
            gate = write_gate(repo, ready=True)
            gate["governance_profile"] = invalid_profile
            persist(repo, gate)
            assert_denied(
                label,
                run_script(write_guard, repo, event(repo, "Edit", file_path="src/app.py")),
                "governance_profile",
            )

        gate = write_gate(repo, ready=True, profile="Advisory")
        persist(repo, gate)
        assert_denied(
            "Claude Advisory source write",
            run_script(write_guard, repo, event(repo, "Edit", file_path="src/app.py")),
            "Advisory",
        )

        write_gate(repo, ready=True, profile="Controlled")
        assert_allowed(
            "Claude Controlled non-applicable Define-quality remains proportional",
            run_script(write_guard, repo, event(repo, "Edit", file_path="src/app.py")),
        )

        for profile in ("Managed", "Assured", "Distributed"):
            gate = write_gate(repo, ready=True, profile=profile)
            gate["define_quality"]["required"] = False
            persist(repo, gate)
            assert_denied(
                f"Claude {profile} required=false cannot bypass",
                run_script(write_guard, repo, event(repo, "Edit", file_path="src/app.py")),
                "required=false",
            )

        gate = write_gate(repo, ready=True)
        gate.pop("define_quality")
        persist(repo, gate)
        assert_denied(
            "Claude Managed missing Define-quality",
            run_script(write_guard, repo, event(repo, "Edit", file_path="src/app.py")),
            "define_quality",
        )

        gate = write_gate(repo, ready=True)
        gate["define_quality"]["status"] = "PENDING"
        persist(repo, gate)
        assert_denied(
            "Claude Managed Define-quality pending",
            run_script(write_guard, repo, event(repo, "Edit", file_path="src/app.py")),
            "status=READY",
        )

        gate = write_gate(repo, ready=True)
        gate["define_quality"]["consistency_analysis"] = "   "
        persist(repo, gate)
        assert_denied(
            "Claude blank Define-quality evidence",
            run_script(write_guard, repo, event(repo, "Edit", file_path="src/app.py")),
            "consistency_analysis",
        )

        gate = write_gate(repo, ready=True)
        for name in ("review", "verification"):
            (repo / f"docs/reports/{name}.md").write_text(
                f"# {name.title()}\n", encoding="utf-8"
            )
            gate["assurance"][name].update(
                {
                    "status": "READY",
                    "verdict": "READY",
                    "report": f"docs/reports/{name}.md",
                    "isolation": "separate-session",
                }
            )
        gate["assurance"]["evaluation"].update(
            {
                "status": "SKIPPED",
                "verdict": "UNVERIFIED",
                "skip_reason": "No non-deterministic output or trajectory requirement in fixture.",
            }
        )
        gate["assurance"]["drift"].update(
            {
                "status": "SKIPPED",
                "verdict": "PENDING",
                "skip_reason": "No behavior or contract change in fixture.",
            }
        )
        gate["closeout_mode"] = "success-closeout"
        persist(repo, gate)
        assert_allowed(
            "evidence-backed success closeout",
            run_script(assurance_guard, repo, {"cwd": str(repo)}),
        )

        gate["assurance"]["evaluation"]["required"] = True
        persist(repo, gate)
        assert_denied(
            "required evaluation cannot be skipped",
            run_script(assurance_guard, repo, {"cwd": str(repo)}),
            "evaluation",
        )

        gate["assurance"]["evaluation"]["required"] = False
        gate["assurance"]["verification"]["verdict"] = "BLOCKED"
        persist(repo, gate)
        assert_denied(
            "blocked verification cannot success-closeout",
            run_script(assurance_guard, repo, {"cwd": str(repo)}),
            "Verification",
        )


def main() -> int:
    static_contracts()
    repository_graph_bootstrap_fixture()
    executable_fixtures()
    print("Integration adapter contracts and fixtures: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
