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

## How to Use

1. Classify the DB action mode BEFORE any DB-related command
2. Record it in the Stage 0 Preflight
3. If the required mode needs Owner approval → Hard Stop
4. Never assume DB access because you can run `psql` or see `DATABASE_URL`

## Common Mistakes

- Running `prisma migrate dev` on a live DB (should be `local_temp`)
- Querying live data for debugging (should be `live_readonly` with approval)
- "Just checking the schema" against a production DB without approval
