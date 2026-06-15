# Changelog

## Unreleased

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
