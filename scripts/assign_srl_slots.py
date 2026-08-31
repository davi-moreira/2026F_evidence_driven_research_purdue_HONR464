#!/usr/bin/env python3
"""Draw the lab-meeting REPORTER assignment for the semester. WITHDRAWN by D75.

WITHDRAWN BY D75 (2026-08-31), KEPT ON DISK
-------------------------------------------
D74 made ONE assigned student the reporter at every Mon/Wed lab meeting. D75
withdraws that assignment entirely. The ten-minute opening block stays; the
assignment does not. NO student is designated, on any lecture, ever. There is no
draw, no assigned question or request, and no preparation of any kind before
class by anybody. The instructor asks the room how the projects are going and
the room answers: what was decided since last time, what the evidence looks
like, where somebody is stuck. From minute 10 the instructor leads the lesson,
and nothing said in the lab meeting is graded.

So this draw does not run. `DRAW_ENABLED = False` below is the guard, and
`main()` stops on it rather than writing an assignment nobody is bound by. Every
line of the drawing logic is KEPT below, unchanged, under D75's ruling that
nothing is deleted: setting `DRAW_ENABLED = True` reinstates the draw for a
future edition that wants assigned reporters back.

The rest of this docstring describes the draw as it stood under D74, preserved
for that future edition.

Every Mon/Wed lecture from Week 2 opens with a ten-minute LAB MEETING. One
student is that lecture's REPORTER: seven minutes on a decision from their OWN
project and the evidence behind it, then three minutes of questions from the
room. The reporter does not teach the lecture's concept, and the report itself
carries no score (D74). This script assigns those slots at the start of the
semester -- randomly, with no rotation and no seats (D22, as amended by D74).

D74 (2026-08-31) retired the Student Research Lead ROLE and its 25% grade
category. It did NOT retire this draw and did NOT order a re-draw: the standing
D69/D71 assignment carries over unchanged -- the same 25 slots over 6 students,
still 4/4/4/4/4/5, the same dates and the same students. Only the name of the
job changed, from lead to reporter. Rerun this script when the ROSTER changes
(see `_adm/roster/ROSTER_CHANGE_RUNBOOK.md`), never to "refresh" the draw for
D74. The script is kept for future editions under D74's ruling that no SRL
artefact is ever deleted.

The paths below keep their `srl_` stem on purpose: the assignment already on
disk is the one that carries over, and every downstream reader (chiefly
`scripts/build_srl_packet.py`) opens it under that name.

FERPA: the roster is student data. It lives in the gitignored `_adm/roster/`
and is read at run time; this script carries no names, and its output is
written back into `_adm/` so the assignment is never committed or published.
Students learn their own slots through the course platform, not the site.

Fairness constraints, all enforced by rejection sampling:
  1. Report counts are as even as the roster allows. When the slots do not
     divide evenly, `len(slots) % n_students` students carry one extra report
     and WHICH students those are is itself drawn at random, so the remainder
     is not handed out by name, by seniority, or by enrolment date.
  2. No student reports at two consecutive lab meetings.
  3. No student reports at both lab meetings of the same week.
  4. Each student's slots spread across the semester: at least one in the
     first half and one in the second.

Locked slots (`LOCKED`): a slot already announced to the class is frozen and
excluded from the redraw, so a late roster change never moves a date a student
has already been told to prepare for. Everything after the locked slots is
redrawn from scratch.

Usage (inert while DRAW_ENABLED is False; each invocation prints why):
    .venv/bin/python scripts/assign_srl_slots.py
    .venv/bin/python scripts/assign_srl_slots.py --seed 464 --dry-run
    .venv/bin/python scripts/assign_srl_slots.py --ignore-locks   # clean draw
"""
from __future__ import annotations

import argparse
import csv
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEDULE = ROOT / "planning" / "MEETING_SCHEDULE.csv"
ROSTER = ROOT / "_adm" / "roster" / "2026F_HONR46400_roster.csv"
OUT_CSV = ROOT / "_adm" / "roster" / "2026F_HONR46400_srl_assignment.csv"
OUT_MD = ROOT / "_adm" / "roster" / "2026F_HONR46400_srl_assignment.md"

