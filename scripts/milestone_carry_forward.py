#!/usr/bin/env python3
"""milestone_carry_forward.py — the carry-forward record, authored ONCE (D82).

From M4 on, every course milestone opens with a CARRY-FORWARD RECORD: the
student's answer to everything the instructor asked since the last milestone.
It has two parts, and both are personal to each student:

  * every numbered request (`IR-MNN-##`) from the review of the last milestone,
    sent in the mentoring email and the Brightspace feedback (D80), and
  * every step the student's research action plan sets for this milestone.

THE PDF RULE (instructor ruling, 2026-09-25). The milestone PDF does NOT detail
what the requests or the plan ask for; they differ per student and live in the
email and the plan. The PDF says, at the very top, only that the record comes
first, what it holds, and how to answer each item. The same block opens every
brief, so a student meets the rule first on every surface.

Authored once here and projected onto four surfaces, so they cannot disagree:

  * scripts/build_handout_pdfs.py      opens every milestone PDF from M4 on
  * scripts/build_milestone_anchors.py injects it into every brief from M4 on,
                                        inside the marker pair below
  * scripts/update_schedule_badges.py  marks M4 onward with the plus sign
    (through milestone_map.marked_on_schedule) and prints the legend below
  * scripts/build_station_pages.py     opens every milestone workbook from
                                        Milestone 4 on with a book-neutral cell

CONSTRAINTS (enforced by build_handout_pdfs.py's scanner): no em dashes, no
calendar dates, no clock times, no semester labels. Written TO the student, in
the instructor's own mentoring voice, never about "students".
"""
from __future__ import annotations

#: The first course milestone that opens with the record. D80 made M4 the first
#: milestone graded on numbered review requests; the action plan is issued with
#: the M2 review, so by M4 both parts exist for every student.
FIRST = 4

BEGIN = "<!-- carry-forward-start:begin -->"
END = "<!-- carry-forward-start:end -->"

#: The rubric row every milestone from M4 on carries (see D82).
ROW_NAME = "Carry-forward: your action plan's steps"
ROW_POINTS = 10


def applies(num: int | str) -> bool:
    """True when course milestone `num` opens with the carry-forward record."""
    return int(num) >= FIRST


def _ir(num: int) -> str:
    return f"`IR-M{num:02d}-01`"


def _record_item(num: int) -> str:
    return (
        "**Your carry-forward record, at the very top.** This is where you "
        "answer me. It holds two things you already have: every numbered "
        "request from my review of your last milestone (in my email and your "
        f"Brightspace feedback, each with an ID like {_ir(num)}), and every "
        "step your research action plan sets for this milestone (use the "
        "latest version I sent you). Next to each one, write **Done** and "
        "where I can find it, or **Not adopted**, with your reason and what "
        "you did instead."
    )


def _scoring(num: int) -> str:
    return (
        "**How it is scored.** The course rubric on Brightspace scores this "
        "milestone. It already includes the book's own checks, plus two "
        "things for the course: your action-plan steps are one row of the "
        "rubric, and each numbered request left unanswered costs 5 points, "
        "up to 20. If I sent you no numbered requests, say so in one line and "
        "move on. Not sure whether something applies to you? Ask me before "
        "the deadline; that is exactly what I am here for."
    )


def pdf_block(num: int, *, file_lead: str, has_additions: bool) -> str:
    """The "Start here" opening of a milestone PDF from M4 on.

    `file_lead` is the builder's own sentence naming the file to hand in.
    """
    items = [_record_item(num),
             "**Your milestone work**, as the book milestone below describes it."]
    if has_additions:
        items.append("**The Expo work** in *What this course adds*, below.")
    listed = "\n".join(f"{i}. {t}" for i, t in enumerate(items, 1))
    return "\n".join([
        "## Start here",
        "",
        f"{file_lead} Build it in this order:",
        "",
        listed,
        "",
        "When a request, a plan step and the book work ask for the same thing, "
        "do it once and point to it from your record.",
        "",
        _scoring(num),
        "",
    ])


def brief_block(num: int, *, ir_component: int | None,
                plan_component: int | None) -> str:
    """The same opening, for the top of a milestone brief (M4 on)."""
    where = []
    if ir_component:
        where.append(f"Component {ir_component} shows the request table")
    if plan_component:
        where.append(f"Component {plan_component} the plan section")
    layout = (" " + " and ".join(where) + ".") if where else ""
    return "\n".join([
        BEGIN,
        "> **Start here: what this milestone collects from you.**",
        ">",
        f"> 1. {_record_item(num)}{layout}",
        "> 2. **Your milestone work**, as the components below describe it.",
        ">",
        "> When a request, a plan step and a component ask for the same thing, "
        "do it once and point to it from your record.",
        ">",
        f"> {_scoring(num)}",
        END,
    ])


#: Schedule legend (Milestone column), under the table.
SCHEDULE_LEGEND = (
    "A **{plus}** means that the milestone asks for something beyond its book "
    "milestone. From M4 on, that always includes your **carry-forward "
    "record**: your answer to the numbered requests in my review email and "
    "to the steps your action plan sets for that milestone. Some milestones "
    "also carry Expo work. The first page of the milestone's handout on "
    "Brightspace tells you exactly what goes in."
)

#: Book-neutral opening cell for milestone workbooks from Milestone 4 on. The
#: book is institution-agnostic, so it speaks of "whoever reviewed your last
#: version" rather than of a course, an instructor or a grade.
WORKBOOK_HEAD = (
    "## Answer your last review first\n\n"
    "If someone reviewed your last milestone version (a mentor, an "
    "instructor, a peer reviewer) and asked you for specific changes, or "
    "gave you a plan with steps for this milestone, answer them here before "
    "anything else. A researcher who responds to review item by item keeps "
    "control of the project; one who responds in general loses track of "
    "what was asked.\n\n"
    "For each item: **Done**, and where the change is; or **Not adopted**, "
    "with your reason and what you did instead. A reasoned refusal is a "
    "decision. A silent one is drift.\n"
)
WORKBOOK_CELL = (
    "✍️ **Your response to review.** Double-click and fill one row per "
    "item. If nobody reviewed your last version, write \"No review to "
    "answer\" and move on.\n\n"
    "| ID or plan step | What was asked | Done or Not adopted | Where it is, "
    "or your reason and what you did instead |\n"
    "|---|---|---|---|\n"
    "|  |  |  |  |\n"
)
