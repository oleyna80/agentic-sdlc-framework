# Agentic SDLC Framework

Project-agnostic scaffold for running software projects with AI agents through
a controlled SDLC: plan, spec, implementation, review, and verification.

Primary tool: **Claude Code**. Optional support files are included for **Codex**
and other local agent runtimes.

## What This Gives You

- **Operating contract**: `AGENTS.md` defines roles, authority, hard stops, stage
  flow, scope control, and reporting expectations.
- **Reusable skill library**: portable skills for discovery, coding, review,
  verification, design, security, debugging, MCP tooling, and closeout.
- **Claude runtime layer**: custom agents, hooks, settings, and installed skills
  under `.claude/`.
- **Project-neutral routing layer**: `.agent/` keeps roster, workflows, and skill
  routing readable by tools that do not use Claude's native skill directory.
- **Memory starters**: `memory_bank/` plus per-agent memory files for durable,
  evidence-backed project context.
- **Publication hygiene**: validation script, third-party notices, security
  policy, and a private archive exclusion boundary.

## Philosophy

1. **Authority is structural**: roles define what agents may do.
2. **Gates before action**: preflight, scope approval, review, and verification
   happen before risky work advances.
3. **Intentional friction**: unclear work is decomposed before code is changed.
4. **Local-first by default**: generated projects keep `.agent/`, `.codex/`, and
   `memory_bank/` private unless a team deliberately publishes them.

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

## Directory Structure

```text
agentic-sdlc-framework/
├── README.md
├── SETUP.md
├── bootstrap.sh
├── scripts/validate-publication.sh
├── template/
│   ├── project.gitignore        # copied to generated projects as .gitignore
│   ├── AGENTS.md
│   ├── CLAUDE.md
│   ├── .agent/                  # project-neutral routing layer
│   ├── .claude/                 # Claude agents, hooks, skills, memory
│   ├── .codex/                  # optional Codex local config and write gate
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
- `jq` for the Claude hard-stop hook
- Optional: `python3` for the Codex write-gate hook and publication validation
- Optional: `node`/`npx` for MCP servers and JavaScript/TypeScript projects

The hook scripts assume a Unix-like environment. Windows users should run them
from WSL or Git Bash.

## Skill Locations

The framework keeps skills in `skills/<name>/`.

Bootstrap installs the core set into both:

- `.claude/skills/<name>/` for Claude Code runtime loading
- `.agent/skills/<name>/` for project-neutral routing and tool-agnostic review

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
