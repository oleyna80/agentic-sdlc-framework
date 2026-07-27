#!/usr/bin/env python3
from pathlib import Path

path = Path("docs/reports/closeout/wb-008-post-merge-ssot-release-gate.md")
text = path.read_text(encoding="utf-8")
old_invariant = (
    "- raw syntax-dependent forms are checked before normalization, including\n"
    "  `**Merge status:** open` and `merged_at`;\n"
)
new_invariant = (
    "- raw syntax-dependent merge-status markers and merge-timestamp keys are checked\n"
    "  before Markdown normalization;\n"
)
old_acceptance = (
    "- [x] Raw `Merge status` and `merged_at` hosting-state forms are rejected.\n"
)
new_acceptance = (
    "- [x] Raw merge-status markers and merge-timestamp keys are rejected.\n"
)
if old_invariant not in text or old_acceptance not in text:
    raise RuntimeError("generated closeout sanitizer anchors are missing")
text = text.replace(old_invariant, new_invariant, 1)
text = text.replace(old_acceptance, new_acceptance, 1)
path.write_text(text, encoding="utf-8")
