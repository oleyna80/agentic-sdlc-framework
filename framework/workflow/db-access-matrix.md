# DB Access Matrix

> Controls how agents interact with databases. Use before any DB command,
> migration, or verification gate.

---

| DB action mode | Allowed | Forbidden |
|---|---|---|
| `none` | No DB access needed | DB commands, credentials, schema assumptions |
| `local_temp` | temp/local DB smoke, test migrations, disposable data | live DB, real credentials |
| `live_readonly` | Owner-approved sanitized schema/status inspection | writes, DDL, migrations, row dumps |
| `live_migration_apply` | Owner-approved migration files, stop-on-error | arbitrary/destructive SQL |
| `runtime_app` | app writes through reviewed code paths | LLM/manual direct DB mutation |
| `emergency_remediation` | separately approved remediation Work Block | implicit fixes, exploratory writes |

## Runtime Agent DB Boundary

Agents are untrusted planners, not trusted DB executors. In runtime product
flows, an agent may propose a structured action, prepare a draft, summarize
data, or request a read-only view through an approved API. It must not hold DB
credentials, execute raw SQL, mutate rows, or call unrestricted internal tools.

All DB writes must pass through trusted application code:

1. Agent proposes an `ActionSpec` or equivalent structured request.
2. Backend validates user/session authority, resource scope, payload shape, and
   business invariants.
3. Policy logic decides `deny`, `read-only`, `requires_approval`, or
   `execute`.
4. User/admin approval is collected for risky mutations with a concrete diff
   or preview.
5. Backend service/repository code executes the allowed operation in the
   expected transaction/idempotency/audit context.

Prompt instructions are advisory only. They never replace backend policy,
typed service boundaries, audit logs, idempotency, or transaction handling.

## How to Use

1. Classify the DB action mode BEFORE any DB-related command
2. Record it in the Stage 0 Preflight
3. If the required mode needs Owner approval → Hard Stop
4. Never assume DB access because you can run `psql` or see `DATABASE_URL`
5. For runtime product features, document the backend executor and policy/audit
   path before allowing any agent-proposed mutation

## Common Mistakes

- Running `prisma migrate dev` on a live DB (should be `local_temp`)
- Querying live data for debugging (should be `live_readonly` with approval)
- "Just checking the schema" against a production DB without approval
- Letting an agent write SQL or call DB tooling directly because the prompt
  says it will be careful
