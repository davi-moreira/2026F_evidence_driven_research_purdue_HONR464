#!/usr/bin/env python3
"""build_participation_schedules.py — the two instructor-facing assignment tables.

Both are DERIVED, never hand-written, so they cannot drift from the calendar:

  planning/READING_FEEDBACK_SCHEDULE.md
      One row per EDR|AI chapter: when its reading-feedback survey opens and
      closes. Reading feedback is graded inside Participation (9%), which the
      syllabus already defines as "feedback surveys, lecture-notebook
      completion, and other constructive contributions".

      The partition is exact. Every active lesson has exactly one HOME ANCHOR
      in planning/MEETING_SCHEDULE.csv: the session where it is first required.
      Feedback rides that anchor, so each chapter is rated once and only once,
      and the responses land BEFORE the session that teaches it.

  planning/SRL_ASSIGNMENT_SCHEDULE.md
      One row per Student Research Lead slot: which lecture it is, which frame
      it runs, when the preparation script is due, and the seed puzzle.

      NO STUDENT NAMES. The draw itself is FERPA-protected student data and
      lives only in the gitignored `_adm/roster/` (scripts/assign_srl_slots.py,
      scripts/build_srl_packet.py). This table is the slot structure, which is
      the part that is safe to keep in the repository and reuse.

Usage:
    .venv/bin/python scripts/build_participation_schedules.py
    .venv/bin/python scripts/build_participation_schedules.py --check
"""
from __future__ import annotations

import csv
import datetime as dt
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from session_readings import lesson_index, parse  # noqa: E402

SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.CSV"
if not SCHEDULE.exists():
    SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.csv"
READING_OUT = REPO / "planning" / "READING_FEEDBACK_SCHEDULE.md"
SRL_OUT = REPO / "planning" / "SRL_ASSIGNMENT_SCHEDULE.md"

sys.path.insert(0, str(REPO / "scripts"))
from validate_calendar import no_class_days  # noqa: E402

CLOSED = set(no_class_days())

#: How a lesson's anchoring mode maps onto who owes feedback on it.
#: `route` / `route-contrast` lessons are read by every student, but only two
#: of the five apply to any one student: their own declared route plus the
#: contrast the instructor assigns them.
REQUIREMENT = {
    "first-read": "Everyone",
    "assigned": "Everyone",
    "route": "Route only (your declared route or your assigned contrast)",
    "route-contrast": "Route only (your declared route or your assigned contrast)",
    "optional": "Only if your design has stages",
}


def rows() -> list[dict]:
    with SCHEDULE.open(newline="") as fh:
        return list(csv.DictReader(fh))


def pretty(iso: str, day: str) -> str:
    return f"{day} {dt.date.fromisoformat(iso).strftime('%b %-d')}"


def week_of(unit: str) -> tuple[str, str]:
    m = re.match(r"Week (\d+) — (.+)$", unit)
    return (f"{m.group(1)}", m.group(2)) if m else ("", unit)


# ---------------------------------------------------------------------------
# 1. reading feedback

def reading_table(meetings: list[dict]) -> str:
    index = lesson_index()
    anchor: dict[str, tuple[int, str]] = {}
    assigned_at: dict[str, int] = {}
    #: `assigned` means "handed out today, read it for the NEXT session", so it
    #: opens the feedback window but never closes it. The closing session is the
    #: first one where the chapter is actually required to have been read.
    READ_MODES = ("first-read", "route", "route-contrast", "optional")
    for r in meetings:
        for lid, mode in parse(r["book_reading"]):
            n = int(r["meeting"])
            if mode == "assigned":
                assigned_at.setdefault(lid, n)
            if lid in anchor or mode not in READ_MODES:
                continue
            anchor[lid] = (n, mode)
    #: a chapter handed out but never re-listed as required falls back to its
    #: assignment session rather than dropping out of the schedule entirely
    for lid, n in assigned_at.items():
        anchor.setdefault(lid, (n, "assigned"))

    missing = [l for l in index if l not in anchor]
    if missing:
        raise SystemExit(f"✗ no anchor session for: {missing}")

    by_meeting = {int(r["meeting"]): r for r in meetings}
    # calendar order: this is the order the instructor works through the term
    ordered = sorted(index.values(),
                     key=lambda l: (anchor[l["id"]][0], l["display"]))

    counts = {"Everyone": 0, "route": 0, "conditional": 0}
    lines = [
        "| # | Chapter | Title | Week | Studio | Feedback closes at the start of "
        "| Who owes it |",
        "|---|---|---|---|---|---|---|",
    ]
    seq = 0
    for lesson in ordered:
        seq += 1
        n, mode = anchor[lesson["id"]]
        r = by_meeting[n]
        week, studio = week_of(r["unit"])
        req = REQUIREMENT[mode]
        if req == "Everyone":
            counts["Everyone"] += 1
        elif req.startswith("Route"):
            counts["route"] += 1
        else:
            counts["conditional"] += 1
        opens = assigned_at.get(lesson["id"])
        session = (f"Meeting {n}, {pretty(r['date'], r['day'])}"
                   + (f" (assigned meeting {opens})" if opens and opens < n else ""))
        lines.append(
            f"| {seq} | Ch. {lesson['display']} | {lesson['title']} "
            f"| {week} | {studio} | {session} | {req} |")

    per_student = counts["Everyone"] + 2
    head = f"""# Reading Feedback Schedule — EDR\\|AI

*Generated by `scripts/build_participation_schedules.py`. Do not hand-edit.*

Every chapter of **EDR\\|AI** carries one reading-feedback response, graded inside
**Participation (9%)**. One Qualtrics survey serves all of them; the student picks
the chapter on the first question. The instrument, its scoring rule and its
Qualtrics import files live in [`surveys/`](../surveys/).

**When it is due.** Feedback closes at the **start of the session where the chapter
is first required**, which is the same moment the reading itself is due. That is
deliberate: the responses arrive before the session that teaches the chapter, so
they can shape it, and a student cannot write the feedback from the class
discussion instead of from the reading.

**How many responses each student owes**

| | Chapters | Note |
|---|---|---|
| Required of everyone | {counts['Everyone']} | one per chapter |
| Pathway chapters | {counts['route']} | each student reads **2** of these: their own declared route plus the contrast the instructor assigns |
| Conditional | {counts['conditional']} | binds only if the design has stages |
| **Baseline per student** | **{per_student}** | {counts['Everyone']} + 2 pathway |

**Grading.** Scored for completion and seriousness, not for praise. The rubric and
the drop allowance are in [`surveys/reading_feedback_grading.md`](../surveys/reading_feedback_grading.md).

---

## The schedule

"""
    return head + "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# 2. SRL slots

