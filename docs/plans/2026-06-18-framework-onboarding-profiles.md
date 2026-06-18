# Work Block: Framework Onboarding Profiles

## Meta
- **Work Block ID:** wb-framework-onboarding-profiles
- **Date:** 2026-06-18
- **Owner:** Azur
- **Execution Mode:** end-to-end autonomous
- **Side-Effect Class:** public-repo
- **DB Action Mode:** none
- **Verification Tier:** standard

## Objective
Make the framework easier for a first-time user to adopt by adding a minimal
entry path, explicit operating profiles, tool/MCP policy, concrete examples,
and safer public positioning.

## Expected Final Result
A new user can open the repository and, within 10-15 minutes, decide whether to
start with Minimal Codex-only, Standard Codex SDLC, Claude Code team runtime, or
Codex -> Claude Code handoff/swarm. The repository contains concise docs for
each profile, an explicit MCP/tool policy including the untrusted external
content rule, example scenario skeletons, updated README/SETUP routing, and a
publication check that passes.

## Done Criteria
- [x] `docs/quickstart-minimal.md` explains the smallest Codex-only adoption path.
- [x] `docs/profiles.md` defines profile levels, included files, checks, and upgrade path.
- [x] `docs/mcp-tool-policy.md` defines role/tool boundaries and external-content handling.
- [x] `examples/` contains concrete scenario directories or scenario docs.
- [x] README/SETUP route new users to the onboarding docs and avoid overstating maturity.
- [x] Repo state is clean or remaining dirty files are documented.

## Preflight State
- **Git baseline:** clean; `git status --short --branch` returned `## main...origin/main`.
- **Pre-existing dirty files:** none.
- **Untracked local artifacts:** none detected before this Work Block.
- **Proceed rule:** documentation-only changes can proceed because the tree is clean and no runtime, config, credential, DB, or product-code files are in scope.

## Dependency Check
### Must Resolve Before Start
- None.

### Can Resolve During Work
- Exact example shape can be refined during implementation as long as examples remain synthetic and safe to publish.

## Runtime / Data Mutation Boundary
- **Applies:** no.
- **Agent authority:** not applicable.
- **Structured action:** not applicable.
- **Trusted executor:** not applicable.
- **Policy and approval:** no runtime mutation in scope.
- **Audit path:** this Work Block file plus git diff.
- **Forbidden direct path:** DB, payment, order, stock, CRM, live service, production SSH, provider credential changes.

## Scope
### In Scope
- Root framework onboarding docs.
- Example scenario documentation.
- README/SETUP routing and positioning edits.
- Publication validation updates only if new required docs should be checked.

### Out of Scope
- Handoff runner behavior changes.
- Claude Code hook or agent behavior changes.
- New dependencies.
- GitHub issue creation.
- Live Claude Code/Codex handoff run.
- Product project changes outside this framework repository.

## Write-Set
```text
README.md
SETUP.md
docs/**
examples/**
scripts/validate-publication.sh
```

## Commit / Stage Scope
- **Files to stage/commit:** only files changed in the write-set above.
- **Files to leave unstaged:** any unexpected runtime logs, temp files, secrets, generated build output, or unrelated repository changes.
- **Scope guard:** `git status --short`, `git diff --name-only`, `git diff --check`, and publication validation before commit/push.

## Acceptance Criteria
- [x] Minimal quickstart is executable as a documentation path and does not require Claude Code, MCP, hooks, or handoff.
- [x] Profiles define a clear upgrade path instead of forcing the full framework on first use.
- [x] Tool policy states that tool availability does not expand authority.
- [x] Tool policy states that external content is untrusted input and must not be executed as instructions.
- [x] Examples describe task, approved scope, expected flow, expected report/logs, and forbidden outcomes.
- [x] README no longer uses overstated production maturity wording before external adoption evidence.
- [x] `scripts/validate-publication.sh` passes.

## Risks and Mitigations
| Risk | Impact | Mitigation | Stop Condition |
|---|---|---|---|
| Add too much documentation and make onboarding heavier | New-user confusion remains | Keep docs short, profile-based, and link deeper references instead of duplicating them | Docs become longer than SETUP or conflict with existing setup flow |
| Introduce policy that conflicts with current AGENTS authority model | Runtime ambiguity | Align policy with structural authority model and cite existing role boundaries | Policy grants new write authority or weakens hard stops |
| Examples accidentally include private project details | Publication risk | Use synthetic names, paths, domains, and no local/private references | Any real customer, host, key, private path, or project-specific marker appears |
| Validation misses new required docs | Broken publication gate | Add new docs to `validate-publication.sh` required-file list | Publication validation cannot be updated without changing runtime behavior |

