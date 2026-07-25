# Handoff Transport

Audited file-based task transport for exchanging bounded work between agent
runtimes, sessions, machines, or users.

The public contract is runtime-neutral:

```text
source runtime
  -> portable task envelope
  -> runner or manual transport
  -> target runtime
  -> result envelope, logs, and scope evidence
```

The current `handoff-runner.sh` implementation invokes Claude Code. It is a
compatibility transport, not the definition of the handoff protocol. Future
runners may target Codex, OpenCode, or another runtime without changing the
portable envelope.

Read first:

- `integrations/file-handoff/README.md`
- `handoff/templates/runtime-task-template.md`
- `AGENTS.md` and the active Work Block

## Appropriate Uses

- runtimes on different machines or under different user identities;
- long-running jobs that need observable queue and recovery state;
- strict before/after scope audit;
- workflows without a native plugin or MCP bridge;
- explicit human review between task creation and execution;
- fallback after a preferred integration is unavailable.

Do not use handoff to bypass runtime permissions, hooks, Work Block scope, or
Owner approval.

## Layout

```text
handoff/
├── README.md
├── runner/
│   ├── handoff-runner.sh
│   ├── parallel-runner.sh
│   ├── sanitize-env.sh
│   ├── cleanup.sh
│   ├── watch-queue.sh
│   └── install-systemd-user-service.sh
├── systemd/
│   ├── agentic-sdlc-handoff.service.template
│   └── handoff.env.example
├── templates/
│   ├── runtime-task-template.md
│   └── claude-team-task-template.md
├── queue/
├── active/
├── done/
├── failed/
├── logs/
├── parallel/
├── runtime/
├── agent.lock
└── watcher.lock
```

`claude-team-task-template.md` is a compatibility example for the existing
Claude runner. New orchestration code should start from
`runtime-task-template.md`.

## Task Publication

Tasks are Markdown files with YAML frontmatter. Writers must:

1. create `queue/<task-id>.md.tmp`;
2. write the complete envelope;
3. validate required fields;
4. atomically move it to `queue/<task-id>.md`.

Do not publish a partially written task directly into `queue/`.

Required concepts include:

- `task_id` and `work_block_id`;
- `from_runtime` and `to_runtime`;
- `logical_function`;
- `source_revision`;
- `project_root`;
- authority and side-effect class;
- allowed and forbidden scope;
- timeout and retry policy;
- objective, acceptance criteria, inputs, checks, and output contract;
- Hard Stops and approval evidence;
- data/secret boundary;
- result and log destinations.

## Result Contract

A completed runner or target runtime must report:

- `DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED | FAILED`;
- source revision inspected and resulting revision if changed;
- concise actions taken;
- changed paths;
- checks and outcomes;
- review, verification, or drift verdict when applicable;
- scope-audit result;
- inspected and uninspected areas;
- residual risks;
- session, job, result, and log identifiers;
- recommended next action.

Do not store private chain-of-thought, secrets, raw environment values, or
unbounded command transcripts.

## Existing Claude Code Runner

Run one task manually:

```bash
cd /path/to/framework
handoff/runner/handoff-runner.sh handoff/queue/<task-id>.md
```

Classification:

```yaml
integration: file-handoff
transport_implementation: claude-code-runner
status: compatibility
```

The runner treats Claude Code as an external runtime/team. Its internal
orchestrator, agents, hooks, and memory do not expand the task envelope's
authority.

For a state-changing Claude task, include expected process/evidence paths in
`allowed_scope`, for example:

```yaml
allowed_scope:
  - src/**
  - tests/**
  - memory_bank/external-team-log.md
  - memory_bank/orchestrator-log.md
  - memory_bank/review-log.md
  - .agent/critic-gate.md
  - .agent/verification-gate.md
  - .claude/agent-memory/**
```

Only include paths the task actually needs. Claude process files are project
files, not runner-owned volatile state.

## Runtime Guard

`handoff-runner.sh` runs a preflight guard by default. It rejects:

- dangerous `project_root` values such as `/`, `/home`, `/tmp`, `/etc`, `/usr`,
  `/var`, `/opt`, `/root`, or the current `HOME`;
- broad `allowed_scope` values such as `*`, `**`, `/`, or the entire project;
- scope patterns containing `..`;
- absolute scope patterns outside `project_root`.

The runner appends default forbidden patterns for common secrets:

```text
.env
.env.*
**/.env
**/.env.*
secrets/**
credentials/**
*.pem
*.key
id_rsa
id_ed25519
```

Guard overrides exist for diagnostics and exceptional human-supervised work, but
using them requires explicit Owner approval and a recorded reason:

```bash
HANDOFF_RUNTIME_GUARD=0 ...
HANDOFF_REQUIRE_SCOPE_RULES=1 ...
HANDOFF_DEFAULT_FORBIDDEN_SCOPE=0 ...
HANDOFF_ALLOW_DANGEROUS_PROJECT_ROOTS=1 ...
HANDOFF_TIMEOUT_KILL_AFTER=10s ...
```

