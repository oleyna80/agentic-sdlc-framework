# Bootstrap Installation Profiles

Installation profiles control **which runtime implementation surfaces and skills
are copied into a new project**. They do not select governance authority, admit
an integration, configure a provider account, or grant side-effect permission.

The per-Work Block dimensions remain independent:

```text
installation profile  -> files initially present in the project
governance profile    -> required control and assurance strength
runtime profile       -> runtime executing a logical function
integration profile   -> admitted external bridge, tool, service, or transport
model / isolation     -> actual execution evidence
```

## Usage

List profiles:

```bash
./bootstrap.sh --list-profiles
```

Create a project with an explicit profile:

```bash
./bootstrap.sh --profile codex /path/to/project "My Project" my-project
```

The existing positional invocation remains valid and resolves to
`multi-runtime`:

```bash
./bootstrap.sh /path/to/project "My Project" my-project
```

You may also set the profile through an environment variable:

```bash
AGENTIC_SDLC_PROFILE=core ./bootstrap.sh /path/to/project "My Project"
```

An explicit `--profile` argument takes precedence over the environment default.

## Profiles

### `core`

Smallest runtime-neutral scaffold.

Includes:

- Governance Core;
- portable lifecycle, Work Block, assurance, navigation, and memory contracts;
- generic/sequential runtime guidance;
- runtime and integration documentation;
- shared provider-neutral Hard Stop policy;
- portable core skills.

Does not include executable Codex, Claude Code, OpenCode, or MCP configuration
surfaces.

Alias: `minimal` and `generic`.

### `codex`

`core` plus:

- `.codex/` custom logical-role agents;
- project hooks and compatibility wrappers;
- Codex operational and engineering skills.

It does not pin a model, provider account, auth configuration, or MCP server.

### `claude-code`

`core` plus:

- `CLAUDE.md`;
- `.claude/` logical-role agents;
- Work Block, assurance, typecheck, and Hard Stop hooks;
- project-local agent memory structure;
- mirrored selected skills under `.claude/skills/`.

It does not enable MCP servers, external runtime bridges, or provider-named
authority agents.

### `opencode`

`core` plus:

- `opencode.json` safe project permissions;
- `.opencode/agents/` logical-role subagents.

The public baseline leaves provider/model, plugins, and MCP collections unbound
or empty. Run target-environment permission and denied-action smoke tests before
using it for Managed or Assured work.

### `multi-runtime`

Backward-compatible default containing the Codex, Claude Code, and OpenCode
implementation surfaces plus an empty `.mcp.json` registry.

Use it for:

- framework evaluation;
- mixed-runtime development;
- migration from the previous maximum scaffold;
- projects that deliberately want several local runtime adapters available.

Presence does not activate integrations or allow one runtime to invoke another.

Alias: `full`.

## Generated Profile State

Every scaffold receives:

```text
.agent/bootstrap-profile.json
```

It records:

- requested and resolved profile IDs;
- selected components;
- installed runtime guidance;
- inert integration configuration surfaces;
- selected skills and skill mirrors;
- required paths;
- known unselected paths that must be absent in a fresh scaffold;
- an explicit authority disclaimer.

The file is installation evidence, not a Work Block approval file.

Run the generated health check after moving or restoring a project:

```bash
bash scripts/bootstrap.sh
```

That command validates `.agent/bootstrap-profile.json` through:

```bash
python3 scripts/validate-installation-profile.py
```

It also writes `.agent/project-config.md` with the resolved installation profile
and memory-directory convention.

## Fail-Closed Behavior

Bootstrap exits before changing the target when:

- the profile ID or alias is unknown;
- the catalog schema is invalid;
- a profile references an unknown component or skill set;
- a referenced skill or component source is missing;
- a path is absolute or contains `..`;
- the target exists and is not empty.

The engine does not delete or overwrite a non-empty target.

## Profile Catalog

The source of truth is:

```text
bootstrap/profiles.json
```

The catalog declares:

- schema and default profile;
- aliases;
- common portable paths;
- runtime/integration components and their paths;
- skill sets;
- profile composition.

`bootstrap/bootstrap_project.py`, CI, publication validation, and the generated
profile validator consume the resulting contract.

## Adding a Profile or Component

A framework change must:

1. add or update the catalog entry;
2. keep component paths safe and relative;
3. define selected skill sets;
4. update profile documentation and navigation;
5. extend `scripts/test-bootstrap-profiles.py` when a new canonical profile or
   alias is introduced;
6. update runtime conformance tests when a new runtime implementation is added;
7. bootstrap a disposable project and inspect both selected and unselected
   surfaces;
8. record review, verification, drift, and closeout evidence.

Do not create a profile that encodes concrete provider credentials, model names,
production endpoints, live permissions, or automatic integration activation.

## Conformance Evidence

Framework CI runs:

```bash
python scripts/test-bootstrap-profiles.py
python scripts/test-runtime-conformance.py
```

The first test verifies exact fresh-scaffold composition for every profile and
alias. The second translates runtime-specific agent/config syntax into one
semantic matrix covering:

- Architect, Critic, Coder, Reviewer, and Verifier functions;
- one write-capable Coder surface;
- read-only assurance roles;
- provider-neutral model posture;
- shared Work Block and Hard Stop boundaries;
- inert integration defaults.

Passing conformance does not prove OS isolation or a live runtime installation.
Those require target-environment evidence.
