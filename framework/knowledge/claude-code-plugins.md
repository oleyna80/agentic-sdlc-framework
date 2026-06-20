# Claude Code Plugin Profile

This profile defines the Claude Code plugins approved for work on this
framework repository. It does not change generated-project defaults and does
not install user-global configuration.

## Active Baseline

The project-scoped source of truth is `.claude/settings.json`.

| Plugin | Source | Status | Reason |
|---|---|---|---|
| `skill-creator@claude-plugins-official` | Anthropic official marketplace | enabled | Creates and evaluates reusable skills without replacing the framework lifecycle. |
| `frontend-design@claude-plugins-official` | Anthropic official marketplace | enabled | Adds focused frontend design guidance without taking orchestration authority. |

Reviewed local marketplace snapshot on 2026-06-19:

| Plugin | Reported version | License | Packaged capabilities | Tree fingerprint (SHA-256) |
|---|---|---|---|---|
| `skill-creator` | `unknown` | Apache-2.0 | one skill, three helper-agent prompts, Python evaluation/reporting tools; no plugin hooks or MCP server | `bdd7c6ea6905d5966769e598d8430345eeef54ba88c4a5fa28a1935180e7732a` |
| `frontend-design` | `unknown` | Apache-2.0 | one instruction skill; no plugin hooks, agents, commands, scripts, or MCP server | `08d5c8c5d7c79220db6364a277176cf9d3134598b116bade3cdfb00af8050555` |

Claude Code and the marketplace manifests reported no semantic version for
these snapshots. The fingerprints make this review reproducible but do not pin
future installs. Re-review the downloaded tree when either fingerprint changes.

`skill-creator` has a broader operational surface than its plugin manifest
shows. Its optional evaluation and description-optimization scripts can:

- create temporary command files under the nearest project `.claude/`;
- launch nested `claude -p` processes using the configured model and inherited
  environment (except `CLAUDECODE`), which can incur API cost and send test
  prompts or skill content to the configured provider;
- start a loopback-only HTTP review server and open a browser;
- load Google Fonts and a pinned SheetJS bundle from external CDNs in generated
  review pages.

Creating or editing a skill does not require those optional operations. Do not
run benchmark loops, description optimization, the HTTP viewer, or generated
review pages automatically. Confirm the evaluation dataset, provider, model,
budget, environment exposure, and external-asset policy with the Owner first.

The repository also keeps portable standalone copies under `skills/`. The
copies are part of the generated framework; the plugins are an optional Claude
Code interface for maintainers. Do not delete or silently synchronize one from
the other. Review upstream changes before updating either copy.

## Evaluated But Not Enabled

Checked on 2026-06-19.

| Extension | Classification | Decision |
|---|---|---|
| `superpowers@claude-plugins-official` | competing lifecycle | Do not enable in the baseline. Its planning, TDD, subagent, and review workflow overlaps the Agentic SDLC authority model and gates. |
| `get-shit-done-cc` (GSD) | competing lifecycle and global installer | Do not install from this repository. It modifies user-level Claude Code state and introduces a parallel planning/execution system. |
| `context-mode@context-mode` | experimental context runtime | Keep disabled. It intercepts broad tool and lifecycle events and maintains local SQLite state, so hook ordering and audit behavior require an isolated compatibility test. |
| `claude-mem` | experimental persistent-memory runtime | Keep disabled. It adds lifecycle hooks, a local worker service, storage, and provider configuration that overlap framework memory and observability. |

## Installed Inventory Decisions

The local Claude Code registry is machine-wide and can contain entries owned by
other repositories. The following decisions apply to the framework profile;
they do not authorize cleanup of user scope or another project's scope.

Reviewed on 2026-06-19:

| Plugin | Observed scope | Framework decision | Reason |
|---|---|---|---|
| `skill-creator` | framework project | keep enabled | Bounded skill-authoring capability; optional evaluation runtimes remain Owner-gated. |
| `frontend-design` | framework project and pre-existing user/other-project entries | keep enabled for framework project | Focused design skill with no hooks, MCP server, or competing lifecycle. |
| `codex` | user | do not enable; global cleanup is separate | Calls Codex CLI and can add a Stop review gate, conflicting with the framework's MCP-backed GPT critic/verifier contract and direct-CLI hard stop. |
| `feature-dev` | user | do not enable | Introduces its own exploration, architecture, implementation, and review lifecycle. |
| `code-simplifier` | user | do not enable | Proactive write-capable refactoring conflicts with one-Coder scope control and explicit review/fix stages. |
| `security-guidance` | user | isolated profile only | Adds SessionStart, prompt, edit, commit, push, and Stop hooks; sends diffs to a configured model and defaults to an Anthropic model id that may not work through the current gateway. |
| `session-report` | user | manual diagnostics only | Reads cross-project transcript history and writes an HTML artifact; useful for explicit cost/process analysis, not normal execution or canonical logging. |
| `github` | user | project-specific only | Adds a broad remote MCP authority surface, including repository writes; enable only for a Work Block that needs GitHub operations. |
| `pyright-lsp` | user | stack-specific only | Useful in Python projects, but not a generic framework runtime dependency. |
| `code-review`, `commit-commands`, `typescript-lsp` | another project | out of scope | They are not installed for this repository. Do not change another project's plugin registry from this profile. |

