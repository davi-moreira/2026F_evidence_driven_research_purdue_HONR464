#!/usr/bin/env python3
"""build_participation_schedules.py — the completion-contract assignment tables.

All four are DERIVED, never hand-written, so they cannot drift from the calendar:

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

  planning/LECTURE_NOTEBOOK_SCHEDULE.md          (D74)
      The weekly lecture-notebook submissions. One row per notebook nb01-nb16,
      due 11:59 PM on the Sunday that ends its studio week (Week 16 closes on
      the last day of class instead, because the term ends first), plus the
      assignments to create and the ONE instruction paragraph that serves every
      one of them. Graded by completion inside Lecture Notebooks (20%), the
      category D74 opened when it retired the Student Research Lead grade.
      Every number in its header comes from course_config.yaml's
      `lecture_notebooks:` block; every date comes from the meeting calendar.

  planning/SRL_ASSIGNMENT_SCHEDULE.md            (the lab meeting, D74; the
      draw WITHDRAWN by D75)
      One row per lab-meeting slot: which lecture it is, which frame it runs,
      which weekly notebook carries it, and the puzzle that opens the
      instructor-led block.

      D74 retired the Student Research Lead ROLE and kept the draw. The same 25
      slots now name each lecture's REPORTER, who spends seven minutes on a
      decision from their own project and three on the room's questions; the
      reporter does not teach the concept, and the report is not graded. The
      filename stays as it is: D74 deletes nothing, and the Brightspace kit
      points at this path.

      D75 WITHDREW THE ASSIGNMENT ENTIRELY. There is no draw, no designated
      reporter on any lecture, no assigned question or request, and nothing to
      prepare before class. The ten-minute opening block stays as an OPEN ROUND
      the instructor runs: the instructor asks the room how the projects are
      going, and the room answers. Nothing said in it is graded. This page and
      this generator are KEPT — D75 deletes nothing — and the page now opens
      with a banner saying so, with the slot table below preserved only as the
      record of the withdrawn draw. The per-slot puzzles stay live: each still
      opens its lecture's instructor-led investigation block.

      NO STUDENT NAMES. The draw itself is FERPA-protected student data and
      lives only in the gitignored `_adm/roster/` (scripts/assign_srl_slots.py,
      scripts/build_srl_packet.py — both KEPT under D74 Ruling 5). This table is
      the slot structure, which is the part that is safe to keep in the
      repository and reuse.

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
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from notebooks_map import NOTEBOOKS, colab_url, nb_of, session_kind  # noqa: E402
from session_readings import lesson_index, parse  # noqa: E402

SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.CSV"
if not SCHEDULE.exists():
    SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.csv"
IYT_OUT = REPO / "planning" / "IYT_SUBMISSION_SCHEDULE.md"
STUDIO_OUT = REPO / "planning" / "STUDIO_FEEDBACK_SCHEDULE.md"
LECTURE_NB_OUT = REPO / "planning" / "LECTURE_NOTEBOOK_SCHEDULE.md"
SRL_OUT = REPO / "planning" / "SRL_ASSIGNMENT_SCHEDULE.md"

sys.path.insert(0, str(REPO / "scripts"))
from validate_calendar import no_class_days  # noqa: E402

CLOSED = set(no_class_days())

@lru_cache(maxsize=1)
def _config() -> dict:
    """course_config.yaml — the machine record behind every contract here."""
    import yaml
    return yaml.safe_load((REPO / "course_config.yaml").read_text())


def _studio_overrides() -> dict[int, dt.date]:
    """Studio -> hand-set close date, from course_config.yaml (D66).

    The course platform is authoritative for due dates. Where a studio's
    computed Sunday is not the date students actually see there, the config
    carries the real one and it wins.
    """
    raw = (_config()["participation"]["items"]["studio_feedback"]
           .get("overrides") or {})
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
a PDF of it (**File → Print → Save as PDF**). If you hand in the PDF, run \
**Runtime → Run all** and expand every collapsed section first: printing \
captures what is on the screen, so an unrun or folded cell arrives empty. Name \
the file `LASTNAME_iyt_ch<nn>.ipynb`. Answer in your own words, keep every \
question in order, and add an AI Research Ledger row for anything you delegated \
to an AI tool.

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
# 3. the weekly lecture notebooks (D74)

#: The one instruction block every weekly lecture-notebook assignment carries.
#: Built deliberately like IYT_INSTRUCTION above — what the assignment collects,
#: what to hand in, how it is graded, and nothing else — because the two are read
#: by the same person in the same week and should not sound like two courses.
#: Written TO the student. It names no date and no drop count: the course
#: platform carries the date, and the contract's numbers live in the header of
#: the generated page and in course_config.yaml, so they cannot drift from here.
LECTURE_NOTEBOOK_INSTRUCTION = """\
**What this assignment collects.** Your week's lecture notebook — the same \
`nbNN` you opened in class, with your own work in it: the in-class moves, the \
exercises you worked, and one **📒 AI Research Ledger** row for each lecture. \
Open the notebook from its badge on the course website, then \
**File → Save a copy in Drive** so the copy is yours, and finish whatever class \
left open before you hand it in.

