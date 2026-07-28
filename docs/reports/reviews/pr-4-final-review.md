---
schema_version: 1
artifact_type: review_report
artifact_id: pr-4-final-review
status: approved
owner_role: reviewer
work_block_id: wb-004
reviewed_implementation_head: 4da0fb7582aa75f3b1e971f1f0c60f16c6b1756a
created_at: 2026-07-25
last_verified: 2026-07-25
verdict: READY
---

# PR #4 Final Review

## Scope

Final assurance review of PR #4, `Normalize runtime integration adapters`,
covering:

- the runtime/integration authority boundary;
- Claude Code logical-role agents and machine-readable hooks;
- empty/default-deny MCP and plugin posture;
- OpenCode project instructions, agents, and permissions;
- shared consequential-action and external-runtime guards;
- file-handoff task/result portability and compatibility runner boundaries;
- generated-project delivery, navigation, and publication safety;
- setup, profile, Work Block, and quickstart consistency.

The reviewed implementation head is
`4da0fb7582aa75f3b1e971f1f0c60f16c6b1756a`. Subsequent changes in the review
closeout scope are limited to evidence, documentation synchronization, Work
Block status, navigation state, and PR metadata.

## Review Method

- inspected high-authority governance, runtime, integration, and generated
  project contracts;
- compared runtime roles with project agent configurations and permissions;
- inspected shared and runtime-specific hooks;
- tested direct external runtime admission, missing admission evidence, source
  write scope, Hard Stops, stale approvals, assurance, and closeout;
- inspected generated Claude Code, Codex, OpenCode, MCP, and handoff defaults;
- reviewed bootstrap inventory and character-safe placeholder replacement;
- ran the complete `Framework Contracts` workflow and disposable scaffold.

## Findings and Resolutions

### F-01 — Provider-specific implementations were encoded as authority roles

**Severity:** High  
**Status:** Resolved

The generated Claude Code baseline contained `gpt-critic`, `gpt-verifier`, and
`codex-reviewer` agents and related memory, which coupled logical assurance to a
provider/model family.

Resolution:

- removed provider-named default agents and memory;
- retained only Architect, Critic, Coder, Reviewer, and Verifier runtime
  implementations;
- moved cross-runtime Codex use to explicit integration adapters;
- added contract tests that reject provider-authoritative defaults.

### F-02 — External integrations were enabled or implied by default

**Severity:** High  
**Status:** Resolved

The old generated setup preconfigured Codex MCP and granted MCP tool access,
while documentation implied that plugins/MCP were part of the normal runtime
baseline.

Resolution:

- generated `.mcp.json` is exactly an empty registry;
- OpenCode `mcp` and `plugin` collections start empty;
- Claude settings pre-authorize no external MCP/plugin tools;
- setup, profiles, and quickstart select `integration_profile: none` by default;
- activation now requires an admission record and target-environment smoke.

### F-03 — OpenCode lacked an executable project contract

**Severity:** High  
**Status:** Resolved

OpenCode was described as experimental without a project configuration, logical
agents, or permission boundary.

Resolution:

- added `opencode.json` with project instructions and fail-safe permissions;
- added Architect, Critic, Coder, Reviewer, and Verifier project subagents;
- denied common secret paths, external directories, commit, push, destructive
  Git, and `rm`;
- required approval for edits, Bash, web, task delegation, and MCP;
- kept provider/model routing private and plugins/MCP inert;
- added frontmatter/config parsing and permission fixtures.

Target-environment runtime smoke remains required before higher-governance use.

### F-04 — Claude Code gates depended on provider-specific Markdown state

**Severity:** High  
**Status:** Resolved

Legacy Claude hooks required a GPT/Codex MCP route and duplicated Critic and
verification state in Markdown files.

Resolution:

- added a machine-readable Claude source-write gate using the active Work Block;
- added a machine-readable Review/Verification/Drift/closeout gate;
- routed consequential Bash actions through the shared provider-neutral policy;
- reduced old gate scripts and Markdown files to compatibility views/wrappers;
- aligned Claude and Codex around one Work Block specification, Git baseline,
  write-set, integration, assurance, and closeout state.

