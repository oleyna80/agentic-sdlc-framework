# LiteLLM + Claude Code: Tri-Model QC Research & Plan

> Research date: 2026-06-13
> Source: generalized dual-model QC smoke-test pattern
> Status: research complete, plan ready, implementation deferred

## Research Results

### Claude Code Proxy Support

Claude Code supports routing API calls through a proxy via env vars:

| Variable | Purpose |
|----------|---------|
| ANTHROPIC_BASE_URL | Custom API endpoint (appends /v1/messages) |
| ANTHROPIC_AUTH_TOKEN | Authorization: Bearer header value |
| ANTHROPIC_API_KEY | X-Api-Key header |
| ANTHROPIC_MODEL | Default model override |
| CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 | Strip beta headers (critical for proxy) |
| CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1 | Show proxied models in /model picker (v2.1.129+) |

### Subagent Model Field

Agent definitions support model field in YAML frontmatter:
- model: inherit -- uses parent session model (current default)
- model: sonnet -- latest Claude Sonnet
- model: opus -- latest Claude Opus
- model: haiku -- latest Claude Haiku
- model: claude-sonnet-4-20250514 -- explicit version pin

When ANTHROPIC_BASE_URL is set, subagents with explicit models route through proxy.

### LiteLLM Docker Setup

Key config: docker-compose.yml with ghcr.io/berriai/litellm:main-latest image on port 4000.
Config.yaml defines 3 models (Sonnet/Opus/Haiku) with per-model 30-day budgets.
drop_params: true strips unsupported params before forwarding to Anthropic.

### Gotchas

1. Beta headers -- LiteLLM may reject anthropic-beta headers. Fix: CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1
2. Model name mismatch -- model: sonnet resolution may not match LiteLLM config. Test first.
3. Hard-stop hook blocks commands with DATABASE_URL literally -- even grep. Narrow the pattern.
4. Cost tracking needs explicit model listing -- wildcard routing unsupported for budgets.
5. Non-Anthropic passthrough streaming + tool calls may fail. Not relevant here.

---

## Implementation Plan

### Target Architecture

Stage 0.5: critic (DeepSeek) + gpt-critic (GPT-5.5) + claude-critic (Claude Sonnet) -> 3-way merge
Stage 2:   verifier (DeepSeek) + gpt-verifier (GPT-5.5) + claude-verifier (Claude Sonnet) -> 3-way merge

Data flow: Claude Code -> ANTHROPIC_BASE_URL:4000/v1/messages -> LiteLLM auth -> budget check -> api.anthropic.com

### Budget

| Model | Monthly Cap | Purpose |
|-------|------------|---------|
| Sonnet 4.6 | $25 | Primary QC (~$0.20/WB, 125+/month) |
| Opus 4.5 | $15 | Reserve for critical reviews |
| Haiku 4.5 | $10 | Light checks |

### Files to Create (3)

1. docker/litellm/docker-compose.yml
2. docker/litellm/config.yaml
3. docker/litellm/.env.litellm.example

### New Agent Definitions (2)

4. .claude/agents/claude-critic.md -- model: sonnet, read-only, skills: critic-review, color: cyan
5. .claude/agents/claude-verifier.md -- model: sonnet, read-only, skills: verifier + security-verification-gate, color: magenta

Both reason DIRECTLY as Claude Sonnet -- no Codex MCP delegation. Advisory only (cannot BLOCKED).

### Files to Modify (10)

6. .claude/settings.json -- add env block (ANTHROPIC_BASE_URL, AUTH_TOKEN, beta flags)
7. .agent/ROSTER.md -- 2 new agent rows
8. .agent/skills/merge-protocol/SKILL.md -- 3-way conflict resolution rules
9. CLAUDE.md -- Dual-model -> Tri-model QC
10. docs/templates/consolidation-report-template.md -- 3 agent columns
11-14. .claude/agents/{critic,verifier,gpt-critic,gpt-verifier}.md -- update diagrams
15. memory-bank/review-log.md -- 2 new rows

### 3-Way Merge Rules

| Distribution (3 agents) | Result |
|---|---|
| All PASS/APPROVE | PASS/APPROVE |
| 2 PASS, 1 ISSUES/SUPPLEMENT | ISSUES/SUPPLEMENT wins |
| 2 PASS, 1 BLOCKED/RECONSIDER | BLOCKED/RECONSIDER wins |
| Any 1 BLOCKED | BLOCKED wins |
| 3-way split (APPROVE/SUPPLEMENT/RECONSIDER) | ESCALATE to Control Tower |
| Any 1 UNVERIFIED | Log gap, proceed with 2 |

### Risks

| Risk | Mitigation |
|------|-----------|
| Beta headers rejected | CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 |
| Model name mismatch | Test first; fallback to explicit version |
| LiteLLM not running | Agent -> UNVERIFIED; CT proceeds with 2-model |
| Budget exceeded | LiteLLM 429; fallback to 2-model |

---

## Smoke Test Evidence Pattern

Dual-model QC should be tested with tightened agent tools:

- `gpt-critic`: Codex MCP only, read-only shell access, report artifact required.
- `gpt-verifier`: Codex MCP only, read-only shell access, report artifact required.

Expected validation signal:

- GPT critic can challenge the native Control Tower plan.
- GPT verifier can find implementation defects missed by the native verifier.
- Cross-family findings are consolidated before closeout.
- Session IDs, project names, defect details, and token counts stay in private
  project logs, not in the public framework repository.
