# WB-CORE-004 Tasklist — GitHub-Native Authority Model

- [x] Confirm public repository and active `main` ruleset.
- [x] Record decision to retire SSH signatures from the normal development path.
- [x] Record reasons and security-boundary rationale.
- [ ] Update authority and lifecycle contracts.
- [ ] Update self-hosting `AGENTS.md`.
- [ ] Introduce active Work Block schema v3 without signed authorization binding.
- [ ] Replace lifecycle helper with non-cryptographic coordination state.
- [ ] Update shared Hard Stop policy: commits/feature pushes allowed; consequential operations denied externally.
- [ ] Update Codex write-set guardrail and Move-destination handling.
- [ ] Update doctor and write-gate documentation.
- [ ] Mark `.agent/authorizations/` as legacy compatibility/history only.
- [ ] Update Codex/session documentation.
- [ ] Update contract tests.
- [ ] Run Framework Contracts.
- [ ] Run Release State Contract.
- [ ] Critic review.
- [ ] Reviewer review.
- [ ] Verifier acceptance.
- [ ] Closeout and release-state reconciliation.

## Stop conditions

Stop rather than weaken the GitHub ruleset, expose credentials to the agent, allow direct default-branch mutation, or represent project-local hooks as a security boundary.
