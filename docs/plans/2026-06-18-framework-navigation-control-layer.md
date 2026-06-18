# Work Block: Framework Navigation Control Layer

## Meta
- **Work Block ID:** wb-framework-navigation-control-layer
- **Date:** 2026-06-18
- **Owner:** Azur
- **Execution Mode:** end-to-end autonomous
- **Side-Effect Class:** public-repo
- **DB Action Mode:** none
- **Verification Tier:** standard

## Objective
Add a lightweight navigation control layer that helps humans and agents quickly
understand the framework repository and generated project structure without
requiring generated knowledge graph tooling.

## Expected Final Result
A new human maintainer or agent can orient in this repository or in a generated
project in 3-5 minutes by reading a short project map, a machine-readable file
registry, and a session bootstrap guide. The navigation layer clearly separates
normative files, examples, logs, generated/derived artifacts, and local-only
state. Publication validation checks that these navigation files exist in both
the framework repository and generated project template.

## Done Criteria
- [x] Root `PROJECT_MAP.md` explains framework layers, authority, key paths,
  generated/log/example boundaries, and new-session read order.
- [x] Root `FILE_REGISTRY.yml` describes important files and path patterns with
  role, authority, ownership, update triggers, and related files.
- [x] Root `docs/session-bootstrap.md` defines the default session intake flow.
- [x] Template navigation files provide the same lightweight orientation for
  generated projects.
- [x] README, SETUP, profiles, and Work Block template route users to the
  navigation layer.
- [x] Publication validation passes.

## Preflight State
- **Git baseline:** clean working tree, `main...origin/main [ahead 1]`
  from the previous local Work Block commit.
- **Pre-existing dirty files:** none.
- **Untracked local artifacts:** none.
- **Proceed rule:** the previous commit is local and unrelated to uncommitted
  changes; this Work Block can proceed and remain as a separate local diff.

## Dependency Check
### Must Resolve Before Start
- None.

### Can Resolve During Work
- Exact registry breadth: keep path-pattern level instead of trying to register
  every file.

## Runtime / Data Mutation Boundary
- **Applies:** no.
- **Agent authority:** not applicable.
- **Structured action:** not applicable.
- **Trusted executor:** not applicable.
- **Policy and approval:** not applicable.
- **Audit path:** this Work Block plan and git diff.
- **Forbidden direct path:** not applicable.

## Scope
### In Scope
- Lightweight navigation files for framework maintainers.
- Lightweight navigation files copied into generated projects.
- Documentation routing updates.
- Publication validation coverage for required navigation files.

### Out of Scope
- Graphify integration.
- Dependency-cruiser, madge, or import graph tooling.
- Full traceability matrix.
- ADR system.
- Changes in downstream product projects.
- Commit or push unless separately approved.

## Write-Set
```text
PROJECT_MAP.md
FILE_REGISTRY.yml
docs/session-bootstrap.md
docs/plans/2026-06-18-framework-navigation-control-layer.md
template/PROJECT_MAP.md
template/FILE_REGISTRY.yml
template/AGENTS.md
template/docs/session-bootstrap.md
README.md
SETUP.md
docs/profiles.md
template/docs/templates/work-block-template.md
bootstrap.sh
template/scripts/bootstrap.sh
scripts/validate-publication.sh
```

## Navigation Impact
- **Files added/moved/removed:** added root and template navigation files.
- **PROJECT_MAP.md update needed:** yes; this Work Block creates it.
- **FILE_REGISTRY.yml update needed:** yes; this Work Block creates it.
- **Session bootstrap or profile docs update needed:** yes; this Work Block
  creates session bootstrap and routes profiles to it.
- **Generated/derived/local-only boundary changed:** yes; documented generated,
  log, derived, example, and local-state boundaries.

## Commit / Stage Scope
- **Files to stage/commit:** only the write-set above.
- **Files to leave unstaged:** unrelated local artifacts, secrets, generated
  build output, runtime logs.
- **Scope guard:** `git status --short --branch`, `git diff --name-only`.

## Acceptance Criteria
- [x] Navigation docs state that `AGENTS.md`, explicit Owner instructions, task
  files, and approved Work Block scope outrank generated/discovery context.
- [x] Registry marks key paths as `normative`, `derived`, `example`, `log`, or
  `local_state`.
- [x] Session bootstrap says not to assume stale memory is current and to run
  `git status --short --branch` before implementation.
