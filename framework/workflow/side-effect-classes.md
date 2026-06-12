# Side-Effect Classes

> Classify non-trivial work before execution. The class controls who may act
> and whether Owner approval is required.

---

| Class | Examples | Authority |
|---|---|---|
| Read-only | file inspection, `git diff`, logs with sanitized output | Orchestrator, Reviewer, Verifier |
| Local docs/workflow write | `.agent/*`, `memory_bank/*`, `docs/tasklist/*` | Control Tower inside approved scope |
| Production code write | `src/*`, `app/*`, `scripts/*` | Scoped Coder inside approved write-set |
| Local/test side effect | temp DB, local dev server, local test artifacts | Approved Work Block; no live data |
| Public repo side effect | commit, push, release tag | Explicit Owner approval |
| Live infra side effect | deploy, Docker push/pull, service restart | Hard Stop approval |
| Live data side effect | live DB migration, live DB write, manual row change | Hard Stop approval |
| Client-facing side effect | email/SMS/messaging API/client notification | Hard Stop approval |
| Destructive side effect | `reset --hard`, `git clean`, force push, delete/drop | Hard Stop approval |

## Usage

Before executing any non-trivial action, classify it into one of these 9 classes.
The class determines:
1. Whether the action is allowed at all
2. Which role may perform it
3. Whether Owner approval is required

If you're unsure which class applies → escalate to Control Tower before acting.