FRAME = {
    "Mon": ("Monday · guided investigation",
            "0–9 your research puzzle · 9–31 guided AI investigation · "
            "31–43 verification and formalization (instructor) · 43–50 decision and defense"),
    "Wed": ("Wednesday · applied AI laboratory",
            "0–7 your retrieval challenge · 7–30 applied AI laboratory · "
            "30–38 peer defense · 38–42 synthesis and accuracy lock · 42–50 project transfer"),
}


def srl_table(meetings: list[dict]) -> str:
    slots = []
    for r in meetings:
        raw = (r.get("srl_slot") or "").strip()
        if not raw:
            continue
        m = re.search(r"slot\s*(\d+)", raw, re.I)
        if not m:
            raise SystemExit(f"✗ unparseable srl_slot on meeting {r['meeting']}: {raw!r}")
        slots.append((int(m.group(1)), r))
    slots.sort()

    lines = ["| Slot | Meeting | Lecture date | Prep script due | Week | Studio "
             "| Lecture | Frame |",
             "|---|---|---|---|---|---|---|---|"]
    for slot, r in slots:
        week, studio = week_of(r["unit"])
        d = dt.date.fromisoformat(r["date"])
        # Two days ahead (D18), but never ON a day the course does not meet:
        # two slots would otherwise fall due on Labor Day and October Break.
        pd_ = d - dt.timedelta(days=2)
        while pd_.weekday() not in (0, 2, 4) or pd_.isoformat() in CLOSED:
            pd_ -= dt.timedelta(days=1)
        prep = pd_.strftime("%a %b %-d")
        name, _ = FRAME[r["day"]]
        title = re.sub(r"\s+", " ", r["title"]).strip()
        lines.append(
            f"| **{slot:02d}** | {r['meeting']} | {pretty(r['date'], r['day'])} "
            f"| {prep} | {week} | {studio} | {title} | {name} |")

    puzzles = ["\n---\n\n## The seed puzzle for each slot\n"]
    for slot, r in slots:
        focus = re.sub(r"\s+", " ", (r.get("srl_focus") or "").strip())
        puzzles.append(f"**Slot {slot:02d}** · {pretty(r['date'], r['day'])} · "
                       f"{re.sub(r'\\s+', ' ', r['title']).strip()}\n\n> {focus}\n")

    head = f"""# Student Research Lead — Slot Schedule

*Generated by `scripts/build_participation_schedules.py`. Do not hand-edit.*

**{len(slots)} leadable lectures**, every Monday and Wednesday from Week 2 onward.
Week 1's two lectures are instructor-led to model the format. Slots are drawn
**randomly at the start of the semester**, with no rotation and no seats (D22).

**This table carries no names.** The draw is FERPA-protected student data: it is
made by `scripts/assign_srl_slots.py` and written only into the gitignored
`_adm/roster/`, and the per-lead messages come from `scripts/build_srl_packet.py`.
What is safe to keep here is the slot structure, which is also the part that
survives into the next edition.

**What each lead owes.** A preparation script or notebook **two days before** the
lecture (the "Prep script due" column), prepared from one week ahead. The student
instructions are the SRL handout PDFs in `_handouts/srl/`, built by
`scripts/build_handout_pdfs.py`; those carry no names and no dates, so they upload
to Brightspace once and stay correct.

**Weight.** Student Research Lead Performance is **20%** of the course grade.
The rubric is `project/srl/srl_rubric.md`.

---

## The slots

"""
    return head + "\n".join(lines) + "\n" + "\n".join(puzzles)


def main() -> None:
    check = "--check" in sys.argv
    meetings = rows()
    outputs = [(READING_OUT, reading_table(meetings)),
               (SRL_OUT, srl_table(meetings))]
    stale = []
    for path, content in outputs:
        if check:
            if not path.exists() or path.read_text() != content:
                stale.append(path.name)
            continue
        path.write_text(content)
        n = content.count("\n| ")
        print(f"  ✓ {path.relative_to(REPO)} ({n} rows)")
    if check:
        if stale:
            print("✗ stale: " + ", ".join(stale))
            sys.exit(1)
        print("✓ participation schedules up to date")


if __name__ == "__main__":
    main()
