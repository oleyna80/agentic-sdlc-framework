#!/usr/bin/env python3
from pathlib import Path

path = Path("scripts/wb008-seventh-review-fix.py")
text = path.read_text(encoding="utf-8")
old = '''        expect_failure(
            "historical-closeout-blocked-review",
            root,
            "review verdict=READY",
        )

'''
new = '''        expect_failure(
            "historical-closeout-blocked-review",
            root,
            "review verdict=READY",
        )
        (root / OLDER_CLOSEOUT).unlink()

'''
if old not in text:
    raise RuntimeError("historical fixture cleanup anchor missing")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
