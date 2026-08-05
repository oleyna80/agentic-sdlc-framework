---
schema_version: 1
artifact_type: work_block
artifact_id: wb-opencode-001-adapter-baseline-refresh
work_block_id: WB-OPENCODE-001
status: draft
owner_role: orchestrator
created_at: 2026-08-03
process_level: Controlled
governance_profile: Controlled
branch: agent/opencode-integration
---

# WB-OPENCODE-001 — OpenCode Runtime Adapter Baseline Refresh

Привести runtime adapter OpenCode в соответствие с текущей версией OpenCode
(август 2026): документировать новые capabilities, обновить permission keys,
валидировать agent definitions, добавить coverage в CI-тесты. Без активации
hooks, плагинов, MCP, провайдеров или моделей.

## Scope

**In scope:**

1. `runtimes/opencode/README.md` — обновить capability snapshot, добавить
   документацию новых фич (plugins, skills, server API, `default_agent`,
   `subagent_depth`, `disabled_providers`), обновить activation checklist.
2. `template/opencode.json` — добавить недостающие permission keys: `question`,
   `doom_loop`, `todowrite`, `lsp`, `list`. Обновить `task` на per-agent glob
   (`"*": ask`). Добавить `default_agent: build`, `subagent_depth: 1`,
   `share: manual`. `permission.skill` с `internal-*: deny`.
3. `template/.opencode/agents/{architect,critic,coder,reviewer,verifier}.md` —
   синхронизировать permission frontmatter с обновлённым `opencode.json`.
   Добавить `question`, `doom_loop`, `todowrite`, `lsp`, `list`.
4. `docs/bootstrap-profiles.md` — обновить описание `opencode` профиля.
5. `scripts/test-runtime-conformance.py` — добавить проверки на новые
   permission keys, структуру агентов, `opencode.json` schema keys.
6. `scripts/test-integration-contracts.py` — проверить `opencode.json`
   структуру.

**Out of scope:**

- Активация MCP серверов, плагинов, провайдеров, моделей.
- Создание или изменение hooks.
- Изменение governance authority, Hard Stops, lifecycle.
- `candidate/portable-agentic-sdlc-kit/`.
- Target-environment smoke.
- Skill bridge реализация.
- Plugin-based write-gate.

## Risk Profile

- **Risk level:** Low. Изменения документируют существующие возможности, не
  меняют authority.
- **Side effects:** None. Runtime не активируется.
- **Data mode:** Read/write — только утверждённый write-set Work Block; live
  data, secrets, and external systems prohibited.
- **Isolation:** Один Coder в этом dedicated worktree; Reviewer и Verifier —
  отдельные read-only sessions.

## Acceptance Checks

```text
python scripts/test-runtime-conformance.py          # passes
python scripts/test-integration-contracts.py         # passes
python3 scripts/validate_publication.py               # passes or known worktree false-positive
python scripts/validate-release-state.py             # passes или UNVERIFIED
```

Ручная проверка: `template/opencode.json` валидируется по
`https://opencode.ai/config.json` схеме.

## Hard Stops

- Любое изменение authority, write gate, Hard Stop boundaries — отдельный
  Owner approval.
- Активация MCP, plugin, provider, model — отдельный Owner approval.
- Commit, push — Owner approval.

## Write-set

```
runtimes/opencode/README.md
template/opencode.json
template/.opencode/agents/architect.md
template/.opencode/agents/critic.md
template/.opencode/agents/coder.md
template/.opencode/agents/reviewer.md
template/.opencode/agents/verifier.md
docs/bootstrap-profiles.md
scripts/test-runtime-conformance.py
scripts/test-integration-contracts.py
```

## Critic Gate

Required before execution.

## Reviewer / Verifier

Required — read-only, independent subagent (separate session or worktree).
