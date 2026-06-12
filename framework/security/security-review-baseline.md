# Security Review Baseline

> Code-level security review checklist and STRIDE-lite threat modeling.

---

## STRIDE-Lite Threat Model

For security-sensitive Work Blocks, list:
1. **Trust boundaries** — where does untrusted data cross into trusted code?
2. **Attacker-controlled inputs** — query params, body, headers, file uploads, webhooks
3. **Privileged actions** — admin routes, DB writes, config changes, sends
4. **Persistence points** — DB writes, file writes, cache, session storage
5. **One mitigation per relevant threat class** (Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation)

Required for: new/changed auth, authorization, admin routes, webhooks,
external-provider integrations, client-facing sends, data export/import,
file/path handling, payment/order flows, schema/storage changes, security headers.

---

## Code-Level Security Checklist

- [ ] No SQL string interpolation; queries are parameterized
- [ ] No `dangerouslySetInnerHTML` without explicit sanitization
- [ ] No `eval`, `new Function`, or dynamic execution of user-controlled input
- [ ] No `Math.random()` or non-crypto randomness for secrets, tokens, or IDs
- [ ] Mutation endpoints have CSRF, origin, webhook secret, or equivalent guard
- [ ] Redirect URLs and file/path parameters validated against allowlists or fixed roots
- [ ] Errors do not expose stack traces, SQL messages, internal paths, secrets, or provider tokens
- [ ] Logs never include tokens, secrets, passwords, `DATABASE_URL`, full request headers/bodies, connection strings, or row payloads
- [ ] Security headers checked where relevant, including CSP for browser apps
- [ ] No hardcoded API keys, tokens, credentials, private keys, or live endpoints beyond documented public hostnames

---

## Runtime Proof Matrix

| Surface | Minimum proof | Blocked state |
|---|---|---|
| Public web | `curl -fsSI` against target URLs including changed routes | DNS/network unavailable |
| Admin app | `curl -fsSI` against admin hostname and health/login route | hostname unresolved or app not deployed |
| API/webhook routes | positive + negative route smoke + response headers | route not deployed or live action unapproved |
| Deploy/runtime logs | sanitized log scan for token/secret/provider/DB leakage | deploy/live log access not approved |

---

## Security Tooling Baseline

- `scripts/secret-scan.sh staged` — before commits touching security/runtime/config/deploy/auth/webhooks/DB
- `scripts/secret-scan.sh tracked` — during security Work Blocks and before release
- `npm audit --omit=dev --audit-level=high` — for changed Node applications
- Classify `npm audit` findings as: runtime, build-time, dev-only, false-positive/stale, or blocked
