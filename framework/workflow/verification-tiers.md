# Verification Tiers

> Tiered quality gates — right-size verification for each Work Block.

---

## Tier Selection

| Work Block Type | Tier |
|---|---|
| Typo fix, single-line change | Lite |
| Most feature work, refactoring | Standard |
| Security, auth, deploy, DB, payments | Full |

Control Tower or Work Block specifies the tier. If unspecified — use Standard.

---

## Lite

For trivial changes: at most 2 planned implementation/write-set files,
excluding lifecycle evidence, with no logic, route, schema, API, security, or
governance impact.

- [ ] Changed files match task description
- [ ] No obvious regressions
- [ ] Types pass, build succeeds
- [ ] Tests pass (if they exist)

---

## Standard

Most Work Blocks. Extends Lite.

- [ ] Route contract: URLs return expected status codes
- [ ] Schema contract: field keys, types, required/optional match spec
- [ ] Anchor targets exist on target page
- [ ] No new errors in dev server
- [ ] Security baseline: no secrets, injections, parameterized queries
- [ ] Production Maintainability Standard met

---

## Full

Security, auth, deploy, DB, or payment Work Blocks. Extends Standard.

- [ ] STRIDE-lite threat model verified
- [ ] Security review checklist (all 10 items)
- [ ] `scripts/secret-scan.sh staged` clean
- [ ] `npm audit --omit=dev --audit-level=high` clean
- [ ] Runtime proof: `curl -fsSI` for affected routes
- [ ] CSP/security headers in actual responses
- [ ] Mutation endpoints: CSRF/origin guard in place

---

## Verdicts

| Verdict | Meaning | Next Action |
|---|---|---|
| READY | All tier checks passed | Merge, deploy, closeout |
| BLOCKED | One or more checks failed | Fix issues, re-verify |
| UNVERIFIED | Check could not be executed | Control Tower resolves blocker |

---

## Verifier Isolation

Role policy is not a technical boundary: a native subagent can inherit the
parent process, credentials, network access, and filesystem permissions. Choose
and record the required isolation before implementation, then record the
actual isolation and launch evidence in the verification report and gate.

| Condition | Minimum isolation | Formal closeout |
|---|---|---|
| Lite, non-sensitive quick-fix | `same-session-degraded` | Inline verification is allowed |
| Standard, non-sensitive work | `same-session-degraded` | Inline verification is allowed; use an independent root when stronger evidence is needed |
| Full tier or auth, payments, DB schema, middleware, hooks, runtime configuration | `independent-readonly-root` | Separate top-level read-only verifier after freezing the diff |
| Credentials, live data, deploy, external-provider mutation | `os-isolated` | Separate OS user, container, or equivalent with read-only source and no production credentials |

`independent-readonly-root` is a separate top-level verifier with a read-only
filesystem/write policy. It does not prove credential or network isolation.
`os-isolated` is required when those boundaries matter. A gate can validate a
declared level and evidence path; it cannot prove the isolation claim, so the
verification report must name the launch mechanism and residual limits.