Disabled registry entries have no framework runtime effect. Do not remove them
merely to make `claude plugin list` shorter: uninstalling user or foreign
project entries changes state outside this repository. Perform such cleanup in
a separate, explicitly global Work Block.

## Candidate Scan

The official marketplace contains many useful integrations, but usefulness is
not sufficient for baseline activation. The baseline must remain portable,
provider-neutral, and compatible with existing authority gates.

| Candidate class | Decision | Adoption condition |
|---|---|---|
| `pr-review-toolkit`, `code-review`, external review services | optional review profile | Prove read-only behavior, bounded cost, and added value beyond Claude reviewer plus GPT critic. |
| `security-guidance`, Semgrep, SonarQube | optional security profile | Test hook ordering, provider/model routing, diff disclosure, latency, and coexistence with critic and verification Stop hooks. |
| `session-report` | manual observability profile | Owner explicitly requests cross-session analysis and approves transcript scope and generated report path. |
| `typescript-lsp`, `pyright-lsp`, other LSP plugins | project stack profile | The target project uses the language and the required language server is available. |
| GitHub, Playwright, Context7, provider or deployment MCP plugins | task-specific profile | A Work Block requires the external system and defines credentials, read/write authority, data boundary, and rollback. |
| `claude-code-setup`, `claude-md-management`, memory/context plugins | do not add to baseline | They overlap framework onboarding, navigation, memory, or lifecycle ownership. Evaluate only against a demonstrated gap. |
| `plugin-dev` | framework-development tool only | Add temporarily when this repository starts authoring a distributable Claude Code plugin. |

No new plugin was promoted by the 2026-06-19 inventory audit. The two-plugin
baseline is intentional, not an incomplete installation.

Experimental plugins require a separate Work Block with an isolated test
project, explicit hook-order analysis, data-retention review, rollback steps,
and before/after evidence. Successful installation alone is not approval.

The active maintainer profile received static capability review and activation
checks. It has not received a generated-project runtime test with critic,
verification, write, and hard-stop hooks because `.claude/settings.json` is not
copied from the repository root into generated projects. Do not promote these
plugins into `template/.claude/settings.json` until that compatibility test
passes.

## Installation And Scope

Claude Code reads the checked-in `enabledPlugins` map when this repository is
opened. If an approved plugin is missing from the local cache, install it from
the repository root:

```bash
claude plugin install skill-creator@claude-plugins-official --scope project
claude plugin install frontend-design@claude-plugins-official --scope project
```

Rules:

- Always use `--scope project` for this profile.
- Do not use `--global`, `--scope user`, or edit `~/.claude` from framework
  automation.
- Do not add plugin-generated caches or runtime state to git.
- A plugin does not expand file, tool, approval, or orchestration authority.
- Keep existing critic, verification, write, and hard-stop gates authoritative.

## Review Checklist

Before approving a new plugin or version:

1. Record source, revision or version, license, and review date.
2. Inspect skills, agents, commands, hooks, MCP servers, scripts, and runtime
   dependencies.
3. Identify overlaps with the framework lifecycle, memory, logs, and gates.
4. Check network calls, telemetry, credential access, and persistent storage.
5. Test install, activation, disable, and uninstall in an isolated project.
6. Run a representative task and verify that critic and verification gates
   still execute.
7. Promote it to the baseline only after review evidence is recorded.

## References

- Claude Code plugins: https://code.claude.com/docs/en/plugins
- Claude Code plugin marketplaces: https://code.claude.com/docs/en/plugin-marketplaces
- Anthropic plugin marketplace: https://github.com/anthropics/claude-plugins-official
- Superpowers: https://github.com/obra/superpowers
- Context Mode: https://github.com/mksglu/context-mode
- Claude Mem: https://github.com/thedotmack/claude-mem
- GSD: https://github.com/gsd-build/get-shit-done
