#!/usr/bin/env python3
"""Build the lab-meeting distribution packet for the semester. WITHDRAWN by D75.

WITHDRAWN BY D75 (2026-08-31), KEPT ON DISK
-------------------------------------------
D74 made ONE assigned student the reporter at every Mon/Wed lab meeting, and
this script told each of them so. D75 withdraws that assignment entirely. The
ten-minute opening block stays; the assignment does not. NO student is
designated, on any lecture, ever. There is no draw, no assigned question or
request, and no preparation of any kind before class by anybody. The instructor
asks the room how the projects are going and the room answers, and from minute
10 the instructor leads the lesson. Nothing said in the lab meeting is graded.

With nobody assigned there is no packet to distribute, so this script does not
run. `PACKET_ENABLED = False` below is the guard and `main()` stops on it.

**Whatever this script wrote before is now STALE AND RETIRED**: the slot briefs
under `_adm/roster/srl_packet/`, the per-student summaries beside them, and the
class announcement at `_announcements/03_srl_slots_and_logistics.md` all name
slots nobody holds, dates nobody is bound by, and a 📣 My Report Plan cell that
D75 removed from every notebook. Those files are kept on file, exactly as D58
kept the quiz banks, and none of them may be sent to anybody.

Every generator below is KEPT unchanged for a future edition that wants assigned
reporters back: set `PACKET_ENABLED = True` here, re-enable the draw in
`scripts/assign_srl_slots.py`, and reword the generated prose, which still
describes the withdrawn D74 arrangement.

The rest of this docstring describes the packet as it stood under D74, preserved
for that future edition.

`assign_srl_slots.py` draws who reports at which lecture. This script turns that
draw into the things Davi actually sends: one class announcement, one reporter
message per slot, and one summary per student.

D74 (2026-08-31) retired the Student Research Lead role and its 25% grade
category and opened every Mon/Wed lecture with a ten-minute LAB MEETING instead.
One student is that lecture's reporter: seven minutes on a decision from their
OWN project and the evidence behind it, then three minutes of questions from the
room. The reporter does not teach the lecture's concept, and the report is NOT
graded. The instructor leads from minute 10 and owns accuracy, the AI tooling
and the clock. What IS graded is the lecture notebook every student works in
class and submits weekly on completion (Lecture Notebooks, 20%).

This script, the draw it reads and the whole `project/srl/` suite are KEPT for a
future edition under D74's ruling that nothing is deleted; the file names keep
their `srl_` stem because the assignment already on disk is the one that carries
over, unchanged and never re-drawn.

FERPA: the assignment carries student names and emails, so it lives in the
gitignored `_adm/roster/` and everything written here goes back into
`_adm/roster/srl_packet/`. This script itself carries no student data; it
reads the draw at run time. Nothing here may be committed or published on the
course site -- the class announcement is for the course platform only.

Each slot message is assembled from the machine spine, never hand-written:
  * date, day, week and lecture title      <- the assignment CSV
  * the format and its minute frame        <- day (D22/D34/D74 Mon/Wed frames)
  * required reading, linked               <- `book_reading` via session_readings
  * the notebook and its Colab link        <- `other_material` via notebooks_map
  * the instructor's opening puzzle        <- `srl_focus`
  * the day the report plan is ready       <- the assignment CSV

Usage:
    .venv/bin/python scripts/build_srl_packet.py
    .venv/bin/python scripts/build_srl_packet.py --slot 1        # one slot
    .venv/bin/python scripts/build_srl_packet.py --dry-run
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
import textwrap
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import notebooks_map as nbmap          # noqa: E402
import session_readings as readings    # noqa: E402

ASSIGNMENT = ROOT / "_adm" / "roster" / "2026F_HONR46400_srl_assignment.csv"
SCHEDULE = ROOT / "planning" / "MEETING_SCHEDULE.csv"
OUT = ROOT / "_adm" / "roster" / "srl_packet"

SITE = "https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464"
SRL_DIR = f"https://github.com/{nbmap.REPO_SLUG}/tree/main/project/srl"

#: D75 (2026-08-31) withdrew the reporter assignment, so there is nobody to send
#: a packet to. This flag is the guard and `main()` stops on it, so a run can
#: never quietly refresh an announcement that names slots no student holds.
#: Everything below is kept working and unchanged for a future edition that
#: wants assigned reporters back: set this to True, turn the draw back on in
#: `scripts/assign_srl_slots.py`, and reword the D74 prose the builders emit.
PACKET_ENABLED = False


def srl_file(name: str) -> str:
    return f"https://github.com/{nbmap.REPO_SLUG}/blob/main/project/srl/{name}"


# The two D74 frames (D22/D34 boundaries 3 and 4 untouched), in the words the
# notebooks use. Both still sum to 50: Monday 10/21/12/7, Wednesday 10/20/12/8,
# with the Wednesday third block still split 30-38 / 38-42 as D34 set it. The
# lab meeting takes the opener; everything from minute 10 is the instructor's.
# The minute frames are unchanged by D75 and remain correct. What is stale is
# the "yours" wording in the 0-10 row and every reporter sentence built from it:
# D75 withdrew the assignment, so those ten minutes belong to the whole room and
# to nobody in particular. Kept verbatim, unreachable while PACKET_ENABLED is
# False, and to be reworded by any edition that turns the packet back on.
FRAMES = {
    "Mon": {
        "name": "Monday — the guided investigation",
        "rows": [
            ("0–10", "Lab meeting",
             "yours: seven minutes on a decision from your own project, then "
             "three minutes of questions from the room"),
            ("10–31", "Guided AI research-partner investigation",
             "the instructor's block: the research puzzle opens it, then the "
             "room directs the AI together"),
            ("31–43", "Human verification and formalization",
             "the instructor's block: the room checks what came back and the "
             "idea is formalized"),
            ("43–50", "Decision and defense",
             "the room closes: one committed decision defended aloud, then the "
             "ledger row and the Claim Ticket"),
        ],
        "owned": "**0–10**",
    },
    "Wed": {
        "name": "Wednesday — the applied AI laboratory",
        "rows": [
            ("0–10", "Lab meeting",
             "yours: seven minutes on a decision from your own project, then "
             "three minutes of questions from the room"),
            ("10–30", "Applied AI laboratory",
             "the instructor's block: hands-on prompting, split roles, hunting "
             "AI-failure patterns"),
            ("30–38", "Peer defense",
             "everybody's block: adversarial questions, and answers that stay "
             "honest about what the evidence supports"),
            ("38–42", "Synthesis and accuracy lock",
             "the instructor states the room's conclusion and its uncertainty, "
             "and locks accuracy"),
            ("42–50", "Transfer to projects",
             "the room closes: connect the skill to your own project, then the "
             "ledger row and the Claim Ticket"),
        ],
        "owned": "**0–10**",
    },
}


def slugify(name: str) -> str:
    n = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", n.lower()).strip("_")


def pretty(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return d.strftime("%A, %B %-d, %Y")


def short(iso: str) -> str:
    return dt.date.fromisoformat(iso).strftime("%a %b %-d")


def load_assignment() -> list[dict]:
    if not ASSIGNMENT.exists():
        raise SystemExit(
            f"assignment not found: {ASSIGNMENT}\n"
            "Run scripts/assign_srl_slots.py first. FERPA: never move this "
            "file out of _adm/."
        )
    with ASSIGNMENT.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    return sorted(rows, key=lambda r: int(r["slot"]))


def load_meetings() -> dict[int, dict]:
    with SCHEDULE.open(newline="") as fh:
        return {int(r["meeting"]): r for r in csv.DictReader(fh)}


#: Reading lead-ins, reworded for a message that arrives a week ahead of the
#: lecture rather than on the schedule page for the day itself.
MODE_LEAD = {
    "first-read": "**Required before the lecture you open:**",
    "assigned": "**Assigned at that lecture, for the session after:**",
    "continue": "**Still in play from Monday:**",
    "revisit": "**Revisit:**",
    "route": "**Required — everyone reads their own declared route:**",
    "route-contrast": "**Required — everyone reads their assigned contrast route:**",
    "optional": "**Only for students whose design has stages:**",
}


def reading_block(row: dict, index: dict) -> str:
    """The meeting's chapters, one per line, as links a student can click.

    The schedule page's mode wording ("Required before today") is dropped:
    this message arrives a week out, not on the day.
    """
    grouped = readings.by_mode(row["book_reading"])
    blocks = []
    for mode, ids in grouped.items():
        lead = MODE_LEAD.get(mode, readings.MODE_LABEL[mode].strip(" —*"))
        items = "\n".join(
            f"- [Ch. {index[lid]['display']} — {index[lid]['title']}]"
            f"({SITE}/book/{index[lid]['url_path']})"
            for lid in ids if lid in index)
        if items:
            blocks.append(f"{lead}\n\n{items}")
    return "\n\n".join(blocks) if blocks else \
        "_No new required reading for this meeting._"


#: The schedule column that holds the lecture's opening puzzle. It still has its
#: pre-D74 name in the CSV; newer names are accepted so a future schedule build
#: can rename it without breaking this packet.
FOCUS_COLUMNS = ("srl_focus", "lab_meeting_focus", "reporter_focus")


def focus_of(m: dict) -> str:
    """The puzzle the instructor opens the investigation with, if there is one."""
    for name in FOCUS_COLUMNS:
        v = (m.get(name) or "").strip()
        if v:
            return v
    return ""


def build_slot_message(a: dict, m: dict, index: dict, labels: dict) -> str:
    day = a["day"]
    frame = FRAMES[day]
    nb = nbmap.nb_of(m["other_material"])
    colab = (f"https://colab.research.google.com/github/{nbmap.REPO_SLUG}/blob/"
             f"main/notebooks/student/{nbmap.student_filename(nb)}") if nb else ""
    lab = labels.get(int(a["meeting"]))
    lecture_n = f"Lecture {lab[1]}" if lab else "the lecture"
    lecture_of = f"Lecture {lab[1]} of {lab[2]}" if lab else "the lecture"

    compression = ("""
