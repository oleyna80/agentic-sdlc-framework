# Agentic SDLC Framework

Project-agnostic scaffold for running software projects with AI agents through
a controlled SDLC: plan, spec, implementation, review, and verification.

The core SDLC contract is runtime-neutral. Codex, Claude Code, and other local
agent runtimes can use the same workflow, authority model, memory bank, skills,
and verification gates. This repository also ships a production-oriented Claude
Code runtime layer and a file-based Codex -> Claude Code handoff layer for
controlled multi-agent work.

## What This Gives You

- **Core SDLC layer**: generated project `AGENTS.md`, `.agent/`,
  `memory_bank/`, `docs/`, and
  `skills/` define roles, authority, hard stops, stage flow, scope control,
  reporting expectations, and reusable practices for any capable agent.
- **Codex runtime support**: `.codex/` provides Codex-specific instructions,
  config templates, subagent usage policy, Stage 0 write gate, Codex critic
  review contract, and decision logs so Codex can operate as an independent
  SDLC agent without unchecked Orchestrator decisions.
- **Reusable skill library**: portable skills for discovery, coding, review,
  verification, design, security, debugging, MCP tooling, and closeout.
- **Claude Code runtime layer**: custom agents, hooks, settings, installed
  skills, and per-agent memory under `.claude/` for teams that want Claude Code
  to act as its own orchestrator with subagents.
- **Handoff layer**: `handoff/` lets Codex delegate scoped work to Claude Code
  as an independent external delivery team and read the returned result.
- **Project-neutral routing layer**: `.agent/` keeps roster, workflows, and skill
  routing readable by runtimes that do not use Claude Code's native skill
  directory.
- **Memory starters**: `memory_bank/` plus per-agent memory files for durable,
  evidence-backed project context.
- **Publication hygiene**: validation script, third-party notices, security
  policy, and a private archive exclusion boundary.

## Philosophy

1. **Authority is structural**: roles define what agents may do.
2. **Gates before action**: preflight, scope approval, review, and verification
   happen before risky work advances.
3. **Intentional friction**: unclear work is decomposed before code is changed.
4. **Local-first by default**: generated projects keep `.agent/`, `.codex/`,
   `.claude/agent-memory/`, and `memory_bank/` private unless a team
   deliberately publishes them.

## Runtime Layers

The framework is intentionally layered:

1. **Agentic SDLC core**: the portable process and authority model. Codex or any
   other capable agent can run this layer directly using the generated
   project's `AGENTS.md`, `.agent/`, `skills/`, `docs/`, and `memory_bank/`.
   In Codex mode, Stage 0
   decisions are tracked in `memory_bank/orchestrator-log.md` and checked by
   the Codex critic contract in `.codex/critic.md` when triggers match.
2. **Inter-agent handoff**: `handoff/` coordinates Codex -> Claude Code
   delegation through task files, locks, logs, status files, and queue
   recovery. Codex remains the control tower unless a Work Block explicitly
   delegates work.
3. **Claude Code team runtime**: `.claude/` gives Claude Code its own
   orchestrator/subagent architecture, hooks, critic/verifier gates, MCP access,
   and per-agent memory. Treat it as an external team with its own process and
   observable delivery log.

## Quick Start

From this repository:

```bash
./bootstrap.sh /tmp/my-agentic-project "My Agentic Project" my-agentic-project
cd /tmp/my-agentic-project
bash scripts/bootstrap.sh
```

For a real project, replace the target path:

```bash
./bootstrap.sh /path/to/new-project "My Project" my-project
cd /path/to/new-project
git init
git add -A
git commit -m "Initial scaffold from Agentic SDLC Framework"
```

The generated project receives a `.gitignore` copied from
`template/project.gitignore`. By default it keeps local agent state private.

If you are new to the framework, start with:

- `PROJECT_MAP.md` and `FILE_REGISTRY.yml` for repository orientation.
- `docs/session-bootstrap.md` for the default new-session intake flow.
- `docs/quickstart-minimal.md` for the smallest Codex-only path.
- `docs/profiles.md` for choosing Minimal, Standard, Claude Code team, or
  Codex -> Claude Code handoff mode.
- `docs/mcp-tool-policy.md` before adding MCP servers, browser automation,
  database clients, vendor CLIs, or external research tools.

## First 15 Minutes

Use this path to confirm the scaffold is understandable before customizing it:

