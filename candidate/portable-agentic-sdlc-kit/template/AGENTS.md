# Future Installed Project Authority

This file becomes the installed project root authority only after a later safe
installer. While in the candidate it is draft, noncanonical, uninstalled, and
unpromoted, with no current authority in the current repository.

## Source of truth and lifecycle

Order: current Owner instruction; this root file; accepted specifications and
decisions; active Work Block; approved plan/tasklist; mission brief; frozen
artifact; assurance reports; committed memory; local/external notes. Follow the
authoritative lifecycle in this order:

```text
Intake/classify
  → Define: discovery, architecture, specification, plan/tasks, Critic
  → Execute: bounded implementation and self-checks
  → Assure: Reviewer and Verifier against an exact normative subject
  → Close: SSOT/memory sync and truthful closeout
```

When applicable, Owner-authorized status finalization, final applicable
assurance, an evidence-only report commit, and CI on the resulting PR head occur
between Assure and Close; separate Owner-controlled integration follows Close.
Lower artifacts, roles, and skills cannot expand authority, scope, write-set,
side effects, Hard Stops, or approval requirements.

## Roles and stops

Orchestrator routes and closes; Architect designs; Critic challenges assumptions;
one Coder changes one exact approved write-set; Reviewer and Verifier are
read-only. Stop for unapproved scope, architecture, dependencies, configuration,
secrets, destructive action, deployment, external side effect, failed required
verification, or unclear authority. Route work through `agentic/roles/`; use
procedures only as non-authoritative guidance.
