# Authorization Records

Each authorization JSON requires a detached sibling signature:
`<record>.json.sig`. Lifecycle and PreToolUse independently reload both exact
`HEAD` blobs, reject dirty or widened material, and verify the JSON with
`ssh-keygen -Y verify`, namespace `agentic-sdlc-authorization`, and principal
`owner@agentic-sdlc`.

The locally held trust anchor is deliberately outside the project and must be
provided explicitly for every authority-bearing operation:

```bash
export AGENTIC_SDLC_OWNER_SIGNERS=/absolute/path/to/owner-signers
```

It is an OpenSSH `allowed_signers` file; do not place it in repository `HEAD`.
The helper never creates, edits, or signs authorization records. Hooks remain
cooperative controls and do not prevent hook bypass or an OS-level same-user
writer from altering local project files; the external trust anchor prevents
that writer from forging a valid Owner signature.
