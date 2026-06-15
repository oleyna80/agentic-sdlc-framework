# Lessons Learned - Dual-Model QC (Claude + GPT)

> Generalized from an internal dual-model Quality Control pilot on 2026-06-12.
> Token usage varies by Work Block; record actual usage in the closeout report.

## What Worked

### Work Block retrospectives preserve process gains

When a Work Block exposes a repeatable failure pattern, record it before
closeout instead of leaving it in the chat transcript. The closeout should
capture what worked, what failed, what the critic caught, what wording was
overclaimed, and whether the framework gained a reusable skill, hook, checklist,
or template update.

This is especially important for Codex as Orchestrator: the Owner should be able
to audit not only the final artifact, but also whether the Orchestrator's
decisions were independently challenged and what changed in the process as a
result.

### Complementary blind spots are the primary value

Claude critic is strong at process control: skip chains, weak skip reasons,
missing approval records, and unclear scope boundaries.

GPT verifier is useful as an adversarial second model for code-level issues:
callback gaps, unsafe defaults, component/runtime boundary mistakes, dependency
risk, contract mismatches, and edge cases.

These are different failure categories. No single model-family review should be
assumed to cover both process and implementation blind spots.

### Adversarial review catches same-model blind spots

A same-model reviewer can share assumptions with the agent that produced the
change. A GPT-backed verifier gives the SDLC a second reasoning path and is most
valuable after the primary verifier has already checked the obvious contract.

### Evidence matters more than model opinion

The useful GPT reports cited concrete file/line evidence and tool results. The
framework should treat GPT output as evidence for Control Tower to merge, not as
a standalone acceptance decision.

Use precise evidence wording:

- `demonstrated` for one successful live run or manual exercise;
- `validated` for repeatable scripted checks;
- avoid `proved` or `guaranteed` unless the claim is formally justified.

## What Was Hard

### 1. MCP server availability

The Codex MCP server must be configured and approved before `mcp__codex__codex`
appears as a tool. If it is absent, GPT agents must report an inspection gap and
Control Tower proceeds with Claude-only findings.

**Fix:** keep `codex` in `enabledMcpjsonServers` and document the one-time MCP
approval step.

### 2. Direct Codex CLI is the wrong control plane

Allowing `Bash(codex *)` lets agents bypass the CC-native reviewer/verifier
contract and makes read-only enforcement weaker.

**Fix:** template settings allow only `mcp__codex__codex`; `.mcp.json` starts
Codex with `--sandbox read-only --ask-for-approval never`; hard-stop blocks
direct `codex` shell calls except `codex mcp-server`.

### 3. Prompt construction needs an explicit read-only contract

The Codex prompt must state mode, scope, base/ref, allowed inspection, forbidden
side effects, output schema, and merge recommendation. Without that contract,
adversarial review becomes noisy and harder to consolidate.

**Fix:** GPT agent prompts and the `codex-verification` skill require mode,
scope, base/ref, session id, findings, inspection gaps, and merge recommendation.

### 4. Separate critic and verifier calls are intentional

Combining Stage 0.5 critic and Stage 2 verifier into one Codex call saves tokens
but muddles timing and authority. The critic reviews decisions before changes;
the verifier reviews implementation after changes.

**Decision:** keep `gpt-critic` and `gpt-verifier` separate. Use
`codex-reviewer` only for explicit extra deep review.

## Current Pattern

```
Stage 0.5: Critic Gate
  ├── 1. Launch critic (Claude)
  ├── 2. IF Full tier OR first-WB-in-domain OR Claude critic SUPPLEMENT/RECONSIDER:
  │     Launch gpt-critic through mcp__codex__codex
  └── 3. Merge findings -> APPROVE / SUPPLEMENT / RECONSIDER

Stage 2: Verify
  ├── 1. Launch verifier (Claude)
  ├── 2. IF Full tier OR security/auth/DB/payments/middleware:
  │     Launch gpt-verifier through mcp__codex__codex
  │     Optionally launch codex-reviewer for explicit extra deep review
  └── 3. Merge findings -> consolidation report
```

GPT agents are advisory. Claude agents remain the authoritative gates. Control
Tower validates, deduplicates, and decides.

## Gate Improvements

### Critic gate

The gate should block `Edit`, `MultiEdit`, and `Write` unless:

- `.agent/critic-gate.md` exists;
- `Work Block` is set;
- `Status` is `READY` or authorized `SKIPPED`;
- optional `Expires` is still valid;
- optional `Session` matches the current session;
- the edited file is inside `Approved Write-Set`.

When write-set drift is detected, the denial should name the exact file and show
the exact line to add under `Approved Write-Set` if the scope expansion is
intended.

### Hard-stop hook

`DATABASE_URL` alone is not a live database operation. Blocking every grep or
documentation lookup creates avoidable friction.

Block DB commands when `DATABASE_URL` appears in the same command segment as a
DB-mutating command, or when the command is clearly a live migration/apply path.

## When to Use GPT QC

```
Is the Work Block Full tier? (security/auth/deploy/DB)
  ├── YES -> Launch gpt-critic and gpt-verifier
  └── NO:
      Is this the first WB in a new domain? (no-skip)
        ├── YES -> Launch gpt-critic + gpt-verifier
        └── NO:
            Did Claude critic return SUPPLEMENT/RECONSIDER?
              ├── YES -> Launch gpt-critic for second opinion
              └── NO -> Claude-only QC is sufficient
```

Use `codex-reviewer` only for an explicit extra deep-review slice beyond the
default GPT verifier.

## Verdict

Dual-model QC is useful for Full-tier and high-risk Work Blocks when it is kept
inside a controlled contract: MCP-only invocation, read-only Codex sandboxing,
read-only prompts, explicit write-set gates, and consolidated Control Tower
acceptance.
