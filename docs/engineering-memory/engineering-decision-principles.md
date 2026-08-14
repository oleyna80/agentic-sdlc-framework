---
schema_version: 1
artifact_type: engineering_memory
artifact_id: engineering-decision-principles
status: promoted
owner_role: owner
last_verified: 2026-08-14
authority: lower_than_root_agents_and_accepted_governance
review_trigger: material_change_to_project_scale_risk_model_or_operating_context
---

# Engineering Decision Principles

This document explains the engineering posture summarized in `AGENTS.md`.
It is durable guidance, not a substitute for current Owner instruction,
accepted governance, specifications, ADRs, or an active Work Block.

The objective is not to minimize engineering quality. It is to choose the
**simplest sufficient solution** for the actual requirement, credible risk, and
operating scale.

## 1. Prefer the simplest sufficient solution

Choose the simplest design that reliably satisfies the requirement and its
acceptance criteria. Do not add abstractions, services, gates, protocols,
configuration layers, or infrastructure unless they solve a concrete problem.

Simple does not mean careless. Tests, error handling, security boundaries, and
recovery mechanisms remain necessary when the requirement or credible risk
justifies them.

## 2. Complexity must pay for itself

Before materially increasing complexity, identify:

- the concrete failure or risk being addressed;
- how likely and consequential it is in the actual environment;
- the simplest viable alternative;
- the implementation, maintenance, debugging, cognitive, and operational cost;
- the new failure modes introduced by the control itself.

If the additional mechanism cannot be justified against those costs, prefer the
simpler solution.

## 3. Design for actual scale, not hypothetical enterprise scale

Use the real operating context: number of users, developers, deployers,
deployment frequency, exposure, data sensitivity, project lifetime, and threat
model.

A project with one trusted deployer does not automatically need the same
controls as a multi-team production platform. Do not build for hypothetical
scale before the scale creates a real requirement.

## 4. Make security proportional to credible risk

Protect real boundaries such as secrets, authentication and authorization,
externally exposed services, destructive operations, production data, and
supply-chain integrity.

Do not add cryptographic ceremonies, multi-stage authorization systems, or
enterprise-grade controls to reversible development operations merely because
they are theoretically stronger. Prefer a small number of understandable,
independently meaningful controls.

This is not a rule against strong security. Strong controls are appropriate when
there is a credible threat and a real boundary for them to protect.

## 5. Prefer existing mechanisms over custom machinery

Use existing platform, operating-system, runtime, repository-hosting, and CI/CD
capabilities when they adequately solve the problem.

Prefer this order:

1. existing platform capability;
2. simple configuration;
3. small local implementation;
4. custom framework or protocol only when necessary.

Do not rebuild a weaker project-local version of a boundary already enforced
more reliably outside the project.

## 6. Add complexity incrementally and prefer reversible decisions

Start with the minimum reliable implementation. Observe real limitations, then
add controls or abstractions when evidence shows they are needed.

When several solutions are adequate, prefer the one that is easier to
understand, test, debug, roll back, remove, or replace.

## 7. Distinguish blockers from improvements

Classify findings before changing the system. A finding may be:

- a correctness or security blocker;
- a material operational risk;
- a maintainability issue;
- an optional improvement;
- a cosmetic preference.

Do not treat every possible improvement as a release blocker, and do not perform
large refactors solely to make an already sufficient implementation more
elegant.

## 8. Optimize total engineering economics

Developer time, agent time, tokens, review effort, debugging effort, and
operational attention are finite resources.

Evaluate a proposed mechanism using its total cost, not only its theoretical
benefit. A technically valid improvement can still be the wrong decision when
its implementation and maintenance cost is disproportionate to the risk or
problem it removes.

## 9. Every control creates a failure surface

A guardrail, validator, workflow, security gate, abstraction, or automation is
itself software and can fail.

Do not assume reliability increases monotonically as controls are added.
Evaluate whether a new mechanism removes more meaningful failure modes than it
creates.

## 10. Stop when the requirement is satisfied

Once acceptance criteria, relevant security boundaries, and required assurance
are satisfied, prefer completion over additional sophistication.

Further improvement should require a concrete benefit, new evidence, or a new
requirement rather than the mere possibility of making the design more complex.

## Default decision rule

When uncertain, choose the simplest reliable and maintainable solution
appropriate to the project's actual scale and credible risk. Escalate complexity
only when evidence, a real boundary, or an explicit requirement justifies it.
