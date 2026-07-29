# Ecosystem Watchlist

Optional sources discovered by the Owner. This is not an import queue and does
not override the priority catalog. Check an entry only when it matches an
approved project need or an Owner requests a refresh. For GitHub sources,
resolve the relevant default ref to a full SHA during each check. Do not run
upstream installers, configure integrations, or copy content without a
separate approved adaptation Work Block.

| Source | Type and useful scope | Suggested review | Current disposition |
| --- | --- | --- | --- |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Skill source; visual direction and frontend design. Local `taste-skill` overlaps its `skills/taste-skill/` path. | Relevant frontend/design work | Track. MIT; first reconcile local provenance and delta before calling any change an update. |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Skill collection; UI styling, design systems, brand and slides. | Relevant UI/design-system work | Track as a candidate. MIT; adapt only non-conflicting guidance because the local design library already overlaps. |
| [obra/superpowers](https://github.com/obra/superpowers) | Methodology and SDLC skill reference. | Framework/process review | Track as a reference. MIT; its plugin, hooks, installers, and autonomous workflows are never adopted by a watchlist check. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Marketing/CRO/SEO skill collection. | Marketing, ecommerce, or growth project | Track for future use. MIT; no baseline import into the core engineering framework. |
| [charlie947/social-media-skills](https://github.com/charlie947/social-media-skills) | Social-content and creative-production skill collection. | Social-media delivery project | Track for future use. MIT; select individual skills only after a content, rights, and tool review. |
| [Jakubantalik/transitions.dev](https://github.com/Jakubantalik/transitions.dev) | Motion and transition skill reference for web applications. | Motion-heavy frontend project | Watch manually. Repository metadata did not assert a reusable license; do not copy until the license is verified. |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | Persistent-context runtime integration. | Explicit memory-runtime evaluation | Watch as an integration candidate. Apache-2.0, but installation, hooks, local data, telemetry, and retention need their own security and configuration approval. |
| [upstash/context7](https://github.com/upstash/context7) | Version-aware documentation MCP/CLI integration. | Explicit documentation-tool evaluation | Watch as an integration candidate. MIT; MCP/CLI setup, credentials, and external data flow are out of scope for skill adaptation. |
| [Claude Finance plugin](https://claude.com/plugins/finance), [Legal plugin](https://claude.com/plugins/legal), [Small Business plugin](https://claude.com/plugins/small-business) | Hosted product capabilities for finance, legal, and small-business tasks. | Owner-requested product review | Manual availability/terms review only. They expose no version-pinned GitHub skill source here, so they are never copied or treated as an update source. |

The Anthropic Skills repository is intentionally absent from this table because
it is already priority source 2 in `priority-sources.md`.
