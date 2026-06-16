# Changelog

## Unreleased

## v0.1.0 - 2026-06-16

- Added first-15-minutes onboarding docs that explain Codex-only, Claude Code
  team, and Codex-to-Claude Code swarm operating modes with smoke-test evidence.
- Expanded Work Block closeout with an evidence-based retrospective gate,
  critic value capture, and evidence wording rules.
- Added a Live Handoff Smoke Work Block report demonstrating Codex-to-Claude
  Code runner execution on a clean scaffold with scope audit and
  external-team log.
- Added a `handoff-live-smoke` skill so future sessions reuse the verified
  live handoff checklist and avoid sandbox/scope/evidence overclaims.
- Added Codex-layer critic review and decision-log parity docs so Codex can run
  as an independent Orchestrator with auditable critic feedback.
- Added a Codex critic layer Work Block report with critic findings and
  verification evidence.
- Fixed publication validation private-marker scanning for fresh GitHub archive
  layouts.
- Expanded the Work Block template with expected final result, done criteria,
  dependency check, subagent strategy, execution log, and retrospective notes.
- Added Claude Code global bootstrap guidance for provider env, shared
  subagents, portable hooks, and project-local gate boundaries.
- Added publication validation and public repository hygiene docs.
- Added root MIT license and third-party notices.
- Split generated project ignore rules into `template/project.gitignore` so
  framework template files remain publishable.
- Added missing SDLC work directories and agent memory starter files.
- Bootstrap now installs core skills into both `.claude/skills/` and
  `.agent/skills/`.
- Bootstrap placeholder replacement now handles slashes, backslashes, and `&`
  in project names and paths.
