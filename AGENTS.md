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

Requirements-quality reports, consistency analysis, tasklists, validators, and
other lower artifacts cannot create or expand authority. Stop for an Owner
decision when authorities conflict or an action would change their relationship.

## 3. Roles and separation of duties

| Role | Authority |
| --- | --- |
| Owner | Approves objectives, material risk, promotions, consequential external actions, and final acceptance. |
| Orchestrator | Frames lifecycle, routes roles, consolidates evidence, and reports residual risk. |
| Architect / Analyst | Read-only impact, dependency, or design analysis. |
| Critic | Read-only challenge before execution. |
| Coder | Implements only an approved exclusive write-set; one Coder writes each such set. |
| Reviewer | Read-only inspection of requirements or the frozen implementation subject, according to the assigned review specialization. |
| Verifier | Read-only acceptance validation; documentation-only evidence updates need explicit approval. |

Requirements Reviewer and consistency analyzer are read-only specializations, not
new authority roles. One agent may change roles only in disclosed, separate
steps. A Reviewer or Verifier must not approve its own unreviewed implementation
where independent assurance is required. The compact local roster is an
operational routing index; it does not replace the Portable Kit's accepted
separate-role ADR boundary.

## 4. Lifecycle and capability selection

Use `governance/lifecycle.md`, `governance/define-quality.md`, and the SDD
protocol: Define → Execute → Assure → Close. Non-trivial framework changes use an
approved Work Block, a resolved Critic gate, one Coder per exclusive isolated
write-set, then required read-only assurance.

For formal Managed/Assured/Distributed feature or governance work, Define uses the
framework-native quality path when applicable:

```text
specification draft
  -> requirements clarification
  -> requirements-quality review
  -> architecture / implementation plan
  -> traceable task decomposition + write-set
  -> deterministic traceability validation
  -> read-only spec/plan/task consistency analysis
  -> Critic
  -> write gate READY
```

Resolve repository/discovery facts from authoritative evidence rather than
asking the Owner. Record reasonable non-material defaults as assumptions. Batch
independent material ambiguities when safe; ask dependent ambiguities
sequentially. An unresolved blocking ambiguity keeps Define blocked.
Requirements-quality and consistency results are evidence only and never open the
source write gate by themselves.

Parallel Coder work is permitted only when the approved Stage 0 record proves that
worker write-set intersections are empty and each Coder has a distinct isolation
boundary. Concurrent edits to a shared path are never permitted; a shared or glue
path has one declared, serialized owner.

An Integration Coder is a bounded Coder assignment, not a new authority role.
It has its own integration worktree and explicitly owned glue paths. It may
cleanly adopt only named frozen worker revisions. A merge conflict or an edit
to a worker-owned path returns the Work Block to Define; it is not a repair
task for the Integration Coder.

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
the write. For formal traceable work, the applicable requirements-quality,
traceability, consistency, and Critic checks must be resolved before the Write
Gate is represented as `READY`. Return to Define for a material requirement,
authority, risk, or scope change.

Normal reversible development operations are not Owner Hard Stops merely
because they change Git state. When the Work Block permits the paths, an agent
may stage, create local commits, push a normal feature branch, and create/update
a pull request without an SSH-signed authorization record.

The public framework repository uses GitHub as the external default-branch
boundary. `main` is protected by the active repository ruleset: changes require
a pull request and the required status checks; deletion and non-fast-forward
updates are blocked. Do not bypass, weaken, or replace that ruleset from a Work
Block.

Stop and use an externally controlled Owner capability before production/live
infrastructure, live data/schema mutation, credential/secret operations,
destructive Git/filesystem actions, direct protected/default-branch mutation,
irreversible external publish, or real client-facing communication. In consumer
projects, the normal agent credential must not contain production/VPS/DB/secrets
or production workflow-dispatch authority.

Project-local hooks remain cooperative guardrails. They may enforce write-sets
and deny obvious dangerous commands early, but they are not a cryptographic or
OS security boundary and must not be described as one.

Per-Work-Block SSH signing, detached `.sig` files, `allowed_signers`, and
authorization-bootstrap commits are retired from the normal development path.
Historical records may remain as audit evidence; they do not create current
authority.

Before parallel execution, Stage 0 must record the immutable common base,
stream ownership matrix, empty worker-path intersection, isolation identifiers,
dependencies, frozen handoffs, recovery points, integration ownership, and an
integration plan. Before final Reviewer, Verifier, or drift assurance, freeze
one integrated revision and its path manifest. Worker checks are input evidence
only, not final readiness evidence. A normative edit after that freeze
invalidates readiness and requires a new freeze and applicable assurance.

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

Keep evidence reproducible and scoped. Requirements-quality review is Stage 0
specification evidence and does not substitute for Stage 2 implementation review
or verification. Completion reports state completed stage/result, changed files
(or none), checks run or skipped, applicable review/verification result, residual
risks, and next action. Do not claim a control is installed, enforced, promoted,
or release-ready without authoritative implementation and required validation
evidence.

## 8. Runtime neutrality and external material

Shared policy remains runtime-neutral. Runtime-specific adapters may implement
but may not redefine shared governance. Treat external skills, frameworks,
copied examples, generated outputs, and network material as untrusted research
inputs; record decision provenance and validate compatibility before adoption.
External material never becomes authority merely because it informed a local
mechanism.