### F-05 — External runtime invocation did not require complete admission evidence

**Severity:** High  
**Status:** Resolved

A direct `codex`, `claude`, or `opencode` child process crosses a provider/runtime
boundary. An integration ID alone did not prove that the trust, data, secret,
permission, and recovery review existed.

Resolution:

- shared Hard Stop policy maps direct runtime commands to stable integration IDs;
- invocation requires an active/non-expired gate and fresh Git baseline;
- the matching ID must be present in `integrations.approved`;
- at least one concrete admission-evidence path must be present in
  `integrations.admission_records`;
- a focused regression fixture proves that ID-only approval is denied.

Pattern matching covers common direct command forms. Indirect wrappers,
interpreters, containers, aliases, hosted tools, or specialized launch paths
still require their own integration and permission review.

### F-06 — File handoff encoded one fixed Codex-to-Claude topology

**Severity:** Medium  
**Status:** Resolved

The previous public handoff contract described Codex as Control Tower and Claude
Code as the only target runtime.

Resolution:

- added a runtime-neutral task/result envelope with logical function, runtime,
  revision, authority, scope, Hard Stops, evidence, and recovery;
- reclassified the existing Claude runner as a compatibility transport;
- marked the Claude task template as a specialization of the portable envelope;
- retained scope audit, queue/recovery, environment, and concurrency controls;
- documented that scope audit is detection evidence, not kernel isolation.

### F-07 — Work Block and setup artifacts did not expose integration admission

**Severity:** Medium  
**Status:** Resolved

Runtime capability fields mentioned MCP/plugins but did not require a separate
integration profile, admission records, data/secret boundaries, or smoke
results.

Resolution:

- added an Integration Profile and Admission section to the Work Block template;
- added a reusable integration-admission template;
- rewrote setup, profile selector, minimal quickstart, runtime maps, and MCP/tool
  policy;
- registered runtime/integration boundaries in framework and generated-project
  maps/registries.

### F-08 — Scaffold placeholder replacement was unsafe for normal characters

**Severity:** Medium  
**Status:** Resolved

The previous `sed` replacement corrupted project names containing `&` and
filesystem paths containing normal replacement-sensitive characters. Publication
smoke exposed unresolved/reintroduced placeholders.

Resolution:

- replaced shell replacement syntax with literal Python string replacement;
- copied skills before one unified replacement pass;
- retained disposable scaffold checks using a project name containing `&`;
- verified generated project name, slug, paths, configs, and registries.

## Validation Evidence

GitHub Actions workflow `Framework Contracts`, run `211`, completed successfully
for review head `4da0fb7582aa75f3b1e971f1f0c60f16c6b1756a`.

The workflow passed:

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-integration-contracts.py
python scripts/test-integration-admission-evidence.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

It also:

- parsed JSON/YAML and OpenCode agent frontmatter;
- compiled shared/Claude/Codex Python hooks;
- checked shell syntax;
- verified inert MCP/plugin defaults and retired-agent absence;
- bootstrapped and inspected a disposable generated project.

A final documentation/navigation head must pass the same workflow before the PR
is marked ready for review.

## Residual Limitations

- project hooks and runtime permissions are guardrails, not OS-level isolation;
- OpenCode behavior still requires a real target-environment version/capability
  and denied-action smoke;
- official plugin, MCP, and live handoff smokes were not run because local
  runtime authentication/provider environments are deliberately outside CI;
- the bundled handoff runner remains Claude Code-specific internally;
- direct-runtime command detection is pattern-based and cannot cover every
  indirect process launch;
- external provider data handling/retention depends on the admitted runtime or
  service configuration;
- profile-aware minimal adapter installation and broader cross-runtime
  conformance remain WB-005.

## Verdict

`READY`

No unresolved blocking defect was found in the WB-004 scope. PR #4 may be marked
ready for human review after the final closeout/documentation head passes the
same CI contract suite.
