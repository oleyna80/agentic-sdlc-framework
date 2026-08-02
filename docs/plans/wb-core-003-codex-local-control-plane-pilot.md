---
schema_version: 1
artifact_type: work_block
artifact_id: wb-core-003-codex-local-control-plane-pilot
work_block_id: WB-CORE-003
status: completed
owner_role: orchestrator
created_at: 2026-08-02
process_level: Standard
---

# WB-CORE-003 — Codex Local Control-Plane Pilot

Implement only project-scoped Codex lifecycle and doctor helpers, profile registration, targeted CI routing, tests, and evidence. READY state derives from a role-separated authorization JSON and detached signature committed at `HEAD`; helpers and hooks reload both, require working-tree equality, bind their blobs and Work Block/spec digest/write-set/expiry/Owner/Critic evidence, and verify the signature against an explicit external Owner trust anchor. Hooks remain cooperative and are not an OS boundary, but arbitrary same-user project writers cannot forge Owner approval without the separately held private key. No installer, global configuration, credentials, remote operation, commit, or promotion is in scope. Native smoke is opt-in and unavailable capability is UNVERIFIED.

## Final State

- **Stage:** Close
- **Stage State:** completed
- **Write Gate:** CLOSED
- **Review Gate:** READY
- **Verification Verdict:** READY
- **Evaluation Verdict:** READY
- **Drift Gate:** ALIGNED
- **Closeout Mode:** success-closeout
- **Task Status:** completed

Formal independent Verifier assurance was recorded on 2026-08-02 for this
completed Work Block; the Review Gate is recorded as `READY` in this terminal
state. The repository closeout evidence is
`docs/reports/closeout/wb-core-003-agent-operations-bottlenecks.md`; evaluation
evidence remains under `docs/evals/wb-core-003/` and
`docs/reports/evaluations/wb-core-003.json`. This terminal lifecycle state does
not claim delivery, release, installation, promotion, commit, push, or mutable
external VCS status.
