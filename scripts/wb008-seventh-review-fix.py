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
token_anchor = (
    'MUTABLE_VCS_STATE_TOKEN_RE = '
    're.compile(rf"\\b{MUTABLE_VCS_STATES}\\b", re.IGNORECASE)\n'
)
validator = replace_once(
    validator,
    token_anchor,
    token_anchor
    + 'MARKDOWN_MUTABLE_VCS_STATE = '
    + 'rf"(?:\\*\\*)?{MUTABLE_VCS_STATES}\\b(?:\\*\\*)?"\n',
    "markdown state token",
)

pattern_start = validator.index("MUTABLE_CLOSEOUT_PATTERNS = (")
pattern_end = validator.index("STALE_MAP_PATTERNS = (")
region = validator[pattern_start:pattern_end]
if region.count("{MUTABLE_VCS_STATES}\\b") != 4:
    raise RuntimeError("unexpected prose-state pattern count")
region = region.replace(
    "{MUTABLE_VCS_STATES}\\b", "{MARKDOWN_MUTABLE_VCS_STATE}"
)
table_state = "{MUTABLE_VCS_STATES}\\s*\\|"
if table_state not in region:
    raise RuntimeError("missing Markdown table state pattern")
region = region.replace(
    table_state, "{MARKDOWN_MUTABLE_VCS_STATE}\\s*\\|", 1
)
validator = validator[:pattern_start] + region + validator[pattern_end:]

historical_function = r'''

def validate_completed_closeout_reports(
    root: Path, completed_records: dict[str, dict[str, Any]]
) -> None:
    reports_root = root / "docs/reports/closeout"
    if not reports_root.is_dir():
        return

    completed_by_id = {
        str(record["frontmatter"]["work_block_id"]): record
        for record in completed_records.values()
    }
    seen: dict[str, str] = {}

    for path in sorted(reports_root.rglob("*.md")):
        try:
            raw = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ReleaseStateError(
                f"cannot read closeout report {path}: {exc}"
            ) from exc
        if not raw.startswith("---\n"):
            continue

        relative = path.relative_to(root).as_posix()
        label = f"completed Work Block closeout {relative}"
        frontmatter, body, _ = parse_frontmatter(path, label)
        if frontmatter.get("artifact_type") != "closeout_report":
            continue

        work_block_id = frontmatter.get("work_block_id")
        if work_block_id not in completed_by_id:
            continue
        if work_block_id in seen:
            raise ReleaseStateError(
                f"completed Work Block {work_block_id} has multiple closeout reports: "
                f"{seen[work_block_id]} and {relative}"
            )
        seen[str(work_block_id)] = relative

        if frontmatter.get("status") != "approved":
            raise ReleaseStateError(f"{label} must be approved")

        markers = parse_markers(body, label)
        required_exact = {
            "stage execution state": "completed",
            "review verdict": "READY",
            "verification verdict": "READY",
            "drift verdict": "ALIGNED",
            "closeout classification": "SUCCESS",
            "task status": "completed",
        }
        for key, expected in required_exact.items():
            actual = markers.get(key)
            if actual != expected:
                raise ReleaseStateError(
                    f"{label} requires {key}={expected}, found {actual!r}"
                )

        work_block_evaluation = completed_by_id[str(work_block_id)][
            "markers"
        ].get("evaluation verdict")
        closeout_evaluation = markers.get("evaluation verdict")
        if work_block_evaluation is not None:
            expected_evaluation = evaluation_verdict(
                work_block_evaluation,
                f"completed Work Block {work_block_id} evaluation verdict",
            )
            if closeout_evaluation is None:
                raise ReleaseStateError(
                    f"{label} requires evaluation verdict={expected_evaluation}"
                )
            actual_evaluation = evaluation_verdict(
                closeout_evaluation, f"{label} evaluation verdict"
            )
            if actual_evaluation != expected_evaluation:
                raise ReleaseStateError(
                    f"{label} requires evaluation verdict={expected_evaluation}, "
                    f"found {actual_evaluation!r}"
                )
        elif closeout_evaluation is not None:
            evaluation_verdict(
                closeout_evaluation, f"{label} evaluation verdict"
            )

        validate_external_vcs_boundary(markers.get("external vcs state", ""))
        extract_single_section(
            body, "Residual Risks and Limitations", label
        )
        extract_single_section(body, "Follow-Up Work", label)
'''
validator = replace_once(
    validator,
    "\n\ndef validate_closeout(\n",
    historical_function + "\n\ndef validate_closeout(\n",
    "historical closeout validator",
)
validator = replace_once(
    validator,
    "    validate_release_assets(root, release_state)\n"
    "    validate_closeout(root, release_state, completed, completed_records)\n",
    "    validate_release_assets(root, release_state)\n"
    "    validate_completed_closeout_reports(root, completed_records)\n"
    "    validate_closeout(root, release_state, completed, completed_records)\n",
    "historical closeout invocation",
)
validator_path.write_text(validator, encoding="utf-8")

