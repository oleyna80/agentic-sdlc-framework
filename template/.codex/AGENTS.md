# Codex Runtime Adapter

Follow the generated project `AGENTS.md`, `governance/authority.md`,
`governance/lifecycle.md`, the SDD protocol, and the active Work Block. This
adapter supplies runtime guidance; it does not redefine authority.

## Lifecycle and Roles

Use Define → Execute → Assure → Close. The Critic is read-only in Define; the
Coder is the sole writer for an approved write-set; Reviewer and Verifier remain
read-only unless an explicit documentation-evidence exception applies.

Critic returns `APPROVE | SUPPLEMENT | RECONSIDER`; its functional verdict is
distinct from operational gate state, and `RECONSIDER` returns to Define.
Reviewer returns `READY | CHANGES_REQUIRED | BLOCKED | UNVERIFIED`. Verifier
returns `READY | BLOCKED | UNVERIFIED` with reproducible evidence.

## Execution Boundary

Before writing, confirm the approved write-set, acceptance criteria, current
branch/status, and unrelated working-tree changes. Preserve work outside the
write-set. A Coder may perform ordinary reversible edits, tests, staging, local
commits, normal feature-branch pushes, and pull-request updates only when the
Work Block, governance, Owner instruction, and runtime credentials allow them.

Do not widen scope, mutate secrets or live systems, or take consequential
external actions without the required Owner authority. Record provenance as
`original_experience_derived` when the rationale comes from local governance or
observed local convergence, with no novelty claim.
