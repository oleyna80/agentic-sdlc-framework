# Framework Profiles

The framework separates installation composition from Work Block control. Do not
collapse these dimensions into one vendor-specific preset.

A generated project records one installation profile. Each Work Block then
selects independently:

```yaml
installation_profile: codex
governance_profile: Managed
runtime_profile: codex
integration_profile: none
model_class: balanced_engineering
isolation: separate_session
evaluation_posture: required
approved_evaluation_plan: docs/evals/feature-x/plan.json
```

Installation determines copied runtime surfaces and skills. Governance determines
control and assurance. Runtime executes a logical function. Integration admits an
external bridge/tool/transport. Model and isolation record actual execution.
Evaluation posture determines whether deterministic tests alone are sufficient or
an approved output/trajectory evaluation is required.

None of these dimensions grants authority by itself.

## 1. Installation Profiles

Source: `bootstrap/profiles.json`. Detailed guide: `docs/bootstrap-profiles.md`.

| Profile | Project-local implementation surfaces | Default use |
|---|---|---|
| `core` | none; generic guidance only | smallest runtime-neutral scaffold |
| `codex` | `.codex/` | Codex-primary project |
| `claude-code` | `CLAUDE.md`, `.claude/` | Claude Code-primary project |
| `opencode` | `opencode.json`, `.opencode/` | OpenCode-primary project after smoke |
| `multi-runtime` | Codex + Claude Code + OpenCode + empty `.mcp.json` | mixed-runtime baseline |

Aliases: `minimal`/`generic` → `core`; `full` → `multi-runtime`.

Every profile includes runtime-neutral evaluation governance, templates, and
`scripts/validate-evaluation.py`. This does not make evaluation required and does
not activate a runtime, judge, integration, or authority gate.

Rules:

- `.agent/bootstrap-profile.json` records composition only;
- installed files do not prove CLI/auth/provider/hooks/sandbox/isolation;
- changing composition is a deliberate migration;
- no profile activates plugins, MCP servers, external runtime calls, credentials,
  watchers, services, or LM judges.

## 2. Governance Profiles

### Advisory

Read-only research, architecture discussion, explanation, or decision support.

Required:

- objective, scope, inspected sources, assumptions, gaps;
- no source-write or consequential mutation authority;
- evaluation normally optional;
- any score or comparison must be labeled as advisory and non-independent.

### Controlled

Small, bounded, low-risk changes.

Required:

- explicit objective and write-set;
- one Coder;
- side-effect and Hard Stop classification;
- deterministic checks when applicable;
- targeted review/verification and rollback path;
- evaluation decision with reason.

Output/trajectory evaluation becomes required when behavior is materially
non-deterministic, autonomous tool selection matters, or process compliance is an
acceptance condition.

#### Narrow Deterministic Repair

NDR is a Controlled submode for a deterministic and reversible compatibility
repair. It requires an exact CI/bootstrap/runtime-validation allowlist, one repair
record, deterministic commands, and one independent combined assurance report.
It excludes architecture, product, auth, security-boundary, public API, schema,
data, deploy, and dependency-upgrade work. One implementation pass and one
correction are permitted; otherwise the Owner decides whether to stop, open a new
Work Block, change the specification, or accept residual risk.

Integration Stabilization may group no more than three sequentially discovered
eligible NDR items and two correction rounds. It is an execution envelope, not a
new governance profile, and it never widens an item's exact allowlist.

### Managed

Default for non-trivial product and engineering work.

Required:

- approved specification/revision and architecture baseline;
- implementation plan/task decomposition;
- Critic when triggered;
- one Coder per write-set;
- independent Reviewer and evidence-based Verifier;
- approved evaluation plan for agent behavior, non-deterministic outputs,
  consequential automation, or benchmark/rubric acceptance;
- durable reports and SSOT synchronization.

```text
Define -> Critic -> Execute -> Review -> Verify -> Evaluate when required -> Close
```

### Assured

High failure cost, ambiguity, security, schema, provider, deployment, or public
contract impact.

Managed controls plus:

- stronger Reviewer/Verifier/Evaluator isolation;
- fixed rubric and benchmark/dataset revisions;
- independent output and observable trajectory evaluation when applicable;
- Full verification tier and drift audit;
- threat/abuse analysis where relevant;
- explicit degraded-mode, residual-risk, and recovery evidence.

### Distributed

Multiple runtimes, machines, worktrees, or teams.

Assured controls plus:

- explicit handoff and event-source provenance;
- capability snapshot for every participant;
- non-overlapping write-sets and isolated roots for parallel writers;
- durable queue/status/recovery when needed;
- cross-runtime evaluation consolidation rules;
- assurance of the merged result;
- one Orchestrator accountable for closure.

Distributed does not mean “use more agents by default.”

## 3. Evaluation Posture

Evaluation is assurance evidence, not a new authority role.

### Not Required

Allowed only when deterministic checks and ordinary review/verification fully
prove the objective. Record the reason in the Work Block.

### Optional

May be run for learning or additional confidence. If skipped, record a concrete
`skip_reason`. Optional evaluation cannot be presented as a required passing gate.

### Required

Use when any condition applies:

