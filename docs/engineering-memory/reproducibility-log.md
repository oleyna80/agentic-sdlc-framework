# Reproducibility Log

Record stable commands and recovery knowledge, not raw terminal transcripts.

| Purpose | Command | Expected result | Authority | Verification date | Owner | Review trigger |
| --- | --- | --- | --- | --- | --- | --- |
| SDD contract | `bash scripts/test-sdd-contract.sh` | `OK` | `.agent/workflows/sdd-protocol.md` | 2026-08-03 | Verifier | protocol or workflow-contract change |
| Governance contract | `bash scripts/validate-governance.sh` | `Governance validation: OK` | `AGENTS.md` and accepted governance | 2026-08-03 | Verifier | governance-control change or failed check |
| Release-state contract | `python3 scripts/validate-release-state.py` | `READY` when lifecycle projection permits it | active Work Block and release-state contract | 2026-08-03 | Verifier | state transition or terminal projection |

Record only durable, evidence-backed environment assumptions, recovery steps,
or changed expected results. Re-run a command when its result is needed for a
current claim; this log is not proof of current execution.
