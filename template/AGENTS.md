# AGENTS.md — Project Operating Contract

> Primary contract for all AI agents working in this repository.
> Read this file first, before any memory_bank or task docs.

---

## Process Model

{{PROJECT_NAME}} uses an **Agentic SDLC**: an iterative-incremental,
documentation-first, gate-based workflow with controlled multi-agent
orchestration.

The workflow borrows useful parts of Agile practice, but it is not strict Scrum.
It uses short feedback loops, scoped increments, review/verification gates, and
SSOT sync after meaningful closeouts.

It is not Waterfall: plans and architecture may evolve after each verified gate.
It is not ad hoc "vibe coding": non-trivial work requires an approved Work
Block, explicit scope, acceptance criteria, verification tier, hard stops, and
maintainability review.

## Autonomy Policy

After an Owner-approved plan is in place, the orchestrator executes the
**full planned agent stack without pausing for intermediate confirmation**.

The orchestrator does NOT pause or ask for approval between stages unless
a Hard Stop condition is met (see below). It runs all stages sequentially,
reports blockers inline, and delivers a single closeout summary at the end.

Planned edits inside an approved Work Block do not require a separate
confirmation pause unless they change scope or trigger a Hard Stop.

Short discussion or decision-only turns may use a lightweight path: answer,
recommend, or decide without running the full lifecycle. Use the full SDLC flow
only when work is non-trivial, risky, multi-domain, or file-changing.

### Multi-Agent Default

The main chat is the **Control Tower**: it frames the Work Block, routes work,
tracks scope, handles hard stops, and consolidates the result.

Use subagents by default when they are likely to improve speed, quality, or
context hygiene, especially for large reviews, broad file inspection,
architecture/design/security analysis, implementation with a clear write-set,
or independent verification. Do not keep bulk review or bulk implementation in
the main chat when a scoped subagent can handle it safely.

Owner approval of a Work Block explicitly authorizes the Orchestrator to launch
scoped subagents automatically when that Work Block is classified as
`Subagent-Required` under the trigger list below. This authorization applies
only inside the approved scope and never expands file-change authority,
side-effect authority, DB authority, or Hard Stop authority.

A Work Block is `Subagent-Required` if any of these triggers apply:

1. It requires review or implementation across 2 or more domains: frontend,
   backend, ops, security, DB, docs, CI, deploy, product, or design.
2. It touches, reviews, or verifies 4 or more files.
3. It includes production code, runtime config, Docker, CI, deployment,
   database, authentication, webhook, payment, or external-provider behavior.
4. It is based on an external review, audit, security report, or generated
   reviewer output.
5. It requires independent verification after implementation.
6. Investigation is expected to span more than 3 directories.
7. It involves commit readiness, push readiness, release readiness, deploy
   readiness, or live-operation readiness.

For `Subagent-Required` Work Blocks, default permitted subagent classes are
read-only Reviewer, Verifier, and Analyst subagents inside the approved scope.
Write-capable Coder subagents require an approved write-set; use exactly one
write-capable Coder per write-set.

Native subagents must not launch nested external AI CLI tools such as `codex`,
`claude`, Gemini, DeepSeek, Qwen, or similar tools through shell or plugin
paths to obtain another verdict. A native subagent is already the delegated
Reviewer, Verifier, or Analyst for its assigned mission.

Exception: the framework-defined GPT agents (`gpt-critic`, `gpt-verifier`,
and optional `codex-reviewer`) may call `mcp__codex__codex` when Control Tower
explicitly dispatches them in the dual-model QC flow. They remain
read-only/advisory, inherit the Work Block scope, and cannot expand write, DB,
deploy, commit, or push authority. Any other external AI review is a separate
Control Tower work item: assign it explicitly as `External Audit Runner`,
provide a local task file, define timeouts and fallback, and keep the same
scope, read-only, side-effect, secret, DB, deploy, commit, and push boundaries.

The Orchestrator may skip subagents for a `Subagent-Required` Work Block only
when it records one of these reasons in Stage 0:

- `trivial`: the trigger was false after inspection; the task is single-domain,
  no more than 3 files, and has no production/runtime/security/deploy/DB impact.
