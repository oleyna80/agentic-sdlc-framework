# Examples

Examples in this repository must be synthetic and safe to publish.

Use fictional names, paths, domains, and URLs:

- Project name: `Example SaaS`
- Repository path: `/home/user/projects/example-saas`
- Domain: `example.com`
- API URL: `https://api.example.com`

Do not copy private project scripts, deployment targets, IP addresses, registry
names, customer names, or local machine paths into this directory.

## Available Scenarios

| Scenario | Profile | Purpose |
|---|---|---|
| `codex-only-nextjs/` | Level 1/2 | Minimal Codex-only Work Block for a small Next.js UI change. |
| `codex-claude-reviewer/` | Level 3 | Claude Code acts as an independent read-only reviewer. |
| `codex-claude-handoff-smoke/` | Level 4 | Codex delegates a smoke task to Claude Code through the handoff runner. |

Each scenario documents:

- task;
- approved scope;
- expected agent flow;
- expected final report;
- expected logs;
- what must not happen.

Use these as adoption examples, not as private project templates.
