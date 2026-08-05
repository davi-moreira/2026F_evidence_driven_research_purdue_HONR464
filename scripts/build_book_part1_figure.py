#!/usr/bin/env python3
"""build_book_part1_figure.py — the book-organization figure (D27, D38, D43).

D43 retired the Studio-1-contains-the-book frame. The figure is now the
research road: the reader's curiosity enters on the left, six road stages
(Studio 1 through Studios 11–12) carry it to a released claim on the right,
and the four persistent rails run beneath the whole road. Monochrome, in
the book cover's aesthetic. Localized per edition, written to

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
        "start": ("YOUR CURIOSITY", "a question that\nwill not leave\nyou alone"),
        "end": ("YOUR DECISION", "release, defended,\nor honestly withheld;\nthe next study opens"),
        "road": [
            ("STUDIO 1", "begin the research,\ngovern the work"),
            ("STUDIOS 2–4", "frame the question,\nground it, declare it"),
            ("STUDIOS 5–6", "develop the pathway,\ngovern the data"),
            ("STUDIOS 7–8", "first analysis,\nstress-test it"),
            ("STUDIOS 9–10", "write and bound,\nadapt and defend"),
            ("STUDIOS 11–12", "reproduce, package;\ndirect agents, release"),
        ],
        "rails_title": "Four rails cross every studio",
        "rails": [
            "Ethics, permissions, and data exposure",
            "Evidence, provenance, and reproducibility",
            "AI activity, verification, and human decisions",
            "Uncertainty, claim boundary, and revision history",
        ],
    },
    "book-pt": {
        "start": ("SUA CURIOSIDADE", "uma pergunta que\nnão sai da\nsua cabeça"),
        "end": ("SUA DECISÃO", "publicar, defendida,\nou reter com honestidade;\no próximo estudo abre"),
        "road": [
            ("ESTÚDIO 1", "começar a pesquisa,\ngovernar o trabalho"),
            ("ESTÚDIOS 2–4", "formular a pergunta,\nfundamentar, declarar"),
            ("ESTÚDIOS 5–6", "desenvolver a trilha,\ngovernar os dados"),
            ("ESTÚDIOS 7–8", "primeira análise,\nteste de estresse"),
            ("ESTÚDIOS 9–10", "escrever e delimitar,\nadaptar e defender"),
            ("ESTÚDIOS 11–12", "reproduzir, empacotar;\ndirigir agentes, liberar"),
        ],
        "rails_title": "Quatro trilhos cruzam todos os estúdios",
        "rails": [
            "Ética, permissões e exposição de dados",
            "Evidência, proveniência e reprodutibilidade",
            "Atividade de IA, verificação e decisões humanas",
            "Incerteza, fronteira da alegação e histórico de revisão",
        ],
    },
    "book-es": {
        "start": ("TU CURIOSIDAD", "una pregunta que\nno te deja\nen paz"),
        "end": ("TU DECISIÓN", "publicar, defendida,\no retener con honestidad;\nel próximo estudio abre"),
        "road": [
            ("ESTUDIO 1", "comenzar la investigación,\ngobernar el trabajo"),
            ("ESTUDIOS 2–4", "formular la pregunta,\nfundamentar, declarar"),
            ("ESTUDIOS 5–6", "desarrollar la ruta,\ngobernar los datos"),
            ("ESTUDIOS 7–8", "primer análisis,\nprueba de estrés"),
            ("ESTUDIOS 9–10", "escribir y delimitar,\nadaptar y defender"),
            ("ESTUDIOS 11–12", "reproducir, empaquetar;\ndirigir agentes, liberar"),
        ],
        "rails_title": "Cuatro rieles cruzan todos los estudios",
        "rails": [
            "Ética, permisos y exposición de datos",
            "Evidencia, procedencia y reproducibilidad",
            "Actividad de IA, verificación y decisiones humanas",
            "Incertidumbre, frontera de la afirmación y revisión",
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
    fig, ax = plt.subplots(figsize=(10.2, 4.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    road_y = .66
    # start capsule: the reader's curiosity
    box(ax, .072, road_y, .112, .30, "white", INK, lw=1.5, r=0.03)
    ax.text(.072, road_y + .085, strings["start"][0], ha="center",
            va="center", fontsize=8.0, fontweight="bold", color=INK)
    ax.text(.072, road_y - .05, strings["start"][1], ha="center",
            va="center", fontsize=7.0, color="#444440", linespacing=1.3)

    # the six road stages
    rxs = [.2017 + i * .1242 for i in range(6)]
    prev_right = .072 + .056
    for i, (rx, (head, sub)) in enumerate(zip(rxs, strings["road"])):
        box(ax, rx, road_y, .110, .26, FILL, SOFT, lw=1.0)
        ax.text(rx, road_y + .07, head, ha="center", va="center",
                fontsize=8.0, fontweight="bold", color=INK)
        ax.text(rx, road_y - .045, sub, ha="center", va="center",
                fontsize=6.8, color="#444440", linespacing=1.3)
        arrow(ax, prev_right, road_y, rx - .055, road_y)
        prev_right = rx + .055

    # end capsule: the released claim
    box(ax, .944, road_y, .100, .30, "white", INK, lw=1.5, r=0.03)
    ax.text(.944, road_y + .085, strings["end"][0], ha="center",
            va="center", fontsize=7.8, fontweight="bold", color=INK)
    ax.text(.944, road_y - .05, strings["end"][1], ha="center",
            va="center", fontsize=6.8, color="#444440", linespacing=1.3)
    arrow(ax, prev_right, road_y, .944 - .050, road_y)

    # the four rails, running under the whole road
    ax.text(.5, .40, strings["rails_title"], ha="center", va="center",
            fontsize=9.0, fontweight="bold", color=INK)
    rail_ys = [.325, .255, .185, .115]
    for ry, label in zip(rail_ys, strings["rails"]):
        ax.plot([.06, .96], [ry, ry], color=SOFT, lw=1.0, zorder=1)
        ax.text(.5, ry + .028, label, ha="center", va="center",
                fontsize=7.6, color="#444440",
                bbox=dict(facecolor="white", edgecolor="none", pad=1.2))

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
