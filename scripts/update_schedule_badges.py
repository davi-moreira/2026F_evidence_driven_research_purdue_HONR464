#!/usr/bin/env python3
"""update_schedule_badges.py — (re)generate schedule.qmd from the meeting
schedule, adding a Colab badge for every topic notebook whose STUDENT file
exists in notebooks/student/.

This is the single source of truth for the public schedule page: one row per
MWF meeting (43 rows), generated from planning/MEETING_SCHEDULE.csv +
scripts/notebooks_map.py. Week and Studio are COLUMNS repeated on every row,
not spanning group headers, so any row read on its own still says which Studio
it belongs to (and every row stays sortable and filterable). Badges appear
automatically as each nbNN_*_student.ipynb is finalized — run this after
generating a student notebook (also wired as a Claude Code PostToolUse hook).

Usage:
    python3 scripts/update_schedule_badges.py            # rewrite schedule.qmd
    python3 scripts/update_schedule_badges.py --check    # exit 1 if stale
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from notebooks_map import (NOTEBOOKS, colab_badge, student_filename,  # noqa: E402
                           nb_of, session_kind, lecture_labels)
from session_readings import (lesson_index, rdss_note,  # noqa: E402
                              render_cell, studio_pages)


def tracked_students() -> set[str]:
    """Student notebooks known to git (staged or committed) — a badge may only
    point at a notebook that will exist on GitHub, never at local-only WIP."""
    out = subprocess.run(
        ["git", "ls-files", "--cached", "notebooks/student/"],
        cwd=REPO, capture_output=True, text=True)
    return {Path(p).name for p in out.stdout.split()}

SCHEDULE_CSV = REPO / "planning" / "MEETING_SCHEDULE.csv"
OUT = REPO / "schedule.qmd"

HEADER = '''---
title: "Schedule"
author: "Davi Moreira"
editor: visual
---

```{=html}
<style>
  .overflow-table { font-size: 0.85rem; width: 100%; line-height: 1.2; }
  .overflow-table th, .overflow-table td {
    padding: 0.3rem; text-align: left; word-wrap: break-word; vertical-align: top;
  }
  .overflow-table th:nth-child(1), .overflow-table td:nth-child(1) { width: 3%; }
  .overflow-table th:nth-child(2), .overflow-table td:nth-child(2) { width: 7%; }
  .overflow-table th:nth-child(3), .overflow-table td:nth-child(3) { width: 5%; }
  .overflow-table th:nth-child(4), .overflow-table td:nth-child(4) { width: 13%; }
  .overflow-table th:nth-child(5), .overflow-table td:nth-child(5) { width: 19%; }
  .overflow-table th:nth-child(6), .overflow-table td:nth-child(6) { width: 7%; }
  .overflow-table th:nth-child(7), .overflow-table td:nth-child(7) { width: 12%; }
  .overflow-table th:nth-child(8), .overflow-table td:nth-child(8) { width: 34%; }
  .below-table { font-size: 0.85rem; line-height: 1.2; margin-top: 1rem; }
</style>
```

# Course Schedule

'''

FOOTER = '''
::: below-table

**Key dates:** URC abstract internal gate **Fri Oct 9** · Final poster
**Fri Nov 6** · **Purdue Fall Undergraduate Research Expo: Tue Nov 17**
(required poster presentation) · Evidence Defenses **Dec 7 & 9** · Course
reflection **Fri Dec 11**. No class: Sep 7 (Labor Day), Oct 12 (October Break),
Nov 25/27 (Thanksgiving). Async-online meeting: Mon Nov 23.

**The one required meeting outside the MWF pattern is the Expo, Tue Nov 17.**
It is a graded component of M15, not an optional showcase, and it falls on a
day this section never otherwise meets. Hold the day from Week 1: you set up
before your window, stand with your poster through it, and complete your peer
evaluations of at least three posters on the floor, so budget well beyond one
class period. Exact hours are published by the Expo closer to the date and
posted to Brightspace as soon as they are known. Bring a Tuesday conflict to
the instructor in the first two weeks, while it can still be worked around.

## Core Course References

- **Blair, G., Coppock, A., & Humphreys, M.** (2023). *Research Design in the
  Social Sciences: Declaration, Diagnosis, and Redesign*. Princeton University
  Press. Read free online: [book.declaredesign.org](https://book.declaredesign.org/){target="_blank"}.
- **Bergstrom, C. T., & West, J. D.** (2020). *Calling Bullshit: The Art of
  Skepticism in a Data-Driven World* — optional companion; public case studies
  at [callingbullshit.org](https://callingbullshit.org/){target="_blank"}.
- Course datasets ship from the MIT-licensed `rdss` package (see
  [`notebooks/data/`](https://github.com/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/tree/main/notebooks/data){target="_blank"}).

:::
'''


def pretty_date(iso: str, day: str) -> str:
    d = date.fromisoformat(iso)
    return f"{day} {d.strftime('%b %-d')}"


def week_studio(unit: str, studios: dict[int, dict]) -> tuple[str, str]:
    """`unit` -> ("Week 4", the Studio cell), repeated on every row.

    Weeks 1-12 are Studios 1-12 (D49), so the cell links to that Studio's own
    page in the book; the four dated exception weeks have no Studio and carry
    their label instead.
    """
    m = re.match(r"Week (\d+) — (.+)$", unit)
    if not m:
        return "", f"**{unit}**"
    n, label = int(m.group(1)), m.group(2)
    st = next((item for item in studios.values() if item["title"] == label), None)
    if st:
        cell = (f"**[{label}](book/{st['url_path']})"
                f"{{target=\"_blank\"}}**")
    else:
        cell = f"*{label}*"
    return f"**Week {n}**", cell


def build() -> str:
    with open(SCHEDULE_CSV, newline="") as f:
        rows = list(csv.DictReader(f))

    tracked = tracked_students()
    labels = lecture_labels(rows)
    lines = [HEADER, "::: overflow-table\n"]
    index = lesson_index()
    studios = studio_pages()
    lines.append("| # | Date | Week | Studio | Topic | Notebook | Milestone "
                 "| Required reading |")
    lines.append("|---|------|------|--------|-------|----------|-----------"
                 "|------------------|")

    for r in rows:
        week, studio = week_studio(r["unit"], studios)

        n = nb_of(r["other_material"])
        badge = ""
        if n is not None:
            badge = (colab_badge(n) if student_filename(n) in tracked
                     else f"*nb{n:02d} (coming)*")

        title = r["title"]
        if r["modality"] == "async-online":
            title = f"**ASYNC** — {title.replace('ASYNC — ', '')}"
        lab = labels.get(int(r["meeting"]))
        if lab:
            _nb, i, total = lab
            title = f"{title} *(Lecture {i}/{total})*"

        mile = r["milestone_developed"]
        # compact for the site: keep the course id + any "Book Milestone N"
        # bridge token; drop the long title between them (D41)
        bm = re.search(r"Book Milestone \d+[^|]*", mile)
        mile = re.sub(r" — [^|]*", "", mile).strip()
        mile = mile.replace("(presented + submitted)", "").strip()
        if bm:
            mile = f"{mile} · {bm.group(0).strip()}" if mile else bm.group(0).strip()

        # Chapter identity is GENERATED from the book (session_readings), so
        # the page can never paraphrase a title the book publishes.
        blocks = [render_cell(r["book_reading"], index)]
        rec = rdss_note(r["rdss_reading"])
        if rec:
            blocks.append(f"*Recommended companion — RDSS {rec}.*")
        if r["cb_reading"].strip():
            blocks.append("*Optional: Calling Bullshit case study.*")
        materials = "<br>".join(b for b in blocks if b and b != "—") or "—"

        lines.append(
            f"| {r['meeting']} | {pretty_date(r['date'], r['day'])} | {week} "
            f"| {studio} | {title} | {badge} | {mile} | {materials} |"
        )

        # The URC Expo sits between M35 and M36 (Tue Nov 17, not an MWF meeting).
        if r["meeting"] == "35":
            lines.append(
                f"| — | Tue Nov 17 | {week} | {studio} | **🎓 Purdue Fall "
                "Undergraduate Research Expo — REQUIRED poster presentation "
                "(graded M15 component)** | | M15 · Book Milestone 10 v3 "
                "| *No new chapter — you present the artifact Studio 10 "
                "built.* |"
            )

    lines.append("\n:::")
    lines.append(FOOTER)
    return "\n".join(lines)


def main() -> None:
    content = build()
    if "--check" in sys.argv:
        if OUT.read_text() != content:
            print("✗ schedule.qmd is stale — run scripts/update_schedule_badges.py")
            sys.exit(1)
        print("✓ schedule.qmd up to date")
        return
    OUT.write_text(content)
    tracked = tracked_students()
    built = sum(1 for n in NOTEBOOKS if student_filename(n) in tracked)
    print(f"✓ schedule.qmd regenerated — {built}/{len(NOTEBOOKS)} notebook "
          f"badges live (git-tracked only)")


if __name__ == "__main__":
    main()