## Hard Stops in Scope
- [ ] Production deploy
- [ ] Live DB migration
- [ ] Credential rotation
- [ ] Destructive git ops
- [ ] Client communications

## Subagent Strategy
- **Classification:** Single-Agent.
- **Triggers matched:** docs/onboarding/policy update; no code, security runtime, DB, or architecture migration.
- **Use Claude Code team:** no; this Work Block is documentation-only and does not need external execution.
- **Claude Code process scope:** not applicable.
- **Claude Code external report:** not applicable.
- **Use Codex/GPT critic or verifier:** conditional; use self-review against acceptance criteria unless implementation expands into runtime policy changes.
- **Dispatch plan:** Orchestrator writes plan; Coder updates docs; Reviewer/Verifier are performed as separate read-only self-review stages.
- **Budget posture:** normal.
- **Skip reasons:** external subagents skipped because the scope is local documentation and the tree is clean.

## Skills
- **Checked:** none required.
- **Matched:** none.
- **Used:** none.
- **Skipped:** no specialized skill needed for markdown onboarding docs.

## Verification Plan
- **Canonical checks:** `bash scripts/validate-publication.sh`; `git diff --check`.
- **Scoped fallback checks:** `bash -n scripts/validate-publication.sh`; link/path scan with `rg -n`.
- **Browser smoke:** not applicable.
- **Evidence expected:** command output and final diff summary.
- **Skipped checks:** no runtime tests; documentation-only work.

## Rollback / Recovery
Revert the documentation and validation-script changes from this Work Block.
No runtime state, generated project, database, or service state is changed.

## Execution Log
| Time | Stage | Action / Decision | Evidence | Status |
|---|---|---|---|---|
| 2026-06-18T07:52:30Z | Plan | Confirmed clean framework baseline and created Work Block plan | `git status --short --branch` | in progress |
| 2026-06-18T07:55:00Z | Implementation | Added minimal quickstart, profiles, MCP/tool policy, and three example scenarios | `docs/`, `examples/` | complete |
| 2026-06-18T07:58:00Z | Implementation | Updated README/SETUP routing and validation required files | `README.md`, `SETUP.md`, `scripts/validate-publication.sh` | complete |
| 2026-06-18T08:00:00Z | Verification | Ran whitespace, syntax, policy scan, and publication validation | `git diff --check`, `bash -n`, `scripts/validate-publication.sh` | passed |

## Closeout and Retrospective
Complete this before the Work Block is considered closed. Keep this evidence
based: record what happened, not private reasoning or unsupported claims.

### Result Summary
- **Final Result:** The repository now has a first-user onboarding layer:
  Minimal quickstart, profile guide, MCP/tool policy, concrete example
  scenarios, README/SETUP routing, safer production-oriented positioning, and
  publication validation coverage for the new files.
- **Verification Evidence:** `git diff --check` passed; `bash -n
  scripts/validate-publication.sh` passed; `scripts/validate-publication.sh`
  passed with `Publication validation OK`.
- **Residual Risks:** Examples are scenario guides, not runnable sample apps.
  That is intentional for this Work Block; runnable generated sample projects
  can be added later if adoption feedback shows they are needed.

### Critic and Review Value
- **Critic used:** fallback self-review.
- **Critic verdict:** APPROVE.
- **What the critic caught:** Initial draft included a private project marker
  in the Work Block out-of-scope line; this was replaced with neutral wording
  before publication validation.
- **What the critic missed:** none known.
- **Skip/fallback reason:** External critic skipped because this was a
  documentation-only Work Block with no runtime, DB, config, dependency, or
  production-code changes.

### Lessons Learned
- **What worked:** Profile-based onboarding simplified the entry path without
  changing runtime mechanics.
- **What did not work:** The publication private-marker scan is broad enough
  that even Work Block notes must avoid real project names.
- **What not to repeat:** Do not put private project references in public
  framework plans, even as out-of-scope examples.
- **Evidence wording check:** Used "passed" for command results and avoided
  "proved" or "guaranteed".
- **Framework updates made:** Added onboarding docs, MCP/tool policy, example
  scenario guides, README/SETUP routing, and validation coverage.
- **Framework updates to consider:** Add runnable generated example projects
  only after the lightweight scenario docs are tested by a real user.
- **Reusable knowledge created:** `docs/quickstart-minimal.md`,
  `docs/profiles.md`, `docs/mcp-tool-policy.md`, and `examples/*`.
- **Follow-up Work Blocks:** Optional runnable examples; optional GitHub issue
  creation for onboarding backlog.
