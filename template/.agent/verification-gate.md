Status: PENDING
Work Block: [wb-id]
Verification Tier: PENDING
New Domain: PENDING
Sensitive Domains: PENDING
Claude Verifier Verdict: PENDING
Verification Report: [docs/reports/verification-[wb-id].md]
GPT Verifier Status: PENDING
GPT Verifier Reason: [why NOT_REQUIRED, READY, or DEGRADED]
GPT Verifier Report: [docs/reports/gpt-verifier-[wb-id].md]
GPT Verifier Degraded Reason: [none]
Quick-Fix: false
Stage 3 Mode: PENDING

# Verification Gate

> Control Tower updates this file before final closeout. Use
> `Sensitive Domains: none` or a comma-separated subset of
> `auth,payments,db-schema,middleware`.
> The `verification-gate.sh` Stop hook blocks final response until
> verification and GPT verifier decisions are resolved.

## Control Boundary

The gate controls closeout evidence, not Claude Code's private internal
process. It must verify that implementation was checked, verifier outcomes
were recorded, and GPT verifier triggers were either completed or degraded with
an explicit reason.

It must not require a fixed internal subagent sequence or private chain of
thought. It requires artifacts and decisions that an external orchestrator can
audit.

## Gate Status

| Status | Meaning | Closeout |
|---|---|---|
| PENDING | Verification not resolved | BLOCKED |
| READY | Verification report exists and GPT verifier decision is resolved | ALLOWED |
| SKIPPED | Quick-Fix verifier-agent dispatch skipped; inline verification still required | ALLOWED only with inline `READY` |

`READY` means the evidence decision is resolved; it does not imply successful
verification. It requires `Verification Report` to point to an existing
non-empty file under `docs/reports/`. `Claude Verifier Verdict` must be
`READY`, `BLOCKED`, or `UNVERIFIED`.

## GPT Verifier Status

| Status | Meaning | Closeout |
|---|---|---|
| PENDING | GPT verifier trigger not resolved | BLOCKED |
| NOT_REQUIRED | No Full/new-domain/sensitive-domain/non-READY trigger matched | ALLOWED |
| READY | `gpt-verifier` completed and findings were merged | ALLOWED |
| DEGRADED | Codex MCP unavailable; degraded reason recorded | ALLOWED |

GPT verifier is required when `Verification Tier: full`, `New Domain: true`,
`Sensitive Domains` includes auth, payments, db-schema, or middleware, or
`Claude Verifier Verdict` is `BLOCKED`/`UNVERIFIED`. `READY` requires `GPT Verifier Report` to
point to an existing non-empty file under `docs/reports/`. `DEGRADED` requires
`GPT Verifier Degraded Reason: review-degraded:codex-mcp-unavailable` and a
matching orchestrator-log entry. `NOT_REQUIRED` requires `GPT Verifier Reason`
to explain why no trigger matched.

## Stage 3 Mode

- `success-closeout` requires `Claude Verifier Verdict: READY`.
- `reporting-only` is required for `BLOCKED` or `UNVERIFIED`; the task remains
  blocked and no promotion, merge, deploy, release-ready, successful closure,
  or completed task state is allowed.
- GPT status `DEGRADED` never upgrades the Claude verifier verdict.

## Skip Record (if SKIPPED)

Only valid for `Quick-Fix: true`, `Claude Verifier Verdict: READY`, an inline
verification report, and `Stage 3 Mode: success-closeout`. `SKIPPED` skips the
verifier-agent dispatch, not verification or the authoritative verdict.
Must match orchestrator-log entry exactly.
Format: `verification: SKIPPED — Quick-Fix — [reason]`