**One thing about drawing the first slot.** Every later reporter gets a full week
between the draw and their lab meeting; you get the short end of Week 1. Bring
whatever your project has actually reached, even if that is one narrowed question
and one source you have checked. A first decision reported plainly is exactly
what these ten minutes are for, and none of it is graded.
""" if int(a["slot"]) == 1 else "")

    frame_rows = "\n".join(
        f"| **{mins}** | {sec} | {what} |" for mins, sec, what in frame["rows"]
    )

    puzzle = focus_of(m)
    puzzle_block = (f"""## What comes after your ten minutes

Once the lab meeting closes, I open the lecture with this:

> {puzzle}

You do not have to prepare it. It is here so you can see where the day goes
after your report.

""" if puzzle else "")

    return f"""# You report at the lab meeting on {short(a['date'])} — slot {int(a['slot']):02d}

**To:** {a['student']} <{a['email'] or 'ADDRESS MISSING FROM THE ROSTER'}>
**Subject:** HONR 46400 — you are the reporter on {short(a['date'])}

---

Hi {a['student'].split()[0]},

You drew **lab meeting slot {int(a['slot']):02d}**: you are the reporter on
**{pretty(a['date'])}**, 1:30–2:20 PM in HCRS-1054.

Ten minutes, right at the top of class. **Seven minutes on one decision your own
project has reached and the evidence behind it**, then **three minutes of
questions from the room**. You are not teaching the day's topic, and the report
carries no grade. I take the room from minute 10.

