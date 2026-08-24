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
import html
import re
import sys
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

**To:** {a['student']} <{a['email']}>
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

**Submit your preparation script or notebook by {pretty(a['prep_due'])}**
(two days before you lead). Use the template:
{srl_file('srl_prep_template.md')}

It asks for the puzzle, the commitment question, three Socratic questions with
the answers you expect (right and wrong), the exact AI prompt or prompts the
class will run with an honest prediction of what the AI will get wrong, your
assumption-probe, your counterexample request, the decision you will make the
room defend, a timing plan, and a fallback if the AI tool is down.

I review it and send you notes. That review is the cheapest place to fix a
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
2. Two days ahead, submit your **preparation script or notebook**
   ({srl_file('srl_prep_template.md')}). I send you notes.
3. On the day, arrive a few minutes early, open Colab, confirm your AI tool
   responds, and have your fallback ready.

Read the handbook once before your first slot: {srl_file('srl_handbook.md')}
You are graded on the rubric: {srl_file('srl_rubric.md')}

Dates, formats and content for every meeting are on the course Schedule page:
{SITE}/schedule.html
"""


def build_announcement(rows: list[dict], meetings: dict) -> str:
    table = "\n".join(
        f"<tr><td>{int(a['slot']):02d}</td><td>{short(a['date'])}</td>"
        f"<td>{html.escape(a['student'])}</td>"
        f"<td>{html.escape(meetings[int(a['meeting'])]['title'])}</td></tr>"
        for a in rows
    )
    first = rows[0]
    per_student: dict[str, list[str]] = {}
    for a in rows:
        per_student.setdefault(a["student"], []).append(short(a["date"]))
    bullets = "\n".join(
        f"<li><strong>{html.escape(n)}</strong> — {', '.join(d)}</li>"
        for n, d in per_student.items()
    )
    return f"""<h2>Your Student Research Lead slots are drawn</h2>

<p>From Week 2 on, <strong>one of you runs each Monday and Wednesday
lecture</strong> as a Socratic investigation — you pose a puzzle, hold the room
to a written commitment before any AI tool opens, direct the AI investigation,
and close on a decision someone defends aloud. That is the Student Research
Lead role, and it is <strong>25% of your grade</strong>.</p>

