#!/usr/bin/env python3
"""validate_book_sync.py — chapter <-> notebook synchronization gate (D20/D25).

Reads lesson identity from planning/BOOK_ARCHITECTURE.yml through the shared
loader (round-9 N2: this gate previously parsed BOOK_MAP's display numbers
and hard-coded 37, so a valid 39-lesson architecture would have failed while
number-misbound artifacts passed) and checks the book both directions:

  1. every ACTIVE lesson has its source file and its companion notebook
     (paths from the manifest — never derived from numeric prefixes)
  2. every chapter file links its OWN companion notebook (the chapter badge);
     the lesson-to-lab mapping lives in the For Instructors appendix, not in
     chapter bodies (D35 Phase 4 de-coursing)
  3. every registered notebook (nb01-nb16) is the primary of >= 1 lesson
  4. every chapter carries the required element headings
  5. the For-instructors appendix exists in all three editions and the EN
     edition links every course lab nb01-nb16 (D25)
  6. the PT/ES chapter files link their localized companion notebooks
     (mirrored source paths while the editions are frozen, D36)
  7. NO ORPHANS: every book/part*/*.qmd and notebooks/book/*.ipynb (and
     pt/es) is claimed by the manifest — a tombstoned or renamed lesson
     cannot leave debris behind.

Usage: python3 scripts/validate_book_sync.py [--strict]
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from notebooks_map import NOTEBOOKS, student_filename  # noqa: E402
from book_manifest import (active_lessons, load_architecture,  # noqa: E402
                           primary_nb_by_lesson)

BOOK_DIR = REPO / "book"
NB_BOOK = REPO / "notebooks" / "book"

REQUIRED_ELEMENTS = [
    "research decision", "worked example", "Do not delegate",
    "failure", "It is your turn",
]

# D38 practice-first template: these section headings are RETIRED in EN —
# prompts attach to the IYT step they serve; the companion intro lives in
# "It is your turn".
RETIRED_HEADINGS = ["## Recommended AI prompts", "## The Colab laboratory"]

# D38: "worked examples must come with data and evidence." Chapters below
# still await their seeded data block (data) or their citation (evidence);
# the lists SHRINK as upgrades land and new entries are forbidden. An empty
# list retires itself.
DATA_PENDING: set[str] = {         # lesson ids awaiting a data-backed example
    "ai-adversarial-reviewer", "ai-analytical-assistant",
    "ai-as-programmer", "claim-evidence-tables", "conflicting-agents", "data-provenance",
    "difficult-questions",
    "false-confidence", "final-portfolio",
    "managing-ai-agents", "measurement", "negative-tests", "poster-criticism",
    "poster-to-note",
    "replication-reproduction",
    "research-packages", "research-pitches", "research-posters", "results-to-claims", "robustness-sensitivity",
}
EVIDENCE_PENDING: set[str] = {     # lesson ids awaiting an in-example citation
    "ai-arm-not-brain", "research-director", "sdiivdd",
    "responsibility-ownership", "curiosity-to-problem", "question-kinds",
    "research-builds", "verifying-prior-evidence", "mida",
    "declare-diagnose", "observational-causal",
    "experimental-descriptive",
    "experimental-causal", "data-provenance",
    "measurement", "ai-as-programmer", "ai-analytical-assistant",
    "robustness-sensitivity", "negative-tests", "ai-adversarial-reviewer",
    "false-confidence", "results-to-claims", "claim-evidence-tables",
    "research-posters", "poster-criticism", "research-pitches",
    "difficult-questions", "ai-disclosure", "replication-reproduction",
    "poster-to-note", "research-packages", "managing-ai-agents",
    "conflicting-agents", "final-portfolio",
}


def main() -> None:
    strict = "--strict" in sys.argv          # kept for CI compatibility
    arch = load_architecture()
    lessons = active_lessons(arch)
    primary = primary_nb_by_lesson()
    errs, warns = [], []

    # (3) coverage both directions, from the crosswalk home anchors
    covered = {int(primary[l["id"]][2:]) for l in lessons if l["id"] in primary}
    for n in NOTEBOOKS:
        if n not in covered:
            errs.append(f"nb{n:02d} is not the primary notebook of any lesson")
    for l in lessons:
        if l["id"] not in primary:
            errs.append(f"{l['id']}: no home anchor in the crosswalk")

    for l in lessons:
        src = BOOK_DIR / l["source"]
        comp = NB_BOOK / l["companion"]
        if not src.exists():
            errs.append(f"{l['id']}: source missing: book/{l['source']}")
            continue
        if not comp.exists():
            errs.append(f"{l['id']}: companion missing: "
                        f"notebooks/book/{l['companion']}")
        text = src.read_text()
        # D35 Phase 4: chapter BODIES are de-coursed — the lesson-to-lab
        # mapping lives in the For Instructors appendix, checked below.
        if f"notebooks/book/{l['companion']}" not in text:
            errs.append(f"{l['id']}: no link to its companion "
                        f"notebooks/book/{l['companion']}")
        missing = [e for e in REQUIRED_ELEMENTS if e.lower() not in text.lower()]
        if missing:
            warns.append(f"{l['id']}: missing element(s) {missing}")
        # (4b) D38 practice-first template
        for h in RETIRED_HEADINGS:
            if h in text:
                errs.append(f"{l['id']}: retired section survives: {h!r} — "
                            f"prompts attach to IYT steps (D38)")
        iyt_at = text.find("## It is your turn")
        if iyt_at >= 0:
            iyt = text[iyt_at:]
            if "companion notebook" not in iyt:
                errs.append(f"{l['id']}: IYT lost the companion-notebook fold")
            stray = text.count("After running, verify") - \
                iyt.count("After running, verify")
            if stray:
                errs.append(f"{l['id']}: {stray} prompt verify note(s) outside "
                            f"the IYT section")
        # (4c) worked example: data + evidence (D38)
        we_at = text.find("## A worked example")
        nxt = text.find("\n## ", we_at + 1) if we_at >= 0 else -1
        we = text[we_at:nxt] if we_at >= 0 else ""
        has_data = "```python" in we or "load_course_data" in we
        has_cite = "[@" in we
        if we:
            if not has_data and l["id"] not in DATA_PENDING:
                errs.append(f"{l['id']}: worked example has no data block and "
                            f"is not on DATA_PENDING (D38)")
            if has_data and l["id"] in DATA_PENDING:
                errs.append(f"{l['id']}: has a data block — remove from "
                            f"DATA_PENDING")
            if not has_cite and l["id"] not in EVIDENCE_PENDING:
                errs.append(f"{l['id']}: worked example cites nothing and is "
                            f"not on EVIDENCE_PENDING (D38)")
            if has_cite and l["id"] in EVIDENCE_PENDING:
                errs.append(f"{l['id']}: has a citation — remove from "
                            f"EVIDENCE_PENDING")

    # (5) For-instructors appendix
    for edition in ("book", "book-pt", "book-es"):
        if not (REPO / edition / "for-instructors.qmd").exists():
            errs.append(f"{edition}/for-instructors.qmd missing")
    fi = BOOK_DIR / "for-instructors.qmd"
    if fi.exists():
        fi_text = fi.read_text()
        for n in NOTEBOOKS:
            if student_filename(n) not in fi_text:
                errs.append(f"For-instructors appendix does not link nb{n:02d}")
        for l in lessons:                      # every lesson mapped to its lab
            if f"| Ch. {l['display']} |" not in fi_text:
                errs.append(f"{l['id']}: missing from the For-instructors "
                            f"adoption table")

    # (6) localized companion links (frozen editions: verify only, D36)
    for edition, sub in (("book-pt", "pt"), ("book-es", "es")):
        for l in lessons:
            hit = REPO / edition / l["source"]
            if hit.exists() and f"notebooks/book/{sub}/{l['companion']}" \
                    not in hit.read_text():
                errs.append(f"{edition} {l['id']}: no localized companion link")

    # (7) orphan enumeration (round-9 N2)
    claimed_qmd = {str(BOOK_DIR / l["source"]) for l in lessons}
    for f in BOOK_DIR.glob("part*/*.qmd"):
        if f.name.endswith("-overview.qmd"):
            continue                      # the Part I overview page (D27)
        if str(f) not in claimed_qmd:
            errs.append(f"ORPHAN chapter file not in the manifest: "
                        f"{f.relative_to(REPO)}")
    claimed_comp = {l["companion"] for l in lessons}
    for sub in ("", "pt", "es"):
        d = NB_BOOK / sub if sub else NB_BOOK
        for f in sorted(d.glob("*.ipynb")):
            if f.name not in claimed_comp:
                errs.append(f"ORPHAN companion notebook not in the manifest: "
                            f"{f.relative_to(REPO)}")

    for w in warns:
        print(f"  ⚠️ {w}")
    if errs:
        print(f"✗ book sync: {len(errs)} problem(s)")
        for e in errs:
            print("  " + e)
        sys.exit(1)
    n_planned = sum(1 for l in arch["lessons"] if l["state"] == "planned")
    pend = ""
    if DATA_PENDING or EVIDENCE_PENDING:
        pend = (f"; D38 pending: {len(DATA_PENDING)} worked examples await "
                f"data, {len(EVIDENCE_PENDING)} await a citation")
    print(f"✓ book manifest consistent — {len(lessons)} active lessons "
          f"(+{n_planned} planned), all {len(NOTEBOOKS)} notebooks covered, "
          f"no orphans{pend}")


if __name__ == "__main__":
    main()