**The lecture you are opening:** {m['title']}
*({a['unit']} · {lecture_of})*

**The driving question the room has to leave with an answer to:**
> {m['driving_question']}

## The shape of the day: {frame['name']}

| Min | Section | What happens |
|---|---|---|
{frame_rows}

Your ten minutes are {frame['owned']}. After that you are a member of the room
like everybody else.

## What to bring

Open the notebook and read the **📣 Lab Meeting: Today's Reporter** cell at the
top of **{lecture_n}**, then fill in the **📣 My Report Plan** cell under it.
Four lines: the decision you are bringing, the evidence behind it, where it is
still uncertain, and the question you want the room to answer for you.

- **Notebook:** {colab}
- Nothing is emailed to you and nothing is held back from your classmates. Both
  cells are ordinary cells everybody can read.

Bring a real decision rather than a polished result. "I chose this outcome
measure over that one, and here is the check that made me" is a complete report.
So is a decision you are still unsure about, and those usually draw the most
useful questions back.

{puzzle_block}## Read before class

{reading_block(m, index)}

Everybody reads these, reporter or not.

## Your dates

**Have your 📣 My Report Plan cell filled in by {pretty(a['prep_due'])}**, the
day before you report. Nothing is handed in that day. The plan travels inside
the lecture notebook, and **the notebook is submitted at the end of the studio
week** with everybody else's, graded on completion (Lecture Notebooks, 20% of
the course grade). Your course platform carries that deadline.

