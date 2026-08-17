# WB-DEFINE-001 — Corrective Critic Round 3

- Subject head: `3bde7e76365ee307bfdc463e623bf26f96f40524`
- Subject integrity: `EXACT`
- Verdict: `APPROVE`
- Scope: narrow R-02A corrective loop only
- Source Write Gate authorization: `YES`, limited to the four paths below

## Finding under correction

R-02A: Codex and Claude source-write guards derived formal Define-quality applicability from an unvalidated `governance_profile`. Missing, blank, malformed, or unknown profile values could therefore become non-formal and fail open.

## Approved semantics

Before Define-quality applicability is derived, each source guard must:

1. inspect the raw `governance_profile` value without coercion;
2. require a string;
3. trim and reject blank values;
4. require membership in `Advisory | Controlled | Managed | Assured | Distributed`;
5. deny source writes for `Advisory`;
6. preserve proportional `Controlled` behavior;
7. preserve mandatory Define-quality for `Managed | Assured | Distributed`.

## Approved source write-set

```text
template/.codex/hooks/pre_tool_use_policy.py
template/.claude/hooks/work_block_gate.py
scripts/test-codex-adapter.py
scripts/test-integration-contracts.py
```

Any fifth source path requires return to Define/Critic.

## Required regression matrix

Each executable guard must prove: missing profile, empty profile, whitespace-only profile, unknown/typo profile, non-string profile, Advisory source write, Controlled proportional positive path, and Managed/Assured/Distributed `required=false` denial. Existing missing aggregate, PENDING, blank-evidence, and positive READY fixtures must remain green.

This approval authorizes only future R-02A corrective Execute. It does not establish final PR readiness or merge authority. After Execute the source gate must close again, a new head must be frozen, deterministic CI rerun, and fresh Reviewer → Verifier → Drift assurance performed.
