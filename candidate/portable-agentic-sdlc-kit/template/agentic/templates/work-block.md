---
artifact_type: work_block
work_block_id: {{id}}
status: {{status}}
owner_role: {{owner_role}}
process_level: {{Quick|Standard|High-Risk}}
---
# {{title}}

## Objective

{{objective}}

## Source Contracts

- Owner authority: {{owner_instruction_or_recorded_approval}}
- Governing `AGENTS.md`, specifications, and ADRs: {{source_contracts}}
- Related active Work Block, plan, tasklist, or mission brief: {{related_artifacts}}

## Process-Level Classification

- Selected level: {{Quick|Standard|High-Risk}}
- Dimensions assessed: ambiguity; behavioral and architecture impact; system
  boundaries; authority and approvals; side effects; reversibility/rollback;
  security/data; legal/privacy/financial consequence; verification cost;
  nondeterminism; writers and handoffs.
- Rationale and rejected higher/lower levels: {{classification_rationale}}
- Classify before execution using this fail-closed order: evaluate every
  High-Risk trigger first (any trigger selects High-Risk); select Quick only
  when every Quick eligibility condition is met; otherwise select Standard.
  Any uncertainty, conflict, or elevation trigger defaults or escalates to
  Standard or High-Risk as applicable; revise the Work Block before further
  execution when reclassification is required.
- Mandatory High-Risk triggers: irreversible or difficult-to-reverse side
  effects; production deployment or restart; secrets, credentials, or
  permissions; destructive operations; live data or business-state mutation;
  security or trust-boundary change; consequential external communication or
  transaction; material legal, privacy, or financial consequence; or harmful or
  difficult-to-bound nondeterminism.
- Quick eligibility is cumulative: the objective and acceptance are
  unambiguous; an accepted contract governs the behavior; no material
  architecture, authority, public-interface, data-model, or system-boundary
  decision is required; no High-Risk trigger or Owner Hard Stop applies; side
  effects are local, bounded, and understood; rollback is simple; verification
  is deterministic, inexpensive, and available; no independent Critic,
  Reviewer, or domain assurance is required; one Coder with one bounded
  write-set is sufficient; and no migration, multi-system coordination, or
  consequential external action is involved.

## Scope and Out of Scope

- In scope: {{scope}}
- Out of scope: {{out_of_scope}}
- Exact write-set: {{exact_repository_paths}}

## Roles and Execution Mode

- Orchestrator: {{orchestrator_responsibility}}
- Architect and Critic: {{define_stage_responsibility}}
- Coder: {{single_coder_and_owned_write_set}}
- Reviewer and Verifier: {{assurance_responsibility_and_independence_mode}}
- Execution mode and handoff boundary: {{native|sequential|manual}}

## Side Effects, Risks, and Hard Stops

- Expected side effects and affected boundaries: {{side_effects}}
- Risks and residual risk: {{risks}}
- Hard Stops and escalation conditions: {{hard_stops}}

## Approvals and Rollback

- Required approvals and authority limits: {{approvals}}
- Rollback or recovery plan: {{rollback}}

## Acceptance and Assurance

- Acceptance criteria: {{acceptance_criteria}}
- Required checks and evidence: {{assurance_and_verification}}
- Closeout conditions: {{truthful_closeout_conditions}}

## Write-Gate State

- State: {{OPEN|CLOSED|BLOCKED}}
- Active writer/worktree and overlap control: {{write_gate_and_concurrency_state}}
