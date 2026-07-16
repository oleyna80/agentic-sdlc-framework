---
name: video-provider-router
description: Select an approved video-generation provider and model using current official terms, cost, capabilities, watermark behavior, data handling, and project constraints. Use before every paid generation and whenever a fallback or model switch is proposed.
user-invocable: true
argument-hint: "[generation requirements and budget]"
allowed-tools:
  - Read
  - Write
  - Agent
  - WebSearch
  - WebFetch
---

# Video Provider Router

Route by verified capability and risk. Never choose a model solely because it is fashionable or produces attractive demos.

## Registry requirement

Use the project provider registry. If none exists, create one from:

> **Reference:** [`reference/provider-registry.template.yml`](reference/provider-registry.template.yml) — load when initializing or refreshing approved provider entries.

Every production entry must have a recent `verified_at` date and official source URLs.

## Routing dimensions

Evaluate:
- generation mode;
- reference-image and first/last-frame support;
- maximum duration and required aspect ratio;
- identity or product fidelity;
- camera and motion control;
- output resolution;
- visible watermark behavior;
- invisible provenance marking;
- commercial-use terms;
- preview/beta status;
- IP protection or indemnity, if any;
- retention and training policy for submitted assets;
- geographic availability;
- expected cost and latency;
- API stability and rate limits.

## Risk policy

Default production rules:
- block models with unknown commercial terms;
- block visible-watermarked output;
- allow invisible provenance marks;
- never remove or evade provenance or watermarks;
- block preview/beta models for rights-sensitive final output unless explicitly approved;
- prefer direct provider APIs for final client assets when an aggregator does not extend equivalent contractual protection;
- allow aggregators for drafts only when the underlying model terms and endpoint are recorded.

## Decision format

```yaml
requirements:
  mode:
  duration:
  aspect_ratio:
  fidelity:
  budget:
selected:
  provider:
  model:
  endpoint:
  verified_at:
  reason:
  estimated_cost:
  visible_watermark:
  provenance_mark:
  commercial_use:
  preview_or_beta:
  rights_protection:
fallbacks:
  - provider:
    model:
    trigger:
rejected:
  - provider:
    model:
    reason:
```

## Cost control

Estimate:
- cost per second or request;
- number of candidates;
- upscaling or post-processing cost;
- expected retries;
- separate desktop and mobile generations.

Do not hide fallback cost inside a generic buffer.

## Freshness gate

Terms and model availability change. Re-verify from official sources when:
- the registry entry is older than the project-defined freshness window;
- a model version changed;
- the provider changed its pricing, watermarking, or terms;
- a client requests an explicit rights guarantee.

## Exit criteria

Return exactly one selected route, one bounded fallback plan, and documented reasons for rejecting plausible alternatives.
