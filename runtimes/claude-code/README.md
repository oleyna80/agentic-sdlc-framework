# Claude Code Runtime Adapter

## Status

Implemented generated-project baseline for logical-role subagents, project hooks,
portable skills, and explicit opt-in integrations.

This adapter implements the Governance Core. It does not redefine authority,
source-of-truth order, external Hard Stops, lifecycle gates, or completion.

## Authority Boundary

Generated projects use active Work Block schema v3 with:

```text
authority_mode: github_capability
```

The active Work Block, role separation, write-set, and project-local hooks are
cooperative engineering guardrails. They are not a cryptographic or operating-
system security boundary.

Per-Work-Block SSH signing is retired from the normal development path. Claude
Code does not need an Owner private signing key, `ssh-keygen`, an
`allowed_signers` file, an authorization-bootstrap commit, or a detached `.sig`
merely to edit approved source, create a local commit, or push a normal feature
branch when the runtime credential permits it.

Consequential authority belongs outside the mutable project wherever practical:

- GitHub rulesets and protected branches;
- least-privilege agent credentials and Actions permissions;
- OS/user/container isolation;
- separately held production, VPS, database, and secret credentials.

Production/live infrastructure, direct live-data mutation, credential/secret
operations, destructive Git/filesystem operations, direct protected/default-
branch mutation, irreversible external publication, and real client-facing
communication require the separately Owner-controlled external capability.

## Logical Role Mapping

| Logical role | Claude Code implementation | Default authority |
|---|---|---|
| Orchestrator | Main Claude Code session | workflow and coordination artifacts |
| Architect | `.claude/agents/solution-architect.md` | read-only plus approved drafts |
| Critic | `.claude/agents/critic.md` | read-only |
| Coder | `.claude/agents/scoped-coder.md` | approved write-set only |
| Reviewer | `.claude/agents/reviewer.md` | read-only |
| Verifier | `.claude/agents/verifier.md` | read-only plus approved reports |

Names in `.claude/agents/` are runtime identifiers. The logical role and active
Work Block determine local process authority.

Provider-named agents such as `gpt-critic`, `gpt-verifier`, and
`codex-reviewer` are no longer part of the generated-project default. Cross-
runtime review is performed through an admitted integration and remains bound
to the normal Critic, Reviewer, or Verifier function.

## Installed Project Files

```text
CLAUDE.md
.claude/
├── settings.json
├── agents/
│   ├── solution-architect.md
│   ├── critic.md
│   ├── reviewer.md
│   ├── scoped-coder.md
│   └── verifier.md
├── hooks/
│   ├── assurance_gate.py
│   ├── critic-gate.sh
│   ├── hard-stop.sh
│   ├── typecheck.sh
│   ├── verification-gate.sh
│   └── work_block_gate.py
├── skills/
└── agent-memory/

.agent/hooks/
└── hard_stop_policy.py
```

`.mcp.json` is present but empty by default. No plugin, MCP server, external
runtime, credential, watcher, or service is installed or enabled automatically.

## Session Bootstrap

1. Read `CLAUDE.md`.
2. Read `AGENTS.md` and follow its progressive read set.
3. Identify the active Work Block and approved specification.
4. Record actual Claude Code capabilities, permission mode, hooks, integrations,
   and isolation.
5. Bind required logical functions to Claude Code agents or admitted external
   integrations.
6. Keep source writes blocked until Define and the required Critic function are resolved.
7. Open only the exact schema-v3 write-set needed for the Coder.

`CLAUDE.md` is a runtime entry point, not a second governance contract.

## Hooks

The generated baseline registers project hooks for:

- shared consequential Bash / external Hard Stop checks;
- Work Block/write-set checks for `Bash`, `Edit`, `MultiEdit`, and `Write`;
- staged-path validation before a local `git commit`;
- targeted post-edit type checks;
- Review/Verification/Evaluation/Drift closeout checks at Stop.

A Bash command must pass both applicable PreToolUse layers. The shared
`.agent/hooks/hard_stop_policy.py` rejects obvious consequential commands and
external-runtime calls without admission. `.claude/hooks/work_block_gate.py`
checks explicit mutation targets and staged commit paths against the active Work
Block. Complex mutating Bash that cannot be scoped safely fails closed.