tests = tests_path.read_text(encoding="utf-8")
closeout_constant = (
    'CLOSEOUT = '
    '"docs/reports/closeout/wb-007-agent-evaluation-trajectory-assurance.md"\n'
)
tests = replace_once(
    tests,
    closeout_constant,
    closeout_constant
    + 'OLDER_CLOSEOUT = '
    + '"docs/reports/closeout/wb-006-bootstrap-restore-hardening.md"\n',
    "older closeout constant",
)
positive_anchor = (
    '    with tempfile.TemporaryDirectory('
    'prefix="release-state-skipped-") as temp:\n'
)
positive_fixture = '''    with tempfile.TemporaryDirectory(prefix="release-state-historical-closeout-") as temp:
        root = Path(temp)
        completed = [OLDER, COMPLETED]
        populate(root, registry(completed), project_map(completed))
        write(root / OLDER, work_block("wb-006", "completed", evaluation=None))
        write(root / OLDER_CLOSEOUT, closeout(work_block_id="wb-006", evaluation=None))
        assert validator.validate_repository(root)["verdict"] == "READY"

'''
tests = replace_once(
    tests,
    positive_anchor,
    positive_fixture + positive_anchor,
    "positive historical closeout fixture",
)
bold_anchor = (
    '            ("mutable-pr-bold-colon", '
    '"**PR #9:** merged"),\n'
)
tests = replace_once(
    tests,
    bold_anchor,
    bold_anchor
    + '            ("mutable-pr-bold-state", '
    + '"**PR #9:** **merged**"),\n'
    + '            ("mutable-pr-table-bold-state", '
    + '"| **PR #9** | **open** |"),\n',
    "bold state fixtures",
)
negative_anchor = (
    '        populate(root)\n'
    '        write(root / CLOSEOUT, closeout(include_residual=False))\n'
)
negative_fixture = '''        populate(root, registry([OLDER, COMPLETED]), project_map([OLDER, COMPLETED]))
        write(root / OLDER, work_block("wb-006", "completed", evaluation=None))
        write(
            root / OLDER_CLOSEOUT,
            closeout(work_block_id="wb-006", evaluation=None, review="BLOCKED"),
        )
        expect_failure(
            "historical-closeout-blocked-review",
            root,
            "review verdict=READY",
        )

'''
tests = replace_once(
    tests,
    negative_anchor,
    negative_fixture + negative_anchor,
    "adversarial historical closeout fixture",
)
tests_path.write_text(tests, encoding="utf-8")

governance = governance_path.read_text(encoding="utf-8")
governance = replace_once(
    governance,
    "- bold Markdown forms such as a pull-request identifier followed by a state;\n",
    "- bold Markdown forms such as a pull-request identifier followed by a state, "
    "including Markdown decoration around the state token itself;\n",
    "Markdown state governance",
)
boundary_anchor = (
    "A clean non-normative ownership statement remains permitted; a concrete mutable\n"
    "state assertion does not, including when appended to the boundary marker itself.\n"
)
governance = replace_once(
    governance,
    boundary_anchor,
    boundary_anchor
    + "\nEvery existing `closeout_report` under `docs/reports/closeout/` that binds to a\n"
    + "completed Work Block ID must retain approved status, exact successful lifecycle\n"
    + "markers, matching evaluation semantics, a non-normative external-state boundary,\n"
    + "and the required residual-risk and follow-up sections. Historical closeout drift\n"
    + "fails closed even when the latest closeout remains valid.\n",
    "historical closeout governance",
)
governance = replace_once(
    governance,
    "- normative mutable GitHub-state claims anywhere in closeout evidence, including\n"
    "  structured frontmatter, VCS parent-key descendants, boundary-marker payloads,\n"
    "  and common Markdown forms.\n",
    "- normative mutable GitHub-state claims anywhere in the current canonical closeout,\n"
    "  including structured frontmatter, VCS parent-key descendants, boundary-marker\n"
    "  payloads, and common Markdown forms;\n"
    "- adverse or contradictory lifecycle evidence in any existing closeout report bound\n"
    "  to a completed Work Block ID.\n",
    "historical fail-closed governance",
)
governance_path.write_text(governance, encoding="utf-8")
