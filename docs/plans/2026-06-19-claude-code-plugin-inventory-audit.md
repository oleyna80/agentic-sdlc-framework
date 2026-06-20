# Work Block: Claude Code Plugin Inventory Audit

## Meta
- **Work Block ID:** wb-claude-code-plugin-inventory-audit
- **Date:** 2026-06-19
- **Owner:** Azur
- **Execution Mode:** autonomous within repository scope
- **Side-Effect Class:** public-repo documentation
- **DB Action Mode:** none
- **Verification Tier:** standard

## Objective

Classify installed and candidate Claude Code plugins against the framework's
authority, lifecycle, logging, provider, and data-boundary rules.

## Expected Final Result

Maintainers can distinguish plugins installed for this repository from
user-wide and foreign-project registry entries. Every relevant installed
plugin and generic SDLC candidate has an explicit keep, reject, quarantine, or
project-specific decision. The active baseline contains only compatible
plugins, no global or foreign-project state is modified, and publication
validation passes.

## Done Criteria
- [x] Current project installs and machine-wide registry entries are separated.
- [x] Installed plugins are classified against SDLC authority and hooks.
- [x] Relevant marketplace candidates are classified.
- [x] Baseline activation is changed only if evidence justifies it.
- [x] Repository checks pass.

## Scope

### In Scope
- `.claude/settings.json` framework baseline review.
- Local manifests, hooks, skills, agents, commands, and MCP declarations.
- Plugin policy and audit evidence.

### Out of Scope
- User-scope uninstall or activation.
- Changes to another project's plugin registry.
- Generated-project defaults.
- Live compatibility tests for quarantined plugins.
- Commit and push.

## Write-Set

```text
framework/knowledge/claude-code-plugins.md
docs/plans/2026-06-19-claude-code-plugin-inventory-audit.md
```

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Aggregated CLI output is mistaken for current-project state | Filter the installation registry by both scope and project path. |
| A useful plugin silently replaces framework lifecycle authority | Reject baseline plugins with competing workflows or proactive writes. |
| Hooks duplicate or reorder critic and verification gates | Quarantine hook-bearing plugins until an isolated runtime test. |
| Cleanup damages other projects | Do not modify user or foreign-project scope in this Work Block. |
| Optional integrations expand data or credential boundaries | Require a task-specific profile and explicit Owner approval. |

## Subagent Strategy

- **Classification:** single-agent audit with read-only review stage.
- **Claude Code team:** not used; Claude Code is the audited runtime.
- **Critic:** policy diff review after implementation.

## Verification Plan

- Parse project settings and filter the local plugin registry by project path.
- Confirm the exact two-plugin allowlist remains unchanged.
- Run `git diff --check`.
- Run `bash scripts/validate-publication.sh`.

## Execution Log

| Time | Stage | Action / Decision | Evidence | Status |
|---|---|---|---|---|
| 2026-06-19T17:32:07Z | Plan | Confirmed clean repository and two project-scoped installs | git status; installed plugin registry | complete |
| 2026-06-19T17:32:07Z | Spec | Classified installed plugins and generic marketplace candidates | cached manifests, hooks, skills, agents, MCP declarations | complete |
| 2026-06-19T17:32:07Z | Implementation | Expanded plugin policy; retained two-plugin baseline | policy diff | complete |
| 2026-06-19T17:33:47Z | Review | Checked decisions against authority, lifecycle, hook, and data-boundary rules | read-only policy diff review | complete |
| 2026-06-19T17:33:47Z | Verification | Confirmed exact project allowlist and registry scope; ran publication validation | jq assertions; git diff --check; validate-publication.sh | complete |

## Result

The framework keeps `skill-creator` and `frontend-design` as its intentional
project baseline. No plugin was installed, removed, or enabled by this audit:
the remaining observed entries are user-scoped, foreign-project, quarantined,
or project-specific. Global cleanup remains a separate Owner-approved Work
Block. All planned repository checks passed.
