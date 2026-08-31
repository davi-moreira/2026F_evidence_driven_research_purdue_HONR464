#!/usr/bin/env python3
"""build_brightspace_kit.py — generate the paste-ready Brightspace build kit.

Brightspace is the delivery surface for a course whose source of truth is this
repository. Rather than hand-authoring 16 units in a web editor (and letting
them drift the first time the schedule changes), this script renders the kit
from the same machine spine everything else derives from:

    course_config.yaml          weights, milestones, calendar, week->studio map
    planning/MEETING_SCHEDULE.csv   43 meetings: dates, titles, readings, prep
    _research_project/2026Fall/     the milestone briefs students submit against

Output lands in `brightspace/` (gitignored): one HTML file per weekly unit,
ready to paste into Brightspace's HTML editor, plus the operational checklists
that only a human with the account can carry out.

Re-run after ANY schedule, milestone, or weight change, then re-paste the units
that changed.

Usage:
    .venv/bin/python scripts/build_brightspace_kit.py
"""
from __future__ import annotations

import csv
import datetime
import html
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import yaml

from validate_calendar import no_class_days


def same_week(iso: str, meetings: list[dict]) -> bool:
    """Does this date fall in the same calendar week as one of these meetings?"""
    wk = datetime.date.fromisoformat(iso).isocalendar()[:2]
    return any(datetime.date.fromisoformat(m["date"]).isocalendar()[:2] == wk
               for m in meetings)

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "course_config.yaml"
SCHEDULE = ROOT / "planning" / "MEETING_SCHEDULE.csv"
BRIEFS = ROOT / "_research_project" / "2026Fall"
QUIZZES = ROOT / "_quizzes" / "2026Fall" / "weekly"
OUT = ROOT / "brightspace"
ANNOUNCEMENTS = ROOT / "_announcements"

REPO = "davi-moreira/2026F_evidence_driven_research_purdue_HONR464"
SITE = f"https://{REPO.split('/')[0]}.github.io/{REPO.split('/')[1]}"
COLAB = f"https://colab.research.google.com/github/{REPO}/blob/main"

DAYNAME = {"Mon": "Monday", "Wed": "Wednesday", "Fri": "Friday"}


# D58 (2026-08-23) retired the quiz GRADE CATEGORY and the Friday class-time
# block, not the material. The banks under _quizzes/, every quiz builder and
# scripts/audit_answer_length.py are KEPT for a future edition, and so are the
# two helpers below: they are deliberately defined and deliberately UNCALLED,
# so re-enabling quizzes is one call site away. Retiring the category is never
# permission to delete a quiz file or a quiz script.
# Side effect to know about: quiz_handouts() was also the only check that every
# active quiz JSON has a rendered handout and that no two declare the same
# course week. With nothing calling it, that validation no longer runs.
def quiz_handouts() -> dict[int, Path]:
    """Return active course week -> generated printed quiz handout.

    Unused since D58; kept for the edition that brings quizzes back."""
    result: dict[int, Path] = {}
    for source in sorted(QUIZZES.glob("*.json")):
        spec = json.loads(source.read_text())
        if not spec.get("active", True):
            continue
        week = spec.get("week")
        if isinstance(week, bool) or not isinstance(week, int):
            raise ValueError(f"{source}: active quiz requires an integer week")
        handout = source.with_name(f"{source.stem}_quiz.md")
        if not handout.exists():
            raise FileNotFoundError(f"active quiz handout missing: {handout}")
        if week in result:
            raise ValueError(f"multiple active quizzes declare course week {week}")
        result[week] = handout
    return result


def n_quizzes() -> int:
    """How many course weeks actually carry a printed quiz.

    Unused since D58; kept alongside quiz_handouts()."""
    return len(quiz_handouts())


# D74 (2026-08-31) retired the Student Research Lead GRADE CATEGORY and the live
# role. Every Mon/Wed lecture now opens with a ten-minute LAB MEETING, and the
# instructor leads from minute 10. The 25% category is replaced by Lecture
# Notebooks (20%), and the 5 points that were freed went to Milestone
# Deliverables inside the Final Project, which rose from 50% to 55%.
#
# D75 (2026-08-31) then withdrew the assignment inside that opening block. The
# ten minutes stay exactly where D74 put them, but nobody is designated to
# report, on any lecture: no slot draw, no assigned question, no preparation of
# any kind by anyone. The instructor asks the room how the projects are going and
# the room answers. Nothing said there is graded, so nothing about it reaches a
# gradebook item, a dropbox or a weight in this kit. What D75 does leave here is
# one administrative consequence: the third Week-1 announcement no longer
# publishes a slot schedule, and if that schedule already went out, the slots
# have to be withdrawn out loud on the platform.
#
# Exactly as D58 did for the quizzes, NOTHING IS DELETED. All of project/srl/,
# scripts/assign_srl_slots.py and scripts/build_srl_packet.py stay on disk for a
# future edition, and so does every SRL string in this file: the category label,
# the two-kinds-of-item gradebook bullet and the two checklist to-dos are all
# preserved verbatim below, simply not emitted. The flag is the whole switch —
# set it True and the SRL category, its 25 slot dropboxes and its checklist
# entries come back exactly as they were. Retiring the category is never
# permission to delete an SRL file, an SRL script or an SRL section.
SRL_CATEGORY_ENABLED = False

# Registered under BOTH spellings of the key on purpose, so that a rename in
# course_config.yaml can never print a raw config key as a category name.
SRL_GRADEBOOK_LABELS = {
    "srl_performance": (
        "Student Research Lead",
        "4 or 5 leads per student (25 slots, 6 students), averaged and "
        "scored on project/srl/srl_rubric.md",
    ),
    "student_research_lead": (
        "Student Research Lead",
        "4 or 5 leads per student (25 slots, 6 students), averaged and "
        "scored on project/srl/srl_rubric.md",
    ),
}

# The gradebook bullet the SRL category used to contribute to "Items inside each
# category". Kept verbatim; emitted only when SRL_CATEGORY_ENABLED is True.
SRL_GRADEBOOK_ITEM_BULLET = (
    "- **Student Research Lead** — two kinds of item, and they are not the "
    "same thing. (a) **One submission item per SRL slot (25 in all)**, each a "
    "dropbox that takes the lead's filled lecture notebook, due 11:59 PM the "
    "day before that lecture; planning/SRL_ASSIGNMENT_SCHEDULE.md is the "
    "dated list, and only the assigned lead submits to each. (b) **One scored "
    "item per student**, entered after each of their leads against "
    "project/srl/srl_rubric.md and averaged; a single item scored four or "
    "five times is simpler than five items for a class of six, and the "
    "average is what makes an uneven lead count harmless. The submission "
    "items carry the deadline; the scored item carries the 25%."
)

