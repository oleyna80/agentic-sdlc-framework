# Changelog

## Unreleased

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