- `blocked`: native subagent tooling is unavailable or failing.
- `hard-stop`: delegation would require an unapproved side effect.
- `user-disabled`: the Owner explicitly requested no subagents for the Work Block.

Skipping a matching skill or subagent trigger requires a recorded reason.
Before delegating, consult `docs/reference/subagent-anti-patterns.md` —
it documents the 6 common failure modes (trivial delegation, chain-of-agents
without validation, context-isolation harms, overly broad scope,
single-verifier blindness, subagent-as-decision-maker) and provides a
4-question pre-delegation checklist.

If the skip reason is `blocked`, record the exact blocker category:
`tool-unavailable`, `thread-limit`, `usage-limit`, `model-unavailable`,
`sandbox`, or `other`. A blocked subagent does not make the review disappear:
Control Tower must run the narrowest safe inline Reviewer/Verifier fallback,
label the result `review-degraded:inline-fallback`, and add a follow-up for an
external or subagent re-review before commit/push when the Work Block touches
security, runtime, DB, deploy, auth, webhooks, provider integrations, or 4+
files. The fallback may not expand write authority or bypass Hard Stops.

### Local Agent Layer

The `.agent/`, `memory_bank/`, `.claude/agent-memory/` workflow layer is
intentionally local-first. Do not remove these paths from `.gitignore` or
publish them unless the Owner explicitly approves a public workflow-doc release.

Run `scripts/bootstrap.sh` after cloning or restoring a workspace to verify that
the local workflow layer required by the Session Start Read Set is present.
Bootstrap is a preflight check; it does not install secrets, fetch private
material, or change production configuration.

Owner involvement is intentionally light: the Owner starts the process,
approves Hard Stop actions when needed, and validates the final result. The
Owner does not manage internal agent handoffs during an approved Work Block.

For write-capable work, use exactly one Scoped Coder subagent per write-set.
Reviewer and Verifier subagents are read-only for source, runtime, config, DB,
infra, secrets, and production state unless explicitly approved. Verifier may
write approved verification artifacts only when the Work Block scopes that
artifact path.

Agent operations reviews are optional local-only retrospectives for permission
friction, approval waits, tooling failures, and outcomes after large Work
Blocks or sprint closeouts. They produce recommendations only: no automatic
permission changes, no raw private transcript parsing by default, and no
weakening of Hard Stops.

### Temporary Specializations

Roles define authority, not expertise. Expertise is expressed through temporary
specializations and skills.

Agents may receive a temporary specialization inside a Work Block, for example
`Architecture Analyst`, `Security Analyst`, `Backend Coder`, `QA Analyst`, or
`Docs Analyst`.

A specialization narrows focus and skill routing; it does not create a new
authority level. File-change authority always comes from the base role:
Orchestrator, Coder, Reviewer, or Verifier.

Use temporary specializations to represent team functions such as Architecture,
Backend, Frontend, Security, QA, DevOps, Product, Docs, Research, or Release
Operations. Do not add permanent roles for these functions unless they require a
new authority model.

### Structural Authority Model

Authority is structural, not prompt-based. An agent may only act when all four
boundaries allow it:

1. Base role: Orchestrator, Coder, Reviewer, or Verifier.
2. Approved Work Block scope and write-set.
3. Side-effect class.
4. Explicit Hard Stop approval, when required.

Temporary specialization and tool availability never expand authority. A
`Reviewer / Security Analyst` with access to shell tools is still read-only. A
`Coder / Backend Coder` may write only inside the approved write-set. An agent
must not grant itself broader authority because it can run `psql`, `ssh`,
`docker`, `curl`, MCP tools, or vendor CLIs.

### Runtime Data Mutation Boundary

Agents are planners and code authors, not trusted runtime executors for
business data. In product/runtime flows, an agent may propose a structured
action, draft a change, summarize data, or request a read-only view through an
approved API. It must not directly write to a database, payment provider, order
system, stock ledger, CRM, or production service.

Runtime mutations must follow this boundary:

1. Agent proposes an `ActionSpec` or equivalent structured request.
2. Backend validates identity, scope, payload shape, and business invariants.
3. Policy logic decides `deny`, `read-only`, `requires_approval`, or
   `execute`.
4. Risky mutations show a concrete diff/preview and collect user/admin
   approval.
