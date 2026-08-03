---
schema_version: 1
artifact_type: verification
artifact_id: wb-core-003b-preliminary-verification
work_block_id: WB-CORE-003B
reviewed_stage: preliminary_assure
reviewed_subject: repaired initial normative subject
verdict: READY
isolation: separate_subagent
recorded_by_role: orchestrator
---

# Preliminary Verification — WB-CORE-003B

This evidence-only record faithfully transcribes independent Verifier outputs.
It is excluded from the repaired normative subject.

## Current result

**Verdict: READY.**

The second independent Verifier recomputed the repaired initial-subject
SHA-256 as `44c9e571f4e7a34cb072434f40851604473423292f20cf05c97376c63334d32b`.
It found exactly twelve approved non-operational subject paths, six approved
lower-authority operational records, and predeclared evidence-only reports;
map and registry were unchanged. SDD, governance, release-state fixtures,
relative links, metadata/truthful-state, capability neutrality, format, and
secret-marker checks passed. The Verifier was a `separate_subagent` read-only
context. This result applies only before terminal projection.

## Superseded first result

The first independent Verification returned `BLOCKED` solely because
`.agent/ROSTER.md` linked `../../AGENTS.md` outside the worktree. Its
initial-subject SHA-256 was
`74d9fe97756dd30398c96292fc6e87c8ac535c7dbede888890e1b68d96401799`.
The Coder corrected the link and related review findings within the initial
write-set; the current result above supersedes that block without concealing it.
