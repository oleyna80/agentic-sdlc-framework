# Codex Critic Layer Work Block - 2026-06-15

## Expected Final Result

Codex can run the framework as an independent SDLC runtime with an auditable
decision trail:

- Codex-Orchestrator decisions are logged in `memory_bank/orchestrator-log.md`.
- Codex critic findings are logged in `memory_bank/review-log.md`.
- Non-trivial Work Blocks use Stage 0.5 Codex Critic Review before writes.
- The write gate records whether the critic was `READY`, `FALLBACK`, or
  `SKIPPED`.
- The docs do not overclaim Claude Code-style runtime enforcement where Codex
  only has a process contract and a declaration gate.

## Scope

Updated Codex-layer scaffold and reference docs:

- `.codex/critic.md`
- `.codex/AGENTS.md`
- `.codex/instructions.md`
- `.codex/write-gate.md`
- `.codex/hooks/stage0_write_gate.py`
- `memory_bank/orchestrator-log.md`
- `memory_bank/review-log.md`
- framework overview, README, validation, bootstrap verification

Out of scope:

- Claude Code runtime changes
- live external LLM or MCP integration
- secrets, env files, or project-specific configuration

## Execution Plan

1. Inspect existing Codex docs, logs, write gate, and critic skill.
2. Add Codex critic contract and wire it into Stage 0/Stage 0.5 flow.
3. Strengthen write-gate fields so unresolved critic requirements block writes.
4. Update logging templates and public overview docs.
5. Run read-only Codex critic review.
6. Resolve critic findings and rerun publication validation.

## Critic Result

Read-only Codex critic verdict: `SUPPLEMENT`.

Findings addressed:

- Replaced imprecise `standard or higher` side-effect wording with
  `Production code write or higher`.
- Corrected generated-project skill reference to
  `.agent/skills/critic-review/SKILL.md`.
- Added `Orchestrator Response` to `.codex/write-gate.md` and hook validation
  for `SUPPLEMENT` / `RECONSIDER`.
- Clarified that the read-only critic returns findings and the Orchestrator
  writes logs/artifacts.

Residual risk:

- The hook validates declared gate fields, not the semantic quality of the
  critic run. This is documented as process enforcement, not a full runtime
  proof system.

## Verification

Passed:

- `python3 -B` AST parse for `.codex/hooks/stage0_write_gate.py`
- `git diff --check`
- temporary `/tmp` hook behavior smoke for `REQUIRED`, `APPROVE`, and
  `SUPPLEMENT` without response
- `bash scripts/validate-publication.sh`

## Outcome

Ready for commit after Owner approval.
