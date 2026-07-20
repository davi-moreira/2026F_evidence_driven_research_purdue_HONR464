#!/usr/bin/env python3
"""audit_sources.py — citation-integrity gate for student-facing notebooks.

The course's evidence-integrity rule (CLAUDE.md): every citation in shipped
material is real and retrievable; fabricated citations are forbidden EVERYWHERE
(Decision 16, 2026-07-20 — the planted-fake teaching device is retired;
verification exercises use real sources). This gate enforces the
machine-checkable half:

  1. External URL allowlist — every http(s) URL in a student notebook must be
     on the course's verified-domain allowlist (unknown domains fail).
  2. Verified-citation registry — "Author (Year)"-shaped citations must match
     the registry of works verified during the build (unknown ones fail until
     added here WITH a verification note).
  3. Fake-citation blocklist — the names once used as planted fakes must never
     appear in any student notebook, disclosed or not.

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
    "www.nytimes.com",             # nb00: Olinda carnival coverage (professor's own slide links)
    "blogs.worldbank.org",         # nb00: professor's World Bank work
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

# Fake-citation blocklist (D16): these names were once planted fakes; they must
# never appear in student material again, with or without disclosure.
BLOCKED = ["Martinez, R., & Chen", "Thompson, K. E.", "Reynolds, D. M.",
           "Halvorsen, K."]

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

    # 3. fake-citation blocklist (no disclosure exemption — D16)
    for fake in BLOCKED:
        if fake in text:
            problems.append(f"blocked fake citation {fake!r} (D16: fabricated "
                            f"citations are forbidden everywhere)")

    # 2. citation registry
    for m in set(CITATION_SHAPE.findall(text)) and set(
            x.group(0) for x in CITATION_SHAPE.finditer(text)):
        if any(re.search(v, m) for v in VERIFIED):
            continue
        if any(f.split(",")[0] in m for f in BLOCKED):
            continue  # already reported by the blocklist check
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
