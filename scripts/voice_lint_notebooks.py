#!/usr/bin/env python3
"""voice_lint_notebooks.py — enforce the CLAUDE.md voice rules on STUDENT
notebooks: student-facing cells speak TO the student, never ABOUT "students",
never to the instructor, never in facilitation voice. Also enforces the
Undergraduate-Friendly Voice rule (D14): em-dash budget (≤ EM_DASH_CELL_MAX per
markdown cell, ≤ EM_DASH_NB_MAX per notebook), no fourth-wall meta-references,
and the Lecture-Labels rule (D13): no dates, no "Meeting M#" references.

Usage:
    python3 scripts/voice_lint_notebooks.py [paths...]   # default: all student nbs
Exit non-zero on any violation. Also importable: lint_notebook(path) -> list.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import nbformat

REPO = Path(__file__).resolve().parent.parent

FORBIDDEN = [
    (re.compile(r"\bstudents?\b", re.I), 'third-person "student(s)"'),
    (re.compile(r"\bthe instructor\b", re.I), 'instructor reference'),
    (re.compile(r"\bhave them\b", re.I), "facilitation voice"),
    (re.compile(r"\bask the class\b", re.I), "facilitation voice"),
    (re.compile(r"\bfacilitat", re.I), "facilitation voice"),
    (re.compile(r"\bon camera\b", re.I), "camera language"),
    (re.compile(r"\bspeaking prompt\b", re.I), "camera language"),
    # D14 — fourth-wall meta-references about the material's construction
    (re.compile(r"\bfabricated for\b", re.I), "fourth-wall meta-reference"),
    (re.compile(r"\binvented for this\b", re.I), "fourth-wall meta-reference"),
    (re.compile(r"\bplanted fakes?\b", re.I), "fourth-wall meta-reference"),
    # D13 — lecture labels only, never meetings or dates
    (re.compile(r"\bMeeting M\d+\b"), 'meeting reference (use "Lecture i of N")'),
    (re.compile(r"\b(19|20)\d\d-\d\d-\d\d\b"), "calendar date"),
    (re.compile(r"\b(January|February|March|April|June|July|August|September|"
                r"October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept?|"
                r"Oct|Nov|Dec)\.?\s+\d{1,2}\b"), "calendar date"),
]

EM_DASH_CELL_MAX = 1    # per markdown cell (D14)
EM_DASH_NB_MAX = 20     # per notebook (D14)

# Text stripped before linting (URLs and repo paths legitimately contain
# "student", e.g. the Colab badge target notebooks/student/...).
STRIP = [
    re.compile(r"https?://\S+"),
    re.compile(r"notebooks/student/\S*"),
    re.compile(r"\S*_student\.ipynb"),
]


def lint_source(source: str) -> list[str]:
    text = source
    for pat in STRIP:
        text = pat.sub(" ", text)
    hits = []
    for pat, label in FORBIDDEN:
        for m in pat.finditer(text):
            ctx = text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            hits.append(f"{label}: …{ctx.strip()}…")
    return hits


def lint_notebook(path: Path) -> list[str]:
    nb = nbformat.read(path, as_version=4)
    problems = []
    em_total = 0
    for i, cell in enumerate(nb.cells):
        for hit in lint_source(cell.source):
            problems.append(f"{path.name} cell {i}: {hit}")
        if cell.cell_type == "markdown":
            n_em = cell.source.count("—")
            em_total += n_em
            if n_em > EM_DASH_CELL_MAX:
                problems.append(
                    f"{path.name} cell {i}: {n_em} em-dashes in one markdown "
                    f"cell (budget {EM_DASH_CELL_MAX}) — rewrite with periods, "
                    f"commas, or bold lead-ins")
    if em_total > EM_DASH_NB_MAX:
        problems.append(
            f"{path.name}: {em_total} em-dashes in markdown cells "
            f"(notebook budget {EM_DASH_NB_MAX})")
    return problems


def main() -> None:
    if len(sys.argv) > 1:
        targets = [Path(a) for a in sys.argv[1:]]
    else:
        targets = sorted((REPO / "notebooks" / "student").glob("nb*_student.ipynb"))
    if not targets:
        print("voice_lint: no student notebooks found (nothing to lint)")
        return
    all_problems = []
    for t in targets:
        all_problems += lint_notebook(t)
    if all_problems:
        print(f"✗ voice lint: {len(all_problems)} violation(s)")
        for p in all_problems:
            print("  " + p)
        sys.exit(1)
    print(f"✓ voice lint clean across {len(targets)} student notebook(s)")


if __name__ == "__main__":
    main()
