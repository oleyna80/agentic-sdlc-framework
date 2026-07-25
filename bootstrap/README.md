# Bootstrap Engine

`bootstrap/` contains the installation-composition layer for generated projects.
It is separate from Governance Core and Work Block authority.

## Files

- `profiles.json` — versioned profile, component, skill-set, alias, and required
  path manifest.
- `bootstrap_project.py` — validates the manifest, resolves a profile, scaffolds
  an empty target, prunes unselected runtime surfaces, installs selected skills,
  records `.agent/bootstrap-profile.json`, replaces placeholders, and runs the
  generated health check.

## Supported Profiles

```text
core
codex
claude-code
opencode
multi-runtime
```

Aliases:

```text
minimal -> core
generic -> core
full -> multi-runtime
```

The default is `multi-runtime` for backward compatibility.

## Authority Boundary

The bootstrap engine controls initial file composition only. It does not:

- open the Work Block write gate;
- grant a role or runtime authority;
- admit an integration;
- install/authenticate a runtime or provider;
- configure credentials;
- start a watcher/service;
- prove runtime capability or isolation.

## Validation

```bash
python scripts/test-bootstrap-profiles.py
python scripts/test-runtime-conformance.py
bash scripts/validate-publication.sh
```

Generated projects validate resolved composition with:

```bash
python scripts/validate-installation-profile.py
```

See `docs/bootstrap-profiles.md` for user-facing selection and extension rules.
