#!/usr/bin/env python3
"""build_participation_schedules.py — the completion-contract assignment tables.

All three are DERIVED, never hand-written, so they cannot drift from the calendar:

  planning/IYT_SUBMISSION_SCHEDULE.md            (D57; recategorized D58)
      The book "It is your turn" (IYT) submissions. One row per EDR|AI chapter,
      due on the date that chapter's reading was due, plus the grouped list of
      Brightspace assignments to create and the ONE instruction paragraph that
      serves every one of them. Graded by completion inside IYT Practice (15%),
      its own category since D58 took the family out of Participation.

  planning/STUDIO_FEEDBACK_SCHEDULE.md           (D57; replaces the per-chapter
      READING_FEEDBACK_SCHEDULE.md)
      One row per Studio: which chapters it covers and when its feedback survey
      closes. Feedback is now collected ONCE PER STUDIO, closing the Sunday that
      ends the studio week — right before the next studio starts.

  planning/SRL_ASSIGNMENT_SCHEDULE.md
      One row per Student Research Lead slot: which lecture it is, which frame
      it runs, when the filled notebook is due, and the seed puzzle.

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
import math
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from session_readings import lesson_index, parse  # noqa: E402

SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.CSV"
if not SCHEDULE.exists():
    SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.csv"
IYT_OUT = REPO / "planning" / "IYT_SUBMISSION_SCHEDULE.md"
STUDIO_OUT = REPO / "planning" / "STUDIO_FEEDBACK_SCHEDULE.md"
SRL_OUT = REPO / "planning" / "SRL_ASSIGNMENT_SCHEDULE.md"

sys.path.insert(0, str(REPO / "scripts"))
from validate_calendar import no_class_days  # noqa: E402

CLOSED = set(no_class_days())

def _studio_overrides() -> dict[int, dt.date]:
    """Studio -> hand-set close date, from course_config.yaml (D66).

    The course platform is authoritative for due dates. Where a studio's
    computed Sunday is not the date students actually see there, the config
    carries the real one and it wins.
    """
    import yaml
    cfg = yaml.safe_load((REPO / "course_config.yaml").read_text())
    raw = (cfg["participation"]["items"]["studio_feedback"].get("overrides")
           or {})
    return {int(k): dt.date.fromisoformat(v) for k, v in raw.items()}


SITE = ("https://davi-moreira.github.io/"
        "2026F_evidence_driven_research_purdue_HONR464")
COLAB = ("https://colab.research.google.com/github/davi-moreira/"
         "2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/book")

#: How a lesson's anchoring mode maps onto who owes the submission.
#: `route` / `route-contrast` lessons are read by every student, but only two
#: of the five apply to any one student: their own declared route plus the
#: contrast the instructor assigns them.
REQUIREMENT = {
    "first-read": "Everyone",
    "assigned": "Everyone",
    "route": "Pathway — only if this is YOUR declared route",
    "optional": "Only if your design has stages",
}

#: The order roles are listed when one due date carries more than one.
ROLE_RANK = {"Everyone": 0, "Pathway — only if this is YOUR declared route": 1,
             "Only if your design has stages": 2}

#: A due date's assignment title, when the whole group is one non-Everyone role.
ROLE_TITLE = {
    "Pathway — only if this is YOUR declared route": "your declared route",
}


def rows() -> list[dict]:
    with SCHEDULE.open(newline="") as fh:
        return list(csv.DictReader(fh))


def pretty(iso: str, day: str) -> str:
    return f"{day} {dt.date.fromisoformat(iso).strftime('%b %-d')}"


def long_date(d: dt.date) -> str:
    return d.strftime("%a %b %-d, %Y")


def week_of(unit: str) -> tuple[str, str]:
    m = re.match(r"Week (\d+) — (.+)$", unit)
    return (f"{m.group(1)}", m.group(2)) if m else ("", unit)


#: `assigned` means "handed out today, read it for the NEXT session", so it
#: opens the window but never closes it. The closing session is the first one
#: where the chapter is actually required to have been read.
READ_MODES = ("first-read", "route", "route-contrast", "optional")

#: Modes that produce a COLLECTED "It is your turn" submission. `route-contrast`
#: is deliberately absent (D60): the contrast route is still required reading and
#: still drives Wednesday's jigsaw and the milestone's mandated-contrast section,
#: but only the student's OWN declared route hands in an "It is your turn"
#: section. Reading a second pathway to argue against it is not the same act as
#: building your project's pathway, and only the second one is a submission.
SUBMITTED_MODES = ("first-read", "route", "optional", "assigned")


def submissions(meetings: list[dict]) -> list[tuple[int, str, str]]:
    """Every "It is your turn" submission event: (meeting, lesson id, mode).

    One per (lesson, ROLE), not one per lesson — but since D60 only ONE pathway
    role is collected, every lesson now yields exactly one event. A pathway
    chapter produces its event on the Monday its declared-route readers are due;
    the Wednesday contrast reading is required but never handed in. Any one
    student owes exactly one of the five pathway chapters.
    """
    events: list[tuple[int, str, str]] = []
    taken: set[tuple[str, str]] = set()
    assigned_at: dict[str, int] = {}
    for r in meetings:
        n = int(r["meeting"])
        for lid, mode in parse(r["book_reading"]):
            if mode == "assigned":
                assigned_at.setdefault(lid, n)
                continue
            if mode not in SUBMITTED_MODES or (lid, mode) in taken:
                continue
            taken.add((lid, mode))
            events.append((n, lid, mode))
    covered = {lid for _, lid, _ in events}
    for lid, n in assigned_at.items():
        if lid not in covered:
            events.append((n, lid, "assigned"))
            covered.add(lid)
    missing = [l for l in lesson_index() if l not in covered]
    if missing:
        raise SystemExit(f"✗ no anchor session for: {missing}")
    return sorted(events, key=lambda e: (e[0], e[1]))


def anchors(meetings: list[dict]) -> dict[str, int]:
    """lesson id -> the FIRST meeting where it is required (studio grouping)."""
    first: dict[str, int] = {}
    for n, lid, _ in submissions(meetings):
        first.setdefault(lid, n)
    return first


# ---------------------------------------------------------------------------
# 1. the "It is your turn" submissions

#: AUTHORED BY DAVI, 2026-08-23. This is his wording, recorded verbatim: it is
#: what students read on every "It is your turn" assignment. Do not reword it,
#: do not add paragraphs to it, and do not soften it to match a generated page.
#: Three things about it are deliberate and were his call, not an omission:
#:   * ONE SUBMISSION PER CHAPTER, not one per assignment. An assignment that
#:     names four chapters collects four files, hence `ch<nn>` and not a range.
#:   * Upload only. The Colab share link is not offered.
#:   * No "when it is due" paragraph. Brightspace already shows the date on the
#:     assignment, and the deadline rule lives in surveys/participation_grading.md.
IYT_INSTRUCTION = """\
**What this assignment collects.** Submit the completed **"It is your turn"** \
section of every EDR|AI chapter named in this assignment's title. Open the \
chapter from the EDR|AI book, work its "It is your turn" section in that \
chapter's companion Colab notebook (use the badge at the top of the chapter, \
then **File → Save a copy in Drive** so the copy is yours), or work it inside \
your own project notebook if you would rather keep everything in one place.

