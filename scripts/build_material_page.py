#!/usr/bin/env python3
"""build_material_page.py — (re)generate material.qmd and instructor.qmd.

material.qmd is the student-facing, topic-indexed resource catalog (D15): one
row per topic notebook with its Colab badge, lecture count, the course dataset
bundle, and readings — the QM670-style split where Material is the catalog and
Schedule is the calendar. instructor.qmd is the same catalog pointing at the
PRIVATE instructor repo (instructor notebooks + session guides); the page ships
openly (D35) — the private repo + GitHub auth is the protection.

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
from session_readings import (by_mode, chapter_link, lesson_index,  # noqa: E402
                              rdss_note)

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

One Studio per week, listed in course order — the week's classroom lab, its
datasets, and **the book chapters that week requires**. Open a notebook in
Colab from its badge (no installation needed), download every dataset the
course uses in one bundle, and find the per-session calendar on the
[Schedule](schedule.qmd) page.

**This course is the book, applied.** Required reading comes from
[**EDR|AI** — *Evidence-Driven Research in the Age of AI*](book/index.html){{target="_blank"}}
(a work in progress, growing across the semester). Monday and Wednesday teach
the Studio's chapters and the work their closing **"It is your turn"** sections
ask for; **Friday is that Studio's milestone**, and those completed sections are
submitted with it. Chapter titles below are the book's own — follow a link to
land on the chapter, where a badge opens its **companion Colab notebook**. The
matching RDSS chapters are a *recommended* companion, never a substitute.
Milestone instructions and rubrics are on Brightspace.

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

Instructor notebooks (with solutions) and session guides, one row per Studio,
each with the week's required **EDR|AI** chapters — the same reading students
see on [Material](material.qmd) and [Schedule](schedule.qmd), generated from the
book's own manifest so the three surfaces cannot drift apart.
Both live in the **private** repository
[`{PRIVATE_SLUG}`](https://github.com/{PRIVATE_SLUG}){{target="_blank"}} —
opening them requires being signed in to GitHub as the instructor. One-time
Colab setup: open [colab.research.google.com](https://colab.research.google.com/github){{target="_blank"}},
choose the GitHub tab, and check **"Include private repos"** when authorizing.

'''

INSTRUCTOR_FOOTER = '''
::: below-table

Instructor material is synced by `scripts/sync_instructor_repo.sh` after each
notebook build. The private repository plus GitHub authentication is what
protects it — the links above open only for the instructor's GitHub account.

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


BOOK_MAP = REPO / "planning" / "BOOK_MAP.md"
BOOK_PART_SLUGS = {
    "I": "part1-research-with-ai", "II": "part2-curiosity-to-design",
    "III": "part3-pathways", "IV": "part4-credible-evidence",
    "V": "part5-communicating", "VI": "part6-after-conference",
}


def book_chapters_by_nb() -> dict[int, list[dict]]:
    """nb number -> the lessons that notebook's week owns, in book order.

    Identity (display number, PUBLISHED title, url_path) comes from
    session_readings/book_manifest — never from a numeric filename prefix
    (round-8 P1 / A10: display numbers are derived labels). The
    primary-notebook mapping comes from the crosswalk's home anchors.
    """
    import yaml
    cw = yaml.safe_load((REPO / "planning" / "COURSE_BOOK_CROSSWALK.yml").read_text())
    primary: dict[str, tuple[int, str]] = {}
    for r in cw["rows"]:
        for a in r.get("assignments", []):
            if a.get("home_anchor"):
                primary[a["lesson"]] = (int(r["nb"][2:]), a["requirement"])
    out: dict[int, list[dict]] = {}
    for lesson in lesson_index().values():
        hit = primary.get(lesson["id"])
        if hit is not None:
            nb, requirement = hit
            out.setdefault(nb, []).append({**lesson, "requirement": requirement})
    for v in out.values():
        v.sort(key=lambda l: l["display"])
    return out


def topic_info() -> list[dict]:
    """Per-notebook aggregates from the schedule: sessions, book readings, data."""
    rows = load_schedule_rows()
    chapters = book_chapters_by_nb()
    info: dict[int, dict] = {}
    for r in rows:
        n = nb_of(r["other_material"])
        if n is None:
            continue
        d = info.setdefault(n, {"datasets": set(), "async": False, "rdss": [],
                                "unit": r["unit"], "revisits": []})
        rec = rdss_note(r["rdss_reading"])
        if rec:
            # One catalog row aggregates a whole week, and two sessions often
            # recommend the same RDSS chapters in different words. Keep a note
            # only when it brings a chapter the row does not already carry.
            chs = set(re.findall(r"ch\.\s*(\d+)", rec))
            known = set().union(*(set(re.findall(r"ch\.\s*(\d+)", n))
                                  for n in d["rdss"])) if d["rdss"] else set()
            if rec not in d["rdss"] and not (chs and chs <= known):
                d["rdss"].append(rec)
        for lid in by_mode(r["book_reading"]).get("revisit", []):
            if lid not in d["revisits"]:
                d["revisits"].append(lid)
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
        d["chapters"] = chapters.get(n, [])
        ordered.append(d)
    return ordered


def sessions_label(d: dict) -> str:
    if d["async"] and d["lectures"] == 0:
        return "async module"
    n = d["lectures"]
    return f"{n} lecture{'s' if n != 1 else ''}"


#: Course policy on a chapter that does not bind every student (crosswalk C1).
CONDITION = {
    "route-required": " *— your declared route, or the contrast assigned to you*",
    "optional": " *— only if your design has stages*",
}


def readings_label(d: dict, index: dict[str, dict]) -> str:
    """Required EDR|AI chapters BY THEIR PUBLISHED TITLES, then the RDSS note.

    Titles are read from each chapter's own front matter, so this page can
    never carry a paraphrase of something the book publishes differently.
    """
    parts = []
    if d["chapters"]:
        links = "<br>".join(chapter_link(l) + CONDITION.get(l.get("requirement"), "")
                            for l in d["chapters"])
        parts.append(f"**Required — EDR\\|AI**<br>{links}")
    if d.get("revisits"):
        seen = [index[i] for i in d["revisits"] if i in index]
        seen.sort(key=lambda l: l["display"])
        if seen:
            parts.append("**Revisited this week**<br>"
                         + "<br>".join(chapter_link(l) for l in seen))
    if d.get("rdss"):
        parts.append("*Recommended companion — RDSS "
                     + "; ".join(d["rdss"]) + ".*")
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

    index = lesson_index()
    for d in topic_info():
        n = d["nb"]
        # The unit string is held equal to the book's published studio title
        # by scripts/validate_session_readings.py (check F).
        week, _, studio = d["unit"].partition(" — ")
        topic = f"**{studio or NOTEBOOKS[n][1]}**<br>*{week} · nb{n:02d}*"
        if instructor:
            lines.append(f"| {topic} | {sessions_label(d)} | {instructor_badge(n)} "
                         f"| {guide_link(n)} | {readings_label(d, index)} |")
        else:
            badge = (colab_badge(n) if student_filename(n) in tracked
                     else f"*nb{n:02d} (coming)*")
            lines.append(f"| {topic} | {sessions_label(d)} | {badge} "
                         f"| {data_cell(d)} | {readings_label(d, index)} |")
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
