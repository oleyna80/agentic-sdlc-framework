# Agent Definition Guide

> How to create custom Claude Code agents following the framework pattern.

---

## Agent File Structure

Agents live in `.claude/agents/<name>.md`. Each agent has frontmatter and body.

### Frontmatter

```yaml
---
name: "agent-name"
description: "When to use this agent — triggers and examples"
tools: Bash, Read, LSP, ...     # Allowed tools
skills: skill-a, skill-b        # Skills this agent can invoke
model: inherit                  # Model override (usually inherit)
color: green|red|blue|yellow   # Display color
memory: project                 # Memory scope
---
```

### Body Structure

1. **Role definition** — who you are in the SDLC
2. **Mission** — what you do, what you produce
3. **Methodology** — step-by-step process
4. **Output format** — structured template for reports
5. **Rules of conduct** — boundaries, constraints, style
6. **Obstacle reporting** — what to do when blocked
7. **Work Block integration** — how Control Tower uses your output
8. **Persistent agent memory** — memory types and how to use them

## Agent Types

### Solution Architect (read-only)
- **Role:** Pre-implementation research
- **Tools:** Read, Bash (read-only), LSP, WebFetch, WebSearch, Context7
- **Skills:** architecture-discovery, technical-discovery, project-estimation, task-decomposition
- **Output:** Solution Architect Report

### Verifier (read-only)
- **Role:** Post-implementation verification gate
- **Tools:** Read, Bash, LSP, IDE diagnostics
- **Skills:** verifier, security-verification-gate
- **Output:** Verifier Report with READY/BLOCKED verdict

## Key Design Rules

1. **Explicit boundaries** — list allowed AND forbidden actions
2. **Structured output** — define exact format (ideally JSON Schema)
3. **Obstacle protocol** — never guess, report blockers with evidence
4. **Memory system** — persistent memory for institutional knowledge
5. **SDLC integration** — document how Control Tower uses the output