**What to hand in.** One submission per chapter, covering all required \
chapters. Either upload the notebook (**File → Download → Download .ipynb**) or \
a PDF of it (**File → Print → Save as PDF**). Name the file \
`LASTNAME_iyt_ch<nn>.ipynb`. Answer in your own words, keep every question in \
order, and add an AI Research Ledger row for anything you delegated to an AI \
tool.

**How it is graded.** Completion only: submitted, complete, and on time, or \
not. Your answers are never graded right or wrong here, and nothing you write \
in them can lower another grade."""


STUDIO_FEEDBACK_INSTRUCTION = """\
**What this is.** Once per studio you tell the author of EDR|AI what the reading \
actually did for you. It takes about three minutes, and the link is the same one \
all semester: **[PASTE THE QUALTRICS SURVEY LINK HERE]**. Pick this studio on the \
first page, and answer from the reading rather than from class.

**What to do.** One response per studio. Sign it with your Purdue username: it \
carries participation credit, so it cannot be anonymous. Answer the six short \
questions, then the one open question, which asks you to name a chapter and a \
specific place inside it. Two exact sentences beat two vague paragraphs.

**How it is graded.** On whether you submitted a real, specific response on time, \
never on what you said. A careful complaint and a careful compliment earn exactly \
the same credit, and the complaint is the more useful of the two. Your ratings and \
your comments never affect any other grade. The book is still being written, and \
what you flag here is what gets rewritten.

