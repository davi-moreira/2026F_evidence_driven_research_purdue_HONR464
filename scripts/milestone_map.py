#!/usr/bin/env python3
"""milestone_map.py — the ONE map from a course milestone to its Book Milestone.

The course is the book applied, so every course milestone presents one or two of
the book's twelve Book Milestones. That correspondence is declared once, in
planning/COURSE_BOOK_CROSSWALK.yml, and read here. It is never retyped into
course prose, exactly like the per-session readings.

WHICH MILESTONES THE COURSE ACTUALLY RUNS is a separate question, and its answer
is the `milestones:` table in course_config.yaml. A crosswalk row can outlive the
milestone it was written for: D54 (2026-08-23) retired M17, because the last
Friday of the semester is the course reflection session and there is no
submission slot for it. Week 16 still TEACHES Studio 12's lessons on Monday and
Wednesday, so the M17 crosswalk row keeps its `assignments:` and those three
lessons keep their home anchor. Only the submission is gone.

So this module reads BOTH files and returns only the live chain. A milestone
dropped from course_config disappears from the handout PDFs and from the
schedule at the same moment, with no second list to remember.

Two consumers share this module so the page and the PDF can never disagree:

  * scripts/update_schedule_badges.py  links the schedule's Milestone column
    straight at the book page, and marks the milestones that add more.
  * scripts/build_handout_pdfs.py      builds each milestone PDF from that book
    page, plus the course additions where there are any.

`additions()` reads _research_project/milestone_course_additions.yml, whose
`classification:` is the single source of truth for which milestones carry more
than their Book Milestone.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from book_manifest import load_architecture  # noqa: E402

BRIEFS = REPO / "_research_project" / "2026Fall"
STUDIOS = REPO / "book" / "studios"
CROSSWALK = REPO / "planning" / "COURSE_BOOK_CROSSWALK.yml"
COURSE_CONFIG = REPO / "course_config.yaml"
ADDITIONS_FILE = REPO / "_research_project" / "milestone_course_additions.yml"

SITE_REL = "book/studios"          # site-relative, for links on course pages


def live_milestones() -> set[str]:
    """"M01".."M16": the milestones the course actually runs.

    Read from course_config.yaml's `milestones:` table, which is where the
    course declares its own chain. Retiring a milestone there retires it
    everywhere this module feeds.
    """
    cfg = yaml.safe_load(COURSE_CONFIG.read_text())
    return {f"M{int(k[1:]):02d}" for k in cfg["milestones"]}


def milestone_map() -> dict[str, dict]:
    """"M07" -> {num, brief, topic, pages, books}.

    `pages`  book milestone .qmd paths, primary first
    `books`  [{n, station, relationship, version_label, url_path, title}]
    """
    arch = load_architecture()
    rank = {s["id"]: s["rank"] for s in arch["stations"]}
    files = {int(p.name[9:11]): p for p in STUDIOS.glob("milestone*.qmd")}
    cw = yaml.safe_load(CROSSWALK.read_text())
    briefs = {b.name.split("_")[1]: b for b in BRIEFS.glob("milestone_*.md")}
    live = live_milestones()

    out: dict[str, dict] = {}
    for row in cw["rows"]:
        if not row.get("milestone"):        # D54: teaching-only rows (Week 16)
            continue
        nn = f"{int(row['milestone'][1:]):02d}"
        if f"M{nn}" not in live:      # retired: the row survives, the milestone does not
            continue
        brief = briefs[nn]
        h1 = re.search(r"^# (.+)$", brief.read_text(), re.M)
        topic = (re.sub(r"^Course milestone M\d+\s*[:—-]\s*", "", h1.group(1).strip())
                 if h1 else brief.stem)
        books, pages = [], []
        for b in row.get("book_milestones") or []:
            n = rank[b["station"]]
            path = files[n]
            pages.append(path)
            books.append({
                "n": n,
                "station": b["station"],
                "relationship": b["relationship"],
                "version_label": b.get("version_label", "version 1"),
                "url_path": f"{SITE_REL}/{path.stem}.html",
                "title": _title_of(path),
            })
        out[f"M{nn}"] = {"num": nn, "brief": brief, "topic": topic,
                         "pages": pages, "books": books}
    return out


#: A leading YAML front matter block. It has to come off before the H1 search:
#: D70 (2026-08-28) put a "# GENERATED FILE - DO NOT EDIT." comment inside the
#: front matter of every generated studio page, and a YAML comment starts with
#: the same "# " a markdown H1 does. Without this strip, every milestone PDF
#: announced that it presents "Book Milestone 1: GENERATED FILE - DO NOT EDIT."
FRONT_MATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)


def _title_of(path: Path) -> str:
    """The book milestone's title AS PUBLISHED, from its own H1."""
    body = FRONT_MATTER.sub("", path.read_text(), count=1)
    m = re.search(r"^# (.+?)(?:\s*\{[^}]*\})?\s*$", body, re.M)
    if not m:
        raise SystemExit(f"✗ no H1 in {path}")
    return m.group(1).strip()


def additions() -> dict[str, dict]:
    """"M07" -> the authored course-additions record, or {} for a pure milestone."""
    if not ADDITIONS_FILE.exists():
        return {}
    doc = yaml.safe_load(ADDITIONS_FILE.read_text()) or {}
    return doc.get("milestones", {})


def has_additions(key: str, adds: dict | None = None) -> bool:
    """True when the milestone PDF carries a "What this course adds" section."""
    adds = additions() if adds is None else adds
    return (adds.get(key, {}).get("classification") == "additions")


def marked_on_schedule(key: str, adds: dict | None = None) -> bool:
    """True when the Schedule page marks this milestone with the plus sign.

    Deliberately NOT the same question as has_additions(): the mark is about
    what a student still owes beyond the book, the section is about what the PDF
    has to print. Demoting `classification` to quiet the schedule would delete
    required instruction from the PDF, so they are separate flags.
    """
    adds = additions() if adds is None else adds
    return bool(adds.get(key, {}).get("schedule_mark"))
