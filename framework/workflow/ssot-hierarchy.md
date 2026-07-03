# SSOT Hierarchy

> Single Source of Truth — conflict resolution order.

---

When sources of truth conflict, resolve in this order:

1. **`docs/tasklist/`** — active tasks with acceptance criteria (highest priority)
2. **`docs/plans/`** — approved plans
3. **`docs/specs/`** — specifications
4. **`docs/reports/`** — verification and closeout reports
5. **`docs/engineering-memory/`** — durable project engineering memory
6. **`memory_bank/`** — operational context, progress, and logs

## Rules

- Tasklist beats plan: if a task says "changed approach", the plan is stale
- Plan beats spec: if the plan revised the spec, the plan is current
- Engineering memory preserves durable context, but current approved task,
  plan, spec, or report files still beat it
- Memory bank is operational context, not a contract: always verify against
  docs/
- Update higher-priority sources before lower ones when resolving conflicts

## When to Update

- **Tasklist:** After every Stage 3 (Sync & Report)
- **Plans:** When the approach changes during implementation
- **Specs:** When requirements change
- **Engineering memory:** When reusable project knowledge should survive beyond
  operational logs
- **Memory bank:** After verified closeouts only