# The two checklist entries, in their live SRL form and in the open-round form
# that replaced them. D74 kept the draw and changed only the job on the day; D75
# withdrew the draw itself, so the disabled variants publish no slot schedule at
# all — they say the assignment is withdrawn, and they tell you to say so to
# students if the schedule already went out. The SRL wordings below are kept
# verbatim, and the generated files keep their `srl` names on disk, because
# nothing is deleted or renamed.
SRL_CHECKLIST_ANNOUNCEMENT = (
    "`03_srl_slots_and_logistics.md` (after the draw — generated by\n"
    "      `scripts/build_srl_packet.py`, so fix the generator, never the file; FERPA,\n"
    "      course platform only). Send each student their\n"
    "      `_adm/roster/srl_packet/per_student/*.md` summary alongside the third."
)
LAB_MEETING_CHECKLIST_ANNOUNCEMENT = (
    "a third one that is **not** `03_srl_slots_and_logistics.md` as generated.\n"
    "      `scripts/build_srl_packet.py` wrote that file from a slot draw, and D75\n"
    "      withdrew the draw: **nobody is assigned to report, on any lecture**. So do\n"
    "      not publish it, and do not send the per-student summaries under\n"
    "      `_adm/roster/srl_packet/per_student/`. What the third announcement says\n"
    "      instead is the whole of the new arrangement: every Monday and Wednesday\n"
    "      lecture opens with a ten-minute **lab meeting**, it is an open round — you\n"
    "      ask how the projects are going and whoever has something says it — nothing\n"
    "      is prepared for it beforehand by anyone, and nothing said in it is graded.\n"
    "      The packet files keep their `srl` names on disk because D75 deletes\n"
    "      nothing; they are simply not published this edition."
)
SRL_CHECKLIST_ASSIGNMENT_TODO = (
    "- [ ] **Post the SRL assignment** so each student sees their own dates\n"
    "      (`_adm/roster/2026F_HONR46400_srl_assignment.md`). FERPA: post each\n"
    "      student's slots to that student, or post a slot table by date that names\n"
    "      only the lead for that date — never distribute the roster file itself."
)
LAB_MEETING_CHECKLIST_ASSIGNMENT_TODO = (
    "- [ ] **Post no slot schedule — there is none.** D75 withdrew the D69/D71 draw\n"
    "      for this edition, so no student holds a lab-meeting date and no student\n"
    "      prepares anything for one. `_adm/roster/2026F_HONR46400_srl_assignment.md`\n"
    "      keeps its name and stays on disk, unpublished; nothing in\n"
    "      `_adm/roster/srl_packet/` goes out either. **If the schedule already\n"
    "      reached students**, that has to be corrected where they read it: a short\n"
    "      follow-up announcement saying the dates are withdrawn, the ten-minute lab\n"
    "      meeting stays as an open round, nothing is prepared for it, and nothing\n"
    "      about it is graded."
)


def esc(text: str) -> str:
    return html.escape((text or "").strip())


def pretty(datestr: str, weekday: bool = False) -> str:
    """Human date. The weekday is opt-in: meeting bullets already name the day,
    but a milestone due date reads better carrying it."""
    d = datetime.date.fromisoformat(datestr)
    return d.strftime("%A, %B %-d" if weekday else "%B %-d")


def load() -> tuple[dict, list[dict]]:
    config = yaml.safe_load(CONFIG.read_text())
    with SCHEDULE.open(newline="") as fh:
        meetings = list(csv.DictReader(fh))
    return config, meetings


def week_of(meeting: dict) -> int:
    m = re.match(r"Week (\d+)", meeting["unit"])
    return int(m.group(1)) if m else 0


def notebook_for(week: int, config: dict) -> str | None:
    for w in config["weeks"]:
        if w["week"] == week:
            return w.get("notebook")
    return None


def milestone_for(week: int, config: dict) -> tuple[str, dict] | tuple[None, None]:
    for w in config["weeks"]:
        if w["week"] == week:
            key = w.get("milestone")
            if key:
                return key, config["milestones"].get(key, {})
    return None, None


def brief_path(key: str) -> Path | None:
    """The milestone brief file for M1, M2, ... (numbered 00, 01, ... on disk)."""
    n = int(key[1:])
    hits = sorted(BRIEFS.glob(f"milestone_{n:02d}_*.md"))
    return hits[0] if hits else None


def week_for_milestone(key: str, config: dict) -> int | None:
    for w in config["weeks"]:
        if w.get("milestone") == key:
            return w["week"]
    return None


def lecture_notebook_dues(config: dict) -> list[tuple[int, str, str]]:
    """(week, notebook, ISO due date) for each weekly lecture notebook (D74).

    The rule is the one recorded in course_config.yaml `lecture_notebooks:`:
    11:59 PM on the Sunday that ends the week. It is COMPUTED from the meeting
    calendar rather than typed, so the deadline cannot drift from the schedule.
    Week 16 is the one exception, and it falls out of the same computation: the
    term ends before that Sunday arrives, so the deadline lands on the last
    class day instead (Friday, December 11).
    """
    with SCHEDULE.open(newline="") as fh:
        meetings = list(csv.DictReader(fh))
    last_class = datetime.date.fromisoformat(config["calendar"]["last_class"])
    rows: list[tuple[int, str, str]] = []
    for w in config["weeks"]:
        week = w["week"]
        dates = [
            datetime.date.fromisoformat(m["date"])
            for m in meetings
            if week_of(m) == week
        ]
        notebook = w.get("notebook")
        if not dates or not notebook:
            continue
        end = max(dates)
        sunday = end + datetime.timedelta(days=(6 - end.weekday()) % 7)
        rows.append((week, notebook, min(sunday, last_class).isoformat()))
    return rows


_LN_DUES: dict[int, str] | None = None


def lecture_notebook_due(week: int, config: dict) -> str | None:
    """This week's lecture-notebook deadline, from the one derivation above, so
    a weekly unit page and the gradebook spec can never disagree."""
    global _LN_DUES
    if _LN_DUES is None:
        _LN_DUES = {wk: due for wk, _nb, due in lecture_notebook_dues(config)}
    return _LN_DUES.get(week)


