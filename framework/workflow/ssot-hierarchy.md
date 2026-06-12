# SSOT Hierarchy

> Single Source of Truth — conflict resolution order.

---

When sources of truth conflict, resolve in this order:

1. **`docs/tasklist/`** — active tasks with acceptance criteria (highest priority)
2. **`docs/plans/`** — approved plans
3. **`docs/specs/`** — specifications
4. **`docs/reports/`** — verification and closeout reports
5. **`memory_bank/`** — context, progress, decisions (lowest priority)

## Rules

- Tasklist beats plan: if a task says "changed approach", the plan is stale
- Plan beats spec: if the plan revised the spec, the plan is current
- Memory bank is a cache, not a contract: always verify against docs/
- Update higher-priority sources before lower ones when resolving conflicts

## When to Update

- **Tasklist:** After every Stage 3 (Sync & Report)
- **Plans:** When the approach changes during implementation
- **Specs:** When requirements change
- **Memory bank:** After verified closeouts only
