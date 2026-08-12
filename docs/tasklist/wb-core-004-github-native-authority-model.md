# WB-CORE-004 Tasklist — GitHub-Native Authority Model

- [x] Confirm public repository and active `main` ruleset.
- [x] Record decision to retire SSH signatures from the normal development path.
- [x] Record reasons and security-boundary rationale.
- [x] Update authority and lifecycle contracts.
- [x] Update self-hosting `AGENTS.md`.
- [x] Introduce active Work Block schema v3 without signed authorization binding.
- [x] Replace lifecycle helper with non-cryptographic coordination state.
- [x] Update shared Hard Stop policy: commits/feature pushes allowed; consequential operations denied externally.
- [x] Update Codex write-set guardrail and Move-destination handling.
- [x] Update Claude Bash write-set/staged-commit parity and runtime documentation.
- [x] Update doctor and write-gate documentation.
- [x] Mark `.agent/authorizations/` as legacy compatibility/history only.
- [x] Update Codex/session documentation.
- [x] Update contract tests.
- [x] Run Framework Contracts — run `31624961564` success on evidence head `c7400ca569b58f94ba68a64fb8ba341e975092e8`.
- [x] Run Release State Contract — run `31624961808` success on the same evidence head.
- [x] Critic review — `docs/reports/reviews/wb-core-004-critic.md`, APPROVE.
- [x] Reviewer review — `docs/reports/reviews/wb-core-004-review.md`, READY.
- [x] Verifier acceptance — `docs/reports/verification/wb-core-004-verification.md`, READY.
- [ ] Final exact-head required checks and protected PR merge.
- [ ] Post-merge closeout and release-state reconciliation.

## Stop conditions

Stop rather than weaken the GitHub ruleset, expose credentials to the agent, allow direct default-branch mutation, or represent project-local hooks as a security boundary.

The Critic/Reviewer/Verifier evidence for this Work Block is same-session connector-backed assurance and is not represented as independent human or separate-runtime review. The protected GitHub merge path remains authoritative.