SEED = 464
MAX_TRIES = 200_000

#: D75 (2026-08-31) withdrew the reporter assignment: no student is designated
#: at any lab meeting, so there is nothing to draw. This flag is the guard and
#: `main()` stops on it, so running the script can never silently produce an
#: assignment that no longer applies to anybody. Everything below is kept
#: working and unchanged for a future edition that wants assigned reporters
#: back: set this to True and the draw runs exactly as it did under D74.
DRAW_ENABLED = False

# Slots whose reporter was ALREADY ANNOUNCED to the class and is therefore
# frozen. The first draw (5 students, 2026-08-22) was posted before the roster
# grew to 7 on 2026-08-25; it has since settled back at 6 (D71, a same-size
# swap). Week 2's two lectures are days away and those two
# students are already preparing, so they keep their dates; slots 3+ are redrawn
# across the full roster. Keyed by slot number, valued by roster `display_name`.
# The names were drawn while the job was still called Student Research Lead;
# D74 renamed the job, not the draw, so the locks stand as they are. D75 then
# withdrew the assignment altogether, so nothing is locked in practice this
# edition: these two names are kept, untouched, for the future edition that
# turns DRAW_ENABLED back on.
LOCKED = {
    1: "Erika Chiommino",      # Mon Aug 31 - Week 2 Monday
    2: "Aren Dominic Damayo",  # Wed Sep 2  - Week 2 Wednesday
}


#: The schedule CSV still names these columns `srl_slot` / `srl_focus`: the
#: draw and the column names both predate D74's rename. The newer names are
#: accepted too, so a future schedule build can rename the columns without
#: breaking the draw.
SLOT_COLUMNS = ("srl_slot", "lab_meeting_slot", "reporter_slot")
FOCUS_COLUMNS = ("srl_focus", "lab_meeting_focus", "reporter_focus")


def cell(row: dict, names: tuple[str, ...]) -> str:
    """First non-empty value among `names`, so old and new headers both work."""
    for n in names:
        v = (row.get(n) or "").strip()
        if v:
            return v
    return ""


def load_slots() -> list[dict]:
    """Every Mon/Wed meeting carrying a lab-meeting slot, in calendar order."""
    with SCHEDULE.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    slots = []
    for r in rows:
        raw = cell(r, SLOT_COLUMNS)
        if not raw:
            continue
        m = re.search(r"slot\s*(\d+)", raw, re.I)
        if not m:
            raise SystemExit(
                f"unparseable slot column on meeting {r['meeting']}: {raw!r}")
        week = re.match(r"Week (\d+)", r["unit"])
        slots.append(
            {
                "slot": int(m.group(1)),
                "meeting": int(r["meeting"]),
                "date": r["date"],
                "day": r["day"],
                "week": int(week.group(1)) if week else 0,
                "unit": r["unit"],
                "title": r["title"],
                "focus": cell(r, FOCUS_COLUMNS),
            }
        )
    slots.sort(key=lambda s: s["slot"])
    expected = list(range(1, len(slots) + 1))
    if [s["slot"] for s in slots] != expected:
        raise SystemExit("lab-meeting slot numbers are not a contiguous 1..N run")
    return slots


def load_roster() -> list[dict]:
    if not ROSTER.exists():
        raise SystemExit(
            f"roster not found: {ROSTER}\n"
            "Consolidate it first (see _adm/roster/README.md). FERPA: never "
            "move this file out of _adm/."
        )
    with ROSTER.open(newline="") as fh:
        students = list(csv.DictReader(fh))
    if not students:
        raise SystemExit("roster is empty")
    return sorted(students, key=lambda s: int(s["sort_key"]))


def valid(assignment: list[int], slots: list[dict], quota: list[int]) -> bool:
    n = len(quota)
    counts = [0] * n
    for who in assignment:
        counts[who] += 1
    if counts != quota:
        return False
    for i in range(1, len(assignment)):
        if assignment[i] == assignment[i - 1]:
            return False                                   # consecutive slots
        if (
            slots[i]["week"] == slots[i - 1]["week"]
            and assignment[i] == assignment[i - 1]
        ):
            return False                                   # same week twice
    half = len(slots) / 2
    for who in range(n):
        mine = [i for i, a in enumerate(assignment) if a == who]
        if not (any(i < half for i in mine) and any(i >= half for i in mine)):
            return False                                   # semester spread
    return True


