---
schema_version: 1
artifact_type: verification_report
artifact_id: wb-core-001-preliminary-verification
work_block_id: WB-CORE-001
verification_stage: preliminary
verified_normative_subject: 674e992548c0474b79bbf261ee7fbceae8eaff4a
inspected_pr_head: 51aff172018c7fb5b077751799cc324dd185daa5
verdict: NOT_READY
created_at: 2026-07-30
---

# Preliminary Verification — WB-CORE-001

## 1. Subject

Verified normative subject:

```text
674e992548c0474b79bbf261ee7fbceae8eaff4a
```

Resolved starting PR head:

```text
51aff172018c7fb5b077751799cc324dd185daa5
```

The starting head matched the expected value. The normative subject exists, is an
ancestor of the starting head, and is followed by two commits that add only:

```text
docs/reports/reviews/wb-core-001-pr-review-4.md
docs/reports/reviews/wb-core-001-pr-review-ready.md
```

No applicable normative file changed after the verified subject. Mutable PR-body
content was not treated as authority.

## 2. Scope

Authoritative files inspected at the exact subject:

```text
docs/specs/portable-agentic-sdlc-project-kit.md
docs/architecture/decisions/2026-07-29-portable-kit-product-boundary.md
docs/architecture/decisions/2026-07-29-portable-kit-roles-memory-installation.md
docs/plans/wb-core-001-normative-architecture.md
PROJECT_MAP.md
FILE_REGISTRY.yml
```

All listed Critic and Reviewer reports were used only as evidence. The complete
PR changed-file inventory was checked for scope integrity.

## 3. Procedures

1. Resolved PR #12 state, branch, merge state, and exact head.
2. Compared the normative subject with the starting head.
3. Inspected all authoritative files at the exact subject.
4. Resolved the three immutable evidence revisions.
5. Inspected final Reviewer identity and verdict.
6. Evaluated VER-001 through VER-020 independently.
7. Inspected workflow runs, jobs, parsing, governance, release-state, and
   publication steps.
8. Performed no repair or normative modification.

## 4. Evidence Identity

| Evidence | Revision | Result |
|---|---|---|
| Current framework baseline | `0fce7389d27690482e910e942a1f3138c2fef123` | revision exists in the framework repository |
| Historical practical baseline | `0c632db0b0444e556251c384f6254141c9df59bc` | revision exists in the framework repository |
| Superpowers reference | `obra/superpowers@44c9b2d6e889982ac18c27d05a19fefe335194e1` | revision exists in the recorded external repository |

The normative documents represent these revisions as evidence/source revisions,
not as portable runtime authority.

| Subject/head | Workflow | Run | Conclusion |
|---|---|---:|---|
| `674e992548c0474b79bbf261ee7fbceae8eaff4a` | Framework Contracts | 744 | `success` |
| `674e992548c0474b79bbf261ee7fbceae8eaff4a` | Release State Contract | 323 | `success` |
| `9889be4a5dcd2c4b07844ac8e9ba2c3cf81ad72d` | Framework Contracts | 746 | `success` |
| `9889be4a5dcd2c4b07844ac8e9ba2c3cf81ad72d` | Release State Contract | 325 | `success` |
| `51aff172018c7fb5b077751799cc324dd185daa5` | Framework Contracts | 748 | `success` |
| `51aff172018c7fb5b077751799cc324dd185daa5` | Release State Contract | 327 | `success` |

Run 748 completed syntax/configuration parsing, runtime-neutral contracts,
governance, release-state, and publication validation. Run 327 completed
validator syntax, adversarial fixtures, and repository release-state validation.

## 5. Verification Matrix

### VER-001 — Exact subject identity

- **Expected result:** exact subject exists, is the last applicable normative
  commit, and later commits through the starting head are evidence-only.
- **Procedure:** resolved the PR head and compared `674e992...` to `51aff172...`.
- **Exact evidence:** comparison reports two later commits and only the two
  review-report paths listed in section 1.
- **Actual result:** no post-subject normative change exists.
- **Status:** `PASS`
- **Limitations:** semantic classification still requires path/content inspection.

### VER-002 — Approved product boundary

- **Expected result:** complete project kit, not a skills-only library or runtime
  control plane.
- **Procedure:** inspected specification sections 1–2 and the product-boundary ADR.
- **Exact evidence:** entry contract, lifecycle, process levels, roles, skills,
  Work Blocks, specifications, ADRs, plans, tasks, mission briefs, handoffs,
  memory, assurance, closeout, and installer are enumerated.
- **Actual result:** required boundary and rejected reductions are explicit.
- **Status:** `PASS`
- **Limitations:** candidate content is intentionally not implemented.

### VER-003 — Runtime-neutrality boundary

- **Expected result:** no ownership of provider/runtime concerns; current operations
  remain legacy operational architecture during migration.
- **Procedure:** inspected specification exclusions, both ADRs, map, and registry.
- **Exact evidence:** provider agents/directories, model routing, hooks,
  permissions, MCP, plugins, negotiation, snapshots, profiles, queues, daemons,
  services, and duplicated mirrors are outside the portable core; current runtime
  assets remain classified under `runtime_neutral_control_plane`.
- **Actual result:** target non-ownership and current-operation preservation agree.
- **Status:** `PASS`
- **Limitations:** legacy assets remain until authorized promotion/archive.

### VER-004 — Source-of-truth hierarchy

- **Expected result:** exact precedence and Work Block non-expansion rules.
- **Procedure:** compared specification section 4, map Authority Order, and registry
  `artifact_authority_order`.
- **Exact evidence:** all ten levels occur in required order; plans and mission
  briefs cannot expand the active Work Block.
- **Actual result:** hierarchy matches.
- **Status:** `PASS`
- **Limitations:** no material ambiguity found.

### VER-005 — Roles and execution modes

- **Expected result:** six separate roles, shared root authority, three execution
  modes, disclosed non-independence, and bounded Coder authority.
- **Procedure:** inspected specification sections 7–9 and roles/memory ADR.
- **Exact evidence:** six target role files are named; root `AGENTS.md` remains
  canonical; native subagents, sequential passes, and manual handoffs are
  supported; sequential reuse is non-independent; Coder changes one approved
  write-set while requirements, review, and verification are assigned elsewhere.
- **Actual result:** required separation is specified.
- **Status:** `PASS`
- **Limitations:** role files are not yet implemented.

### VER-006 — Core skill inventory

- **Expected result:** exactly nine named skills, explicit historical-mechanism
  disposition, and runtime/provider mechanisms outside core.
- **Procedure:** inspected specification sections 12 and 20–23, ADRs, and Critic
  resolution against the authoritative subject.
- **Exact evidence:** exactly nine required skills are listed and runtime/provider
  mechanisms are excluded. No disposition table or equivalent per-mechanism
  disposition for relevant current and historical mechanisms exists in the
  normative subject. The Critic evidence says such a table exists, but that claim
  is not present in the authoritative specification.
- **Actual result:** inventory and runtime exclusion pass; historical disposition
  is missing.
- **Status:** `FAIL`
- **Limitations:** a generic optional-extension list is not an explicit historical
  disposition.

### VER-007 — Project memory contract

- **Expected result:** canonical tree, ownership, update triggers, secret/transcript
  rules, ignored scratch, and no local-only accepted decisions/evidence.
- **Procedure:** inspected specification section 14 and roles/memory ADR.
- **Exact evidence:** all required paths exist; `.agentic-local/` is ignored and
  noncanonical; transcripts/tool output are excluded; local scratch cannot hold
  the only accepted decision or required evidence.
- **Actual result:** location/content boundaries pass, but memory ownership and
  update triggers are not normatively assigned.
- **Status:** `FAIL`
- **Limitations:** current or historical conventions cannot replace the missing
  portable contract.

### VER-008 — Process levels

- **Expected result:** risk, ambiguity, side effects, and reversibility determine
  Quick/Standard/High-Risk rather than file count; artifacts, assurance, Owner
  boundaries, and fail-closed degradation are operational.
- **Procedure:** inspected Design Principles, specification section 6, Work Block
  decisions, and CRIT-006 against the exact subject.
- **Exact evidence:** risk/ambiguity principle, artifact requirements, High-Risk
  triggers, approvals, and fail-closed assurance exist. Reversibility is not a
  classification dimension; file-count selection is not expressly rejected; the
  claimed strict Quick eligibility and Standard escalation rules are absent.
- **Actual result:** process levels exist, but selection semantics are incomplete.
- **Status:** `FAIL`
- **Limitations:** High-Risk triggers only partially cover side effects.

### VER-009 — Work Block and concurrency rules

- **Expected result:** one write Work Block per tree, read-only coexistence,
  isolated parallel writers, one Coder per write-set, integration plan for overlap.
- **Procedure:** inspected specification section 9 and roles/memory ADR.
- **Exact evidence:** every required concurrency rule is explicit.
- **Actual result:** rules match.
- **Status:** `PASS`
- **Limitations:** worktree automation is outside core.

### VER-010 — Reviewer and Verifier verdict semantics

- **Expected result:** exact vocabularies and final Reviewer `READY` against
  `674e992...`.
- **Procedure:** inspected specification sections 15–16, ADRs, registry, and final
  Reviewer report.
- **Exact evidence:** all vocabularies match; final report records `READY` and the
  exact normative subject.
- **Actual result:** semantics and Reviewer identity pass.
- **Status:** `PASS`
- **Limitations:** Reviewer readiness does not determine Verifier readiness.

### VER-011 — Normative subject and evidence-only commits

- **Expected result:** exact-SHA assurance, report-following semantics, normative
  invalidation, resulting-head CI, and no self-reference.
- **Procedure:** inspected specification section 10, ADRs, registry, and commit
  chain.
- **Exact evidence:** all required rules are explicit; later commits are report-only.
- **Actual result:** contract and history match.
- **Status:** `PASS`
- **Limitations:** evidence-only status depends on exact semantic scope.

### VER-012 — Assurance navigation boundary

- **Expected result:** no mutable assurance mirrors; directory/frontmatter
  discovery; static evidence classes; indexing grants no authority.
- **Procedure:** inspected specification, map, and registry assurance sections.
- **Exact evidence:** mutable verdict/SHA/finding/pointer state is prohibited; four
  evidence classes are registered; reports need no per-report navigation update.
- **Actual result:** boundary is consistent.
- **Status:** `PASS`
- **Limitations:** consumers must enumerate reports and parse frontmatter.

### VER-013 — Current operational architecture preservation

- **Expected result:** current runtime-neutral architecture, proposed target,
  active in-progress WB, restored contracts, and no promotion/archive.
- **Procedure:** inspected map, registry, Work Block, and subject diff.
- **Exact evidence:** `architecture: runtime_neutral_control_plane`, target
  `status: proposed`, active WB and `in_progress`, required static rules/classes,
  and restored relationships are present.
- **Actual result:** current operations are preserved.
- **Status:** `PASS`
- **Limitations:** coexistence remains until WB-CORE-006.

### VER-014 — Candidate and installer contract

- **Expected result:** candidate tree and plan/apply interface with collision,
  traversal, symlink, staging, and no-silent-overwrite requirements.
- **Procedure:** inspected specification sections 19 and 21 and roles/memory ADR.
- **Exact evidence:** candidate tree, interface, collision classes, root/path
  safety, symlink checks, staging, revalidation, collision refusal, and no
  overwrite/delete exist. Path traversal is not named or assigned a precise
  rejection rule.
- **Actual result:** most safety clauses pass; explicit traversal protection is
  absent.
- **Status:** `FAIL`
- **Limitations:** generic “path safety” cannot prove the exact criterion; tests are
  deferred to WB-CORE-003.

### VER-015 — Migration sequence

- **Expected result:** six bounded Work Blocks and dependency preventing candidate
  implementation before WB-CORE-001 acceptance.
- **Procedure:** inspected specification section 22 and Work Block scope.
- **Exact evidence:** WB-CORE-001 through WB-CORE-006 are enumerated; later blocks
  depend on predecessor accepted/verified results; implementation is excluded now.
- **Actual result:** sequence and dependency match.
- **Status:** `PASS`
- **Limitations:** later Work Blocks are not yet detailed active plans.

### VER-016 — Git and Owner authority

- **Expected result:** Owner approval for status finalization, protected/default
  integration, deployment, secrets, destructive/live/consequential actions, and
  material scope/architecture expansion.
- **Procedure:** inspected specification sections 10 and 18, Work Block authority,
  ADR transitions, and evidence reports.
- **Exact evidence:** all gates are explicit; feature-branch evidence commits grant
  no merge authority.
- **Actual result:** no restricted permission is granted.
- **Status:** `PASS`
- **Limitations:** hosting-platform permissions remain external state.

### VER-017 — Acceptance-state transition

- **Expected result:** preliminary assurance, Owner authorization, status-only
  subject, final assurance, evidence-only reports, resulting-head CI, separate
  merge approval.
- **Procedure:** compared specification and ADR diagrams with registry sequence.
- **Exact evidence:** sequence matches; proposed documents are not accepted by PR,
  review, CI, or merge presence.