def poster_template_files() -> list[Path]:
    """Any poster template shipped in this repository.

    D53 turned "a poster template and assessment rubric will be shared" into a
    public syllabus promise, and as of that ruling the template did not exist.
    The checklist has to say so out loud rather than quietly assume it. This
    check keeps that warning honest: once a template lands in one of the three
    places it would plausibly live, the warning turns into a plain to-do.
    """
    hits: list[Path] = []
    dedicated = BRIEFS / "template"
    if dedicated.is_dir():
        hits += [
            f
            for f in sorted(dedicated.glob("*"))
            if f.is_file() and not f.name.startswith(".")
        ]
    for root in (BRIEFS, ROOT / "project" / "poster"):
        if root.is_dir():
            hits += [
                f
                for f in sorted(root.glob("*"))
                if f.is_file() and "template" in f.name.lower()
            ]
    return hits


def unit_html(week: int, meetings: list[dict], config: dict) -> str:
    mine = [m for m in meetings if week_of(m) == week]
    if not mine:
        return ""
    unit_title = mine[0]["unit"]
    nb = notebook_for(week, config)
    mkey, mdata = milestone_for(week, config)

    nb_slug = None
    if nb:
        for m in mine:
            hit = re.search(rf"({nb}_[a-z0-9_]+_student)\.ipynb", m["other_material"])
            if hit:
                nb_slug = hit.group(1)
                break
        if nb_slug is None:
            hits = sorted((ROOT / "notebooks" / "student").glob(f"{nb}_*_student.ipynb"))
            nb_slug = hits[0].stem if hits else None

    out: list[str] = []
    add = out.append
    add(f"<h2>{esc(unit_title)}</h2>")

    reading = next((m["rdss_reading"] for m in mine if m["rdss_reading"].strip()), "")
    if reading:
        add("<h3>Read before Monday</h3>")
        add(f"<p>{esc(reading)}</p>")
        # The IYT Practice sentence is emitted ONLY for a week that actually
        # owes a submission. The conference block (Weeks 11-14) has non-empty
        # reading rows that are all REVISITS, so it owes nothing; printing the
        # sentence there would invent a deadline. `submissions()` is the same
        # derivation planning/IYT_SUBMISSION_SCHEDULE.md is built from, so the
        # unit page and the schedule can never disagree.
        if any(int(m["meeting"]) in _iyt_meetings() for m in mine):
            add(
                "<p>Each chapter closes with an <em>It is your turn</em> "
                "section. Complete it in that chapter's companion Colab "
                "notebook and submit it here by 11:59 PM on the date the "
                "chapter's reading is due. It is graded for completion, not "
                "for the conclusions you reach, and it is your "
                "<strong>IYT Practice</strong> credit.</p>"
            )

    if nb_slug:
        url = f"{COLAB}/notebooks/student/{nb_slug}.ipynb"
        add("<h3>This week's notebook</h3>")
        add(
            f'<p><a href="{url}" target="_blank" rel="noopener">'
            f"Open {esc(nb)} in Google Colab</a> — save your own copy to Drive "
            "before you start, and work in that copy all week.</p>"
        )
        # D74: the notebook you work in class is now collected every week.
        nb_due = lecture_notebook_due(week, config)
        if nb_due:
            add(
                "<p><strong>Hand that copy in by "
                f"{esc(pretty(nb_due, weekday=True))} at 11:59 PM.</strong> "
                "Export it to PDF and submit it here. It is graded for "
                "completion — that you worked through it and handed it in, "
                "never on whether your answers came out right — and it is your "
                "<strong>Lecture Notebooks</strong> credit.</p>"
            )

    # The week's own meetings PLUS any no-class day that falls inside it, in
    # date order. Weeks 3, 8, 13 and 14 do not have three meetings, and a unit
    # that says "the three meetings" over one bullet reads like a mistake.
    breaks = [(iso, text) for iso, text in no_class_days().items()
              if same_week(iso, mine)]
    entries = sorted(
        [(m["date"], m, None) for m in mine] + [(iso, None, text)
                                                for iso, text in breaks],
        key=lambda e: e[0])
    n = len(mine)
    word = {1: "meeting", 2: "two meetings", 3: "three meetings"}.get(
        n, f"{n} meetings")
    add(f"<h3>{'The one ' + word if n == 1 else 'The ' + word}</h3>")
    add("<ul>")
    for iso, m, label in entries:
        day = DAYNAME.get(
            datetime.date.fromisoformat(iso).strftime("%a"),
            datetime.date.fromisoformat(iso).strftime("%a"))
        if m is None:
            add(f"<li><strong>{esc(day)}, {esc(pretty(iso))}</strong> — "
                f"<em>{esc(label)}</em></li>")
            continue
        day = DAYNAME.get(m["day"], m["day"])
        add(
            f"<li><strong>{esc(day)}, {esc(pretty(m['date']))}</strong> — "
            f"{esc(m['title'])}"
            + (
                f"<br><em>{esc(m['driving_question'])}</em>"
                if m["driving_question"].strip()
                else ""
            )
            + "</li>"
        )
    add("</ul>")

    if mkey and mdata:
        add(f"<h3>Milestone {mkey}: {esc(mdata.get('title', ''))}</h3>")
        due = mdata.get("due")
        if due:
            add(
                f"<p><strong>Due {esc(pretty(due, weekday=True))} at "
                "11:59 PM.</strong> "
                "You build it in Friday's studio and submit it from there.</p>"
            )
        bp = brief_path(mkey)
        if bp:
            add(
                f"<p>The full brief is the page <em>{esc(bp.stem)}</em> in this "
                "unit. Read it before the studio.</p>"
            )

    prep = next((m["student_prep"] for m in mine if m["student_prep"].strip()), "")
    if prep:
        add("<h3>Come to Monday with</h3>")
        add(f"<p>{esc(prep)}</p>")

    return "\n".join(out) + "\n"



_IYT_MEETINGS: set[int] | None = None


def _iyt_meetings() -> set[int]:
    """Meetings that actually carry an "It is your turn" submission (D58).

    Read through build_participation_schedules.submissions() so this page and
    planning/IYT_SUBMISSION_SCHEDULE.md are derived from ONE rule.
    """
    global _IYT_MEETINGS
    if _IYT_MEETINGS is None:
        from build_participation_schedules import submissions
        with open(SCHEDULE, newline="") as f:
            rows = list(csv.DictReader(f))
        _IYT_MEETINGS = {n for n, _lid, _mode in submissions(rows)}
    return _IYT_MEETINGS


