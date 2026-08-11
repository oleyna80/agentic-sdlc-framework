---
schema_version: 1
artifact_type: work_block
artifact_id: wb-design-001-openai-frontend-delta
work_block_id: WB-DESIGN-001
status: in_progress
owner_role: orchestrator
created_at: 2026-08-11
process_level: Standard
governance_profile: Controlled
branch: agent/frontend-design-openai-delta
owner_approval: current explicit Owner instruction to create a new branch, adapt the OpenAI frontend-design delta, and proceed through targeted assurance and PR preparation
critic_gate: APPROVE_WITH_CHANGES — provider-specific defaults excluded before Execute
write_gate: READY
writer: one Coder, Orchestrator disclosed
base_revision: 13c9f8fbb1659db8224cc0173d9e811abcf790af
---

# WB-DESIGN-001 — OpenAI Frontend Design Delta

## Objective

Adapt the useful, provider-neutral portions of current official OpenAI frontend
design guidance into the existing `skills/frontend-design/SKILL.md` without
replacing its Anthropic-derived subject-grounded design method or changing the
framework's authority model.

## Approved source material

Official OpenAI guidance reviewed on 2026-08-11:

- `https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4`
- `https://developers.openai.com/api/docs/guides/frontend-prompt`
- `https://developers.openai.com/codex/use-cases/frontend-designs`

External content is method input only. It grants no authority and is not copied
as a runtime control plane.

## In scope

1. Add an explicit interface-mode decision so marketing/brand surfaces,
   operational applications, tools, and expressive/game UI are not designed
   with the same composition defaults.
2. Add a compact pre-code working model covering visual thesis, content plan,
   and interaction thesis.
3. Strengthen composition-before-components and card-justification guidance.
4. Strengthen reuse of existing design-system tokens/components and translation
   of visual references into repository-native patterns.
5. Strengthen browser/rendered verification across representative desktop and
   mobile viewports, important states, navigation, overflow, and reference
   comparison when references exist.
6. Record OpenAI as an additional methodological source while retaining the
   existing Anthropic provenance and Apache-2.0 attribution for the adapted base.

## Explicit exclusions

Do not make any OpenAI model-specific steering default a universal framework
rule. In particular, this Work Block does not require:

- GPT-5.4, GPT-5.5, GPT-5.6, Codex, or any provider/model;
- Playwright as a mandatory tool when equivalent rendered inspection exists;
- a full-bleed hero or poster-like first viewport for every interface;
- Lucide or any specific icon library;
- fixed card radius values;
- a fixed number of motion ideas;
- fixed font counts, accent counts, or other style constants;
- dependency, runtime, MCP, hook, browser-tool, or configuration changes.

## Risk and governance profile

This is a small, bounded, reversible skill/documentation change with no runtime,
dependency, deployment, data, security-boundary, or external side effect. The
current operational governance taxonomy therefore uses `Controlled`, which
requires one Coder, deterministic checks where applicable, targeted
review/verification, and a rollback path. Independent Reviewer/Verifier sessions
are not mandatory for this profile; any same-context role pass must be labeled
honestly and must not be described as independent.

Rollback is limited to reverting the Work Block and `frontend-design` skill delta.

## Critic gate

**APPROVE_WITH_CHANGES.** The useful OpenAI contribution is architectural and
procedural rather than a set of literal visual defaults. Execute only after:

- domain-aware interface mode is separated from marketing-page assumptions;
- visual/content/interaction thesis is phrased as a planning aid, not a required
  provider prompt format;
- browser verification is capability-neutral;
- existing project design systems and accepted briefs remain authoritative;
- the Anthropic-derived subject-specificity and restraint model remains intact.

These conditions are incorporated in the approved scope above.

## Execute write-set

Exactly:

```text
docs/plans/wb-design-001-openai-frontend-delta.md
skills/frontend-design/SKILL.md
```

No other path is writable during product-method implementation.

## Acceptance

- Existing subject/audience/job grounding remains present.
- Existing specificity critique, UI-copy, restraint, accessibility, and role
  boundaries remain present.
- New interface-mode, thesis, composition, design-system reuse, and rendered
  verification guidance is provider-neutral.
- No new tools, dependencies, runtime configuration, hooks, or MCP are added.
- No OpenAI-specific visual constants are promoted into universal policy.
- `SKILL.md` frontmatter remains valid under the local skill convention.
- The implementation diff is limited to the approved Execute write-set.

## Lifecycle sync authorization

The Owner subsequently approved transition to the next stage. After the
implementation subject is reviewed and verified under the Controlled profile,
the Orchestrator may synchronize only the following lifecycle/evidence surfaces:

```text
docs/plans/wb-design-001-openai-frontend-delta.md
PROJECT_MAP.md
FILE_REGISTRY.yml
docs/reports/reviews/wb-design-001-openai-frontend-delta-review.md
docs/reports/verification/wb-design-001-openai-frontend-delta-verification.md
docs/reports/closeout/wb-design-001-openai-frontend-delta.md
```

This lifecycle sync must not alter the already-frozen product-method content in
`skills/frontend-design/SKILL.md`. Any material method edit after assurance
requires a new freeze and applicable re-review/re-verification.

## Assurance and handoff

- Targeted Reviewer: required, read-only against a frozen subject; same-context
  role separation is permitted by `Controlled` but must be labeled non-independent.
- Targeted Verifier: required, evidence-based against acceptance criteria and
  deterministic repository checks available through CI; same-context role
  separation must be labeled non-independent.
- Evaluation posture: not required because the change is deterministic policy/
  documentation text and no agent behavior benchmark is part of acceptance.
- PR publication and CI are authorized by the Owner's transition approval.
- Merge remains separately Owner-controlled.