- output is materially non-deterministic;
- the agent autonomously selects tools or execution paths;
- process/trajectory compliance is an acceptance condition;
- consequential automation depends on correct gate/tool behavior;
- a benchmark, dataset, rubric, or LM judge is part of acceptance;
- the governance profile or risk classification requires it.

Required evaluation needs an approved plan and cannot be skipped. Successful
closeout requires evaluation status/verdict `READY`.

### Evidence Classes

- **Deterministic tests:** compilation, type, unit, integration, contract,
  property, regression, schema, or rule checks.
- **Output evaluation:** final artifact quality against approved criteria,
  thresholds, weights, and evaluator types.
- **Observable trajectory evaluation:** tool calls/results, gates, commands,
  checks, retries, failures/recoveries, side effects, stopping conditions, and
  produced evidence.

Trajectory evidence must not request or store private chain-of-thought, hidden
reasoning, model scratchpads, secrets, or unredacted protected payloads.

An LM judge cannot prove deterministic correctness, waive failing evidence,
approve architecture/product scope, or open write/integration/deployment/Hard
Stop gates.

## 4. Runtime Profiles

### Codex

Adapter: `runtimes/codex/`. Project-local `.codex/` exists only in `codex` or
`multi-runtime` installations. Native agents may bind logical roles, but names and
models do not redefine authority.

### Claude Code

Adapter: `runtimes/claude-code/`. Project-local `CLAUDE.md`/`.claude/` exists only
in `claude-code` or `multi-runtime`. The Stop gate enforces required evaluation
closeout through the portable validator.

### OpenCode

Adapter: `runtimes/opencode/`. Use after target smoke establishes provider,
agents, permissions, tools, denied actions, and observable-event capability.
Static configuration is not OS isolation.

### Generic / Sequential

Adapter: `runtimes/generic/`. Available as guidance in every profile. Required
functions run as separate documented passes/sessions. Degraded independence and
missing event sources must be recorded honestly.

### Custom Runtime

A custom adapter declares:

- supported logical functions and read/write controls;
- isolation, hooks, tools, skills, integrations;
- observable event sources and limitations;
- capability evidence and fallback.

## 5. Integration Profiles

Integrations connect runtimes or external tools. They do not define governance or
become active because configuration files exist.

- **None:** no external bridge.
- **Official plugin:** admitted exact capability/scope/data/secret/side-effect contract.
- **MCP:** admitted exact server/tool names and boundaries.
- **File handoff:** durable queue/recovery/audit when justified.
- **Direct runtime CLI:** treated as an integration with admission evidence.
- **Manual handoff:** portable task/result artifacts when automation is unavailable.

Admission does not grant child-runtime write authority. Evaluation does not grant
integration admission.

## 6. Model Routing Overlay

Portable classes:

- `strong_reasoning` — architecture, ambiguity, Critic, high-risk evaluation;
- `balanced_engineering` — implementation, review, verification;
- `fast_readonly` — discovery, classification, deterministic checks;
- `local_executor` — bounded work after smoke.

Concrete model names belong in local runtime configuration or execution evidence.
A stronger model does not grant authority; a cheaper model does not remove
assurance. LM-judge identity and prompt/rubric revision must be recorded when used.

## 7. Isolation Levels

Record the actual boundary:

```text
same_context
separate_subagent
separate_session
separate_worktree
separate_runtime
os_isolated
```

Different model names in one context are not independent assurance. Required
trajectory evaluation must record the real event source and isolation boundary.

## 8. Selection Matrix

| Work characteristic | Governance | Evaluation posture | Typical runtime/integration |
|---|---|---|---|
| Read-only discussion | Advisory | not required/optional | any capable runtime; none |
| Small deterministic fix | Controlled | not required with reason | one safe runtime; none |
| Normal product feature | Managed | risk-based | installed/approved runtime; optional integration |
| Agent response/tool workflow | Managed/Assured | required | runtime with observable event evidence |
| Auth/DB/payment/deploy/security | Assured | required when agent behavior/non-determinism applies | stronger isolation; admitted integration only if needed |
| Parallel/cross-runtime delivery | Distributed | required for handoff/trajectory compliance | isolated roots/runtimes + explicit transport |

## 9. Selection Rules

- Start with the smallest sufficient installation and governance profiles.
- Increase governance because of risk/evidence needs, not installed runtime count.
- Determine evaluation from non-determinism, autonomy, consequences, and acceptance
  criteria—not vendor or model name.
- Select runtime only after installation and live capability checks.
- Prefer native/official integrations when they satisfy admission contracts.
- Keep credentials and private runtime configuration outside the public framework.
- Missing capability produces a recorded fallback, not a missing logical function.
- Never describe same-context review/evaluation as independent.
- Reassess profiles when scope, risk, rubric, benchmark, or event sources change.

## 10. Generated Project Evidence

Every generated project contains:

```text
.agent/bootstrap-profile.json
scripts/validate-installation-profile.py
scripts/validate-evaluation.py
docs/templates/evaluation-plan-template.json
docs/templates/evaluation-report-template.json
docs/templates/trajectory-event-template.json
```

Run:

```bash
bash scripts/bootstrap.sh
```

This validates composition and the fail-closed default. It does not prove live
runtime authentication, network access, judge stability, plugin installation,
trajectory observability, or OS isolation.
