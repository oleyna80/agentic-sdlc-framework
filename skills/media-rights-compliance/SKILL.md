---
name: media-rights-compliance
description: Perform rights, consent, licensing, watermark, provenance, and provider-terms checks for AI-generated media. Use before generation and before publication whenever source images, identifiable people, brands, client assets, third-party styles, or commercial website usage are involved.
user-invocable: true
argument-hint: "[brief, source assets, and selected provider]"
allowed-tools:
  - Read
  - Write
  - Agent
  - WebSearch
  - WebFetch
---

# Media Rights Compliance

Provide an operational gate, not legal certainty. Escalate material uncertainty instead of inventing permission.

## Pre-generation checks

Verify:
- who owns or licenses every source image, video, audio track, logo, and 3D asset;
- whether the intended use falls within that license;
- whether identifiable people consented to this use and to synthetic alteration;
- whether minors or sensitive contexts are involved;
- whether the prompt asks for protected characters, logos, or close imitation of a living artist;
- whether the selected model permits commercial output;
- whether the exact endpoint is generally available, preview, or beta;
- whether visible watermarks will appear;
- whether an invisible provenance mark is added;
- whether submitted client assets may be retained or used for training;
- whether any advertised IP protection applies to this exact service and account tier.

## Hard stops

Return `blocked` when:
- source rights are unknown;
- required consent is missing;
- the output depends on removing or hiding a watermark;
- commercial terms for the exact model/endpoint are unknown;
- a client expects exclusivity that the provider terms do not support;
- the prompt requests misleading impersonation or unauthorized brand endorsement;
- a rights-sensitive final asset would use a disallowed preview/beta route.

## Publication checks

Confirm that:
- only the approved candidate is delivered;
- rejected or source assets are not accidentally published;
- attribution is included when required;
- the generation manifest and terms verification date are retained;
- the page does not imply that a synthetic scene is documentary evidence;
- a human approved the exact final output.

## Report format

```yaml
status: cleared | conditional | blocked
asset_rights:
  owner:
  evidence:
  restrictions: []
people_and_consent:
  identifiable_people:
  consent_evidence:
provider_terms:
  provider:
  model:
  endpoint:
  verified_at:
  commercial_use:
  output_rights:
  visible_watermark:
  provenance_mark:
  preview_or_beta:
  ip_protection:
  exclusions: []
publication_conditions: []
blocking_issues: []
reviewer_note:
```

## Rules

- Use official provider terms as primary evidence.
- Distinguish ownership of an output from freedom from third-party claims.
- Distinguish “commercial use permitted” from contractual indemnity.
- Distinguish a direct provider API from an aggregator endpoint.
- Never promise that an output is copyrightable in every jurisdiction.
- Never recommend stripping metadata or provenance to conceal AI origin.

## Exit criteria

The report must make the remaining risk visible to the project owner and provide a clear `cleared`, `conditional`, or `blocked` result.
