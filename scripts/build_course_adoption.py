#!/usr/bin/env python3
"""build_course_adoption.py — de-course the chapter bodies (D35 Phase 4).

The book is institution-agnostic (D25/D35): chapter BODIES must not carry
course machinery. Every lesson's "Colab laboratory" section ended with a
paragraph naming its classroom lab (`nbNN`) and describing that lab's
activities — 40 of the A2 leakage hits, and the reason A2 could not become a
hard gate.

The content is not deleted, it is MOVED. This script:

  1. strips the course-lab tail from each lesson body, leaving the
     companion-notebook introduction, which is book material;
  2. collects each stripped description into the generated adoption table in
     `book/for-instructors.qmd`, which is where D25 says the companion course
     is presented.

The descriptions live in `planning/COURSE_LAB_NOTES.yml`, extracted once from
the chapter bodies so nothing is lost, then authored there from now on.

    .venv/bin/python scripts/build_course_adoption.py            # write
    .venv/bin/python scripts/build_course_adoption.py --check    # CI: fresh?
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from book_manifest import (active_lessons, load_crosswalk,  # noqa: E402
                           primary_nb_by_lesson, require_lock)
from notebooks_map import NOTEBOOKS, student_filename  # noqa: E402

NOTES = REPO / "planning" / "COURSE_LAB_NOTES.yml"
FI = REPO / "book" / "for-instructors.qmd"
COURSE_NB = ("https://colab.research.google.com/github/davi-moreira/"
             "2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/student")

LAB_TAIL = re.compile(
    r"\s*The full classroom laboratory behind this chapter is course notebook.*?(?=\n\n)",
    re.S)
BEGIN = "<!-- course-adoption:begin -->"
END = "<!-- course-adoption:end -->"
BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)


def extract_notes() -> dict:
    """One-time extraction of the lab descriptions before they are stripped."""
    notes = {}
    if NOTES.exists():
        notes = yaml.safe_load(NOTES.read_text()) or {}
    changed = False
    for l in active_lessons():
        if l["id"] in notes:
            continue
        m = LAB_TAIL.search((REPO / "book" / l["source"]).read_text())
        if not m:
            continue
        text = " ".join(m.group(0).split())
        # keep only the sentence(s) describing what the lab does
        after = re.split(r"appendix\.\s*", text, maxsplit=1)
        notes[l["id"]] = after[1].strip() if len(after) > 1 else ""
        changed = True
    if changed:
        NOTES.write_text(
            "# COURSE_LAB_NOTES.yml — what each course lab does (GENERATED once,\n"
            "# then authored here). Rendered into book/for-instructors.qmd by\n"
            "# scripts/build_course_adoption.py. Keyed by lesson id.\n\n"
            + yaml.dump(notes, sort_keys=False, allow_unicode=True, width=78))
    return notes


def adoption_table(notes: dict) -> str:
    primary = primary_nb_by_lesson()
    rows = ["| Lesson | Course lab | What the lab does |", "|---|---|---|"]
    for l in active_lessons():
        nb = primary.get(l["id"], "")
        if not nb:
            continue
        n = int(nb[2:])
        title = NOTEBOOKS[n][1] if n in NOTEBOOKS else nb
        link = f"[{nb}]({COURSE_NB}/{student_filename(n)})"
        note = notes.get(l["id"], "") or "—"
        rows.append(f"| Ch. {l['display']} | {link} — {title} | {note} |")
    # Revisit-only labs (D41): a course week may carry no first-read lesson
    # — its notebook still exists and is listed here so the course lab set
    # stays complete (nb13 is the public-test/Expo week).
    anchored_nbs = {int(nb[2:]) for nb in primary.values()}
    revisit_lines = []
    for r in load_crosswalk()["rows"]:
        n = int(r["nb"][2:])
        if n in anchored_nbs or not r.get("assignments"):
            continue
        title = NOTEBOOKS[n][1] if n in NOTEBOOKS else r["nb"]
        revisit_lines.append(
            f"[{r['nb']}]({COURSE_NB}/{student_filename(n)}) — {title}")
    revisit_para = ""
    if revisit_lines:
        revisit_para = ("\n\nRevisit-only labs (no new lesson; the week "
                        "revisits earlier chapters): "
                        + "; ".join(revisit_lines) + ".")
    return (f"{BEGIN}\n\n### Which lab goes with which lesson\n\n"
            "Each lesson's companion notebook belongs to the book. The table\n"
            "below maps every lesson to the classroom lab that carries it in the\n"
            "companion course, and says what that lab does.\n\n"
            + "\n".join(rows) + revisit_para + f"\n\n{END}")


def render() -> tuple[dict[Path, str], str]:
    require_lock()
    notes = extract_notes()
    out: dict[Path, str] = {}
    for l in active_lessons():
        path = REPO / "book" / l["source"]
        text = path.read_text()
        stripped = LAB_TAIL.sub("", text)
        if stripped != text:
            out[path] = stripped
    fi = FI.read_text()
    table = adoption_table(notes)
    if BLOCK_RE.search(fi):
        fi_new = BLOCK_RE.sub(table, fi)
    else:
        fi_new = fi.rstrip() + "\n\n" + table + "\n"
    return out, fi_new


def main() -> int:
    check = "--check" in sys.argv
    bodies, fi_new = render()
    stale = [p.relative_to(REPO).as_posix() for p in bodies]
    if FI.read_text() != fi_new:
        stale.append("book/for-instructors.qmd")
    if check:
        if stale:
            print(f"✗ course adoption is STALE ({len(stale)}): "
                  f"{', '.join(stale[:3])}… — run scripts/build_course_adoption.py")
            return 1
        print("✓ chapter bodies are de-coursed and the adoption table is fresh")
        return 0
    for path, content in bodies.items():
        path.write_text(content)
    FI.write_text(fi_new)
    print(f"✓ de-coursed {len(bodies)} lesson bodies; adoption table regenerated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