If you would like me to look at your plan before you report, send it over and I
will send notes back. That is optional, and it is not graded either.
{compression}
## If you have to miss your slot

Tell me as far ahead as you can. Swapping with a classmate's later slot, by
agreement, is the first option, and it is far easier to arrange in advance than
on the morning of.

## Kept on file, not used this edition

The Student Research Lead suite is still in the repository: the role was retired
for this edition, not the material. None of it is assessed this term and none of
it describes your ten minutes, so read it only if you are curious.

- Handbook: {srl_file('srl_handbook.md')}
- How to run the AI moments: {srl_file('srl_ai_integration_guide.md')}
- Question bank: {srl_file('socratic_question_bank.md')}
- Planning worksheet: {srl_file('srl_prep_template.md')}
- The retired lead rubric: {srl_file('srl_rubric.md')}
- The retired peer feedback form: {srl_file('srl_peer_feedback_form.md')}

One line to keep in mind while you plan: **you are not presenting a finding. You
are asking your colleagues for help with a decision.** That is what a lab meeting
is for, and it rehearses exactly the conversation you will have at the Expo.

— Davi
"""


def build_student_summary(name: str, mine: list[dict], meetings: dict) -> str:
    rows = "\n".join(
        f"| {int(a['slot']):02d} | **{pretty(a['date'])}** | "
        f"{FRAMES[a['day']]['name'].split(' — ')[0]} | {short(a['prep_due'])} | "
        f"{meetings[int(a['meeting'])]['title']} |"
        for a in mine
    )
    return f"""# Your lab meeting dates — {name}

You report at **{len(mine)} lab meetings** this semester. The dates were drawn at
random at the start of the term: nothing rotates and nothing shifts, so these are
yours for the whole semester.

Each one is ten minutes at the top of class. Seven minutes on a decision your own
project has reached and the evidence behind it, then three minutes of questions
from the room. You are not teaching the day's topic, and the report is not graded.

| Slot | You report | Format | Plan ready by | The lecture |
|---:|---|---|---|---|
{rows}

**For each one:**

1. A few days ahead, open that lecture's notebook and read the **📣 Lab Meeting:
   Today's Reporter** cell at the top, then read the rest of the notebook and its
   required chapters, as you would for any class.
2. The day before, fill in the **📣 My Report Plan** cell: the decision, the
   evidence behind it, where it is still uncertain, and the question you want the
   room to answer. Nothing is handed in that day. Send it to me if you would like
   notes back.
3. On the day, arrive a few minutes early, open Colab, and have your decision and
   your one question ready to say out loud.

The notebook itself goes in at the end of the studio week with everybody else's,
graded on completion (Lecture Notebooks, 20% of the course grade). Your course
platform carries that deadline.

The Student Research Lead suite is still in the repository, kept for a future
edition rather than deleted: the handbook ({srl_file('srl_handbook.md')}) and the
retired lead rubric ({srl_file('srl_rubric.md')}) are there if you are curious,
but neither is used or assessed this term.

