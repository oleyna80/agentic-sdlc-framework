# Independent Review — WB-010 skill-library maintenance integration

## Scope and subject

The read-only review covered the complete candidate diff against base revision
`96f4a50e3c485c3de641c8841fa6d982f2b199d8`, including the deterministic
bootstrap mode repair and the review correction. The final reviewed
implementation subject is:

`e4279a416d60ccd13ad7d51620a60fa4d0e2b322`

The candidate implementation was produced before WB-010. This review therefore
assesses whether that existing diff may be admitted; it does not represent the
candidate as having been pre-approved.

Reviewed surfaces:

```text
SETUP.md
bootstrap/profiles.json
framework/workflow/external-skill-discovery.md
framework/workflow/skill-routing-gate.md
skills/catalog.yml
skills/skill-library-maintenance/**
template/.agent/ROSTER.md
template/AGENTS.md
template/CLAUDE.md
bootstrap.sh file mode
```

## Review questions

1. Is external skill discovery read-only until an exact Owner-approved adaptation
   write-set exists?
2. Are moving refs resolved to immutable commit SHAs before comparison or
   provenance recording?
3. Does unavailable GitHub evidence fail closed rather than become a current or
   safe result?
4. Can imported instructions, scripts, tools, hooks, credentials, or permissions
   override local governance?
5. Are source priority and the optional watchlist clearly non-authoritative?
6. Does baseline installation remain deterministic and profile-driven?
7. Are generated runtime contracts aligned across the roster, `AGENTS.md`, and
   `CLAUDE.md`?
8. Does the change preserve bootstrap behavior, executable mode, publication
   safety, and release-state authority?

## Findings

### HIGH / P1

None.

### MEDIUM / P2

#### Resolved — unbound license assertions in the ecosystem watchlist

The original watchlist described several external repositories as MIT or
Apache-2.0 without recording a check date, resolved immutable revision, or
license evidence. Those statements could become stale and contradicted the new
skill's own provenance rules.

Resolution in `e4279a416d60ccd13ad7d51620a60fa4d0e2b322`:

- removed unbound license claims from the discovery table;
- stated that the table is discovery metadata only;
- required a resolved SHA, check date, license evidence, local delta, and decision
  before recommendation or adaptation;
- classified missing evidence as `unverified` or `license-blocked`.

### LOW / P3

None requiring correction.

## Observations

- `skill-library-maintenance` separates discovery/comparison from adaptation.
- External GitHub content is explicitly untrusted and is never executed during
  discovery.
- An update classification is only a proposal; it grants no write authority.
- The provenance schema requires a full immutable revision and license evidence.
- Priority sources define lookup order, not publisher trust or adaptation rights.
- The watchlist is opt-in and cannot become an automatic installer or poller.
- The skill cannot grant commit, push, publish, credential, integration, or
  external-contact authority.
- The core installation manifest includes the skill consistently with setup and
  generated-project routing documentation.
- Root `bootstrap.sh` mode `100755` was restored after the first CI failure.
- Repository required checks remain external live merge authority; neither the
  skill nor this review authorizes merge.

## Scope integrity

The admitted implementation changes only skill guidance, skill/catalog content,
installation composition, generated-project operating documentation, and related
setup guidance. It introduces no product behavior, dependency upgrade, schema,
data, deployment, credential, repository ruleset, or automatic external-service
change.

## Verdict

**APPROVED / READY.** The medium evidence-quality finding is resolved. The
corrected implementation is bounded, fail-closed, internally consistent, and
suitable for deterministic verification and repository closeout. External skill
adaptation, scheduling, integration, publication, and merge remain separate
Owner-controlled actions.
