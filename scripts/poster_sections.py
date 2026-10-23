#!/usr/bin/env python3
"""poster_sections.py — the poster's sections, once (D87 amended; D89).

The course poster template (`project/poster/honr464_poster_template.pptx`,
built by scripts/build_poster_kit.py) carries thirteen sections. D89
(2026-10-23) made the M9 research note the poster's FIRST FULL DRAFT: the
note is written under the same thirteen headings, in the same order, so every
panel of the board already has its text when the poster draft is due at M10.

This list is the one place those sections live. It feeds:

  * the template's section bars        (scripts/build_poster_kit.py)
  * the M9 brief's note-sections block  (scripts/build_poster_kit.py writes it
                                         between NOTE_BEGIN / NOTE_END)
  * the M9 PDF's "What this course adds" (scripts/build_handout_pdfs.py fills
                                         the {{NOTE_SECTIONS}} token)
  * the M9 studio workbench             (_production_kit/nb_sources/ms08_*.py)

Change a section here, rerun build_poster_kit.py, build_handout_pdfs.py and
`nbbuild.py ms08`, and the template, the brief, the PDF and the workbench move
together. No date, no clock time, no em dash: the PDF gates apply to this text.
"""
from __future__ import annotations

NOTE_BEGIN = "<!-- note-sections:begin -->"
NOTE_END = "<!-- note-sections:end -->"
TOKEN = "{{NOTE_SECTIONS}}"

#: In reading order: column 1, then 2, 3 and 4 of the template.
#: `heading` is the section bar's text (the template prints it in capitals);
#: `note` is what the research note writes under that heading at M9.
SECTIONS: list[dict] = [
    {"key": "abstract", "column": 1, "heading": "Abstract",
     "note": ("Your conference abstract, updated to your verified results: one paragraph of up "
              "to 150 words with the question and its answer, what the literature concludes "
              "and what you add, the data and the design, and the main result with its "
              "uncertainty and the limitation that matters most. Add one line saying what "
              "changed since you submitted it.")},
    {"key": "question", "column": 1, "heading": "The question and why it matters",
     "note": ("Your research question in one sentence, as your Research Contract declares it, "
              "with its kind and its reach; why it matters, and to whom; your main hypothesis "
              "as you recorded it before the analysis ran.")},
    {"key": "known", "column": 1, "heading": "What is already known",
     "note": ("The main conclusion of the literature, from at least two sources you read "
              "yourself; the gap; and what your project adds. With the question above, this "
              "is your problem-gap-question spine.")},
    {"key": "design", "column": 2, "heading": "Design: what your claim needs",
     "note": ("Kind, reach, target and warrant, one line each, plus the identification "
              "status. A causal question your design cannot identify is a causal target, "
              "currently unidentified, never relabeled descriptive.")},
    {"key": "data", "column": 2, "heading": "Data and measurement",
     "note": ("Source and route with retrieval dates; observations kept apart from "
              "independent units; the time window; each concept and the measure that stands "
              "for it; missing data; permissions.")},
    {"key": "methods", "column": 2, "heading": "Methods",
     "note": ("The analysis you declared before seeing results and why it fits your design, "
              "with any later change and its reason; how you computed the uncertainty, at the "
              "level of your independent unit, with any dependence named; software and seed.")},
    {"key": "result", "column": 3, "heading": "Main result",
     "note": ("The result in numbers and units, with its interval in the same sentence, and "
              "the figure you plan to print, captioned with the notebook cell that drew it.")},
    {"key": "checks", "column": 3, "heading": "Checks and verification",
     "note": ("The checks from your robustness audit and what each one changed, and what has "
              "been reproduced so far, by whom and when.")},
    {"key": "conclusions", "column": 4, "heading": "Conclusions",
     "note": ("Your bounded headline claim, carrying its kind and its reach, then what this "
              "evidence supports and what it does not yet support.")},
    {"key": "limitations", "column": 4, "heading": "Limitations",
     "note": ("The two or three limitations that genuinely threaten the claim, led by the one "
              "your robustness audit could not fix, each with the next step that would "
              "settle it.")},
    {"key": "ai", "column": 4, "heading": "AI use disclosure",
     "note": ("Drafted from your AI Research Ledger: for each tool, the task, what you changed "
              "or kept, and how you checked it; what you sent to tools; and what you did not "
              "verify.")},
    {"key": "references", "column": 4, "heading": "References",
     "note": ("Every source the note cites, each one retrievable: author, year, title, venue, "
              "DOI or URL.")},
    {"key": "acknowledgments", "column": 4, "heading": "Acknowledgments",
     "note": ("One line is enough: your mentor, and anyone who provided data, took part, or "
              "funded the work.")},
]

_WORDS = {10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen"}


def count_word() -> str:
    """'thirteen' today; follows the list if a section is added or removed."""
    return _WORDS.get(len(SECTIONS), str(len(SECTIONS)))


def heading(key: str) -> str:
    """The section bar's text, as the template prints it."""
    for s in SECTIONS:
        if s["key"] == key:
            return s["heading"].upper()
    raise KeyError(f"no poster section {key!r}")


def note_sections_markdown() -> str:
    """The lead and the table every surface prints (brief, PDF, workbench)."""
    lines = [
        "Open with your working title and your **headline sentence**: the bounded claim,",
        "with its interval or its boundary in the same sentence, as it will run in the",
        "poster's headline banner. Then write the "
        f"{count_word()} sections of the course poster",
        "template, in its order, each under its own heading:",
        "",
        "| # | Section | What your note writes there |",
        # Dash counts set the PDF's column widths (Pandoc pipe tables): about 4 / 32 / 64.
        "|--|----------------|--------------------------------|",
    ]
    for i, s in enumerate(SECTIONS, 1):
        lines.append(f"| {i} | **{s['heading']}** | {s['note']} |")
    return "\n".join(lines)


def brief_block() -> str:
    """The generated block for the M9 brief, markers included."""
    return "\n".join([
        NOTE_BEGIN,
        "<!-- Generated by scripts/build_poster_kit.py (D89) from",
        "     scripts/poster_sections.py. Edit that list and rerun; edits here are",
        "     overwritten. -->",
        "",
        note_sections_markdown(),
        "",
        NOTE_END,
    ])


if __name__ == "__main__":
    print(note_sections_markdown())
