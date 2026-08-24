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

from notebooks_map import (NOTEBOOKS, colab_url, student_filename,  # noqa: E402
                           nb_of, session_kind, lecture_labels)
from validate_calendar import no_class_days  # noqa: E402
from session_readings import (lesson_index, rdss_note_compact,  # noqa: E402
                              render_cell, studio_pages)
from milestone_map import (additions, live_milestones,  # noqa: E402
                           milestone_map)


def tracked_students() -> set[str]:
    """Student notebooks known to git (staged or committed) — a badge may only
    point at a notebook that will exist on GitHub, never at local-only WIP."""
    out = subprocess.run(
        ["git", "ls-files", "--cached", "notebooks/student/"],
        cwd=REPO, capture_output=True, text=True)
    return {Path(p).name for p in out.stdout.split()}

SCHEDULE_CSV = REPO / "planning" / "MEETING_SCHEDULE.csv"
OUT = REPO / "schedule.qmd"

#: Hard ceiling on the RENDERED schedule page. The page has to stay pasteable
#: into a 65,535-character field, and the table only ever grows, so the limit is
#: checked here rather than discovered by whoever pastes it. Nothing else in the
#: build measures a rendered page, so if this check is removed the ceiling is
#: unguarded again.
RENDERED = REPO / "docs" / "schedule.html"
BYTE_CEILING = 65535

HEADER = '''---
title: "Schedule"
author: "Davi Moreira"
editor: visual
format:
  html:
    toc: false
    anchor-sections: false
    citations-hover: false
    footnotes-hover: false
---

```{=html}
<script>addEventListener("DOMContentLoaded",function(){document.querySelectorAll("main a[href]").forEach(function(a){a.target="_blank"})})</script>
```

# Course Schedule

'''

PLUS = "✚"

#: `{PLUS}` below is substituted at build time; FOOTER stays a plain string so
#: the Quarto attribute braces in it need no escaping.
FOOTER = '''
::: below-table

**Milestone column.** Every milestone links to the Book Milestone it presents in
[EDR|AI](book/index.html){target="_blank"}. A **{PLUS}** means that this
course requests something in addition to the book milestone.

## Core Course References

- **Blair, G., Coppock, A., & Humphreys, M.** (2023). *Research Design in the
  Social Sciences: Declaration, Diagnosis, and Redesign*. Princeton University
  Press. Read free online: [book.declaredesign.org](https://book.declaredesign.org/){target="_blank"}.

:::
'''.replace("{PLUS}", PLUS)


#: The Notebook cell: the Colab badge, and under it the one dataset bundle the
#: course and the book share, so a student never has to leave the row to find
#: the data the notebook loads.
DATA_ZIP = "[data.zip](notebooks/data/data.zip)"


def notebook_cell(n: int) -> str:
    return (f'<a href="{colab_url(n)}"><img src="https://colab.research.'
            f'google.com/assets/colab-badge.svg" alt="Open In Colab"></a>'
            f"<br>{DATA_ZIP}")


DAYNAMES = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri",
            5: "Sat", 6: "Sun"}


def pretty_date(iso: str, day: str) -> str:
    d = date.fromisoformat(iso)
    return f"{day} {d.strftime('%b %-d')}"


def week_studio(unit: str, studios: dict[int, dict],
                first: bool = True) -> tuple[str, str]:
    """`unit` -> ("Week 4", the Studio cell), repeated on every row.

    `first` marks the week's first row: only there does the Studio cell spell the
    title out. Later rows keep the link and the "Studio N" label, so a row still
    says which Studio it belongs to on its own.

    Weeks 1-12 are Studios 1-12 (D49), so the cell links to that Studio's own
    page in the book; the four dated exception weeks have no Studio and carry
    their label instead.
    """
    m = re.match(r"Week (\d+) — (.+)$", unit)
    if not m:
        return "", unit
    n, label = int(m.group(1)), m.group(2)
    st = next((item for item in studios.values() if item["title"] == label), None)
    if st:
        # The week's first row spells the title out; its repeats carry the
        # short label, and every row keeps the link.
        text = label if first else label.split(":")[0]
        cell = f"[{text}](book/{st['url_path']})"
    else:
        cell = f"*{label}*" if first else f"*{label.split(':')[0]}*"
    return f"Week {n}", cell


# ---------------------------------------------------------------------------
# The schedule page carries NO em dashes (instructor request, 2026-08-23).
#
# Em dashes reach this page from three upstream sources that legitimately keep
# them: authored session titles in scripts/schedule_data/, the shared reading
# renderer in session_readings.py, and the milestone chain in
# planning/MEETING_SCHEDULE.csv. Rewriting those would change the session
# guides, the Material page and the planning docs too, so the page normalizes
# on the way OUT instead: this is the last step of build().
#
# Ordered, most specific first. The two generic rules at the end are the net:
# any em dash a future edit introduces becomes a middle dot rather than
# leaking onto the page, and --check will never pass with one left.
EM = "\u2014"

