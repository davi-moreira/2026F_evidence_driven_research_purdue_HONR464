#!/usr/bin/env python3
"""
Video-Guide Blockquote Voice Check
==================================

Video lecture guides have two zones with different voice rules:

  1. Wrapper prose (instructor-facing, read silently). Phrases like "Students
     often ask…" are FINE here — the instructor is being told ABOUT the
     audience.
  2. Blockquote read-aloud scripts (lines starting with "> "). The instructor
     SPEAKS these on camera, so the listener IS a student. Inside blockquotes,
     the same rule as student notebooks applies: no third-party "students", no
     "the instructor", no "on camera", no "speaking prompt".

This script flags voice violations only inside blockquotes, leaving wrapper
prose untouched. Run it before committing any video_guides/*.md edit.

Note: video_guides/ is gitignored (instructor-only). This script lives in the
tracked repo so it persists; the files it audits do not.

Usage
-----
    python scripts/voice_check_guides.py
    python scripts/voice_check_guides.py video_guides/09_video_lecture_guide.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

VIOLATION_PATTERNS = [
    re.compile(r"\bstudents?\b", re.IGNORECASE),
    re.compile(r"\bthe instructor\b", re.IGNORECASE),
    re.compile(r"\bon camera\b", re.IGNORECASE),
    re.compile(r"\bspeaking prompt\b", re.IGNORECASE),
]

# False positive — Student's t (the statistical test) is allowed, including
# markdown italics around the t (e.g., "Student's *t*").
WHITELIST = re.compile(r"Student'?s \*?t\*?", re.IGNORECASE)


def audit_file(path: Path) -> list[tuple[int, str]]:
    hits: list[tuple[int, str]] = []
    for lineno, raw in enumerate(path.read_text().splitlines(), start=1):
        stripped = raw.lstrip()
        if not stripped.startswith(">"):
            continue
        if WHITELIST.search(raw):
            continue
        for pat in VIOLATION_PATTERNS:
            if pat.search(raw):
                hits.append((lineno, raw.rstrip()))
                break
    return hits


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent

    if len(argv) > 1:
        targets = [Path(p) for p in argv[1:]]
    else:
        guides_dir = repo_root / "video_guides"
        if not guides_dir.is_dir():
            print(
                f"NOTE: {guides_dir} not found (it is gitignored — local only). "
                "Pass a path to audit a specific guide.",
                file=sys.stderr,
            )
            return 0
        targets = sorted(guides_dir.glob("*.md"))

    if not targets:
        print("No guide files to audit.")
        return 0

    any_hits = False
    for path in targets:
        if not path.is_file():
            print(f"SKIP: {path} (not found)", file=sys.stderr)
            continue
        hits = audit_file(path)
        if not hits:
            continue
        any_hits = True
        print(f"{path}: {len(hits)} blockquote violations")
        for lineno, line in hits:
            print(f"  line {lineno}: {line}")

    if not any_hits:
        print("Clean — no blockquote voice violations.")
        return 0

    print()
    print("Fix in place: rewrite each blockquote line in second person ('you'),")
    print("neutral imperative, or first person — and verify with this script again.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
