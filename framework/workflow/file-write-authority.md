# File Write Authority

> Who can write to which paths. Enforced by role, not by tool capability.

---

| Path pattern | Who can write |
|---|---|
| `AGENTS.md`, `.agent/*`, `docs/specs`, `docs/plans`, `docs/tasklist`, `docs/templates/*`, `memory_bank/*` | Control Tower |
| `src/*`, `app/*`, `scripts/*` (project code) | Scoped Coder (within approved write-set) |
| `docs/reports/*` | Verifier, Scoped Coder (closeout reports) |
| `.env`, secrets, production infra | Owner only |

## Rules

- Write authority is defined by the approved write-set, not by what tools can do
- A Verifier with shell access is still read-only for source code
- A Coder may only write files listed in the approved write-set
- No scope expansion without re-approval