1. **Bootstrap a clean project.**

   ```bash
   ./bootstrap.sh /tmp/my-agentic-project "My Agentic Project" my-agentic-project
   cd /tmp/my-agentic-project
   bash scripts/bootstrap.sh
   ```

2. **Choose the operating mode.**

   | Mode | Use when | Start here |
   |---|---|---|
   | Minimal Codex-only | You want the smallest useful path with no Claude Code, MCP, hooks, or handoff | `docs/quickstart-minimal.md` |
   | Codex-only SDLC | You want Codex or another agent to run the core workflow directly | `AGENTS.md`, `.codex/write-gate.md`, `.codex/critic.md` |
   | Claude Code team | You want Claude Code to act as its own orchestrator with agents, hooks, and memory | `CLAUDE.md`, `.claude/settings.json`, `.claude/agents/` |
   | Codex -> Claude Code swarm | Codex should delegate scoped work to Claude Code as an external team | framework `handoff/README.md` |

3. **Open the operating contract.**

   Read `AGENTS.md` first, then `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, and
   `docs/session-bootstrap.md`. `AGENTS.md` defines roles, Stage 0 preflight,
   write gates, critic review, verification, hard stops, and closeout
   expectations. The map and registry explain which files are normative,
   template, reference, example, log, derived, or local state.

4. **Run one local health check.**

   ```bash
   bash scripts/bootstrap.sh
   ```

   Expected result: required workflow files print `OK`, followed by
   `Workflow layer: OK`. Warnings about missing `node_modules/` or
   `DATABASE_URL` are normal for a fresh scaffold before project-specific setup.

5. **Know where evidence goes.**

   - `memory_bank/orchestrator-log.md`: why the orchestrator made decisions
   - `memory_bank/review-log.md`: what critics/reviewers/verifiers found
   - `memory_bank/external-team-log.md`: how delegated Claude Code teams worked
   - `docs/templates/work-block-template.md`: expected final result, execution
     log, verification plan, and retrospective closeout

6. **Keep secrets local.**

   Do not commit `.env`, provider tokens, private memory, MCP credentials,
   generated logs with secrets, or user-level Claude Code env files.

## Directory Structure

```text
agentic-sdlc-framework/
├── README.md
├── SETUP.md
├── PROJECT_MAP.md              # human-readable repository navigation map
├── FILE_REGISTRY.yml           # machine-readable key file/path registry
├── bootstrap.sh
├── scripts/validate-publication.sh
├── docs/                       # first-user onboarding and framework plans
├── examples/                   # synthetic scenario guides
├── template/
│   ├── project.gitignore        # copied to generated projects as .gitignore
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── .agent/                  # runtime-neutral routing layer
│   ├── .claude/                 # Claude Code runtime team layer
│   ├── .codex/                  # Codex runtime config, instructions, write gate
│   ├── memory_bank/
│   ├── docs/{plans,reports,specs,tasklist,templates,reference}/
│   └── scripts/
├── framework/                   # reference documentation
├── skills/                      # portable skill library
└── archive/                     # private examples, ignored for publication
```

## Requirements

- Linux, WSL, or macOS shell environment
- `bash`, `git`, `find`, `sed`, `grep`, `chmod`
- `jq` for Claude Code runtime hooks
- Optional: `python3` for the Codex write-gate hook and publication validation
- Optional: `node`/`npx` for MCP servers and JavaScript/TypeScript projects

The hook scripts assume a Unix-like environment. Windows users should run them
from WSL or Git Bash.

## Skill Locations

The framework keeps skills in `skills/<name>/`.

Bootstrap installs the core set into both:

- `.agent/skills/<name>/` for project-neutral routing and tool-agnostic review
- `.claude/skills/<name>/` for Claude Code runtime loading

Keep both directories aligned when adding or removing project-local skills.

## Local vs Team-Published Mode

Generated projects start in **local-first mode**. Their `.gitignore` excludes
agent state and memory directories so private context does not get committed by
accident.

For a team-published workflow, deliberately edit the generated `.gitignore` and
decide which files are safe to publish. Do not publish secrets, private memory,
credentials, MCP tokens, or environment files.

## Publication Check

Before publishing this framework repository:

```bash
bash scripts/validate-publication.sh
```

The check verifies required scaffold files, script syntax, placeholder
replacement, absence of generated Python bytecode, and scans public paths for
known project-specific private markers. The `archive/` directory is intentionally
ignored by `.gitignore` and must not be published.

## License

MIT. See `LICENSE`.

Bundled third-party skills may retain their own license files. See
`THIRD_PARTY_NOTICES.md`.