**What to hand in.** One notebook per week. Either upload the notebook \
(**File → Download → Download .ipynb**) or a PDF of it (**File → Print → Save as \
PDF**). If you hand in the PDF, run **Runtime → Run all** and expand every \
collapsed section first: printing captures what is on the screen, so an unrun or \
folded cell arrives empty. Name the file `LASTNAME_nb<nn>`, keeping whichever \
extension the file you uploaded actually has. Answer in your \
own words, keep every question in order, and add a ledger row for anything you \
delegated to an AI tool.

**How it is graded.** Completion only: worked through, handed in, and on time, or \
not. Your answers are never graded right or wrong here, and nothing you say in \
the lab meeting that opens class enters this grade. A notebook \
up to seven days late earns half credit; after that it earns none. Your lowest \
few lecture-notebook credits are dropped automatically, so one bad week does not \
need an email."""


def _lecture_notebook_overrides() -> dict[int, dt.date]:
    """nb number -> hand-set due date, from course_config.yaml (D66).

    Same rule as the studio survey: where the course platform shows a date the
    Sunday rule does not produce, the platform is right and the config carries
    it. None are set today, and the key is read rather than assumed so that
    setting one never requires touching this generator.
    """
    block = _config()["lecture_notebooks"]
    raw = ((block.get("items", {}).get("weekly_lecture_notebook", {}) or {})
           .get("overrides") or block.get("overrides") or {})
    return {int(k): dt.date.fromisoformat(v) for k, v in raw.items()}


def notebook_submissions(meetings: list[dict]) -> list[dict]:
    """One record per weekly notebook, nb01-nb16, with its sessions and due date.

    Which notebook a meeting belongs to is read from the schedule's
    `other_material` column — the same nbNN token the badge updater, the session
    guides and the validators key off — so this table cannot drift from the
    calendar. The due date is the Sunday that ends the notebook's own week,
    capped at the last day of class, which is what makes Week 16 close on the
    Friday instead (D74).
    """
    per: dict[int, list[dict]] = {}
    for r in meetings:
        n = nb_of(r.get("other_material") or "")
        if n is None:
            raise SystemExit(
                f"✗ meeting {r['meeting']} names no nbNN in other_material")
        if n not in NOTEBOOKS:
            raise SystemExit(
                f"✗ meeting {r['meeting']} names unknown notebook nb{n:02d}")
        per.setdefault(n, []).append(r)
    absent = [f"nb{n:02d}" for n in NOTEBOOKS if n not in per]
    if absent:
        raise SystemExit(f"✗ no meeting carries: {', '.join(absent)}")

    last_class = max(dt.date.fromisoformat(r["date"]) for r in meetings)
    overrides = _lecture_notebook_overrides()
    records = []
    for n in sorted(per):
        rs = sorted(per[n], key=lambda r: r["date"])
        end = max(dt.date.fromisoformat(r["date"]) for r in rs)
        due = end + dt.timedelta(days=(6 - end.weekday()) % 7 or 7)
        note = ""
        if due > last_class:
            due = last_class
            note = (" *(the term ends first, so this one closes on the last day "
                    "of class)*")
        if n in overrides:
            due = overrides[n]
            note = " *(the course platform carries this date, and it wins)*"
        weeks = sorted({int(w) for w, _ in
                        (week_of(r["unit"].replace('"', "")) for r in rs) if w})
        _, unit = week_of(rs[-1]["unit"].replace('"', ""))
        worked = [r for r in rs if session_kind(r) != "studio"]
        records.append({
            "nb": n,
            "file": f"{NOTEBOOKS[n][0]}_student.ipynb",
            "title": NOTEBOOKS[n][1],
            "week": (f"{weeks[0]}–{weeks[-1]}" if len(weeks) > 1
                     else (str(weeks[0]) if weeks else "—")),
            "unit": unit.split(":")[0],
            "due": due,
            "note": note,
            "worked": " · ".join(pretty(r["date"], r["day"]) for r in worked),
        })
    return records


def lecture_notebook_page(meetings: list[dict]) -> str:
    cfg = _config()
    block = cfg["lecture_notebooks"]
    item = block["items"]["weekly_lecture_notebook"]
    weight = float(cfg["assessment"]["lecture_notebooks"])
    records = notebook_submissions(meetings)

    baseline = int(block["baseline_credits"])
    if baseline != len(records) or int(item["count"]) != len(records):
        raise SystemExit(
            f"✗ course_config.yaml says {baseline} weekly notebooks "
            f"(items.count {item['count']}), the calendar carries "
            f"{len(records)}")
    drops = math.ceil(0.10 * baseline)
    kept = baseline - drops

    build = ["| Brightspace assignment name | Due (11:59 PM) | Notebook file "
             "| Worked in class |", "|---|---|---|---|"]
    detail = ["| # | Notebook | What it covers | Due (11:59 PM) | Week · Studio "
              "| Worked in class | Open |", "|---|---|---|---|---|---|---|"]
    for rec in records:
        n = rec["nb"]
        build.append(
            f"| Lecture notebook — Week {rec['week']} · nb{n:02d} "
            f"| {long_date(rec['due'])}{rec['note']} | `{rec['file']}` "
            f"| {rec['worked']} |")
        detail.append(
            f"| {n} | nb{n:02d} | {rec['title']} | {long_date(rec['due'])} "
            f"| {rec['week']} · {rec['unit']} | {rec['worked']} "
            f"| [open]({colab_url(n)}) |")

    head = f"""# Lecture notebooks — the weekly submissions

