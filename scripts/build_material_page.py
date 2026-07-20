#!/usr/bin/env python3
"""build_material_page.py — (re)generate material.qmd and instructor.qmd.

material.qmd is the student-facing, topic-indexed resource catalog (D15): one
row per topic notebook with its Colab badge, lecture count, the course dataset
bundle, and readings — the QM670-style split where Material is the catalog and
Schedule is the calendar. instructor.qmd is the same catalog pointing at the
PRIVATE instructor repo (instructor notebooks + session guides); the rendered
docs/instructor.html is encrypted post-render by scripts/protect_instructor_page.py.

Both pages are generated from planning/MEETING_SCHEDULE.csv +
scripts/notebooks_map.py — never hand-edit them; edit this generator or the
schedule data and rerun.

Usage:
    python3 scripts/build_material_page.py            # rewrite both pages
    python3 scripts/build_material_page.py --check    # exit 1 if stale
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from notebooks_map import (NOTEBOOKS, REPO_SLUG, colab_badge,  # noqa: E402
                           instructor_filename, lecture_count,
                           load_schedule_rows, nb_of, student_filename)

PRIVATE_SLUG = f"{REPO_SLUG}_instructor"
ZIP_LINK = ("[all datasets (.zip)](notebooks/data/honr46400_datasets.zip)")

MATERIAL_OUT = REPO / "material.qmd"
INSTRUCTOR_OUT = REPO / "instructor.qmd"

STYLE = '''```{=html}
<style>
  .overflow-table { font-size: 0.85rem; width: 100%; line-height: 1.25; }
  .overflow-table th, .overflow-table td {
    padding: 0.35rem; text-align: left; word-wrap: break-word; vertical-align: top;
  }
  .overflow-table th:nth-child(1), .overflow-table td:nth-child(1) { width: 34%; }
  .overflow-table th:nth-child(2), .overflow-table td:nth-child(2) { width: 12%; }
  .overflow-table th:nth-child(3), .overflow-table td:nth-child(3) { width: 18%; }
  .overflow-table th:nth-child(4), .overflow-table td:nth-child(4) { width: 16%; }
  .below-table { font-size: 0.85rem; line-height: 1.3; margin-top: 1rem; }
</style>
```'''

MATERIAL_HEADER = f'''---
title: "Material"
author: "Davi Moreira"
editor: visual
page-layout: full
toc: false
---

{STYLE}

# Course Material

One notebook per topic, listed in course order. Open a notebook in Colab from
its badge (no installation needed), download every dataset the course uses in
one bundle, and find the week-by-week calendar on the [Schedule](schedule.qmd)
page. Milestone instructions and rubrics are on Brightspace.

'''

MATERIAL_FOOTER = f'''
::: below-table

The **Data** column links the **course datasets (.zip)** — every dataset used
across the notebooks, in one download. Notebooks also load the same files
automatically from the course repository, so the bundle is your offline copy.

## Core Course References

- **Blair, G., Coppock, A., & Humphreys, M.** (2023). *Research Design in the
  Social Sciences: Declaration, Diagnosis, and Redesign*. Princeton University
  Press. Read free online: [book.declaredesign.org](https://book.declaredesign.org/){{target="_blank"}}.
- **Bergstrom, C. T., & West, J. D.** (2020). *Calling Bullshit: The Art of
  Skepticism in a Data-Driven World* — optional companion; public case studies
  at [callingbullshit.org](https://callingbullshit.org/){{target="_blank"}}.
- Course datasets ship from the MIT-licensed `rdss` package (see
  [`notebooks/data/`](https://github.com/{REPO_SLUG}/tree/main/notebooks/data){{target="_blank"}}).

:::
'''

INSTRUCTOR_HEADER = f'''---
title: "Instructor"
author: "Davi Moreira"
editor: visual
page-layout: full
toc: false
---

{STYLE}

# Instructor Material

Instructor notebooks (with solutions) and session guides, one row per topic.
Both live in the **private** repository
[`{PRIVATE_SLUG}`](https://github.com/{PRIVATE_SLUG}){{target="_blank"}} —
opening them requires being signed in to GitHub as the instructor. One-time
Colab setup: open [colab.research.google.com](https://colab.research.google.com/github){{target="_blank"}},
choose the GitHub tab, and check **"Include private repos"** when authorizing.

'''

INSTRUCTOR_FOOTER = '''
::: below-table

Instructor material is synced by `scripts/sync_instructor_repo.sh` after each
notebook build. This page is encrypted at render time
(`scripts/protect_instructor_page.py`); the password gate is a courtesy lock —
the private repository plus GitHub authentication is the real protection.

:::
'''


def instructor_badge(n: int) -> str:
    url = (f"https://colab.research.google.com/github/{PRIVATE_SLUG}/"
           f"blob/main/notebooks/instructor/{instructor_filename(n)}")
    return (f"[![Open In Colab](https://colab.research.google.com/assets/"
            f"colab-badge.svg)]({url}){{target=\"_blank\"}}")


def guide_link(n: int) -> str:
    url = (f"https://github.com/{PRIVATE_SLUG}/blob/main/"
           f"session_guides/{n:02d}_session_guide.md")
    return f"[session guide]({url}){{target=\"_blank\"}}"


def tracked_students() -> set[str]:
    out = subprocess.run(["git", "ls-files", "--cached", "notebooks/student/"],
                         cwd=REPO, capture_output=True, text=True)
    return {Path(p).name for p in out.stdout.split()}


def topic_info() -> list[dict]:
    """Per-notebook aggregates from the schedule: phase, sessions, readings, data."""
    rows = load_schedule_rows()
    info: dict[int, dict] = {}
    for r in rows:
        n = nb_of(r["other_material"])
        if n is None:
            continue
        d = info.setdefault(n, {"unit": r["unit"], "chapters": [], "cb": False,
                                "datasets": set(), "async": False})
        for ch in re.findall(r"ch\.\s*(\d+)", r["rdss_reading"]):
            if ch not in d["chapters"]:
                d["chapters"].append(ch)
        if r["cb_reading"].strip():
            d["cb"] = True
        if r["modality"] == "async-online":
            d["async"] = True
        for ds in ("lapop_brazil", "la_voter_file", "foos_etal",
                   "cliningsmith_etal", "bonilla_tillery"):
            if ds in r["dataset_simulation"].lower():
                d["datasets"].add(ds)
    ordered = []
    for n in sorted(info):
        d = info[n]
        d["nb"] = n
        d["lectures"] = lecture_count(n, rows)
        ordered.append(d)
    return ordered


def sessions_label(d: dict) -> str:
    if d["async"] and d["lectures"] == 0:
        return "async module"
    n = d["lectures"]
    return f"{n} lecture{'s' if n != 1 else ''}"


def readings_label(d: dict) -> str:
    parts = []
    if d["chapters"]:
        parts.append("RDSS ch. " + ", ".join(d["chapters"]))
    if d["cb"]:
        parts.append("*+ optional CB case*")
    return "<br>".join(parts) if parts else "—"


def data_cell(d: dict) -> str:
    named = "<br>".join(f"`{ds}.csv`" for ds in sorted(d["datasets"]))
    return f"{named}<br>{ZIP_LINK}" if named else ZIP_LINK


def build_table(instructor: bool) -> str:
    tracked = tracked_students()
    lines = ["::: overflow-table\n"]
    if instructor:
        lines.append("| Topic | Sessions | Notebook (solutions) | Session guide | Readings |")
        lines.append("|-------|----------|----------------------|---------------|----------|")
    else:
        lines.append("| Topic | Sessions | Notebook | Data | Readings |")
        lines.append("|-------|----------|----------|------|----------|")

    current_unit = None
    for d in topic_info():
        n = d["nb"]
        if d["unit"] != current_unit:
            current_unit = d["unit"]
            lines.append(f"| **{current_unit}** | | | | |")
        title = NOTEBOOKS[n][1]
        topic = f"**Topic {n:02d} · {title}**"
        if instructor:
            lines.append(f"| {topic} | {sessions_label(d)} | {instructor_badge(n)} "
                         f"| {guide_link(n)} | {readings_label(d)} |")
        else:
            badge = (colab_badge(n) if student_filename(n) in tracked
                     else f"*nb{n:02d} (coming)*")
            lines.append(f"| {topic} | {sessions_label(d)} | {badge} "
                         f"| {data_cell(d)} | {readings_label(d)} |")
    lines.append("\n:::")
    return "\n".join(lines)


def build(instructor: bool) -> str:
    if instructor:
        return INSTRUCTOR_HEADER + build_table(True) + INSTRUCTOR_FOOTER
    return MATERIAL_HEADER + build_table(False) + MATERIAL_FOOTER


def main() -> None:
    targets = {MATERIAL_OUT: build(False), INSTRUCTOR_OUT: build(True)}
    if "--check" in sys.argv:
        stale = [p.name for p, c in targets.items()
                 if not p.exists() or p.read_text() != c]
        if stale:
            print(f"✗ stale: {stale} — run scripts/build_material_page.py")
            sys.exit(1)
        print("✓ material.qmd + instructor.qmd up to date")
        return
    for p, c in targets.items():
        p.write_text(c)
        print(f"✓ wrote {p.relative_to(REPO)}")


if __name__ == "__main__":
    main()
