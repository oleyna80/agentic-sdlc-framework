# Agent Routing Roster

This compact roster routes framework lifecycle work. It is subordinate to
[`AGENTS.md`](../AGENTS.md), accepted governance, the active Work Block,
and the approved write-set. It is an operational index, not a replacement for
the Portable Kit's accepted separate-role ADR or a runtime/model catalog.

| Role | Outcome | Boundary | Procedure route |
| --- | --- | --- | --- |
| Orchestrator | Scope, gates, evidence, next action | Does not implement during Coder step | `task-decomposition` |
| Architect / Analyst | Read-only recommendation | Cannot approve/write outside scope | `architecture-discovery` |
| Critic | Pre-execution challenge | Read-only | `critic-review` |
| Coder | Approved implementation and evidence | One writer for the write-set | `scoped-coder` |
| Reviewer | Frozen-subject review | Read-only; no silent repair | `reviewer` |
| Verifier | Reproducible acceptance verdict | Read-only except expressly approved evidence docs | `verifier` |

Temporary Product, Architecture, Frontend, Backend, Design, Security, QA, or
Docs Analyst labels only narrow a research lens; they never expand base-role
authority.

For non-trivial delegation, use the mission brief template and state role,
specialization, scope, exclusions, authorities, allowed procedure, file-change
permission, expected output, isolation, and Hard Stops. Inspect live capability
evidence before assigning a role: unknown is unavailable. Cost is considered
only among choices meeting required authority, write permission, isolation,
assurance, and Hard Stops. A skill supplies procedure, not authority.

Sequential reuse is not independent assurance. Where the profile does not
permit a documented degraded fallback, stop rather than claim independence.
