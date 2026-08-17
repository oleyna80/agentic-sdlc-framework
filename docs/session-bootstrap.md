# Session Bootstrap — Framework Maintenance

Use this guide when starting or resuming non-trivial work **on the Agentic SDLC
Framework repository itself**. Generated consumer projects use the separate
`template/docs/session-bootstrap.md` that is copied during bootstrap.

The goal is progressive disclosure: load enough current context to work safely
without reading the entire repository or carrying historical implementation
narrative into every session.

## Always read for non-trivial framework work

1. root `AGENTS.md` and the current Owner instruction;
2. active Work Block/current task and governing specification/ADR when present;
3. current branch, commit, status, and relevant diff;
4. `PROJECT_MAP.md` when repository structure or migration state matters.

Do not load every registry, runtime adapter, skill, memory file, or assurance
report by default.

## Read conditionally

- `governance/*` for authority, lifecycle, artifact, evaluation, or capability
  rules affected by the task;
- `.agent/workflows/sdd-protocol.md` for detailed self-hosting stage semantics;
- `.agent/ROSTER.md` and `.agent/skills/README.md` for role/procedure routing;
- the matching `skills/<skill>/SKILL.md` only when its trigger applies;
- `bootstrap/profiles.json` and bootstrap/validation code when installation
  composition changes;
- runtime/integration adapters only when the task affects them;
- `FILE_REGISTRY.yml` for canonical path/authority classification;
- relevant engineering memory for reusable rationale or known failure patterns;
- relevant reports/evidence when verifying a prior claim or current gate.

Current higher-authority source always outranks memory and historical evidence.

## Framework preflight

Before implementation, answer briefly:

- What exact result is required?
- Is this read-only analysis or an authorized mutation?
- Which specification/ADR/Work Block governs it?
- Which files are normative, derived/configuration, evidence, generated, or
  local operational state?
- What paths are explicitly writable?
- Are there unrelated dirty/untracked changes to preserve?
- Does the change affect governance, templates, installation profiles, runtime
  adapters, integrations, skills, publication, or generated-project behavior?
- Which deterministic checks and assurance functions are required?
- Are there external Hard Stops or capabilities the normal agent must not hold?
- Is the proposed solution the simplest sufficient one for the actual risk and
  scale?

If the proposal materially increases complexity, compare it with a simpler
alternative before implementation. Use
`docs/engineering-memory/engineering-decision-principles.md` for the detailed
decision posture.

## Role and procedure routing

Use `governance/authority.md` for role authority, `.agent/ROSTER.md` for routing,
and `.agent/skills/README.md` for the procedure index.

Do not restate a full skill inside the session record. Record which procedure was
used and any material limitation. Unknown/unverified runtime capability is not
assumed available.

## Repository state record

```text
Stage:
Objective:
Expected result:
Role/function:
Governing specification/ADR:
Work Block:
Scope / exclusions:
Write-set:
Branch / commit:
Git status / unrelated work:
Affected repository layers:
Runtime/integration capability needed:
External Hard Stops:
Required checks / assurance:
Relevant files read:
Next action:
```

Inspect relevant uncommitted diffs before planning edits. Never stage, overwrite,
or discard unrelated work silently.

## Capability and security check

Separate process permission from technical capability.

For any runtime/tool used, record only what matters to the task:

- available / unavailable / unknown;
- relevant version/config/auth/smoke evidence;
- actual isolation;
- fallback and residual limitation.

Normal reversible feature-branch development is governed by the active Work
Block/write-set and repository process. Consequential production, live-data,
credential, destructive, protected-branch, irreversible-publication, and real
client-facing actions require the applicable externally controlled capability.

Historical rationale for earlier authority mechanisms is kept in engineering
memory and closeout evidence rather than this startup guide.

## Structural impact check

When adding or redefining an important path or contract, inspect the affected
subset of:

- root `AGENTS.md`, `PROJECT_MAP.md`, and `FILE_REGISTRY.yml`;
- Governance Core and accepted ADRs/specifications;
- `bootstrap/profiles.json`, bootstrap engine, generated defaults, and profile
  validation fixtures;
- `template/AGENTS.md`, template workflow/skills, and generated-project docs;
- runtime/integration adapters and conformance tests;
- publication/privacy rules;
- engineering memory and user-facing documentation.

Related files indicate impact, not automatic permission to edit them.

## Evidence and memory

- evidence must be reproducible and bound to the subject it claims to verify;
- unavailable checks remain unavailable/unverified, never silently passed;
- durable rationale, lessons, and recurring failure patterns belong in
  `docs/engineering-memory/`;
- temporary progress belongs in `memory_bank/`;
- raw transcripts, hidden reasoning, secrets, and protected payloads do not
  belong in either location.

At closeout, state changed files, checks run/skipped, assurance result, residual
risk, reusable knowledge classification, and the next action.
