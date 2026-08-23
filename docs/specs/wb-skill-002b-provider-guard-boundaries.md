---
schema_version: 1
artifact_type: specification
artifact_id: wb-skill-002b-provider-guard-boundaries
work_block_id: WB-SKILL-002B
status: approved
created_at: 2026-08-23
revision: execute-r1-2026-08-23
owner_approval: Owner prospectively approved this exact specification revision and the exact one-path source write-set scripts/test-sdd-contract.sh on 2026-08-23. This approval establishes WB-SKILL-002B Execute authority only; it grants no commit, push, pull-request, merge, or GitHub-thread authority.
---

# WB-SKILL-002B — Provider Guard Imperative and Fence Boundary Correction

## Purpose and Authority

This Managed corrective Work Block addresses two confirmed P2 findings against
the merged WB-SKILL-002A closeout subject. It preserves the accepted
provider-neutral semantics of `skills/codex-verification/SKILL.md` and confines
any future source correction to its existing target-only contract guard.

The first finding is that direct imperative provider-assurance instructions,
such as `Ask Codex to review the implementation.`, are not necessarily
recognized by the current predicate. The second is that fenced-code exclusion
uses a delimiter toggle rather than a compatible opener/closer boundary.

This approved specification is the behavioral authority for the exact one-path
WB-SKILL-002B Execute write-set, `scripts/test-sdd-contract.sh`. Its Owner
approval is prospective as of 2026-08-23; it does not change the closed
WB-SKILL-002A historical or lifecycle record, or create an external GitHub
action.

## Requirements

- REQ-001: The target-only provider guard must reject only these normalized
  direct imperative provider-assurance statement forms: an optional purpose
  introduction `To verify,`; optional `please` or `kindly`; `ask` or `request`;
  a recognized provider alias (`provider`, `Codex`, `additional model`, or
  `second model`); `to`; and an assurance action (`review`, `verify`, or
  `perform verification`). The forms must be recognized on one line and when
  ordinarily wrapped within one Markdown statement, without becoming a general
  NLP system or scanning repository paths other than
  `skills/codex-verification/SKILL.md`.
- REQ-002: Fenced-code handling must record the opening fence delimiter
  character and run length, and must leave fenced content excluded until a
  compatible closer has at least the opening run length and only whitespace
  after it.
- REQ-003: The guard's executable fixtures must call the same predicate used
  for the target skill and demonstrate forbidden, allowed, and statement/fence
  boundary cases, including ordinary Markdown wrapping.
- REQ-004: The correction must preserve the accepted WB-SKILL-002
  provider-neutral skill behavior and WB-SKILL-002A lifecycle/P1 correction.
  It must not expand into a broad Markdown parser, a new dependency, or a
  repository-wide provider vocabulary scan.
- REQ-005: The only possible future source implementation path is
  `scripts/test-sdd-contract.sh`. Source execution remains blocked until the
  Owner approves an authoritative specification revision, the exact frozen
  write-set, and the required Define gates have completed.
- REQ-006: The exact frozen source subject must receive independent Reviewer,
  fresh-clone Verifier, and Specification Drift assurance before closeout.

## Acceptance Criteria

- AC-001 [req=REQ-001]: The target-only predicate rejects only direct
  imperative provider-assurance prose in the required normalized forms:
  optional `To verify,`, optional `please` or `kindly`, `ask` or `request`, a
  recognized provider alias, `to`, then `review`, `verify`, or `perform
  verification`. It rejects each form on one line and ordinarily wrapped within
  one Markdown statement.
- AC-002 [req=REQ-001]: The correction remains bounded to recognizable
  provider-assurance imperative patterns required by this Work Block; it adds
  neither repository-wide scanning nor general natural-language inference.
- AC-003 [req=REQ-002]: A regular Markdown fence opener has at most three
  leading spaces, a backtick or tilde run of at least three characters, and an
  optional information-string tail. It records its delimiter character and run
  length; a closer ends exclusion only when it has at most three leading
  spaces, uses the same character, has an equal-or-longer run, and has a
  whitespace-only tail.
- AC-004 [req=REQ-002]: Mismatched delimiter characters, too-short delimiter
  runs, invalid closer suffixes, and unclosed fences remain excluded; valid
  closing fences permit later ordinary prose to be scanned.
- AC-005 [req=REQ-003]: Fixtures invoke the production predicate and cover
  one-line and ordinarily wrapped forbidden imperative samples, including
  `please`/`kindly` and `To verify,` introductions; allowed negatives such as
  `Do not ask Codex to review the implementation.` and advisory controls;
  paragraph-separated terms; a four-backtick opener with a three-backtick
  non-closer; mismatched delimiter, invalid closer suffix, and unclosed fence
  cases; and valid equal-or-longer closure followed by prohibited prose.
- AC-006 [req=REQ-003]: Fixtures prove that unrelated text separated by a
  Markdown statement boundary does not create a provider-assurance match.
- AC-007 [req=REQ-004]: The frozen implementation diff changes only
  `scripts/test-sdd-contract.sh`; it neither modifies
  `skills/codex-verification/SKILL.md` nor alters WB-SKILL-002A lifecycle/P1
  behavior.
- AC-008 [req=REQ-005]: No source task starts while this specification is
  `draft`, the Write Gate is `BLOCKED`, or the exact future source write-set
  lacks recorded Owner approval.
- AC-009 [req=REQ-006]: The exact frozen source subject has independent
  Reviewer `READY`, fresh-clone Verifier `READY`, and Drift `ALIGNED` evidence
  before any terminal closeout.

## Verification Boundary

Define quality, Critic, independent source review, fresh-clone verification,
and drift analysis are required. Evaluation is not required because this is a
deterministic contract-script correction with adversarial fixtures, not
non-deterministic product behavior.

## Non-Goals

- Modifying `skills/codex-verification/SKILL.md` or reverting WB-SKILL-002.
- Reopening or altering WB-SKILL-002A terminal evidence, its P1 lifecycle fix,
  `FILE_REGISTRY.yml`, or `PROJECT_MAP.md`.
- Building a general Markdown parser or adding dependencies.
- Governance/release-state changes, GitHub thread resolution, push, PR, merge,
  rebase, or any external mutation.
- Gemini backlog, legacy convergence, extensions, presets, workflows, or
  bundles.
