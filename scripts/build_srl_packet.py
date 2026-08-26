#!/usr/bin/env python3
"""Build the Student Research Lead distribution packet for the semester.

`assign_srl_slots.py` draws who leads which lecture. This script turns that
draw into the things Davi actually sends: one class announcement, one lead
message per slot, and one summary per student.

FERPA: the assignment carries student names and emails, so it lives in the
gitignored `_adm/roster/` and everything written here goes back into
`_adm/roster/srl_packet/`. This script itself carries no student data; it
reads the draw at run time. Nothing here may be committed or published on the
course site -- the class announcement is for the course platform only.

Each slot message is assembled from the machine spine, never hand-written:
  * date, day, week and lecture title      <- the assignment CSV
  * the format and its minute frame        <- day (D22/D34 Monday/Wednesday)
  * required reading, linked               <- `book_reading` via session_readings
  * the notebook and its Colab link        <- `other_material` via notebooks_map
  * the seed puzzle                        <- `srl_focus`
  * the prep deadline (lecture minus 2)    <- the assignment CSV

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


def srl_file(name: str) -> str:
    return f"https://github.com/{nbmap.REPO_SLUG}/blob/main/project/srl/{name}"


# The two D22/D34 frames, in the words the handbook uses.
FRAMES = {
    "Mon": {
        "name": "Monday — the guided investigation",
        "rows": [
            ("0–9", "Your research puzzle",
             "you own it: pose the puzzle, take the room's written commitment, "
             "every AI tool closed"),
            ("9–31", "Guided AI investigation",
             "you run it: direct the prompts, compare human against AI, probe "
             "what comes back"),
            ("31–43", "Verification and formalization",
             "the instructor's block: hand off cleanly and keep the thread visible"),
            ("43–50", "Decision and defense",
             "you close: one committed decision defended aloud, then the ledger "
             "row and the Claim Ticket"),
        ],
        "owned": "**0–9** and **9–31**",
    },
    "Wed": {
        "name": "Wednesday — the applied AI laboratory",
        "rows": [
            ("0–7", "Your retrieval challenge",
             "you own it: a challenge that forces recall and exposes a fault line"),
            ("7–30", "Applied AI laboratory",
             "you steer it: hands-on prompting, split roles, hunt AI-failure "
             "patterns; pacing is on you"),
            ("30–38", "Peer defense",
             "you referee: keep the adversarial questions coming and the answers "
             "honest"),
            ("38–42", "Synthesis and accuracy lock",
             "you state the room's conclusion and its uncertainty; the instructor "
             "locks accuracy"),
            ("42–50", "Transfer to projects",
             "you close: connect the skill to each person's project, then the "
             "ledger row and the Claim Ticket"),
        ],
        "owned": "**0–7** and **7–30**",
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
    "first-read": "**Required for your lecture:**",
    "assigned": "**Assigned in your lecture, for the session after:**",
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
**One thing about drawing the first slot.** Every later lead gets a full week
between the draw and their lecture; you get the short end of Week 1. If the
turnaround is tight, send me what you have by the deadline and we will fix the
rest together — a rough script on time beats a polished one late. And you have
the advantage nobody else has: you will have watched me run the exact same
format twice before you do it.
""" if int(a["slot"]) == 1 else "")

    frame_rows = "\n".join(
        f"| **{mins}** | {sec} | {what} |" for mins, sec, what in frame["rows"]
    )

    return f"""# You are leading {short(a['date'])} — SRL slot {int(a['slot']):02d}

**To:** {a['student']} <{a['email'] or 'ADDRESS MISSING FROM THE ROSTER'}>
**Subject:** HONR 46400 — you lead {short(a['date'])}; prep due {short(a['prep_due'])}

---

Hi {a['student'].split()[0]},

You drew **SRL slot {int(a['slot']):02d}**: you run the room on
**{pretty(a['date'])}**, 1:30–2:20 PM in HCRS-1054.

**The lecture:** {m['title']}
*({a['unit']} · {lecture_of})*

**The driving question the room has to leave with an answer to:**
> {m['driving_question']}

## Your format: {frame['name']}

| Min | Section | What you do |
|---|---|---|
{frame_rows}

Your owned blocks are {frame['owned']}. Everything else you either hand off
cleanly or referee.

## Your brief is already written, and it is public

Open the notebook and read the **🎤 SRL Lead Brief** at the top of
**{lecture_n}**. Nothing is emailed to you and nothing is held back from your
classmates — the brief is a normal cell they can read too.

- **Notebook:** {colab}
- It names your mission, the run of show, three questions that keep the room
  thinking, one AI trap to watch for, and the checkpoints that tell you your
  pace is right.

**Treat the brief as a floor, not a ceiling.** The minute frame and the
checkpoints are fixed; the staging is yours. In your prep script, name one
thing you are adding that the brief does not contain.

## Your seed puzzle

> {m['srl_focus']}

Use it, sharpen it, or bring your own — a puzzle works when it has a real
answer, more than one tempting wrong answer, and can be stated in a few
sentences.

## Read before you plan

{reading_block(m, index)}

Read these as a learner first. You cannot lead an investigation into an idea
you have not sat with.

## Your deadline

**Submit your lecture's notebook, filled in, by {pretty(a['prep_due'])}**
(the day before you lead), on Brightspace.

Two things make it complete. Fill the **🎤 My Lead Plan** cell at the top of
your lecture: how you will stage the puzzle, the one thing you are adding, your
commitment question, the decision you will close on, and your fallback if the
AI tool is down. Then work the rest of the notebook as a learner, so you have
sat with every answer the room will reach.

A longer planning worksheet is available if you want one
({srl_file('srl_prep_template.md')}), but it is optional and you do not submit it.

I review the notebook and send you notes. That review is the cheapest place to fix a
session, so send it on time even if it is rough.
{compression}

## The rest of the guide

- **Handbook** (read this first, once): {srl_file('srl_handbook.md')}
- **How to run the AI moments:** {srl_file('srl_ai_integration_guide.md')}
- **Question bank, if you get stuck:** {srl_file('socratic_question_bank.md')}
- **How you are graded:** {srl_file('srl_rubric.md')}
- **What classmates score you on afterwards:** {srl_file('srl_peer_feedback_form.md')}

One line to keep in mind while you plan: **you are not there to present. You
are there to make the room think.** The single most important move is making
everyone commit to an answer in writing *before* any AI tool is opened.

— Davi
"""