def gradebook_spec(config: dict) -> str:
    a = config["assessment"]
    fp = config["final_project_breakdown"]
    mode = config["course"]["project_mode"]
    ln = config["lecture_notebooks"]
    ln_n = ln["baseline_credits"]              # D74: N = 16, one per weekly notebook
    ln_d = math.ceil(ln_n / 10)                # ceil(0.10 * N) dropped automatically
    labels = {
        "attendance": ("Attendance", "iClicker; 85% target"),
        "participation": (
            "Participation",
            "One undivided block (D57, re-partitioned by D58): 12 studio "
            "feedback surveys, the student profile survey, the course "
            "reflection, and other constructive contributions",
        ),
        "iyt_practice": (
            "IYT Practice",
            # the pipe is escaped: this string lands in a markdown table cell
            "EDR\\|AI 'It is your turn' submissions, completion-graded; "
            "lowest ceil(0.10 * N) credits dropped",
        ),
        "lecture_notebooks": (
            "Lecture Notebooks",
            # D74's third undivided completion contract, in the slot the
            # Student Research Lead category used to hold.
            f"One undivided block (D74): the weekly notebook nbNN worked in "
            f"class, one submission per week, completion-graded; lowest "
            f"ceil(0.10 * {ln_n}) = {ln_d} credits dropped",
        ),
        "final_project": (
            "Final Project",
            "One category with the same five QM474 component items, re-shared "
            "by D74 so Milestone Deliverables carries 20 course points; "
            "Milestone Deliverables contains M1-M16",
        ),
    }
    # The retired Student Research Lead category is registered ONLY when the
    # flag brings it back (D74 Ruling 5: retire in place, delete nothing).
    if SRL_CATEGORY_ENABLED:
        labels.update(SRL_GRADEBOOK_LABELS)
    # D74 re-shared the five components: the 5 course points freed by retiring
    # Student Research Lead went to Milestone Deliverables, so the project-share
    # column no longer reads QM474's 30/20/10/20/20. The project shares are
    # exact to two decimals and sum to 100.00; the course shares sum to 55.
    expected_fp = [
        ("milestone_deliverables", "Milestone Deliverables", 36.37, 20),
        ("peer_evaluation", "Peer Evaluation", 18.18, 10),
        ("peer_review", "Peer Review", 9.09, 5),
        (
            "poster_presentation_at_the_conference",
            "Poster Presentation at the Purdue Undergraduate Research Conference",
            18.18,
            10,
        ),
        ("instructor_ta_evaluation", "Instructor/TA Evaluation", 18.18, 10),
    ]
    if mode != {
        "default": "individual",
        "groups_allowed": True,
        "approval_required": True,
        "maximum_approved_groups": 1,
        "maximum_group_size": 3,
        "individual_project_peer_evaluators": 2,
        "minimum_active_projects_for_peer_review": 3,
        "peer_assignment_plan_required": True,
    }:
        raise ValueError(
            "D52 requires individual-default projects, at most one approved "
            "group of no more than three students, three active projects, two "
            "project-peer evaluators for each individual project, and a "
            "feasible evaluation plan"
        )
    if "final_project_milestones" in a:
        raise ValueError(
            "D52 permits one top-level Final Project category; remove "
            "assessment.final_project_milestones"
        )
    if a.get("final_project") != 55:
        raise ValueError(
            "D74 requires assessment.final_project to equal 55 (D52 set it at "
            "50; the 5 points freed by retiring the Student Research Lead "
            "category are forced inside the project, on Milestone Deliverables)"
        )
    if "quizzes" in a:
        raise ValueError(
            "D58 retired the quiz grade category; remove assessment.quizzes "
            "(the banks and builders under _quizzes/ are kept, uncalled)"
        )
    if a.get("iyt_practice") != 15:
        raise ValueError(
            "D61 requires assessment.iyt_practice to equal 15 "
            "(D58 created the category at 10)"
        )
    srl_weight = a.get("srl_performance", a.get("student_research_lead"))
    if SRL_CATEGORY_ENABLED:
        if srl_weight != 25:
            raise ValueError(
                "D61 requires the Student Research Lead category to equal 25 "
                "(D58 had it at 30)"
            )
    elif srl_weight is not None:
        raise ValueError(
            "D74 retired the Student Research Lead GRADE CATEGORY; remove it "
            "from assessment: (project/srl/, scripts/assign_srl_slots.py and "
            "scripts/build_srl_packet.py are KEPT — the category is retired, "
            "never the material). To bring the category back in a future "
            "edition, set SRL_CATEGORY_ENABLED = True"
        )
    if a.get("lecture_notebooks") != 20:
        raise ValueError(
            "D74 requires assessment.lecture_notebooks to equal 20 — the "
            "completion contract that took the Student Research Lead's slot"
        )
    if ln_n != len(config["weeks"]):
        raise ValueError(
            "D74 collects one lecture notebook per week: "
            f"lecture_notebooks.baseline_credits is {ln_n} but the course has "
            f"{len(config['weeks'])} weeks"
        )
    if list(fp) != [key for key, _, _, _ in expected_fp]:
        raise ValueError("Final Project must use D52's five components in order")
    for key, label, project_share, course_share in expected_fp:
        if (
            fp[key].get("label") != label
            or fp[key].get("project_share") != project_share
            or fp[key].get("course_share") != course_share
        ):
            raise ValueError(
                f"{key} must be labelled {label!r}, carry {project_share}% of "
                f"Final Project, and contribute {course_share}% of the course"
            )
    fp_project_total = sum(item["project_share"] for item in fp.values())
    fp_course_total = sum(item["course_share"] for item in fp.values())
    if any(not item.get("scoring_rule") for item in fp.values()):
        raise ValueError("Every Final Project item must define a scoring_rule")
    # The project shares carry two decimals since D74, so compare them rounded:
    # 36.37 + 18.18 + 9.09 + 18.18 + 18.18 is 100.00 in decimal and a hair off
    # in binary floating point.
    if round(fp_project_total, 2) != 100 or fp_course_total != a["final_project"]:
        raise ValueError(
            "Final Project breakdown must sum to 100% of the project and "
            f"{a['final_project']}% of the course; got "
            f"{fp_project_total}% and {fp_course_total}%"
        )
    lines = [
        f"# Brightspace gradebook — the {len(a)} categories",
        "",
        "Build these as **weighted categories** (Grades → Manage Grades → "
        "Settings → Weighted). The weights are the syllabus contract and sum "
        "to 100; do not let Brightspace normalize them for you.",
        "",
        "| Category | Weight | Contains |",
        "|---|---:|---|",
    ]
    total = 0
    for key, weight in a.items():
        if key not in labels:
            raise ValueError(
                f"assessment.{key} has no gradebook label; add one to labels "
                "so the spec cannot ship a raw config key as a category name"
            )
        name, contains = labels[key]
        total += weight
        lines.append(f"| {name} | {weight}% | {contains} |")
    lines.append(f"| **Total** | **{total}%** | |")
    if total != 100:
        lines.append("")
        lines.append(f"> ⚠️ Weights sum to {total}, not 100. Fix course_config.yaml.")
    lines += [
        "",
        "## Final Project items",
        "",
        "Create these as five grade items inside the **Final Project** "
        "category. No component was renamed and no scoring rule inside a "
        "component changed, but D74 re-shared them: the 5 course points freed "
        "by retiring Student Research Lead went to Milestone Deliverables, so "
        "the project shares no longer read QM474's 30/20/10/20/20. Type them "
        "in to two decimals exactly as printed — they sum to 100.00% of the "
        "category. The **share of course** column is the one students see, and "
        f"it totals {a['final_project']}%.",
        "",
        "| Item | Share of Final Project | Share of course | Contains | Scoring rule |",
        "|---|---:|---:|---|---|",
    ]
    for item in fp.values():
        lines.append(
            f"| {item['label']} | {item['project_share']}% | "
            f"{item['course_share']}% | {item['includes']} | "
            f"{item['scoring_rule']} |"
        )
    lines += [
        f"| **Total** | **{round(fp_project_total, 2):.2f}%** | "
        f"**{fp_course_total}%** | | |",
        "",
        "Do not create a top-level Final Project Milestones category. M1-M16 "
        "are the source scores for the Milestone Deliverables item inside the "
        "single Final Project category. Enter that item as the equal-weight "
        "mean of all sixteen 0-100 milestone scores. Keep the sixteen "
        "numeric source items for feedback without giving them additional "
        "weight; use a calculated item when available or enter the verified "
        "mean manually.",
        "",
        "A milestone may also supply evidence to Peer Review, Poster "
        "Presentation at the Purdue Undergraduate Research Conference, or "
        "Instructor/TA Evaluation. Keep the milestone rubric and terminal "
        "rubric distinct; never copy one raw "
        "score into two component calculations.",
        "",
        "**Project modes.** Individual work is the default; groups require "
        "instructor approval before shared work begins. Approvals must "
        "create at most one group of no more than three students, preserve at "
        "least three active projects, and include a feasible peer-assignment "
        "plan in which every individual researcher has two observers and every "
        "student has at least one evaluation to submit. Group members share "
        "rubric-row scores for shared milestone evidence, the poster-quality "
        "subscore, and the final-artifact subscore. Requirements marked "
        "individual are scored per member, so a milestone score may differ "
        "only on those rows. Peer Evaluation, Peer Review, live "
        "presentation, AI-management portfolio, and Evidence Defense remain "
        "per student. Build the confidential Peer Evaluation form from "
        "project/final_dossier/peer_evaluation_instrument.md.",
        "",
        "## Peer Evaluation is not Peer Review",
        "",
        "These are two different Final Project items and neither substitutes "
        "for the other. **Peer Evaluation** is the confidential, per-student "
        "accountability score awarded by the people who observed the work. "
        "**Peer Review** is the graded quality of the structured criticism a "
        "student gives other projects. They are submitted separately and "
        "scored from different instruments.",
        "",
        "**The Peer Evaluation conversion.** Let the received-rating mean be "
        "the mean of all valid 1-5 ratings the student receives across the "
        "five dimensions and all evaluators, and let the submission fraction "
        "be the number of complete evaluations that student submits divided "
        "by the nonzero size of their submission set. A complete evaluation "
        "carries all five ratings and both usable comments.",
        "",
        "```",
        "received_rating_score = min(100, 100 * received_rating_mean / 3)",
        "submission_points     = 20 * submission_fraction",
        "Peer Evaluation item  = 0.80 * received_rating_score "
        "+ submission_points",
        "```",
        "",
        "- A received-rating mean of 3 with a complete submission scores "
        "80 + 20 = 100. Ratings above 3 confirm full received-rating credit "
        "but never create credit above 100.",
        "- The 20 submission points are earned in full for completing every "
        "assigned evaluation, 0 for completing none, and pro rata in "
        "between.",
        "- Non-submission costs the non-submitter their own submission "
        "points and nothing else. It never lowers the score of the "
        "classmates they were assigned to rate.",
        "- A missing rating is never entered as a zero for its intended "
        "recipient. Follow up with the assigned evaluator and calculate from "
        "whatever valid ratings arrive.",
        "- If no valid received rating survives that follow-up, use the "
        "neutral 80-point received-rating portion, equivalent to a mean "
        "rating of 3. Do not add a substitute evaluator after the "
        "observation period has ended.",
        "",
        "Moderation of strategically inflated or deflated ratings requires a "
        "documented evidence record; see "
        "project/final_dossier/peer_evaluation_instrument.md for the "
        "instrument, the five dimensions, and that record's format.",
        "",
        "## Items inside each category",
        "",
        f"- **Final Project → Milestone Deliverables** — {len(config['milestones'])} "
        "source items, M1 through M16, each with the due date below; the "
        "component score is their equal-weight mean.",
        "- **Final Project → Peer Evaluation** — one confidential per-student "
        "item; use every teammate for approved groups and two assigned project "
        "peers for individual researchers. No self-rating. If evaluator "
        "non-submission leaves no valid received rating after follow-up, use "
        "the neutral 80-point received-rating portion; do not add a substitute "
        "evaluator after observation ends.",
        "- **Final Project → Peer Review** — one individually scored item from "
        "the M12 Final Project Peer Review rubric.",
        "- **Final Project → Poster Presentation at the Purdue Undergraduate "
        "Research Conference** — one per-student item: 70% M13 poster quality "
        "+ 30% M15 live presentation.",
        "- **Final Project → Instructor/TA Evaluation** — one per-student "
        "item: 100% the instructor's evaluation of the final poster "
        "submission locked at M13 (D54). The final research chapter, the "
        "AI-management portfolio and the oral Evidence Defense no longer "
        "carry grade weight and get no gradebook item.",
        f"- **Lecture Notebooks** — ONE undivided {a['lecture_notebooks']}% "
        "category (D74), the third completion contract and the one that took "
        "the Student Research Lead category's place. Create "
        f"**{ln_n} dropboxes, one per weekly notebook (nb01-nb{ln_n:02d})**, "
        "each due 11:59 PM on the Sunday that ends its week; the last one "
        "closes on the last class day instead, because the term ends before "
        "that Sunday arrives. The dated list is directly below and in "
        "planning/LECTURE_NOTEBOOK_SCHEDULE.md. EVERY student submits to EVERY "
        "one of them, unlike the retired SRL dropboxes, which only one student "
        "could use. Take the notebook the same way every milestone is taken, "
        "as the PDF export of the student's own Colab copy. Grade on "
        "**completion only**: worked through and handed in, never on whether "
        "the answers came out right. Nothing said in the ten-minute lab meeting "
        "that opens each Monday and Wednesday lecture is graded either (D75): "
        "it is an open round, nobody is assigned to it and nobody prepares for "
        "it, so it never reaches this credit or any other. "
        "Credit 1.0 on time, 0.5 within seven days, 0 after that; "
        f"N = {ln_n} and the lowest ceil(0.10 x {ln_n}) = {ln_d} credits are "
        "dropped automatically, so points = "
        f"{a['lecture_notebooks']}.0 x (sum of the highest {ln_n - ln_d} "
        f"credits) / {ln_n - ln_d}. This is NOT participation: it never draws "
        "participation's +/- 0.9 contribution adjustment, and it may never be "
        "reintroduced as a participation item.",
        # D74 Ruling 5: the SRL bullet is kept, not deleted — one flag away.
        *([SRL_GRADEBOOK_ITEM_BULLET] if SRL_CATEGORY_ENABLED else []),
        "- **Participation** — ONE undivided 9% category (D57, re-partitioned "
        "by D58). Create one item for the studio feedback survey, one for the "
        "student profile survey (Aug 30), and one for the course reflection "
        "(Dec 11). The survey item carries SEVERAL ledger credits (12, one per "
        "studio), so enter its running credit total rather than a single "
        "pass/fail. N = 14 baseline credits and the lowest "
        "ceil(0.10 x 14) = 2 are dropped; every credit is equal and graded for "
        "completion. Lecture notebooks ARE collected since D74, but in their "
        "own Lecture Notebooks category above: D57's ban stands in its amended "
        "form, so notebook completion may never come back HERE, as a "
        "participation item. surveys/participation_grading.md is the authority "
        "for the item list and the counts; Brightspace is where the running "
        "total is posted.",
        "- **IYT Practice** — ONE 15% category, the EDR|AI 'It is your turn' "
        "family D58 moved out of Participation. Create one assignment per due "
        "date (planning/IYT_SUBMISSION_SCHEDULE.md lists them, with the "
        "instruction paragraph to paste into every one). Every item is "
        "completion-graded and equally weighted, and the lowest "
        "ceil(0.10 x N) credits are dropped: 4 at the typical N = 35 "
        "(36 when the declared design has stages, which still drops 4). N is "
        "per student, so read it off the schedule rather than hard-coding it. "
        "surveys/participation_grading.md carries the student-facing "
        "contract.",
        "",
        "## Milestone due dates",
        "",
        "| Milestone | Title | Due |",
        "|---|---|---|",
    ]
    for key, m in config["milestones"].items():
        lines.append(f"| {key} | {m.get('title','')} | {m.get('due','TBD')} |")
    lines += [
        "",
        "## Lecture notebook due dates",
        "",
        f"One dropbox per weekly notebook, {ln_n} in all, every one of them at "
        "11:59 PM. The date is the Sunday that ends that week, except for the "
        "last, which lands on the last class day because the term ends before "
        "its Sunday arrives. Put all of these on the Brightspace calendar too.",
        "",
        "| Week | Notebook | Due (11:59 PM) |",
        "|---|---|---|",
    ]
    for week, notebook, due in lecture_notebook_dues(config):
        weekday = pretty(due, weekday=True).split(",")[0]
        lines.append(f"| {week} | {notebook} | {due} ({weekday}) |")
    lines.append("")
    return "\n".join(lines)