- [x] Generated project `AGENTS.md` Session Start Read Set routes agents
  through `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, and `docs/session-bootstrap.md`.
- [x] Work Block template requires map/registry impact check when important
  files are added, moved, or removed.
- [x] Publication validator requires the new navigation files and smoke project
  receives the template navigation files.
- [x] Bootstrap replaces placeholders in `.yml` files so generated project
  registry files are not left with raw template markers.

## Risks and Mitigations
| Risk | Impact | Mitigation | Stop Condition |
|---|---|---|---|
| Registry becomes too detailed | The navigation layer becomes maintenance burden | Register key files and path patterns only | Need to list every file manually |
| Root and template maps drift | Generated projects miss important rules | Add both to publication validation | Validator cannot cover required files |
| Docs duplicate existing profiles | Users read conflicting paths | Route to profiles rather than restating mode details | Conflict with `docs/profiles.md` |

## Hard Stops in Scope
- [ ] Production deploy
- [ ] Live DB migration
- [ ] Credential rotation
- [ ] Destructive git ops
- [ ] Client communications

## Subagent Strategy
- **Classification:** Single-Agent
- **Triggers matched:** documentation architecture, but low-risk and scoped.
- **Use Claude Code team:** no; this is a framework documentation/navigation WB.
- **Claude Code process scope:** not applicable.
- **Claude Code external report:** not applicable.
- **Use Codex/GPT critic or verifier:** fallback self-review; no external CC
  needed.
- **Dispatch plan:** Orchestrator writes plan, Coder edits docs, Reviewer
  checks authority/drift risk, Verifier runs publication checks.
- **Budget posture:** normal.
- **Skip reasons:** Graphify and external reviewers are intentionally out of
  scope.

## Skills
- **Checked:** local framework docs and validation script.
- **Matched:** documentation architecture, publication validation.
- **Used:** built-in repo workflow.
- **Skipped:** Claude Code/handoff; unnecessary for this docs-only WB.

## Verification Plan
- **Canonical checks:**
  - `git diff --check`
  - `bash -n scripts/validate-publication.sh`
  - `scripts/validate-publication.sh`
- **Scoped fallback checks:** targeted `rg` scans for navigation terms and
  private markers if publication validation is blocked.
- **Browser smoke:** not applicable.
- **Evidence expected:** command output and final git status/diff summary.
- **Skipped checks:** none planned.

## Rollback / Recovery
Revert this Work Block's files from the git diff before staging. Do not rewrite
history or revert prior user work.

## Execution Log
| Time | Stage | Action / Decision | Evidence | Status |
|---|---|---|---|---|
| 2026-06-18T08:30:00Z | Plan | Started from clean local working tree with one previous ahead commit | `git status --short --branch` | done |
| 2026-06-18T08:36:00Z | Implementation | Added root and template navigation files | `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, `docs/session-bootstrap.md` | done |
| 2026-06-18T08:42:00Z | Implementation | Routed onboarding docs and bootstrap validators to navigation layer | README, SETUP, profiles, scripts | done |
| 2026-06-18T08:48:00Z | Verification | Ran syntax, whitespace, and publication checks | `git diff --check`, `bash -n`, `scripts/validate-publication.sh` | passed |

## Closeout and Retrospective
Complete this before the Work Block is considered closed. Keep this evidence
based: record what happened, not private reasoning or unsupported claims.
Use `none` or `not applicable` when there is no real signal; do not invent
lessons to fill the form.

### Result Summary
- **Final Result:** Navigation control layer added for both framework
  maintainers and generated projects. Humans and agents now have a short map,
  structured registry, and session bootstrap guide before reading the full
  repository.
- **Verification Evidence:** `git diff --check`; `bash -n bootstrap.sh`;
  `bash -n template/scripts/bootstrap.sh`;
  `bash -n scripts/validate-publication.sh`;
  `scripts/validate-publication.sh`.
- **Residual Risks:** Registry is intentionally selective. It will need updates
  when major paths, authority boundaries, or generated/local-only boundaries
  change.

### Critic and Review Value
- **Critic used:** fallback self-review.
- **Critic verdict:** APPROVE.
- **What the critic caught:** Root docs initially treated `AGENTS.md` as a
  tracked framework-repo file, but only `template/AGENTS.md` exists in this
  repository. The authority wording was corrected to active workspace
  `AGENTS.md` for the framework and generated project `AGENTS.md` for
  scaffolded projects. The review also caught that `.yml` placeholders needed
  bootstrap support.
- **What the critic missed:** none discovered in verification.
- **Skip/fallback reason:** External critic was unnecessary for a scoped
  documentation/navigation Work Block.

### Lessons Learned
- **What worked:** Keeping the registry selective made it useful without
  turning it into a full file inventory.
- **What did not work:** Initial scope missed the `.yml` placeholder behavior in
  `bootstrap.sh`; smoke validation made the dependency visible before closeout.
- **What not to repeat:** Do not introduce a new template file type without
  checking placeholder replacement and bootstrap validation.
- **Evidence wording check:** Use "demonstrated" for this one Work Block run;
  publication validation is repeatable and can be called "validated" for the
  scripted checks.
- **Framework updates made:** Added project maps, file registries, session
  bootstrap docs, Work Block navigation impact fields, and publication
  validation requirements.
- **Framework updates to consider:** Add a lightweight registry consistency
  script later if the framework grows enough that manual registry drift becomes
  common.
- **Reusable knowledge created:** `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, and
  `docs/session-bootstrap.md`.
- **Navigation updates:** created and validated root and template navigation
  files.
- **Follow-up Work Blocks:** none required before use; Graphify remains a
  future option only after repository scale justifies it.
