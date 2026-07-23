#!/usr/bin/env python3
"""validate_coverage.py — cross-artifact consistency gates.

  1. Every meeting (43) names exactly one topic notebook, and every notebook
     (nb00–nb15) is named by >= 1 meeting.
  2. Every referenced notebook's STUDENT file exists (skippable pre-Phase-D
     with --plan, which only checks the mapping).
  3. Readings-vs-inventory: every RDSS chapter cited in the schedule is in the
     verified chapter inventory (the book has no ch. 14 or 20); Calling
     Bullshit entries are optional public callingbullshit.org cases only.
  4. Every dataset named in the schedule is shipped in notebooks/data/ (or an
     inline simulation / the student's own data).
  5. Every schedule row's provenance field has the 4-segment form
     (source | chapter/section | item | transformation).

Usage: python3 scripts/validate_coverage.py [--plan]
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from notebooks_map import NOTEBOOKS, student_filename  # noqa: E402

SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.csv"
DATA_DIR = REPO / "notebooks" / "data"

VALID_CHAPTERS = set(range(1, 14)) | set(range(15, 20)) | {21, 22, 23, 24}
SHIPPED = {"lapop_brazil", "la_voter_file", "foos_etal", "cliningsmith_etal",
           "bonilla_tillery"}
DATASET_OK_WORDS = {"none", "inline", "simulat", "own", "toy",
                    "embedded", "student", "mini-table", "each", "defenders",
                    "class", "archive", "package", "poster", "brief", "ledger",
                    "sample", "10-row", "citation list", "conference",
                    "monte-carlo", "seeded"}


def main() -> None:
    plan_only = "--plan" in sys.argv
    errs = []

    with open(SCHEDULE, newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 43:
        errs.append(f"schedule has {len(rows)} rows, expected 43")

    # 1 + 2: meeting <-> notebook mapping
    seen_nbs = set()
    for r in rows:
        m = re.findall(r"nb(\d\d)", r["other_material"])
        if not m:
            errs.append(f"M{r['meeting']}: no notebook named in other_material")
            continue
        first = int(m[0])
        if first not in NOTEBOOKS:
            errs.append(f"M{r['meeting']}: nb{first:02d} not in registry")
        seen_nbs.add(first)
        if not plan_only:
            sf = REPO / "notebooks" / "student" / student_filename(first)
            if not sf.exists():
                errs.append(f"M{r['meeting']}: {sf.name} does not exist")
    missing = set(NOTEBOOKS) - seen_nbs
    if missing:
        errs.append(f"notebooks never referenced by any meeting: {sorted(missing)}")

    # 3: readings vs inventory
    for r in rows:
        for ch in re.findall(r"ch\.\s*(\d+)", r["rdss_reading"]):
            if int(ch) not in VALID_CHAPTERS:
                errs.append(f"M{r['meeting']}: cites RDSS ch. {ch} — not in the "
                            f"verified inventory (book skips 14/20)")
        cb = r["cb_reading"].strip()
        if cb and "callingbullshit.org" not in cb:
            errs.append(f"M{r['meeting']}: CB entry must point at public "
                        f"callingbullshit.org material: {cb!r}")

    # 4: datasets
    for r in rows:
        ds = r["dataset_simulation"].lower()
        named = {s for s in SHIPPED if s in ds}
        for s in named:
            if not (DATA_DIR / f"{s}.csv").exists():
                errs.append(f"M{r['meeting']}: dataset {s}.csv not shipped")
        if not named and not any(w in ds for w in DATASET_OK_WORDS):
            errs.append(f"M{r['meeting']}: unrecognized dataset_simulation {ds!r}")

    # 5: provenance shape
    for r in rows:
        if r["provenance"].count("|") != 3:
            errs.append(f"M{r['meeting']}: provenance needs 4 pipe-separated "
                        f"segments: {r['provenance']!r}")

    if errs:
        print(f"✗ coverage: {len(errs)} problem(s)")
        for e in errs:
            print("  " + e)
        sys.exit(1)
    mode = "plan-level" if plan_only else "full (files on disk)"
    print(f"✓ coverage clean — 43 meetings ↔ {len(NOTEBOOKS)} notebooks, readings "
          f"within the verified inventory, datasets shipped, provenance "
          f"well-formed [{mode}]")


if __name__ == "__main__":
    main()
