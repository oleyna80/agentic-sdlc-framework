# Intentional Friction Policy

> Why AI agents must slow down before generating code.

---

## The Problem

AI agents are fast. Speed is not the default success metric. An agent that
generates code quickly can produce:
- Over-engineered solutions that are hard to maintain
- Changes that don't address the real user outcome
- Code that ignores existing patterns and helpers
- Work that creates more maintenance cost than value

## The Policy

Before non-trivial implementation, the Orchestrator must answer 6 questions:

1. **What user or technical outcome** is this change meant to create?
2. **What is the smallest approved write-set** that can produce that outcome?
3. **What existing implementation, pattern, helper, or skill** should be reused?
4. **What test or verification evidence** will prove the change worked?
5. **What rollback or recovery path** exists if the change is wrong?
6. **Who maintains the result later**, and is the new code/abstraction worth that cost?

## When to Apply

- **Full 6 questions:** Non-trivial features, refactoring, API changes, DB changes, 3+ files
- **Quick self-check (one-liner):** Typo fixes, single-line changes, trivial tweaks

## High-Risk Areas

For these areas, the Orchestrator should explicitly challenge timing and
rollback assumptions before seeking approval:
- Deploy
- Auth
- Payments
- Database
- Secrets
- External communications
- Production config

## Anti-Patterns

- "The user asked for it so I built it" — without checking scope and reuse
- "It compiles so it's done" — without verification evidence
- "I'll add this helper just in case" — speculative abstraction
- "It's a quick fix" — for changes touching security, DB, or deploy
