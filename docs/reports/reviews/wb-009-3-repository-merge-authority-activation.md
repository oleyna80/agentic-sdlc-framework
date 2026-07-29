# Independent policy review: WB-009.3 repository merge authority activation

## Scope and verdict

Preflight review was independent and read-only. It confirmed that the approved
policy is representable by one active repository branch ruleset and that the
exact GitHub Actions job contexts are `contracts` and `release-state`, both
from integration `15368`. The review approved the one-time policy mutation only
within the Work Block's stated policy shape.

## Pre-state

On 2026-07-28, provider reads of `/repos/{repository}/rulesets` and
`/repos/{repository}/rules/branches/main` both returned an empty array. `main`
had no live repository ruleset authority.

## Required policy shape

- target: only `refs/heads/main`; enforcement: `active`; bypass actors: none;
- rules: `deletion`, `non_fast_forward`, pull request with zero required
  approvals and required conversation resolution, and strict required-status
  checks;
- check contexts: only `contracts` and `release-state`, each bound to GitHub
  Actions integration `15368`;
- no merge queue, deployment, signature, snapshot, aggregate, or other gate.

## Review risks retained for verification

1. `release-state` appears from both `push` and `pull_request`, so provider
   evidence must bind check context and app identity precisely.
2. PR #9 initially had an unresolved conversation. Required conversation
   resolution could correctly keep it blocked after check success; WB-009.3
   could not alter PR metadata merely to make the test green.
3. A direct-push rejection was not dynamically tested because that would have
   been a risky write to `main`; effective provider rules were the approved
   evidence.

The initial final verdict was deferred to independent verification of the exact
created ruleset and the authorized rerun trajectory.

## Durable closeout update

Following Owner-approved resolution of the sole review conversation, an
independent read-only live-provider re-verification at `2026-07-28T18:41:04Z`
returned `READY` for subject SHA `f6650acfa357411485d0f205532ca69f235d700e`
under ruleset `19916164`. The required checks `contracts` and `release-state`
were successful, unresolved review threads were `0`, and merge eligibility was
confirmed by REST `mergeable: true` and GraphQL `mergeable: MERGEABLE`.

GraphQL also observed `mergeStateStatus: UNSTABLE`, solely because historical
`final-aggregator=failed` remained in the status history. That check was
non-required and non-authoritative: it was not a ruleset requirement and did
not affect the live ruleset gate or merge eligibility.

The earlier verifier `BLOCKED` outcome remains the historical interim verdict;
the later re-verification is `READY`, and WB-009.3 is `SUCCESS`. This
time-bounded provider read does not claim to prevent future reruns or future
provider-state changes.

## Integration note

The evidence originated in commit
`6781f9ee470bc35b2b88478e5f23ed9609fc836b`. Owner approval on 2026-07-29
authorized its docs-only integration from a fresh `main` branch. Repository URL
markers were normalized for publication hygiene. The later canonical WB-009
closeout remains authoritative for the parent lifecycle and is not modified or
reopened by this evidence import.