def checklist(config: dict) -> str:
    c = config["course"]
    cal = config["calendar"]
    ln_dues = lecture_notebook_dues(config)
    ln_n = config["lecture_notebooks"]["baseline_credits"]
    ln_last = pretty(ln_dues[-1][2], weekday=True) if ln_dues else "the last class day"
    # D74 Ruling 5 again: both wordings are kept, and one flag chooses.
    srl_announcement = (
        SRL_CHECKLIST_ANNOUNCEMENT
        if SRL_CATEGORY_ENABLED
        else LAB_MEETING_CHECKLIST_ANNOUNCEMENT
    )
    srl_assignment_todo = (
        SRL_CHECKLIST_ASSIGNMENT_TODO
        if SRL_CATEGORY_ENABLED
        else LAB_MEETING_CHECKLIST_ASSIGNMENT_TODO
    )

    guidelines = "_research_project/2026Fall/final_project_grading_and_project_modes.md"
    poster_key = "M11"
    poster_due = config["milestones"].get(poster_key, {}).get("due")
    poster_when = (
        f"{pretty(poster_due, weekday=True)}, {poster_due[:4]}" if poster_due else "TBD"
    )
    poster_week = week_for_milestone(poster_key, config)
    poster_unit = f"the Week {poster_week} unit" if poster_week else "the poster-draft unit"
    lock_due = config["milestones"].get("M13", {}).get("due", "TBD")
    templates = poster_template_files()

    if templates:
        found = ", ".join(f"`{t.relative_to(ROOT)}`" for t in templates)
        poster_banner = (
            "> **Syllabus promise, item 4.** Students are promised \"a poster "
            "template and assessment rubric\". Both now exist in the repo "
            f"({found}); section 4 is where you publish them."
        )
        template_todo = (
            f"- [ ] **Publish the poster template.** {found}. It must reach "
            f"students in {poster_unit}, on or before {poster_key} "
            f"({poster_when}), because the syllabus promises it."
        )
    else:
        poster_banner = (
            "> ⚠️ **OPEN SYLLABUS PROMISE — the poster template does not "
            "exist.** Item 4 of the syllabus tells students \"a poster "
            "template and assessment rubric will be shared\". The **rubric "
            "exists**. The **template does not exist anywhere in this "
            f"repository** and is due to students by {poster_key} "
            f"({poster_when}). See section 4."
        )
        template_todo = (
            "- [ ] ⚠️ **BUILD the poster template — it does not exist yet.** "
            "Nothing in the repository matches a poster template, and "
            "`_research_project/2026Fall/template/` is an empty directory. "
            "The syllabus now promises one, so this is a commitment to "
            f"students, not a nice-to-have. Deadline: in students' hands by "
            f"{poster_key} ({poster_when}), published in {poster_unit}. Size "
            "it for the shared print run that locks at M13 "
            f"({lock_due}, 11:59 PM) with QM 47400."
        )

    poster_section = f"""## 4. Two promises the syllabus makes to students

Syllabus item 4 says a poster template **and** an assessment rubric will be
shared. Both are instructor deliverables with a date, not background material.

{template_todo}
- [ ] **Publish the poster assessment rubric.** `project/poster/poster_rubric.md`
      is a pointer file: the authoritative rubric is the poster-quality rubric
      inside `_research_project/2026Fall/milestone_13_final_poster_lock.md`.
      Publish the rubric students will actually be graded on, in {poster_unit},
      with the template. Say plainly that it supplies 70% of the Poster
      Presentation item, with the M15 live presentation supplying the other 30%.
"""

    return f"""# Brightspace — pre-semester checklist

Ordered so the **Monday-critical** subset comes first. Everything in section 1
must be true before **{pretty(cal['first_class'], weekday=True)}**; sections 2 and 3 can land
during Week 1. Section 4 is dated later in the semester but is listed here
because it is a promise the syllabus already makes.

Course: **{c['number']}-{c['section']}**, CRN {c['crn']}, {c['title']} —
{c['credit_hours']} credit hours, {c['enrollment']} students enrolled.

{poster_banner}

---

## 1. Before Monday {cal['first_class']} — students cannot start without these

- [ ] **Activate the course.** Course Admin → Course Offering Information →
      check **Course is active**. Until this is ticked, students see nothing.
      As of the 2026-08-22 classlist export, `LastAccessed` was empty for all
      five students then enrolled, which is consistent with the shell never
      having been open; two more students joined on 2026-08-25.
- [ ] **Set the course start and end dates** to {cal['first_class']} and
      {cal['last_class']}, and make sure the start date is not *also* acting as
      a release gate that hides Week 1.
- [ ] **Post the Week 1 announcements.** They live in `_announcements/` as
      Markdown, ready to open in the editor and paste into Brightspace:
      `01_welcome.md` (before Monday), `02_how_the_course_runs.md` (how Monday,
      Wednesday and Friday work, and what closes each Sunday night), and
      {srl_announcement}
- [ ] **Publish the Week 1 unit** (`units/week01.html`) with the M1 brief.
- [ ] **Publish the Final Project guidelines** — `{guidelines}` — as a page in
      the **Week 1 unit**, next to the M1 brief, and link it from Course Home
      and from the Final Project category description. This is the
      "comprehensive set of project guidelines" the syllabus promises: the
      syllabus carries only the five components and their shares, so this
      document is the only student-facing home for the component table, the
      four scoring formulas, the individual-versus-group rules, and the
      Peer Evaluation conversion. Every milestone brief links to it, so it has
      to be live before M1 is due.
- [ ] **Link the course site and the book** on Course Home:
      {SITE} and {SITE}/book/.
- [ ] **Check preferred names** on the myPurdue Faculty tab and record them in
      `_adm/roster/` before you address anyone by name on Monday.

## 2. Week 1 — the machinery

- [ ] **Build the gradebook** from `gradebook_spec.md` ({len(config['assessment'])} weighted categories).
- [ ] **Create all {len(config['milestones'])} milestone items** with the due dates in that file, and put
      every date on the Brightspace **calendar** (Purdue's 2026-08-21 guidance
      asks for dates on all assignments).
- [ ] **Create the {ln_n} lecture-notebook dropboxes** — one per weekly notebook,
      inside the **Lecture Notebooks** category, with the due dates in
      `gradebook_spec.md` and `planning/LECTURE_NOTEBOOK_SCHEDULE.md`. Every
      student submits to every one of them; the last closes on {ln_last},
      because the term ends before its Sunday arrives. Completion only, and the
      lowest two credits drop automatically, so set them up as pass/fail rather
      than as something you have to mark. These replace the 25 SRL slot
      dropboxes, which are **not** created this edition (D74).
- [ ] **Publish units 2-16** with sequential release, or publish weekly by hand.
      With six students, weekly by hand is defensible and less brittle.
      D58 rewrote the reading section of *every* unit and removed the Friday
      quiz block, and D74 added the weekly notebook deadline to every one of
      them, so re-paste all of them, not only the weeks you changed.
{srl_assignment_todo}

## 3. Dated obligations that are not about content

- [ ] **Simple Syllabus — due Friday, 2026-09-04.** Mandatory for Fall 2026 and
      it replaces Course Insights. Instructor-of-record only. Draft the
      generative-AI policy component from `simple_syllabus_ai_policy.md`, which
      is written from this course's actual AI policy rather than the template
      default.
- [ ] **Initial Course Participation (ICP) reporting — by Week 3**
      (~{ (datetime.date.fromisoformat(cal['first_class']) + datetime.timedelta(days=18)).isoformat() }),
      federally mandated, in myPurdue Faculty Tools.

{poster_section}
---

## 5. The three completion contracts the syllabus points at

The syllabus tells students that the full list of Participation items, their due
dates and their submission instructions "are posted on the course page", that
the IYT Practice dated list lives on the schedule page and on Brightspace, and
since D74 that the weekly lecture notebook is collected on a dated schedule of
its own. All three promises need something published.

- [ ] **Publish the IYT Practice assignments.** `planning/IYT_SUBMISSION_SCHEDULE.md`
      lists every due date, the chapters that share it, and the ONE instruction
      paragraph to paste into each assignment. Create one Brightspace assignment
      per due date inside the **IYT Practice** category. Every item is
      completion-graded and equally weighted.
- [ ] **Publish the studio feedback survey.** One Qualtrics link, reused for all
      twelve responses; the closes are in `planning/STUDIO_FEEDBACK_SCHEDULE.md`
      (each is the Sunday that ends its studio week, the same night that studio's
      milestone is due). Post the link where students will find it every week.
- [ ] **Publish the student profile survey** (due Sun Aug 30) and the
      **course reflection** (collected in the last class, Fri Dec 11). Both are
      single Participation credits; the instruments live in `surveys/`.
- [ ] **Publish the lecture-notebook dropboxes.** The notebook worked in class is
      handed in every week (D74): {ln_n} dropboxes, each due 11:59 PM on the
      Sunday that ends its week, the last on {ln_last}. Completion only — worked
      through and handed in, never whether the answers came out right. Say that
      in the dropbox instructions, because it is the sentence that keeps the
      contract from reading like a quality grade, and point students at the
      Colab-to-PDF routine every milestone already uses.
- [ ] **State the drop rule once, where students read it.** The lowest
      `ceil(0.10 x N)` credits are dropped automatically in EACH contract
      separately — they are three pools, not one, and D74's notebook pool drops
      two of {ln_n}. `surveys/participation_grading.md` is the student-facing
      contract for participation and IYT Practice.

---

## The one thing that is easy to get wrong

Markdown pasted into Brightspace's HTML editor renders as literal text. The
files in `units/` are **HTML**: open one, copy its contents, and paste into the
editor's **source view** (the `</>` button), not the rich-text view.

## The Schedule description

Paste `schedule.html`, not the course page. Brightspace caps a description at
**65,535 characters including hidden formatting**, and the rendered course page
does not fit: it carries about 18 KB of Quarto navigation, its links are relative
and would 404 from Brightspace, its table CSS lives in a stylesheet that does not
travel with a paste, and its new-tab behaviour is a script Brightspace strips.

`schedule.html` is the same table built for that field: absolute links, layout
inline, no script, whitespace collapsed. Its builder refuses to write a file that
would breach the ceiling, so if it wrote one, it fits. Paste it in **source
view**, and rebuild it after any schedule change with

    .venv/bin/python scripts/build_brightspace_schedule.py
"""


