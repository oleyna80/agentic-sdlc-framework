---
schema_version: 1
artifact_type: work_block
artifact_id: wb-004-integration-adapter-normalization
status: completed
owner_role: orchestrator
work_block_id: wb-004
created_at: 2026-07-25
last_verified: 2026-07-25
---

# WB-004 — Integration Adapter Normalization

## Objective

Normalize Claude Code plugins, MCP, OpenCode, and file-based handoff as explicit
runtime or integration adapters that implement the Governance Core without
creating provider-specific authority.

## Final Result

Completed.

- Claude Code generated defaults now expose only logical-role agents.
- The official Codex plugin for Claude Code is documented as the preferred
  optional Codex-from-Claude bridge.
- Codex MCP is an opt-in compatibility route; generated `.mcp.json` is empty.
- OpenCode has a project-scoped configuration, five logical-role subagents, and
  explicit fail-safe permissions.
- File handoff uses a runtime-neutral task/result envelope; the current Claude
  runner is labelled as a compatibility transport.
- Shared machine state records integration approvals/admission evidence and
  independent Review, Verification, Drift, and closeout state.
- Claude Code and Codex use shared provider-neutral consequential-action policy.
- Integration admission, permission, data/secret, evidence, recovery, and
  disable requirements are machine-testable.
- Generated projects receive normalized adapters without credentials or
  automatically enabled plugins, MCP servers, external runtimes, watchers, or
  services.

## Scope Delivered

- `integrations/**`
- `runtimes/claude-code/**`
- `runtimes/opencode/**`
- `runtimes/codex/**` synchronization
- `docs/mcp-tool-policy.md`
- `docs/profiles.md`
- `docs/quickstart-minimal.md`
- `SETUP.md`
- `handoff/README.md`
- `handoff/templates/**`
- `template/.agent/**`
- `template/.claude/**`
- `template/.codex/**` wrappers/documentation
- `template/.mcp.json`
- `template/.opencode/**`
- `template/opencode.json`
- bootstrap, navigation, registries, CI, and publication validation

## Out of Scope Preserved

- production credentials or provider endpoints;
- automatic runtime/plugin/MCP installation or authentication;
- paid/live cross-runtime smoke requiring local accounts;
- removal of compatibility shims before migration evidence exists;
- profile-aware minimal installation and broader cross-runtime conformance,
  reserved for WB-005.

## Accepted Design Decisions

1. Runtime adapters execute logical roles; integrations connect runtimes,
   services, tools, or transports.
2. Generated projects default to `integration_profile: none`.
3. Preferred integration order is native capability, official integration,
   reviewed MCP, audited file handoff, manual exchange, then exceptional direct
   process invocation.
4. Provider/model/integration names do not become authority roles.
5. Permissions and hooks fail safe but are not represented as OS isolation.
6. File handoff is direction-neutral even while the current runner remains
   Claude-specific.
7. Capabilities stay unknown/unverified until evidence exists.
8. Direct external runtime CLI invocation requires an active gate, fresh Git
   baseline, approved integration ID, and concrete admission-evidence path.
9. Plugin/MCP/external runtime access never expands the bound role/write-set.

## Implemented Controls

### Integration Layer

- `integrations/README.md`
- official Claude Code Codex plugin adapter
- MCP exact-tool/admission adapter
- file-handoff transport adapter
- integration admission template

### Claude Code

- logical-role agents only;
- no default MCP/plugin permission;
- machine-readable source write gate;
- machine-readable assurance/closeout gate;
- shared Hard Stop policy;
- provider-specific gate scripts/Markdown reduced to compatibility views.

### OpenCode

- committed `opencode.json` instructions and permissions;
- Architect, Critic, Coder, Reviewer, and Verifier project subagents;
- secrets/external directories denied;
- edit/Bash/web/task/MCP require approval where applicable;
- commit/push/destructive commands denied;
- no public provider/model pin;
- empty plugin/MCP collections.

### Handoff

- portable runtime task/result envelope;
- Claude runner/template labelled compatibility implementation;
- existing atomic queue, scope audit, locks, timeout, recovery, environment, and
  concurrency controls retained and documented.

### Shared Machine State

- integration IDs and admission records;
- Review/Verification/Drift state, evidence, isolation, and skip reasons;
- closeout mode;
- shared provider-neutral consequential-action policy;
- direct runtime IDs `codex-cli`, `claude-code-cli`, and `opencode-cli`.

## Review Findings

Final review:

`docs/reports/reviews/pr-4-final-review.md`

Resolved high/medium findings:

- provider-named agents encoded as authority;
- automatically enabled/implied MCP integration;
- missing OpenCode executable baseline;
- Claude gates tied to provider-specific Markdown/GPT route;
- incomplete external runtime admission evidence;
- handoff tied to Codex-to-Claude topology;
- missing Work Block integration admission fields;
- unsafe placeholder replacement for `&`, paths, and replacement characters.

## Verification Evidence

Framework Contracts review run `211` passed on implementation head
`4da0fb7582aa75f3b1e971f1f0c60f16c6b1756a`.

Validated:

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-integration-contracts.py
python scripts/test-integration-admission-evidence.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

Also validated:

- JSON/YAML and OpenCode agent frontmatter;
- shared, Claude, and Codex hook syntax;
- inert MCP/plugin defaults;
- removed provider-agent absence;
- direct runtime admission and missing-evidence denial;
- Claude write scope and assurance gates;
- Codex write/Hard Stop regressions;
- character-safe placeholder replacement;
- disposable generated-project inventory and configuration.

## Residual Limitations

- hooks/permissions are guardrails, not kernel/OS isolation;
- OpenCode requires real target-environment smoke before higher-governance use;
- plugin, MCP, and live handoff smokes remain environment-dependent and were not
  run in CI;
- current file-handoff runner remains Claude-specific internally;
- direct runtime command detection is pattern-based and indirect launch paths
  require separate admission review;
- provider data/retention boundaries depend on local admitted configuration;
- WB-005 remains responsible for profile-aware bootstrap and broader
  cross-runtime conformance.

## Closeout State

- **Stage:** Close
- **Stage State:** completed
- **Write Gate:** closed for implementation
- **Critic Gate:** resolved through reviewed Work Block/design decisions
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Drift Gate:** READY
- **Closeout Mode:** success-closeout
- **Review Report:** `docs/reports/reviews/pr-4-final-review.md`
- **Follow-up:** WB-005 profile-aware bootstrap and cross-runtime conformance
