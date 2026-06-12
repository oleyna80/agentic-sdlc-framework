# Git Workflow

> Commit style and branch strategy for Agentic SDLC projects.

---

## Commit Style

```bash
# Good — Short, descriptive
fix: remove duplicate /api/v1 in endpoints
feat: add WebSocket reconnection logic
refactor: extract validation helpers to separate module

# Avoid — Vague or too long
update files
fixed some bugs
```

## Branch Strategy

- `main` — stable production
- `dev` — active development
- `fix/bug-name` — bug fixes
- `feat/feature-name` — new features

## Before Commit

- Code works locally
- No `console.log()` or debug prints
- Tests pass (if exist)
- No unused imports
- `scripts/secret-scan.sh staged` clean (for security-sensitive changes)
- Crash Test Gate passed (for route/navigation changes)
