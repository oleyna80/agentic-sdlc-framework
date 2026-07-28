---
schema_version: 1
artifact_type: work_block
artifact_id: wb-007-agent-evaluation-trajectory-assurance
status: completed
owner_role: orchestrator
work_block_id: wb-007
created_at: 2026-07-26
last_verified: 2026-07-26
---

# WB-007 — Agent Evaluation and Trajectory Assurance

## Objective

Add a runtime-neutral evaluation layer that distinguishes deterministic tests,
output evaluation, and observable trajectory evaluation, then binds required
evaluation evidence to Work Block assurance and successful closeout.

## Delivered Result

WB-007 delivered:

- `governance/evaluation.md` as the normative evaluation contract;
- deterministic, output, and observable trajectory evidence classes;
- explicit exclusion of hidden reasoning, private chain-of-thought, and model
  scratchpads from trajectory evidence;
- portable evaluation plan, report, and event templates;
- `scripts/validate-evaluation.py` for generated projects;
- approved plan and frozen-subject revision binding;
- output threshold and evaluator-type enforcement;
- required/prohibited trajectory event enforcement;
- LM-judge restrictions preventing deterministic overrides and authority grants;
- required evaluation binding to successful closeout;
- fail-closed clone/restore defaults;
- positive and adversarial fixtures;
- installation-profile, publication, and Framework Contracts integration.

## Scope Boundary

WB-007 did not deliver:

- a hosted tracing or telemetry backend;
- live provider authentication or runtime event collectors;
- automatic model routing;
- live MCP/plugin/deployment activation;
- LM-judge calibration;
- cross-runtime live evaluation smoke.

These remain follow-up work and were not represented as passing evidence.

## Evidence

- Evaluation plan: `docs/evals/wb-007/plan.json`
- Observable event ledger: `docs/evals/wb-007/events.jsonl`
- Evaluation report: `docs/reports/evaluations/wb-007.json`
- Final review: `docs/reports/reviews/pr-7-final-review.md`
- Drift audit: `docs/reports/drift/wb-007-evaluation-assurance.md`
- Closeout: `docs/reports/closeout/wb-007-agent-evaluation-trajectory-assurance.md`
- Final pre-merge Framework Contracts: run 432, success
- Squash merge commit: `c604f8d2085ca3469de54a525880e3f11eba0fa7`

The GitHub merge commit is historical external evidence. It does not define Work
Block authority or repository lifecycle state.

## Acceptance Result

- [x] Runtime-neutral evaluation terminology and authority boundary defined.
- [x] Deterministic, output, and observable trajectory evidence separated.
- [x] Hidden reasoning/private chain-of-thought excluded.
- [x] Approved plan and frozen subject revision required.
- [x] Output evaluator and threshold enforced.
- [x] Required/prohibited trajectory events enforced.
- [x] LM judge cannot waive deterministic evidence or open authority gates.
- [x] Required evaluation blocks successful closeout until READY.
- [x] Portable templates and validator installed in every profile.
- [x] Blocked default and clone/restore remain fail-closed.
- [x] Positive/adversarial fixtures and publication smoke pass.
- [x] Review, verification, evaluation, drift, and closeout completed.

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Write Gate:** CLOSED
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Evaluation Verdict:** READY
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed
