#!/usr/bin/env python3
"""book_manifest.py — THE validated manifest loader for every book consumer.

Round-9 N2: generators and validators each re-derived identity from display
numbers or numeric filename prefixes, so activating a lesson (or tombstoning
one) would misbind artifacts while gates stayed green. This module is the one
place book structure is read:

  - lesson identity, order, sources, url_path, and companion paths come from
    planning/BOOK_ARCHITECTURE.yml (dup-key strict);
  - primary course notebooks come from COURSE_BOOK_CROSSWALK.yml home anchors;
  - `require_lock()` refuses to serve consumers when the manifests changed
    after the last validator pass (D35(7): the validator is the arbiter).

Display chapter numbers are DERIVED here (rank order among active lessons)
and exist only for presentation; nothing may parse them back out of
filenames. D83 adds two filtered views that keep those numbers:
`studio_lessons()` (no book-only lessons) and `course_lessons()` (no lesson
the crosswalk lists as `not_adopted:`).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ARCH = REPO / "planning" / "BOOK_ARCHITECTURE.yml"
CW = REPO / "planning" / "COURSE_BOOK_CROSSWALK.yml"
LOCK = REPO / "planning" / ".crosswalk_lock.json"


class _DupKeyLoader(yaml.SafeLoader):
    pass


def _no_dup(loader, node, deep=False):
    m = {}
    for k, v in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in m:
            raise yaml.constructor.ConstructorError(
                None, None, f"duplicate key {key!r}", k.start_mark)
        m[key] = loader.construct_object(v, deep=deep)
    return m


_DupKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_dup)


def load_architecture() -> dict:
    return yaml.load(ARCH.read_text(), Loader=_DupKeyLoader)


def load_crosswalk() -> dict:
    return yaml.load(CW.read_text(), Loader=_DupKeyLoader)


def require_lock() -> None:
    """Refuse to serve a consumer when the manifests moved past the lock."""
    if not LOCK.exists():
        raise SystemExit("✗ no crosswalk lock — run "
                         "scripts/validate_book_architecture.py first")
    lock = json.loads(LOCK.read_text())
    # The COMPLETE locked manifest set is checked (D41 review round): a
    # consumer must not run against ANY manifest that moved past the lock —
    # BOOK_ASSESSMENTS feeds the station/rubric pages, LEAKAGE the A2 gate.
    for name in ("BOOK_ARCHITECTURE.yml", "COURSE_BOOK_CROSSWALK.yml",
                 "BOOK_STATIONS.yml", "BOOK_ASSESSMENTS.yml",
                 "BOOK_LEAKAGE_POLICY.yml"):
        if name not in lock.get("manifests", {}):
            raise SystemExit(f"✗ lock predates {name} coverage — re-run "
                             "scripts/validate_book_architecture.py")
        p = REPO / "planning" / name
        if hashlib.sha256(p.read_bytes()).hexdigest() != lock["manifests"][name]:
            raise SystemExit(f"✗ {name} changed since the last validator pass "
                             f"— re-run scripts/validate_book_architecture.py")


def active_lessons(arch: dict | None = None) -> list[dict]:
    """Active lessons in rank order, each augmented with `display` (1..N)."""
    arch = arch or load_architecture()
    active = sorted((l for l in arch["lessons"] if l["state"] == "active"),
                    key=lambda l: l["rank"])
    out = []
    for i, l in enumerate(active, start=1):
        d = dict(l)
        d["display"] = i
        out.append(d)
    return out


# D83 (book-only further routes): a lesson may carry `scope: book-only`. It
# is a real, numbered chapter of the book (display numbers still come from
# ALL active lessons above, so appending it renumbers nothing), but it sits
# in a book-only TOC section after the twelve studios, joins no studio deck,
# studio page or milestone checklist, and the companion course does not
# adopt it (the crosswalk lists it under `not_adopted:`).
def is_book_only(l: dict) -> bool:
    return l.get("scope") == "book-only"


def studio_lessons(arch: dict | None = None) -> list[dict]:
    """Active lessons that belong to a studio: active_lessons() minus the
    book-only ones, `display` unchanged (D83)."""
    return [l for l in active_lessons(arch) if not is_book_only(l)]


def not_adopted_ids(cw: dict | None = None) -> set[str]:
    """Lesson ids the crosswalk declares the course does NOT adopt (D83)."""
    cw = cw or load_crosswalk()
    return {x["lesson"] for x in (cw.get("not_adopted") or [])}


def course_lessons(arch: dict | None = None,
                   cw: dict | None = None) -> list[dict]:
    """Active lessons the COURSE adopts: active_lessons() minus the crosswalk's
    `not_adopted:` list, `display` unchanged (D83)."""
    skip = not_adopted_ids(cw)
    return [l for l in active_lessons(arch) if l["id"] not in skip]


def primary_nb_by_lesson(cw: dict | None = None) -> dict[str, str]:
    """lesson id -> 'nbNN' from the crosswalk's home anchors."""
    cw = cw or load_crosswalk()
    out: dict[str, str] = {}
    for r in cw["rows"]:
        for a in r.get("assignments", []):
            if a.get("home_anchor"):
                out[a["lesson"]] = r["nb"]
    return out
