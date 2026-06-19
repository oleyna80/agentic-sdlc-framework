# Work Block: Claude Code Plugin Profile

## Meta
- **Work Block ID:** wb-claude-code-plugin-profile
- **Date:** 2026-06-19
- **Owner:** Azur
- **Execution Mode:** end-to-end autonomous
- **Side-Effect Class:** public-repo
- **DB Action Mode:** none
- **Verification Tier:** standard

## Objective
Create a controlled, reproducible Claude Code plugin profile for maintainers of
this framework without changing global Claude Code state or generated-project
defaults.

## Expected Final Result
The framework repository declaratively enables only the approved official
`skill-creator` and `frontend-design` plugins at project scope. Maintainers can
see which evaluated extensions were accepted, rejected, or quarantined and
why. Plugin configuration, documentation, navigation, and publication checks
are consistent, and verification passes without this Work Block requesting or
modifying user-scoped plugin activation or generated-project defaults. A
pre-existing user-scoped installation may still exist. Claude Code may update its normal
user-local download cache and installation registry for the project-scoped
install.

## Done Criteria
- [x] Project-scoped plugin settings contain only the two approved plugins.
- [x] Plugin policy documents scope, compatibility decisions, and review gate.
- [x] Claude CLI reports the approved plugins enabled in this repository.
- [x] Publication validation and diff checks pass.
- [x] Repository changes are reviewed and this Work Block did not request or modify user-scoped plugin activation.

## Preflight State
- **Git baseline:** clean; `git status --short --branch` returned `## main...origin/main`.
- **Pre-existing dirty files:** none.
- **Untracked local artifacts:** none detected.
- **Proceed rule:** Owner approved project-local implementation; global Claude Code state and generated-project defaults remain out of scope.

## Scope
### In Scope
- Project-scoped Claude Code plugin activation.
- Plugin compatibility policy and audit record.
- Navigation and publication validation updates.

### Out of Scope
- User-global Claude Code configuration.
- Generated-project plugin defaults.
- GSD installation.
- Enabling Superpowers, Context Mode, or Claude Mem.
- Plugin source modification.
- Commit or push.

## Write-Set
```text
.claude/settings.json
PROJECT_MAP.md
FILE_REGISTRY.yml
framework/knowledge/**
docs/plans/2026-06-19-claude-code-plugin-profile.md
scripts/validate-publication.sh
```

## Navigation Impact
- **Files added/moved/removed:** added project settings, plugin policy, and this Work Block.
- **PROJECT_MAP.md update needed:** yes; register project plugin configuration.
- **FILE_REGISTRY.yml update needed:** yes; register authority and update triggers.
- **Session bootstrap or profile docs update needed:** no; runtime profile selection is unchanged.
- **Generated/derived/local-only boundary changed:** no.

## Risks and Mitigations
| Risk | Impact | Mitigation | Stop Condition |
|---|---|---|---|
| Plugin workflow overrides SDLC gates | Loss of authority control | Enable only focused official skills; retain existing gates | Plugin introduces hooks, agents, or commands that bypass gates |
| User-wide plugin activation is modified | Other projects change unexpectedly | Use checked-in project settings and `--scope project` only; allow only Claude's normal local cache metadata | A required step needs user scope |
| Standalone and plugin skills drift | Inconsistent behavior | Keep both roles explicit and review updates independently | Automatic synchronization would overwrite local adaptations |
| CLI installation hangs | Incomplete local activation | Treat checked-in config as source of truth; verify with bounded CLI checks | Activation cannot be verified without modifying global state |

## Subagent Strategy
- **Classification:** Single-Agent.
- **Triggers matched:** bounded configuration and documentation change.
- **Use Claude Code team:** no; Claude Code is the configured target and should not modify its own control policy in this Work Block.
- **Use Codex/GPT critic or verifier:** read-only review after implementation.
- **Dispatch plan:** Coder implementation, Reviewer diff audit, Verifier checks.
- **Budget posture:** normal.

## Verification Plan
- **Canonical checks:** `claude plugin list`, JSON parse, `git diff --check`, `bash scripts/validate-publication.sh`.
- **Scoped fallback checks:** inspect `.claude/settings.json` and marketplace manifests if plugin installation remains blocked.
- **Browser smoke:** not applicable.
- **Evidence expected:** CLI output, parsed settings, validation output, and final diff.

