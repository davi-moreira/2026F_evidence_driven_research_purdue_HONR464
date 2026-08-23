#!/usr/bin/env python3
"""session_readings.py — the ONE renderer for per-session required readings.

The course is the book applied: Monday and Wednesday teach a Studio's lessons
with their "It is your turn" work, and Friday IS that Studio's milestone (D49).
For that to be legible to a student, every session on the public schedule has
to name the chapters it requires — in the book's OWN published wording.

So chapter identity is never retyped into course prose. It is read here from
the manifests, exactly like the milestone Book Anchors:

  - the lesson set per session comes from `book_reading` in
    scripts/schedule_data/ (tokens `lesson-id:mode`, semicolon-separated);
  - the display number comes from book_manifest.active_lessons() (rank order);
  - the TITLE comes from the chapter's own `title:` front matter, i.e. the
    string published on the book page;
  - the STUDIO title comes from BOOK_ARCHITECTURE.yml stations, which the
    validator holds equal to the published studio page.

Modes:
    first-read     read BEFORE this session (its home anchor)
    assigned       assigned today, read for the next session
    continue       still in play from earlier THIS week (its first read was
                   an earlier session of the same Studio)
    revisit        re-read; the lesson's home anchor was an earlier week
    route          your OWN declared route's pathway lesson (D49 policy)
    route-contrast the instructor-assigned contrast route's lesson
    optional       binds only under the lesson's own condition
    due            the week's chapters, whose "It is your turn" sections the
                   Friday milestone submits

Consumers: update_schedule_badges.py, build_material_page.py,
validate_session_readings.py.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from book_manifest import active_lessons, load_architecture  # noqa: E402

SITE_REL = "book"  # site-relative prefix for links on the course pages

#: Order in which modes are presented inside one session's cell.
MODE_ORDER = ["first-read", "route", "route-contrast", "assigned", "continue",
              "revisit", "optional", "due"]

#: Student-facing lead-in for each mode.
MODE_LABEL = {
    "first-read": "**Required before today —** ",
    "assigned": "**Assigned today, read for the next session —** ",
    "continue": "**Still in play from Monday —** ",
    "revisit": "**Revisit —** ",
    "route": "**Required, your declared route —** ",
    "route-contrast": "**Required, your assigned contrast route —** ",
    "optional": "**Only if your design has stages —** ",
    "due": "**Due today** (submit these chapters' *It is your turn* sections) **—** ",
}

VALID_MODES = set(MODE_LABEL)


def _title_of(lesson: dict) -> str:
    """The chapter title AS PUBLISHED — its `title:` front matter, verbatim."""
    src = REPO / "book" / lesson["source"]
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', src.read_text(), re.M)
    if not m:
        raise SystemExit(f"✗ {lesson['id']}: no `title:` in {lesson['source']}")
    return m.group(1)


def lesson_index() -> dict[str, dict]:
    """lesson id -> {display, title (as published), url_path, companion}."""
    out = {}
    for l in active_lessons():
        out[l["id"]] = {
            "id": l["id"],
            "display": l["display"],
            "title": _title_of(l),
            "url_path": l["url_path"],
            "companion": l["companion"],
        }
    return out


def studio_titles() -> dict[int, str]:
    """Studio rank -> the studio title as published in the book."""
    arch = load_architecture()
    return {s["rank"]: f"Studio {s['rank']}: {s['title']}"
            for s in arch["stations"]}


def parse(field: str) -> list[tuple[str, str]]:
    """`book_reading` -> [(lesson id, mode)], order preserved."""
    pairs = []
    for tok in (t.strip() for t in str(field).split(";")):
        if not tok:
            continue
        if ":" not in tok:
            raise SystemExit(f"✗ malformed book_reading token {tok!r} "
                             f"(expected 'lesson-id:mode')")
        lid, mode = (p.strip() for p in tok.split(":", 1))
        if mode not in VALID_MODES:
            raise SystemExit(f"✗ unknown reading mode {mode!r} in {tok!r}")
        pairs.append((lid, mode))
    return pairs


def by_mode(field: str) -> dict[str, list[str]]:
    """`book_reading` -> {mode: [lesson id, ...]} in MODE_ORDER order."""
    grouped: dict[str, list[str]] = {}
    for lid, mode in parse(field):
        grouped.setdefault(mode, []).append(lid)
    return {m: grouped[m] for m in MODE_ORDER if m in grouped}


def chapter_link(lesson: dict, prefix: str = SITE_REL) -> str:
    """`[Ch. 12 — Declaring and Diagnosing a Research Design](book/…)`."""
    return (f"[Ch. {lesson['display']} — {lesson['title']}]"
            f"({prefix}/{lesson['url_path']}){{target=\"_blank\"}}")


#: What a cell says instead of relisting links the same week already carries.
#: Used only when `seen` is threaded through render_cell().
BACKREF = "linked in this week's rows above"

#: Modes whose wording already points at what the week showed earlier, so a
#: back-reference reads naturally and no link is lost (anything NOT shown
#: earlier is still listed in full).
BACKREF_MODES = {"due", "continue", "revisit"}


def render_cell(field: str, index: dict[str, dict] | None = None,
                prefix: str = SITE_REL,
                seen: set[str] | None = None) -> str:
    """One schedule cell: every mode present, book wording, linked.

    Pass `seen` (a per-WEEK set of lesson ids, mutated in place) to collapse the
    back-reference modes ("Due today", "Still in play from Monday", "Revisit")
    down to a pointer for the chapters the same week already links above.
    Chapters that appear nowhere earlier in the week are still listed in full,
    so nothing loses its link. Callers that do not pass `seen` (the Material
    page) are unaffected.
    """
    index = index or lesson_index()
    grouped = by_mode(field)
    if not grouped:
        return "—"
    blocks = []
    for mode, ids in grouped.items():
        ids = [i for i in ids if i in index]
        if not ids:
            continue
        fresh = ids if seen is None else [i for i in ids if i not in seen]
        if seen is not None:
            repeated = len(fresh) < len(ids)
            seen.update(ids)
            if mode in BACKREF_MODES and repeated:
                links = " · ".join(chapter_link(index[i], prefix) for i in fresh)
                tail = f"{links} · {BACKREF}" if links else BACKREF
                blocks.append(MODE_LABEL[mode] + tail)
                continue
        links = " · ".join(chapter_link(index[i], prefix) for i in ids)
        if links:
            blocks.append(MODE_LABEL[mode] + links)
    return "<br>".join(blocks) if blocks else "—"


#: The authored note carries one RECOMMENDED RDSS clause; the EDR|AI half of
#: that prose is now redundant (the chapter list above is generated from the
#: book itself), so only the RDSS clause is lifted onto the page.
RDSS_CLAUSE = re.compile(
    r"(?:Recommended RDSS:|Optional send-off:\s*RDSS|RDSS ch\.)", re.I)


def rdss_note(rdss_reading: str) -> str:
    """The recommended-RDSS sentence from an authored note, or ''.

    RDSS is the course's RECOMMENDED companion (EDR|AI is what is required),
    so this is rendered in a quieter register under the required chapters.
    """
    text = str(rdss_reading).strip()
    m = RDSS_CLAUSE.search(text)
    if not m:
        return ""
    clause = text[m.start():].strip()
    clause = re.sub(r"^Recommended RDSS:\s*", "", clause, flags=re.I)
    clause = re.sub(r"^Optional send-off:\s*", "", clause, flags=re.I)
    clause = re.sub(r"^RDSS\s+", "", clause)
    clause = re.sub(r"\s*\(book\.declaredesign\.org\)", "", clause)
    clause = re.sub(r",?\s*book\.declaredesign\.org", "", clause)
    clause = clause.rstrip(" .;")
    # a trailing ')' left behind when the parenthetical held only the URL
    if clause.count("(") < clause.count(")"):
        clause = clause.rstrip(")").rstrip(" ,;")
    return clause


def studio_pages() -> dict[int, dict]:
    """Studio rank -> {title (as published), url_path} for the studio page.

    The studio page is the book's own home for that Studio, so the schedule's
    Studio column links there rather than restating what the Studio is.
    """
    arch = load_architecture()
    return {s["rank"]: {"title": f"Studio {s['rank']}: {s['title']}",
                        "url_path": f"studios/studio{s['rank']:02d}-{s['id']}.html"}
            for s in arch["stations"]}
