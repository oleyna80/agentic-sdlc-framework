#!/usr/bin/env python3
from pathlib import Path

OLD_IMPL = "770d2c4d0cb1805fc111160ed1440182f151e272"
NEW_IMPL = "f711781a3a4eae95657813ee81738c29fee54ff1"
OLD_RESTORED = "7d05b855e03701e15dce6dd522aec050dda10753"
NEW_RESTORED = "9657b92634463c6fe316ead3909615ff9763621c"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing evidence anchor: {label}")
    return text.replace(old, new, 1)


def replace_all(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing evidence value: {label}")
    return text.replace(old, new)


work_block_path = Path("docs/plans/wb-008-post-merge-ssot-release-gate.md")
work_block = work_block_path.read_text(encoding="utf-8")
work_block = replace_once(work_block, "resolved eight Codex Review rounds", "resolved nine Codex Review rounds", "work-block review count")
work_block = replace_once(
    work_block,
    "15. Asterisk and underscore Markdown emphasis is normalized before semantic state\n    matching, so italic, bold, combined emphasis, and decorated table cells cannot\n    bypass mutable-state detection.\n16. Every existing closeout report bound to a completed Work Block ID retains exact\n",
    "15. Syntax-dependent raw VCS patterns run on the original closeout text before\n    Markdown normalization, preserving forms such as `**Merge status:** open` and\n    `merged_at`.\n16. Asterisk and underscore Markdown emphasis is normalized before semantic state\n    matching, so italic, bold, combined emphasis, and decorated table cells cannot\n    bypass mutable-state detection.\n17. Every existing closeout report bound to a completed Work Block ID retains exact\n",
    "work-block two-phase invariant",
)
work_block = replace_once(work_block, "17. Release-state evidence", "18. Release-state evidence", "work-block invariant renumber")
work_block = replace_all(work_block, OLD_IMPL, NEW_IMPL, "work-block implementation")
work_block = replace_all(work_block, OLD_RESTORED, NEW_RESTORED, "work-block restored head")
work_block = replace_all(work_block, "run 153", "run 168", "work-block release run")
work_block = replace_all(work_block, "run 602", "run 617", "work-block framework run")
work_block = replace_once(
    work_block,
    "- [x] Italic, bold, combined, underscore, and table Markdown state forms have regressions.\n",
    "- [x] Raw `Merge status` and `merged_at` forms have dedicated regressions.\n- [x] Italic, bold, combined, underscore, and table Markdown state forms have regressions.\n",
    "work-block raw acceptance",
)
work_block_path.write_text(work_block, encoding="utf-8")

review_path = Path("docs/reports/reviews/pr-8-final-review.md")
review = review_path.read_text(encoding="utf-8")
review = replace_all(review, OLD_IMPL, NEW_IMPL, "review implementation")
review = replace_all(review, OLD_RESTORED, NEW_RESTORED, "review restored head")
review = replace_once(review, "all eight Codex Review rounds", "all nine Codex Review rounds", "review scope count")
review = replace_once(
    review,
    "Eight Codex Review rounds produced fourteen P1 findings and four P2 findings. All\n",
    "Nine Codex Review rounds produced fourteen P1 findings and five P2 findings. All\n",
    "review convergence count",
)
ninth_section = '''### Ninth review finding

#### F-022 — Markdown normalization disabled raw syntax-dependent VCS checks

**Severity:** P2  
**Resolution:** fixed

The eighth-round normalization ran before every mutable-state regex. That removed the
asterisks required by the raw `**Merge status:**` pattern and removed the underscore
from `merged_at`, allowing both hosting-state forms to bypass detection.

Resolution:

- raw syntax-dependent patterns run against the original complete closeout text;
- semantic PR/pull-request state patterns run separately against the Markdown-
  normalized copy;
- exact adversarial fixtures reject `- **Merge status:** open` and a `merged_at`
  timestamp;
- all earlier italic, bold, combined-emphasis, underscore, table, and clean non-state
  fixtures remain green.

'''
review = replace_once(review, "## Contract Review\n", ninth_section + "## Contract Review\n", "review ninth finding")
review = replace_once(
    review,
    "- mutable hosting-platform assertions are rejected across prose, parsed frontmatter,\n  VCS-parent descendants, boundary-marker payloads, and Markdown forms normalized\n  before semantic state matching;\n",
    "- syntax-dependent raw forms are checked on original text before normalization;\n- mutable hosting-platform assertions are rejected across prose, parsed frontmatter,\n  VCS-parent descendants, boundary-marker payloads, and Markdown forms normalized\n  before semantic state matching;\n",
    "review boundary two-phase",
)
review = replace_once(
    review,
    "- italic, bold, combined asterisk, underscore, and combined-underscore state values;\n",
    "- raw `**Merge status:** open` and `merged_at` hosting-state forms;\n- italic, bold, combined asterisk, underscore, and combined-underscore state values;\n",
    "review regression raw forms",
)
review = replace_all(review, "run **153**", "run **168**", "review release run")
review = replace_all(review, "run **602**", "run **617**", "review framework run")
review = replace_once(
    review,
    "- Markdown emphasis normalization intentionally removes asterisk and underscore\n  decoration before VCS-state matching; it is a governance parser, not a complete\n  CommonMark renderer.\n",
    "- Raw syntax-dependent checks run before Markdown normalization; the normalized\n  semantic pass remains a governance parser, not a complete CommonMark renderer.\n",
    "review residual two-phase",
)
review = replace_once(review, "resolve the eighth-round", "resolve the ninth-round", "review recommendation round")
review_path.write_text(review, encoding="utf-8")

drift_path = Path("docs/reports/drift/wb-008-post-merge-ssot-release-gate.md")
drift = drift_path.read_text(encoding="utf-8")
drift = replace_all(drift, OLD_IMPL, NEW_IMPL, "drift implementation")
drift = replace_all(drift, OLD_RESTORED, NEW_RESTORED, "drift restored head")
drift = replace_once(drift, "and eight Codex Review correction rounds", "and nine Codex Review correction rounds", "drift count")
drift = replace_once(
    drift,
    "  ↔ prose, structured, parent-context, boundary-marker, Markdown-normalized, and table detection\n",
    "  ↔ raw syntax, prose, structured, parent-context, boundary-marker, Markdown-normalized, and table detection\n",
    "drift baseline raw scan",
)
drift = replace_once(
    drift,
    "| Markdown forms | all asterisk/underscore emphasis normalized before state matching | italic, bold, combined, underscore, table, and non-state positive fixtures | ALIGNED |\n",
    "| Raw VCS syntax | syntax-dependent patterns run before normalization | `Merge status` and `merged_at` regressions | ALIGNED |\n| Markdown forms | all asterisk/underscore emphasis normalized before semantic state matching | italic, bold, combined, underscore, table, and non-state positive fixtures | ALIGNED |\n",
    "drift raw matrix",
)
drift = replace_all(drift, "runs 153 and 602", "runs 168 and 617", "drift CI runs")
drift = replace_once(drift, "All eight review rounds", "All nine review rounds", "drift convergence count")
drift = replace_once(
    drift,
    "8. normalization of italic, bold, combined, and underscore Markdown emphasis before\n   semantic state matching.\n",
    "8. normalization of italic, bold, combined, and underscore Markdown emphasis before\n   semantic state matching;\n9. preservation of raw syntax-dependent checks before normalization.\n",
    "drift ninth item",
)
drift = replace_once(drift, "after eighth-round regression coverage", "after ninth-round regression coverage", "drift stale test")
drift = replace_once(drift, "resolve the eighth-round", "resolve the ninth-round", "drift recommendation")
drift_path.write_text(drift, encoding="utf-8")

closeout_path = Path("docs/reports/closeout/wb-008-post-merge-ssot-release-gate.md")
closeout = closeout_path.read_text(encoding="utf-8")
closeout = replace_all(closeout, OLD_IMPL, NEW_IMPL, "closeout implementation")
closeout = replace_all(closeout, OLD_RESTORED, NEW_RESTORED, "closeout restored head")
closeout = replace_once(closeout, "eight Codex Review rounds", "nine Codex Review rounds", "closeout count")
closeout = replace_once(
    closeout,
    "- bare identifier-plus-state prose is rejected without a connector verb;\n- asterisk and underscore Markdown emphasis is normalized before mutable-state\n",
    "- bare identifier-plus-state prose is rejected without a connector verb;\n- raw syntax-dependent forms are checked before normalization, including\n  `**Merge status:** open` and `merged_at`;\n- asterisk and underscore Markdown emphasis is normalized before mutable-state\n",
    "closeout raw invariant",
)
closeout = replace_all(closeout, "run 153", "run 168", "closeout release run")
closeout = replace_all(closeout, "run 602", "run 617", "closeout framework run")
closeout = replace_once(
    closeout,
    "- [x] Italic, bold, combined, underscore, and table Markdown state forms are rejected.\n",
    "- [x] Raw `Merge status` and `merged_at` hosting-state forms are rejected.\n- [x] Italic, bold, combined, underscore, and table Markdown state forms are rejected.\n",
    "closeout raw acceptance",
)
closeout = replace_once(
    closeout,
    "- Markdown emphasis normalization removes asterisk and underscore decoration before\n  VCS-state matching; it is a governance parser rather than a complete CommonMark\n  renderer.\n",
    "- Raw syntax-dependent checks run before Markdown normalization; the normalized\n  semantic pass is a governance parser rather than a complete CommonMark renderer.\n",
    "closeout residual two-phase",
)
closeout_path.write_text(closeout, encoding="utf-8")
