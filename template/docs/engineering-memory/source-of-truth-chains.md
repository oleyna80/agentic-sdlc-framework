# Source-of-Truth Chains

Use this file to prevent project drift. Each row answers: where should a future
agent look first when the project has conflicting information?

| Question / Domain | Highest Authority | Supporting Sources | Operational Evidence | Last Verified |
|---|---|---|---|---|
| Agent operating contract | `AGENTS.md` | `PROJECT_MAP.md`, `FILE_REGISTRY.yml` | `memory_bank/orchestrator-log.md` | [YYYY-MM-DD] |
| Work Block scope and acceptance | current `docs/plans/**` Work Block | `docs/tasklist/**`, `docs/specs/**` | `docs/reports/**`, `memory_bank/progress.md` | [YYYY-MM-DD] |
| Durable engineering memory | `docs/engineering-memory/README.md` and related entries | `framework` or project docs | closeout reports | [YYYY-MM-DD] |

Add rows only for domains that future agents repeatedly need to resolve.