*Generated by `scripts/build_participation_schedules.py`. Do not hand-edit.*

Every week's notebook is collected. You work `nbNN` in class, you finish whatever
the room left open, and you hand that same notebook in once: **11:59 PM on the
Sunday that ends the studio week**. Week 16 is the one exception, and the
calendar forces it — the term ends first, so the last notebook closes on the last
day of class.

It is graded **by completion** inside **Lecture Notebooks ({weight:g}%)**: worked
through and handed in, or not. Nothing in it is scored right or wrong, and nothing
you say in the ten-minute lab meeting that opens class ever reaches this grade,
because nothing in that round is graded at all (D74, D75).

There are **{baseline}** of them and the **{drops} lowest credits are dropped
automatically** (⌈0.10 × N⌉), so {kept} valid, on-time submissions earn the full
{weight:g} points:

> `lecture notebook points = {weight:.1f} × (sum of the highest {kept} credits) / {kept}`

Credit is **1.0** on time, **0.5** within seven days of the deadline, and **0**
otherwise — the same credit rule Participation and IYT Practice use. Lecture
Notebooks is still its own undivided category: it is **not** participation, and
participation's ±0.9 contribution adjustment never touches it.

The machine record is the `lecture_notebooks:` block of
[`course_config.yaml`](../course_config.yaml), and the ruling that opened the
category is D74 in
[`_project_docs/DECISIONS.md`](../_project_docs/DECISIONS.md).

---

## 1. The instruction — one paragraph block, every assignment

Paste this into every weekly lecture-notebook assignment on the course page. It
is written to be correct for all {baseline}, so nothing has to be edited per
assignment except the title and the due date.

<!-- lecture-notebook-instruction:begin -->
{LECTURE_NOTEBOOK_INSTRUCTION}
<!-- lecture-notebook-instruction:end -->

---

## 2. The assignments to create ({baseline})

One assignment per week, each collecting that week's notebook.

"""
    detail_head = f"""

---

## 3. Every submission, one row ({baseline})

