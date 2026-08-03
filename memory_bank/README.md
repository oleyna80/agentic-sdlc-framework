# Operational Memory Bank

This directory carries concise, secret-free operating context between sessions.
It supports work but never grants authority or overrides approved artifacts.
Detailed assurance belongs in `docs/reports/`; reusable verified knowledge
belongs in `docs/engineering-memory/`.

| Record | Responsible role | Update rule | Retrieval rule |
| --- | --- | --- | --- |
| `context.md` | Orchestrator | replace only when current context materially changes | read at session start after higher authority |
| `progress.md` | Orchestrator | append material stage outcomes and next actions | retrieve for the active Work Block only |
| `decisions.md` | Orchestrator | append accepted Owner decisions with durable authority | retrieve after governing authority is read |
| `orchestrator-log.md` | Orchestrator | append routing, gate, and handoff facts | retrieve when resuming orchestration or a handoff |
| `review-log.md` | Orchestrator | append evidence-report links and report-backed verdicts | retrieve before assurance routing; do not infer a verdict without its report |

Retrieve current higher authority first, then only the relevant operational
entry. Each entry must link its source when practical and label proposed,
pending, blocked, or unverified state. Operational memory cannot be the sole
record of an accepted decision, required evidence, authorized scope, blocker,
or next authorized action. Never add transcripts, hidden reasoning, tokens,
credentials, private payloads, or unverified completion claims.
