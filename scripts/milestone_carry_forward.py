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
        "**Your carry-forward record, at the very top.** Open my review email "
        "and your research action plan side by side. Answer every numbered "
        f"request for this milestone (each has an ID like {_ir(num)}) and every "
        "step your plan sets for this milestone. Next to each one, write "
        "**Done** and exactly where I can find it, or **Not adopted**, with "
        "your reason and what you chose instead. Several items can point to "
        "the same piece of work."
    )


def _work_item() -> str:
    return (
        "**Then your milestone work and files.** The book milestone below "
        "explains the research work. The complete course checklist, the files "
        "to hand in and the rubric are in this milestone's assignment on "
        "Brightspace: check them before you submit."
    )


def _scoring(num: int) -> str:
    return (
        "**How this counts.** Your answer to the action plan is worth 10 "
        "points of the rubric, scored for you individually. Each numbered "
        "request left unanswered costs 5 points, up to 20. Only requests and "
        "plan steps I sent you at least 48 hours before the deadline count; "
        "anything later moves to the next milestone. A step that is also a "
        "numbered request is counted once, as a request. If I sent you no "
        "numbered requests, or no plan steps apply, say so in one line. Not "
        "sure what applies to you? Write to me before the deadline; that is "
        "exactly what I am here for."
    )


def pdf_block(num: int, *, file_lead: str, has_additions: bool) -> str:
    """The "Start here" opening of a milestone PDF from M4 on.

    It says THAT the record comes first and how to answer each item; it never
    details the requests or the plan, and it points to the Brightspace
    assignment for the complete course checklist rather than claiming the
    book page is everything (Codex review, 2026-09-25).
    """
    items = [_record_item(num), _work_item()]
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
        "> 2. **Then your milestone work and files**, exactly as *What to Submit "
        "on Brightspace* and the components below list them.",
        ">",
        f"> {_scoring(num)}",
        END,
    ])


#: Schedule legend (Milestone column), under the table.
SCHEDULE_LEGEND = (
    "A **{plus}** marks course requirements that come with the book "
    "milestone. From M4 on, that always includes your **carry-forward "
    "record**: your answer to the numbered requests in my review email and "
    "to the steps your action plan sets for that milestone. Some milestones "
    "also carry Expo work. The milestone's assignment on Brightspace has the "
    "complete checklist, the files, the deadline and the rubric."
)

#: Book-neutral opening cell for milestone workbooks from Milestone 4 on. The
#: book is institution-agnostic, so it speaks of "whoever reviewed your last
#: version" rather than of a course, an instructor or a grade.
WORKBOOK_HEAD = (
    "## Answer your last review first\n\n"
    "If someone reviewed your last milestone version (a mentor, an "
    "instructor, a peer reviewer) and asked for specific changes, or gave "
    "you a plan with steps for this milestone, bring each of them into the "
    "table below before anything else. It keeps track of what changed and "
    "why, which is exactly what a reader of your work will want to know.\n\n"
    "For each item, write **Done** and where the change is, or **Not "
    "adopted**, with your reason and what you chose instead. A reasoned "
    "choice not to adopt something is a real decision, and it counts.\n"
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