def build_student_summary(name: str, mine: list[dict], meetings: dict) -> str:
    rows = "\n".join(
        f"| {int(a['slot']):02d} | **{pretty(a['date'])}** | "
        f"{FRAMES[a['day']]['name'].split(' — ')[0]} | {short(a['prep_due'])} | "
        f"{meetings[int(a['meeting'])]['title']} |"
        for a in mine
    )
    return f"""# Your Student Research Lead slots — {name}

You lead **{len(mine)} lectures** this semester. They were drawn at random at
the start of the term: nothing rotates and nothing shifts, so these are your
lectures for the whole semester.

| Slot | You lead | Format | Prep due | The lecture |
|---:|---|---|---|---|
{rows}

**For each one:**

1. About a week ahead, open that lecture's notebook and read the **🎤 SRL Lead
   Brief** at the top, then read the rest of the notebook and its required
   chapters as a learner.
2. The day before, submit **that notebook, filled in**, with its **🎤 My Lead
   Plan** cell complete. I send you notes on it.
3. On the day, arrive a few minutes early, open Colab, confirm your AI tool
   responds, and have your fallback ready.

Read the handbook once before your first slot: {srl_file('srl_handbook.md')}
You are graded on the rubric: {srl_file('srl_rubric.md')}

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
        return f"everyone leads exactly {WORDS.get(n, n)} times", ""
    parts = [
        f"{'one of you leads' if people == 1 else WORDS.get(people, people) + ' of you lead'}"
        f" {WORDS.get(leads, leads)} times"
        for leads, people in sorted(tally.items(), reverse=True)
    ]
    lo, hi = min(tally), max(tally)
    tail = wrap(
        "The lectures do not divide evenly across the class, so "
        + " and ".join(parts)
        + ". Which of you carries the extra one was part of the same random "
        "draw, and it costs you nothing: leads are averaged, not added up, so "
        f"{WORDS.get(lo, lo)} strong sessions and {WORDS.get(hi, hi)} strong "
        "sessions come to the same grade."
    )
    return "lead counts are as even as the calendar allows", "\n\n" + tail


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

    # A slot already announced keeps its lead through a redraw (assign_srl_slots
    # LOCKED). When any slot is frozen, the announcement is a REPOST and has to
    # say so, or students trust dates that moved under them.
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
            "lectures, because they are already preparing them. **Every other "
            "slot is new**, so check your dates below rather than trusting the "
            "ones you wrote down."
        ) + "\n\n"
    else:
        redraw = ""
    opener = (
        "Here is the draw again, and this one is final."
        if frozen
        else "The draw is done, so you now know exactly which lectures are "
        "yours for the whole semester."
    )
    intro = wrap(
        f"{opener} Have a look below, put your dates in your calendar, and "
        "then read the rest of this so the role itself is not a mystery."
    )
    constraints = wrap(
        f"The {len(rows)} leadable lectures were drawn **at random**, with a "
        f"reproducible seed and four fairness constraints: {counts}, nobody "
        "leads two lectures in a row, nobody leads both lectures of the same "
        "week, and everybody leads in both halves of the semester. Nothing "
        "rotates and nothing shifts, so these are your lectures for the term."
    )
    heading = (
        "# Your Student Research Lead slots — the new draw"
        if frozen
        else "# Your Student Research Lead slots are drawn"
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

From Week 2 on, one of you runs each Monday and Wednesday lecture. You pose a
puzzle, hold the room to a written commitment before any AI tool opens, direct
the AI investigation, and close on a decision that someone defends out loud. That
is the Student Research Lead role, and it is **25% of your grade**.

I want to say something about that number up front, because it looks
intimidating. Leading is the single best way to learn this material, which is why
it carries real weight. It is also the part of the course students tell me they
were most nervous about and ended up enjoying most. You are not being thrown in
cold: every session comes with a brief already written for you, you send me a
plan the day before and I send notes back, and I am in the room the whole time.

{constraints}{counts_tail}

## Your dates

{bullets}

## The full draw

| Slot | Date | Lead | The lecture |
|---:|---|---|---|
{table}

## What leading actually looks like

You are **not presenting**. You are not summarizing a reading and you are not
walking us through slides. You are running a **Socratic investigation**, which
just means you lead by asking rather than telling, and the room does the
reasoning.

The single most important move you make all day is holding everyone to a written
commitment before any AI tool opens. Without it, the AI's answer quietly becomes
everyone's answer and nobody learns anything. If you do only one thing well, do
that one.

Both formats run 50 minutes and the minute frames are fixed. I post checkpoint
signals at the section boundaries, so you will always know your pace without
having to watch the clock yourself.

**If you drew a Monday: the guided investigation**

| Minutes | Section |
|---|---|
| 0–9 | Your research puzzle, committed in writing before any tool opens |
| 9–31 | Guided AI research-partner investigation |
| 31–43 | Human verification and formalization |
| 43–50 | Decision and defense, ledger row, Claim Ticket |

**If you drew a Wednesday: the applied AI laboratory**

| Minutes | Section |
|---|---|
| 0–7 | Your retrieval and challenge |
| 7–30 | Intensive applied AI laboratory, the longest block, so pacing is on you |
| 30–38 | Peer defense and adversarial questioning |
| 38–42 | Synthesis, then my accuracy lock |
| 42–50 | Project transfer, ledger row, Claim Ticket |

I will step in during your session, and I want you to expect it rather than read
it as a rescue.

## How each lead is graded

You are graded live, during the session, on nine rows worth 100 points:
conceptual correctness (15), the quality of your Socratic questions (15),
exposing an assumption (10), productive use of AI (15), interrogating what the AI
returns (15), including every classmate (10), time management (5), connection to
real research decisions (10), and how you handle wrong or uncertain answers (5).
Each of your leads is scored on its own and they are **averaged**, so leading a
different number of times than a classmate changes nothing about your grade.

Two things are worth knowing before you plan anything.

First, and please take this seriously: the rubric does **not** measure whether
you knew every answer. Leading an investigation well while genuinely unsure can
score Exemplary. "I don't know either. How could we find out?" is one of the
strongest moves available to you, not an admission of failure. Uncertainty is the
raw material of research.

Second, there is one hard cap. Presenting an AI answer as settled without
verifying it in front of the room caps the AI row at Beginning, regardless of how
well everything else went. AI may propose; the researcher must verify. That is
the discipline this whole course exists to build, so it has teeth here.

Your classmates fill out a short peer feedback form after each session. Read it.
It is the fastest way to be better on your next slot.

## The logistics of your slot

1. **About a week ahead**, read the 🎤 SRL Lead Brief at the top of that lecture
   in the notebook, then read the rest of the notebook and its required chapters
   as a learner. Then decide the one thing *you* are adding that the brief does
   not have. Your own example, your own staging, your own opening question. One
   thing is enough, and it is what separates a good session from a fine one.
2. **On the day**, arrive a few minutes early, open Colab, confirm your AI tool
   responds, paste your first prompt into a scratch cell, and have your fallback
   ready. A dead tool should never kill your session. And breathe. You are not
   performing, you are hosting a good argument.
3. **If you have to miss a slot**, tell me as far ahead as you can. Swapping with
   a classmate's later slot, by agreement, is the first option, and it is far
   easier to arrange in advance than on the morning of.

## What to do now

1. Put your dates in your calendar, along with a **prep deadline the day before
   each one**.
2. Look your dates up on the [Schedule page]({SITE}/schedule.html) to see which
   notebook each one uses and what it covers.

Every led lecture already contains its own **🎤 SRL Lead Brief** at the top of
that lecture in the notebook, with the mission, the run of show, three questions,
one AI trap, and the checkpoints. It is visible to everyone, not just to the
lead. Treat it as a floor rather than a ceiling. It guarantees your session works
even on a bad week, and the memorable sessions are the ones where the lead adds
something of their own.

**First up is {first['student']}, on {pretty(first['date'])}.**

Week 1's two lectures are mine. I run the format first so you can see it before
you have to do it, and you should feel free to steal anything I do.

If you are nervous about your first slot, come talk to me. That is a completely
normal thing to feel, and a ten-minute conversation usually fixes it.

All the best,

Prof. Moreira
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slot", type=int, help="build only this slot's message")
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
                  f"· prep {a['prep_due']}")
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
        (OUT / "README.md").write_text(f"""# SRL distribution packet

🚨 **FERPA — student data. Never commit, never publish.** Generated by
`scripts/build_srl_packet.py` from the gitignored assignment draw. The class
announcement goes on the **course platform**, never on the course website.

Regenerate after any change to the draw or to `MEETING_SCHEDULE.csv`:

```bash
.venv/bin/python scripts/build_srl_packet.py
```

| File | Where it goes | When |
|---|---|---|
| `../../../_announcements/03_srl_slots_and_logistics.md` | Brightspace announcement | Week 1, once |
| `per_student/*.md` | to each student individually | Week 1, with the announcement |
| `slot_briefs/slot_NN_*.md` | to that lead, by email | about a week before each slot |

{len(rows)} slots · {len(set(a['student'] for a in rows))} students · first slot
{short(rows[0]['date'])} (prep due {short(rows[0]['prep_due'])}).
""")

    print(f"✓ {written} slot brief(s) written")
    print(f"  {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