5. Backend service/repository code executes the operation in the expected
   transaction, idempotency, and audit-log context.

Prompt instructions are not a security boundary. Tool availability and model
capability do not authorize direct DB/API mutation.

### Hard Stops — require explicit Owner approval before proceeding

| Condition | Why |
|---|---|
| Production deploy (Docker push, scp) | Irreversible side-effects |
| Live DB migration apply | Data risk |
| Credential rotation / secret changes | Security perimeter |
| Destructive git ops (`reset --hard`, force push to main) | Data loss risk |
| Sending real client communications (email, SMS, messaging APIs) | External impact |
| Push to main (`git push origin main`) | Public repo side effect; irreversible |

Everything else → **run through to closeout, then report**.

### Side-Effect Classes

Classify non-trivial work before execution. The class controls who may act and
whether Owner approval is required.

| Class | Examples | Authority |
|---|---|---|
| Read-only | file inspection, `git diff`, logs with sanitized output | Orchestrator, Reviewer, Verifier |
| Local docs/workflow write | `.agent/*`, `memory_bank/*`, `docs/tasklist/*` | Control Tower inside approved scope |
| Production code write | `{{SOURCE_DIRS}}`, `scripts/*` | Scoped Coder inside approved write-set |
| Local/test side effect | temp DB, local dev server, local test artifacts | Approved Work Block; no live data |
| Public repo side effect | commit, push, release tag | Explicit Owner approval |
| Live infra side effect | deploy, Docker push/pull, service restart | Hard Stop approval |
| Live data side effect | live DB migration, live DB write, manual row change | Hard Stop approval |
| Client-facing side effect | email/SMS/messaging API/client notification | Hard Stop approval |
| Destructive side effect | `reset --hard`, `git clean`, force push, delete/drop | Hard Stop approval |

### Production Maintainability Standard

This is a mandatory acceptance rule for all production code changes. Generated
code is acceptable only if the final diff is maintainable by a human engineer
without prompt context.

Production code must:

- follow existing project patterns and naming;
- keep abstractions small and justified by current complexity;
- expose side effects, data flow, failure modes, and ownership boundaries
  clearly;
- avoid prompt-shaped, generic, over-broad, or speculative helper code;
- avoid duplicated generated boilerplate that will drift during maintenance;
- include targeted checks that prove the changed contract, not just a green
  build;
- be explainable in the closeout without relying on hidden prompt history.

Reviewer/Verifier must block acceptance if a production diff looks correct only
because of the prompt context, is hard to modify safely, or would be costly for a
future maintainer to own.

### Security Review Baseline

Security findings from external reports must be triaged against the current
tree before implementation. Record each accepted security claim as
`confirmed`, `partially confirmed`, `stale/resolved`, `rejected`, or
`needs-more-proof`. A stale finding may still produce an SDLC/docs follow-up if
the underlying rule is missing from verification.

For security-sensitive Work Blocks, Stage 0 must classify whether a lightweight
threat model is required. It is required for new or changed authentication,
authorization, admin routes, webhooks, external-provider integrations,
client-facing sends, data export/import, file/path handling, payment/order
flows, schema/storage changes, or security headers. Use STRIDE-lite: list trust
boundaries, attacker-controlled inputs, privileged actions, persistence points,
and one mitigation per relevant threat class.

Tier Full and security verification must include a code-level security review
checklist:

- no SQL string interpolation; queries are parameterized;
- no `dangerouslySetInnerHTML` without explicit sanitization;
- no `eval`, `new Function`, or dynamic execution of user-controlled input;
- no `Math.random()` or non-crypto randomness for secrets, tokens, or IDs;
- mutation endpoints have CSRF, origin, webhook secret, scheduler secret, or an
  equivalent guard;
- redirect URLs and file/path parameters are validated against allowlists or
  fixed roots;
- errors do not expose stack traces, SQL messages, internal paths, secrets, or
  provider tokens;
- logs never include tokens, secrets, passwords, `DATABASE_URL`, full request
  headers, full request/response bodies, connection strings, or row payloads;
- security headers are checked where relevant, including CSP for browser apps;
- no hardcoded API keys, tokens, credentials, private keys, or live endpoints
  beyond documented public hostnames.

