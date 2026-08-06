#!/usr/bin/env python3
"""audit_attribution.py — borrowed vocabulary never travels without its credit (D48).

The D48 audit found no copied prose but plenty of borrowed FRAMEWORK taught with
no local credit: MIDA, "diagnosand", and the four-pathway design library, used
on pages a reader can land on directly. Prose fixes alone regress, because
studio pages and notebooks are GENERATED and drift silently.

So this is the rule, machine-checked: any public teaching surface that uses a
borrowed term must name its source in the same file. A citation key, the
authors' names, "RDSS", or the book's title all count as credit.

Passing surfaces credit once per file — not per occurrence. Pages that merely
LINK to a lesson (tables of contents, adoption tables) are not teaching
surfaces and are skipped.

    .venv/bin/python scripts/audit_attribution.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# term -> the pattern that counts as crediting it in the same file
BORROWED = {
    "MIDA": r"blair2019declaring|blair2023rdss|RDSS|Blair|declaredesign",
    "diagnosand": r"blair2019declaring|blair2023rdss|RDSS|Blair|declaredesign",
}

# Surfaces a reader can land on directly. Generated files are included on
# purpose: that is exactly where credit goes missing.
GLOBS = (
    "book/**/*.qmd",
    "notebooks/student/*.ipynb",
    "notebooks/book/**/*.ipynb",
)

# Not teaching surfaces: pure navigation, or the generated rubric collection
# whose parent appendix carries the credit.
SKIP_NAMES = {"_iyt-rubrics.qmd", "for-instructors.qmd", "BOOK_MAP.md"}

# The frozen translations (D36) are replayed from English, not edited here.
SKIP_DIRS = ("book-pt", "book-es", "notebooks/book/pt", "notebooks/book/es")


def uses(text: str, term: str) -> bool:
    return re.search(rf"\b{re.escape(term)}", text, re.IGNORECASE) is not None


def main() -> int:
    problems: list[str] = []
    checked = 0

    for glob in GLOBS:
        for path in sorted(REPO.glob(glob)):
            rel = path.relative_to(REPO).as_posix()
            if path.name in SKIP_NAMES or any(d in rel for d in SKIP_DIRS):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            checked += 1
            for term, credit in BORROWED.items():
                if uses(text, term) and not re.search(credit, text):
                    problems.append(
                        f"    {rel}: teaches '{term}' with no credit in the file"
                    )

    if problems:
        print(f"✗ attribution audit: {len(problems)} surface(s) missing credit")
        print("\n".join(problems))
        print("\n  Fix at the SOURCE, never in a generated file:")
        print("    book/**/*.qmd            → the chapter")
        print("    book/studios/*.qmd       → planning/BOOK_STATIONS.yml")
        print("    notebooks/student/*.ipynb→ _production_kit/nb_sources/*.py")
        print("    notebooks/book/*.ipynb   → the chapter it is generated from")
        return 1

    print(f"✓ attribution audit: {checked} public surfaces clean — every use of "
          f"{', '.join(BORROWED)} names its source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
