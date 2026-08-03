#!/usr/bin/env python3
"""build_book_part1_figure.py — the book-organization figure (D27, D38).

A designed, monochrome figure in the book cover's aesthetic: the four
operating-rule lessons chained inside the Studio 1 frame, and the road of
Studios 2–12 beneath. Localized per edition, written to

    book/images/part1_arc.png   book-pt/images/...   book-es/images/...

(The filename keeps its historical name; the page that embeds it is the
"How this book is organized" front page.) Frozen editions (D36) are skipped.

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
        "container": "STUDIO 1  ·  Govern the work — the operating rules",
        "chapters": [
            ("Lesson 1 · The principle", "AI is your arm,\nnot your brain"),
            ("Lesson 2 · Your role", "the research\ndirector"),
            ("Lesson 3 · The protocol", "SDIIVDD, the loop of\nevery delegation"),
            ("Lesson 4 · The ownership", "your name\non the claim"),
        ],
        "parts": [
            ("STUDIOS 2–4", "frame the question,\nground it, declare it"),
            ("STUDIOS 5–6", "develop the pathway,\ngovern the data"),
            ("STUDIOS 7–8", "first analysis,\nstress-test it"),
            ("STUDIOS 9–10", "write and bound,\nadapt and defend"),
            ("STUDIOS 11–12", "reproduce, package,\nrelease"),
        ],
    },
    "book-pt": {
        "container": "ESTÚDIO 1  ·  Governar o trabalho — as regras de operação",
        "chapters": [
            ("Lição 1 · O princípio", "a IA é o seu braço,\nnão o seu cérebro"),
            ("Lição 2 · O seu papel", "quem dirige\na pesquisa"),
            ("Lição 3 · O protocolo", "SDIIVDD, o ciclo de\ncada delegação"),
            ("Lição 4 · A propriedade", "o seu nome\nna alegação"),
        ],
        "parts": [
            ("ESTÚDIOS 2–4", "formular a pergunta,\nfundamentar, declarar"),
            ("ESTÚDIOS 5–6", "desenvolver a trilha,\ngovernar os dados"),
            ("ESTÚDIOS 7–8", "primeira análise,\nteste de estresse"),
            ("ESTÚDIOS 9–10", "escrever e delimitar,\nadaptar e defender"),
            ("ESTÚDIOS 11–12", "reproduzir, empacotar,\nliberar"),
        ],
    },
    "book-es": {
        "container": "ESTUDIO 1  ·  Gobernar el trabajo — las reglas de operación",
        "chapters": [
            ("Lección 1 · El principio", "la IA es tu brazo,\nno tu cerebro"),
            ("Lección 2 · Tu papel", "quien dirige la\ninvestigación"),
            ("Lección 3 · El protocolo", "SDIIVDD, el ciclo de\ncada delegación"),
            ("Lección 4 · La propiedad", "tu nombre en\nla afirmación"),
        ],
        "parts": [
            ("ESTUDIOS 2–4", "formular la pregunta,\nfundamentar, declarar"),
            ("ESTUDIOS 5–6", "desarrollar la ruta,\ngobernar los datos"),
            ("ESTUDIOS 7–8", "primer análisis,\nprueba de estrés"),
            ("ESTUDIOS 9–10", "escribir y delimitar,\nadaptar y defender"),
            ("ESTUDIOS 11–12", "reproducir, empaquetar,\nliberar"),
        ],
    },
}

# D36: frozen editions are never regenerated; their figures stay at the
# snapshot. The labels above are kept current so the translation pass can
# simply re-run this script with the freeze lifted.
ACTIVE_EDITIONS = ("book",)


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
        if edition not in ACTIVE_EDITIONS:
            print(f"— {edition}: frozen (D36), skipped")
            continue
        out = REPO / edition / "images" / "part1_arc.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        build(strings, out)
        print(f"✓ {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