def locked_positions(
    slots: list[dict], students: list[dict], honour: bool
) -> dict[int, int]:
    """Map slot POSITION -> student index for every frozen slot."""
    if not honour:
        return {}
    by_name = {s["display_name"]: i for i, s in enumerate(students)}
    fixed: dict[int, int] = {}
    for pos, slot in enumerate(slots):
        name = LOCKED.get(slot["slot"])
        if name is None:
            continue
        if name not in by_name:
            raise SystemExit(
                f"slot {slot['slot']} is locked to {name!r}, who is not on the "
                "roster; update LOCKED or the roster before drawing."
            )
        fixed[pos] = by_name[name]
    return fixed


def draw(
    slots: list[dict], n_students: int, seed: int, fixed: dict[int, int]
) -> tuple[list[int], list[int]]:
    """Return the assignment and the per-student report quota it satisfies."""
    base, extra = divmod(len(slots), n_students)
    if base == 0:
        raise SystemExit(
            f"{len(slots)} slots cannot give every one of {n_students} students "
            "a report; the lab meeting needs at least one slot per student."
        )
    rng = random.Random(seed)
    for _ in range(MAX_TRIES):
        # The remainder is drawn, not assigned: shuffle the roster and hand the
        # `extra` additional reports to whoever comes out in front.
        order = list(range(n_students))
        rng.shuffle(order)
        quota = [0] * n_students
        for rank, who in enumerate(order):
            quota[who] = base + (1 if rank < extra else 0)

        pool = [who for who in range(n_students) for _ in range(quota[who])]
        for who in fixed.values():
            if who not in pool:            # this quota cannot honour the locks
                break
            pool.remove(who)
        else:
            rng.shuffle(pool)
            free = iter(pool)
            candidate = [
                fixed[pos] if pos in fixed else next(free)
                for pos in range(len(slots))
            ]
            if valid(candidate, slots, quota):
                return candidate, quota
    raise SystemExit(
        f"no assignment satisfied the constraints in {MAX_TRIES} draws; "
        "relax a constraint or change the seed"
    )