def ai_policy_component(config: dict) -> str:
    p = config["ai_policy"]
    never = "\n".join(f"- {x}" for x in p["never_delegate"])
    return f"""# Simple Syllabus — generative-AI policy component

Due **Friday, 2026-09-04**. Paste into the AI-policy component of the Simple
Syllabus template. Written for this course specifically: an AI-methods course
cannot ship the generic "ask your instructor before using AI" default, because
using AI is the assignment.

---

**Generative AI in this course: required, directed, and documented.**

This course does not restrict generative AI. It teaches you to direct it. You
are expected to use AI tools on nearly every assignment, and you are graded in
part on how well you manage them.

The rule the course runs on is this: **{p['principle'].lower().rstrip('.')}**.
An AI may draft, compute, summarize, and criticize. It may not decide. The
discipline you will practise every week is **{p['discipline_shorthand']}**:
specify the task, delegate it, interrogate the output, inspect it, verify it
against something independent, document what happened, and defend the result as
your own.

**What you must document.** Every deliverable carries an **AI Research Ledger**
entry recording, for each delegated task: what you asked for, which tool you
used, the prompt, a summary of the output, the decision you made, how you
verified it, what still concerns you, and your name as the responsible
researcher. A missing ledger entry returns the submission ungraded.

**What never leaves your hands.** These decisions are yours, and presenting an
AI's answer to any of them as your own judgment is academic dishonesty:

{never}

**Verification is not optional.** {p['verify_rule'].capitalize()} Any factual
claim, citation, or number that an AI produced must be traced to a real,
retrievable source and independently confirmed before it appears in your work.
A fabricated citation is treated as fabricated evidence, whatever produced it.

**Approved tools.** {p['tools']['primary']} is the primary research assistant.
{p['tools']['reviewer_bench']} supplies the reviewer roles you use to attack
your own work. {p['tools']['also_permitted']}

**Privacy.** Do not put anyone's private or identifiable data into a
general-purpose AI tool. Purdue's data-protected services exist for that.
"""


