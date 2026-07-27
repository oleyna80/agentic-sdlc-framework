---
schema_version: 1
artifact_type: review_report
artifact_id: pr-8-final-review
status: approved
owner_role: reviewer
work_block_id: wb-008
subject_revision: 9ae16b927aa072a81f4fdc58a773fddeb8aafac8
created_at: 2026-07-26
last_verified: 2026-07-27
---

# PR #8 Final Review — Post-Merge SSOT Reconciliation and Release Gate

## Scope

Reviewed implementation revision
`9ae16b927aa072a81f4fdc58a773fddeb8aafac8` against:

- `docs/plans/wb-008-post-merge-ssot-release-gate.md`;
- `governance/release-state.md`;
- normalized Work Blocks WB-001 through WB-008;
- `PROJECT_MAP.md` and `FILE_REGISTRY.yml`;
- existing closeout reports bound to completed Work Blocks;
- `scripts/validate-release-state.py`;
- `scripts/test-release-state-contracts.py`;
- `.github/workflows/release-state-contract.yml`;
- all seven Codex Review rounds on PR #8.

## Review Verdict

**READY**

No known blocking engineering, governance, authority, or release-state findings
remain on the reviewed implementation revision.

## Review Convergence

Seven Codex Review rounds produced fourteen P1 findings and three P2 findings. All
were accepted, fixed, and covered by positive or adversarial fixtures.

### Initial SSOT and parser findings

- WB-007 and earlier Work Blocks retained stale or non-canonical lifecycle state;
- mutable hosting-platform state was stored as repository closeout SSOT;
- closeout identity used substring matching;
- machine and visible map state could disagree;
- release assets and latest-completed ordering were incompletely bound;
- drift used substring matching;
- duplicate closeout markers used last-value-wins behavior;
- active-path validation was scoped to the whole map document.

### Second review findings

- completed Work Blocks accepted blocked or unverified terminal verdicts;
- required evaluation could be omitted from closeout;
- ordinary mutable PR-state assertions were not fully recognized;
- residual-risk and follow-up closeout sections were not enforced.

### Third review findings

- non-evaluation terminal suffixes were discarded;
- mutable VCS claims in YAML frontmatter bypassed body-only scanning;
- colon-form PR status assertions were missed.

### Fourth review finding

#### F-015 — Structured and Markdown PR-state assertions were missed

**Severity:** P1  
**Resolution:** fixed

The complete-document text scan permitted structured keys such as
`pr_status: merged` or `pull_request_state: open`, as well as common Markdown forms
that separated the pull-request identifier from its state.

Resolution:

- parsed YAML frontmatter is recursively inspected;
- key spelling is normalized across underscores, hyphens, spaces, and nesting;
- compound PR/pull-request/merge `status` and `state` keys reject mutable values;
- bold Markdown identifier/state forms and table rows are rejected;
- dedicated fixtures cover direct, nested, bold, plain-table, and bold-table forms.

### Fifth review findings

#### F-016 — VCS parent context was lost during YAML recursion

**Severity:** P1  
**Resolution:** fixed

Natural nested frontmatter such as `pr: {status: merged}` and
`pull_request: {state: open}` separated the VCS parent from the generic descendant
key.

Resolution:

- recursive structured inspection carries an explicit VCS-context flag;
- normalized `pr`, `pull_request`, `pullrequest`, and `merge` parents establish that
  context through dictionary and list descendants;
- `status` or `state` under that context rejects exact mutable-state values.

#### F-017 — Mutable state could be appended to the boundary marker

**Severity:** P1  
**Resolution:** fixed

The `External VCS state` marker accepted any value beginning with `non-normative`,
including a concrete appended merge state.

Resolution:

- boundary validation still requires the non-normative prefix;
- the remainder is independently scanned for mutable-state tokens;
- negative and clean-marker positive fixtures preserve the ownership boundary.

### Sixth review finding

#### F-018 — Bare pull-request state assertions were missed

**Severity:** P1  
**Resolution:** fixed

