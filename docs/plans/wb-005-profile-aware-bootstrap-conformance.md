---
schema_version: 1
artifact_type: work_block
artifact_id: wb-005-profile-aware-bootstrap-conformance
status: in_progress
owner_role: orchestrator
work_block_id: wb-005
created_at: 2026-07-25
last_verified: 2026-07-25
---

# WB-005 — Profile-Aware Bootstrap and Cross-Runtime Conformance

## Objective

Make generated-project installation deliberately selectable without coupling
installation composition to governance authority. Add executable conformance
checks proving that Codex, Claude Code, OpenCode, and generic/sequential
adapters preserve the same logical-role, Work Block, assurance, and Hard Stop
contracts.

## Expected Final Result

- `bootstrap.sh` accepts an explicit installation profile while preserving the
  existing positional invocation.
- Installation profiles are manifest-driven, versioned, inspectable, and
  validated before copying files.
- Supported profiles are `core`, `codex`, `claude-code`, `opencode`, and
  `multi-runtime`, with `minimal` and `full` compatibility aliases.
- The default remains `multi-runtime` for backward compatibility.
- Generated projects contain `.agent/bootstrap-profile.json` recording the
  resolved profile, components, runtime surfaces, skills, and expected
  present/absent paths.
- Unselected runtime implementation surfaces are absent from a fresh scaffold.
- Governance Core, portable lifecycle, Work Block, assurance, and navigation
  remain present in every profile.
- Generated-project health checks are conditional on the resolved installation
  profile rather than assuming the maximum scaffold.
- Cross-runtime conformance fixtures verify logical roles, write authority,
  read-only assurance roles, shared Work Block usage, provider-neutral model
  posture, and safe integration defaults.
- CI bootstraps and validates every installation profile and both aliases.

## Scope

### In Scope

- `bootstrap.sh`
- `bootstrap/**`
- `template/scripts/bootstrap.sh`
- generated-project bootstrap profile state and validation
- runtime-profile and installation-profile documentation
- cross-runtime conformance tests
- CI, publication, navigation, registry, and Work Block closeout changes

### Out of Scope

- automatically installing runtime CLIs, plugins, MCP servers, credentials, or
  provider packages;
- changing Governance Core authority or lifecycle semantics;
- selecting concrete models or provider accounts;
- live paid-runtime smoke tests;
- converting the framework into a package manager;
- removing runtime adapter documentation from lean profiles.

## Design Decisions

1. **Installation composition is not governance.** A profile controls copied
   implementation surfaces and skills only. Work Block authority remains
   independent and fail-closed.
2. **Documentation stays portable.** Governance, runtime adapter documentation,
   integration adapter documentation, templates, and navigation remain available
   in every profile; executable runtime surfaces are selective.
3. **Default is backward compatible.** No `--profile` means `multi-runtime`,
   matching the current maximum scaffold.
4. **Profiles are data, not shell branches.** A versioned JSON catalog defines
   components, skill sets, aliases, and profile composition.
5. **Fresh scaffolds are exact.** Selected component paths must exist; unselected
   component paths must be absent. Later user additions are allowed but are not
   confused with bootstrap output.
6. **Conformance is semantic.** Tests compare logical role and permission
   contracts, not provider-specific file syntax alone.
7. **Safe integrations remain inert.** Profiles do not activate external tools,
   plugins, MCP servers, credentials, watchers, or services.
8. **Unknown profile IDs fail closed.** Bootstrap lists valid profiles and exits
   before mutating the target.

## Planned Installation Profiles

| Profile | Runtime implementation surfaces | Skill posture | Intended use |
|---|---|---|---|
| `core` | none; generic/sequential guidance only | portable core | smallest runtime-neutral project scaffold |
| `codex` | `.codex/` | core + Codex operational skills | Codex-primary projects |
| `claude-code` | `CLAUDE.md`, `.claude/` | core + Claude Code operational skills | Claude Code-primary projects |
| `opencode` | `opencode.json`, `.opencode/` | portable core | OpenCode-primary projects after smoke |
| `multi-runtime` | Codex + Claude Code + OpenCode + empty `.mcp.json` | complete existing baseline | compatibility/default and mixed-runtime evaluation |

Aliases:

- `minimal` → `core`
- `full` → `multi-runtime`

## Implementation Tasks

1. Add the profile catalog and bootstrap engine.
2. Replace shell-only scaffold composition with a thin backward-compatible shell
   wrapper around the Python engine.
3. Record resolved profile state in each generated project.
4. Add a generated-project installation-profile validator.
5. Make `template/scripts/bootstrap.sh` validate common and conditional paths.
6. Add profile matrix fixtures for exact fresh-scaffold contents.
7. Add cross-runtime semantic conformance fixtures.
8. Extend publication validation and Framework Contracts CI.
9. Update setup, quickstart, profiles, project maps, registries, and runtime docs.
10. Open a draft PR, resolve CI findings, run final review, and close the Work
    Block before merge.

## Assurance Plan

### Review

Check:

- profile selection never grants Work Block authority;
- default behavior remains compatible;
- aliases resolve deterministically;
- target mutation begins only after profile validation;
- unselected runtime surfaces are actually absent;
- selected runtime surfaces and skills are complete;
- generated health checks do not assume all runtimes;
- runtime conformance tests compare the same logical functions and boundaries;
- no integration is enabled automatically.

### Verification

Run in CI:

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-bootstrap-profiles.py
python scripts/test-runtime-conformance.py
python scripts/test-integration-contracts.py
python scripts/test-integration-admission-evidence.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

Bootstrap and inspect:

- `core`;
- `codex`;
- `claude-code`;
- `opencode`;
- `multi-runtime`;
- alias `minimal`;
- alias `full`.

## Risks

| Risk | Mitigation |
|---|---|
| Lean profile removes a required portable contract | Maintain an explicit common required-path contract and test every profile |
| Profile manifests drift from bootstrap behavior | One engine consumes the same catalog used by tests and generated validation |
| Existing users expect all runtime files | Preserve `multi-runtime` as default and `full` alias |
| Runtime syntaxes cannot be compared directly | Normalize semantic facts into a conformance matrix |
| Profile state becomes authority | State explicitly that it records installation composition only |
| Later user additions fail health checks | Generated validator requires selected paths and forbids only known unselected bootstrap surfaces |
| Python dependency surprises shell users | Python 3 is already required by the existing literal placeholder replacement path |

## Current State

- **Stage:** Define
- **Stage State:** in_progress
- **Write Gate:** READY for this branch and documented scope
- **Review Gate:** PENDING
- **Verification Verdict:** PENDING
- **Drift Gate:** PENDING
- **Closeout Mode:** pending
