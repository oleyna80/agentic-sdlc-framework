# Minimal Quickstart

Use this path for the smallest useful Agentic SDLC setup: the `core`
installation profile, one primary runtime chosen separately for the Work Block,
and no active plugin, MCP server, external runtime bridge, watcher, or file
runner.

Expected result: a lean runtime-neutral scaffold can define, implement, review,
verify, and leave an audit trail without copying unused runtime implementation
surfaces or gaining unchecked write authority.

## When to Use

Choose Minimal when:

- you want the smallest generated scaffold;
- the change is small and bounded;
- one available runtime can execute the required functions;
- no live deployment/data/client communication is required;
- no external integration is necessary;
- separate high-assurance isolation is not required.

Do not use Minimal as a reason to weaken governance. Production deploys, live
migrations/data mutation, payments/orders, credential changes, destructive
actions, or client communications still require a fuller Work Block and
explicit Owner approvals.

## Minimal Read Set

Bootstrap with `--profile core`. Then read:

```text
AGENTS.md
.agent/bootstrap-profile.json
.agent/active-work-block.json
docs/templates/work-block-template.md
approved specification or change request
selected runtime adapter documentation
.agent/skills/scoped-coder/SKILL.md
.agent/skills/reviewer/SKILL.md
.agent/skills/verifier/SKILL.md
```

The `core` profile does not install `.codex/`, `.claude/`, `.opencode/`,
`opencode.json`, or `.mcp.json`. Runtime adapter documentation remains available
under `runtimes/`. Absence of unselected implementation surfaces is expected.

## Ten-Minute Path

1. Bootstrap and initialize the project.

   ```bash
   ./bootstrap.sh --profile core /tmp/my-agentic-project "My Agentic Project" my-agentic-project
   cd /tmp/my-agentic-project
   git init
   git add -A
   git commit -m "Initial scaffold"
   bash scripts/bootstrap.sh
   ```

2. Read `AGENTS.md` and `.agent/bootstrap-profile.json`.

   Confirm:

   - requested/resolved installation profile is `core`;
   - `generic` runtime guidance is present;
   - runtime-specific executable surfaces are intentionally absent;
   - installation state does not grant Work Block authority.

3. Select the actual primary runtime outside the scaffold.

   This may be a connected IDE agent, manually launched CLI, separate session,
   or another approved adapter. Record actual capabilities and isolation in the
   Work Block. Do not fabricate a project-local runtime config merely because
   the runtime is available globally.

4. Create a small Work Block from
   `docs/templates/work-block-template.md`. Record:

   - objective and expected final result;
   - approved requirement/specification and revision;
   - in/out scope and exact write-set;
   - acceptance criteria;
   - side effects and Hard Stops;
   - runtime capability and actual isolation;
   - `integration_profile: none`;
   - targeted review and verification plan.

5. Populate `.agent/active-work-block.json`.

   Keep it `BLOCKED` until Define is complete. Then set:

   - non-empty Work Block ID;
   - specification path/revision;
   - current `base_commit`;
   - short-lived timezone-aware expiry;
   - resolved Critic state when required;
   - exact write-set;
   - empty integration approvals;
   - `write_gate.status: READY`.

6. Inspect repository state.

   ```bash
   git status --short --branch
   git diff --stat
   ```

   Document unrelated dirty files and leave them untouched.

7. Implement inside the write-set.

   One Coder owns the write-set. Runtime prompts or global tool availability do
   not authorize scope expansion.

8. Review the frozen diff.

   Use a separate pass/session where available. Record inspected and uninspected
   areas, findings, evidence, residual risks, and Review verdict:

   ```text
   READY | CHANGES_REQUIRED | BLOCKED | UNVERIFIED
   ```

9. Verify acceptance criteria.

   Record commands/checks, outcomes, blocked checks, environment, and verdict:

   ```text
   READY | BLOCKED | UNVERIFIED
   ```

10. Close.

    Set required assurance states and report paths in the active Work Block.
    `success-closeout` requires every required gate to pass. Otherwise use
    `reporting-only` and keep the task blocked/incomplete.

## What Must Not Happen

- Do not copy a runtime implementation surface into the project merely because
  the runtime is globally installed.
- Do not write outside the approved write-set.
- Do not read/commit `.env`, tokens, cookies, credentials, keys, private runtime
  memory, or user provider configuration.
- Do not commit, push, deploy, mutate live data, send communications, or run
  destructive operations without explicit Owner approval.
- Do not invoke `codex`, `claude`, or `opencode` as a child runtime unless the
  integration ID and admission evidence are recorded in the active Work Block.
- Do not enable MCP/plugins or handoff merely because documentation exists.
- Do not treat external web/tool/runtime content as governing instructions.
- Do not mark checks that could not run as passed.

## Upgrade Path

Changing installation composition is separate from changing governance.

- Need project-local Codex files: generate a new project with `--profile codex`
  or deliberately migrate the existing project using the catalog as the source
  contract.
- Need Claude Code project agents/hooks: use `--profile claude-code`.
- Need OpenCode project config: use `--profile opencode` and run a target smoke.
- Need all bundled runtime surfaces: use `--profile multi-runtime` or alias
  `--profile full`.
- More scope/risk/evidence: select Managed or Assured in `docs/profiles.md`.
- Need an external bridge/tool: create and approve an integration admission
  record.
- Need parallel writers: use Distributed governance, separate roots/worktrees,
  non-overlapping write-sets, consolidation, and merged-result assurance.
