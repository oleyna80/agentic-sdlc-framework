# User Profile Template

> Copy to your global `CLAUDE.md` and customize.
> This defines who you are and how AI agents should work with you.

---

## 👤 About Me

**Role:** [Your role — e.g. Senior Product Manager, Fullstack Developer, Technical Lead]

**Experience:**
- [Domain 1]
- [Domain 2]
- [Domain 3]

**My Approach:**
- Break tasks into stages
- Ask clarifying questions before coding
- Short, concrete instructions
- Wait for confirmation on the Work Block plan, then execute autonomously (Hard Stops only)
- Keep it simple — no over-engineering

**Communication Style:**
- Short answers (no essays)
- Step-by-step execution
- Concrete examples over theory
- "Explain simpler" is always OK
- Ask "what does this mean?" anytime

---

## 💰 Budget & Token Management

**Monthly Budget:** [Your budget]

**Cost Control:**
- Minimize token usage where possible
- Concise code comments (avoid verbose docstrings unless needed)
- Use short variable names when context is clear
- Don't repeat yourself — reference previous context
- Ask before large refactors that use many tokens

**When to be verbose:**
- Critical business logic
- Complex algorithms
- Public APIs
- Security-sensitive code

---

## 🎯 Task Prioritization

| Level | When |
|---|---|
| 🔴 CRITICAL | Blocking work, production broken — fix immediately |
| 🟡 HIGH | Important feature, user-facing — plan carefully |
| 🟢 MEDIUM | Nice to have, optimization — can wait |
| ⚪ LOW | Future enhancement, refactor — defer if time-constrained |

---

## 📝 Code Review Checklist

- [ ] Code runs without errors
- [ ] No unused imports/variables
- [ ] Type hints (Python) / Types (TypeScript)
- [ ] Error handling for expected failures
- [ ] Minimal comments (code should be self-documenting)
- [ ] No hardcoded values (use env vars or config)
- [ ] Git commit with clear message
- [ ] Manual testing done

---

## 🤖 Multi-Agent & Subagent Context

**Subagent defaults (from AGENTS.md):**
- Subagents used by default for multi-domain, 4+ file, production/runtime/security/deploy/DB, or 3+ directory work
- Default permitted subagent classes: read-only Reviewer, Verifier, Analyst; one write-capable Coder per write-set
- Subagent output is evidence, not acceptance — Control Tower validates before accepting

**Skill routing:**
- Check `.agent/ROSTER.md` before non-trivial Work Blocks
- Match and invoke project-local skills from `.agent/skills/*/SKILL.md`
- Record skills checked, matched, used, and skipped in the Work Block

---

## Notes for AI Agents

- Proactive suggestions appreciated but ask before big changes
- Short responses preferred
- Use examples when explaining
- "I don't know" is fine — we'll figure it out together
- Cost-conscious = happy, verbose = concerned