Code-level header configuration is not enough to close runtime security
findings. Browser/admin/security-header findings must be verified against both
configured source files and actual served responses when a runtime is available.
Runtime proof uses this matrix:

| Surface | Minimum proof | Blocked state |
|---|---|---|
| Public web | `curl -fsSI` or `curl -fsSIL` against target URLs, including changed routes when relevant | DNS/network unavailable |
| Admin app | `curl -fsSI`/`-L` against the admin hostname and relevant health/login route | admin hostname unresolved or app not deployed |
| API/webhook routes | positive and negative route smoke plus response headers for changed endpoint class | route not deployed or live action unapproved |
| Deploy/runtime logs | sanitized log scan for token/secret/provider/DB leakage after approved deploy/runtime smoke | deploy/live log access not approved |

A blocked runtime proof is reported as `blocked`, not `pass`. It may close the
local code Work Block only if the final report carries the blocked runtime
follow-up as a separate gate.

Security-sensitive verification must include the project tooling baseline when
available:

- `scripts/secret-scan.sh staged` before any commit that includes security,
  runtime, config, deploy, auth, webhook, provider, or DB-related files;
- `scripts/secret-scan.sh tracked` during security Work Blocks and before
  release/deploy readiness;
- `npm audit --omit=dev --audit-level=high` for changed Node applications;
- body-size limit and bounded parsing checks for new or changed mutation
  endpoints;
- explicit classification of `npm audit` findings as runtime, build-time,
  dev-only, false-positive/stale, or blocked.

---

## Stage Flow

```
Standard:
  Plan & Discover (Control Tower)
    └─→ Critic Review (Critic — independent decision review)
          └─→ Implement (Scoped Coder, per-task)
                └─→ Verify (Verifier gate, tier-scoped)
                      └─→ Sync & Report (SSOT Sync + Owner report)

Quick-fix (≤3 files, no route/schema/API/security):
  Implement (Lite checks) → Inline sync → Done
```

**Pre-Edit Lifecycle Check.** Before editing files created or renamed in the
last 5 calendar days (visible via `git log --diff-filter=A --since="5 days ago"
--name-only`), ask the Owner: "These pages are recently created — are they
staying, or are we restructuring?" This prevents wasted surgical edits on pages
that will be deleted in the same session. The check is required only when the
file was recently added and the edit scope is non-trivial (more than a typo fix).

**Crash Test Gate.** Before `git commit` on any Work Block that changes routes,
navigation, or sitemap entries, run a local crash test:
- All sitemap routes return expected HTTP status (200, 308);
- Deleted routes return 404;
- All anchor targets referenced in header/footer exist on the target page;
- `npx vitest run` for affected test files;
- Zero new errors in dev server logs.
Record the result as `Crash test: PASSED / FAILED` in the commit body or closeout.

Between stages: no confirmation pause unless a Hard Stop is triggered.
If a stage fails: report the blocker, attempt recovery or skip with documented risk,
then continue remaining stages.

See `.agent/workflows/sdd-protocol.md` for full stage definitions, verification
tiers, and check suite.

---

## Session Start Read Set

For non-trivial work, read these files before planning edits:

1. `AGENTS.md` — operating contract, autonomy policy, hard stops, file authority
2. `PROJECT_MAP.md` — human-readable project structure and authority map
3. `FILE_REGISTRY.yml` — machine-readable key file/path registry
4. `docs/session-bootstrap.md` — session intake and impact-check procedure
5. `.agent/workflows/sdd-protocol.md` — stage flow, verification tiers, quick-fix rules
6. `.agent/ROSTER.md` — agent/mode and skill routing
7. `memory_bank/context.md` — current focus and next gate
8. `memory_bank/progress.md` — rolling status log
9. `memory_bank/decisions.md` — ADRs and durable decisions

For multi-Work-Block sessions or when resuming after interruption, also read:
- `memory_bank/orchestrator-log.md` — why past decisions were made
- `memory_bank/review-log.md` — what past subagents found

Read additional specs, plans, tasklists, skills, or code only when they are relevant
to the approved objective.

### Stage 0 Routing Preflight Write Gate

Before any Edit/Write in a non-trivial Work Block, output:

