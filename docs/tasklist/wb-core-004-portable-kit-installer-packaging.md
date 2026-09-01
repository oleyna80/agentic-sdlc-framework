---
schema_version: 1
artifact_type: tasklist
artifact_id: wb-core-004-portable-kit-installer-packaging
work_block_id: WB-CORE-004
status: approved
owner_approval: OWNER_CORE_004_DEFINE_APPROVAL_GATE in Issue #50; tasks are prospective until OWNER_CORE_004_EXECUTE_GATE.
---

# WB-CORE-004 — Task List

## Requirements and implementation tasks

- [ ] TASK-001 [type=requirement] [req=REQ-001] [ac=AC-001] [paths=candidate/portable-agentic-sdlc-kit/package-manifest.json,candidate/portable-agentic-sdlc-kit/tools/install.py] Define deterministic package identity, schema, revision, and approved-create manifest handling.
- [ ] TASK-002 [type=requirement] [req=REQ-002] [ac=AC-002] [paths=candidate/portable-agentic-sdlc-kit/tools/install.py,candidate/portable-agentic-sdlc-kit/tests/test_install.py] Implement a non-mutating target plan and empty-target fixture.
- [ ] TASK-003 [type=requirement] [req=REQ-003] [ac=AC-003] [paths=candidate/portable-agentic-sdlc-kit/tools/install.py,candidate/portable-agentic-sdlc-kit/tests/test_install.py] Enforce host-neutral containment, traversal, absolute-path, and symlink-escape rejection.
- [ ] TASK-004 [type=requirement] [req=REQ-004] [ac=AC-004] [paths=candidate/portable-agentic-sdlc-kit/tools/install.py,candidate/portable-agentic-sdlc-kit/tests/test_install.py] Classify collisions and preserve pre-existing target artifacts.
- [ ] TASK-005 [type=requirement] [req=REQ-005] [ac=AC-005] [paths=candidate/portable-agentic-sdlc-kit/tools/install.py,candidate/portable-agentic-sdlc-kit/tests/test_install.py] Revalidate plan inputs and approved creates before publication.
- [ ] TASK-006 [type=requirement] [req=REQ-006] [ac=AC-006] [paths=candidate/portable-agentic-sdlc-kit/tools/install.py,candidate/portable-agentic-sdlc-kit/tests/test_install.py] Stage bytes, publish approved creates, inject failures, and verify bounded reverse rollback.
- [ ] TASK-007 [type=requirement] [req=REQ-007] [ac=AC-007] [paths=candidate/portable-agentic-sdlc-kit/tools/install.py,candidate/portable-agentic-sdlc-kit/tests/test_install.py] Keep implementation stdlib-only and exercise host-neutral path fixtures.
- [ ] TASK-008 [type=requirement] [req=REQ-008] [ac=AC-008] [paths=candidate/portable-agentic-sdlc-kit/CANDIDATE.md,candidate/portable-agentic-sdlc-kit/tools/README.md,candidate/portable-agentic-sdlc-kit/tests/README.md] Document noncanonical boundaries and prove root control-plane nonmutation.
- [ ] TASK-009 [type=requirement] [req=REQ-009] [ac=AC-009] [paths=candidate/portable-agentic-sdlc-kit/tests/test_install.py,candidate/portable-agentic-sdlc-kit/tests/README.md] Build deterministic production-behavior fixtures for success and adversarial cases.
- [ ] TASK-010 [type=requirement] [req=REQ-010] [ac=AC-010] [paths=candidate/portable-agentic-sdlc-kit/CANDIDATE.md,candidate/portable-agentic-sdlc-kit/package-manifest.json] Bind implementation evidence to the approved boundary and assurance contract.

## Enabling, documentation, and assurance tasks

- [ ] TASK-011 [type=enabling] [req=-] [ac=-] [paths=candidate/portable-agentic-sdlc-kit/tools/install.py] Keep Python 3.12 stdlib-only imports and deterministic diagnostics.
- [ ] TASK-012 [type=documentation] [req=-] [ac=-] [paths=candidate/portable-agentic-sdlc-kit/tools/README.md,candidate/portable-agentic-sdlc-kit/tests/README.md] Document plan/apply commands, collision behavior, and rollback limits.
- [ ] TASK-013 [type=assurance] [req=-] [ac=-] [paths=candidate/portable-agentic-sdlc-kit/tests/test_install.py] Run the complete deterministic fixture suite on the frozen subject.
- [ ] TASK-014 [type=assurance] [req=-] [ac=-] [paths=candidate/portable-agentic-sdlc-kit/CANDIDATE.md,candidate/portable-agentic-sdlc-kit/package-manifest.json] Confirm exact write-set and candidate boundary after implementation.
- [ ] TASK-015 [type=assurance] [req=-] [ac=-] [paths=candidate/portable-agentic-sdlc-kit/tools/install.py,candidate/portable-agentic-sdlc-kit/tests/test_install.py] Provide fresh Reviewer, Verifier, and Drift evidence before closeout.
