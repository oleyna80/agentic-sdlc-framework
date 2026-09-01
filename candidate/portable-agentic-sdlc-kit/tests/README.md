# Installer fixtures

Run the deterministic production-behavior suite with:

```text
python3 candidate/portable-agentic-sdlc-kit/tests/test_install.py
```

The fixtures use disposable targets and the actual installer module. They cover
non-mutating plans, successful first installation, repeat `skip-identical`,
collision preservation, invalid and Windows-style manifest paths, symlink
escapes, apply-time drift, staged publication failure, and incomplete rollback
reporting. They do not claim a live multi-OS pilot or candidate promotion.