Normal feature-branch `git push` is intentionally left to the shared Hard Stop
and external GitHub boundary. The shared guard rejects direct default-branch,
force/history-rewriting, branch-deletion, broad/mirror/prune, tag-publication,
and other configured consequential push forms.

Hooks are defense in depth, not OS-level isolation. They depend on the installed
Claude Code version, project trust, settings, shell environment, and event
payload. Review hook source and run safe fixtures after runtime updates.

If a hook is unavailable or cannot enforce the required boundary:

- label the capability degraded;
- use a more restrictive permission mode, separate worktree/runtime, or manual
  approval;
- keep consequential credentials outside the runtime;
- do not upgrade blocked or unverified evidence.

## Permissions

Default project settings do not pre-authorize MCP tools or external integrations.

Role agents further restrict tools in their frontmatter. The runtime's effective
permissions must be recorded because user, enterprise, CLI, and project settings
may combine or override one another.

A Claude Code approval prompt is not external Owner authority. Do not use it to
approve production deployment, live DB mutation, credential changes,
destructive operations, protected/default-branch mutation, or other external
Hard Stops.

## Skills and Memory

Portable skills are copied to `.claude/skills/` and `.agent/skills/`. Skills
provide procedures; they do not grant tool or write authority.

`.claude/agent-memory/` is runtime-local operational state. It may contain useful
patterns but is not normative. Promote durable, evidence-backed knowledge to
`docs/engineering-memory/` through closeout.

Do not store secrets, credentials, personal data, or hidden reasoning in agent
memory.

## Integrations

### Codex from Claude Code

Preferred route:

- `integrations/claude-code-codex-plugin/` — official Codex plugin.

Compatibility route:

- `integrations/mcp/` — reviewed Codex MCP configuration.

Recovery/transport route:

- `integrations/file-handoff/` — audited task/result files.

None is enabled by default. An integration must have an admission record and
must be bound to a logical function in the active Work Block. Admission does not
grant production, secret, live-data, destructive, or protected-branch authority.

### Other MCP and Plugins

Treat plugins, MCP tools, browser tools, issue trackers, and vendor CLIs as
integration adapters. Tool access does not expand the invoking role.

## Capability Snapshot

Start with observed values, not assumptions:

```yaml
runtime: claude-code
status: available
capabilities:
  project_instructions: observed
  custom_subagents: observed
  project_hooks: observed
  bash_work_set_guard: configured
  staged_commit_guard: configured
  per_agent_tool_policy: observed
  native_plan_mode: observed
  separate_child_sessions: observed
  plugins: unknown_until_installed
  mcp: unknown_until_configured
  worktrees: external_workflow
  os_isolation: false
  production_authority: unavailable_by_design
limitations:
  - same machine and checkout unless separately configured
  - user and enterprise settings may affect effective permissions
  - project hooks are cooperative guardrails, not an operating-system security boundary
```

Replace `observed` with evidence and version references in project state.

## Assurance Topology

For low-risk work, separate subagent passes may be sufficient. For stronger
independence:

- use a separate Claude Code session or worktree;
- use an admitted Codex/OpenCode integration;
- use a separate runtime, container, account, machine, or human review where the
  governance profile requires it.

A different model name alone does not establish independence.

Passing Review or Verification does not grant an external capability. A
verified deployable artifact still requires the applicable GitHub/OS/credential
boundary before production action.

## Validation

After bootstrap or runtime/plugin updates:

- parse `.claude/settings.json`;
- verify only logical-role agents are active by default;
- run harmless hook fixtures;
- confirm Bash mutations outside the Work Block write-set are denied;
- confirm staged out-of-scope commits are denied;
- confirm normal scoped source writes are allowed only while the local gate is READY;
- confirm configured destructive/default-branch/broad/tag pushes are denied by the shared guard;
- confirm `.mcp.json` is empty unless explicitly admitted;
- confirm no committed secret values;
- test one read-only Architect/Reviewer task;
- record runtime version and inspection gaps.

## Degraded Mode

When subagents or hooks are unavailable, preserve the lifecycle through separate
manual passes or sessions. Record actual authority and isolation. Keep external
Hard Stop capabilities outside the runtime and do not claim independent review
or executable enforcement that did not occur.

## References

- Claude Code documentation: <https://docs.anthropic.com/en/docs/claude-code/>
- Integration adapters: `integrations/`
