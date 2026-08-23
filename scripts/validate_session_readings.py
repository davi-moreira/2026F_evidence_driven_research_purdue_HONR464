#!/usr/bin/env python3
"""validate_session_readings.py — the gate that keeps the published schedule's
readings equal to the book.

The course runs the book: Monday and Wednesday teach a Studio's lessons, Friday
is that Studio's milestone (D49). The schedule page therefore names, per
session, the chapters that session requires. Two things can silently rot:

  1. the per-session lesson sets can drift from COURSE_BOOK_CROSSWALK.yml, so
     the calendar assigns a chapter the milestone never collects (or misses one
     it does);
  2. course prose can paraphrase a chapter or a studio instead of using the
     wording published in the book.

This validator refuses both.

    A. every `book_reading` token names an ACTIVE lesson and a known mode
    B. per milestone, the `first-read` set == the crosswalk's *required* home
       anchors; `route`/`route-contrast` == its *route-required* home anchors;
       `optional` == its *optional* home anchors
    C. every `revisit` token is a revisit assignment the crosswalk carries for
       that milestone
    D. every `due` token is something that week actually read
    E. every `assigned` and every `continue` token is first-read in the same
       week (`assigned` before its read, `continue` after it)
    F. each Week 1-12 `unit` string carries its studio title AS PUBLISHED, and
       BOOK_ARCHITECTURE's station title equals the studio page's own `title:`

    .venv/bin/python scripts/validate_session_readings.py
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from book_manifest import load_architecture, load_crosswalk, require_lock  # noqa: E402
from session_readings import (by_mode, lesson_index, parse,  # noqa: E402
                              studio_titles)

CSV_PATH = REPO / "planning" / "MEETING_SCHEDULE.csv"


def crosswalk_sets() -> dict[str, dict[str, set[str]]]:
    """milestone -> {'required','route-required','optional','revisit'} sets."""
    out: dict[str, dict[str, set[str]]] = {}
    for r in load_crosswalk()["rows"]:
        d = {k: set() for k in
             ("required", "route-required", "optional", "revisit")}
        for a in r.get("assignments", []):
            if a.get("purpose") == "revisit":
                d["revisit"].add(a["lesson"])
            elif a.get("home_anchor"):
                d.setdefault(a["requirement"], set()).add(a["lesson"])
        # D54: a teaching-only row (Week 16) is keyed by its notebook instead.
        out[r.get("milestone") or f"nb:{r['nb']}"] = d
    return out


def main() -> int:
    require_lock()
    rows = list(csv.DictReader(open(CSV_PATH, newline="")))
    index = lesson_index()
    cw = crosswalk_sets()
    errors: list[str] = []

    # --- A. tokens resolve ------------------------------------------------
    for r in rows:
        for lid, _mode in parse(r["book_reading"]):
            if lid not in index:
                errors.append(f"meeting {r['meeting']}: {lid!r} is not an "
                              f"active lesson in BOOK_ARCHITECTURE.yml")

    # --- group meetings by milestone --------------------------------------
    weeks: dict[str, list[dict]] = {}
    nb_of_unit = {}
    for r in rows:
        m = re.match(r"\s*(M\d+)", r["milestone_developed"])
        if m:
            weeks.setdefault(m.group(1), []).append(r)
            continue
        # D54: Week 16 teaches Studio 12 with no milestone. Such meetings are
        # still reading-checked, keyed by the notebook their unit names.
        nb = re.search(r"\bnb(\d{2})\b", r["other_material"])
        if not nb:
            errors.append(f"meeting {r['meeting']}: no milestone id in "
                          f"milestone_developed and no nbNN in other_material")
            continue
        weeks.setdefault(f"nb:nb{nb.group(1)}", []).append(r)

    for mi, meetings in weeks.items():
        want = cw.get(mi)
        if want is None:
            errors.append(f"{mi}: no crosswalk row")
            continue
        got: dict[str, set[str]] = {}
        for r in meetings:
            for mode, ids in by_mode(r["book_reading"]).items():
                got.setdefault(mode, set()).update(ids)

        # --- B. first reads and route reads match the crosswalk exactly ----
        checks = [
            ("first-read", want["required"], "required home anchors"),
            ("route", want["route-required"], "route-required home anchors"),
            ("route-contrast", want["route-required"],
             "route-required home anchors"),
            ("optional", want["optional"], "optional home anchors"),
        ]
        for mode, expected, label in checks:
            have = got.get(mode, set())
            if have != expected:
                missing = sorted(expected - have)
                extra = sorted(have - expected)
                if missing or extra:
                    errors.append(
                        f"{mi}: {mode!r} set != the crosswalk's {label}"
                        + (f" — missing {missing}" if missing else "")
                        + (f" — unexpected {extra}" if extra else ""))

        # --- C. revisits are crosswalk revisits ---------------------------
        stray = sorted(got.get("revisit", set()) - want["revisit"])
        if stray:
            errors.append(f"{mi}: revisit of {stray} is not a revisit "
                          f"assignment in the crosswalk")

        # --- D. RETIRED with the `due` mode (D57) -------------------------
        # The "It is your turn" submission is a PARTICIPATION assignment due at
        # 11:59 PM on the chapter's own reading day, so it rides the read modes
        # and no longer needs a token of its own. Its deadline is generated
        # into planning/IYT_SUBMISSION_SCHEDULE.md from the same home anchors.

        # --- E. 'assigned' and 'continue' bracket a same-week first read ---
        #: A pathway lesson's first read is 'route' / 'route-contrast', and a
        #: conditional one's is 'optional', so a Friday 'continue' on the week's
        #: route shelf is legitimate (round D57).
        FIRST = ("first-read", "route", "route-contrast", "optional")
        first = set().union(*(got.get(k, set()) for k in FIRST)) if any(
            k in got for k in FIRST) else set()
        for mode in ("assigned", "continue"):
            for lid in got.get(mode, set()):
                if lid not in first:
                    errors.append(f"{mi}: {lid!r} is {mode!r} but never "
                                  f"first read in the same week")

    # --- F. studio wording is the book's ----------------------------------
    published = studio_titles()
    for rank, title in sorted(published.items()):
        page = REPO / "book" / "studios" / f"studio{rank:02d}-{_slug(rank)}.qmd"
        if page.exists():
            m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$',
                          page.read_text(), re.M)
            if m and m.group(1) != title:
                errors.append(
                    f"Studio {rank}: BOOK_ARCHITECTURE title {title!r} != the "
                    f"published studio page title {m.group(1)!r}")
    units = []
    for r in rows:
        if r["unit"] not in units:
            units.append(r["unit"])
    # D50: a studio's calendar week is no longer its rank. Studios 1-10 land on
    # Weeks 1-10, the conference block occupies Weeks 11-14, and Studios 11-12
    # run post-conference on Weeks 15-16. The mapping is READ from the crosswalk
    # (the week whose milestone fires that station's checkpoint), never assumed.
    station_rank = {s["id"]: s["rank"] for s in load_architecture()["stations"]}
    studio_week: dict[int, int] = {}
    for r in load_crosswalk().get("rows", []):
        for bm in r.get("book_milestones", []) or []:
            if bm.get("relationship") == "checkpoint":
                rank = station_rank.get(bm["station"])
                if rank is not None:
                    studio_week[rank] = int(str(r["nb"])[2:])
        # D54: a station taught without a graded checkpoint declares its week.
        taught = r.get("teaches_station")
        if taught and station_rank.get(taught) is not None:
            studio_week[station_rank[taught]] = int(str(r["nb"])[2:])
    for rank, title in sorted(published.items()):
        week = studio_week.get(rank, rank)
        unit = next((u for u in units if u.startswith(f"Week {week} —")), None)
        if unit is None:
            errors.append(f"Studio {rank}: no Week {week} unit in the schedule")
        elif unit != f"Week {week} — {title}":
            errors.append(f"Week {week} unit {unit!r} != the published studio "
                          f"title, which requires {f'Week {week} — {title}'!r}")

    if errors:
        print(f"✗ session readings INVALID — {len(errors)} problem(s):")
        for e in errors:
            print("   " + e)
        return 1
    n = sum(len(parse(r["book_reading"])) for r in rows)
    print(f"✓ session readings consistent — {len(rows)} meetings, {n} chapter "
          f"assignments, all matched to the crosswalk and to the book's own "
          f"published titles")
    return 0


def _slug(rank: int) -> str:
    from book_manifest import load_architecture
    for s in load_architecture()["stations"]:
        if s["rank"] == rank:
            return s["id"]
    raise SystemExit(f"✗ no station with rank {rank}")


if __name__ == "__main__":
    sys.exit(main())
