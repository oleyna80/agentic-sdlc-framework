# Subagent Mission Brief Specification

> The standard format for delegating work to subagents.

---

## Required Fields

| Field | Description |
|---|---|
| Base Role | Orchestrator, Coder, Reviewer, or Verifier |
| Mission Role | Temporary specialization (Architecture Analyst, Security Analyst, etc.) |
| Skill(s) | Which skills to invoke, with rationale |
| Objective | One sentence — what must the subagent accomplish? |
| Scope / Out of Scope | Exact boundaries |
| Inputs / Files to Read | Must-read files before starting |
| Allowed Tools / MCP | Tool and MCP server whitelist |
| Approved Write-Set | Path patterns (empty for read-only) |
| Side-Effect Class | From AGENTS.md § Side-Effect Classes |
| DB Action Mode | From AGENTS.md § DB Access Matrix |
| Parallel Group | Other subagents running concurrently |
| Hard Stops | Which Hard Stops apply |
| Required Checks | Verification evidence to produce |
| Expected Output | Format, file path, schema |
| Acceptance Owner | Who receives and validates the output |

## Rules

1. **Output is evidence, not acceptance** — Control Tower validates before accepting
2. **Tool capability ≠ authority** — having a tool doesn't grant permission to use it
3. **No nested external AI** — subagents don't launch Codex, Claude, Gemini, etc.
4. **One Coder per write-set** — never two Coders touching the same files

## Example

```
Spawn agent: implement-contact-form

Base Role: Coder
Mission Role: Backend Coder
Skill(s): scoped-coder (implementation)
Objective: Implement contact form API route per approved spec

Scope: POST /api/contact route + validation + storage
Out of Scope: UI, email notifications, admin panel

Inputs:
- docs/specs/contact-form.md
- src/app/api/contact/route.ts (existing stub)

Approved Write-Set:
- src/app/api/contact/route.ts
- src/lib/contact/validation.ts
- src/lib/contact/storage.ts

Side-Effect Class: production code write
DB Action Mode: runtime_app
Hard Stops: None in scope

Required Checks:
- Route returns 200 on valid POST
- Route returns 400 on invalid body
- Types pass (npx tsc --noEmit)
- No secrets in diff

Expected Output: Implementation report with files changed + checks passed
Acceptance Owner: Control Tower
```
