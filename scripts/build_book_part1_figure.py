#!/usr/bin/env python3
"""build_book_part1_figure.py — the Part I overview figure (D27).

Replaces the retired mermaid flowchart with a designed, monochrome figure in
the book cover's aesthetic: the four Part I chapters chained inside a Part I
frame, and the Part II–VI road beneath. Localized per edition, written to

    book/images/part1_arc.png   book-pt/images/...   book-es/images/...

Rerun after editing the labels here:
    .venv/bin/python scripts/build_book_part1_figure.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

REPO = Path(__file__).resolve().parent.parent
INK, SOFT, FILL = "#1a1a19", "#8a8a86", "#f4f4f3"

L = {
    "book": {
        "container": "PART I  ·  Research when AI does “everything”",
        "chapters": [
            ("Ch. 1 · The principle", "AI is your arm,\nnot your brain"),
            ("Ch. 2 · Your role", "the research\ndirector"),
            ("Ch. 3 · The protocol", "SDIIVDD, the loop of\nevery delegation"),
            ("Ch. 4 · The ownership", "your name\non the claim"),
        ],
        "parts": [
            ("PART II", "From curiosity to\nresearch design"),
            ("PART III", "Research\npathways"),
            ("PART IV", "Credible evidence\nwith AI"),
            ("PART V", "Communicating and\ndefending research"),
            ("PART VI", "Research after\nthe conference"),
        ],
    },
    "book-pt": {
        "container": "PARTE I  ·  Pesquisa quando a IA faz “tudo”",
        "chapters": [
            ("Cap. 1 · O princípio", "a IA é o seu braço,\nnão o seu cérebro"),
            ("Cap. 2 · O seu papel", "quem dirige\na pesquisa"),
            ("Cap. 3 · O protocolo", "SDIIVDD, o ciclo de\ncada delegação"),
            ("Cap. 4 · A propriedade", "o seu nome\nna alegação"),
        ],
        "parts": [
            ("PARTE II", "Da curiosidade ao\ndesenho de pesquisa"),
            ("PARTE III", "Trilhas de\npesquisa"),
            ("PARTE IV", "Evidência crível\ncom IA"),
            ("PARTE V", "Comunicar e defender\na pesquisa"),
            ("PARTE VI", "A pesquisa depois\nda conferência"),
        ],
    },
    "book-es": {
        "container": "PARTE I  ·  Investigar cuando la IA lo hace “todo”",
        "chapters": [
            ("Cap. 1 · El principio", "la IA es tu brazo,\nno tu cerebro"),
            ("Cap. 2 · Tu papel", "quien dirige la\ninvestigación"),
            ("Cap. 3 · El protocolo", "SDIIVDD, el ciclo de\ncada delegación"),
            ("Cap. 4 · La propiedad", "tu nombre en\nla afirmación"),
        ],
        "parts": [
            ("PARTE II", "De la curiosidad al\ndiseño de investigación"),
            ("PARTE III", "Rutas de\ninvestigación"),
            ("PARTE IV", "Evidencia creíble\ncon IA"),
            ("PARTE V", "Comunicar y defender\nla investigación"),
            ("PARTE VI", "La investigación\ntras la conferencia"),
        ],
    },
}


def box(ax, cx, cy, w, h, fc, ec, lw=1.1, r=0.018):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw))


def arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1,
                                shrinkA=0, shrinkB=0, mutation_scale=11))


def build(strings: dict, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(9.2, 5.0))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    # Part I frame
    box(ax, .5, .715, .92, .47, "white", INK, lw=1.5, r=0.025)
    ax.text(.5, .895, strings["container"], ha="center", va="center",
            fontsize=11.5, fontweight="bold", color=INK)

    # the four chapters, chained
    cxs = [.155, .385, .615, .845]
    for i, (cx, (head, sub)) in enumerate(zip(cxs, strings["chapters"])):
        box(ax, cx, .66, .195, .27, "white", SOFT, lw=1.0)
        ax.text(cx, .715, head, ha="center", va="center", fontsize=9.3,
                fontweight="bold", color=INK)
        ax.text(cx, .615, sub, ha="center", va="center", fontsize=8.4,
                color="#444440", linespacing=1.35)
        if i:
            arrow(ax, cxs[i - 1] + .0975, .66, cx - .0975, .66)

    # down to the road
    arrow(ax, .124, .48, .124, .315)

    # Parts II–VI
    pxs = [.124, .312, .5, .688, .876]
    for i, (px, (head, sub)) in enumerate(zip(pxs, strings["parts"])):
        box(ax, px, .175, .168, .225, FILL, SOFT, lw=1.0)
        ax.text(px, .225, head, ha="center", va="center", fontsize=9.3,
                fontweight="bold", color=INK)
        ax.text(px, .135, sub, ha="center", va="center", fontsize=8.0,
                color="#444440", linespacing=1.35)
        if i:
            arrow(ax, pxs[i - 1] + .084, .175, px - .084, .175)

    fig.tight_layout(pad=0.4)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def main() -> None:
    for edition, strings in L.items():
        out = REPO / edition / "images" / "part1_arc.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        build(strings, out)
        print(f"✓ {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
