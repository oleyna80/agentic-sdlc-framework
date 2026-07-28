# Project Map

First human-readable map for `{{PROJECT_NAME}}`. It explains authority, the
resolved installation profile, major repository zones, and what an agent should
read next.

## Architecture

`{{PROJECT_NAME}}` uses a runtime-neutral Agentic SDLC control plane with four
separable layers:

1. **Governance Core** — authority, lifecycle, artifacts, evaluation, risk gates,
   capability negotiation, assurance, and closeout.
2. **Portable workflow** — specifications, decisions, Work Blocks, implementation
   and evaluation plans, tasks, reports, skills, memory, and observable evidence.
3. **Runtime adapters** — Codex, Claude Code, OpenCode, generic, or another
   approved execution runtime.
4. **Integration adapters** — optional plugins, MCP servers, external runtime
   CLIs, hosted tools, and audited file transport.

Runtime, model, judge, integration, or installation-profile selection never
changes governance authority.

## Installation Profile

Read `.agent/bootstrap-profile.json` first when runtime availability matters. It
records which runtime implementation surfaces and skills were installed. It is
installation evidence only and does not grant Work Block authority, integration
admission, credentials, side-effect permission, or a passing evaluation verdict.

Possible conditional surfaces:

- `.codex/` for Codex;
- `CLAUDE.md` and `.claude/` for Claude Code;
- `opencode.json` and `.opencode/` for OpenCode;
- `.mcp.json` as an inert MCP configuration surface.

Absence of an unselected runtime surface is expected.

## Authority Order

1. current Owner instruction or approved change request;
2. `AGENTS.md` and Governance Core;
3. approved specification and acceptance criteria;
4. accepted architecture decisions and external contracts;
5. approved implementation and evaluation plans and write-set;
6. active tasklist;
7. review, verification, evaluation, drift, integration, and closeout evidence;
8. durable engineering memory;
9. runtime/integration policy, operational logs, generated output, references.

Reports, scores, judges, and logs are evidence; they do not silently revise product
requirements or open authority gates.

## Work Block Profiles

Each Work Block selects independently:

- **Governance profile:** Advisory, Controlled, Managed, Assured, Distributed.
- **Runtime profile:** one installed or otherwise approved runtime adapter.
- **Integration profile:** none or an admitted bridge/tool/transport.
- **Model class:** task-appropriate capability class.
- **Isolation:** actual boundary from same context to OS-isolated.
- **Evaluation posture:** not required or an approved deterministic/output/trajectory plan.

The installation profile constrains local availability; it does not activate a
runtime, integration, or evaluation authority.

## Narrow Deterministic Repair

NDR is a constrained `Controlled` submode for deterministic, reversible
CI/bootstrap/runtime-validation repairs. It uses one repair record, one Coder
pass, deterministic checks, and one independent combined assurance report. It
permits one correction. Integration Stabilization may group at most three eligible
items and two correction rounds; both ceilings fail closed to an Owner decision.

## Evaluation Assurance

`governance/evaluation.md` distinguishes:

- deterministic tests for objective contracts;
- output evaluation against an approved rubric;
- observable trajectory evaluation for tool, gate, check, retry, side-effect,
  and evidence events.

Trajectory evidence never requires private chain-of-thought, hidden reasoning,
or model scratchpads. Missing events are blocked/unverified, not passed. An LM
judge cannot waive deterministic failures or open write/integration/deployment gates.

Use:

```text
docs/evals/<evaluation-id>/plan.json
docs/evals/<evaluation-id>/events.jsonl
docs/reports/evaluations/<evaluation-id>.json
scripts/validate-evaluation.py
```

## Key Paths