- **Actual result:** transition is non-self-referential and Owner-controlled.
- **Status:** `PASS`
- **Limitations:** later gates have not occurred.

### VER-018 — Scope integrity

- **Expected result:** only approved normative/evidence paths; no implementation or
  operational mutation.
- **Procedure:** inspected all 12 starting-head PR filenames and post-subject diff.
- **Exact evidence:** only six authoritative documents and six review reports were
  present; no candidate, installer, role/skill implementation, migration script,
  runtime/provider configuration, deployment, or repository-setting path exists.
- **Actual result:** scope is documentation and assurance only.
- **Status:** `PASS`
- **Limitations:** semantic scope was checked independently of PR-body claims.

### VER-019 — Structural checks

- **Expected result:** stated workflows succeed and structure, frontmatter, paths,
  active WB, authority language, placeholders, and evidence boundaries agree.
- **Procedure:** resolved runs 744/323, 746/325, and 748/327; inspected run jobs and
  authoritative files.
- **Exact evidence:** all six runs succeeded; parsing, contract, governance,
  release-state, publication, and adversarial fixture steps succeeded.
- **Actual result:** structural contracts pass.
- **Status:** `PASS`
- **Limitations:** structural success does not prove semantic completeness of the
  failed criteria.

### VER-020 — WB-CORE-001 preliminary acceptance

- **Expected result:** every currently applicable preliminary criterion passes;
  later finalization, accepted-status, final assurance, closeout, and merge gates
  may remain pending.
- **Procedure:** evaluated all checked acceptance statements against VER-001 through
  VER-019.
- **Exact evidence:** later-stage gates are correctly pending, but VER-006,
  VER-007, VER-008, and VER-014 fail.
- **Actual result:** preliminary acceptance is not demonstrated.
- **Status:** `FAIL`
- **Limitations:** this does not reject the architecture direction; it requires
  normative correction and renewed assurance.

## 6. Failed or Blocked Criteria

Failed:

- `VER-006` — no explicit historical-mechanism disposition.
- `VER-007` — no ownership/update-trigger contract for project memory.
- `VER-008` — incomplete process-level selection contract.
- `VER-014` — traversal protection is not explicit.
- `VER-020` — preliminary acceptance fails because applicable criteria fail.

Blocked: none.

Not applicable: none.

## 7. Limitations

- External repositories were not re-evaluated in full; only immutable revision
  identity and authority representation were checked.
- A separate local clone was unavailable in the execution environment. Exact
  files, commits, comparisons, workflow runs, jobs, and PR state were retrieved
  through the connected repository interface; required coverage remained
  available.
- Candidate, installer, role, skill, test, and migration behavior cannot be run
  because WB-CORE-001 intentionally defines architecture only.
- Structural workflow success is not proof that every semantic clause exists.

## 8. Residual Risks

- The final Reviewer `READY` and this Verifier `NOT_READY` legitimately differ
  because the roles apply different criteria. The historical Reviewer verdict
  must remain unchanged, but status finalization should not proceed.
- Missing historical dispositions can cause scope drift or silent loss of useful
  mechanisms.
- Missing memory ownership/update triggers can produce stale or conflicting
  committed memory.
- Under-specified process-level selection can permit inconsistent assurance and
  file-count heuristics.
- Generic path safety can produce divergent traversal behavior in installer
  implementations.

## 9. Verdict

```text
NOT_READY
```

Fresh evidence demonstrates that four currently applicable normative criteria are
not fully satisfied. No authority, access, environment, or dependency issue
prevented a reliable verdict.

This verdict does not accept the proposed documents, authorize status
finalization, complete WB-CORE-001, authorize promotion, or authorize merge.

## 10. Next Gates

1. Correct the normative subject under an explicitly authorized write-set:
   - add explicit historical-mechanism dispositions;
   - define memory ownership and update triggers;
   - define process-level selection using risk, ambiguity, side effects, and
     reversibility, expressly excluding file-count selection and defining Quick
     eligibility and Standard escalation;
   - define explicit path-traversal rejection for the installer contract.
2. Obtain a new Reviewer assessment against the corrected normative subject.
3. Run a new preliminary Verifier assessment against that same subject.
4. After preliminary applicable assurance is `READY`, obtain separate Owner
   authorization for accepted-status finalization.
5. Create the status-only normative commit and perform final applicable assurance.
6. Commit evidence-only reports and obtain green CI on the resulting PR head.
7. Complete closeout and obtain separate explicit Owner merge approval.
