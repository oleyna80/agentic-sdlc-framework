---
schema_version: 1
artifact_type: review_report
artifact_id: pr-5-final-review
work_block_id: wb-005
reviewed_revision: ea0bc918361b4ba9ce1dda8697e0a54ec7c68265
review_date: 2026-07-25
verdict: READY
reviewer_role: reviewer
---

# PR #5 Final Review — Profile-Aware Bootstrap and Runtime Conformance

## Scope

Reviewed the complete diff from `main` to
`agent/profile-aware-bootstrap-conformance`, including:

- installation-profile authority separation;
- profile catalog and scaffold engine;
- exact selected/unselected runtime surfaces;
- skill selection and mirrors;
- generated installation state and health validation;
- Git tracking and clone/restore behavior;
- transactional/fail-closed bootstrap behavior;
- Codex, Claude Code, OpenCode, and generic adapter semantics;
- integration safe defaults;
- CI, publication, maps, registries, setup, quickstart, and session bootstrap.

## Normative Baseline

- `docs/architecture/decisions/2026-07-25-runtime-neutral-control-plane.md`
- `governance/authority.md`
- `governance/lifecycle.md`
- `governance/artifacts.md`
- `governance/runtime-capabilities.md`
- `docs/plans/wb-005-profile-aware-bootstrap-conformance.md`

## Review Method

1. Inspected profile catalog, bootstrap engine, generated health check, validators,
   runtime agent/config files, ignore rules, documentation, and CI wiring.
2. Compared runtime-specific syntax through a normalized semantic contract:
   logical role, implementation/source write authority, model posture, Work Block
   authority source, consequential-action policy, and integration default.
3. Exercised all profiles and aliases in disposable projects.
4. Tested malformed catalog sources, unknown profiles, occupied/symlink targets,
   synthetic staged failure, Git tracking boundaries, clone/restore, repeated
   health checks, and blocked default state.
5. Ran the full Framework Contracts workflow on the reviewed revision.

## Resolved Findings

### F-01 — Installation profile was only documentation

**Severity:** High  
**Status:** Resolved

The previous bootstrap always copied the maximum runtime scaffold. Governance,
runtime, and integration profile terminology did not change generated
composition.

**Resolution:**

- added `bootstrap/profiles.json`;
- added canonical `core`, `codex`, `claude-code`, `opencode`, and
  `multi-runtime` profiles;
- added compatibility aliases;
- preserved `multi-runtime` as the default;
- recorded resolved composition in `.agent/bootstrap-profile.json`.

### F-02 — Installation composition could be confused with authority

**Severity:** High  
**Status:** Resolved

A runtime-specific scaffold risked being interpreted as authority to use that
runtime, its tools, or integrations.

**Resolution:**

- documented installation, governance, runtime, integration, model, and
  isolation as independent dimensions;
- added an explicit no-authority statement to generated profile state;
- kept Work Block gates and integration admission separate;
- conformance checks require `AGENTS.md` as the logical authority source.

### F-03 — Bootstrap could leave a partial target

**Severity:** High  
**Status:** Resolved

Copy or health-check failure after target creation could leave a partially
scaffolded project.

**Resolution:**

- validate manifest and source inventory before mutation;
- build and validate in a sibling temporary directory;
- publish through atomic rename;
- preserve absent/empty targets on synthetic staged failure;
- refuse non-empty targets.

### F-04 — Symlink target bypassed fail-closed target validation

**Severity:** High  
**Status:** Resolved

CLI path normalization used `.resolve()`, converting a symlink target to its real
directory before `is_symlink()` validation.

**Resolution:**

- create an absolute path without symlink dereference;
- reject symlink targets before staging;
- added an executable symlink fixture.

### F-05 — Catalog did not prove all declared source files existed

**Severity:** Medium  
**Status:** Resolved

The original manifest validation checked component roots and skills but not every
common or component-required source path.

**Resolution:**

- validate common sources, component roots, component required paths, duplicate
  lists, profile references, aliases, and skill sources;
- added missing-common and missing-component fixtures.

### F-06 — Generated health check mutated local state before validating portable state

**Severity:** Medium  
**Status:** Resolved

A damaged profile contract could create memory and Work Block state before the
health check failed.

**Resolution:**

- validate `.agent/bootstrap-profile.json` and selected/unselected surfaces
  before restoring any ignored operational files.

### F-07 — Portable control-plane files were hidden by blanket ignore rules

**Severity:** High  
**Status:** Resolved

The generated root ignore policy and a nested `template/.agent/.gitignore` could
hide `.agent/bootstrap-profile.json`, roster, hooks, workflows, selected skills,
and Codex adapter files from the first commit.

**Resolution:**

- removed blanket `.agent/` and `.codex/` generated ignores;
- made nested `.agent/.gitignore` pattern-free;
- ignore only operational Work Block state, project config, runtime memory,
  local Codex config/cache, secrets, dependencies, and build output;
- added diagnostic Git tracking fixtures.

### F-08 — Ignored operational state did not have a portable restore contract

**Severity:** High  
**Status:** Resolved

After clone, ignored `.agent/active-work-block.json` and `memory_bank/` files
could be absent without a safe reconstruction source.

