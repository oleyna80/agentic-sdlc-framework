---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-002-portable-candidate-content
work_block_id: WB-CORE-002
status: completed
owner_role: orchestrator
created_at: 2026-07-31
base_revision: 6f8ea535f7773c96588326e8cda689a57a804070
branch: agent/portable-kit-candidate-content
process_level: Standard
last_verified: 2026-07-31
---

# WB-CORE-002 — Portable Candidate Content

## Objective and authority

Create a complete, provider-neutral, draft candidate payload for the accepted
portable-kit target. Owner instruction dated 2026-07-31 authorizes opening and
executing WB-CORE-002 only. It authorizes no commit, push, merge, promotion,
archival, or later Work Block.

Accepted sources: `docs/specs/portable-agentic-sdlc-project-kit.md`,
`docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md`, and
`docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md`.

## Exact write-set

This Work Block may modify `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, this plan,
and only these candidate paths:

```text
candidate/portable-agentic-sdlc-kit/CANDIDATE.md
candidate/portable-agentic-sdlc-kit/template/README.md
candidate/portable-agentic-sdlc-kit/template/AGENTS.md
candidate/portable-agentic-sdlc-kit/template/PROJECT_BRIEF.md
candidate/portable-agentic-sdlc-kit/template/PROJECT_MAP.md
candidate/portable-agentic-sdlc-kit/template/FILE_REGISTRY.yml
candidate/portable-agentic-sdlc-kit/template/.agentic-local/.gitignore
candidate/portable-agentic-sdlc-kit/template/agentic/README.md
candidate/portable-agentic-sdlc-kit/template/agentic/roles/README.md
candidate/portable-agentic-sdlc-kit/template/agentic/roles/orchestrator.md
candidate/portable-agentic-sdlc-kit/template/agentic/roles/architect.md
candidate/portable-agentic-sdlc-kit/template/agentic/roles/critic.md
candidate/portable-agentic-sdlc-kit/template/agentic/roles/coder.md
candidate/portable-agentic-sdlc-kit/template/agentic/roles/reviewer.md
candidate/portable-agentic-sdlc-kit/template/agentic/roles/verifier.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/README.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/technical-discovery/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/architecture-discovery/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/specification/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/implementation-planning/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/task-decomposition/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/systematic-debugging/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/memory-bank-manager/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/ssot-sync-closeout/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/verification-before-completion/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/README.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/work-block.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/technical-discovery.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/architecture-brief.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/specification.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/architecture-decision.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/implementation-plan.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/tasklist.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/mission-brief.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/handoff.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/critic-report.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/reviewer-report.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/verification-report.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/evaluation-plan.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/evaluation-report.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/drift-report.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/closeout-report.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/context-snapshot.md
candidate/portable-agentic-sdlc-kit/template/docs/README.md
candidate/portable-agentic-sdlc-kit/template/docs/discovery/README.md
candidate/portable-agentic-sdlc-kit/template/docs/specs/README.md
candidate/portable-agentic-sdlc-kit/template/docs/architecture/README.md
candidate/portable-agentic-sdlc-kit/template/docs/architecture/decisions/README.md
candidate/portable-agentic-sdlc-kit/template/docs/work-blocks/README.md
candidate/portable-agentic-sdlc-kit/template/docs/plans/README.md
candidate/portable-agentic-sdlc-kit/template/docs/tasklists/README.md
candidate/portable-agentic-sdlc-kit/template/docs/handoffs/README.md
candidate/portable-agentic-sdlc-kit/template/docs/reports/README.md
candidate/portable-agentic-sdlc-kit/template/docs/reports/reviews/README.md
candidate/portable-agentic-sdlc-kit/template/docs/reports/verification/README.md
candidate/portable-agentic-sdlc-kit/template/docs/reports/evaluations/README.md
candidate/portable-agentic-sdlc-kit/template/docs/reports/drift/README.md
candidate/portable-agentic-sdlc-kit/template/docs/reports/closeout/README.md
candidate/portable-agentic-sdlc-kit/template/memory_bank/context.md
candidate/portable-agentic-sdlc-kit/template/memory_bank/progress.md
candidate/portable-agentic-sdlc-kit/template/memory_bank/decisions.md
candidate/portable-agentic-sdlc-kit/template/memory_bank/orchestrator-log.md
candidate/portable-agentic-sdlc-kit/template/memory_bank/review-log.md
candidate/portable-agentic-sdlc-kit/template/memory_bank/snapshots/README.md
candidate/portable-agentic-sdlc-kit/tools/README.md
candidate/portable-agentic-sdlc-kit/tests/README.md
```

Additional candidate paths require Work Block revision. Future evidence paths,
not created in this stage, are `docs/reports/reviews/wb-core-002-critic-review.md`,
`docs/reports/reviews/wb-core-002-candidate-review.md`,
`docs/reports/verification/wb-core-002-candidate-verification.md`,
`docs/reports/drift/wb-core-002-portable-candidate-content.md`, and
`docs/reports/closeout/wb-core-002-portable-candidate-content.md`.

## Hard stops and exclusions

Stop for any installer, manifest, assembly, executable tool/test, synthetic
fixture/pilot, runtime/provider integration, configuration, model, hook, MCP,
plugin, promotion, canonical-path/current-architecture change, commit, or push.
Do not alter root `AGENTS.md`, `bootstrap/`, `template/`, `runtimes/`,
`integrations/`, `.github/`, `governance/`, scripts, existing skills, specs, or
ADRs. Root `AGENTS.md` is absent from this subject; this residual risk requires
independent review.

## Staged plan and verification

1. Author the isolated candidate content and future-installed contracts.
2. Reconcile the sole active Work Block in map and registry while keeping
   `runtime_neutral_control_plane` operational and the accepted target unpromoted.
3. Run diff, inventory, forbidden-identifier, release-state, and status checks.
4. Obtain Critic, Reviewer, Verifier, drift, and closeout evidence in later
   approved stages.

## Review remediation

The frozen subject `8578dd6c` received `CHANGES_REQUIRED` / `NOT_READY` because
candidate entrypoint wording and reusable role/template contracts were
insufficiently explicit. This remediation remains inside the existing literal
allowlist: every candidate entrypoint must clearly state it is **draft**,
**noncanonical**, **uninstalled**, **unpromoted**, and has **no current
authority**. Six role contracts must add provider-neutral Procedure and Handoff
sections without changing their write rights or boundaries. Static templates must
cover their lifecycle schemas. This changed normative subject requires renewed
Reviewer and Verifier assurance; no evidence report is created in this stage.

## Acceptance criteria composition matrix

| Component | Candidate paths |
|---|---|
| candidate boundary | `CANDIDATE.md`, `tools/README.md`, `tests/README.md` |
| root seed and local boundary | `template/{README.md,AGENTS.md,PROJECT_BRIEF.md,PROJECT_MAP.md,FILE_REGISTRY.yml,.agentic-local/.gitignore}` |
| lifecycle and roles | `template/agentic/README.md`, `template/agentic/roles/**` |
| procedures | `template/agentic/skills/README.md`, nine `*/SKILL.md` files |
| reusable artifacts | `template/agentic/templates/**` |
| documentation evidence layout | `template/docs/**` |
| committed memory seed | `template/memory_bank/**` |

AC: every matrix path exists; all entrypoints state draft/noncanonical/uninstalled/
unpromoted and no current-repository authority; only future-installed template
`AGENTS.md` is root authority; exactly nine skills exist; local state is ignored
except its `.gitignore`; and SSOT declares this sole active Work Block without
changing operational architecture or individually registering assurance reports.

Residual risk: no installer, synthetic execution, pilot, or independent assurance
exists yet; root `AGENTS.md` is missing from this repository subject.

## Assurance and Closeout Record

Historical Critic Stage 0 and pre-execution verdict: `APPROVE_WITH_CHANGES`.
Its required literal allowlist, composition matrix, local-state boundary, and
SSOT transition were all addressed before execution.

Final Reviewer verdict: `READY`, zero findings after two remediation cycles, for
the exact frozen candidate subject identified by base revision
`6f8ea535f7773c96588326e8cda689a57a804070` and manifest
`52ffca998dbb371bfb5b707d9ab310af4330d5ea126f1c5ff6dd913ad587e5bb`.
Earlier review subjects are historical evidence only and do not alter this verdict.

Final Verifier verdict: `READY` for the same exact frozen subject. It passed
allowlist/inventory/isolation/status/roles/templates/local-boundary/security/SSOT,
release-state fixtures, `test-sdd`, and governance validation. Publication
validation was skipped as inapplicable because its repository-wide public-marker
scan excluded Owner-preexisting untracked `PROJECT_BRIEF.md`.

The evaluation verdict is `SKIPPED` because deterministic static candidate
documents, independent Reviewer/Verifier assurance, and contract checks are
sufficient for WB-CORE-002. Installer, synthetic, and pilot tests belong to later
Work Blocks and are not claimed here.

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Write Gate:** CLOSED
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Evaluation Verdict:** SKIPPED — deterministic static candidate documents, independent Reviewer/Verifier assurance, and contract checks are sufficient for WB-CORE-002
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed

WB-CORE-002 completed only the static candidate-content lifecycle. The current
operational architecture remains `runtime_neutral_control_plane`; the accepted
portable target remains unpromoted, uninstalled, and noncanonical. No installer,
synthetic dry run, pilot, promotion, archival, commit, push, or VCS-history
persistence is claimed. Root `AGENTS.md` remains absent from this repository
subject. WB-CORE-003 through WB-CORE-006 remain future, separately gated work.
