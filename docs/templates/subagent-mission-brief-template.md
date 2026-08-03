# Subagent Mission Brief Template

Use for non-trivial delegated work. It narrows an assignment and does not
transfer Owner authority or override `AGENTS.md`, accepted governance, the SDD
protocol, or the active Work Block.

## Identity and outcome

- **Work Block:**
- **Lifecycle stage:** Define / Critic gate / Execute / Assure / Close
- **Base role:** Orchestrator / Architect or Analyst / Critic / Coder / Reviewer / Verifier
- **Temporary specialization:** none, or one bounded analyst lens
- **Objective:**
- **Expected handoff:** findings, recommendation, patch, review, or verification verdict
- **Return to:**

## Scope and authority

- **In scope:**
- **Out of scope:**
- **Required inputs:** relevant `AGENTS.md`, active Work Block, accepted
  specification/ADR, applicable governance/SDD contract, and needed memory.
- **Selected procedure:**
- **Live capability evidence:** available / unavailable / unknown, with source.
- **Required isolation and assurance:**

## Permission boundary

```text
File-change permission: none by default
Approved write-set: <exact paths, or none>
Writer ownership: <one named Coder, or not applicable>
External side effects: prohibited / explicitly named and Owner-approved
Database or live data: prohibited / explicitly named and Owner-approved
```

An unknown capability is unavailable. Choose the least-cost option only from
options already satisfying role authority, write permission, required isolation
and independence, assurance, and Hard Stops. Do not treat runtime/model/tool
names as authority.

## Evidence, isolation, and hard stops

- **Required checks/evidence:**
- **Sibling assignments:** list scopes, or `none`.
- **Independence:** independent / same-context sequential / unavailable.
- **Expected response:** conclusion, evidence, changed files or `no files
  changed`, residual risks, and next action.

Stop and return before scope/write-set expansion, failed required check,
unresolved authority, dependency/configuration/secret/hook/runtime/CI change,
database/schema/deploy/live-system effect, destructive action, unrelated dirty
file collision, staging, commit, or push.
