---
schema_version: 1
artifact_type: drift_assessment
artifact_id: wb-core-003a-drift-assessment
work_block_id: WB-CORE-003A
reviewed_stage: Evidence
reviewed_subject: working-tree artifact subject based on 1710c44bf38ddfb2330e86838e8f976b5e9a71d6 plus five normative paths; diff_sha256 1e05ba31861e606c26b4f1741e670317fff601e5db01b871933985a8d53d67bb
verdict: READY
final_reviewed_subject: working-tree terminal artifact based on 1710c44bf38ddfb2330e86838e8f976b5e9a71d6 plus nine ordered normative and lifecycle paths
final_subject_manifest_kind: canonical_content_aggregate
final_subject_manifest_sha256: 7b4235d451d549dd6cfbaccb2e6c4dd84ca8323a6a6f6e6fc78a4f3dbacc893e
final_drift_conclusion: ALIGNED
created_at: 2026-08-03
---

# Drift Assessment — WB-CORE-003A

## Subject and Boundary

This assessment covers a working-tree artifact, not a commit, created from
base `1710c44bf38ddfb2330e86838e8f976b5e9a71d6`. The exact normative subject is:

```text
docs/specs/portable-agentic-sdlc-project-kit.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/work-block.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/closeout-report.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/task-decomposition/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/ssot-sync-closeout/SKILL.md
```

`git diff --binary -- <the five paths above>` has SHA-256
`1e05ba31861e606c26b4f1741e670317fff601e5db01b871933985a8d53d67bb`.

## Assessment

| Boundary | Evidence | Result |
| --- | --- | --- |
| Candidate state | `candidate/portable-agentic-sdlc-kit/CANDIDATE.md` continues to declare the kit draft, noncanonical, uninstalled, unpromoted, and non-authoritative. | ALIGNED |
| Product boundary | The frozen five-path diff modifies a specification and candidate templates or skills only. It changes no installer, runtime, provider or model routing, hooks, MCP, plugin, configuration, or legacy `template/` path. | ALIGNED |
| Evidence-only barrier | Material findings have required observable and evidence fields and are forbidden from maps, registries, plans, and tasklists; the closeout template and `ssot-sync-closeout` retain them in reports. | ALIGNED |
| Role and write-set separation | The rule retains one Coder-owned write-set; the task list assigns Critic, Reviewer, and Verifier report-only authority, and the Reviewer wrote no normative path. | ALIGNED |
| Lifecycle | The change retains Define → Execute → Assure → evidence-only reports → Close and creates no competing transition or source of truth. | ALIGNED |

## Verdict and Invalidation

**Verdict: READY.** Findings: 0.

The assessment found no drift beyond the accepted Portable Agentic SDLC Project
Kit boundary. It does not promote, install, or grant authority to the candidate,
and it does not authorize installer, runtime, configuration, commit, push, merge,
or external action.

Any change to one of the five named normative paths changes the reviewed subject
and invalidates this READY assessment. Re-run independent assurance against the
new exact subject before relying on it.

## Checks and Limitation

- Recomputed the exact five-path binary-diff SHA-256.
- `git diff --check` passed.
- `python3 scripts/validate-release-state.py` returned `READY`.
- No automated candidate-contract test specifically exercises these textual rules;
  reproducible diff, structural, and accepted-contract checks provide the current
  evidence.

No prompts, transcripts, hidden reasoning, secrets, or mutable activity log are
recorded in this report.

## Final Re-assessment — Nine-Path Terminal Subject

This final re-assessment preserves the preceding preliminary five-path record.
It assesses the terminal working-tree artifact, not a commit, based on
`1710c44bf38ddfb2330e86838e8f976b5e9a71d6` and these paths in this exact order:

```text
docs/specs/portable-agentic-sdlc-project-kit.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/work-block.md
candidate/portable-agentic-sdlc-kit/template/agentic/templates/closeout-report.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/task-decomposition/SKILL.md
candidate/portable-agentic-sdlc-kit/template/agentic/skills/ssot-sync-closeout/SKILL.md
PROJECT_MAP.md
FILE_REGISTRY.yml
docs/plans/wb-core-003a-work-block-composition-and-flow-feedback.md
docs/tasklist/wb-core-003a.md
```

The canonical-content aggregate SHA-256 is
`7b4235d451d549dd6cfbaccb2e6c4dd84ca8323a6a6f6e6fc78a4f3dbacc893e`.
It is calculated by hashing each listed file as
`<content-sha256><two spaces><path><newline>` in that order, then hashing the
resulting byte stream. It is deliberately not a `git diff --binary` digest,
because the terminal subject includes untracked lifecycle artifacts.

### Drift Result

**Conclusion: ALIGNED.** Findings: 0.

| Boundary | Final evidence | Result |
| --- | --- | --- |
| Source hierarchy | The map retains the accepted Portable Kit as target architecture and the runtime-neutral control plane as the current operational architecture. The completed plan and tasklist bind lifecycle evidence but do not override Owner instruction, root governance, accepted specification, or ADR authority. | ALIGNED |
| Candidate nonauthority | `candidate/portable-agentic-sdlc-kit/CANDIDATE.md` still declares the kit draft, noncanonical, uninstalled, unpromoted, and without current repository authority. | ALIGNED |
| Runtime neutrality | The nine-path subject contains no runtime adapter, installer, provider/model routing, hook, MCP, plugin, configuration, or legacy-template change. The map expressly records that no runtime adapter was installed. | ALIGNED |
| Evidence-only barrier | The candidate rule keeps material findings in reports and excludes them from maps, registries, plans, and tasklists. This re-assessment is itself a report outside the nine-path subject; adding it changes no normative navigation or authority state. | ALIGNED |
| Lifecycle consistency | `PROJECT_MAP.md`, `FILE_REGISTRY.yml`, the completed plan, and tasklist agree on WB-CORE-003A completion, no active Work Block, the exact closeout binding, and WB-CORE-004 as planned. The final Reviewer and Verifier evidence bind the same nine-path aggregate. | ALIGNED |

The closeout's terminal values are expressly an uncommitted repository-local
projection, not a claim about staging, commit, push, merge, release,
installation, promotion, or external mutable state. Recording this evidence-only
final drift result does not promote the candidate or alter that boundary.

### Final Checks and Invalidation

- Recomputed the canonical-content aggregate SHA-256 above.
- `git diff --check -- <the nine paths above>` passed; the two untracked
  lifecycle paths also had no trailing whitespace.
- `bash scripts/test-sdd-contract.sh` passed.
- `python3 scripts/test-release-state-contracts.py` passed.
- `python3 scripts/validate-release-state.py` returned `READY` with fifteen
  completed Work Blocks and no active Work Block.

Any change to one of the nine listed paths changes the terminal subject and
invalidates this conclusion. Re-run final applicable assurance against the new
exact subject before relying on it. No prompts, transcripts, hidden reasoning,
secrets, or mutable activity log are recorded here.
