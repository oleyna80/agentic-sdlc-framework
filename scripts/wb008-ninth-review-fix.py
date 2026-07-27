#!/usr/bin/env python3
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing patch anchor: {label}")
    return text.replace(old, new, 1)


validator_path = Path("scripts/validate-release-state.py")
tests_path = Path("scripts/test-release-state-contracts.py")
governance_path = Path("governance/release-state.md")

validator = validator_path.read_text(encoding="utf-8")
old_patterns = '''MUTABLE_CLOSEOUT_PATTERNS = (
    re.compile(r"^\\s*[-*]?\\s*\\*\\*Merge status:\\*\\*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\\bnot merged\\b", re.IGNORECASE),
    re.compile(r"\\bmerge commit\\b", re.IGNORECASE),
    re.compile(r"\\bmerged_at\\b", re.IGNORECASE),
    re.compile(
        rf"\\b(?:PR|pull[ -]?request)\\s*(?:#\\s*\\d+)?\\s*"
        rf"(?:(?::|=)\\s*|(?:is|was|remains?|became|has\\s+been)\\s*|"
        rf"(?:status|state)\\s*(?:is|=|:)\\s*){NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\\b(?:PR|pull[ -]?request)\\s*(?:#\\s*\\d+)?\\s+"
        rf"{NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\\*\\*(?:PR|pull[ -]?request)\\s*(?:#\\s*\\d+)?\\s*:\\*\\*\\s*"
        rf"{NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\\*\\*(?:PR|pull[ -]?request)\\s+(?:status|state):\\*\\*\\s*"
        rf"{NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"^\\s*\\|\\s*(?:\\*\\*)?(?:PR|pull[ -]?request)\\s*(?:#\\s*\\d+)?"
        rf"(?:\\*\\*)?\\s*\\|\\s*{NORMALIZED_MUTABLE_VCS_STATE}\\s*\\|",
        re.IGNORECASE | re.MULTILINE,
    ),
)
'''
new_patterns = '''RAW_MUTABLE_CLOSEOUT_PATTERNS = (
    re.compile(r"^\\s*[-*]?\\s*\\*\\*Merge status:\\*\\*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\\bnot merged\\b", re.IGNORECASE),
    re.compile(r"\\bmerge commit\\b", re.IGNORECASE),
    re.compile(r"\\bmerged_at\\b", re.IGNORECASE),
)
NORMALIZED_MUTABLE_CLOSEOUT_PATTERNS = (
    re.compile(
        rf"\\b(?:PR|pull[ -]?request)\\s*(?:#\\s*\\d+)?\\s*"
        rf"(?:(?::|=)\\s*|(?:is|was|remains?|became|has\\s+been)\\s*|"
        rf"(?:status|state)\\s*(?:is|=|:)\\s*){NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\\b(?:PR|pull[ -]?request)\\s*(?:#\\s*\\d+)?\\s+"
        rf"{NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\\*\\*(?:PR|pull[ -]?request)\\s*(?:#\\s*\\d+)?\\s*:\\*\\*\\s*"
        rf"{NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"\\*\\*(?:PR|pull[ -]?request)\\s+(?:status|state):\\*\\*\\s*"
        rf"{NORMALIZED_MUTABLE_VCS_STATE}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"^\\s*\\|\\s*(?:\\*\\*)?(?:PR|pull[ -]?request)\\s*(?:#\\s*\\d+)?"
        rf"(?:\\*\\*)?\\s*\\|\\s*{NORMALIZED_MUTABLE_VCS_STATE}\\s*\\|",
        re.IGNORECASE | re.MULTILINE,
    ),
)
'''
validator = replace_once(validator, old_patterns, new_patterns, "split raw and normalized patterns")
old_reject = '''    if structured is not None:
        reject_structured_vcs_claims(structured, label)
    normalized_text = normalize_markdown_decoration(text)
    for pattern in MUTABLE_CLOSEOUT_PATTERNS:
        if pattern.search(normalized_text):
            raise ReleaseStateError(f"{label} contains mutable GitHub/VCS state: {pattern.pattern}")
'''
new_reject = '''    if structured is not None:
        reject_structured_vcs_claims(structured, label)
    for pattern in RAW_MUTABLE_CLOSEOUT_PATTERNS:
        if pattern.search(text):
            raise ReleaseStateError(f"{label} contains mutable GitHub/VCS state: {pattern.pattern}")
    normalized_text = normalize_markdown_decoration(text)
    for pattern in NORMALIZED_MUTABLE_CLOSEOUT_PATTERNS:
        if pattern.search(normalized_text):
            raise ReleaseStateError(f"{label} contains mutable GitHub/VCS state: {pattern.pattern}")
'''
validator = replace_once(validator, old_reject, new_reject, "two-phase VCS scan")
validator_path.write_text(validator, encoding="utf-8")

tests = tests_path.read_text(encoding="utf-8")
test_anchor = '''        for label, assertion in (
            ("mutable-pr-open", "PR #9 is open."),
'''
test_replacement = '''        for label, assertion in (
            ("mutable-merge-status-open", "- **Merge status:** open"),
            ("mutable-merged-at", "merged_at: 2026-07-27T19:45:39Z"),
            ("mutable-pr-open", "PR #9 is open."),
'''
tests = replace_once(tests, test_anchor, test_replacement, "raw-pattern regressions")
tests_path.write_text(tests, encoding="utf-8")

governance = governance_path.read_text(encoding="utf-8")
governance_anchor = '''The mutable-state scan covers the entire closeout document, including parsed YAML
frontmatter and Markdown body. It rejects:
'''
governance_replacement = '''The mutable-state scan covers the entire closeout document, including parsed YAML
frontmatter and Markdown body. Syntax-dependent raw patterns run against the original
document before asterisk/underscore normalization; semantic state patterns then run
against the normalized copy. It rejects:
'''
governance = replace_once(
    governance, governance_anchor, governance_replacement, "raw-before-normalized contract"
)
bullet_anchor = '''- Markdown-emphasized forms after normalizing asterisk and underscore decoration,
  including italic, bold, and combined emphasis around mutable state tokens;
- Markdown table rows that pair a pull-request identifier with a mutable state;
- merge timestamps, merge commit state, or equivalent hosting-platform facts.
'''
bullet_replacement = '''- raw syntax-dependent forms such as `**Merge status:** open` and keys such as
  `merged_at` before Markdown normalization can erase their syntax;
- Markdown-emphasized forms after normalizing asterisk and underscore decoration,
  including italic, bold, and combined emphasis around mutable state tokens;
- Markdown table rows that pair a pull-request identifier with a mutable state;
- merge timestamps, merge commit state, or equivalent hosting-platform facts.
'''
governance = replace_once(governance, bullet_anchor, bullet_replacement, "raw-pattern examples")
governance_path.write_text(governance, encoding="utf-8")