Dates, formats and content for every meeting are on the course Schedule page:
{SITE}/schedule.html
"""


WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}


def wrap(text: str) -> str:
    """Fill to the width the rest of this announcement is written at."""
    return textwrap.fill(text, width=79, break_on_hyphens=False)


def count_sentences(per_student: dict[str, list[str]]) -> tuple[str, str]:
    """The constraint clause and, when counts are uneven, the sentence after it."""
    tally: dict[int, int] = {}
    for dates in per_student.values():
        tally[len(dates)] = tally.get(len(dates), 0) + 1
    if len(tally) == 1:
        n = next(iter(tally))
        return f"everyone reports exactly {WORDS.get(n, n)} times", ""
    parts = [
        f"{'one of you reports' if people == 1 else WORDS.get(people, people) + ' of you report'}"
        f" {WORDS.get(leads, leads)} times"
        for leads, people in sorted(tally.items(), reverse=True)
    ]
    lo, hi = min(tally), max(tally)
    tail = wrap(
        "The lectures do not divide evenly across the class, so "
        + " and ".join(parts)
        + ". Which of you carries the extra one was part of the same random "
        "draw, and it costs you nothing: the report is not graded, so "
        f"{WORDS.get(lo, lo)} turns and {WORDS.get(hi, hi)} turns come to "
        "exactly the same grade."
    )
    return "report counts are as even as the calendar allows", "\n\n" + tail


def build_announcement(rows: list[dict], meetings: dict) -> str:
    """The class-wide slot announcement, as Brightspace-ready Markdown."""
    table = "\n".join(
        f"| {int(a['slot']):02d} | {short(a['date'])} | {a['student']} | "
        f"{meetings[int(a['meeting'])]['title']} |"
        for a in rows
    )
    first = rows[0]
    per_student: dict[str, list[str]] = {}
    for a in rows:
        per_student.setdefault(a["student"], []).append(short(a["date"]))
    bullets = "\n".join(
        f"- **{n}** — {', '.join(per_student[n])}" for n in sorted(per_student)
    )
    counts, counts_tail = count_sentences(per_student)

    # A slot already announced keeps its reporter through a redraw
    # (assign_srl_slots LOCKED). When any slot is frozen, the announcement is a
    # REPOST and has to say so, or students trust dates that moved under them.
    frozen = [a for a in rows if a.get("locked") == "yes"]
    if frozen:
        held = " and ".join(
            f"**{a['student']}** on {short(a['date'])}" for a in frozen
        )
        redraw = wrap(
            "**Please read this even if you saw an earlier draw — the dates "
            "have changed.** The class list moved after I posted that draw, so "
            "I ran the whole thing again across everybody who is enrolled now. "
            f"The one thing I would not move is Week 2: {held} keep their "
            "dates, because they are already preparing them. **Every other "
            "slot is new**, so check your dates below rather than trusting the "
            "ones you wrote down."
        ) + "\n\n"
    else:
        redraw = ""
    opener = (
        "Here is the draw again, and this one is final."
        if frozen
        else "The draw is done, so you now know exactly which lab meetings are "
        "yours for the whole semester."
    )
    intro = wrap(
        f"{opener} Have a look below, put your dates in your calendar, and "
        "then read the rest of this so the ten minutes are not a mystery."
    )
    constraints = wrap(
        f"The {len(rows)} lectures that carry a lab meeting were drawn **at "
        f"random**, with a reproducible seed and four fairness constraints: "
        f"{counts}, nobody reports twice in a row, nobody reports at both lab "
        "meetings of the same week, and everybody reports in both halves of "
        "the semester. Nothing rotates and nothing shifts, so these are your "
        "dates for the term."
    )
    heading = (
        "# Your lab meeting dates — the new draw"
        if frozen
        else "# Your lab meeting dates are drawn"
    )
    posting = wrap(
        "*REPOST. This replaces the slot announcement already on Brightspace. "
        "Post it as a NEW announcement rather than editing the old one, so "
        "everybody gets the notification. Paste the body below (everything "
        "under the rule) into the announcement editor. Generated by "
        "`scripts/build_srl_packet.py` — do not hand-edit; fix the generator "
        "instead.*"
        if frozen
        else "*Post on Brightspace in Week 1, after the draw. Paste the body "
        "below (everything under the rule) into the announcement editor. "
        "Generated by `scripts/build_srl_packet.py` — do not hand-edit; fix "
        "the generator instead.*"
    )
    return f"""{heading}

{posting}

🚨 **FERPA — student names. Course platform only, never the public site.**

---

Hello everyone,

{redraw}{intro}

From Week 2 on, every Monday and Wednesday lecture opens with a **ten-minute lab
meeting**, run the way a research group runs one. One of you is that day's
**reporter**: seven minutes on a decision your own project has reached and the
evidence behind it, then three minutes of questions from the rest of us. You are
not teaching the day's topic, you are not presenting a finished result, and the
report is **not graded**. I take the room from minute 10 and run the lecture.

There was a larger role here before, with a grade attached, and I retired it.
Reporting on your own project is the one thing you are already the expert in the
room on, and it rehearses the exact conversation you will have at the Expo in
November. What is graded instead is the notebook we work in class:

| Part of your grade | Weight |
|---|---:|
| Attendance | 1% |
| Participation | 9% |
| "It is your turn" practice | 15% |
| **Lecture notebooks** | **20%** |
| Final project | 55% |
| **Total** | **100%** |

