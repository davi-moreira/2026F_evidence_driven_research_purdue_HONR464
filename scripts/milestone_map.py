#!/usr/bin/env python3
"""milestone_map.py — the ONE map from a course milestone to its Book Milestone.

The course is the book applied, so every course milestone M1..M17 presents one
or two of the book's twelve Book Milestones. That correspondence is declared
once, in planning/COURSE_BOOK_CROSSWALK.yml, and read here. It is never retyped
into course prose, exactly like the per-session readings.

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
ADDITIONS_FILE = REPO / "_research_project" / "milestone_course_additions.yml"

SITE_REL = "book/studios"          # site-relative, for links on course pages


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

    out: dict[str, dict] = {}
    for row in cw["rows"]:
        nn = f"{int(row['milestone'][1:]):02d}"
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


def _title_of(path: Path) -> str:
    """The book milestone's title AS PUBLISHED, from its own H1."""
    m = re.search(r"^# (.+?)(?:\s*\{[^}]*\})?\s*$", path.read_text(), re.M)
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
    """True when the COURSE asks for more than the Book Milestone page does."""
    adds = additions() if adds is None else adds
    return (adds.get(key, {}).get("classification") == "additions")