DASH_RULES: list[tuple[object, str]] = [
    # reading-mode lead-ins from session_readings.MODE_LABEL: label, then list
    (f") **{EM}** ", "): "),
    (f" {EM}** ", ":** "),
    # chapter identity: "[Ch. 12 — Title]" reads as "Ch. 12: Title"
    (re.compile(rf"\[Ch\. (\d+) {EM} "), r"[Ch. \1: "),
    (f"companion {EM} ", "companion: "),
    # milestone column: "; M6 — Data and measurement governance, Book …"
    (re.compile(rf"(; M\d+) {EM} "), r"\1: "),
    # the terminal-lock parenthetical
    (f"11:59 PM {EM} ", "11:59 PM: "),
    # authored titles whose dash introduces rather than separates
    (f"indicator {EM} ", "indicator: "),
    (f"can carry {EM} ", "can carry; "),
    (f"for a stranger {EM} then", "for a stranger, then"),
    (f"Course reflection {EM} ", "Course reflection: "),
    (f"*No new chapter {EM} you present", "*No new chapter. You present"),
    # the net
    (f" {EM} ", " · "),
    (EM, "·"),
]


def no_em_dash(text: str) -> str:
    """Apply DASH_RULES in order; the page must contain no U+2014."""
    for find, repl in DASH_RULES:
        text = find.sub(repl, text) if hasattr(find, "sub") else text.replace(find, repl)
    if EM in text:                                    # unreachable via the net
        raise SystemExit("✗ em dash survived normalization")
    return text


#: One "M5 — title, Book Milestone 5 v1 (state)" segment of `milestone_developed`.
#: Only the course id and the trailing state are read from the authored prose.
#: WHICH Book Milestone a course milestone presents is NEVER parsed from here:
#: it comes from planning/COURSE_BOOK_CROSSWALK.yml through milestone_map, the
#: same way chapter identity comes from the book. The two had already drifted
#: (the authored M13 row says "Book Milestone 11"; the crosswalk says 10), and
#: the crosswalk is the source of truth.
SEG = re.compile(r"\s*(M\d+)\s*—\s*(.*?)\s*$")
STATE = re.compile(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)\s*$")

#: Marks a milestone whose Book Milestone does not by itself get the student to
#: the Purdue Fall Undergraduate Research Expo. Driven by the `schedule_mark` flag
#: in _research_project/milestone_course_additions.yml, which is a SEPARATE
#: decision from the `classification` that governs the PDF's "What this course
#: adds" section: turning a mark off must never delete a student instruction.
#: (defined above, next to FOOTER, which prints its legend)


def milestone_cell(raw: str, mmap: dict, adds: dict) -> str:
    """The Milestone column: the course id, its Book Milestone LINKED, the state.

    A milestone the course no longer runs prints as "No milestone". That is read
    from the live chain in course_config.yaml, never hardcoded: D54 retired M17
    because the last Friday of the semester is the course reflection session.
    The authored prose in scripts/schedule_data/ still names it, and the
    crosswalk row still carries Week 16's lessons, so the suppression happens
    here, at the page.
    """
    raw = raw.strip()
    if not raw:
        return ""
    lead = re.match(r"\s*M(\d+)", raw)
    if not lead:
        # D54: a session that develops no milestone says so in its own words
        # ("None — the chain closed at M16 ..."). Without this the segment
        # loop below would re-prefix it and print "MNone".
        return "No milestone"
    if f"M{int(lead.group(1)):02d}" not in live_milestones():
        return "No milestone"

    out = []
    for seg in raw.split("; M"):
        seg = seg if seg.lstrip().startswith("M") else "M" + seg
        m = SEG.match(seg)
        if not m:
            out.append(seg.strip())
            continue
        cid, rest = m.group(1), m.group(2)
        key = f"M{int(cid[1:]):02d}"
        info = mmap.get(key)
        if not info or not info["books"]:
            out.append(f"**{cid}**")
            continue
        mark = f" {PLUS}" if adds.get(key, {}).get("schedule_mark") else ""
        # The course id carries the link to the Book Milestone it presents;
        # naming both was saying the same thing twice in every row.
        first, rest = info["books"][0], info["books"][1:]
        cell = (f"**[{cid}]({first['url_path']}){{target=\"_blank\"}}**{mark}")
        if rest:
            cell += " + " + " + ".join(
                f"[Book Milestone {b['n']}]({b['url_path']}){{target=\"_blank\"}}"
                for b in rest)
        # The state ("dev", "worked; DUE …") is dropped: the milestone brief on
        # Brightspace carries it, and it was three different phrasings of the
        # same thing repeated down the column.
        out.append(cell)
    return "<br>".join(out)