**When it is due.** 11:59 PM on the Sunday that closes the studio week, which is \
the night before the next studio starts and, in most weeks, the same night that \
studio's milestone is due. Three studios sit on a different date because the calendar \
moved: Studio 2 closes Tuesday, September 8, after the Labor Day weekend; Studio 7 \
keeps its Sunday while its milestone moves past October Break; and Studio 12 closes \
Friday, December 11, with the course reflection. The course platform carries the date \
for every one of them. A response up to seven days late earns half credit; after that it earns \
none. Your lowest few participation credits are dropped automatically, so a bad \
week does not need an email."""


def chapter_range(nums: list[int]) -> str:
    """[2,3,4,5] -> '2-5'; [2,3,5] -> '2-3, 5'."""
    nums = sorted(nums)
    out, start, prev = [], nums[0], nums[0]
    for n in nums[1:] + [None]:
        if n == prev + 1:
            prev = n
            continue
        out.append(f"{start}" if start == prev
                   else (f"{start}, {prev}" if prev == start + 1
                         else f"{start}-{prev}"))
        if n is None:
            break
        start = prev = n
    return ", ".join(out)


def iyt_page(meetings: list[dict]) -> str:
    index = lesson_index()
    events = submissions(meetings)
    by_meeting = {int(r["meeting"]): r for r in meetings}

    counts = {"Everyone": 0, "route": 0, "conditional": 0}
    detail = [
        "| # | Chapter | Title | Due (11:59 PM) | Week · Studio | Who owes it "
        "| Companion notebook |",
        "|---|---|---|---|---|---|---|",
    ]
    groups: dict[int, list] = {}
    for seq, (n, lid, mode) in enumerate(events, start=1):
        lesson = index[lid]
        r = by_meeting[n]
        d = dt.date.fromisoformat(r["date"])
        week, studio = week_of(r["unit"].replace('"', ""))
        req = REQUIREMENT[mode]
        if req == "Everyone":
            counts["Everyone"] += 1
        elif req.startswith("Pathway"):
            counts["route"] += 1
        else:
            counts["conditional"] += 1
        groups.setdefault(n, []).append((lesson, req))
        detail.append(
            f"| {seq} | Ch. {lesson['display']} "
            f"| [{lesson['title']}]({SITE}/book/{lesson['url_path']}) "
            f"| {long_date(d)} | {week} · {studio.split(':')[0]} | {req} "
            f"| [open]({COLAB}/{lesson['companion']}) |")

    build = [
        "| Brightspace assignment name | Due (11:59 PM) | Chapters collected "
        "| Who owes it |",
        "|---|---|---|---|",
    ]
    for n in sorted(groups):
        r = by_meeting[n]
        d = dt.date.fromisoformat(r["date"])
        nums = [l["display"] for l, _ in groups[n]]
        reqs = sorted({req for _, req in groups[n]},
                      key=lambda t: ROLE_RANK.get(t, 9))
        who = " · ".join(reqs)
        titles = {ROLE_TITLE[q] for q in reqs if q in ROLE_TITLE}
        suffix = f" ({titles.pop()})" if len(titles) == 1 else ""
        build.append(f"| It is your turn — Ch. {chapter_range(nums)}{suffix} "
                     f"| {long_date(d)} | {chapter_range(nums)} | {who} |")

    per_student = counts["Everyone"] + 1
    drops = math.ceil(0.10 * per_student)
    head = f"""# "It is your turn" — the IYT Practice submissions

*Generated by `scripts/build_participation_schedules.py`. Do not hand-edit.*

Every chapter of **EDR\\|AI** that a student is required to read carries one
submission: that chapter's closing **"It is your turn"** section. It is graded
**by completion** inside **IYT Practice (15%)** — submitted or not — and it is
due on **the date the chapter's reading was due**, so the section is written
from the reading rather than reconstructed from class.

A typical student owes **{per_student}** of them, and the **{drops} lowest
credits are dropped automatically** (⌈0.10 × N⌉), so {per_student - drops} valid,
on-time submissions earn the full 15 points. The scoring rule and the rest of the
IYT Practice contract are in
[`surveys/participation_grading.md`](../surveys/participation_grading.md).

**How many submissions each student owes**

| | Chapters | Note |
|---|---|---|
| Required of everyone | {counts['Everyone']} | one per chapter |
| Pathway submissions | {counts['route']} | one per pathway chapter, all due Mon Sep 21. Each student owes exactly **1**: their own declared route. The instructor-assigned contrast is still required reading, and it is still worked in Wednesday's jigsaw and in the milestone's mandated-contrast section, but its "It is your turn" section is not collected (D60) |
| Conditional | {counts['conditional']} | binds only if the design has stages |
| **Baseline per student** | **{per_student}** | {counts['Everyone']} + 1 pathway |

---

## 1. The instruction — one paragraph block, every assignment

Paste this into every "It is your turn" assignment on the course page. It is
written to be correct for all of them, so nothing has to be edited per
assignment except the title and the due date.

<!-- iyt-instruction:begin -->
{IYT_INSTRUCTION}
<!-- iyt-instruction:end -->

**Studio 5 collects one pathway chapter per student.** Add one line to its
assignment: *"Submit only your own declared route's chapter. If your design has
stages, also submit Ch. 19, Hybrid and Complex Designs. The other pathway
chapters, including the contrast route assigned to you, are required reading and
jigsaw material for Wednesday, and their sections are not collected."*

---

## 2. The assignments to create ({len(groups)})

One assignment per due date, each collecting the chapters that share it. This is
the shortest build that still keeps every deadline honest.

"""
    detail_head = f"""

---

## 3. Every submission, one row ({len(events)})

"""
    return (head + "\n".join(build) + detail_head + "\n".join(detail) + "\n")


