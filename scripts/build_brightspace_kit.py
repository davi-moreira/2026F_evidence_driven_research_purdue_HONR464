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


def quiz_handouts() -> dict[int, Path]:
    """Return active course week -> generated printed quiz handout."""
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
    """How many course weeks actually carry a printed quiz."""
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

    if nb_slug:
        url = f"{COLAB}/notebooks/student/{nb_slug}.ipynb"
        add("<h3>This week's notebook</h3>")
        add(
            f'<p><a href="{url}" target="_blank" rel="noopener">'
            f"Open {esc(nb)} in Google Colab</a> — save your own copy to Drive "
            "before you start, and work in that copy all week.</p>"
        )

    add("<h3>The three meetings</h3>")
    add("<ul>")
    for m in mine:
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

    if week in quiz_handouts():
        add("<h3>Friday quiz</h3>")
        add(
            "<p>The studio opens with a 10-minute printed multiple-choice quiz "
            "on this week's material. It is closed-book and closed-device.</p>"
        )

    prep = next((m["student_prep"] for m in mine if m["student_prep"].strip()), "")
    if prep:
        add("<h3>Come to Monday with</h3>")
        add(f"<p>{esc(prep)}</p>")

    return "\n".join(out) + "\n"


def gradebook_spec(config: dict) -> str:
    a = config["assessment"]
    fp = config["final_project_breakdown"]
    mode = config["course"]["project_mode"]
    labels = {
        "attendance": ("Attendance", "iClicker; 85% target"),
        "participation": (
            "Participation",
            "Feedback surveys, lecture-notebook completion, and other "
            "constructive contributions to the course",
        ),
        "quizzes": (
            "Quizzes",
            f"{n_quizzes()} weekly printed MC quizzes, entered by hand",
        ),
        "srl_performance": (
            "Student Research Lead",
            "5 leads per student, scored on project/srl/srl_rubric.md",
        ),
        "final_project": (
            "Final Project",
            "One category with five QM474 component items (30/20/10/20/20); "
            "Milestone Deliverables contains M1-M17",
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
        name, contains = labels.get(key, (key, ""))
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
        "Do not create a top-level Final Project Milestones category. M1-M17 "
        "are the source scores for the Milestone Deliverables item inside the "
        "single Final Project category. Enter that item as the equal-weight "
        "mean of all seventeen 0-100 milestone scores. Keep the seventeen "
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
        "## Items inside each category",
        "",
        f"- **Final Project → Milestone Deliverables** — {len(config['milestones'])} "
        "source items, M1 through M17, each with the due date below; the "
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
        "item: 50% M17 Final Research Artifact + 25% M17 AI-management "
        "portfolio + 25% Evidence Defense.",
        f"- **Quizzes** — {n_quizzes()} items, one per teaching week that "
        "carries a quiz (Week 14 is asynchronous and has none). Quizzes are "
        "printed and graded on paper, so create them as **numeric grade "
        "items**, not Brightspace quizzes.",
        "- **Student Research Lead** — 5 items per student is wrong; create "
        "**one** item per SRL slot the student holds, or a single item scored 5 "
        "times. One item, entered after each lead, is simpler for 5 students.",
        "- **Participation** — create items for feedback surveys and lecture-"
        "notebook completion, plus an item for other constructive contributions "
        "to the course.",
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
    return f"""# Brightspace — pre-semester checklist

Ordered so the **Monday-critical** subset comes first. Everything in section 1
must be true before **{pretty(cal['first_class'], weekday=True)}**; sections 2 and 3 can land
during Week 1.

Course: **{c['number']}-{c['section']}**, CRN {c['crn']}, {c['title']} —
{c['credit_hours']} credit hours, {c['enrollment']} students enrolled.

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
