---
name: video-generator
description: Execute approved video-generation requests through project-configured APIs or CLIs, including async job submission, polling, download, manifests, retries, and cost tracking. Use only after brief, rights, prompt, provider, and budget gates are approved.
user-invocable: true
argument-hint: "[approved generation package]"
allowed-tools:
  - Read
  - Write
  - Bash
---

# Video Generator

Execute the approved request exactly. Do not make creative or provider decisions during generation.

## Preconditions

Require:
- approved brief;
- cleared or explicitly conditional rights report;
- selected provider/model with fresh registry entry;
- approved prompt package;
- candidate count and maximum cost;
- output workspace;
- credentials available through environment or a secret manager.

Stop if a credential appears in a tracked file.

## Adapter contract

A provider adapter must support:

```text
validate-config
estimate
submit
status
download
cancel
```

It should accept a provider-neutral request and write normalized JSON. Provider-specific parameters belong in the request manifest, not scattered through application code.

## Execution sequence

1. Validate local dependencies and credentials without printing secret values.
2. Run a cost estimate and compare it with the approved limit.
3. Create a request manifest before submission.
4. Submit exactly the approved number of candidates.
5. Persist request IDs immediately.
6. Poll with bounded backoff and a maximum wait policy.
7. Download outputs to the raw candidate directory.
8. Verify file type, non-zero size, duration, dimensions, and decodeability.
9. Update actual cost and result metadata.
10. Return control to quality review.

## Retry rules

- Retry transient transport failures at most twice.
- Do not resubmit when a request ID exists until its status is resolved.
- Use idempotency keys when supported.
- Do not retry moderation or rights failures through another provider.
- Do not silently increase candidate count, duration, resolution, or cost.

## Manifest

Write:

```json
{
  "assetId": "",
  "provider": "",
  "model": "",
  "endpoint": "",
  "requestIds": [],
  "submittedAt": "",
  "completedAt": "",
  "promptFile": "",
  "inputFiles": [],
  "parameters": {},
  "estimatedCost": 0,
  "actualCost": 0,
  "outputs": [],
  "termsVerifiedAt": ""
}
```

## Security

- Read keys from environment variables or an approved secret manager.
- Redact authorization headers, signed URLs, tokens, and account IDs from logs.
- Never commit raw provider responses if they contain secrets or private URLs.
- Do not upload unrelated repository files.
- Respect client data-retention restrictions.

## Exit criteria

Every output is traceable to a request ID, prompt, source set, provider/model, parameters, terms verification date, and recorded cost.
