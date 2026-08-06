#!/usr/bin/env python3
"""build_book_concept_figures.py — the book's own framework diagrams (D48).

D48 removed the RDSS figure conversions from the repository: an exact
reproduction of a copyrighted figure is not made safe by a README credit.
The concepts still deserve pictures, so the book draws its OWN, in the same
monochrome house style as the organization figure
(``build_book_part1_figure.py``). The frameworks are credited in the prose
that surrounds each figure; the drawings are this book's.

    book/images/concepts/mida_map.png         (ch9)
    book/images/concepts/diagnose_loop.png    (ch10)
    book/images/concepts/sampling_groups.png  (ch11)

Localized per edition; frozen editions (D36) are skipped. Rerun after
editing the labels here:

    .venv/bin/python scripts/build_book_concept_figures.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

REPO = Path(__file__).resolve().parent.parent
INK, SOFT, FILL = "#1a1a19", "#8a8a86", "#f4f4f3"
MUTE = "#444440"

L = {
    "book": {
        "mida": {
            "rows": ("ON PAPER", "IN THE WORLD"),
            "cells": [
                ("MODEL", "how the world\ncould work"),
                ("INQUIRY", "the one quantity\nyou want from it"),
                ("DATA STRATEGY", "every procedure that\nmakes the data:\nsampling, assignment,\nmeasurement"),
                ("ANSWER STRATEGY", "how those data\nbecome an answer,\nuncertainty included"),
            ],
            "top_link": "makes askable",
            "bottom_link": "feeds",
            "align": "alignment: does the answer\nreach the inquiry?",
            "foot": "Four parts, one question. A design holds together when the bottom row actually reaches the top right.",
        },
        "loop": {
            "steps": [
                ("DECLARE", "write the design as\nsomething a computer\ncould run"),
                ("DIAGNOSE", "run it over many\nsimulated worlds and\nwatch how it behaves"),
                ("REDESIGN", "change exactly one\nthing, then diagnose\nagain"),
            ],
            "readout": "read out: bias  ·  wobble  ·  how often it detects",
            "return": "one change at a time",
            "call": "THE HONEST CALL: run it as declared, redesign again, or narrow the claim to what this design can deliver",
        },
        "groups": {
            "target": "TARGET POPULATION",
            "target_sub": "everyone your question is about",
            "accessible": "ACCESSIBLE POPULATION",
            "accessible_sub": "who you could reach in principle",
            "frame": "SAMPLING FRAME",
            "frame_sub": "the list you actually draw from",
            "sample": "SAMPLE",
            "miss": "eligible people the\nframe never lists",
            "extra": "units the frame lists that\ndo not belong, plus\nduplicates drawn twice",
            "foot": "The frame is not a tidy slice of the population above it. That is where a description quietly goes wrong.",
        },
    },
    "book-pt": {
        "mida": {
            "rows": ("NO PAPEL", "NO MUNDO"),
            "cells": [
                ("MODELO", "como o mundo\npoderia funcionar"),
                ("INDAGAÇÃO", "a única quantidade\nque você quer dele"),
                ("ESTRATÉGIA DE DADOS", "todo procedimento que\ncria os dados: amostragem,\natribuição, mensuração"),
                ("ESTRATÉGIA DE RESPOSTA", "como esses dados\nviram resposta,\nincerteza incluída"),
            ],
            "top_link": "torna perguntável",
            "bottom_link": "alimenta",
            "align": "alinhamento: a resposta\nalcança a indagação?",
            "foot": "Quatro partes, uma pergunta. O desenho se sustenta quando a linha de baixo alcança o alto à direita.",
        },
        "loop": {
            "steps": [
                ("DECLARAR", "escrever o desenho como\nalgo que um computador\npoderia rodar"),
                ("DIAGNOSTICAR", "rodá-lo em muitos\nmundos simulados e ver\ncomo ele se comporta"),
                ("REDESENHAR", "mudar exatamente uma\ncoisa e diagnosticar\nde novo"),
            ],
            "readout": "leitura: viés  ·  oscilação  ·  com que frequência detecta",
            "return": "uma mudança por vez",
            "call": "A DECISÃO HONESTA: rodar como declarado, redesenhar de novo, ou estreitar a alegação ao que este desenho entrega",
        },
        "groups": {
            "target": "POPULAÇÃO-ALVO",
            "target_sub": "todos sobre quem é a sua pergunta",
            "accessible": "POPULAÇÃO ACESSÍVEL",
            "accessible_sub": "quem você poderia alcançar em princípio",
            "frame": "CADASTRO AMOSTRAL",
            "frame_sub": "a lista de onde você de fato sorteia",
            "sample": "AMOSTRA",
            "miss": "gente elegível que o\ncadastro nunca lista",
            "extra": "unidades listadas que não\npertencem, mais duplicatas\nsorteadas duas vezes",
            "foot": "O cadastro não é uma fatia limpa da população acima dele. É aí que uma descrição erra em silêncio.",
        },
    },
    "book-es": {
        "mida": {
            "rows": ("EN EL PAPEL", "EN EL MUNDO"),
            "cells": [
                ("MODELO", "cómo podría\nfuncionar el mundo"),
                ("INDAGACIÓN", "la única cantidad\nque quieres de él"),
                ("ESTRATEGIA DE DATOS", "todo procedimiento que\ncrea los datos: muestreo,\nasignación, medición"),
                ("ESTRATEGIA DE RESPUESTA", "cómo esos datos\nse vuelven respuesta,\nincertidumbre incluida"),
            ],
            "top_link": "hace preguntable",
            "bottom_link": "alimenta",
            "align": "alineación: ¿la respuesta\nalcanza la indagación?",
            "foot": "Cuatro partes, una pregunta. El diseño se sostiene cuando la fila de abajo alcanza la de arriba a la derecha.",
        },
        "loop": {
            "steps": [
                ("DECLARAR", "escribir el diseño como\nalgo que una computadora\npodría ejecutar"),
                ("DIAGNOSTICAR", "ejecutarlo en muchos\nmundos simulados y ver\ncómo se comporta"),
                ("REDISEÑAR", "cambiar exactamente una\ncosa y diagnosticar\nde nuevo"),
            ],
            "readout": "lectura: sesgo  ·  oscilación  ·  con qué frecuencia detecta",
            "return": "un cambio a la vez",
            "call": "LA DECISIÓN HONESTA: ejecutar como se declaró, rediseñar otra vez, o estrechar la afirmación a lo que este diseño entrega",
        },
        "groups": {
            "target": "POBLACIÓN OBJETIVO",
            "target_sub": "todos sobre quienes trata tu pregunta",
            "accessible": "POBLACIÓN ACCESIBLE",
            "accessible_sub": "a quiénes podrías llegar en principio",
            "frame": "MARCO MUESTRAL",
            "frame_sub": "la lista de la que realmente sorteas",
            "sample": "MUESTRA",
            "miss": "gente elegible que el\nmarco nunca lista",
            "extra": "unidades listadas que no\ncorresponden, más duplicados\nsorteados dos veces",
            "foot": "El marco no es una rebanada limpia de la población de arriba. Ahí es donde una descripción falla en silencio.",
        },
    },
}

# D36: frozen editions are never regenerated; labels above stay current so the
# translation pass can rerun this script once the freeze lifts.
ACTIVE_EDITIONS = ("book",)


def box(ax, cx, cy, w, h, fc, ec, lw=1.1, r=0.018, ls="solid", z=2):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls, zorder=z))


def arrow(ax, x0, y0, x1, y1, ls="solid", color=INK, rad=0.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=4,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.1,
                                linestyle=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=11,
                                connectionstyle=f"arc3,rad={rad}"))


def build_mida(S: dict, out: Path) -> None:
    """The four parts of a design, and the alignment check between them."""
    fig, ax = plt.subplots(figsize=(9.4, 4.9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    cxs, cys = (.375, .755), (.735, .335)
    w, h = .30, .245
    coords = [(cxs[0], cys[0]), (cxs[1], cys[0]),
              (cxs[0], cys[1]), (cxs[1], cys[1])]

    for (cx, cy), (head, sub) in zip(coords, S["cells"]):
        strong = cy == cys[0]
        box(ax, cx, cy, w, h, "white" if strong else FILL, INK if strong else SOFT,
            lw=1.4 if strong else 1.0, r=.028)
        ax.text(cx, cy + .072, head, ha="center", va="center",
                fontsize=8.4, fontweight="bold", color=INK)
        ax.text(cx, cy - .035, sub, ha="center", va="center",
                fontsize=6.8, color=MUTE, linespacing=1.35)

    # row labels down the left edge
    for cy, label in zip(cys, S["rows"]):
        ax.text(.045, cy, label, ha="center", va="center", rotation=90,
                fontsize=7.4, fontweight="bold", color=SOFT)
    ax.plot([.105, .105], [.20, .87], color=SOFT, lw=.8, zorder=1)

    # within-row links
    arrow(ax, cxs[0] + w / 2, cys[0], cxs[1] - w / 2, cys[0])
    ax.text((cxs[0] + cxs[1]) / 2, cys[0] + .033, S["top_link"], ha="center",
            va="center", fontsize=6.4, color=MUTE, style="italic")
    arrow(ax, cxs[0] + w / 2, cys[1], cxs[1] - w / 2, cys[1])
    ax.text((cxs[0] + cxs[1]) / 2, cys[1] + .033, S["bottom_link"], ha="center",
            va="center", fontsize=6.4, color=MUTE, style="italic")

    # the alignment check: does the answer reach the inquiry?
    arrow(ax, cxs[1], cys[1] + h / 2, cxs[1], cys[0] - h / 2, ls="dashed")
    ax.text(.615, (cys[0] + cys[1]) / 2, S["align"], ha="center",
            va="center", fontsize=6.8, color=INK, linespacing=1.35)

    ax.text(.5, .075, S["foot"], ha="center", va="center", fontsize=7.2,
            color=MUTE)

    fig.tight_layout(pad=0.4)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_loop(S: dict, out: Path) -> None:
    """Declare, diagnose, redesign: the loop and the call that ends it."""
    fig, ax = plt.subplots(figsize=(9.8, 4.0))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    row_y, w, h = .72, .245, .27
    cxs = [.18, .5, .82]
    for cx, (head, sub) in zip(cxs, S["steps"]):
        box(ax, cx, row_y, w, h, "white", INK, lw=1.4, r=.03)
        ax.text(cx, row_y + .078, head, ha="center", va="center",
                fontsize=8.6, fontweight="bold", color=INK)
        ax.text(cx, row_y - .038, sub, ha="center", va="center",
                fontsize=6.8, color=MUTE, linespacing=1.35)

    arrow(ax, cxs[0] + w / 2, row_y, cxs[1] - w / 2, row_y)
    arrow(ax, cxs[1] + w / 2, row_y, cxs[2] - w / 2, row_y)

    # the return leg, routed under the row so it crosses nothing
    leg_y = .43
    ax.plot([cxs[2], cxs[2]], [row_y - h / 2, leg_y], color=INK, lw=1.1,
            zorder=3)
    ax.plot([cxs[2], cxs[0]], [leg_y, leg_y], color=INK, lw=1.1, zorder=3)
    arrow(ax, cxs[0], leg_y, cxs[0], row_y - h / 2)
    ax.text(.5, .375, S["return"], ha="center", va="center", fontsize=6.6,
            color=MUTE, style="italic")

    # what the middle step reads out
    ax.text(.5, .885, S["readout"], ha="center", va="center", fontsize=7.0,
            color=INK)

    # the exit: the call only you make
    box(ax, .5, .175, .84, .14, FILL, SOFT, lw=1.0, r=.025)
    ax.text(.5, .175, S["call"], ha="center", va="center", fontsize=7.0,
            color=INK)

    fig.tight_layout(pad=0.4)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_groups(S: dict, out: Path) -> None:
    """The four groups a description keeps straight, drawn honestly: the
    frame overlaps the accessible population instead of nesting inside it."""
    fig, ax = plt.subplots(figsize=(9.4, 5.0))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    def region(x0, x1, y0, y1, fc, ec, lw, ls="solid", z=2):
        box(ax, (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, fc, ec,
            lw=lw, r=.02, ls=ls, z=z)

    region(.06, .90, .21, .93, "white", INK, 1.5)
    ax.text(.085, .885, S["target"], ha="left", va="center", fontsize=8.2,
            fontweight="bold", color=INK, zorder=5)
    ax.text(.085, .852, S["target_sub"], ha="left", va="center", fontsize=6.6,
            color=MUTE, zorder=5)

    region(.11, .60, .28, .80, FILL, SOFT, 1.1)
    ax.text(.132, .762, S["accessible"], ha="left", va="center", fontsize=7.6,
            fontweight="bold", color=INK, zorder=5)
    ax.text(.132, .731, S["accessible_sub"], ha="left", va="center",
            fontsize=6.4, color=MUTE, zorder=5)

    region(.40, .855, .35, .70, "none", INK, 1.4, ls="dashed", z=3)
    ax.text(.833, .663, S["frame"], ha="right", va="center", fontsize=7.6,
            fontweight="bold", color=INK, zorder=5)
    ax.text(.833, .632, S["frame_sub"], ha="right", va="center", fontsize=6.4,
            color=MUTE, zorder=5)

    region(.45, .57, .42, .55, INK, INK, 1.0, z=4)
    ax.text(.51, .485, S["sample"], ha="center", va="center", fontsize=7.4,
            fontweight="bold", color="white", zorder=6)

    # what the overlap teaches
    ax.annotate(S["miss"], xy=(.20, .45), xytext=(.175, .13),
                ha="center", va="center", fontsize=6.8, color=INK,
                linespacing=1.35, zorder=6,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0,
                                mutation_scale=10))
    ax.annotate(S["extra"], xy=(.735, .40), xytext=(.735, .13),
                ha="center", va="center", fontsize=6.8, color=INK,
                linespacing=1.35, zorder=6,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0,
                                mutation_scale=10))

    ax.text(.5, .025, S["foot"], ha="center", va="center", fontsize=7.2,
            color=MUTE)

    fig.tight_layout(pad=0.4)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


BUILDERS = (
    ("mida", "mida_map.png", build_mida),
    ("loop", "diagnose_loop.png", build_loop),
    ("groups", "sampling_groups.png", build_groups),
)


def main() -> None:
    for edition, strings in L.items():
        if edition not in ACTIVE_EDITIONS:
            print(f"— {edition}: frozen (D36), skipped")
            continue
        out_dir = REPO / edition / "images" / "concepts"
        out_dir.mkdir(parents=True, exist_ok=True)
        for key, filename, builder in BUILDERS:
            out = out_dir / filename
            builder(strings[key], out)
            print(f"✓ {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