**Lecture notebooks (20%)** works like the other completion contracts in this
course. One notebook a week, the one we work in class, submitted at the end of
that studio week and graded on **completion only**: worked through and handed
in. Never on whether your answers came out right, and never on how your ten
minutes went. The two lowest weeks drop automatically, and your course platform
carries every deadline.

{constraints}{counts_tail}

## Your dates

{bullets}

## The full draw

| Slot | Date | Reporter | The lecture |
|---:|---|---|---|
{table}

## What your ten minutes actually look like

You are **not lecturing**. You are not summarizing a reading and you are not
walking us through slides. You bring one decision your project has reached since
the last lab meeting, say what the evidence behind it is, say where it is still
shaky, and ask us the question you most want answered.

That is it. Seven minutes for the report, three for our questions. Nobody in the
room knows your project better than you do, so there is no answer here you can
get wrong.

A good report sounds like: "I chose this outcome measure over that one, here is
the check that made me, and I am still not sure it captures what I care about.
Would you have chosen differently?" A decision you are unsure about is a better
report than a tidy one, because it gets you more back.

Both lecture formats run 50 minutes, and the lab meeting is the first ten of
them.

**On a Monday: the guided investigation**

| Minutes | Section |
|---|---|
| 0–10 | Lab meeting: the reporter, then the room's questions |
| 10–31 | Guided AI research-partner investigation |
| 31–43 | Human verification and formalization |
| 43–50 | Decision and defense, ledger row, Claim Ticket |

**On a Wednesday: the applied AI laboratory**

| Minutes | Section |
|---|---|
| 0–10 | Lab meeting: the reporter, then the room's questions |
| 10–30 | Intensive applied AI laboratory |
| 30–38 | Peer defense and adversarial questioning |
| 38–42 | Synthesis, then my accuracy lock |
| 42–50 | Project transfer, ledger row, Claim Ticket |

From minute 10 the lecture is mine. I own accuracy, the AI tooling and the
clock, so you can put your whole preparation into your own ten minutes.

## What is graded, and what is not

**The report is not graded.** There is no rubric for it, no score, and no peer
scoring form. Reporting four times or five times comes to exactly the same
grade.

**The notebook is graded, on completion.** Every week, everyone hands in the
notebook we worked in class, and you get the credit for having worked through it
and handed it in. Not for being right. Two weeks drop automatically, and a
notebook up to seven days late still earns half credit.

The course used to run a graded lead role with a nine-row live rubric. That
rubric still exists in the course repository, kept for a future edition, but it
is **not applied this term** and nothing you do at a lab meeting is scored
against it.

## The logistics of your slot

1. **A few days ahead**, read the 📣 Lab Meeting: Today's Reporter cell at the
   top of that lecture in the notebook, then read the rest of the notebook and
   its required chapters, as you would for any class. Decide which decision from
   your own project you are bringing. One real decision is enough.
2. **The day before**, fill in the 📣 My Report Plan cell in that notebook: the
   decision, the evidence behind it, where it is uncertain, and your question
   for the room. Nothing is handed in that day. Send it to me if you want notes
   back, and I will send them.
3. **On the day**, arrive a few minutes early, open Colab, and have your decision
   and your one question ready to say out loud. And breathe. You are asking
   colleagues for help, not defending a thesis.
4. **If you have to miss a slot**, tell me as far ahead as you can. Swapping with
   a classmate's later slot, by agreement, is the first option, and it is far
   easier to arrange in advance than on the morning of.

## When you are not the reporter

Everybody else has one job at the lab meeting: arrive with a question for
whoever is reporting. Line 5 of the 📣 My Report Plan cell is where you write it
down. Ten minutes of real questions from five colleagues is worth more to a
project than an hour of my notes, and you will want the same when your turn
comes.

## What to do now

1. Put your dates in your calendar, and a reminder **the day before each one** to
   fill in your report plan.
2. Look your dates up on the [Schedule page]({SITE}/schedule.html) to see which
   notebook each one uses and what it covers.

Every lecture already contains its own **📣 Lab Meeting: Today's Reporter** cell
at the top, with what the reporter brings, how the ten minutes run, and what the
rest of the room does. It is visible to everyone, not just to that day's
reporter, and the **📣 My Report Plan** cell sits right under it.

**First up is {first['student']}, on {pretty(first['date'])}.**

Week 1's two lectures are mine, with no lab meeting, so you see the shape of a
lecture before your own first turn.

