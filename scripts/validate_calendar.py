#!/usr/bin/env python3
"""
validate_calendar.py — Authoritative Fall 2026 MWF calendar for HONR 46400.

This script is the single source of truth for the meeting backbone. It generates
every Monday/Wednesday/Friday class date from the first day of classes through the
last class, removes the official no-class days, flags the asynchronous-online
meetings and the external events (URC Expo, poster deadline), and PROGRAMMATICALLY
VERIFIES the counts the course design depends on:

    43 total scheduled MWF meetings  =  41 in-person  +  2 asynchronous-online

Run it as a gate before shipping the schedule:

    python3 scripts/validate_calendar.py            # print the report, verify counts
    python3 scripts/validate_calendar.py --emit-csv # also (re)write planning/CALENDAR_BACKBONE.csv

Exit code is non-zero if any invariant fails, so CI / pre-commit can rely on it.

Source of dates: HONR 46400 design brief (2026-07-17), anchored to the Purdue
Fall 2026 academic calendar. The confirmed URC *abstract* submission deadline is
still TBD (tracked separately); the URC *Expo* date below is fixed.
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

# --- Fixed anchors from the design brief -----------------------------------
FIRST_DAY = date(2026, 8, 24)   # Monday — classes begin
LAST_DAY = date(2026, 12, 11)   # Friday — last MWF meeting
MWF = {0, 2, 4}                 # Monday=0, Wednesday=2, Friday=4

# Official no-class days that fall on an MWF (removed from the meeting list).
HOLIDAYS: dict[date, str] = {
    date(2026, 9, 7):  "Labor Day — no class",
    date(2026, 10, 12): "October Break — no class",
    date(2026, 11, 18): "Post-Expo day — no class (course design: conference was Tuesday)",
    date(2026, 11, 25): "Thanksgiving recess — no class",
    date(2026, 11, 27): "Thanksgiving recess — no class",
}

#: Student-facing wording for the same days, used by every artifact that PRINTS
#: the calendar (the Schedule page, the schedule .docx, the syllabus .docx).
#: HOLIDAYS above is the machine truth; this is how a student reads it. Keeping
#: both here stops the printed surfaces from disagreeing with the backbone — they
#: did once, and nothing caught it because each surface owned its own copy.
PUBLIC_NO_CLASS_LABEL: dict[date, str] = {
    date(2026, 9, 7):  "No class — Labor Day",
    date(2026, 10, 12): "No class — October Break (fall break)",
    date(2026, 11, 18): "No class — the day after the Expo, to rest and catch up",
    date(2026, 11, 25): "No class — Thanksgiving Break",
    date(2026, 11, 27): "No class — Thanksgiving Break",
}
assert set(PUBLIC_NO_CLASS_LABEL) == set(HOLIDAYS), (
    "PUBLIC_NO_CLASS_LABEL and HOLIDAYS must cover exactly the same days")


def no_class_days() -> dict[str, str]:
    """ISO date -> student-facing no-class label, for the printed calendars."""
    return {d.isoformat(): text for d, text in sorted(PUBLIC_NO_CLASS_LABEL.items())}


# MWF meetings that are held fully asynchronously online.
#
# The dates are OWNED by course_config.yaml `calendar.async_meetings`; the
# labels live here. Reading them instead of hardcoding is deliberate: the two
# silently disagreed once (config listed 2026-10-02 as async long after the
# ruling that made it a regular in-person studio), and this validator passed
# green throughout because it only ever checked itself.
ASYNC_LABELS: dict[date, str] = {
    date(2026, 11, 20): "Asynchronous online (post-Expo audience-data capture)",
    date(2026, 11, 23): "Asynchronous online (Thanksgiving reflection module)",
}


def _async_days() -> dict[date, str]:
    """Async meeting dates from course_config.yaml, labelled from ASYNC_LABELS."""
    cfg = Path(__file__).resolve().parent.parent / "course_config.yaml"
    declared = yaml.safe_load(cfg.read_text())["calendar"]["async_meetings"]
    days: dict[date, str] = {}
    for iso in declared:
        d = date.fromisoformat(iso)
        if d not in ASYNC_LABELS:
            raise SystemExit(
                f"✗ course_config.yaml declares {iso} async but scripts/validate_calendar.py\n"
                f"  has no label for it. Add one to ASYNC_LABELS, or drop the date from\n"
                f"  calendar.async_meetings — do not let the two disagree."
            )
        days[d] = ASYNC_LABELS[d]
    # EVERY declared count must match the backbone, not only the async list
    # (round-8 P2 + round-9 N4: in_person stayed 41 after the de-asyncing, and
    # total_meetings could drift to 44, while this gate stayed green).
    cal = yaml.safe_load(cfg.read_text())["calendar"]
    declared_total = cal.get("total_meetings")
    if declared_total is not None and declared_total != 43:
        raise SystemExit(
            f"✗ course_config.yaml calendar.total_meetings = {declared_total}, "
            f"but the backbone has 43 scheduled meetings.")
    declared_inperson = cal.get("in_person")
    if declared_inperson is not None and declared_inperson != 43 - len(days):
        raise SystemExit(
            f"✗ course_config.yaml calendar.in_person = {declared_inperson}, "
            f"but 43 total - {len(days)} async = {43 - len(days)} in-person.")
    return days


ASYNC_DAYS: dict[date, str] = _async_days()

# External / non-MWF events that belong on the master schedule as rows even
# though they are not ordinary class meetings.
EVENTS: dict[date, str] = {
    date(2026, 11, 8):  "FINAL POSTER LOCK, Sunday 11:59 PM — terminal (M13); shared print run with QM 47400",
    date(2026, 11, 17): "Purdue Fall Undergraduate Research Expo — REQUIRED poster presentation (Tuesday, not MWF)",
}

# Invariants the whole course design relies on.
EXPECT_TOTAL = 43
EXPECT_INPERSON = 41   # D50: Fri Nov 20 became asynchronous
EXPECT_ASYNC = 2   # D50: Fri Nov 20 + Mon Nov 23


def generate_meetings() -> list[dict]:
    """Return the ordered list of scheduled MWF meetings with modality metadata."""
    meetings: list[dict] = []
    d = FIRST_DAY
    n = 0
    while d <= LAST_DAY:
        if d.weekday() in MWF and d not in HOLIDAYS:
            n += 1
            modality = "async-online" if d in ASYNC_DAYS else "in-person"
            meetings.append(
                {
                    "meeting": n,
                    "date": d.isoformat(),
                    "day": d.strftime("%a"),
                    "modality": modality,
                    "note": ASYNC_DAYS.get(d, ""),
                }
            )
        d += timedelta(days=1)
    return meetings


def verify(meetings: list[dict]) -> list[str]:
    """Return a list of invariant-violation messages (empty == all good)."""
    errors: list[str] = []
    total = len(meetings)
    inperson = sum(m["modality"] == "in-person" for m in meetings)
    asyncs = sum(m["modality"] == "async-online" for m in meetings)

    if total != EXPECT_TOTAL:
        errors.append(f"expected {EXPECT_TOTAL} total meetings, got {total}")
    if inperson != EXPECT_INPERSON:
        errors.append(f"expected {EXPECT_INPERSON} in-person meetings, got {inperson}")
    if asyncs != EXPECT_ASYNC:
        errors.append(f"expected {EXPECT_ASYNC} async meetings, got {asyncs}")
    if meetings and meetings[0]["date"] != FIRST_DAY.isoformat():
        errors.append(f"first meeting is {meetings[0]['date']}, expected {FIRST_DAY.isoformat()}")
    if meetings and meetings[-1]["date"] != LAST_DAY.isoformat():
        errors.append(f"last meeting is {meetings[-1]['date']}, expected {LAST_DAY.isoformat()}")
    for h in HOLIDAYS:
        if any(m["date"] == h.isoformat() for m in meetings):
            errors.append(f"holiday {h.isoformat()} wrongly appears as a meeting")
    for a in ASYNC_DAYS:
        if not any(m["date"] == a.isoformat() and m["modality"] == "async-online" for m in meetings):
            errors.append(f"async day {a.isoformat()} missing or mis-flagged")
    return errors


def print_report(meetings: list[dict]) -> None:
    print("HONR 46400 — Fall 2026 MWF meeting backbone")
    print(f"  first class {FIRST_DAY.isoformat()} ({FIRST_DAY:%A})  ->  "
          f"last class {LAST_DAY.isoformat()} ({LAST_DAY:%A})")
    print(f"  {len(meetings)} meetings  "
          f"({sum(m['modality']=='in-person' for m in meetings)} in-person, "
          f"{sum(m['modality']=='async-online' for m in meetings)} async)\n")
    for m in meetings:
        tag = "  <async>" if m["modality"] == "async-online" else ""
        print(f"  M{m['meeting']:>2}  {m['date']}  {m['day']}  {m['modality']}{tag}")
    print("\n  Removed no-class MWF days:")
    for h, why in sorted(HOLIDAYS.items()):
        print(f"    {h.isoformat()} {h:%a} — {why}")
    print("\n  External events (schedule rows, not MWF meetings):")
    for e, why in sorted(EVENTS.items()):
        print(f"    {e.isoformat()} {e:%a} — {why}")


def emit_csv(meetings: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["meeting", "date", "day", "modality", "note"])
        w.writeheader()
        w.writerows(meetings)
    print(f"\n  wrote {path} ({len(meetings)} rows)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--emit-csv", action="store_true",
                    help="write planning/CALENDAR_BACKBONE.csv")
    ap.add_argument("--quiet", action="store_true", help="only report failures")
    args = ap.parse_args()

    meetings = generate_meetings()
    errors = verify(meetings)

    if not args.quiet:
        print_report(meetings)

    if args.emit_csv:
        repo = Path(__file__).resolve().parent.parent
        emit_csv(meetings, repo / "planning" / "CALENDAR_BACKBONE.csv")

    if errors:
        print("\nCALENDAR VALIDATION FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    if not args.quiet:
        print("\n✓ calendar invariants hold (43 = 41 in-person + 2 async).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
