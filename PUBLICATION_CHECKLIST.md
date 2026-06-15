# Publication Checklist

Use this before first public release or after publication-readiness changes.

- [ ] Run `bash scripts/validate-publication.sh`.
- [ ] Confirm `archive/` is ignored and not staged.
- [ ] Confirm there are no `.pyc` files or `__pycache__/` directories.
- [ ] Confirm examples use synthetic names, domains, paths, and URLs.
- [ ] Confirm root `LICENSE` and `THIRD_PARTY_NOTICES.md` are present.
- [ ] Confirm generated-project `.gitignore` behavior is documented.
- [ ] Confirm README/SETUP explain the three operating modes:
      Codex-only SDLC, Claude Code team runtime, and Codex -> Claude Code swarm.
- [ ] Confirm README/SETUP include first-run smoke checks and expected results.
- [ ] Bootstrap a smoke project and run `bash scripts/bootstrap.sh` inside it.
- [ ] Validate from a fresh remote checkout or downloaded archive, not only the
      local working tree.
- [ ] Confirm publication smoke-test issues are updated or closed with the
      final validation evidence.
- [ ] Review staged files before commit: `git status --short`.
- [ ] Confirm `git status --short --branch` is clean after the final push.
