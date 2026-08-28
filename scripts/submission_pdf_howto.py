#!/usr/bin/env python3
"""submission_pdf_howto.py — the ONE text that tells a student how to turn a
Colab notebook into the PDF a milestone collects.

Every milestone asks for `lastname_mNN.pdf`, and every student's work lives in a
Colab notebook, which has no export-to-PDF button. Until this module existed the
course never said, anywhere a student could read it, how to bridge the two. The
routine is short but every step of it is load-bearing: an unrun cell, a collapsed
section or a scrolling output prints as a blank, and a milestone arrives looking
half done.

Authored ONCE here and projected onto two surfaces, so they can never disagree:

  * scripts/build_handout_pdfs.py     appends it to every milestone PDF
  * scripts/build_milestone_anchors.py injects it into every milestone brief,
                                       inside the marker pair below, and its
                                       `--check` mode keeps it fresh in CI

CONSTRAINTS THIS TEXT MUST KEEP (enforced by build_handout_pdfs.py's scanner):
no em dashes, no calendar dates, no clock times, no semester labels. It is also
student-facing, so it is written TO the student in the second person and never
about "students".
"""
from __future__ import annotations

HEADING = "Making the PDF you hand in"

#: One line for the "What to submit" block, pointing at the section below.
POINTER = ("Your work lives in a Colab notebook, which has no export-to-PDF "
           "button. **{heading}**, at the end of this document, is the "
           "one-minute routine that turns the notebook into the file you "
           "upload.").format(heading=HEADING)

BEGIN = "<!-- submission-pdf-howto:begin -->"
END = "<!-- submission-pdf-howto:end -->"

BODY = """Colab has no export-to-PDF button. You make the PDF by **printing the
notebook to a file**, which takes about a minute once you know the preparation
steps. Skipping them is the most common way a milestone arrives looking half
finished, because a notebook prints what is on the screen and nothing else.

### 1. Prepare the notebook

1. **Run the whole thing.** `Runtime` → `Run all`, then wait for it to finish.
   A cell you never ran prints with nothing underneath it, so an analysis you
   really did can reach the grader as an empty box.
2. **Expand every collapsed section.** Anything folded shut prints as a heading
   with nothing beneath it. Open all of them, including any Colab folded for you.
3. **Shorten any output that scrolls.** When Colab puts a scrollbar on an output,
   or tells you the output is truncated, only the visible part prints. Show the
   first twenty rows instead of the whole table, or summarise it, then rerun that
   cell. A reader did not want the whole table anyway.
4. **Read it once, top to bottom.** You are about to freeze it.

### 2. Print it to a file

`File` → `Print` opens your browser's print dialog. Set the destination to
**Save as PDF**, open the dialog's further settings, and turn on **Background
graphics**, so code cells keep their shading and your figures keep their
backgrounds. Save it under the file name this milestone asks for.

Wide tables and wide figures are the usual casualty. If something runs off the
right edge, switch the layout to **landscape** or reduce the scale, and print
again.

### 3. Check the PDF before you upload it

Open the file you just made and confirm three things: every figure is whole
rather than sliced by a page break, no output stops mid-line, and the pages run
in order with nothing missing. A PDF is an artifact like any other in this
course, so you verify it before your name goes on it.

### One route not to take

Ask an AI assistant how to export a Colab notebook and it will very likely hand
you `jupyter nbconvert --to pdf`. Do not spend your afternoon on it. Inside
Colab that route needs a large LaTeX installation, runs for several minutes, and
then either fails or quietly drops the symbols and emoji these notebooks are
full of. Printing to a file is the route that works.

That is a small, cheap instance of the rule this whole course runs on. The
confident answer is not automatically the correct one, and the way you find out
is to check it against what actually happens."""


def markdown(level: int = 2) -> str:
    """The section, with its own heading at `level` (## in both surfaces)."""
    return f"{'#' * level} {HEADING}\n\n{BODY}\n"


def brief_block() -> str:
    """The marker-wrapped projection injected into each milestone brief."""
    return f"{BEGIN}\n{markdown()}{END}"
