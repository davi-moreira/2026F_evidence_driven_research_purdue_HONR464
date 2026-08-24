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
  1. Every student leads exactly `len(slots) // n_students` lectures.
  2. No student leads two consecutive leadable slots.
  3. No student leads both lectures of the same week.
  4. Each student's slots spread across the semester: at least one in the
     first half and one in the second.

Usage:
    .venv/bin/python scripts/assign_srl_slots.py
    .venv/bin/python scripts/assign_srl_slots.py --seed 464 --dry-run
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


def valid(assignment: list[int], slots: list[dict], n: int, per: int) -> bool:
    counts = [0] * n
    for who in assignment:
        counts[who] += 1
    if any(c != per for c in counts):
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


def draw(slots: list[dict], n_students: int, seed: int) -> list[int]:
    per = len(slots) // n_students
    if per * n_students != len(slots):
        raise SystemExit(
            f"{len(slots)} slots do not divide evenly among {n_students} "
            "students; decide the remainder policy before drawing."
        )
    rng = random.Random(seed)
    pool = [who for who in range(n_students) for _ in range(per)]
    for _ in range(MAX_TRIES):
        candidate = pool[:]
        rng.shuffle(candidate)
        if valid(candidate, slots, n_students, per):
            return candidate
    raise SystemExit(
        f"no assignment satisfied the constraints in {MAX_TRIES} draws; "
        "relax a constraint or change the seed"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--dry-run", action="store_true", help="print, do not write")
    args = ap.parse_args()

    slots = load_slots()
    students = load_roster()
    assignment = draw(slots, len(students), args.seed)

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

    lines = [
        "# SRL slot assignment — HONR 46400-002, Fall 2026",
        "",
        "🚨 **FERPA — student data. Never commit, never publish.** Distribute each",
        "student's own slots through the course platform, not the course site.",
        "",
        f"Drawn with `scripts/assign_srl_slots.py --seed {args.seed}` on the",
        f"{len(slots)} leadable Mon/Wed lectures, {len(slots)//len(students)} per student.",
        "Constraints: no consecutive slots, never both lectures of one week, and",
        "every student leads in both halves of the semester.",
        "",
        "| Slot | Date | Day | Week | Lead | Prep due | Lecture |",
        "|---:|---|---|---:|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['slot']} | {r['date']} | {r['day']} | {r['week']} | "
            f"{r['student']} | {r['prep_due']} | {r['title'][:70]} |"
        )
    lines += ["", "## Per student", ""]
    for s in students:
        mine = [r for r in rows if r["student_index"] == s["sort_key"]]
        dates = ", ".join(f"{r['date']} (slot {r['slot']})" for r in mine)
        lines.append(f"- **{s['display_name']}** — {dates}")
    lines.append("")
    OUT_MD.write_text("\n".join(lines))

    print(f"✓ {len(rows)} slots assigned across {len(students)} students")
    print(f"  {OUT_CSV.relative_to(ROOT)}")
    print(f"  {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