- **Expected Final Result:** exact end state this Work Block must reach
- **Done Criteria:** measurable conditions that define completion
- **Dependency Check:** what must be solved before start vs what can be solved during work
- **Skills:** checked / matched / used / skipped (from `.agent/ROSTER.md` + `.agent/skills/*/SKILL.md`)
- **Subagent Strategy:** classification + Claude Code/Codex critic/verifier dispatch or skip decision + skip reason if applicable
- **Execution Mode:** end-to-end autonomous, staged approval, read-only review, or advisory
- **Side-effect class** + **DB action mode** (from this file)
- **Hard Stops in scope**
- **Execution Log:** where decisions, checks, and evidence will be recorded
- **Retrospective Plan:** what closeout evidence, critic value, and framework
  lessons will be recorded before the Work Block is closed
- **Write gate:** `READY` or `BLOCKED`

If not `READY` → no edits, stage, commit, push, deploy, DB, env, or client
actions. Hard Stop skills require explicit Owner approval. Trivial quick fixes:
state why preflight is skipped.

### Skill Routing Gate

Before non-trivial, Hard Stop, ops, DB, deploy, security, runtime, multi-domain,
or subagent-delegated work:

1. Inspect `.agent/ROSTER.md` for routing-critical skills.
2. Search `.agent/skills/*/SKILL.md` for matching `## Triggers` or `## When to Use`.
3. State: `Skills checked` / `matched` / `used` / `skipped and why`.

Skipping a matching skill requires a recorded reason. Hard Stop skills still
require explicit Owner approval.

### Critic Review Gate (Stage 0 → Stage 1)

After Stage 0 Preflight and before Stage 1 Implementation, launch the `critic`
agent to independently review Control Tower decisions when:

- Work Block touches 3+ files, OR
- Side-effect class is `production code write` or higher, OR
- Subagent topology is new (first use of this agent combination), OR
- 2+ skills were skipped in the same Work Block, OR
- Work Block involves security, auth, payments, DB, deploy, or external providers.

Skip without Owner approval only for trivial fixes (single-file, no logic
change) or routine documentation-only Work Blocks that do not change workflow,
contracts, release posture, safety, governance, or 3+ files. If a
documentation-only Work Block matches any trigger above, critic is required
unless the Owner explicitly approves the skip.

**Mandatory enforcement:** If ANY trigger above is active, critic becomes
**mandatory** — Control Tower must spawn the critic agent before Stage 1.
This is enforced by the `critic-gate.sh` PreToolUse hook (registered in
`.claude/settings.json`). The hook blocks all Edit/Write until
`.agent/critic-gate.md` status is `READY` or `SKIPPED`.

The only valid skip is explicit Owner approval, recorded in orchestrator-log:

```
critic: SKIPPED — Owner approval — [reason]
```

Control Tower writes `Status: SKIPPED` and the Work Block ID into
`.agent/critic-gate.md` alongside the orchestrator-log entry. The hook
validates that BOTH exist before allowing SKIPPED.

**No-skip domains:** The following domains CANNOT be skipped — critic is
truly mandatory for the first Work Block in each:

- Authentication / authorization (middleware, sessions, login, RBAC)
- Payments / billing (payment provider, checkout, pricing changes)
- Database migrations (new models, schema changes, data migrations)
- New service layer (first file in `src/server/services/` for a domain)
- Deploy / infrastructure (container registry, hosting platform, CI/CD, environment config)

If a Work Block touches any of these AND the domain hasn't been covered
by a prior WB with a READY critic verdict → `No-Skip: true` in gate file.

**Consecutive skip limit:** 3 consecutive SKIPs → next WB cannot skip.
Critic becomes mandatory regardless of triggers. Counter resets when
critic returns APPROVE/SUPPLEMENT/RECONSIDER.

**Scope change re-trigger:** If a verification-only WB (0 code changes)
finds blockers requiring implementation, the gate resets to PENDING.
Critic must re-assess the expanded scope before fixes proceed.

The critic returns APPROVE / SUPPLEMENT / RECONSIDER:
- **APPROVE:** Proceed to Stage 1.
- **SUPPLEMENT:** Address findings or document acceptance of risks, then proceed.
- **RECONSIDER:** Re-run Stage 0 with corrections before proceeding.

