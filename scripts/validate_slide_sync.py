#!/usr/bin/env python3
"""validate_slide_sync.py — the gate that keeps the studio decks equal to the book.

The decks under lecture_slides/ are a GENERATED VIEW of EDR|AI. That promise is
only worth something if something checks it, because a chapter edit that never
reaches a deck is invisible: the deck still renders, still looks finished, and
is now quietly wrong in front of a class.

Five checks, in the order they fail usefully:

  1. FRESH        every deck on disk is byte-identical to a fresh build
  2. PLAN AGE     every slide plan's `source_sha256` matches its chapter now
  3. COVERAGE     every active lesson lands on exactly one studio deck, and
                  every studio with lessons has a deck
  4. FIDELITY     every claim-bearing plan bullet's citation keys exist in
                  book/references.bib, and no plan invents a section heading
  5. VOICE        the student-facing voice rules that apply to slide text

    .venv/bin/python scripts/validate_slide_sync.py            # report
    .venv/bin/python scripts/validate_slide_sync.py --strict   # plans-none is an error too

Exit 0 clean, 1 on any failure. Wired into .github/workflows/validate.yml and
into the PostToolUse hook that fires whenever a book chapter is edited.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import slide_parts as sp                                        # noqa: E402
from book_manifest import active_lessons                        # noqa: E402
from build_studio_slides import (PLANS, build_deck, load_plan,   # noqa: E402
                                 studios)

BOOK = REPO / "book"
BIB = BOOK / "references.bib"

#: Vocabulary the book's voice policy bans (D28). Slides inherit the rule:
#: a deck is read by the same student, in the same course.
AI_TELLS = [
    "leverage", "unlock", "seamless", "robust", "powerful", "delve",
    "the power of", "game-changer", "game changer", "empower", "elevate",
    "it is worth noting", "it's worth noting", "tapestry", "realm",
    "in today's data-driven", "when it comes to",
]

#: The builder owns these sections; a plan entry for one is dead configuration.
BUILDER_OWNED = {"an ai failure case", "it is your turn"}


def bib_keys() -> set[str]:
    if not BIB.exists():
        return set()
    return {m.group(1).strip()
            for m in re.finditer(r"@\w+\{([^,]+),", BIB.read_text())}


def plan_text(plan: dict) -> list[tuple[str, str]]:
    """Every author-written string in a plan, with a locator."""
    out: list[tuple[str, str]] = []
    for heading, slides in (plan.get("sections") or {}).items():
        for i, slide in enumerate(slides or [], 1):
            where = f"{heading} #{i}"
            for key in ("title", "lead", "note", "quote", "table"):
                if slide.get(key):
                    out.append((f"{where} {key}", str(slide[key])))
            for b in slide.get("bullets") or []:
                out.append((f"{where} bullet", str(b)))
            for t in slide.get("terms") or []:
                out.append((f"{where} term", f"{t.get('term','')}: "
                                             f"{t.get('definition','')}"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true",
                    help="a chapter with no slide plan is an error, not a note")
    args = ap.parse_args()

    fail: list[str] = []
    warn: list[str] = []
    keys = bib_keys()
    all_studios = studios()

    # -- 1. every deck matches a fresh build ---------------------------------
    for st in all_studios:
        text, _ = build_deck(st)
        out = st["qmd"]
        if not out.exists():
            fail.append(f"deck missing: {out.relative_to(REPO)}")
        elif out.read_text() != text:
            fail.append(f"deck stale: {out.relative_to(REPO)} — rerun "
                        f"scripts/build_studio_slides.py")

    # -- 3. coverage ---------------------------------------------------------
    lessons = active_lessons()
    placed = {l["id"] for st in all_studios for l in st["lessons"]}
    for l in lessons:
        if l["id"] not in placed:
            fail.append(f"lesson on no deck: {l['id']} "
                        f"(station {l['station']})")
    for st in all_studios:
        if st["lessons"] and not st["qmd"].exists():
            fail.append(f"studio {st['rank']} has lessons but no deck")

    # -- 2, 4, 5. per-plan checks -------------------------------------------
    planned = stale = 0
    for l in lessons:
        plan = load_plan(l["id"])
        if not plan:
            (fail if args.strict else warn).append(
                f"no slide plan: {l['id']} (deck uses the mechanical "
                f"fallback for chapter {l['display']})")
            continue
        planned += 1
        where = f"BOOK_SLIDE_PLANS/{l['id']}.yml"

        if plan.get("lesson") != l["id"]:
            fail.append(f"{where}: `lesson:` is {plan.get('lesson')!r}, "
                        f"file is named {l['id']!r}")

        live = sp.digest_of(l["source"])
        if plan.get("source_sha256") != live:
            stale += 1
            fail.append(f"{where}: STALE — written against a different "
                        f"revision of {l['source']}. Reread the chapter and "
                        f"revise the plan, then set source_sha256 to {live}")

        page = sp.parse(BOOK / l["source"])
        headings = {h.lower() for h in page.headings() if h}
        for heading, slides in (plan.get("sections") or {}).items():
            hl = heading.lower()
            if hl in BUILDER_OWNED:
                fail.append(f"{where}: section {heading!r} is built from the "
                            f"chapter itself — remove it from the plan")
            elif hl not in headings:
                fail.append(f"{where}: section {heading!r} is not a heading "
                            f"of {l['source']} — those slides never render")
                continue
            section = page.section(heading)
            if section is None:
                continue
            for i, slide in enumerate(slides or [], 1):
                if not slide.get("title"):
                    fail.append(f"{where}: {heading} #{i} has no title")
                for key, kind in (("code", "code"), ("mermaid", "mermaid")):
                    if slide.get(key) is not None:
                        n = len(section.all(kind))
                        if int(slide[key]) >= n:
                            fail.append(f"{where}: {heading} #{i} asks for "
                                        f"{kind} {slide[key]}, section has "
                                        f"{n}")
                if slide.get("figure"):
                    have = {Path(b.src).name
                            for b in section.all("figure")}
                    if Path(slide["figure"]).name not in have:
                        fail.append(f"{where}: {heading} #{i} figure "
                                    f"{slide['figure']!r} is not in that "
                                    f"section")

        # 4. citation integrity + 5. voice, over every authored string
        for locator, text in plan_text(plan):
            for m in re.finditer(r"@([\w:.-]+)", text):
                if m.group(1) not in keys:
                    fail.append(f"{where}: {locator} cites @{m.group(1)}, "
                                f"which is not in book/references.bib")
            low = text.lower()
            for tell in AI_TELLS:
                if re.search(rf"\b{re.escape(tell)}\b", low):
                    fail.append(f"{where}: {locator} uses banned voice "
                                f"{tell!r} (BOOK_VOICE_POLICY, D28)")
            # The CRITICAL RULE bans addressing the class in the third
            # person, not the word itself: a chapter's own study population
            # ("first-generation students") must survive onto the slide.
            if re.search(r"\b(the|these|those|your|all|most|many|some)\s+"
                         r"students\b|\bstudents\s+(will|should|must|are|"
                         r"have|need|can|may)\b", low):
                fail.append(f"{where}: {locator} writes about \"students\" in "
                            f"the third person — slides speak TO the student")
            if text.count("—") > 1 and "bullet" in locator:
                fail.append(f"{where}: {locator} has "
                            f"{text.count('—')} em dashes (budget: 1)")
            if re.search(r"(?<![\\\w])\$\d", text):
                fail.append(f"{where}: {locator} has unescaped money "
                            f"(write \\$)")

    # -- report --------------------------------------------------------------
    n = len(lessons)
    print(f"  {len(all_studios)} studio decks · {n} chapters · "
          f"{planned} with a slide plan")
    for w in warn:
        print(f"  ○ {w}")
    if fail:
        print(f"\n✗ {len(fail)} problem(s):")
        for f in fail:
            print(f"    {f}")
        raise SystemExit(1)
    print("\n✓ every deck matches the book it is built from")


if __name__ == "__main__":
    main()
