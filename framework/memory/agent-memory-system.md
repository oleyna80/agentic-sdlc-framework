# Agent Memory System

> Persistent, file-based memory for custom agents.
> Builds institutional knowledge across Work Blocks.

---

## Memory Types

### user
Information about the user's role, goals, responsibilities, knowledge.
**When to save:** learning user preferences, role, expertise.
**How to use:** tailor responses to the user's perspective.

### feedback
Guidance from the user about how to approach work — corrections AND confirmations.
**When to save:** user corrects approach ("don't do X") OR confirms a non-obvious approach worked.
**Body structure:** Rule → **Why:** → **How to apply:**

### project
Ongoing work, goals, initiatives, bugs, incidents — not derivable from code or git.
**When to save:** learning who is doing what, why, or by when. Convert relative dates to absolute.
**Body structure:** Fact/decision → **Why:** → **How to apply:**

### reference
Pointers to external resources (dashboards, issue trackers, Slack channels).
**When to save:** learning about resources in external systems.

### failure-pattern (Verifier only)
Recurring patterns of failures found during verification.
**When to save:** encountering a failure that seems systemic or has happened before.
**How to use:** prioritize these checks first in future verifications.

### contract-sensitive (Verifier only)
Files/modules where contracts consistently drift from implementation.
**When to save:** discovering a module with chronic contract mismatches.
**How to use:** always cross-reference these files in relevant verifications.

---

## Memory File Format

```markdown
---
name: <short-kebab-case-slug>
description: <one-line summary for relevance matching>
metadata:
  type: <user|feedback|project|reference|failure-pattern|contract-sensitive>
---

<memory content. Link related memories with [[their-name]].>
```

## MEMORY.md Index

Each memory gets a one-line entry in `MEMORY.md`:
`- [Title](file.md) — one-line hook`

- `MEMORY.md` is an index, never write memory content there
- Keep entries under ~150 characters
- After 200 lines, older entries may be truncated

## What NOT to Save

- Code patterns, architecture, file paths — derivable from current project state
- Git history — `git log` / `git blame` are authoritative
- Fix recipes — the fix is in the code; the commit has context
- Anything in CLAUDE.md files
- Ephemeral task details from a single run

## Before Recommending from Memory

- If a memory names a file path: check the file exists
- If a memory names a function or flag: grep for it
- "The memory says X exists" ≠ "X exists now"
- If a recalled memory conflicts with current information, trust what you observe now
