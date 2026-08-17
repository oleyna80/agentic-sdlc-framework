# Spec Kit Clarify + Checklist Dry Run — 2026-08-14

## Status

Prompt-level dry run, not a CLI execution.

Direct network cloning of `github/spec-kit` was unavailable in the evaluation
environment. The upstream command definitions were therefore read through the
GitHub API at the pinned benchmark revision:
`bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c`.

This distinction matters: the experiment evaluates the **interaction and review
mechanics** of `specify`, `clarify`, and `checklist`; it does not claim that the
Specify CLI, hooks, filesystem bootstrap, extension system, or runtime integration
were executed.

## Goal

Test whether the two highest-priority Spec Kit ideas expose useful behavior that
is missing or under-specified in the current Agentic SDLC Define stage:

1. bounded targeted clarification before technical planning;
2. requirements-quality checklists that test the written requirements rather
   than the implementation.

## Synthetic feature brief

> Build an appointment booking feature for a small service business. Customers
> can choose a service, select an available time, submit a booking, and receive a
> reminder. Staff can see upcoming bookings and mark them completed or cancelled.

The brief is intentionally plausible but incomplete. It contains enough intent
to produce a useful specification while leaving several decisions that materially
change behavior, data modeling, task decomposition, verification, or operations.

## Baseline: current local specification framing

The current local specification contract naturally captures:

- objective;
- authority and sources;
- in-scope / out-of-scope boundaries;
- behavior and cases;
- acceptance criteria and verification;
- risks / open decisions.

A competent Architect is likely to identify several open decisions from the
brief, but the framework does not currently provide a fixed ambiguity taxonomy,
question prioritization heuristic, or bounded interaction protocol.

Likely local open decisions include:

- whether customers need accounts;
- how availability and double-booking conflicts work;
- whether customers may cancel or reschedule;
- reminder channel and timing;
- timezone policy;
- status-transition permissions;
- service duration/capacity assumptions;
- reminder delivery failure behavior.

The baseline is therefore **capable but agent-dependent**: quality depends more
heavily on the Architect/Critic noticing the right omissions.

## Spec Kit `clarify` mechanics observed

At the pinned revision, `clarify` performs a structured coverage scan across:

- functional scope and behavior;
- domain/data model;
- interaction and UX flow;
- non-functional quality attributes;
- integrations and external dependencies;
- edge cases and failure handling;
- constraints and tradeoffs;
- terminology and consistency;
- completion signals;
- unresolved placeholders and vague language.

It then ranks candidate questions by impact and uncertainty, asks at most five,
and restricts questions to decisions that materially affect architecture, data,
tasks, tests, UX, operations or compliance.

The command asks questions sequentially, one at a time, and writes each accepted
answer back into the specification immediately.

## Dry-run clarification queue

Applying that mechanism to the synthetic brief yields the following high-impact
queue.

### Q1 — booking identity

**Question:** Can a customer create a booking without creating an account?

Why it matters: the answer changes identity, contact verification, data model,
privacy requirements and the primary booking flow.

Candidate recommendation for a small service business: guest booking with
required contact details, unless the product already has an account system.

### Q2 — slot ownership and concurrency

**Question:** What should happen when two customers attempt to reserve the same
available time?

Why it matters: this changes the availability contract, concurrency semantics,
error behavior and acceptance tests.

Candidate recommendation: one confirmed booking per capacity unit; the first
successful reservation consumes the slot and the second user receives a clear
conflict response with refreshed alternatives.

### Q3 — customer changes

**Question:** May customers cancel or reschedule their own booking after it is
created?

Why it matters: this adds lifecycle states, permissions, recovery flows and
notification requirements.

No universal default is safe here; business policy materially changes scope.

### Q4 — reminder contract

**Question:** Which reminder channel and timing are required for the first
version?

Why it matters: the current word "reminder" is not testable without a delivery
channel, trigger time and failure expectation.

A simple default might be one email reminder at a defined interval, but this is
product policy and should be explicit.

### Q5 — time interpretation

**Question:** Which timezone governs displayed and stored appointment times when a
customer and the business are in different timezones?

Why it matters: inconsistent timezone assumptions can create incorrect bookings
while appearing technically valid.

Candidate recommendation: business timezone is authoritative for appointment
slots; user-facing display rules are explicit.

## Clarify result

The dry run confirms a real local gap: **we have ambiguity detection as a role
responsibility, but not yet as a reusable protocol with coverage categories,
impact prioritization and bounded questions.**

The useful part is not the five-question limit itself. The useful mechanisms are:

- structured ambiguity coverage;
- impact × uncertainty prioritization;
- questions only for decisions that change downstream work;
- accepted answer written back to the authoritative spec;
- no silent continuation on unresolved blocking ambiguity.

### Local adaptation insight

Do **not** copy the exact interaction model unchanged.

One-question-at-a-time is safe but can impose unnecessary human latency. A local
framework-native protocol should support a small batch of independent high-impact
questions when batching does not cause answer coupling, while preserving
sequential questioning for dependent decisions.

Recommended local rule:

```text
repository/discovery-resolvable fact -> resolve without asking Owner
reasonable non-material default       -> record explicit assumption
material independent ambiguity        -> ask in bounded batch
material dependent ambiguity          -> ask sequentially
unresolved blocking ambiguity          -> keep Define blocked
```

This is a material local delta and therefore remains `adapted`, not `adopted`.

## Spec Kit `checklist` mechanics observed

At the pinned revision, the custom checklist command explicitly treats the
specification as code written in English and the checklist as a requirement-level
test suite.

