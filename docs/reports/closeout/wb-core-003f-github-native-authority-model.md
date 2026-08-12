---
schema_version: 1
artifact_type: closeout_report
artifact_id: wb-core-003f-github-native-authority-model-closeout
status: approved
owner_role: orchestrator
work_block_id: WB-CORE-003F
created_at: 2026-08-12
last_verified: 2026-08-12
---

# WB-CORE-003F — GitHub-Native Authority Model Closeout

## Final State

- **Stage execution state:** completed
- **Review verdict:** READY
- **Verification verdict:** READY
- **Drift verdict:** ALIGNED
- **Closeout classification:** SUCCESS
- **Task status:** completed
- **Evaluation verdict:** SKIPPED — deterministic governance/control-plane contract migration; no nondeterministic model-output benchmark is part of acceptance
- **External VCS state:** non-normative; hosting-platform lifecycle is outside repository SSOT

## Result

WB-CORE-003F completes the framework's migration away from per-Work-Block
SSH-signed authorization as the normal development security boundary.

The completed contract now distinguishes two layers:

- **process guardrails** — Work Block scope, exact write-set, Critic/Reviewer/
  Verifier functions, runtime-local hooks, integration admission, staged-commit
  checks, and deterministic verification;
- **consequential security authority** — externally controlled GitHub repository
  rules, least-privilege credentials, workflow permissions, OS isolation, and
  separately held production/VPS/database/secret capabilities.

Normal scoped source work no longer requires an Owner private signing key,
`ssh-keygen`, `allowed_signers`, an authorization-bootstrap commit, or detached
`.sig` files. Historical signed records may remain as audit evidence but do not
grant current schema-v3 authority.

The implementation also hardened the cooperative local boundary: direct
protected/default-branch pushes, force/history rewriting, remote branch deletion,
broad/mirror/prune pushes, external tag publication, destructive Git/filesystem
operations, live infrastructure/data mutation, credential operations, direct
external image publication, and configured client-facing communications remain
outside the normal agent channel.

Codex and Claude Code enforce source/write-set and staged-commit discipline for
supported mutation paths. OpenCode retains role-specific permission separation.
Lifecycle success-closeout fails closed until required assurance is resolved.

## Identity Reconciliation

Repository discovery during closeout found that the accepted Portable Kit
sequence already reserves `WB-CORE-004` for installer and packaging, followed by
WB-CORE-005 synthetic dry run, WB-CORE-006 HardwareLab pilot, and WB-CORE-007
promotion/legacy archive.

The authority-model work is therefore canonically recorded as **WB-CORE-003F**,
the next unused inserted governance/control-plane follow-up after
WB-CORE-003A—WB-CORE-003E. This correction preserves the accepted product roadmap
instead of silently repurposing or renumbering it.

`PROJECT_MAP.md` and `FILE_REGISTRY.yml` now project the same completed
WB-CORE-003F lifecycle state, with no active implementation Work Block and
WB-CORE-004 still the next planned product Work Block.

## Assurance Summary

The logical Critic pass identified and drove correction of four issues before
terminal closeout:

- premature lifecycle success-closeout with unresolved assurance;
- incomplete broad/tag Git push classification;
- Claude Code Bash mutation bypass of Work Block write-set scope;
- Claude runtime documentation drift from the schema-v3 authority model.

The final Reviewer, Verifier, and Drift reports are stored in the canonical
report directories and explicitly label their same-session connector-backed
isolation. They are not represented as independent human or separate-runtime
assurance.

Deterministic repository CI remains the executable contract evidence for syntax,
runtime/profile conformance, integration admission, Codex/Claude control-plane
fixtures, governance structure, release-state reconciliation, publication, and
disposable generated-project bootstrap.

## Residual Risks and Limitations

- Project-local hooks are cooperative and mutable by the same OS principal. They
  must not be treated as cryptographic or operating-system isolation.
- Git command pattern guards provide defense in depth rather than a complete
  semantic parser for every possible local Git configuration. Protected
  repository rules remain the authoritative default-branch boundary.
- Runtime-specific user/enterprise configuration can change effective Claude
  Code, Codex, or OpenCode permissions; target-environment smoke evidence is
  still required when a consumer project depends on stronger runtime assurance.
- The final Reviewer/Verifier/Drift passes for this closeout are same-session
  connector-backed assurance, not independent human or separate-runtime review.
- Historical records may retain the provisional Work Block identifier in commit
  history. Repository SSOT uses WB-CORE-003F and reserves WB-CORE-004 for the
  accepted product sequence.

## Follow-Up Work

- Begin WB-CORE-004 only as the separately scoped installer and packaging Work
  Block defined by the accepted Portable Kit roadmap.
- Consumer projects adopting schema v3 should move production workflow-dispatch,
  VPS/database access, and production secrets outside the normal agent credential
  before relying on the capability-boundary model for consequential operations.
- Run target-environment runtime smoke checks when a project requires stronger
  evidence than static/generated-project conformance.
