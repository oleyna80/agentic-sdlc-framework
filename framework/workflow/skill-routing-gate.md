# Skill Routing Gate

> How to find and route to the right skill for any task.

---

## The 4-Step Gate

Before non-trivial, Hard Stop, ops, DB, deploy, security, runtime, multi-domain,
or subagent-delegated work:

1. **Inspect** `.agent/ROSTER.md` for routing-critical skills
2. **Search** `.agent/skills/*/SKILL.md` for matching `## Triggers` or `## When to Use`
3. **State:** `Skills checked` / `matched` / `used` / `skipped and why`
4. **Record** in Stage 0 Preflight

## Skip Reasons

Skipping a matching skill requires a recorded reason:
- `trivial` — task too simple for the skill
- `blocked` — skill tooling unavailable
- `hard-stop` — would require unapproved side effect
- `user-disabled` — Owner requested no skills for this Work Block

## Hard Stop Skills

Some skills gate Hard Stop operations. These always require explicit Owner
approval, even if the skill matches. The skill may run analysis but may NOT
execute the Hard Stop action without approval.

## External Skill Discovery

For unfamiliar domains, public/vendor skill libraries may be used as research
inputs only. They never expand: approved scope, file-change authority, tool
authority, DB authority, or Hard Stop boundaries. Verify source, license, and
side effects before adapting.