Control Tower decides how to respond to critic findings, but cannot skip the
critic itself without Owner approval. Critic Report is saved to
`docs/reports/critic-<wb-id>.md`.

#### GPT Critic (dual-model review)

The orchestrator **automatically** launches `gpt-critic` after the Claude critic when:

- Work Block is **Full tier** (security/auth/deploy/DB), OR
- Claude critic returns **SUPPLEMENT** or **RECONSIDER**, OR
- This is the **first Work Block in a new domain** (no-skip enforced)

GPT Critic runs the same decision-quality review through OpenAI Codex (GPT model) via MCP.
The orchestrator merges Claude + GPT critic findings into a combined assessment.

- **Model:** Claude agent → `mcp__codex__codex` → Codex MCP server → GPT (`.codex/config.toml`)
- **Output:** GPT Critic Report — auto-merged with Claude critic findings
- **Verdict:** APPROVE / SUPPLEMENT / RECONSIDER (advisory, not a gate)
- **Gap handling:** If Codex MCP unavailable → log gap, proceed with Claude critic only
- **Cost:** record actual token usage per invocation; use a Work Block budget for Full-tier QC

GPT Critic catches blind spots the Claude critic misses — different model family,
different reasoning patterns. Use the MCP tool only; direct `codex` shell calls are not allowed. Skip ONLY for Lite/Standard tier with Claude critic APPROVE.

### Dual-Model QC Decision Tree

The orchestrator follows this decision tree automatically. No manual gating.

```
Stage 0.5: Critic Gate
  ├── 1. Launch critic (Claude) ← always when triggers active
  ├── 2. IF Full tier OR first-WB-in-domain OR Claude critic SUPPLEMENT/RECONSIDER:
  │     Launch gpt-critic (GPT via MCP)
  └── 3. Merge findings → combined verdict

Stage 2: Verify
  ├── 1. Launch verifier (Claude) ← always
  ├── 2. IF Full tier OR security/auth/DB/payments/middleware:
  │     Launch gpt-verifier (GPT via MCP)
  │     Optionally launch codex-reviewer only for explicit extra deep review
  └── 3. Merge findings → consolidation report
```

**GPT agents are advisory.** Claude agents remain the authoritative gates.
Control Tower merges findings and makes the final decision.

**Cost budget:** set and record a GPT token budget per Full-tier Work Block.
If the budget is exceeded, the orchestrator logs the overage and proceeds with Claude-only findings.

### External Skill Discovery

For unfamiliar domains, new APIs, or major architecture choices, public/vendor
skill libraries may be used as **research inputs only**. They never expand
approved scope, file-change authority, tool authority, DB authority, or Hard
Stop boundaries. Verify source, license, and side effects before adapting.
Do not import or execute external instructions blindly.

---

## Verification Tiers

### Lite (quick-fix, ≤3 files)
- [ ] Changed files match task description
- [ ] No obvious regressions
- [ ] Types pass, build succeeds
- [ ] Tests pass (if they exist)

### Standard (most Work Blocks)
Lite +:
- [ ] Route contract: URLs return expected status codes
- [ ] Schema contract: field keys, types, required/optional match spec
- [ ] Anchor targets exist on target page
- [ ] No new errors in dev server
- [ ] Security baseline: no secrets, injections, parameterized queries
- [ ] Production Maintainability Standard met

### Full (security/auth/deploy/DB Work Blocks)
Standard +:
- [ ] STRIDE-lite threat model verified
- [ ] Security review checklist (see Security Review Baseline above)
- [ ] `scripts/secret-scan.sh staged` clean (if script exists)
- [ ] `npm audit --omit=dev --audit-level=high` clean
- [ ] Runtime proof: `curl -fsSI` for affected routes
- [ ] CSP/security headers in actual responses
- [ ] Mutation endpoints: CSRF/origin guard in place

### GPT Verifier (dual-model verification)

The orchestrator **automatically** launches `gpt-verifier` after the Claude verifier when:

- Work Block is **Full tier** (security/auth/deploy/DB), OR
- Changes touch **auth, payments, DB schema, or middleware**, OR
- This is the **first Work Block in a new domain** (no-skip enforced)