| Path | Status | Purpose |
|---|---|---|
| `AGENTS.md` | normative | Compact project operating contract |
| `.agent/bootstrap-profile.json` | generated | Resolved installation profile and path contract |
| `governance/` | normative | Runtime-neutral authority, lifecycle, artifacts, evaluation, capabilities |
| `governance/evaluation.md` | normative | Deterministic/output/observable trajectory contract |
| `.agent/workflows/sdd-protocol.md` | normative | Define / Execute / Assure / Close semantics |
| `.agent/ROSTER.md` | normative | Logical roles, skill routing, runtime binding, isolation |
| `.agent/active-work-block.json` | operational gate | Specification, write-set, integrations, assurance, closeout |
| `.agent/active-work-block.default.json` | portable default | Fail-closed restore state including optional PENDING evaluation |
| `.agent/verification-gate.md` | compatibility view | Review, verification, evaluation, drift, closeout summary |
| `.agent/hooks/` | shared runtime policy | Provider-neutral consequential-action guards |
| `docs/specs/` | normative | Approved product and technical behavior |
| `docs/architecture/` | normative | Accepted architecture decisions and contracts |
| `docs/plans/` | derived/log | Approved plans and Work Blocks |
| `docs/tasklist/` | derived | Active task decomposition |
| `docs/evals/` | evidence/config | Approved evaluation plans, fixtures, observable events |
| `docs/reports/evaluations/` | evidence | Evaluation matrices, gaps, risks, verdicts |
| `docs/reports/` | evidence | All assurance, integration, and closeout evidence |
| `docs/templates/` | normative templates | Work Block, evaluation, reports, integration admission |
| `docs/engineering-memory/` | durable reference | Evidence-backed reusable decisions |
| `memory_bank/` | operational/local | Current focus, progress, pending decisions, logs |
| `runtimes/` | adapter documentation | Capability, activation, limitation, fallback |
| `integrations/` | adapter documentation | Optional bridge/tool/transport admission |
| `scripts/bootstrap.sh` | health check | Validates profile/default and restores local state |
| `scripts/validate-installation-profile.py` | validator | Selected paths, kinds, absent surfaces, blocked default |
| `scripts/validate-evaluation.py` | validator | Evaluation plan/report consistency and closeout binding |
| `scripts/repair-lifecycle.py` | validator | Fail-closed NDR record limit validation |
| `docs/templates/repair-record-template.md` | normative template | NDR scope, verification, and stop-condition record |
| `docs/templates/combined-assurance-report-template.md` | normative template | Independent NDR review and verification evidence |
| source/test directories | source | Controlled by approved Work Block write-sets |

## Safe Defaults

- no plugin, external bridge, MCP server, or watcher is enabled automatically;
- no provider-named authority agent is installed;
- external runtime calls require active integration approval;
- blocked default evaluation is optional, `PENDING`, unbound, and has no authority;
- credentials and private runtime state remain local;
- observable evidence must exclude secrets, protected payloads, and hidden reasoning.

## Core Lifecycle

```text
Define
  discovery -> architecture -> specification -> implementation/evaluation plans -> critic

Execute
  scoped implementation -> self-check -> observable event capture -> frozen diff

Assure
  independent review -> technical verification -> agent evaluation -> drift audit

Close
  SSOT sync -> engineering memory -> closeout report
```

Required evaluation must be `READY` for `success-closeout`. Optional evaluation
may be skipped only with a concrete reason.

## Generated, Derived, Evidence, and Local Boundaries

- specifications and accepted architecture decisions are normative;
- implementation/evaluation plans and tasklists are derived/configuration;
- reports and observable events are evidence, not requirement authority;
- `.agent/bootstrap-profile.json` is generated installation evidence;
- engineering memory is durable only when evidence-backed and secret-free;
- `memory_bank/**` and runtime memory are operational/local by default;
- provider auth, downloaded plugins, browser sessions, local IDE state, `.env*`,
  tokens, cookies, credentials, keys, and live customer data must not be committed.

## New-Session Read Strategy

Always for non-trivial work:

1. `AGENTS.md`;
2. `.agent/bootstrap-profile.json` when runtime availability matters;
3. active Work Block;
4. active specification and revision;
5. approved implementation/evaluation plans;
6. relevant architecture decisions;
7. repository status and current diff.

Read conditionally:

- relevant Governance Core contract, especially `evaluation.md`;
- detailed SDLC protocol and role/skill roster;
- installed/approved runtime adapter;
- selected integration adapter and admission record;
- evaluation evidence required by the Work Block;
- relevant skills, engineering memory, and operational logs.

Do not treat an absent unselected runtime surface as corruption.

Update this map and `FILE_REGISTRY.yml` when installation composition, authority,
source-of-truth order, lifecycle, evaluation, integration, gates, adapters, or
normative/evidence/local boundaries change.
