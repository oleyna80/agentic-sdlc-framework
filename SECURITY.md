# Security Policy

## Supported Scope

Security reports should focus on this framework, its bootstrap scripts, hooks,
templates, and bundled skills.

## Reporting

Open a private security advisory or contact the repository maintainer through
the private channel used for this project. Do not publish exploit details before
the issue is triaged.

## Sensitive Data Rules

This repository must not contain:

- Secrets, tokens, passwords, private keys, cookies, or session material.
- Real customer names, private project names, production domains, or IP
  addresses.
- `.env` files or local MCP credentials.
- Private agent memory from downstream projects.

Run `bash scripts/validate-publication.sh` before publishing.
