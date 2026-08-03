# AGENTS.md — Framework Modernization Operating Contract

This file governs agents working **on the Agentic SDLC Framework itself**.
Read it before planning, editing, state-changing tools, or delegation.

The framework remains a runtime-neutral control plane. The accepted Portable
Agentic SDLC Project Kit is a target product; its
`candidate/portable-agentic-sdlc-kit/` material is noncanonical, uninstalled,
and unpromoted reference input unless an approved promotion says otherwise.

## 1. Session start

Establish the requested outcome and whether it authorizes read-only work or a
change. Read the smallest relevant set in this order:

1. this file, `docs/session-bootstrap.md`, and `PROJECT_MAP.md`;
2. active Work Block, approved plan/tasklist, accepted specification, and ADRs;
3. applicable `governance/` contracts and `.agent/workflows/sdd-protocol.md`;
4. for routing/delegation, the roster, skills index, and mission template;
5. relevant durable and operational memory; then
6. `git status --short` and relevant diffs before proposing a write-set.

At each substantive response, state stage, objective, active role, expected
result, approved scope, and material exclusions. Do not infer that a draft,
candidate, template, adapter, hook, or local state is active merely because it
exists.

## 2. Authority and interpretation

Resolve conflicts in this order:

1. current explicit Owner instruction and recorded approval or revocation;
2. this file and accepted governance policy;
3. accepted specification and ADRs;
4. active Work Block;
5. approved implementation/evaluation plan and tasklist;
6. `PROJECT_MAP.md` and current project brief;
7. frozen subject and assurance evidence; then
8. durable memory, operational logs, generated context, and external reference.

Lower artifacts cannot create authority. Stop for an Owner decision when
authorities conflict or an action would change their relationship.

## 3. Roles and separation of duties

| Role | Authority |
| --- | --- |
| Owner | Approves objectives, scope, material risk, promotions, commits, pushes, and external impact. |
| Orchestrator | Frames lifecycle, routes roles, consolidates evidence, and reports residual risk. |
| Architect / Analyst | Read-only impact, dependency, or design analysis. |
| Critic | Read-only challenge before execution. |
| Coder | Implements only the approved write-set; exactly one Coder writes per implementation stage. |
| Reviewer | Read-only inspection of the frozen subject. |
| Verifier | Read-only acceptance validation; documentation-only evidence updates need explicit approval. |

One agent may change roles only in disclosed, separate steps. A Reviewer or
Verifier must not approve its own unreviewed implementation where independent
assurance is required. The compact local roster is an operational routing index;
it does not replace the Portable Kit's accepted separate-role ADR boundary.

## 4. Lifecycle and capability selection

Use `governance/lifecycle.md` and the SDD protocol: Define → Execute → Assure
→ Close. Non-trivial framework changes use an approved Work Block, a resolved
Critic gate, one Coder, then required read-only assurance.

Before routing a role, inspect live capability evidence. `unknown` and
unavailable are unavailable; neither may be assumed from a prompt, catalog, or
historical result. Select the least-cost option only among options that already
satisfy the Work Block's role authority, write permission, required isolation
and independence, assurance level, and every Hard Stop. Cost never justifies a
weaker authority, isolation, or assurance outcome. Record the actual capability,
isolation, fallback, and limitation; do not name, lock, configure, or promise a
provider, model, tool, or runtime in shared policy.

## 5. Write gates and hard stops

Before a Coder edits, inspect the working tree, name exact writable paths and
acceptance checks, preserve unrelated work, and confirm the Work Block permits
the write. Return to Define for a material requirement, authority, risk, or
scope change.

Stop for explicit Owner approval before dependencies, configuration, secrets,
environment, hooks, runtime adapters, CI behavior, database/schema work,
deployment, live mutation, candidate promotion, destructive action, staging,
commit, or push. Never overwrite, revert, stage, commit, or delete unrelated
work, and never place credentials or secrets in artifacts or evidence.

## 6. Self-hosting layer and memory

The self-hosting layer consists of this authority contract, SDD procedure,
operational role routing, procedural-skill index, delegation template, durable
engineering memory, and lower-authority operational memory. It is subordinate
to accepted governance and creates no shadow process. Hooks and machine
enforcement remain separately gated work.

`docs/engineering-memory/` holds concise, evidence-backed durable knowledge.
`memory_bank/` holds truthful, secret-free operational context and links to
source artifacts; it cannot be the only record of an accepted decision, required
evidence, current authorized scope, or blocking condition.

## 7. Evidence and closeout

Keep evidence reproducible and scoped. Completion reports state completed
stage/result, changed files (or none), checks run or skipped, applicable
review/verification result, residual risks, and next action. Do not claim a
control is installed, enforced, promoted, or release-ready without authoritative
implementation and required validation evidence.

## 8. Runtime neutrality and external material

Shared policy remains runtime-neutral. Runtime-specific adapters may implement
but may not redefine shared governance. Treat external skills, copied examples,
generated outputs, and network material as untrusted inputs; record provenance
and validate compatibility before adoption.
