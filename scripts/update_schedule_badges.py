#!/usr/bin/env python3
"""update_schedule_badges.py — (re)generate schedule.qmd from the meeting
schedule, adding a Colab badge for every topic notebook whose STUDENT file
exists in notebooks/student/.

This is the single source of truth for the public schedule page: one row per
MWF meeting (43 rows), grouped by course week, generated from
planning/MEETING_SCHEDULE.csv + scripts/notebooks_map.py. Badges appear
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
  .overflow-table th:nth-child(1), .overflow-table td:nth-child(1) { width: 4%; }
  .overflow-table th:nth-child(2), .overflow-table td:nth-child(2) { width: 9%; }
  .overflow-table th:nth-child(5), .overflow-table td:nth-child(5) { width: 12%; }
  .below-table { font-size: 0.85rem; line-height: 1.2; margin-top: 1rem; }
</style>
```

# Course Schedule

Forty-four Monday/Wednesday/Friday meetings (42 in person, 2 asynchronous
online). The weekly rhythm: **Monday and Wednesday are lectures** (new content,
one notebook per topic), and **every Friday is a studio** — a quick recap of
the week, the next project milestone presented, and the rest of the class spent
working on your milestone and research project. Open each notebook in Colab
from its badge; milestone instructions and rubrics are on Brightspace. Topic
resources are also cataloged on the [Material](material.qmd) page, and every
dataset the course uses is in the
[course datasets (.zip)](notebooks/data/honr46400_datasets.zip) bundle.

'''

FOOTER = '''
::: below-table

**Key dates:** URC abstract internal gate **Fri Oct 9** · Final poster
**Fri Nov 6** · **Purdue Fall Undergraduate Research Expo: Tue Nov 17**
(required poster presentation) · Evidence Defenses **Dec 7 & 9** · Final
dossier **Fri Dec 11**. No class: Sep 7 (Labor Day), Oct 12 (October Break),
Nov 25/27 (Thanksgiving). Async-online meetings: Oct 2 and Nov 23.

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


def build() -> str:
    with open(SCHEDULE_CSV, newline="") as f:
        rows = list(csv.DictReader(f))

    tracked = tracked_students()
    labels = lecture_labels(rows)
    lines = [HEADER, "::: overflow-table\n"]
    lines.append("| # | Date | Topic | Notebook | Milestone | Materials |")
    lines.append("|---|------|-------|----------|-----------|-----------|")

    current_unit = None
    for r in rows:
        unit = r["unit"]
        if unit != current_unit:
            current_unit = unit
            lines.append(f"| | | **{unit}** | | | |")

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
        mile = re.sub(r" — [^|]*", "", mile)  # compact: IDs only on the site
        mile = mile.replace("(presented + submitted)", "").strip()

        reading = r["rdss_reading"]
        reading = re.sub(r"\s*\(book\.declaredesign\.org\)", "", reading)
        reading = re.sub(r"\s*\(([^)]*)\)$", "", reading).strip()
        if reading.startswith("(") or not reading:
            reading = "—"
        materials = reading
        if r["cb_reading"].strip():
            materials += "<br>*+ optional CB case*"

        lines.append(
            f"| {r['meeting']} | {pretty_date(r['date'], r['day'])} | {title} "
            f"| {badge} | {mile} | {materials} |"
        )

        # The URC Expo sits between M35 and M36 (Tue Nov 17, not an MWF meeting).
        if r["meeting"] == "35":
            lines.append(
                "| — | Tue Nov 17 | **🎓 Purdue Fall Undergraduate Research "
                "Expo — REQUIRED poster presentation (graded M12 component)** "
                "| | M12 | URC Expo |"
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
