# Decision Log

Append accepted decisions only. Promote durable decisions to
`docs/engineering-memory/` when later Work Blocks depend on them.

| Date | Work Block | Decision | Authority / rationale |
| --- | --- | --- | --- |
| 2026-08-03 | WB-CORE-003B | Reconcile self-hosting policy from accepted baseline; local drafts are selectively reviewed reference input only. | Owner-approved WB-CORE-003B; accepted governance and Portable Kit ADR boundary remain controlling. |
| 2026-08-27 | TBD — post-PR #20 framework retrospective | Adopt risk-based authority as the target operating model: reversible local work (analysis, implementation, local fixes/commits, local assurance/reconciliation) should be agent-autonomous; Owner control should concentrate on scope expansion and external/authority-sensitive boundaries such as push/force-push, published PR mutation, merge, deployment, production/data/secret operations. Quality should be enforced primarily through contracts, deterministic gates, independent assurance, evidence, and race guards rather than repeated Owner confirmations. | Owner-approved direction after the `WB-2026-08-25-shared-analysis-surface` closeout experience. This entry records the decision so it is not lost; it is not yet a normative framework rule. Revisit in a dedicated framework Work Block to define exact authority tiers, update write/Owner gates and runtime guidance, and verify that simplification does not weaken safety or assurance. |
