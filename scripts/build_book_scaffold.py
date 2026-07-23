#!/usr/bin/env python3
"""build_book_scaffold.py — generate the Quarto book project from BOOK_MAP.

Reads the 37-chapter manifest in planning/BOOK_MAP.md and writes, under book/:
  * _quarto.yml   — a Quarto BOOK project (output-dir ../docs/book), chapters
                    grouped into the six parts
  * index.qmd     — the preface
  * <part-slug>/<NN>-<slug>.qmd — one chapter file each, carrying the frontmatter
                    title, a Colab badge to its PRIMARY notebook, and the
                    ten-element section skeleton (validate_book_sync checks these)

Existing chapter files are NOT overwritten unless --force is passed, so the
chapter-authoring pass can fill them and re-running the scaffold is safe.

Usage: python3 scripts/build_book_scaffold.py [--force]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from notebooks_map import NOTEBOOKS, student_filename, REPO_SLUG  # noqa: E402

BOOK_MAP = REPO / "planning" / "BOOK_MAP.md"
BOOK = REPO / "book"

PART_TITLES = {
    "I": "Part I — Research when AI can produce almost everything",
    "II": "Part II — From curiosity to research design",
    "III": "Part III — Research pathways",
    "IV": "Part IV — Producing credible evidence with AI",
    "V": "Part V — Communicating and defending research",
    "VI": "Part VI — Research after the conference",
}
PART_SLUGS = {
    "I": "part1-research-with-ai", "II": "part2-curiosity-to-design",
    "III": "part3-pathways", "IV": "part4-credible-evidence",
    "V": "part5-communicating", "VI": "part6-after-conference",
}
PART_ORDER = ["I", "II", "III", "IV", "V", "VI"]


def slugify(title: str) -> str:
    s = title.lower().replace("–", "-").replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def colab_url(nb: int) -> str:
    return (f"https://colab.research.google.com/github/{REPO_SLUG}/"
            f"blob/main/notebooks/student/{student_filename(nb)}")


def parse_manifest() -> list[dict]:
    rows = []
    for line in BOOK_MAP.read_text().splitlines():
        m = re.match(r"\|\s*([IVX]+)\b[^|]*\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*nb(\d\d)\s*\|", line)
        if m:
            rows.append({"part": m.group(1), "ch": int(m.group(2)),
                         "title": m.group(3), "nb": int(m.group(4))})
    return rows


def chapter_stub(ch: dict) -> str:
    nb = ch["nb"]
    title = ch["title"]
    lab = NOTEBOOKS[nb][1]
    return f"""---
title: "{ch['ch']}. {title}"
---

[![Open the lab in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url(nb)}){{target="_blank"}}

> **The research decision.** *(Forthcoming — one or two sentences naming the exact
> decision this chapter equips you to make and defend.)*

## Why this decision matters

*(Forthcoming.)*

## The concept

*(Forthcoming — plain-language explanation; every term introduced as bold term →
one-sentence definition → concrete example before it is used again.)*

## A worked example

*(Forthcoming — a STEM-relevant worked example.)*

## The Colab laboratory

This chapter's lab is notebook **nb{nb:02d} — {lab}**. Open it in Colab with the
badge above and work the cells alongside this chapter.

## Recommended AI prompts

*(Forthcoming — commit-first, delegable prompt sequences with an "After running,
verify" step that names the failure mode it counters.)*

::: {{.callout-important title="Do not delegate"}}
*(Forthcoming — the decisions in this chapter that stay yours alone.)*
:::

## An AI failure case

*(Forthcoming — a realistic case where an AI tool is confidently wrong here, and
how you catch it.)*

## Verification laboratory

*(Forthcoming — how to verify the chapter's key result yourself.)*

## Project transfer

*(Forthcoming — how this chapter advances your own research project and its
milestone.)*

## Defend your decision

*(Forthcoming — a short prompt asking you to state and defend the decision this
chapter equips, with its boundary and uncertainty.)*
"""


def main() -> None:
    force = "--force" in sys.argv
    chapters = parse_manifest()
    if len(chapters) != 37:
        sys.exit(f"✗ expected 37 chapters in BOOK_MAP, found {len(chapters)}")

    BOOK.mkdir(exist_ok=True)

    # --- _quarto.yml -------------------------------------------------------
    lines = [
        "project:",
        "  type: book",
        "  output-dir: ../docs/book",
        "",
        "book:",
        '  title: "Evidence-Driven Research"',
        '  subtitle: "How to Design, Analyze, Verify, and Defend Empirical Research"',
        '  author: "Professor Davi Moreira"',
        '  description: "The course book for HONR 46400 (Purdue Honors). RDSS is the theory text; this is the AI-era research manual, synchronized with the 16 course notebooks."',
        "  chapters:",
        "    - index.qmd",
    ]
    by_part: dict[str, list[dict]] = {}
    for c in chapters:
        by_part.setdefault(c["part"], []).append(c)
    for p in PART_ORDER:
        lines.append(f'    - part: "{PART_TITLES[p]}"')
        lines.append("      chapters:")
        for c in sorted(by_part[p], key=lambda x: x["ch"]):
            fn = f"{PART_SLUGS[p]}/{c['ch']:02d}-{slugify(c['title'])}.qmd"
            lines.append(f"        - {fn}")
    lines += [
        "",
        "format:",
        "  html:",
        "    theme: cosmo",
        "    toc: true",
        "",
        "editor: visual",
        "",
    ]
    (BOOK / "_quarto.yml").write_text("\n".join(lines))

    # --- index.qmd ---------------------------------------------------------
    (BOOK / "index.qmd").write_text(
        '# Preface {.unnumbered}\n\n'
        "**Evidence-Driven Research** is the course book for HONR 46400 at Purdue's\n"
        "Honors College. Its one message: *AI is your arm and your research\n"
        "assistant, not your brain.* You will direct AI tools through the\n"
        "**Specify → Delegate → Interrogate → Inspect → Verify → Document → Defend**\n"
        "workflow while keeping every research decision your own.\n\n"
        "Blair, Coppock and Humphreys' *Research Design in the Social Sciences*\n"
        "(free at [book.declaredesign.org](https://book.declaredesign.org)) remains\n"
        "the theory text. This book is the course's own AI-era manual: each chapter\n"
        "names a research decision, works a STEM example, links a Colab lab, shows\n"
        "an AI failure and how to catch it, and asks you to defend a claim. The\n"
        "chapters track the sixteen course notebooks; open each chapter's lab and\n"
        "work them together.\n\n"
        "The book has six parts: research when AI can produce almost everything;\n"
        "from curiosity to research design; the research pathways (observational and\n"
        "experimental, descriptive and causal, and prediction); producing credible\n"
        "evidence with AI; communicating and defending research; and research after\n"
        "the conference.\n"
    )

    # --- chapter stubs -----------------------------------------------------
    written, skipped = 0, 0
    for p in PART_ORDER:
        (BOOK / PART_SLUGS[p]).mkdir(exist_ok=True)
        for c in by_part[p]:
            fn = BOOK / PART_SLUGS[p] / f"{c['ch']:02d}-{slugify(c['title'])}.qmd"
            if fn.exists() and not force:
                skipped += 1
                continue
            fn.write_text(chapter_stub(c))
            written += 1

    print(f"✓ book scaffold: _quarto.yml + index.qmd + {written} chapter stub(s) "
          f"written, {skipped} existing kept")
    print("  render with:  quarto render book/")


if __name__ == "__main__":
    main()
