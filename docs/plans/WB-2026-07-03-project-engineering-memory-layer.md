# Work Block: Project Engineering Memory Layer

> Defines a durable, agent-neutral engineering memory layer for projects using
> the Agentic SDLC Framework.

## Meta
- **Work Block ID:** WB-2026-07-03-project-engineering-memory-layer
- **Date:** 2026-07-03
- **Owner:** azur
- **Execution Mode:** end-to-end autonomous after Owner approval
- **Side-Effect Class:** local-docs / public-repo
- **DB Action Mode:** none
- **Verification Tier:** standard

## Lifecycle State
- **Current Stage:** Stage 5
- **Stage Execution State:** complete
- **Write Gate:** APPROVED
- **Owner Approval Evidence:** Owner confirmed start in chat.
- **Critic Gate:** PASSED_AFTER_FIXES
- **Verification Gate:** PASSED
- **Verification Verdict:** PASSED
- **Stage 3 Mode:** single-writer Codex documentation implementation

## Objective
Add a clear Engineering Memory layer so any future agent joining a project can
understand durable engineering decisions, invariants, temporary decisions,
source-of-truth chains, and reproducibility evidence without relying on hidden
conversation history or runtime-specific memory.

The layer must work across the current agent stack:

- Codex
- Claude Code
- OpenCode
- Antigravity

It must remain LLM-neutral for GPT, Claude, Gemini, Deepseek, and future GLM-like
models by using plain Markdown/YAML conventions and stable repository paths.

## Expected Final Result
The framework has a documented and scaffolded Project Engineering Memory
contract:

- `docs/` is clearly the durable, repo-controlled location for project
  engineering memory.
- `memory_bank/` is clearly operational context/cache/log state, not the
  highest source of truth.
- Generated projects include a minimal `docs/engineering-memory/` starter that
  any agent can read during session bootstrap.
- Work Block closeout includes a small conditional Engineering Memory gate:
  update durable memory only when the Work Block changes future engineering
  behavior.
- Session bootstrap, SSOT hierarchy, project map, registry, setup docs, and
  templates agree on the same authority model.
- Publication validation passes, and the repository is clean or remaining dirty
  files are explicitly documented.