If you are nervous about your first slot, come talk to me. That is a completely
normal thing to feel, and a ten-minute conversation usually fixes it.

All the best,

Prof. Moreira
"""


def main() -> int:
    if not PACKET_ENABLED:
        print(
            "D75 (2026-08-31) withdrew the lab-meeting reporter assignment, so\n"
            "there is no packet to build.\n"
            "\n"
            "The ten-minute lab meeting still opens every Mon/Wed lecture, but\n"
            "NO student is designated as its reporter, nothing is prepared\n"
            "before class by anybody, and nothing said there is graded: the\n"
            "instructor asks the room how the projects are going and the room\n"
            "answers, and from minute 10 the instructor leads the lesson.\n"
            "\n"
            "Nothing was written. What is already on disk from the last run is\n"
            "STALE AND RETIRED: the slot briefs and per-student summaries under\n"
            "_adm/roster/srl_packet/, and the announcement at\n"
            "_announcements/03_srl_slots_and_logistics.md, name slots nobody\n"
            "holds, dates nobody is bound by, and a report plan cell that no\n"
            "longer exists in any notebook. They are kept on file only. Do not\n"
            "post or send any of them.\n"
            "\n"
            "Every generator is preserved below this guard, unchanged. To build\n"
            "the packet again for a future edition that wants assigned reporters\n"
            "back, set PACKET_ENABLED = True at the top of this file, re-enable\n"
            "the draw in scripts/assign_srl_slots.py, and reword the D74 prose\n"
            "the builders emit."
        )
        return 0

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slot", type=int,
                    help="build only this slot's reporter message")
    ap.add_argument("--dry-run", action="store_true", help="print, do not write")
    args = ap.parse_args()

    rows = load_assignment()
    meetings = load_meetings()
    index = readings.lesson_index()
    labels = nbmap.lecture_labels()

    wanted = [a for a in rows if args.slot is None or int(a["slot"]) == args.slot]
    if not wanted:
        raise SystemExit(f"no slot {args.slot} in the assignment")

    if args.dry_run:
        for a in wanted:
            print(f"slot {int(a['slot']):02d} · {a['date']} · {a['student']} "
                  f"· plan by {a['prep_due']}")
        return 0

    briefs = OUT / "slot_briefs"
    students = OUT / "per_student"
    for d in (briefs, students):
        d.mkdir(parents=True, exist_ok=True)

    written = 0
    for a in wanted:
        m = meetings[int(a["meeting"])]
        p = briefs / f"slot_{int(a['slot']):02d}_{slugify(a['student'])}.md"
        p.write_text(build_slot_message(a, m, index, labels))
        written += 1

    if args.slot is None:
        by_student: dict[str, list[dict]] = {}
        for a in rows:
            by_student.setdefault(a["student"], []).append(a)
        for name, mine in by_student.items():
            (students / f"{slugify(name)}.md").write_text(
                build_student_summary(name, mine, meetings))
        ann = ROOT / "_announcements"
        ann.mkdir(parents=True, exist_ok=True)
        (ann / "03_srl_slots_and_logistics.md").write_text(
            build_announcement(rows, meetings))
        (OUT / "README.md").write_text(f"""# Lab meeting distribution packet

🚨 **FERPA — student data. Never commit, never publish.** Generated by
`scripts/build_srl_packet.py` from the gitignored assignment draw. The class
announcement goes on the **course platform**, never on the course website.

D74 retired the Student Research Lead role and replaced it with the ten-minute
lab meeting; the draw, this packet and every file name keep their `srl_` stem,
because the assignment on disk carries over unchanged and nothing is deleted.

Regenerate after any change to the draw or to `MEETING_SCHEDULE.csv`:

```bash
.venv/bin/python scripts/build_srl_packet.py
```

| File | Where it goes | When |
|---|---|---|
| `../../../_announcements/03_srl_slots_and_logistics.md` | Brightspace announcement | Week 1, once |
| `per_student/*.md` | to each student individually | Week 1, with the announcement |
| `slot_briefs/slot_NN_*.md` | to that reporter, by email | about a week before each slot |

{len(rows)} slots · {len(set(a['student'] for a in rows))} students · first slot
{short(rows[0]['date'])} (report plan ready by {short(rows[0]['prep_due'])}).
""")

    print(f"✓ {written} slot brief(s) written")
    print(f"  {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
