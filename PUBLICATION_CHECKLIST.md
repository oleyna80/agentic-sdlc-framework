# Publication Checklist

Use this before creating the public GitHub repository.

- [ ] Run `bash scripts/validate-publication.sh`.
- [ ] Confirm `archive/` is ignored and not staged.
- [ ] Confirm there are no `.pyc` files or `__pycache__/` directories.
- [ ] Confirm examples use synthetic names, domains, paths, and URLs.
- [ ] Confirm root `LICENSE` and `THIRD_PARTY_NOTICES.md` are present.
- [ ] Confirm generated-project `.gitignore` behavior is documented.
- [ ] Bootstrap a smoke project and run `bash scripts/bootstrap.sh` inside it.
- [ ] Review staged files before commit: `git status --short`.