## Done Criteria
- [x] SSOT boundary between `docs/` and `memory_bank/` is unambiguous.
- [x] Engineering Memory contract exists in framework docs.
- [x] Generated project template includes minimal Engineering Memory files.
- [x] Work Block template includes conditional Engineering Memory closeout gate.
- [x] Session bootstrap tells joining agents when to read Engineering Memory.
- [x] `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, `README.md`, `SETUP.md`, and profile
      docs are updated only where affected.
- [x] Validation/search checks show no contradictory authority wording.
- [x] Critic/reviewer confirms the layer is useful without becoming process bloat.

## Preflight State
- **Git baseline:** dirty.
- **Observed command:** `git status --short --branch`
- **Pre-existing dirty files:**
  - `FILE_REGISTRY.yml`
  - `PROJECT_MAP.md`
  - `framework/knowledge/README.md`
  - `framework/knowledge/opencode-runtime.md` (untracked)
- **Untracked local artifacts:** `framework/knowledge/opencode-runtime.md`
- **Proceed rule:** these OpenCode-related edits must be preserved. Because this
  Work Block will likely touch `FILE_REGISTRY.yml` and `PROJECT_MAP.md`, the
  implementation stage must inspect existing diffs first and extend them
  deliberately instead of overwriting or separating them by accident.

## Dependency Check
### Must Resolve Before Start
- Owner approval for this Work Block and write-set.
- Decision on whether the current OpenCode dirty files are included in this
  Work Block commit or closed in a separate commit first.

### Can Resolve During Work
- Exact naming inside `docs/engineering-memory/`.
- Whether `template/project.gitignore` needs a comment clarifying that
  `memory_bank/` is ignored while `docs/engineering-memory/` is committed.
- Whether Antigravity gets a lightweight mention now or waits for its dedicated
  design-lab framework.

## Runtime / Data Mutation Boundary
- **Applies:** no.
- **Agent authority:** documentation authoring only inside approved write-set.
- **Structured action:** not applicable.
- **Trusted executor:** not applicable.
- **Policy and approval:** no DB, payment, deployment, secrets, or live data.
- **Audit path:** this Work Block plan, git diff, validation output, and closeout.
- **Forbidden direct path:** not applicable.

## Scope
### In Scope
- Define Engineering Memory authority and routing.
- Clarify `docs/` vs `memory_bank/`.
- Add generated-project Engineering Memory starters.
- Add closeout promotion gate.
- Update bootstrap/read order for joining agents.
- Update navigation/registry/setup/profile docs affected by the new layer.
- Include or preserve existing OpenCode knowledge changes safely.

### Out of Scope
- Vector DBs, embeddings, Graphify, automated transcript summarizers.
- Per-model memory adapters for GPT/Claude/Gemini/Deepseek/GLM.
- Runtime automation or synchronization daemons.
- Project-specific rollout to active downstream repositories.
- Secrets, provider config, deployment, DB, auth, payments, or production code.

## Write-Set
```
docs/plans/WB-2026-07-03-project-engineering-memory-layer.md
README.md
SETUP.md
PROJECT_MAP.md
FILE_REGISTRY.yml
docs/profiles.md
docs/session-bootstrap.md
framework/memory/agent-memory-system.md
framework/memory/memory-bank-protocol.md
framework/memory/project-engineering-memory.md
framework/workflow/ssot-hierarchy.md
skills/ssot-sync-closeout/SKILL.md
skills/memory-bank-manager/SKILL.md
template/AGENTS.md
template/PROJECT_MAP.md
template/FILE_REGISTRY.yml
template/docs/session-bootstrap.md
template/docs/engineering-memory/README.md
template/docs/engineering-memory/decision-record-template.md
template/docs/engineering-memory/source-of-truth-chains.md
template/docs/engineering-memory/temporary-decisions.md
template/docs/engineering-memory/reproducibility-log.md
template/docs/templates/work-block-template.md
template/docs/templates/closeout-report-template.md
template/project.gitignore
template/scripts/bootstrap.sh
scripts/validate-publication.sh
examples/README.md
framework/knowledge/README.md
framework/knowledge/opencode-runtime.md
```

The OpenCode files are included because they are already dirty and overlap with
navigation/registry edits. If the Owner decides to separate them, remove
`framework/knowledge/README.md` and `framework/knowledge/opencode-runtime.md`
from this write-set and close that work first.

## Navigation Impact
- **Files added/moved/removed:** yes; new `framework/memory/project-engineering-memory.md`
  and `template/docs/engineering-memory/*`.
- **PROJECT_MAP.md update needed:** yes; new durable memory path and authority.
- **FILE_REGISTRY.yml update needed:** yes; new files and ownership/update rules.
- **Session bootstrap or profile docs update needed:** yes; joining agents must
  read Engineering Memory after active WB and before operational logs.
- **Generated/derived/local-only boundary changed:** yes; durable Engineering
  Memory is committed under `docs/`, while `memory_bank/` remains local-first by
  default.

## Commit / Stage Scope
- **Files to stage/commit:** exactly the approved write-set after review.
- **Files to leave unstaged:** unrelated local artifacts, secrets, generated
  output, caches, and any dirty files not approved by the Owner.
- **Scope guard:** run `git status --short`, `git diff --name-only`, and inspect
  diffs before staging.

## Acceptance Criteria
- [x] A new agent can identify the durable Engineering Memory path from
      `AGENTS.md`, `PROJECT_MAP.md`, or session bootstrap.
- [x] The framework states that `memory_bank/` supports execution but does not
      override repo-controlled docs.
- [x] Engineering Memory templates are short enough to be maintained and do not
      duplicate plans/specs/reports.
- [x] Temporary decisions require owner/date/review trigger/fallback.
- [x] Evidence pointers prefer stable artifacts: docs, reports, commits, issues,
      commands, or release IDs; not raw chat scrollback.
- [x] Closeout gate is conditional and does not burden trivial tasks.
- [x] Validation catches missing generated-template files or stale registry/map
      references.

## Risks and Mitigations
| Risk | Impact | Mitigation | Stop Condition |
|---|---|---|---|
| SSOT ambiguity between `docs/` and `memory_bank/` | Agents follow stale operational notes | Define authority order first, update registry/map/bootstrap together | Contradictory normative wording remains after search |
| Documentation bloat | Agents skip closeout or ignore memory | Add conditional gate only, not mandatory long forms | Template becomes longer without clear trigger |
| Evidence pointer rot | Future agents cannot verify memory | Require stable repo/issue/commit/command references | Proposed memory relies on chat-only or temp paths |
| Secret/private reasoning leakage | Security and privacy risk | Explicit forbidden-content rules | Any template invites raw transcripts or private CoT |
| Dirty OpenCode edits overwritten | Loss of user/previous work | Inspect and preserve diffs before editing | Conflict cannot be resolved without Owner decision |

## Hard Stops in Scope
- [ ] Production deploy
- [ ] Live DB migration
- [ ] Credential rotation
- [ ] Destructive git ops
- [x] Commit or push
- [ ] Public release/publication
- [ ] Client communications

## Subagent Strategy
- **Classification:** Subagent-Required
- **Triggers matched:** framework governance, multi-runtime contract, memory/SSOT
  authority, publication-facing docs.
- **Use Claude Code team:** no for initial implementation; this is framework
  governance and can be done in Codex layer. Optional later for independent
  review.
- **Claude Code process scope:** not applicable.
- **Claude Code external report:** not applicable.
- **Use Codex/GPT critic or verifier:** yes; critic already completed read-only
  review and approved with required changes. Run another critic/reviewer pass
  after implementation.
- **Dispatch plan:**
  1. Orchestrator implements SSOT and template changes.
  2. Read-only critic reviews authority, bloat, privacy, and cross-agent
     readability.
  3. Verifier runs publication/search checks.
- **Budget posture:** normal.
- **Skip reasons:** Claude Code team skipped because the goal is to strengthen
  the Codex/framework layer, not test external handoff.

## Skills
- **Checked:** orchestrator-log, ssot-sync-closeout, memory-bank-manager,
  subagent-mission-brief.
- **Matched:** ssot-sync-closeout, memory-bank-manager, orchestrator-log.
- **Used:** read-only subagent explorer, read-only critic.
- **Skipped:** handoff-live-smoke; no external handoff runtime change.

## Verification Plan
- **Canonical checks:**
  - `scripts/validate-publication.sh`
  - `bash -n scripts/validate-publication.sh template/scripts/bootstrap.sh`
  - `rg -n "memory_bank.*normative|normative.*memory_bank|cache, not a contract|Engineering Memory|engineering-memory" .`
  - `git diff --check`
- **Scoped fallback checks:** if publication validation is blocked, run targeted
  registry/path checks with `test -f`, `rg`, and `find`.
- **Browser smoke:** not applicable.
- **Evidence expected:** command output, diff summary, critic verdict, updated
  Work Block execution log.
- **Skipped checks:** no frontend/build checks expected unless validation script
  requires them.

## Rollback / Recovery
Revert only this Work Block's changes with an explicit Owner-approved reverse
patch or commit revert. Do not reset or discard unrelated dirty files.

## Execution Log
| Time | Stage | Action / Decision | Evidence | Status |
|---|---|---|---|---|
| 2026-07-03 | Stage 0 | Research completed with explorer + critic | subagent reports in session | complete |
| 2026-07-03 | Stage 0 | Critic required SSOT boundary cleanup before implementation | critic verdict APPROVE WITH REQUIRED CHANGES | accepted |
| 2026-07-03 | Stage 0 | Work Block drafted | this file | complete |
| 2026-07-03 | Stage 1 | Existing dirty OpenCode/navigation files inspected and included in the write-set | `git status --short`, `git diff --name-only` | complete |
| 2026-07-03 | Stage 2 | Engineering Memory contract and generated-project templates added | `framework/memory/project-engineering-memory.md`, `template/docs/engineering-memory/*` | complete |
| 2026-07-03 | Stage 2 | Session bootstrap, SSOT hierarchy, project map, registry, setup/profile docs, and memory skills synchronized | approved write-set diff | complete |
| 2026-07-03 | Stage 3 | Read-only critic pass found stale `memory_bank` authority wording in `template/AGENTS.md` | critic report | fixed |
| 2026-07-03 | Stage 3 | Read-only critic pass found user-specific path hygiene gap and missing temporary-decision owner column | critic report | fixed |
| 2026-07-03 | Stage 4 | Syntax, YAML, privacy-path, stale-wording, whitespace, and publication checks run | verification commands below | passed |

## Closeout and Retrospective
Complete this before the Work Block is considered closed. Keep this evidence
based: record what happened, not private reasoning or unsupported claims.

### Result Summary
- **Final Result:** complete; the framework now has a durable,
  agent-neutral Project Engineering Memory layer and generated-project starter
  files.
- **Closeout Classification:** promoted; this Work Block changed future
  engineering behavior and created durable framework knowledge.
- **Task Status:** complete, not committed.
- **Verification Evidence:** `bash -n bootstrap.sh template/scripts/bootstrap.sh
  scripts/validate-publication.sh`; YAML registry parse; user-specific home-path
  search; stale authority wording search; `git diff --check`; `bash
  scripts/validate-publication.sh`.
- **Residual Risks:** project-specific rollout to active repositories is
  intentionally deferred. Ignored local `handoff/` runtime logs may contain
  machine paths, but they are excluded from publication validation and are not
  tracked release files.

### Critic and Review Value
- **Critic used:** yes; read-only Codex critic subagent
- **Critic verdict:** initial APPROVE WITH REQUIRED CHANGES; implementation
  critic BLOCK; final blockers fixed and verification passed.
- **What the critic caught:** SSOT ambiguity, `memory_bank` authority
  inconsistency, closeout bloat risk, evidence pointer rot, privacy leakage,
  stale `template/AGENTS.md` wording, user-specific absolute path hygiene, and a
  missing owner column in temporary decisions.
- **What the critic missed:** no additional issue found after scripted
  publication validation.
- **Skip/fallback reason:** not applicable

### Lessons Learned
- **What worked:** using a critic before implementation prevented a likely
  duplicate memory layer.
- **What did not work:** stale wording survived in long policy files until a
  focused read-only critic searched specifically for authority drift.
- **What not to repeat:** do not add memory files without a promotion rule and
  source-of-truth ranking.
- **Evidence wording check:** use "defines" for docs and "validated" only after
  scripted checks pass.
- **Framework updates made:** added Project Engineering Memory docs/templates,
  updated bootstrap/read order, clarified `docs/` vs `memory_bank/`, extended
  closeout templates, and hardened publication validation for generated files
  and user-specific path leakage.
- **Framework updates to consider:** future project rollout guide after base
  layer stabilizes.
- **Reusable knowledge created:** this Work Block plan and
  `framework/memory/project-engineering-memory.md`.
- **Navigation updates:** README, SETUP, PROJECT_MAP, FILE_REGISTRY,
  docs/profiles, session bootstrap, and generated-project equivalents updated.
- **Follow-up Work Blocks:** project rollout to selected active repositories
  after this framework layer is merged.
