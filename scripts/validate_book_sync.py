#!/usr/bin/env python3
"""validate_book_sync.py — chapter <-> notebook synchronization gate (D20/D25).

Reads lesson identity from planning/BOOK_ARCHITECTURE.yml through the shared
loader (round-9 N2: this gate previously parsed BOOK_MAP's display numbers
and hard-coded 37, so a valid 39-lesson architecture would have failed while
number-misbound artifacts passed) and checks the book both directions:

  1. every ACTIVE lesson has its source file and its companion notebook
     (paths from the manifest — never derived from numeric prefixes)
  2. every chapter file links its OWN companion notebook (the chapter badge)
     AND still names its PRIMARY course notebook (the crosswalk home anchor)
  3. every registered notebook (nb01-nb16) is the primary of >= 1 lesson
  4. every chapter carries the required element headings
  5. the For-instructors appendix exists in all three editions and the EN
     edition links every course lab nb01-nb16 (D25)
  6. the PT/ES chapter files link their localized companion notebooks
     (mirrored source paths while the editions are frozen, D36)
  7. NO ORPHANS: every book/part*/*.qmd and notebooks/book/*.ipynb (and
     pt/es) is claimed by the manifest — a tombstoned or renamed lesson
     cannot leave debris behind.

Usage: python3 scripts/validate_book_sync.py [--strict]
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from notebooks_map import NOTEBOOKS, student_filename  # noqa: E402
from book_manifest import (active_lessons, load_architecture,  # noqa: E402
                           primary_nb_by_lesson)

BOOK_DIR = REPO / "book"
NB_BOOK = REPO / "notebooks" / "book"

REQUIRED_ELEMENTS = [
    "research decision", "worked example", "Do not delegate",
    "failure", "It is your turn",
]


def main() -> None:
    strict = "--strict" in sys.argv          # kept for CI compatibility
    arch = load_architecture()
    lessons = active_lessons(arch)
    primary = primary_nb_by_lesson()
    errs, warns = [], []

    # (3) coverage both directions, from the crosswalk home anchors
    covered = {int(primary[l["id"]][2:]) for l in lessons if l["id"] in primary}
    for n in NOTEBOOKS:
        if n not in covered:
            errs.append(f"nb{n:02d} is not the primary notebook of any lesson")
    for l in lessons:
        if l["id"] not in primary:
            errs.append(f"{l['id']}: no home anchor in the crosswalk")

    for l in lessons:
        src = BOOK_DIR / l["source"]
        comp = NB_BOOK / l["companion"]
        if not src.exists():
            errs.append(f"{l['id']}: source missing: book/{l['source']}")
            continue
        if not comp.exists():
            errs.append(f"{l['id']}: companion missing: "
                        f"notebooks/book/{l['companion']}")
        text = src.read_text()
        nb = primary.get(l["id"], "")
        if nb and student_filename(int(nb[2:])).replace("_student.ipynb", "") \
                not in text and nb not in text:
            errs.append(f"{l['id']}: does not name its primary {nb}")
        if f"notebooks/book/{l['companion']}" not in text:
            errs.append(f"{l['id']}: no link to its companion "
                        f"notebooks/book/{l['companion']}")
        missing = [e for e in REQUIRED_ELEMENTS if e.lower() not in text.lower()]
        if missing:
            warns.append(f"{l['id']}: missing element(s) {missing}")

    # (5) For-instructors appendix
    for edition in ("book", "book-pt", "book-es"):
        if not (REPO / edition / "for-instructors.qmd").exists():
            errs.append(f"{edition}/for-instructors.qmd missing")
    fi = BOOK_DIR / "for-instructors.qmd"
    if fi.exists():
        fi_text = fi.read_text()
        for n in NOTEBOOKS:
            if student_filename(n) not in fi_text:
                errs.append(f"For-instructors appendix does not link nb{n:02d}")

    # (6) localized companion links (frozen editions: verify only, D36)
    for edition, sub in (("book-pt", "pt"), ("book-es", "es")):
        for l in lessons:
            hit = REPO / edition / l["source"]
            if hit.exists() and f"notebooks/book/{sub}/{l['companion']}" \
                    not in hit.read_text():
                errs.append(f"{edition} {l['id']}: no localized companion link")

    # (7) orphan enumeration (round-9 N2)
    claimed_qmd = {str(BOOK_DIR / l["source"]) for l in lessons}
    for f in BOOK_DIR.glob("part*/*.qmd"):
        if f.name.endswith("-overview.qmd"):
            continue                      # the Part I overview page (D27)
        if str(f) not in claimed_qmd:
            errs.append(f"ORPHAN chapter file not in the manifest: "
                        f"{f.relative_to(REPO)}")
    claimed_comp = {l["companion"] for l in lessons}
    for sub in ("", "pt", "es"):
        d = NB_BOOK / sub if sub else NB_BOOK
        for f in sorted(d.glob("*.ipynb")):
            if f.name not in claimed_comp:
                errs.append(f"ORPHAN companion notebook not in the manifest: "
                            f"{f.relative_to(REPO)}")

    for w in warns:
        print(f"  ⚠️ {w}")
    if errs:
        print(f"✗ book sync: {len(errs)} problem(s)")
        for e in errs:
            print("  " + e)
        sys.exit(1)
    n_planned = sum(1 for l in arch["lessons"] if l["state"] == "planned")
    print(f"✓ book manifest consistent — {len(lessons)} active lessons "
          f"(+{n_planned} planned), all {len(NOTEBOOKS)} notebooks covered, "
          f"no orphans")


if __name__ == "__main__":
    main()