<p>The {len(rows)} leadable lectures have been drawn <strong>at
random</strong>, with a reproducible seed and four fairness constraints: everyone leads
exactly {len(rows)//len(per_student)} times, nobody leads two lectures in a row,
nobody leads both lectures of the same week, and everybody leads in both halves
of the semester. <strong>Nothing rotates and nothing shifts</strong> — these are
your lectures for the term.</p>

<h3>Your dates</h3>
<ul>
{bullets}
</ul>

<h3>The full draw</h3>
<table border="1" cellpadding="6" cellspacing="0">
<thead><tr><th>Slot</th><th>Date</th><th>Lead</th><th>The lecture</th></tr></thead>
<tbody>
{table}
</tbody>
</table>

<h3>What leading actually looks like</h3>

<p>You are <strong>not presenting</strong>. You are not summarizing a reading or
walking us through slides. You are running a <strong>Socratic investigation</strong>:
you lead by asking, and the room does the reasoning. The single most important
move you make all day is holding everyone to a <em>written commitment before any
AI tool opens</em> — without it, the AI's answer quietly becomes everyone's
answer and nobody learns anything.</p>

<p>Both formats run 50 minutes, and the minute frames are fixed. I post
checkpoint signals at the section boundaries so you always know your pace.</p>

<p><strong>If you drew a Monday — the guided investigation</strong></p>
<table border="1" cellpadding="6" cellspacing="0">
<thead><tr><th>Minutes</th><th>Section</th><th>Whose block</th></tr></thead>
<tbody>
<tr><td>0&ndash;9</td><td>Your research puzzle, committed in writing before any tool opens</td><td><strong>Yours</strong></td></tr>
<tr><td>9&ndash;31</td><td>Guided AI research-partner investigation</td><td><strong>Yours</strong> (I watch accuracy)</td></tr>
<tr><td>31&ndash;43</td><td>Human verification + formalization</td><td>Mine &mdash; hand off cleanly</td></tr>
<tr><td>43&ndash;50</td><td>Decision &amp; defense, ledger row, Claim Ticket</td><td><strong>Yours</strong></td></tr>
</tbody>
</table>

<p><strong>If you drew a Wednesday — the applied AI laboratory</strong></p>
<table border="1" cellpadding="6" cellspacing="0">
<thead><tr><th>Minutes</th><th>Section</th><th>Whose block</th></tr></thead>
<tbody>
<tr><td>0&ndash;7</td><td>Your retrieval &amp; challenge</td><td><strong>Yours</strong></td></tr>
<tr><td>7&ndash;30</td><td>Intensive applied AI laboratory &mdash; the longest block, so pacing is on you</td><td><strong>Yours</strong></td></tr>
<tr><td>30&ndash;38</td><td>Peer defense &amp; adversarial questioning</td><td><strong>You referee</strong></td></tr>
<tr><td>38&ndash;42</td><td>Synthesis, then my accuracy lock</td><td>You synthesize; I lock</td></tr>
<tr><td>42&ndash;50</td><td>Project transfer, ledger row, Claim Ticket</td><td><strong>Yours</strong></td></tr>
</tbody>
</table>

<p>I will step in during your session, and that is by design, not a rescue. If a
conceptual error starts spreading I flag it without taking the room from you; if
the room goes quiet I may seed a cold call; if the AI produces a failure you
missed I will usually ask <em>you</em> to put it to the room rather than answer
it myself.</p>

<h3>How each lead is graded</h3>

<p>You are graded <strong>live</strong>, during the session, on nine rows worth
100 points: conceptual correctness (15), quality of your Socratic questions (15),
exposing an assumption (10), productive use of AI (15), interrogating what the AI
returns (15), including every classmate (10), time management (5), connection to
real research decisions (10), and how you handle wrong or uncertain answers (5).
Each of your five leads is scored on its own, and together they are the 25%.</p>

<p>Two things worth knowing before you plan anything. First, the rubric does
<strong>not</strong> measure whether you knew every answer &mdash; leading an
investigation well while genuinely unsure can score Exemplary, and "I don't know
either, how could we find out?" is a strong move. Second, there is one
<strong>hard cap</strong>: presenting an AI answer as settled without verifying it
in front of the room caps the AI row at Beginning regardless of everything else.
AI may propose; the researcher must verify.</p>

<p>Your classmates fill out a short peer feedback form after each session. Read
it &mdash; it is the fastest way to be better on your next slot.</p>

<h3>The logistics of your slot</h3>
<ol>
<li><strong>About a week ahead</strong> &mdash; read the 🎤 SRL Lead Brief at the
top of that lecture in the notebook, then read the rest of the notebook and its
required chapters as a learner. Decide the one thing <em>you</em> are adding that
the brief does not have.</li>
<li><strong>Two days ahead</strong> &mdash; submit your preparation script or
notebook using the template: the puzzle, the commitment question, three Socratic
questions with the answers you expect (right <em>and</em> wrong), the exact AI
prompts the class will run with an honest prediction of what the AI will get
wrong, your assumption-probe, the decision you will make the room defend, a
timing plan, and a fallback if the tool is down. I review it and send you notes.
That review is the cheapest place to fix a session, so send it on time even if it
is rough.</li>
<li><strong>The day of</strong> &mdash; arrive a few minutes early, open Colab,
confirm your AI tool responds, paste your first prompt into a scratch cell, and
have your fallback ready. A dead tool should never kill your session.</li>
<li><strong>If you have to miss a slot</strong> &mdash; tell me as far ahead as
you can. Swapping with a classmate's later slot, by agreement, is the first
option, and it is much easier to arrange in advance than on the morning.</li>
</ol>

<h3>What to do now</h3>
<ol>
<li>Put your dates in your calendar, along with a <strong>prep deadline two days
before each one</strong>.</li>
<li>Read the <a href="{srl_file('srl_handbook.md')}">SRL Handbook</a> once this
week. It is short, and it is the whole job. Then skim the
<a href="{srl_file('srl_rubric.md')}">rubric</a> and the
<a href="{srl_file('srl_prep_template.md')}">preparation template</a>, so you know
what you are aiming at.</li>
<li>Look your dates up on the
<a href="{SITE}/schedule.html">Schedule page</a> to see which notebook each one
uses and what it covers.</li>
</ol>

<p>Every led lecture already contains its own <strong>🎤 SRL Lead Brief</strong>
at the top of that lecture in the notebook — mission, run of show, three
questions, one AI trap, and the checkpoints. It is visible to everyone, not just
the lead. Treat it as a floor, not a ceiling.</p>

<p><strong>First up: {html.escape(first['student'])} on
{pretty(first['date'])}.</strong> I am sending them their brief separately
today; their preparation script is due {pretty(first['prep_due'])}.</p>

<p>Week 1's two lectures are mine — I run the format so you can see it before
you have to do it.</p>
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
        (OUT / "00_class_announcement.html").write_text(
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
| `00_class_announcement.html` | Brightspace announcement | Week 1, once |
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