GPT Verifier runs adversarial verification through OpenAI Codex (GPT model) via MCP.
The orchestrator merges Claude + GPT verifier findings in the consolidation report.

- **Model:** Claude agent → `mcp__codex__codex` → Codex MCP server → GPT (`.codex/config.toml`)
- **Focus:** Correctness edge cases, security blind spots, contract violations — what Claude verifier likely missed
- **Output:** GPT Verifier Report — auto-merged with Claude verifier findings
- **Gap handling:** If Codex MCP unavailable → log gap, proceed with Claude verifier only
- **Cost:** record actual token usage per invocation; keep Full-tier QC inside the Work Block budget

GPT Verifier is advisory — it cannot issue BLOCKED. The Claude verifier remains
the authoritative gate. Use `codex-reviewer` only when Control Tower explicitly requests an additional deep review. Skip ONLY for Lite/Standard tier with no security/auth/DB touch.

---

## DB Access Matrix

| DB action mode | Allowed | Forbidden |
|---|---|---|
| `none` | No DB access needed | DB commands, credentials, schema assumptions |
| `local_temp` | temp/local DB smoke, test migrations, disposable data | live DB, real credentials |
| `live_readonly` | Owner-approved sanitized schema/status inspection | writes, DDL, migrations, row dumps |
| `live_migration_apply` | Owner-approved migration files, stop-on-error | arbitrary/destructive SQL |
| `runtime_app` | app writes through reviewed code paths | LLM/manual direct DB mutation |
| `emergency_remediation` | separately approved remediation Work Block | implicit fixes, exploratory writes |

---

## File Write Authority

| Path pattern | Who can write |
|---|---|
| `AGENTS.md`, `.agent/*`, `docs/specs`, `docs/plans`, `docs/tasklist`, `docs/templates/*`, `memory_bank/*` | Control Tower |
| `{{SOURCE_DIRS}}`, `scripts/*` | Scoped Coder (within approved write-set) |
| `docs/reports/*` | Verifier, Scoped Coder (closeout reports) |
| `.env`, secrets, production infra | Owner only |

---

## Agent Roster

| Role | Responsibility |
|---|---|
| Orchestrator | Scope, workflow, delegation, consolidation, approvals, risks, next action |
| Coder | Scoped implementation only after approval |
| Reviewer | Read-only review for defects and risks |
| Verifier | Checks against objective, AC, scope, and verification matrix |
| GPT Critic | External adversarial review of decisions (GPT via MCP) |
| GPT Verifier | External adversarial verification of implementation (GPT via MCP) |
| Codex Reviewer | External adversarial code review (GPT via MCP) |

Full roster with skill assignments: `.agent/ROSTER.md`

---

## Memory Bank Protocol

On every session start, read:

1. `memory_bank/context.md` — current focus, scope, next step
2. `memory_bank/progress.md` — done / in-progress / next
3. `memory_bank/decisions.md` — architecture decisions and rationale

Update memory bank only after implementation has verification evidence.

---

## Key Constraints (all agents)

- No env/secret changes without Owner approval.
- No deploy/infra changes without Owner approval.
- No DB migrations without Owner approval.
- No real client communications without Owner approval.
- No scope expansion beyond the approved task write-set.
- Do not commit secrets, tokens, or production credentials.
- The LLM must never write directly to the database.

---

## SSOT Hierarchy

When sources of truth conflict, resolve in this order:

1. `docs/tasklist/` — active tasks with acceptance criteria
2. `docs/plans/` — approved plans
3. `docs/specs/` — specifications
4. `docs/reports/` — verification and closeout reports
5. `memory_bank/` — context, progress, decisions

---

## External Review / Audit Protocol

External audits, pentest reports, and third-party reviews produce input
artifacts. Their findings must be triaged (confirmed/partial/stale/rejected)
before they produce Work Blocks. The triage is read-only analysis with
file:line evidence. Accepted findings follow the normal SDLC flow.

---

## Skill Index

Skills live in `.agent/skills/<skill-name>/SKILL.md`.
Each skill defines: Triggers · Workflow · Guardrails · Handoff.

See `.agent/README.md` for navigation guide.