def welcome_announcement(config: dict) -> str:
    """The Week 1 welcome, as Brightspace-ready Markdown."""
    c = config["course"]
    cal = config["calendar"]
    day1 = pretty(cal["first_class"], weekday=True)
    return f"""# Welcome to {c['number']} — {c['title']}

*Post on Brightspace before {day1}. Paste the body below (everything under the
rule) into the announcement editor. Generated by
`scripts/build_brightspace_kit.py` — do not hand-edit; fix the generator instead.*

---

Hello everyone,

Welcome, and I am really glad you are here. We start **{day1}**, and I am looking forward to
meeting all of you. This is a small seminar, which means we will get to know each
other quickly and your questions will genuinely shape how the semester goes.

Here are four things to know before Monday.

**1. There is nothing to buy.** The course book is our own open text, *EDR|AI —
Evidence-Driven Research in the Age of AI*, and it is free at
<{SITE}/book/>. Every other reading is free online too. I wrote it for this
course, so if a passage is confusing, tell me. That is useful feedback, not a
complaint.

**2. Please bring a laptop on day one.** All of our computing runs in your
browser through Google Colab, so there is nothing to install and nothing to set
up in advance. On Monday you will open the first notebook, save your own copy,
and run it. Just come able to sign in to Google.

**3. Here is what you are walking into.** This is a {c['credit_hours']}-credit
seminar built around one research project that is yours from the very first week.
You choose the question. You defend the claim. Plan on about six hours a week
outside class, and know that the work is real research rather than exercises.

The whole course runs on one idea: **AI can be used for scientific discovery and
research. My goal is to prepare you to use it as your best research assistant.**
You will use AI constantly here, and none of that is cheating. What you are
graded on is how well you direct it and how carefully you check it, never on
letting it decide for you.

One date belongs on your calendar right now: **Tuesday, November 17**, the Purdue
Fall Undergraduate Research Expo, where you will present your poster. It is
required and graded.

**4. A few things are due at the end of Week 1, on Sunday, August 30, at 11:59
PM:** Milestone 1 (your curiosity, committed), the student profile survey, and
the Studio 1 feedback survey. None of this should catch you off guard, because we
build Milestone 1 together in class on Friday. Still, it is worth putting on your
calendar today.

The full schedule lives at <{SITE}/schedule.html>. Have a look at the syllabus
before the first class, and please bring your questions with you. Curiosity is the whole
point of this course, so come with some.

If anything at all is unclear before we begin, or if there is something about
your situation I should know, just email me. I would much rather hear from you
early.

All the best,

Prof. Moreira
"""


