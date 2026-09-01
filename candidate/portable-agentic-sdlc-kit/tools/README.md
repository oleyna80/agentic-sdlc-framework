# Portable Kit installer

Use Python 3.12 and the standard library only:

```text
python3 candidate/portable-agentic-sdlc-kit/tools/install.py plan --target <repository>
python3 candidate/portable-agentic-sdlc-kit/tools/install.py apply --target <repository>
```

`plan` is mandatory, deterministic, and does not mutate the target. It reports
every manifest path as `create`, `skip-identical`, `collision`, or `blocked`.
`apply` immediately rebuilds the plan, refuses changed or unsafe input, stages
bytes in a disposable directory outside the target, and creates only approved
new files. Pre-existing files, directories, and links are never overwritten,
merged, moved, or deleted.

On an unexpected publication I/O failure, the installer makes a best-effort
reverse-order rollback of only files and empty directories it created during
that run. If rollback is incomplete, it exits nonzero and reports exact
residual paths plus recovery instructions. This is not a claim of
filesystem-wide transactional atomicity.

The installer does not promote the candidate or alter root bootstrap,
`FILE_REGISTRY.yml`, `PROJECT_MAP.md`, runtime/provider configuration, or
candidate authority.
