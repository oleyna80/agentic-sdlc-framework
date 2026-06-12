# Structural Authority Model

> Authority is structural, not prompt-based.

---

## The Four Boundaries

An agent may only act when ALL four boundaries allow it:

1. **Base role:** Orchestrator, Coder, Reviewer, or Verifier.
2. **Approved Work Block scope and write-set.**
3. **Side-effect class.**
4. **Explicit Hard Stop approval** (when required).

## What Does NOT Expand Authority

- Temporary specialization (e.g., "Security Analyst" narrows focus, doesn't add write access)
- Tool availability (having `psql`, `ssh`, `docker`, `curl`, MCP tools, or vendor CLIs)
- Skill assignment (a skill routes work, doesn't grant permissions)
- Model capability (a smarter model doesn't get more authority)

## Role Definitions

| Role | Write Authority | Key Constraint |
|---|---|---|
| Orchestrator | `.agent/*`, `docs/*`, `memory_bank/*` | Plans and delegates, doesn't implement |
| Coder | Approved write-set only | One Coder per write-set |
| Reviewer | None (read-only) | Reports findings, doesn't fix |
| Verifier | `docs/reports/*` | Issues BLOCKED/READY, doesn't fix |

## Temporary Specializations

Agents may receive a temporary specialization (e.g., `Architecture Analyst`,
`Security Analyst`, `Backend Coder`). The specialization narrows focus and
skill routing; it does NOT create a new authority level. File-change authority
always comes from the base role.