## Scope Audit

When `allowed_scope` or `forbidden_scope` is present, the runner:

1. requires `project_root` to be a Git work tree;
2. records a before snapshot;
3. executes the target runtime;
4. records an after snapshot;
5. compares changed paths, including ignored local-first files;
6. evaluates `forbidden_scope` before allowed/build-artifact rules;
7. fails unexpected writes with status `scope_failed` and exit code `90`.

`allowed_scope` and `forbidden_scope` use Bash glob patterns relative to the
project root. Absolute patterns are accepted only within the project root.

The audit excludes `.git/` and only the current runner-owned volatile files. It
does not blanket-exclude queue, active, done, failed, or project runtime-memory
paths.

Common local build artifacts such as `.next/**` and
`tsconfig.tsbuildinfo` may be ignored by default. Set:

```bash
HANDOFF_SCOPE_AUDIT_IGNORE_BUILD_ARTIFACTS=0
```

when those outputs must be audited. Explicit forbidden patterns still win.

Scope audit is evidence after execution, not an OS sandbox. It cannot prove that
a runtime never read a file or touched a path already dirty before the task.

## Environment Boundary

The runner may load a local ignored file:

```text
handoff/runtime/handoff.env
```

Override with `HANDOFF_ENV_FILE=/path/to/handoff.env`. Keep the file mode `600`.
Logs record only whether a file was loaded and its path, never values.

`sanitize-env.sh` launches Claude Code with a small allowlist needed by the
runtime. Generic token/password variables and `OPENAI_API_KEY` are not forwarded
by the compatibility runner.

Each task receives a private `TMPDIR` under `handoff/runtime/`. The real `HOME`
is retained so the configured Claude Code installation can use its existing
authentication. This is a shared-identity limitation and must be recorded.

## Timeout, Locks, and Recovery

The runner uses `timeout --kill-after` and a lock file. Queue watchers use a
separate watcher lock.

Lifecycle:

```text
queue -> active -> done
                -> failed
```

On startup, the watcher examines stale `active/*.md` tasks. If no runner lock is
held, stale tasks move to `failed/` with a `recovered_failed` result instead of
being silently retried.

A retry must use a fresh task ID or explicit retry record and must revalidate the
source revision, scope, and approvals.

## Watch Queue

Foreground watcher:

```bash
handoff/runner/watch-queue.sh
```

One test pass:

```bash
handoff/runner/watch-queue.sh --once
```

Useful overrides:

```bash
HANDOFF_WATCH_INTERVAL=2
HANDOFF_WATCH_STABLE_SECONDS=1
HANDOFF_RUNNER=/path/to/runner
HANDOFF_SCOPE_AUDIT=0
HANDOFF_REQUIRE_SCOPE_RULES=1
HANDOFF_STATUS_FILE=/tmp/handoff-status.json
```

The watcher does not install or enable itself automatically.

## Parallel Execution

Run independent tasks:

```bash
handoff/runner/parallel-runner.sh --max-jobs 2 \
  handoff/queue/task-a.md \
  handoff/queue/task-b.md
```

Parallel execution requires separate project roots or worktrees and
non-overlapping write-sets. Shared mutable project roots are rejected by default.
The override `--allow-shared-project-root` is for explicitly reviewed exceptional
cases only.

Every child gets a separate lock and status file under `handoff/parallel/`.
Consolidated work still requires independent review and verification.

## systemd User Service

The optional installer creates a user service and local environment file:

```bash
handoff/runner/install-systemd-user-service.sh
```

It does not enable or start the service. Review the generated unit, identity,
`PATH`, environment, project roots, logging, retention, and shutdown procedure
before running:

```bash
systemctl --user enable --now agentic-sdlc-handoff.service
```

For VPS operation after logout, lingering is a separate administrator decision:

```bash
loginctl enable-linger "$USER"
```

System-level service installation is intentionally unsupported.

## Disposable Smoke

Minimum evidence in a throwaway project:

1. publish an atomic read-only task;
2. verify queue/active/done state and result schema;
3. run one allowed-scope write task;
4. run one out-of-scope task and confirm `scope_failed`;
5. confirm `.env`, keys, and secret directories remain forbidden;
6. confirm stale active-task recovery;
7. test timeout and cancellation;
8. record runtime and runner versions plus limitations.

Do not run a paid/live smoke automatically during bootstrap or CI.

## Current Limits

- the bundled runner targets Claude Code only;
- scope audit is post-execution detection, not kernel isolation;
- the real `HOME` and Claude authentication are shared;
- paths dirty before execution cannot be fully attributed;
- `parallel-runner.sh` expects Bash 4.3 or newer;
- systemd support is user-service only;
- live runtime smoke requires a separately configured local environment.
