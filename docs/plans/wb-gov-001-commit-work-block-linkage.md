---
schema_version: 1
artifact_type: work_block
work_block_id: WB-GOV-001
status: completed
governance_profile: Managed
branch: agent/wb-gov-001-commit-work-block-linkage
base_revision: be988807c38543eb90a728fcb4349bc97dd5695a
specification: docs/specs/wb-gov-001-commit-work-block-linkage.md
specification_revision: owner-approved-pr51-correction-r2-2026-09-06
write_gate: BLOCKED
critic_gate: APPROVE
review_gate: READY
verification_verdict: READY
drift_gate: ALIGNED
evaluation_verdict: SKIPPED
closeout_mode: success-closeout
owner_approval: Owner authorized implementation, tests, assurance evidence, commit, and non-force feature-branch push; PR merge and protected/default branch mutation remain out of scope.
---

# WB-GOV-001 — Implementation plan

## Final State

- **Current Stage:** Close
- **Stage State:** completed
- **Write Gate:** BLOCKED
- **Critic Gate:** APPROVE
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Drift Gate:** ALIGNED
- **Evaluation Verdict:** SKIPPED — deterministic contract validation is sufficient.
- **Closeout Mode:** success-closeout
- **Task Status:** completed

## Stage and objective

Execute the approved runtime-neutral commit trailer contract in the generated
framework scaffold, preserve default bootstrap behavior, make hook checks strictly
read-only, and prove the result and known cooperative enforcement limitations
with disposable repositories and existing framework contracts.

## Bounded write-set

`template/.githooks/commit-msg`, `template/scripts/bootstrap.sh`,
`bootstrap/profiles.json`, `scripts/test-commit-work-block-linkage.sh`,
`.github/workflows/framework-contracts.yml`, the smallest required validator or
documentation integration paths, and this WB's `docs/{specs,plans,tasklist,reports}`
artifacts. No runtime provider or application paths are authorized.

## Design decisions

1. The hook uses `git rev-parse`, `git interpret-trailers`, and Python JSON
   parsing available in the generated framework contract; it resolves the
   repository root and never depends on Codex, Claude, OpenCode, or branch names.
2. Bootstrap flags are explicit. No-argument health checks perform no Git config
   write. Install uses `git config --local`; check is strictly read-only and exits
   immediately without modifying files or configuration.
3. The fixture suite uses isolated temporary repositories/configuration and real
   commits, verifying ordinary rejection, exact-trailer success, `--no-verify`
   bypass, and documented commit-producing limitations (such as `git cherry-pick`
   and `git revert`); it does not activate this framework checkout.

## Assurance and stops

Review and Verification will inspect the frozen cumulative diff and execute the
fixture/profile/framework matrix. Drift will compare the implementation against
this specification and current baseline. Evaluation is not required: behavior is
deterministic contract validation. Close only after all required evidence is
READY and release/publication/traceability checks pass. Stop for scope expansion,
schema change, secret/config risk, or any reserved-roadmap impact.
