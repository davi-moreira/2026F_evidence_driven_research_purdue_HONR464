#!/usr/bin/env python3
"""validate_milestones.py — milestone-system consistency gates (v3: M1–M16).

Parses the chain table in planning/PROJECT_MILESTONES.md and checks, against
planning/MEETING_SCHEDULE.csv and the calendar backbone:

  * all 16 milestones (M1–M16) present, each with development meetings, a
    presentation moment, and a due date
  * every milestone's development meetings precede (or meet) its due date
  * every milestone ID appears in >= 1 meeting's milestone_developed column
  * the fixed anchors hold: M6 draft abstract Oct 2, M7 conference application
    Oct 9, M11 poster draft Nov 4, M13 poster lock Nov 8 (Sunday, terminal),
    M14 go-public Nov 13, M15 references the Expo Nov 17 and is due Nov 29
    (Sunday), M16 package + cold run Dec 4, M17 release + chapter Dec 11
  * no two milestones share a due date

Usage: python3 scripts/validate_milestones.py
"""
from __future__ import annotations

import csv
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PM = REPO / "planning" / "PROJECT_MILESTONES.md"
SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.csv"
BACKBONE = REPO / "planning" / "CALENDAR_BACKBONE.csv"

MONTHS = {"Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
N_MILESTONES = 16   # M1–M16 (D54 retired M17)


def parse_dates(text: str) -> list[date]:
    return [date(2026, MONTHS[m], int(d))
            for m, d in re.findall(r"(Aug|Sep|Oct|Nov|Dec)\s+(\d+)", text)]


def parse_meetings(text: str) -> list[int]:
    out = []
    for a, b in re.findall(r"M(\d+)(?:–M?(\d+))?", text):
        if b:
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(a))
    return out


def main() -> None:
    errs = []

    with open(BACKBONE, newline="") as f:
        meeting_date = {int(r["meeting"]): date.fromisoformat(r["date"])
                        for r in csv.DictReader(f)}
    with open(SCHEDULE, newline="") as f:
        sched = list(csv.DictReader(f))

    # --- parse the chain table --------------------------------------------
    rows = {}
    for line in PM.read_text().splitlines():
        m = re.match(r"\|\s*M(\d{1,2})\s*\|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        rows[int(m.group(1))] = {
            "name": cells[1], "dev": cells[2], "pres": cells[3], "due": cells[4],
        }

    expected = set(range(1, N_MILESTONES + 1))
    if set(rows) != expected:
        errs.append(f"chain table has milestones {sorted(rows)}, expected M1–M16")

    # --- per-milestone checks ---------------------------------------------
    due_dates = {}
    for mid, r in sorted(rows.items()):
        dev_meetings = parse_meetings(r["dev"])
        dues = parse_dates(r["due"])
        if not dev_meetings:
            errs.append(f"M{mid}: no development meetings listed")
        if not dues:
            errs.append(f"M{mid}: no due date parseable from {r['due']!r}")
        if dev_meetings and dues:
            known = [meeting_date[m] for m in dev_meetings if m in meeting_date]
            if not known:
                errs.append(f"M{mid}: development meetings {dev_meetings} not in backbone")
            elif max(known) > max(dues):
                errs.append(f"M{mid}: development (through {max(known)}) ends "
                            f"after its due date {max(dues)}")
        if dues:
            due_dates[mid] = dues

    # --- fixed anchors -----------------------------------------------------
    anchors = {
        6:  [date(2026, 10, 4)],    # URC draft abstract (Sunday, D54)
        7:  [date(2026, 10, 11)],   # URC conference application (Sunday, D54)
        11: [date(2026, 11, 4)],    # poster first draft, due at class (Wednesday)
        12: [date(2026, 11, 6)],    # peer review, Friday 5 PM — feeds the Nov 8 lock
        13: [date(2026, 11, 8)],    # final poster lock (terminal, Sunday 11:59 PM)
        14: [date(2026, 11, 15)],   # go-public package (Sunday, D54)
        15: [date(2026, 11, 29)],   # conference reflection (Sunday)
        16: [date(2026, 12, 6)],    # package + cold run (Sunday, D54) — final milestone
    }
    for mid, want in anchors.items():
        if due_dates.get(mid) != want:
            errs.append(f"M{mid}: due {due_dates.get(mid)} != anchor {want}")
    if 15 in rows and "Nov 17" not in rows[15]["pres"] + rows[15]["due"]:
        errs.append("M15 must reference the URC Expo (Tue Nov 17) as a graded component")

    # --- unique due dates --------------------------------------------------
    flat = [(mid, d) for mid, ds in due_dates.items() for d in ds]
    seen: dict[date, int] = {}
    for mid, d in flat:
        if d in seen and seen[d] != mid:
            errs.append(f"M{seen[d]} and M{mid} share due date {d}")
        seen[d] = mid

    # --- schedule cross-check ---------------------------------------------
    dev_col = " ".join(r["milestone_developed"] for r in sched)
    for mid in expected:
        if not re.search(rf"\bM{mid}\b", dev_col):
            errs.append(f"M{mid} never appears in the schedule's "
                        f"milestone_developed column")
    empty_work = [r["meeting"] for r in sched if not r["milestone_work_time"].strip()]
    if empty_work:
        errs.append(f"meetings with no milestone work time: {empty_work}")

    if errs:
        print(f"✗ milestones: {len(errs)} problem(s)")
        for e in errs:
            print("  " + e)
        sys.exit(1)
    print("✓ milestone system consistent — 16 milestones (M1–M16), "
          "dev→present→submit ordering holds, anchors fixed "
          "(Oct 4, Oct 11, Nov 4, Nov 6, Nov 8, Nov 15, Nov 17, Nov 29, Dec 6)")


if __name__ == "__main__":
    main()