def main() -> int:
    if not DRAW_ENABLED:
        print(
            "D75 (2026-08-31) withdrew the lab-meeting reporter assignment.\n"
            "\n"
            "The ten-minute lab meeting still opens every Mon/Wed lecture, but\n"
            "NO student is designated as its reporter, on any lecture, ever.\n"
            "There is no draw, no assigned question or request, and no\n"
            "preparation before class by anybody: the instructor asks the room\n"
            "how the projects are going and the room answers, and from minute 10\n"
            "the instructor leads the lesson. Nothing said there is graded.\n"
            "\n"
            "So nothing was drawn and nothing was written. Any assignment still\n"
            "sitting in _adm/roster/ is the withdrawn D74 draw: kept on file, and\n"
            "binding on nobody.\n"
            "\n"
            "The whole draw is preserved below this guard, unchanged. To\n"
            "reinstate it for a future edition that wants assigned reporters\n"
            "back, set DRAW_ENABLED = True at the top of this file."
        )
        return 0

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--dry-run", action="store_true", help="print, do not write")
    ap.add_argument(
        "--ignore-locks",
        action="store_true",
        help="redraw every slot, including the already-announced ones in LOCKED",
    )
    args = ap.parse_args()

    slots = load_slots()
    students = load_roster()
    fixed = locked_positions(slots, students, honour=not args.ignore_locks)
    assignment, quota = draw(slots, len(students), args.seed, fixed)

    rows = []
    for slot, who in zip(slots, assignment):
        s = students[who]
        rows.append(
            {
                "slot": slot["slot"],
                "meeting": slot["meeting"],
                "date": slot["date"],
                "day": slot["day"],
                "week": slot["week"],
                "student_index": s["sort_key"],
                "student": s["display_name"],
                "email": s["email"],
                "prep_due": "",
                "locked": "yes" if slot["slot"] in LOCKED else "no",
                "unit": slot["unit"],
                "title": slot["title"],
            }
        )

    # Everything from here down is the withdrawn D74 arrangement, unreachable
    # while DRAW_ENABLED is False and kept verbatim. It still names the 📣 My
    # Report Plan cell, which D75 removed from every notebook, so an edition
    # that re-enables the draw has to restore that cell or reword this output.
    # `prep_due` is the CALENDAR DAY BEFORE the lecture: the day the reporter's
    # 📣 My Report Plan cell should be filled in (D66's day-before cadence, kept).
    # Under D74 nothing is handed in on that date. The plan travels inside the
    # lecture notebook, which every student submits weekly on completion
    # (Lecture Notebooks, 20%). No class-day snapping: a Sunday or a holiday is
    # fine, and every slot lands on lecture minus one. The column keeps its name
    # so the packet builder and the draw already on disk still line up.
    import datetime

    for r in rows:
        d = datetime.date.fromisoformat(r["date"])
        r["prep_due"] = (d - datetime.timedelta(days=1)).isoformat()

    if args.dry_run:
        for r in rows:
            print(f"slot {r['slot']:>2} · {r['date']} {r['day']} · {r['student']}")
        return 0

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    counts = sorted({quota[i] for i in range(len(students))})
    spread = (
        f"{counts[0]} each"
        if len(counts) == 1
        else f"{counts[0]} or {counts[-1]} each "
        f"({quota.count(counts[-1])} students report {counts[-1]} times)"
    )
    locked_note = (
        "Every slot was drawn fresh."
        if not fixed
        else "🔒 marks a slot that was **already announced** and therefore frozen "
        "through the redraw: slots "
        + ", ".join(str(slots[pos]["slot"]) for pos in sorted(fixed))
        + " keep the students the class was given."
    )
    lines = [
        "# Lab meeting reporter assignment — HONR 46400-002, Fall 2026",
        "",
        "🚨 **FERPA — student data. Never commit, never publish.** Distribute each",
        "student's own slots through the course platform, not the course site.",
        "",
        "D74 retired the Student Research Lead role; this same draw now names each",
        "lecture's **lab meeting reporter**, who spends 7 minutes on a decision from",
        "their own project and 3 minutes on the room's questions. The report is not",
        "graded, and the draw was not re-run for D74.",
        "",
        f"Drawn with `scripts/assign_srl_slots.py --seed {args.seed}` on the",
        f"{len(slots)} Mon/Wed lectures that carry a lab meeting, across "
        f"{len(students)} students, {spread}.",
        "Constraints: no consecutive slots, never both lectures of one week, and",
        "every student reports in both halves of the semester. Where the slots do",
        "not divide evenly, the students carrying the extra report were drawn at",
        "random with the rest of the assignment.",
        "",
        locked_note,
        "",
        "\"Plan ready by\" is the day before, when the reporter's 📣 My Report Plan",
        "cell should be filled in. Nothing is handed in that day: the plan travels",
        "inside the lecture notebook, submitted weekly on completion.",
        "",
        "| Slot | Date | Day | Week | Reporter | Plan ready by | Lecture |",
        "|---:|---|---|---:|---|---|---|",
    ]
    for r in rows:
        mark = " 🔒" if r["locked"] == "yes" else ""
        lines.append(
            f"| {r['slot']}{mark} | {r['date']} | {r['day']} | {r['week']} | "
            f"{r['student']} | {r['prep_due']} | {r['title'][:70]} |"
        )
    lines += ["", "## Per student", ""]
    for s in students:
        mine = [r for r in rows if r["student_index"] == s["sort_key"]]
        dates = ", ".join(f"{r['date']} (slot {r['slot']})" for r in mine)
        lines.append(f"- **{s['display_name']}** ({len(mine)} reports) — {dates}")
    lines.append("")
    OUT_MD.write_text("\n".join(lines))

    print(f"✓ {len(rows)} slots assigned across {len(students)} students")
    print(f"  {OUT_CSV.relative_to(ROOT)}")
    print(f"  {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
