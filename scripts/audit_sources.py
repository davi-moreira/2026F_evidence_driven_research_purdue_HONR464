#!/usr/bin/env python3
"""audit_sources.py — citation-integrity gate for student-facing notebooks.

The course's evidence-integrity rule (CLAUDE.md): every citation in shipped
material is real and retrievable; fabricated citations exist ONLY inside
disclosed hunt exercises. This gate enforces the machine-checkable half:

  1. External URL allowlist — every http(s) URL in a student notebook must be
     on the course's verified-domain allowlist (unknown domains fail).
  2. Verified-citation registry — "Author (Year)"-shaped citations must match
     the registry of works verified during the build (unknown ones fail until
     added here WITH a verification note).
  3. Planted-fake containment — known planted fakes may appear only in
     notebooks that disclose the plant ("are fabricated" / "fabricated for
     this exercise" phrasing must appear in the same notebook).

Usage: python3 scripts/audit_sources.py [notebooks/student/nbNN_*.ipynb ...]
       (default: all student notebooks; exit non-zero on any violation)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parent.parent

ALLOWED_DOMAINS = {
    "book.declaredesign.org",      # RDSS free online edition
    "callingbullshit.org",         # optional CB public cases (index pages)
    "colab.research.google.com",   # notebook badges
    "raw.githubusercontent.com",   # course data
    "github.com",                  # course repo
    "davi-moreira.github.io",      # course site
    "purdue.brightspace.com",      # LMS
    "purdue.edu", "www.purdue.edu",  # university pages (IRB, URC)
    "scholar.google.com",          # verification workflow pointer
    "gemini.google.com",           # AI-tool pointer (syllabus stack)
}

# Works verified real during the build (each was independently confirmed to
# exist before being cited). Surname-anchored patterns, case-sensitive.
VERIFIED = [
    r"Blair.{0,40}Coppock.{0,40}Humphreys",          # RDSS 2023 (+ rdss pkg)
    r"Bergstrom.{0,20}West",                          # Calling Bullshit 2020
    r"Open Science Collaboration \(2015\)",           # Science 349, aac4716
    r"Tversky.{0,20}Kahneman.{0,10}\(?1974\)?",       # Judgment under Uncertainty
    r"Putnam.{0,15}\(?2000\)?",                       # Bowling Alone
    r"Pariser.{0,15}\(?2011\)?",                      # The Filter Bubble
    r"Foos et al\.|Foos, F",                          # rdss replication dataset
    r"Clingingsmith.{0,30}(Khwaja|Kremer)?",          # rdss replication dataset
    r"Bonilla.{0,15}Tillery",                         # rdss replication dataset
]

# Planted fakes (nb00 + nb03 hunts) — allowed ONLY with an in-notebook
# disclosure that fakes were planted.
PLANTED = ["Martinez, R., & Chen", "Thompson, K. E.", "Reynolds, D. M.",
           "Halvorsen, K."]
DISCLOSURE = re.compile(r"fabricated|invented for this exercise", re.I)

CITATION_SHAPE = re.compile(r"[A-Z][a-z]+, [A-Z]\.(?:[^(\n]{0,60})\((19|20)\d\d\)")


def audit(path: Path) -> list[str]:
    nb = json.loads(path.read_text())
    text = "\n".join("".join(c["source"]) for c in nb["cells"])
    problems = []

    # 1. URL allowlist
    for url in set(re.findall(r"https?://[^\s)\"'\]>]+", text)):
        host = urlparse(url).netloc
        if host not in ALLOWED_DOMAINS:
            problems.append(f"unknown URL domain (verify + allowlist): {url}")

    # 3. planted fakes containment
    disclosed = bool(DISCLOSURE.search(text))
    for fake in PLANTED:
        if fake in text and not disclosed:
            problems.append(f"planted fake {fake!r} without disclosure text")

    # 2. citation registry
    for m in set(CITATION_SHAPE.findall(text)) and set(
            x.group(0) for x in CITATION_SHAPE.finditer(text)):
        if any(re.search(v, m) for v in VERIFIED):
            continue
        if any(f.split(",")[0] in m for f in PLANTED):
            continue  # handled above
        problems.append(f"citation not in verified registry: {m!r}")

    return problems


def main() -> None:
    targets = ([Path(a) for a in sys.argv[1:]] or
               sorted((REPO / "notebooks" / "student").glob("nb*_student.ipynb")))
    failed = False
    for t in targets:
        probs = audit(t)
        if probs:
            failed = True
            print(f"✗ {t.name}")
            for p in probs:
                print("    " + p)
        else:
            print(f"✓ {t.name}")
    if failed:
        sys.exit(1)
    print(f"✓ citation-integrity audit clean across {len(targets)} notebook(s)")


if __name__ == "__main__":
    main()