"""
    return (head + "\n".join(build) + detail_head + "\n".join(detail) + "\n")


# ---------------------------------------------------------------------------
# 4. lab-meeting slots (D74; the draw and the reporter withdrawn by D75)

#: The fifty-minute frames, restated by D74 and untouched by D75. Both still sum
#: to 50, and section boundaries 3 and 4 are untouched (31–43 / 43–50 Monday,
#: 30–42 / 42–50 Wednesday), so D22's and D34's later-block rulings stand. What
#: changed is the opener: the lab meeting takes the first ten minutes, and the
#: 🧩 Research Puzzle folds into the front of the investigation block, run by
#: the instructor. D75 changed only WHO speaks in those ten minutes — no one is
#: assigned, and the instructor runs an open round with the whole room.
FRAME = {
    "Mon": ("Monday · guided investigation",
            "0–10 lab meeting: the instructor's open round · "
            "10–31 guided AI investigation (instructor, opening on the puzzle) · "
            "31–43 verification and formalization · 43–50 decision and defense"),
    "Wed": ("Wednesday · applied AI laboratory",
            "0–10 lab meeting: the instructor's open round · "
            "10–30 applied AI laboratory · 30–38 peer defense · "
            "38–42 synthesis and accuracy lock · 42–50 project transfer"),
}


def lab_meeting_table(meetings: list[dict]) -> str:
    """The slot schedule (written to SRL_OUT, whose name is kept).

    D74 retired the Student Research Lead ROLE and kept everything else: the
    same 25 Monday/Wednesday slots, drawn the same way, now name each lecture's
    REPORTER. The `srl_slot` / `srl_focus` columns of the calendar are read
    unchanged, because the draw carried over unchanged.

    D75 then withdrew the assignment: no slot is given to anyone, so this page
    is emitted with a banner saying so and the table below it stands as the
    record of the withdrawn draw. The function, the file and the calendar
    columns are all KEPT — D75 deletes nothing — and the per-slot puzzles are
    still live, because each opens its lecture's instructor-led block.
    """
    # D75: the calendar column no longer carries a drawn slot number, because
    # there is no draw. Any non-empty value simply marks a lecture that opens
    # with a lab meeting. A legacy "slot NN" value is still honoured so that a
    # future edition can reinstate the draw without touching this function.
    slots = []
    for r in meetings:
        raw = (r.get("srl_slot") or "").strip()
        if not raw:
            continue
        m = re.search(r"slot\s*(\d+)", raw, re.I)
        slots.append((int(m.group(1)) if m else len(slots) + 1, r))
    slots.sort(key=lambda t: int(t[1]["meeting"]))

    # The notebook that carries each lecture, and the Sunday it is handed in.
    # Until D74 this column held a PREPARATION deadline — the filled notebook
    # 11:59 PM the calendar day before the lecture (D66). D74 dropped that
    # deadline, and D75 dropped preparation altogether: nobody prepares anything
    # for the lab meeting, and the notebook is collected weekly like every other.
    due_of = {rec["nb"]: rec["due"] for rec in notebook_submissions(meetings)}

    lines = ["| # | Meeting | Lecture date | Notebook · due (11:59 PM) "
             "| Week | Studio | Lecture | Frame |",
             "|---|---|---|---|---|---|---|---|"]
    for slot, r in slots:
        week, studio = week_of(r["unit"])
        n = nb_of(r.get("other_material") or "")
        if n is None:
            raise SystemExit(
                f"✗ meeting {r['meeting']} names no nbNN in other_material")
        nb = f"nb{n:02d} · {long_date(due_of[n])}"
        name, _ = FRAME[r["day"]]
        title = re.sub(r"\s+", " ", r["title"]).strip()
        lines.append(
            f"| **{slot:02d}** | {r['meeting']} | {pretty(r['date'], r['day'])} "
            f"| {nb} | {week} | {studio} | {title} | {name} |")

    puzzles = ["\n---\n\n## The puzzle for each lecture — still live\n",
               "Kept in full, and re-owned. This section is the one part of the "
               "page D75 did not withdraw. Each puzzle below opens the "
               "instructor-led investigation block that follows the lab "
               "meeting; the ten minutes before it are the open round, which "
               "has no script, no assigned speaker and no preparation.\n"]
    for slot, r in slots:
        focus = re.sub(r"\s+", " ", (r.get("srl_focus") or "").strip())
        title = re.sub(r"\s+", " ", r["title"]).strip()
        puzzles.append(f"**Slot {slot:02d}** · {pretty(r['date'], r['day'])} · "
                       f"{title}\n\n> {focus}\n")

    weight = _config()["assessment"]["lecture_notebooks"]
    head = f"""# Lab Meeting — Slot Schedule *(the draw is withdrawn)*

