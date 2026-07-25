# OpenCode Runtime Adapter

## Status

Experimental. OpenCode may be used as an executor, reviewer, or alternate
orchestrator only after project-local capability and provider smoke tests.

The framework must not assume that a feature exists merely because OpenCode can
access a model provider or tool. Record observed runtime behavior, permissions,
agent configuration, and effective models.

## Intended Uses

- bounded implementation with an approved write set;
- read-only discovery or review;
- alternate provider/model evaluation;
- cross-runtime second opinion;
- experimental orchestration where native agent behavior is verified.

## Adapter Responsibilities

A production-ready adapter should provide:

- installation and version record;
- role-to-agent mapping;
- provider and model-class mapping without credentials;
- permission and write-boundary configuration;
- skills and command integration;
- structured artifact output;
- fallback behavior;
- repeatable smoke tasks;
- limitations compared with the selected governance profile.

## Capability Policy

Start with all untested capabilities marked `unknown`.

```yaml
runtime: opencode
status: experimental
capabilities:
  native_subagents: unknown
  custom_agent_profiles: unknown
  separate_readonly_context: unknown
  workspace_write_sandbox: unknown
  hooks_or_policy_interception: unknown
  skills: unknown
  mcp: unknown
  parallel_read: unknown
  parallel_write: unknown
  worktrees: unknown
```

Upgrade a value only after an evidence-backed test in the target environment.
Provider access alone does not demonstrate orchestration, isolation, or policy
enforcement.

## Existing Research

Current background material remains under:
`framework/knowledge/opencode-runtime.md`.

That file is reference knowledge and does not override governance or project
runtime state.