## Execution Log
| Time | Stage | Action / Decision | Evidence | Status |
|---|---|---|---|---|
| 2026-06-19T17:09:10Z | Plan | Confirmed clean baseline and approved project-only scope | `git status --short --branch` | complete |
| 2026-06-19T17:09:10Z | Spec | Selected two focused official plugins; quarantined competing lifecycle and broad runtime plugins | source/manifests review | complete |
| 2026-06-19T17:09:10Z | Implementation | Added project settings, plugin policy, and navigation updates | approved write-set | complete |
| 2026-06-19T17:10:35Z | Implementation | Installed both approved plugins with project scope; TTY avoided the earlier non-interactive CLI stall | `claude plugin install ... --scope project` | complete |
| 2026-06-19T17:14:00Z | Review | Independent read-only critic requested snapshot evidence, exact allowlist validation, and clearer runtime/user-scope limits | critic verdict `SUPPLEMENT` | complete |
| 2026-06-19T17:16:00Z | Fix | Added source fingerprints, strict allowlist validation, and explicit compatibility boundary | KB and publication gate | complete |
| 2026-06-19T17:16:00Z | Verification | Confirmed one project install per approved plugin, exact settings allowlist, clean diff, and publication validation | CLI registry check; validation log | passed |
| 2026-06-19T17:20:00Z | Review | Repeat critic identified hidden runtime, cost, environment, and CDN surface in optional `skill-creator` eval tools | critic verdict `SUPPLEMENT` | complete |
| 2026-06-19T17:21:00Z | Fix | Added an Owner-gated operational boundary for nested Claude calls, viewer server, and external assets | plugin policy | complete |
| 2026-06-19T17:22:00Z | Review | Final read-only critic found no unresolved material issues | critic verdict `APPROVE` | complete |
| 2026-06-19T17:22:00Z | Verification | Re-ran diff, structured-file, sensitive-marker, and publication checks after final fixes | command output and validation log | passed |

## Closeout and Retrospective

### Result Summary
- **Final Result:** This repository now enables only the approved official
  `skill-creator` and `frontend-design` plugins at project scope, with a
  documented compatibility policy and strict publication allowlist.
- **Verification Evidence:** exact project registry/install check passed for
  both plugins; JSON and YAML parsing passed; `git diff --check` passed; `bash
  scripts/validate-publication.sh` ended with `Publication validation OK`.
- **Residual Risks:** Upstream installs are not semantically versioned or
  pinned. Tree fingerprints provide review evidence but updates require a new
  comparison. Generated-project hook coexistence was not tested because plugin
  defaults were intentionally not added to `template/`.

### Critic and Review Value
- **Critic used:** yes; read-only Codex subagent.
- **Critic verdict:** initial `SUPPLEMENT`; final `APPROVE` after findings were addressed.
- **What the critic caught:** missing reproducible source evidence, a
  presence-only publication check, ambiguous user-scope wording, and an
  untested generated-project runtime claim. Repeat review also caught nested
  Claude calls, inherited environment, local server, and CDN behavior hidden
  behind optional `skill-creator` evaluation tools.
- **What the critic missed:** A failed CLI uninstall can update project
  settings before failing to update the local installation registry. The
  verifier caught and repaired that non-atomic state.
- **Skip/fallback reason:** not applicable.

### Lessons Learned
- **What worked:** Project-scoped declarative settings plus exact registry and
  publication checks produced a narrow, auditable profile.
- **What did not work:** Non-TTY plugin installation stalled, and a later
  failed uninstall partially changed project settings before reporting its
  registry write error.
- **What not to repeat:** Do not infer duplicate installs from unfiltered
  `claude plugin list`; it lists entries from other project paths. Inspect the
  installation registry by both `scope` and `projectPath`, and re-check project
  settings after any failed plugin command.
- **Framework updates made:** project plugin settings, plugin audit policy,
  strict publication allowlist, navigation registry, and this Work Block log.
- **Framework updates to consider:** pending.
- **Reusable knowledge created:** `framework/knowledge/claude-code-plugins.md`.
- **Navigation updates:** `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, and the
  knowledge-base index.
- **Follow-up Work Blocks:** isolated Context Mode and Claude Mem compatibility evaluation, only if real project evidence justifies them.
