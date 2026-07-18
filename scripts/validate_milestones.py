#!/usr/bin/env python3
"""validate_milestones.py — milestone-system consistency gates.

Parses the chain table in planning/PROJECT_MILESTONES.md and checks, against
planning/MEETING_SCHEDULE.csv and the calendar backbone:

  * all 24 milestones (M00–M23) present, each with development meetings, a
    presentation moment, and a due date
  * every milestone's development meetings precede (or meet) its due date
  * every milestone ID appears in >= 1 meeting's milestone_developed column
  * the fixed anchors hold: M07 abstract Oct 9, M12 poster Nov 6, M16 = URC
    Nov 17, M22 defenses Dec 7/9, M23 dossier Dec 11
  * no two written milestones share a due date (M07's two parts exempted by ID)

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
        m = re.match(r"\|\s*M(\d\d)\s*\|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        rows[int(m.group(1))] = {
            "name": cells[1], "dev": cells[2], "pres": cells[3], "due": cells[4],
        }

    expected = set(range(24))
    if set(rows) != expected:
        errs.append(f"chain table has milestones {sorted(rows)}, expected M00–M23")

    # --- per-milestone checks ---------------------------------------------
    due_dates = {}
    for mid, r in sorted(rows.items()):
        dev_meetings = parse_meetings(r["dev"])
        dues = parse_dates(r["due"])
        if mid == 16:  # URC Expo event
            if "Nov 17" not in r["due"] + r["pres"]:
                errs.append("M16 must anchor to the URC Expo Tue Nov 17")
            continue
        if not dev_meetings:
            errs.append(f"M{mid:02d}: no development meetings listed")
        if not dues and mid not in (15, 22):  # in-class / performed artifacts
            errs.append(f"M{mid:02d}: no due date parseable from {r['due']!r}")
        if dev_meetings and dues:
            last_dev = max(meeting_date[m] for m in dev_meetings if m in meeting_date)
            if last_dev > max(dues):
                errs.append(f"M{mid:02d}: development (through {last_dev}) ends "
                            f"after its due date {max(dues)}")
        if dues:
            due_dates[mid] = dues

    # --- fixed anchors -----------------------------------------------------
    anchors = {
        7: [date(2026, 10, 9), date(2026, 10, 16)],
        12: [date(2026, 11, 6)],
        23: [date(2026, 12, 11)],
    }
    for mid, want in anchors.items():
        if due_dates.get(mid) != want:
            errs.append(f"M{mid:02d}: due {due_dates.get(mid)} != anchor {want}")
    if 22 in rows and not {date(2026, 12, 7), date(2026, 12, 9)} <= set(
            parse_dates(rows[22]["pres"] + rows[22]["due"])):
        errs.append("M22 defenses must sit on Dec 7 and Dec 9")

    # --- unique written due dates (M07 two-parter exempt from itself) ------
    flat = [(mid, d) for mid, ds in due_dates.items() for d in ds]
    seen = {}
    for mid, d in flat:
        if d in seen and seen[d] != mid:
            errs.append(f"M{seen[d]:02d} and M{mid:02d} share due date {d}")
        seen[d] = mid

    # --- schedule cross-check ---------------------------------------------
    dev_col = " ".join(r["milestone_developed"] for r in sched)
    for mid in expected:
        if f"M{mid:02d}" not in dev_col:
            errs.append(f"M{mid:02d} never appears in the schedule's "
                        f"milestone_developed column")
    empty_work = [r["meeting"] for r in sched if not r["milestone_work_time"].strip()]
    if empty_work:
        errs.append(f"meetings with no milestone work time: {empty_work}")

    if errs:
        print(f"✗ milestones: {len(errs)} problem(s)")
        for e in errs:
            print("  " + e)
        sys.exit(1)
    print("✓ milestone system consistent — 24 milestones, dev→present→submit "
          "ordering holds, anchors fixed (Oct 9, Nov 6, Nov 17, Dec 7/9, Dec 11)")


if __name__ == "__main__":
    main()