Terse prose such as `PR #9 merged.` or `Pull request #9 closed.` omitted a colon,
equals sign, or connector verb and bypassed the prose grammar.

Resolution:

- direct identifier-plus-state prose is rejected;
- regressions cover open, Draft, merged, Ready for Review, and closed forms;
- a positive fixture preserves a PR reference without a mutable state.

### Seventh review findings

#### F-019 — Markdown decoration around the state token bypassed detection

**Severity:** P2  
**Resolution:** fixed

A closeout could format both sides of the assertion, for example
`**PR #9:** **merged**`, because the state matcher expected the token immediately
after whitespace.

Resolution:

- a shared Markdown-aware mutable-state fragment permits optional `**` around the
  state token;
- prose, bold-label, status/state-label, and Markdown-table patterns use the same
  fragment;
- regressions cover bold state values in prose and table cells.

#### F-020 — Historical completed-Work-Block closeouts were not validated

**Severity:** P2  
**Resolution:** fixed

The release gate validated only the canonical latest closeout. An existing earlier
closeout could therefore retain adverse lifecycle evidence while the latest closeout
remained valid.

Resolution:

- the validator scans existing `docs/reports/closeout/**/*.md` artifacts;
- closeout reports bound to completed Work Block IDs require approved status, exact
  successful lifecycle markers, matching evaluation semantics, a non-normative
  external-state boundary, and mandatory residual-risk and follow-up sections;
- duplicate historical closeouts for the same completed Work Block ID fail closed;
- the canonical latest closeout remains subject to its stricter identity and
  complete-document mutable-state validation;
- positive and adverse historical-closeout fixtures prove both paths.

## Contract Review

### Exact terminal-state semantics

- non-evaluation terminal values are exact and carry no rationale suffix;
- evaluation accepts exact `READY` or documented `SKIPPED` only;
- contradictory suffixes, malformed skips, and adverse tokens fail closed.

**Result:** aligned.

### Repository and hosting-platform boundary

- Work Block lifecycle and closeout remain repository-owned;
- mutable hosting-platform assertions are rejected across prose, parsed frontmatter,
  VCS-parent descendants, boundary-marker payloads, and Markdown forms;
- historical closeouts cannot retain adverse lifecycle evidence unnoticed;
- external state cannot grant authority or redefine closeout.

**Result:** aligned.

### Regression and CI coverage

The fixture suite covers:

- Work Block and closeout exact-value suffix attacks;
- malformed evaluation rationale;
- connector and bare prose, structured frontmatter, normalized compound keys,
  parent-key descendants, Markdown-decorated state values, and table assertions;
- mutable state appended to the non-normative marker plus a clean-marker positive;
- a positive PR reference carrying no mutable state;
- valid and adverse historical closeouts bound to completed Work Blocks;
- all previously resolved path, identity, marker, section, and map drift classes.

**Result:** aligned.

## Verification Evidence

Implementation revision:
`9ae16b927aa072a81f4fdc58a773fddeb8aafac8`.

Workflow-restored validation head:
`1b46c028fb7e1205dda77820694e8b9a43f2f406`.

Successful runs:

- Release State Contract run **134**;
- Framework Contracts run **583**.

Earlier failed, corrective, action-required, and helper-workflow runs remain recorded
as their actual outcomes; no non-successful run was converted into passing evidence.

## Residual Limitations

- Markdown headings and YAML frontmatter form a versioned schema; schema changes
  must update validator and fixtures together.
- Historical discovery validates existing closeout reports bound to known completed
  Work Block IDs; it does not infer missing legacy closeouts that were never created.
- Pattern and structured-key detection are governance guardrails, not a general
  natural-language theorem prover.
- Hosting-platform state is queried externally rather than committed as normative
  closeout data.
- This Work Block does not create a release tag or prove live runtime, provider,
  plugin/MCP, telemetry, or OS isolation behavior.

## Recommendation

Run both workflows on the final evidence head, reply to and resolve the two
seventh-round Codex threads, request one final Codex Review, and keep integration
under explicit Owner approval.
