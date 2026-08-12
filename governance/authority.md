# Authority Model

## Purpose

Authority is structural. A runtime, model, plugin, tool, shell capability, or
project-local hook does not authorize an action by itself.

Every action must be permitted by all applicable dimensions:

1. logical role;
2. approved Work Block scope;
3. write set;
4. side-effect class;
5. external capability boundary when the action is consequential;
6. runtime capability and isolation level.

The framework deliberately separates **process guardrails** from **security
boundaries**. Work Blocks, write sets, Critic/Reviewer/Verifier roles, and local
hooks constrain normal agent behavior. GitHub repository rules, least-privilege
credentials, OS isolation, and secret ownership constrain what the agent can
actually do outside that cooperative process.

## Stable Logical Roles

| Role | Core responsibility | Default write authority |
|---|---|---|
| Owner | Approves objectives, exceptions, consequential external actions, and final business acceptance | Owner-controlled external capability surfaces |
| Orchestrator | Frames Work Blocks, selects topology, controls stage transitions, consolidates evidence, closes work | Governance and coordination artifacts inside scope |
| Architect | Produces architecture, discovery, specification, and plan proposals | Draft architecture/specification artifacts when approved |
| Critic | Challenges scope, assumptions, risks, topology, and verification before execution | Critic report only |
| Coder | Implements the approved change | Approved implementation write set only |
| Reviewer | Reviews the frozen diff for defects, regressions, security, architecture, and maintainability | Review report only |
| Verifier | Gathers evidence against acceptance criteria and contracts | Verification evidence only |

Roles describe authority and accountability, not mandatory separate processes.
One runtime may execute multiple roles when the selected governance profile
permits it. Higher-risk profiles require stronger separation.

## Separate Dimensions

Do not encode runtime or model names as authority-bearing roles.

```yaml
function: code_review
role: reviewer
runtime: claude-code
model_class: balanced_engineering
isolation: separate_session
authority: read_only
```

The same contract may be implemented by another runtime without changing its
authority:

```yaml
function: code_review
role: reviewer
runtime: codex
model_class: strong_reasoning
isolation: separate_subagent
authority: read_only
```

## Isolation Levels

| Level | Meaning | Typical use |
|---|---|---|
| `same_context` | Same active agent/context performs another function | Advisory or low-risk work only |
| `separate_subagent` | Separate delegated context in the same runtime/session | Read-heavy discovery, criticism, review |
| `separate_session` | Independent top-level session against the same repository state | Independent review or verification |
| `separate_worktree` | Independent branch/worktree and write scope | Parallel bounded implementation |
| `separate_runtime` | Different agent runtime or model family | Adversarial second opinion |
| `os_isolated` | Separate OS user, container, or equivalent security boundary | Credentials, live data, deploy, sensitive verification |

A declared isolation level is evidence, not self-authenticating proof. Runtime
adapters must record how it was achieved and any residual limitations.

## GitHub-Native Capability Boundary

For repositories hosted on GitHub, prefer external GitHub controls over a
project-local cryptographic approval state machine.

Normal development may include, when allowed by the Work Block and credential:

- editing approved paths;
- tests/builds;
- staging and local commits;
- normal feature-branch pushes;
- pull-request creation and updates;
- CI/review inspection.

Default-branch authority is external. For this framework, the active `main`
ruleset requires pull requests and the required status checks, rejects branch
deletion and non-fast-forward updates, and has no configured bypass actor.

Consumer projects should give the agent a dedicated least-privilege credential.
A typical production project grants only the repository permissions required for
source/PR work and keeps workflow-dispatch, environment administration, VPS/DB
credentials, and production secrets outside the normal agent credential.

The Owner approval for a production action should therefore occur at the
external boundary (for example, manually starting an exact GitHub Actions
deployment) rather than by signing a mutable project-local authorization file.

## Retired Default: SSH-Signed Work-Block Authorization

Per-Work-Block SSH signatures and authorization-bootstrap commits are **not the
default authority mechanism**.

They were retired because they introduced circular bootstrap and replay/state
complexity (authorization commit, H0/H1/H2 binding, expiry, specification digest,
and runtime parity) while still relying on project-local hooks that are not an
OS security boundary. The control mechanism became a larger failure surface than
ordinary reversible Git operations.

Historical signed authorization artifacts may remain for audit/reference. New
projects and normal Work Blocks must not require an Owner private key,
`ssh-keygen`, detached `.sig`, or external `allowed_signers` file merely to edit,
commit, or push a feature branch.

## Non-Expansion Rule

Temporary specialization narrows focus but never expands authority.

Examples:

- `Reviewer / Security Analyst` remains read-only.
- `Coder / Backend Specialist` may write only the approved backend write set.
- `Verifier / Browser QA` may create only approved evidence artifacts.
- Access to GitHub, shell, Docker, database, browser, MCP, or provider APIs does
  not grant permission to use them for consequential side effects.

## Parallelism

- Parallel read-only roles may inspect the same frozen source state.
- Parallel write roles require non-overlapping write sets and separate
  worktrees/branches unless an adapter provides an equivalent isolation model.
- Use exactly one Coder for each write set.
- The Orchestrator must consolidate conflicts before verification or closeout.

## Failure and Degraded Assurance

If the required role or isolation level is unavailable:

1. do not silently omit the function;
2. select the narrowest documented fallback;
3. label the result as degraded;
4. record what could not be independently established;
5. keep downstream promotion blocked when the selected governance profile
   requires stronger assurance.

## Hard Stops

Hard Stops are consequential operations that the normal agent channel should not
be able to perform merely by editing project-local state:

- production deployment or live service restart;
- live database mutation or migration apply;
- credential or secret changes;
- destructive version-control/filesystem operations;
- direct push, deletion, or non-fast-forward update of protected/default branches;
- irreversible public/package publish where it changes external state;
- real client-facing communications;
- payment, order, stock, CRM, or other live business-data mutation outside an
  approved application execution path.

Enforce these with external capabilities wherever practical: GitHub rules,
least-privilege tokens, workflow permissions, protected environments where
available, OS users/containers, and separately held credentials. Project-local
hooks may deny obvious attempts early, but are cooperative guardrails only.
