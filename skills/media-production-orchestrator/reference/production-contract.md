# Media Production Contract

## Purpose

This contract defines the portable artifacts passed between media-production skills. It is descriptive data, not a workflow replacement.

## Asset identity

Every media asset should have a stable identifier:

```yaml
asset_id: hero-atelier-liora-v1
project: atelier-liora
placement: homepage-hero
owner: project-team
status: planned
```

## Stage statuses

Use only:

- `planned`
- `ready`
- `blocked`
- `generated`
- `rejected`
- `approved`
- `integrated`
- `published`

## Brief contract

```yaml
purpose:
business_goal:
placement:
audience:
source_assets: []
duration_seconds:
deliverables:
  - aspect_ratio:
    viewport:
    text_safe_zone:
motion_intensity:
audio:
loop:
budget:
rights_owner:
```

## Provider decision contract

```yaml
provider:
model:
endpoint:
registry_verified_at:
commercial_use:
visible_watermark:
provenance_mark:
preview_or_beta:
indemnity_or_ip_protection:
data_retention:
estimated_unit_cost:
estimated_total_cost:
fallback:
decision_reason:
```

## Generation manifest contract

```yaml
asset_id:
request_id:
provider:
model:
submitted_at:
completed_at:
status:
input_files: []
prompt_file:
seed:
parameters: {}
cost:
output_files: []
terms_verified_at:
```

## Review contract

```yaml
candidate:
result: approved | rejected | revise
blocking_findings: []
non_blocking_findings: []
technical_checks: {}
visual_checks: {}
rights_checks: {}
reviewer:
reviewed_at:
```

## Closeout contract

```yaml
selected_asset:
delivery_files: []
poster:
source_assets: []
provider:
model:
total_cost:
terms_verified_at:
human_approval:
checks: []
known_limitations: []
```
