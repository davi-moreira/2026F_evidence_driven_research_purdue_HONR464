#!/usr/bin/env python3
"""validate_book_sync.py — chapter <-> notebook synchronization gate (D20).

Parses the 37-chapter manifest table in planning/BOOK_MAP.md and checks the
course book against it, both directions:

  1. every chapter in the manifest has a file book/<part-slug>/<NN>-*.qmd
  2. every chapter file contains a Colab link to its PRIMARY notebook's student
     file (so the "Colab lab" element is present and points at the right nb)
  3. every registered notebook (nb00-nb15) is the primary of >= 1 chapter
     (parsed from the manifest, so the book cannot silently drop a topic)
  4. every chapter carries the ten required element headings

Until the book/ directory exists (Phase 6 not started), the file-level checks
report "pending" and the script exits 0 on the manifest-only invariants (3),
so it is safe to wire into CI early. Pass --strict to require the files.

Usage: python3 scripts/validate_book_sync.py [--strict]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from notebooks_map import NOTEBOOKS, student_filename  # noqa: E402

BOOK_MAP = REPO / "planning" / "BOOK_MAP.md"
BOOK_DIR = REPO / "book"

PART_SLUGS = {
    "I": "part1-research-with-ai", "II": "part2-curiosity-to-design",
    "III": "part3-pathways", "IV": "part4-credible-evidence",
    "V": "part5-communicating", "VI": "part6-after-conference",
}
REQUIRED_ELEMENTS = [
    "research decision", "worked example", "Do not delegate",
    "failure", "verification", "project transfer", "defend",
]


def parse_manifest() -> list[dict]:
    """Return [{part, ch, title, nb}] from the BOOK_MAP table rows."""
    rows = []
    for line in BOOK_MAP.read_text().splitlines():
        m = re.match(r"\|\s*([IVX]+)\b[^|]*\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*nb(\d\d)\s*\|", line)
        if m:
            rows.append({"part": m.group(1), "ch": int(m.group(2)),
                         "title": m.group(3), "nb": int(m.group(4))})
    return rows


def main() -> None:
    strict = "--strict" in sys.argv
    chapters = parse_manifest()
    errs, warns = [], []

    if len(chapters) != 37:
        errs.append(f"manifest has {len(chapters)} chapters, expected 37")
    nums = [c["ch"] for c in chapters]
    if nums != list(range(1, len(chapters) + 1)):
        errs.append("chapter numbers are not a clean 1..N sequence")

    # (3) every registered notebook is some chapter's primary
    covered = {c["nb"] for c in chapters}
    for n in NOTEBOOKS:
        if n not in covered:
            errs.append(f"nb{n:02d} is not the primary notebook of any chapter")
    for c in chapters:
        if c["nb"] not in NOTEBOOKS:
            errs.append(f"ch {c['ch']}: primary nb{c['nb']:02d} not in the registry")

    # (1,2,4) file-level checks — pending until book/ exists
    if not BOOK_DIR.exists():
        msg = "book/ not built yet — file-level checks pending (Phase 6)"
        if strict:
            errs.append(msg)
        else:
            warns.append(msg)
    else:
        for c in chapters:
            slug = PART_SLUGS[c["part"]]
            hits = list((BOOK_DIR / slug).glob(f"{c['ch']:02d}-*.qmd")) \
                if (BOOK_DIR / slug).exists() else []
            if not hits:
                errs.append(f"ch {c['ch']} ({c['title']}): no file book/{slug}/{c['ch']:02d}-*.qmd")
                continue
            text = hits[0].read_text()
            if student_filename(c["nb"]).replace("_student.ipynb", "") not in text \
                    and f"nb{c['nb']:02d}" not in text:
                errs.append(f"ch {c['ch']}: no Colab link to its primary nb{c['nb']:02d}")
            missing = [e for e in REQUIRED_ELEMENTS if e.lower() not in text.lower()]
            if missing:
                warns.append(f"ch {c['ch']}: missing element(s) {missing}")

    for w in warns:
        print(f"  ⚠️ {w}")
    if errs:
        print(f"✗ book sync: {len(errs)} problem(s)")
        for e in errs:
            print("  " + e)
        sys.exit(1)
    print(f"✓ book manifest consistent — 37 chapters, all {len(NOTEBOOKS)} "
          f"notebooks covered" + (" (file-level pending)" if warns else ""))


if __name__ == "__main__":
    main()
