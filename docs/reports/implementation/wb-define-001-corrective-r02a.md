# WB-DEFINE-001 — R-02A Corrective Execute

## Authorization

Corrective Critic Round 3 reviewed frozen head `3bde7e76365ee307bfdc463e623bf26f96f40524` and returned `SOURCE WRITE GATE MAY REOPEN: YES` for exactly four source paths.

Critic evidence: `docs/reports/reviews/wb-define-001-corrective-critic-round-3.md`.

## Executed source write-set

```text
template/.codex/hooks/pre_tool_use_policy.py
template/.claude/hooks/work_block_gate.py
scripts/test-codex-adapter.py
scripts/test-integration-contracts.py
```

No fifth source path was used.

## Correction

Both Codex and Claude source-write guards now validate the raw `governance_profile` before string normalization or Define-quality applicability:

- non-string -> deny;
- blank/whitespace -> deny;
- unknown profile -> deny;
- canonical enum is `Advisory | Controlled | Managed | Assured | Distributed`;
- `Advisory` source writes -> deny;
- `Controlled` retains proportional `define_quality.required` behavior;
- `Managed | Assured | Distributed` retain mandatory Define-quality behavior.

The existing READY/evidence/Critic/Write Gate/write-set semantics remain unchanged.

## Regression evidence

Both executable guard test paths now independently exercise:

1. missing governance profile;
2. empty profile;
3. whitespace-only profile;
4. typo/unknown profile;
5. non-string profile;
6. Advisory source-write denial;
7. Controlled proportional positive path;
8. Managed `required=false` denial;
9. Assured `required=false` denial;
10. Distributed `required=false` denial.

Existing missing Define-quality, PENDING, blank evidence, and positive source-write fixtures remain present.

## Freeze boundary

After these four source changes, source mutation is closed again. Any additional source correction requires a new corrective loop. Fresh deterministic CI and Reviewer -> Verifier -> Drift assurance are required before readiness can be claimed.