def main() -> int:
    config, meetings = load()
    OUT.mkdir(exist_ok=True)
    (OUT / "units").mkdir(exist_ok=True)
    ANNOUNCEMENTS.mkdir(parents=True, exist_ok=True)

    weeks = sorted({week_of(m) for m in meetings if week_of(m)})
    for week in weeks:
        body = unit_html(week, meetings, config)
        if body:
            (OUT / "units" / f"week{week:02d}.html").write_text(body)

    (OUT / "gradebook_spec.md").write_text(gradebook_spec(config))
    (OUT / "00_pre_semester_checklist.md").write_text(checklist(config))
    (OUT / "simple_syllabus_ai_policy.md").write_text(ai_policy_component(config))
    (ANNOUNCEMENTS / "01_welcome.md").write_text(welcome_announcement(config))

    # The Schedule description field is its own edition: it is derived from the
    # RENDERED page, not from the CSV, so it cannot drift from what students see.
    try:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_brightspace_schedule.py")],
            check=True)
    except subprocess.CalledProcessError:
        print("⚠ the Schedule paste edition did not build — see the error above")

    print(f"✓ Brightspace kit written to {OUT.relative_to(ROOT)}/")
    print(f"  {len(weeks)} weekly units, gradebook spec, checklist, AI policy,")
    print(f"  and the Week 1 welcome announcement "
          f"({(ANNOUNCEMENTS / '01_welcome.md').relative_to(ROOT)})")
    print("  (brightspace/ is gitignored — nothing here is published)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
