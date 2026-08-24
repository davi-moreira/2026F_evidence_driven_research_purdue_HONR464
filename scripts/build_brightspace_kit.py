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
import re
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
        # Both spellings of the SRL key are registered on purpose, so a rename
        # in course_config.yaml can never print a raw key in the spec table.
        "srl_performance": (
            "Student Research Lead",
            "5 leads per student, scored on project/srl/srl_rubric.md",
        ),
        "student_research_lead": (
            "Student Research Lead",
            "5 leads per student, scored on project/srl/srl_rubric.md",
        ),
        "final_project": (
            "Final Project",
            "One category with five QM474 component items (30/20/10/20/20); "
            "Milestone Deliverables contains M1-M16",
        ),
    }
    expected_fp = [
        ("milestone_deliverables", "Milestone Deliverables", 30, 15),
        ("peer_evaluation", "Peer Evaluation", 20, 10),
        ("peer_review", "Peer Review", 10, 5),
        (
            "poster_presentation_at_the_conference",
            "Poster Presentation at the Purdue Undergraduate Research Conference",
            20,
            10,
        ),
        ("instructor_ta_evaluation", "Instructor/TA Evaluation", 20, 10),
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
    if a.get("final_project") != 50:
        raise ValueError("D52 requires assessment.final_project to equal 50")
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
    if a.get("srl_performance", a.get("student_research_lead")) != 25:
        raise ValueError(
            "D61 requires the Student Research Lead category to equal 25 "
            "(D58 had it at 30)"
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
    if fp_project_total != 100 or fp_course_total != a["final_project"]:
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
        "Create these as five grade items inside the **Final Project** category. "
        "The project shares preserve QM474's 30/20/10/20/20 structure; the "
        f"course shares total {a['final_project']}%.",
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
        "| **Total** | **100%** | "
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
        "- **Student Research Lead** — 5 items per student is wrong; create "
        "**one** item per SRL slot the student holds, or a single item scored 5 "
        "times. One item, entered after each lead, is simpler for 5 students.",
        "- **Participation** — ONE undivided 9% category (D57, re-partitioned "
        "by D58). Create one item for the studio feedback survey, one for the "
        "student profile survey (Aug 30), and one for the course reflection "
        "(Dec 11). The survey item carries SEVERAL ledger credits (12, one per "
        "studio), so enter its running credit total rather than a single "
        "pass/fail. N = 14 baseline credits and the lowest "
        "ceil(0.10 x 14) = 2 are dropped; every credit is equal and graded for "
        "completion. Lecture notebooks are NOT collected and get no gradebook "
        "item. surveys/participation_grading.md is the authority for the item "
        "list and the counts; Brightspace is where the running total is "
        "posted.",
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
    lines.append("")
    return "\n".join(lines)


def checklist(config: dict) -> str:
    c = config["course"]
    cal = config["calendar"]

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
      five students, which is consistent with the shell never having been open.
- [ ] **Set the course start and end dates** to {cal['first_class']} and
      {cal['last_class']}, and make sure the start date is not *also* acting as
      a release gate that hides Week 1.
- [ ] **Post the welcome announcement** (`announcements/week01_welcome.html`).
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
- [ ] **Publish units 2-16** with sequential release, or publish weekly by hand.
      With five students, weekly by hand is defensible and less brittle.
      D58 rewrote the reading section of *every* unit and removed the Friday
      quiz block, so re-paste all of them, not only the weeks you changed.
- [ ] **Post the SRL assignment** so each student sees their own five dates
      (`_adm/roster/2026F_HONR46400_srl_assignment.md`). FERPA: post each
      student's slots to that student, or post a slot table by date that names
      only the lead for that date — never distribute the roster file itself.

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

## 5. The two completion contracts the syllabus points at

The syllabus tells students that the full list of Participation items, their due
dates and their submission instructions "are posted on the course page", and that
the IYT Practice dated list lives on the schedule page and on Brightspace. Both
promises need something published.

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
- [ ] **State the drop rule once, where students read it.** The lowest
      `ceil(0.10 x N)` credits are dropped automatically in EACH contract
      separately — they are two pools, not one. `surveys/participation_grading.md`
      is the student-facing contract for both.

---

## The one thing that is easy to get wrong

Markdown pasted into Brightspace's HTML editor renders as literal text. The
files in `units/` are **HTML**: open one, copy its contents, and paste into the
editor's **source view** (the `</>` button), not the rich-text view.
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
    c = config["course"]
    cal = config["calendar"]
    return f"""<h3>Welcome to {esc(c['number'])} — {esc(c['title'])}</h3>

<p>We start <strong>{esc(pretty(cal['first_class'], weekday=True))}</strong>. Before then,
three things.</p>

<p><strong>1. Nothing to buy.</strong> The course book is our own open text,
<em>EDR|AI — Evidence-Driven Research in the Age of AI</em>, free at
<a href="{SITE}/book/" target="_blank" rel="noopener">{SITE}/book/</a>. Every
other reading is free online too.</p>

<p><strong>2. Bring a laptop on day one.</strong> All the computing runs in your
browser through Google Colab, with nothing to install. On Monday you will open
the first notebook, save your own copy, and run it, so come able to sign in to
Google and to <a href="https://genai.rcac.purdue.edu" target="_blank"
rel="noopener">genai.rcac.purdue.edu</a>.</p>

<p><strong>3. Know what you are walking into.</strong> This is a
{c['credit_hours']}-credit seminar built around one research project that is
yours from the first week: you choose the question, you defend the claim. Plan
about six hours a week outside class. You will use AI constantly and you will be
graded on how well you direct and check it, never on letting it decide. And one
date belongs on your calendar now: <strong>Tuesday, November 17</strong>, the
Purdue Fall Undergraduate Research Expo, where you present your poster. It is
required, it is graded, and it is not a class day.</p>

<p>The full schedule lives at
<a href="{SITE}/schedule.html" target="_blank" rel="noopener">the course
site</a>. Read the syllabus before Monday and bring your questions.</p>

<p>See you {esc(pretty(cal['first_class'], weekday=True))}.</p>
"""


def main() -> int:
    config, meetings = load()
    OUT.mkdir(exist_ok=True)
    (OUT / "units").mkdir(exist_ok=True)
    (OUT / "announcements").mkdir(exist_ok=True)

    weeks = sorted({week_of(m) for m in meetings if week_of(m)})
    for week in weeks:
        body = unit_html(week, meetings, config)
        if body:
            (OUT / "units" / f"week{week:02d}.html").write_text(body)

    (OUT / "gradebook_spec.md").write_text(gradebook_spec(config))
    (OUT / "00_pre_semester_checklist.md").write_text(checklist(config))
    (OUT / "simple_syllabus_ai_policy.md").write_text(ai_policy_component(config))
    (OUT / "announcements" / "week01_welcome.html").write_text(
        welcome_announcement(config)
    )

    print(f"✓ Brightspace kit written to {OUT.relative_to(ROOT)}/")
    print(f"  {len(weeks)} weekly units, gradebook spec, checklist, AI policy,")
    print("  and the Week 1 welcome announcement")
    print("  (brightspace/ is gitignored — nothing here is published)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