**Resolution:**

- added committed `.agent/active-work-block.default.json`;
- default is blocked, approval-free, integration-free, and empty-write-set;
- generated health check restores missing active Work Block and standard memory
  files;
- existing active Work Block is never replaced;
- clone/restore and idempotence fixtures added.

### F-09 — Git tracking tests depended on runner/user excludes

**Severity:** Medium  
**Status:** Resolved

`git check-ignore` could consume global/system excludes from the GitHub image or
user environment, producing nondeterministic results.

**Resolution:**

- isolate global and system Git config in CI/publication validation;
- set local `core.excludesFile=/dev/null` in generated-project fixtures;
- use verbose effective-rule diagnostics rather than ambiguous quiet status.

### F-10 — Cross-runtime write authority was compared too literally

**Severity:** Medium  
**Status:** Resolved

Claude Code Architect/Critic/Verifier may have narrowly scoped `Edit` access for
runtime memory, approved drafts, or evidence. Treating any `Edit` token as source
write authority produced a false equivalence failure.

**Resolution:**

- normalize **implementation/source write** separately from limited artifact or
  runtime-memory write;
- require only Coder to have implementation write authority;
- require explicit source-write prohibition for non-Coder Claude roles.

### F-11 — OpenCode read-only roles lacked explicit consequential shell denies

**Severity:** High  
**Status:** Resolved

Architect, Critic, Reviewer, and Verifier used general `ask` Bash fallback but did
not all explicitly deny commit, push, reset-hard, clean, and `rm`.

**Resolution:**

- added explicit deny patterns to every OpenCode logical role;
- retained read-only `edit: deny` for non-Coder roles;
- conformance now enforces these patterns.

### F-12 — Minimal and setup documentation still described the maximum scaffold

**Severity:** Medium  
**Status:** Resolved

Public setup, quickstart, maps, registries, and session bootstrap assumed all
runtime surfaces existed.

**Resolution:**

- minimal quickstart now uses `--profile core`;
- setup documents exact profile behavior and no in-place bootstrap upgrades;
- maps/registries distinguish always-present documentation from conditional
  implementation surfaces;
- session bootstrap checks installation state before runtime capability;
- README exposes profile selection and authority separation.

## Verification Evidence

Reviewed revision: `ea0bc918361b4ba9ce1dda8697e0a54ec7c68265`.

Framework Contracts run `311` passed:

```bash
bash scripts/test-sdd-contract.sh
python scripts/test-bootstrap-profiles.py
python scripts/test-profile-restore.py
python scripts/test-runtime-conformance.py
python scripts/test-integration-contracts.py
python scripts/test-integration-admission-evidence.py
python scripts/test-codex-adapter.py
python scripts/test-codex-hard-stops.py
bash scripts/validate-governance.sh
bash scripts/validate-publication.sh
```

Verified profile matrix:

| Requested | Resolved | Result |
|---|---|---|
| `core` | `core` | passed |
| `codex` | `codex` | passed |
| `claude-code` | `claude-code` | passed |
| `opencode` | `opencode` | passed |
| `multi-runtime` | `multi-runtime` | passed |
| `minimal` | `core` | passed |
| `generic` | `core` | passed |
| `full` | `multi-runtime` | passed |

Verified negative/failure behavior:

- unknown profile rejected before target creation;
- invalid/missing manifest sources rejected;
- non-empty target preserved;
- symlink target rejected;
- synthetic staged failure leaves no partial target;
- unselected runtime surfaces absent;
- portable profile/contracts trackable;
- operational state ignored and restorable;
- restored Work Block remains blocked;
- repeated health check preserves existing active Work Block;
- integrations remain inert and admission-gated;
- only logical Coder has implementation/source write authority.

## Specification Drift Audit

| Contract | Result |
|---|---|
| Installation composition remains separate from governance authority | ALIGNED |
| Default invocation remains backward compatible | ALIGNED |
| Lean profiles omit unselected executable runtime surfaces | ALIGNED |
| Governance/runtime/integration documentation remains portable | ALIGNED |
| Generated state records resolved composition | ALIGNED |
| Unknown/invalid profile fails before mutation | ALIGNED |
| Bootstrap failure is transactional | ALIGNED |
| Runtime conformance is semantic, not provider-name based | ALIGNED |
| External integrations remain disabled by default | ALIGNED |
| Clone/restore reconstructs only blocked local state | ALIGNED |

**Drift verdict:** `READY` / `ALIGNED`.

## Residual Limitations

- Static conformance does not prove a live runtime installation, provider auth,
  sandbox, hooks, plugin behavior, network boundary, or OS isolation.
- OpenCode, Claude Code, and Codex still require target-environment smoke before
  higher-governance reliance.
- Bootstrap is intentionally not an in-place upgrader for non-empty projects.
- Python 3 is required for profile-aware bootstrap and validation.
- The bundled handoff runner remains Claude Code-specific internally.
- Custom runtime or integration additions require new manifest/conformance and
  admission evidence.

## Final Verdict

`READY`

No unresolved blocking or high-severity findings remain in the reviewed scope.
PR #5 may move from Draft to human review after closeout documentation and the
final documentation-only head pass Framework Contracts.