def build() -> str:
    with open(SCHEDULE_CSV, newline="") as f:
        rows = list(csv.DictReader(f))

    tracked = tracked_students()
    labels = lecture_labels(rows)
    mmap, adds = milestone_map(), additions()
    lines = [HEADER, "::: overflow-table\n"]
    index = lesson_index()
    studios = studio_pages()
    lines.append("| # | Date | Week | Studio | Topic | Notebook | Milestone "
                 "| Required reading |")
    lines.append("|---|------|------|--------|-------|----------|-----------"
                 "|------------------|")

    seen_this_week: set[str] = set()
    current_unit = None
    #: The five MWF days the term does NOT meet. They carry no meeting number, so
    #: the CSV has no row for them; without a row a student cannot see that class
    #: is off. Each is printed immediately before the next meeting, and takes its
    #: Week and Studio from a meeting in the SAME calendar week — not from the next
    #: meeting, which for the Thanksgiving days sits a week later and would file
    #: them under the wrong studio.
    breaks = dict(no_class_days())
    unit_by_isoweek = {}
    for r in rows:
        unit_by_isoweek.setdefault(
            date.fromisoformat(r["date"]).isocalendar()[:2], r["unit"])

    for r in rows:
        first_of_week = r["unit"] != current_unit
        if first_of_week:
            current_unit, seen_this_week = r["unit"], set()
        week, studio = week_studio(r["unit"], studios, first_of_week)

        for iso in [d for d in sorted(breaks) if d < r["date"]]:
            label = breaks.pop(iso)
            d = date.fromisoformat(iso)
            unit = unit_by_isoweek.get(d.isocalendar()[:2], r["unit"])
            bweek, bstudio = week_studio(unit, studios, False)
            lines.append(
                f"| – | {pretty_date(iso, DAYNAMES[d.weekday()])} | {bweek} "
                f"| {bstudio} | **{label}** | | | |"
            )

        n = nb_of(r["other_material"])
        badge = ""
        if n is not None:
            badge = (notebook_cell(n) if student_filename(n) in tracked
                     else f"*nb{n:02d} (coming)*")

        title = r["title"].replace("ASYNC — ", "")
        lab = labels.get(int(r["meeting"]))
        if lab:
            _nb, i, total = lab
            title = f"{title} *(Lecture {i}/{total})*"

        mile = milestone_cell(r["milestone_developed"], mmap, adds)

        # Chapter identity is GENERATED from the book (session_readings), so
        # the page can never paraphrase a title the book publishes.
        blocks = [render_cell(r["book_reading"], index,
                              seen=seen_this_week, compact=True)]
        rec = rdss_note_compact(r["rdss_reading"])
        if rec:
            blocks.append(f"*Recommended companion — RDSS {rec}.*")
        materials = "<br>".join(b for b in blocks if b and b != "—") or "—"

        lines.append(
            f"| {r['meeting']} | {pretty_date(r['date'], r['day'])} | {week} "
            f"| {studio} | {title} | {badge} | {mile} | {materials} |"
        )

        # The URC Expo sits between M35 and M36 (Tue Nov 17, not an MWF meeting).
        if r["meeting"] == "35":
            lines.append(
                f"| – | Tue Nov 17 | {week} | {studio} | **🎓 Purdue Fall "
                "Undergraduate Research Expo — REQUIRED poster presentation "
                "(graded in Final Project)** | | M15 reflection evidence · "
                "Final Project Poster Presentation at the Purdue "
                "Undergraduate Research Conference "
                "| *No new chapter — you present the artifact Studio 10 "
                "built.* |"
            )

    lines.append("\n:::")
    lines.append(FOOTER)
    page = no_em_dash("\n".join(lines))
    # New-tab behaviour is set once by the HEADER script, so the
    # per-link attribute is stripped from every generated link.
    return page.replace('{target="_blank"}', "")


def check_rendered_size() -> None:
    """Fail if the last render of the schedule page breached the byte ceiling."""
    if not RENDERED.exists():
        print("  (docs/schedule.html not rendered yet — size unchecked)")
        return
    size = RENDERED.stat().st_size
    pct = 100 * (BYTE_CEILING - size) / BYTE_CEILING
    if size > BYTE_CEILING:
        raise SystemExit(
            f"✗ docs/schedule.html is {size:,} bytes — over the {BYTE_CEILING:,} "
            f"ceiling by {size - BYTE_CEILING:,}. Shrink the page (see the "
            f"reductions already applied in HEADER and week_studio) before shipping.")
    flag = "⚠ " if pct < 2 else "✓ "
    print(f"{flag}docs/schedule.html {size:,} bytes — {BYTE_CEILING - size:,} "
          f"under the ceiling ({pct:.1f}% margin)")


def main() -> None:
    content = build()
    if "--check" in sys.argv:
        if OUT.read_text() != content:
            print("✗ schedule.qmd is stale — run scripts/update_schedule_badges.py")
            sys.exit(1)
        print("✓ schedule.qmd up to date")
        check_rendered_size()
        return
    OUT.write_text(content)
    tracked = tracked_students()
    built = sum(1 for n in NOTEBOOKS if student_filename(n) in tracked)
    print(f"✓ schedule.qmd regenerated — {built}/{len(NOTEBOOKS)} notebook "
          f"badges live (git-tracked only)")
    check_rendered_size()


if __name__ == "__main__":
    main()
