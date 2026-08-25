#!/usr/bin/env python3
"""Draw the Student Research Lead slot assignment for the semester.

The SRL system assigns every leadable Mon/Wed lecture to one student at the
start of the semester -- randomly, with no rotation and no seats (D22). This
script performs that draw reproducibly.

FERPA: the roster is student data. It lives in the gitignored `_adm/roster/`
and is read at run time; this script carries no names, and its output is
written back into `_adm/` so the assignment is never committed or published.
Students learn their own slots through the course platform, not the site.

Fairness constraints, all enforced by rejection sampling:
  1. Lead counts are as even as the roster allows. When the slots do not
     divide evenly, `len(slots) % n_students` students carry one extra lead
     and WHICH students those are is itself drawn at random, so the remainder
     is not handed out by name, by seniority, or by enrolment date.
  2. No student leads two consecutive leadable slots.
  3. No student leads both lectures of the same week.
  4. Each student's slots spread across the semester: at least one in the
     first half and one in the second.

Locked slots (`LOCKED`): a slot already announced to the class is frozen and
excluded from the redraw, so a late roster change never moves a date a student
has already been told to prepare. Everything after the locked slots is redrawn
from scratch.

Usage:
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

# Slots whose lead was ALREADY ANNOUNCED to the class and is therefore frozen.
# The first draw (5 students, 2026-08-22) was posted before the roster grew to
# 7 on 2026-08-25. Week 2's two lectures are days away and their leads are
# already preparing, so they keep their dates; slots 3+ are redrawn across the
# full roster. Keyed by slot number, valued by roster `display_name`.
LOCKED = {
    1: "Erika Chiommino",      # Mon Aug 31 - Week 2 Monday
    2: "Aren Dominic Damayo",  # Wed Sep 2  - Week 2 Wednesday
}


def load_slots() -> list[dict]:
    """Every Mon/Wed meeting carrying an SRL slot, in calendar order."""
    with SCHEDULE.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    slots = []
    for r in rows:
        raw = (r.get("srl_slot") or "").strip()
        if not raw:
            continue
        m = re.search(r"slot\s*(\d+)", raw, re.I)
        if not m:
            raise SystemExit(f"unparseable srl_slot on meeting {r['meeting']}: {raw!r}")
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
                "focus": (r.get("srl_focus") or "").strip(),
            }
        )
    slots.sort(key=lambda s: s["slot"])
    expected = list(range(1, len(slots) + 1))
    if [s["slot"] for s in slots] != expected:
        raise SystemExit("SRL slot numbers are not a contiguous 1..N run")
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
    """Return the assignment and the per-student lead quota it satisfies."""
    base, extra = divmod(len(slots), n_students)
    if base == 0:
        raise SystemExit(
            f"{len(slots)} slots cannot give every one of {n_students} students "
            "a lead; the SRL design needs at least one slot per student."
        )
    rng = random.Random(seed)
    for _ in range(MAX_TRIES):
        # The remainder is drawn, not assigned: shuffle the roster and hand the
        # `extra` additional leads to whoever comes out in front.
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

    # The filled notebook is due at 11:59 PM the CALENDAR DAY BEFORE the lecture
    # (D66, adopted from the course-platform dates, superseding D18's two days).
    # No class-day snapping: the deadline is a submission time, not a meeting,
    # so a Sunday or a holiday due date is fine and every slot lands on
    # lecture minus one.
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
        f"({quota.count(counts[-1])} students lead {counts[-1]} times)"
    )
    locked_note = (
        "Every slot was drawn fresh."
        if not fixed
        else "🔒 marks a slot that was **already announced** and therefore frozen "
        "through the redraw: slots "
        + ", ".join(str(slots[pos]["slot"]) for pos in sorted(fixed))
        + " keep the leads the class was given."
    )
    lines = [
        "# SRL slot assignment — HONR 46400-002, Fall 2026",
        "",
        "🚨 **FERPA — student data. Never commit, never publish.** Distribute each",
        "student's own slots through the course platform, not the course site.",
        "",
        f"Drawn with `scripts/assign_srl_slots.py --seed {args.seed}` on the",
        f"{len(slots)} leadable Mon/Wed lectures across {len(students)} students, "
        f"{spread}.",
        "Constraints: no consecutive slots, never both lectures of one week, and",
        "every student leads in both halves of the semester. Where the slots do",
        "not divide evenly, the students carrying the extra lead were drawn at",
        "random with the rest of the assignment.",
        "",
        locked_note,
        "",
        "| Slot | Date | Day | Week | Lead | Prep due | Lecture |",
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
        lines.append(f"- **{s['display_name']}** ({len(mine)} leads) — {dates}")
    lines.append("")
    OUT_MD.write_text("\n".join(lines))

    print(f"✓ {len(rows)} slots assigned across {len(students)} students")
    print(f"  {OUT_CSV.relative_to(ROOT)}")
    print(f"  {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