# ---------------------------------------------------------------------------
# 2. studio feedback

def studio_table(meetings: list[dict]) -> str:
    index = lesson_index()
    first = anchors(meetings)
    chapters_at: dict[int, list] = {}
    for lesson in index.values():
        chapters_at.setdefault(first[lesson["id"]], []).append(lesson)

    studios: dict[int, dict] = {}
    for r in meetings:
        m = re.match(r"Week (\d+) — (Studio (\d+): .+)$", r["unit"].replace('"', ""))
        if not m:
            continue
        k = int(m.group(3))
        s = studios.setdefault(k, {"title": m.group(2), "week": int(m.group(1)),
                                   "dates": [], "meetings": []})
        s["dates"].append(dt.date.fromisoformat(r["date"]))
        s["meetings"].append(int(r["meeting"]))

    last_class = max(dt.date.fromisoformat(r["date"]) for r in meetings)
    overrides = _studio_overrides()
    order = sorted(studios)
    lines = ["| Studio | Week | Studio meetings | Chapters it covers "
             "| Survey closes (11:59 PM) |", "|---|---|---|---|---|"]
    for k in order:
        s = studios[k]
        end = max(s["dates"])
        close = end + dt.timedelta(days=(6 - end.weekday()) % 7 or 7)
        note = ""
        if close > last_class:
            close = last_class
            note = " *(the term ends first, so this one closes with the course "
            note += "reflection on the last day of class)*"
        if k in overrides:
            close = overrides[k]
            note = (" *(Labor Day weekend, so this one runs to the night "
                    "before Studio 3 opens)*")
        nums = sorted(l["display"] for n in s["meetings"]
                      for l in chapters_at.get(n, []))
        covers = f"Ch. {chapter_range(nums)}" if nums else "—"
        span = f"{s['dates'][0].strftime('%b %-d')}–{end.strftime('%b %-d')}"
        lines.append(f"| **{k}** · {s['title'].split(': ',1)[1]} | {s['week']} "
                     f"| {span} | {covers} | **{long_date(close)}**{note} |")

    head = f"""# Studio Feedback Schedule — EDR\\|AI

*Generated by `scripts/build_participation_schedules.py`. Do not hand-edit.*

Feedback on the book is collected **once per Studio**, not once per chapter
(D57). One Qualtrics survey serves all {len(order)} of them; the student picks
the studio on the first question, so the course page carries **one link** all
semester and the export is **one file** with a `studio` column. The instrument
and its Qualtrics import file live in [`surveys/`](../surveys/).

**When it closes.** The **Sunday that ends the studio week, 11:59 PM** — the
night before the next studio starts. In most weeks that is also when the
studio's milestone is due (D55), so one deadline closes the whole week: submit
the milestone, then say what the reading did for you while it is still fresh.
Two weeks break the pattern because the calendar does, the Labor Day and
October Break weeks, and the table below carries the real dates.

**Grading.** Graded inside **Participation (9%)**, for completion and
seriousness, never for praise. A careful complaint and a careful compliment earn
exactly the same credit. They are {len(order)} of Participation's
{len(order) + 2} credits; the student profile survey and the course reflection
are the other two. The rule and the drop allowance are in
[`surveys/participation_grading.md`](../surveys/participation_grading.md).

---

## The instruction — one block, every studio

Paste this beside the survey link on the course page. It is written to be correct
for all twelve, so nothing has to be edited per studio.

<!-- studio-feedback-instruction:begin -->
{STUDIO_FEEDBACK_INSTRUCTION}
<!-- studio-feedback-instruction:end -->

---

## The schedule

"""
    return head + "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# 3. SRL slots

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

    lines = ["| Slot | Meeting | Lecture date | Notebook due | Week | Studio "
             "| Lecture | Frame |",
             "|---|---|---|---|---|---|---|---|"]
    for slot, r in slots:
        week, studio = week_of(r["unit"])
        d = dt.date.fromisoformat(r["date"])
        # 11:59 PM the CALENDAR DAY BEFORE the lecture (D66, adopted from the
        # course-platform dates and superseding D18's two days). No class-day
        # snapping: this is a submission time, not a meeting, so a Sunday or a
        # holiday is a perfectly good due date.
        prep = (d - dt.timedelta(days=1)).strftime("%a %b %-d")
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

**What each lead owes.** Their lecture's notebook, filled in and with its
**🎤 My Lead Plan** cell complete, submitted **the day before** the lecture
(the "Notebook due" column), by 11:59 PM, and prepared from one week ahead. The student
instructions are the SRL handout PDFs in `project/srl/`, built by
`scripts/build_handout_pdfs.py`; those carry no names and no dates, so they upload
to Brightspace once and stay correct.

**Weight.** Student Research Lead is **25%** of the course grade.
The rubric is `project/srl/srl_rubric.md`.

---

## The slots

"""
    return head + "\n".join(lines) + "\n" + "\n".join(puzzles)


def main() -> None:
    check = "--check" in sys.argv
    meetings = rows()
    outputs = [(IYT_OUT, iyt_page(meetings)),
               (STUDIO_OUT, studio_table(meetings)),
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
