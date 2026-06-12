# Contributing

Contributions should keep the framework project-agnostic and safe to publish.

## Rules

- Do not add client names, private domains, IP addresses, credentials, tokens,
  internal infrastructure paths, or production URLs.
- Keep examples synthetic. Use `example.com`, `example.org`, or fictional
  project names.
- Keep generated artifacts out of the repository: Python bytecode, caches,
  build output, dependency directories, and test coverage output.
- Preserve the local-first default for generated projects unless a change
  explicitly documents a team-published mode.
- Update `SETUP.md` and `README.md` when bootstrap behavior changes.

## Validation

Run before proposing publication:

```bash
bash scripts/validate-publication.sh
```

If the script fails, fix the reported issue or document why the check needs to
change.