*Generated by `scripts/build_participation_schedules.py`. Do not hand-edit.*

> **⚠️ D75 withdrew the slot draw. Nobody is assigned to any lecture.**
>
> The ten-minute lab meeting that opens every Monday and Wednesday lecture
> **stays**. The assignment behind it does not. For this edition there is **no
> draw**, **no designated reporter on any lecture**, **no assigned question or
> request**, and **no preparation of any kind before class**, by anyone. The
> **📣 My Report Plan** cell has been removed from every notebook.
>
> **What the ten minutes are now.** The instructor asks the room how the projects
> are going, and the room answers: what you decided since last time, what your
> evidence looks like, where you are stuck. From minute 10 the instructor leads
> the lesson, exactly as D74 already ruled. **Nothing said in the lab meeting is
> graded.**
>
> **Everything below this banner is preserved only as the record of the withdrawn
> draw** — the slot structure, the frames, and the notebook column — because D75
> deletes nothing and the structure is worth reusing in a future edition. Read it
> as history, not as an assignment. The one exception is the puzzle list at the
> end: those are still live, and each still opens its lecture's instructor-led
> block.

---

## The withdrawn draw, kept as a record

**{len(slots)} lab meetings**, one opening every Monday and Wednesday lecture from
Week 2 onward. Week 1's two lectures carry no reporter, because the format is
modeled there first. Slots were drawn **randomly at the start of the semester**,
with no rotation and no seats (D22), and **D74 carried that draw over unchanged**:
the same {len(slots)} slots named each lecture's **reporter** rather than its
lead, and there was no re-draw. **D75 then withdrew the assignment entirely**, so
no slot in the table below is given to anyone.

**What the ten minutes were, under D74.** The reporter spent **seven minutes** on
one decision from **their own project** and the evidence behind it, then took
**three minutes** of questions from the room. The reporter did not teach the
lecture's concept, and the report was **not graded**. The instructor led from
minute 10 and owned accuracy, the AI tooling and the clock (D74). **D75 kept the
instructor's half of that and dropped the reporter's:** the same ten minutes are
now an open round with nobody assigned to it.

**This table carries no names.** The draw is FERPA-protected student data: it was
made by `scripts/assign_srl_slots.py` and written only into the gitignored
`_adm/roster/`, and the per-slot messages come from
`scripts/build_srl_packet.py`. Both scripts and the drawn roster are **kept on
disk and unapplied** (D75, like D74 before it, deletes nothing). What is safe to
keep here is the slot structure, which is also the part that survives into the
next edition.

**What everyone owes — nothing, since D75.** You prepare nothing for the lab
meeting and submit nothing the night before; you arrive ready to say how your
project is going. Your week's notebook is still handed in **once a week**, on the
Sunday that ends the studio week. Dates are in
[`LECTURE_NOTEBOOK_SCHEDULE.md`](LECTURE_NOTEBOOK_SCHEDULE.md), and the "Notebook
· due" column below repeats the one that covers each slot. What D74 asked for, and
D75 withdrew, was this: *"You fill in the 📣 My Report Plan cell of that week's
notebook before class — lines 1–4 when the lab meeting is yours, line 5 when it is
not, so the whole room arrives with a question."* That cell no longer exists in
any notebook.

**Weight.** The lab meeting carries **none**. D74 retired the **25% Student
Research Lead** category and opened **Lecture Notebooks ({weight}%)** in its
place, graded by completion. The SRL suite in `project/srl/` — the handbook, the
rubric, the Socratic question bank, the AI integration guide, the prep template,
the peer feedback form and both protocols, with the handout PDFs
`scripts/build_handout_pdfs.py` builds from them — is **kept on disk for a future
edition and is not applied to this one** (D74 Ruling 5 and D75, neither of which
deletes anything). The per-lecture questions guide is kept in full and re-owned to
the instructor.

---

## The slots *(the withdrawn draw)*

"""
    return head + "\n".join(lines) + "\n" + "\n".join(puzzles)


def main() -> None:
    check = "--check" in sys.argv
    meetings = rows()
    outputs = [(IYT_OUT, iyt_page(meetings)),
               (STUDIO_OUT, studio_table(meetings)),
               (LECTURE_NB_OUT, lecture_notebook_page(meetings)),
               (SRL_OUT, lab_meeting_table(meetings))]
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
