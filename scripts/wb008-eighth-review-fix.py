#!/usr/bin/env python3
from pathlib import Path
import re


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing patch anchor: {label}")
    return text.replace(old, new, 1)


validator_path = Path("scripts/validate-release-state.py")
tests_path = Path("scripts/test-release-state-contracts.py")
governance_path = Path("governance/release-state.md")

validator = validator_path.read_text(encoding="utf-8")
validator, count = re.subn(
    r'^MARKDOWN_MUTABLE_VCS_STATE = .+$',
    'MARKDOWN_DECORATION_RE = re.compile(r"[*_]+")\n'
    'NORMALIZED_MUTABLE_VCS_STATE = rf"{MUTABLE_VCS_STATES}\\b"',
    validator,
    count=1,
    flags=re.MULTILINE,
)
if count != 1:
    raise RuntimeError("missing patch anchor: Markdown mutable-state fragment")
if "MARKDOWN_MUTABLE_VCS_STATE" not in validator:
    raise RuntimeError("missing patch anchor: Markdown mutable-state uses")
validator = validator.replace(
    "MARKDOWN_MUTABLE_VCS_STATE", "NORMALIZED_MUTABLE_VCS_STATE"
)

old_reject = '''def reject_mutable_vcs_claims(
    text: str, label: str, structured: object | None = None
) -> None:
    if structured is not None:
        reject_structured_vcs_claims(structured, label)
    for pattern in MUTABLE_CLOSEOUT_PATTERNS:
        if pattern.search(text):
            raise ReleaseStateError(f"{label} contains mutable GitHub/VCS state: {pattern.pattern}")
'''
new_reject = '''def normalize_markdown_decoration(text: str) -> str:
    """Remove Markdown emphasis markers before semantic VCS-state matching."""
    return MARKDOWN_DECORATION_RE.sub("", text)


def reject_mutable_vcs_claims(
    text: str, label: str, structured: object | None = None
) -> None:
    if structured is not None:
        reject_structured_vcs_claims(structured, label)
    normalized_text = normalize_markdown_decoration(text)
    for pattern in MUTABLE_CLOSEOUT_PATTERNS:
        if pattern.search(normalized_text):
            raise ReleaseStateError(f"{label} contains mutable GitHub/VCS state: {pattern.pattern}")
'''
validator = replace_once(
    validator, old_reject, new_reject, "Markdown normalization before VCS scan"
)
validator_path.write_text(validator, encoding="utf-8")

tests = tests_path.read_text(encoding="utf-8")
positive_anchor = '''    with tempfile.TemporaryDirectory(prefix="release-state-pr-reference-") as temp:
        root = Path(temp)
        populate(root)
        write(
            root / CLOSEOUT,
            closeout("\\nPR #9 review evidence is repository-owned.\\n"),
        )
        assert validator.validate_repository(root)["verdict"] == "READY"
'''
positive_replacement = positive_anchor + '''
    with tempfile.TemporaryDirectory(prefix="release-state-markdown-non-state-") as temp:
        root = Path(temp)
        populate(root)
        write(
            root / CLOSEOUT,
            closeout("\\nPR #9: *review evidence* is repository-owned.\\n"),
        )
        assert validator.validate_repository(root)["verdict"] == "READY"
'''
tests = replace_once(
    tests, positive_anchor, positive_replacement, "Markdown non-state positive fixture"
)
negative_anchor = '''            ("mutable-pr-bold-state", "**PR #9:** **merged**"),
            ("mutable-pr-table-bold-state", "| **PR #9** | **open** |"),
'''
negative_replacement = '''            ("mutable-pr-bold-state", "**PR #9:** **merged**"),
            ("mutable-pr-italic-state", "PR #9: *merged*"),
            ("mutable-pr-combined-state", "**PR #9:** ***merged***"),
            ("mutable-pr-underscore-state", "PR #9: _open_"),
            ("mutable-pull-request-combined-underscore", "Pull request #9: ___closed___"),
            ("mutable-pr-table-bold-state", "| **PR #9** | **open** |"),
'''
tests = replace_once(
    tests, negative_anchor, negative_replacement, "Markdown emphasis adversarial fixtures"
)
tests_path.write_text(tests, encoding="utf-8")

governance = governance_path.read_text(encoding="utf-8")
governance = replace_once(
    governance,
    "- bold Markdown forms such as a pull-request identifier followed by a state;\n",
    "- Markdown-emphasized forms after normalizing asterisk and underscore decoration,\n  including italic, bold, and combined emphasis around mutable state tokens;\n",
    "governance Markdown normalization rule",
)
governance = replace_once(
    governance,
    "  descendants, boundary-marker payloads, and common Markdown forms.\n",
    "  descendants, boundary-marker payloads, and Markdown forms normalized before\n  semantic state matching.\n",
    "governance fail-closed Markdown rule",
)
governance_path.write_text(governance, encoding="utf-8")

print("Applied eighth-review Markdown normalization patch")