The generated items evaluate:

- completeness;
- clarity;
- consistency;
- measurability;
- scenario/edge-case coverage;
- non-functional requirement coverage;
- dependencies and assumptions;
- ambiguity/conflict handling;
- traceability.

Important ownership rule: a generated custom checklist is reviewer-owned;
creation does not mark items complete, and checked requirements-quality items do
not mean implementation is complete.

## Dry-run requirements checklist

A useful requirements-quality checklist for the synthetic brief would include
items such as:

### Scope and actors

- [ ] Are the customer and staff roles defined with their permitted booking
  actions? [Completeness]
- [ ] Is guest-versus-account booking explicitly specified? [Gap]
- [ ] Is first-version scope explicit about customer cancellation and
  rescheduling? [Gap]

### Availability and lifecycle

- [ ] Is the rule for deriving an "available" slot defined, including service
  duration and capacity? [Gap]
- [ ] Is concurrent reservation conflict behavior explicitly specified?
  [Coverage]
- [ ] Are valid booking status transitions and the actors allowed to trigger
  them documented? [Completeness]

### Reminder behavior

- [ ] Is the reminder channel specified? [Gap]
- [ ] Is reminder timing measurable relative to the appointment start?
  [Measurability]
- [ ] Are requirements defined for reminder delivery failure or unavailable
  contact information? [Exception Flow]

### Time and locale

- [ ] Is the authoritative appointment timezone specified? [Gap]
- [ ] Are daylight-saving or cross-timezone display expectations defined where
  relevant? [Edge Case]

### Data and privacy

- [ ] Are the minimum customer contact fields required for a booking specified?
  [Completeness]
- [ ] Are retention/deletion expectations for customer booking data explicitly
  stated or intentionally delegated to an existing project policy? [Dependency]

### UX and failure states

- [ ] Are requirements defined for no available slots? [Coverage]
- [ ] Are requirements defined for a slot becoming unavailable between display
  and submission? [Recovery]
- [ ] Is customer-visible confirmation after successful booking specified?
  [Completeness]

### Acceptance quality

- [ ] Can every primary booking requirement be objectively verified without
  inferring undocumented behavior? [Measurability]
- [ ] Are measurable success criteria present for booking creation and conflict
  handling? [Acceptance Criteria]
- [ ] Is there a requirement/acceptance identifier scheme sufficient to trace
  implementation tasks back to approved behavior? [Traceability]

## Checklist result

This mechanism is clearly useful because it separates two questions that the
current Critic can otherwise mix together:

1. **Is the requirement well specified?**
2. **Is the proposed architecture/plan safe and appropriate?**

The first question deserves a distinct artifact or explicit Critic sub-pass. A
requirements-quality gate would reduce the chance that the Critic spends time
reviewing an architecture built on ambiguous requirements.

## Comparison

| Dimension | Current local baseline | Spec Kit mechanism | Local conclusion |
|---|---|---|---|
| Ambiguity discovery | role-driven, flexible | explicit coverage taxonomy | Spec Kit is more deterministic |
| User-question control | no dedicated protocol | max five, impact-prioritized | adapt with batch/sequential modes |
| Assumption handling | supported by specification/risk practice | guesses reasonable defaults and reserves questions for high-impact uncertainty | align, but local framework should classify assumptions explicitly |
| Requirements review | partly inside Critic | dedicated requirements-quality model | adapt as separate gate/sub-pass |
| Checklist ownership | local review roles exist | reviewer-owned; implementer cannot silently self-approve | strongly aligned |
| Traceability pressure | available through artifacts/Work Blocks but not uniformly encoded per requirement | checklist expects high traceability and tasks are story-linked | adapt explicit IDs/links |
| Authority | structural Work Block/write gate | checklist influences implementation readiness | keep local authority model |

## Findings

### Finding 1 — `clarify` is worth adapting

Confidence: high.

The main value is the ambiguity taxonomy and prioritization algorithm, not the
slash-command UX.

### Finding 2 — requirements-quality review should become explicit

Confidence: high.

The distinction between requirement correctness/quality and implementation
verification is architecturally clean and fits the existing Define/Assure split.

### Finding 3 — exact Spec Kit interaction should not be copied

Confidence: medium-high.

Sequential single-question interaction minimizes coupling but increases Owner
interaction overhead. The local implementation should select batch vs sequential
questioning based on dependency between decisions.

### Finding 4 — the best integration point is before technical planning/Critic

Confidence: high.

The refined flow should be:

```text
specification framing
  -> ambiguity scan / clarification
  -> requirements-quality review
  -> architecture + plan
  -> task decomposition
  -> pre-execution analysis
  -> Critic
  -> write gate
```

This prevents architecture critique from compensating for poor requirements.

## Provenance

### Candidate clarification protocol

- **Classification:** `adapted`
- **Source:** `github/spec-kit`, `templates/commands/clarify.md`, revision
  `bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c`
- **Local delta:** repository-first resolution, explicit assumption class,
  batch/sequential selection, Work Block blocking semantics
- **Novelty claim:** none

### Candidate requirements-quality gate

- **Classification:** `adapted`
- **Source:** `github/spec-kit`, `templates/commands/checklist.md`, revision
  `bf88c9f9a82fa370c7a7257aa2b3cf10b457b65c`
- **Local delta:** local role/authority model remains normative; checklist is
  quality evidence and cannot grant write authority
- **Novelty claim:** none

## Next experiment

The next useful pilot is task decomposition + read-only `analyze`, because those
two mechanisms can be evaluated together for requirement-to-task coverage and
safe parallel write-set routing.
