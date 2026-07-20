#!/usr/bin/env python3
"""
Session-Guide Voice + Date Check
================================

Session guides (session_guides/NN_session_guide.md, gitignored) have two zones
with different voice rules:

  1. Wrapper prose (instructor-facing, read silently). Phrases like "Students
     often ask…" are FINE here — the instructor is being told ABOUT the
     audience.
  2. Blockquote read-aloud scripts (lines starting with "> "). The instructor
     SPEAKS these, so the listener IS a student. Inside blockquotes, the same
     rule as student notebooks applies: no third-party "students", no "the
     instructor", no "on camera", no "speaking prompt".

Additionally (D13, 2026-07-20), guides carry NO calendar dates and NO
"Meeting M#" references anywhere — position is expressed only as lecture
labels ("Lecture i of N", "Studio Friday", "Async module"). This applies to
every line, not just blockquotes.

Usage
-----
    python scripts/voice_check_guides.py
    python scripts/voice_check_guides.py session_guides/09_session_guide.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BLOCKQUOTE_PATTERNS = [
    re.compile(r"\bstudents?\b", re.IGNORECASE),
    re.compile(r"\bthe instructor\b", re.IGNORECASE),
    re.compile(r"\bon camera\b", re.IGNORECASE),
    re.compile(r"\bspeaking prompt\b", re.IGNORECASE),
]

# D13 — no dates, no meeting numbers, anywhere in a guide.
EVERYWHERE_PATTERNS = [
    (re.compile(r"\bMeeting M\d+\b"), 'meeting reference (use "Lecture i of N")'),
    (re.compile(r"\b(19|20)\d\d-\d\d-\d\d\b"), "calendar date"),
    (re.compile(r"\b(January|February|March|April|June|July|August|September|"
                r"October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept?|"
                r"Oct|Nov|Dec)\.?\s+\d{1,2}\b"), "calendar date"),
]

# False positive — Student's t (the statistical test) is allowed, including
# markdown italics around the t (e.g., "Student's *t*").
WHITELIST = re.compile(r"Student'?s \*?t\*?", re.IGNORECASE)


def audit_file(path: Path) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []
    for lineno, raw in enumerate(path.read_text().splitlines(), start=1):
        for pat, label in EVERYWHERE_PATTERNS:
            if pat.search(raw):
                hits.append((lineno, label, raw.rstrip()))
                break
        stripped = raw.lstrip()
        if not stripped.startswith(">"):
            continue
        if WHITELIST.search(raw):
            continue
        for pat in BLOCKQUOTE_PATTERNS:
            if pat.search(raw):
                hits.append((lineno, "blockquote voice", raw.rstrip()))
                break
    return hits


def main(argv: list[str]) -> int:
    repo_root = Path(__file__).resolve().parent.parent

    if len(argv) > 1:
        targets = [Path(p) for p in argv[1:]]
    else:
        guides_dir = repo_root / "session_guides"
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
        print(f"{path}: {len(hits)} violation(s)")
        for lineno, label, line in hits:
            print(f"  line {lineno} [{label}]: {line}")

    if not any_hits:
        print(f"Clean — no voice/date violations across {len(targets)} guide(s).")
        return 0

    print()
    print("Fix in place: rewrite blockquote lines in second person ('you'); replace")
    print("dates and meeting numbers with lecture labels — then run this again.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
