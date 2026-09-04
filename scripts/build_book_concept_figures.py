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
            "rows": ("WHAT YOU WANT TO LEARN", "HOW YOU WILL LEARN IT"),
            "cells": [
                ("MODEL", "how the world\ncould work"),
                ("INQUIRY", "the one quantity\nyou want from it"),
                ("DATA STRATEGY", "every procedure that\nmakes the data:\nsampling, assignment,\nmeasurement"),
                ("ANSWER STRATEGY", "how those data\nbecome an answer,\nuncertainty included"),
            ],
            "top_link": "makes askable",
            "bottom_link": "feeds",
            "align": "alignment: does the answer\nreach the inquiry?",
            "foot": "Four parts, one question. All four are written before you collect anything; the design holds together when the bottom row actually reaches the top right.",
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
            "miss": "in your target, never on\nthe frame: undercoverage",
            "extra": "on the frame, outside your\ntarget: overcoverage",
            "dup": "one unit, listed twice:\na duplicate",
            "foot": "The frame is not a tidy slice of the population above it. That is where a description quietly goes wrong.",
        },
        "leadloop": {
            "span_lead": ("STILL A LEAD", "a candidate source you have not confirmed yet"),
            "span_source": ("NOW A SOURCE", "promoted by retrieval and verification"),
            "steps": [
                ("ASK", "any tool, to surface leads"),
                ("RETRIEVE", "the actual source, yourself"),
                ("VERIFY", "run both checks below"),
                ("DOCUMENT", "where you found it"),
            ],
            "checks_head": "TWO SEPARATE CHECKS",
            "checks": [
                ("does it exist?", "CITATION HALLUCINATION",
                 "an AI inventing a source\nthat does not exist"),
                ("does it say this?", "MISCHARACTERIZED SOURCE",
                 "a real paper cited for a\nclaim it never makes"),
            ],
            "fail": "no",
            "foot": "A lead stays a lead until retrieval and verification promote it to a source.",
        },
        "provenance": {
            "chain_head": "EVERY HAND IT PASSED THROUGH BEFORE IT REACHED YOU",
            "chain": [
                ("PRIMARY SOURCE", "the original record where\nthe value was first produced"),
                ("SECONDARY SOURCE", "re-reports a value\nit did not produce"),
                ("SECONDARY SOURCE", "and so does this one"),
                ("THE VALUE, IN YOUR FILE", "where you met it"),
            ],
            "back": "trace it back yourself, to the primary source",
            "asks_head": "TWO THINGS YOU MUST BE ABLE TO ANSWER",
            "asks": [
                ("PROVENANCE", "where did this value come from,\nand through whose hands?"),
                ("DATA QUALITY", "is it fit for MY question: real, by a method\nI can name, defined the way my question needs?"),
            ],
            "foot": "A value is only as trustworthy as the primary source at the end of its chain.",
        },
        "codeloop": {
            "own_before": "YOURS, BEFORE YOU DELEGATE — the quantity of interest and the frame, in plain words",
            "steps": ["PROMPT", "READ THE\nOUTPUT", "INTERROGATE IT", "REFINE", "RUN IT AGAIN"],
            "gate_head": "YOURS, EVERY CYCLE — NOT EVERY SESSION",
            "gate": "what quantity?    over which cases?",
            "drift": "Any turn can add a filter, drop a join, or reach for a different column.\nNothing announces the change.",
            "foot": "A clean run is not a correct result: a cell can execute with no error and still compute a different number than your question needs.",
        },
        "verbgate": {
            "head": "KEEP THESE THREE APART",
            "fields": [
                ("QUESTION KIND", "what you set out to learn.\nIts kind comes from its own words", "causal"),
                ("IDENTIFICATION STATUS", "whether THIS DESIGN can actually\ndeliver that answer", "not identified by this design\nunder stated assumptions"),
                ("RESULT", "the quantity this evidence\ndid produce", "observed association"),
            ],
            "boundary": ("CLAIM BOUNDARY", "what those three together license you to write"),
            "verb_head": "AND IT LIVES IN THE HEADLINE VERB",
            "verbs": [("you write", "\u201cwas associated with lower\u201d"),
                      ("never", "\u201clowered\u201d")],
            "foot": "What earns a causal verb is a defended identification argument.",
        },
        "capsule": {
            "head": "REPRODUCIBILITY CAPSULE",
            "sub": "everything a stranger needs to rebuild your numbers, and nothing they would have to guess",
            "parts": [
                ("RUNNABLE NOTEBOOK", "passes restart-\nand-run-all"),
                ("DATA-PROVENANCE NOTE", "where each dataset came\nfrom, its version, its use"),
                ("FIXED SEED", "every random step returns\nthe same values"),
                ("DECISION LOG", "the by-hand choices,\neach with its reason"),
                ("AI-USE LEDGER", "every tool, its task, and\nhow you verified it"),
            ],
            "sins_head": "THE FIVE PACKAGE SINS — HOW CAPSULES PREDICTABLY BREAK",
            "sins": "a hard-coded path that exists only on your machine   ·   a missing seed that moves every run   ·   a by-hand edit no clean run reproduces\nan undocumented exclusion with no logged reason   ·   stale data a reader cannot reobtain",
            "foot": "A capsule with zero flags is runnable, never proven correct.",
        },
        "uln": {
            "head": "THE ULN MOVE — THREE BEATS, IN THIS ORDER",
            "beats": [
                ("UNCERTAINTY", "how much your number\ncould wobble, and why",
                 "\u201cwith 812 people, my estimate could\nsit a few points higher or lower\u201d"),
                ("LIMITATION", "a true sentence about what\nyour design cannot show",
                 "\u201cI measured that two things went together,\nso I cannot say one caused the other\u201d"),
                ("NEXT STEP", "the study that would\nresolve that limitation",
                 "the design that would settle it"),
            ],
            "prevents_head": "AND THE FAILURE IT PREVENTS",
            "prevents": ("THE APOLOGY SPIRAL",
                         "burying a real, defensible finding under self-erasure"),
            "choose": [("PRECISION — naming the exact boundary", "\u201cthis is one campus sample\u201d"),
                       ("HEDGING — vague self-protection", "\u201csort of, take it with a grain of salt\u201d")],
            "choose_note": "Precision informs the listener; hedging only protects you.",
            "foot": "Delivered together, ULN sounds like expertise, because you are naming the edge of your evidence on purpose.",
        },
        "criticalpath": {
            "head_par": "NO DEPENDENCY BETWEEN THEM",
            "sub_par": "they run at the same time",
            "par": ["check the design", "check the citations", "tighten the prose"],
            "head_seq": "JOINED BY ONE DEPENDENCY EACH",
            "sub_seq": "they run in order — and this chain is THE CRITICAL PATH",
            "seq": [("WORKER", "drafts"), ("CRITIC", "attacks what\nthe worker produced"), ("YOU", "integrate")],
            "seq_note": "three steps that cannot collapse into fewer",
            "foot": "You orchestrate loops, not prompts.",
        },
        "compass": {
            "axis_kind": ("KIND", "what kind of answer the question wants"),
            "axis_reach": ("REACH", "for which units the answer must hold"),
            "reach": [
                ("DATA AT HAND", "only the units you observed"),
                ("A POPULATION", "a larger group you sample from"),
                ("UNSEEN CASES", "units you have not seen yet"),
            ],
            "kinds": [
                ("DESCRIPTIVE", "what the world is or\nwas — you look and\nrecord"),
                ("CAUSAL", "what would change if\nsomeone intervened"),
            ],
            "cells": [
                ("DESCRIPTION", "what the units you\nactually observed show",
                 "earned by: honest measurement"),
                ("GENERALIZATION", "what the wider group shows,\nbeyond the units you saw",
                 "earned by: a sampling design"),
                ("PREDICTION", "what a case you have not seen\nwill show — a forecast, not a reason",
                 "earned by: a held-out check"),
            ],
            "causal_head": "CAUSAL REASONING",
            "causal_sub": "one kind, asked at three reaches — the only row that earns the word “because”",
            "causal_cells": [
                "the effect for the units\nyou actually studied",
                "the effect for the population\nyour sample stands in for",
                "the effect carried into a\nnew setting or a later time",
            ],
            "causal_earned": "earned by: a credible stand-in for the world that did not happen — the same price at all three reaches",
            "forbidden": "if your design cannot isolate the answer, write\n“causal, currently unidentified” — never descriptive.\nWeak evidence never moves a question up a row.",
            "foot": "Two questions place any question on this map: what kind of answer it wants, and for which units that answer must hold.",
        },
        "declaration": {
            "title": "THE DECLARATION",
            "title_sub": "two parts, and neither substitutes for the other — the project's contract with the evidence",
            "parts": [
                ("1 · THE LEAD QUESTION",
                 "the single sentence your evidence will answer — classified by kind and reach in the last lesson"),
                ("2 · THE FIELD CARD",
                 "the short record that pins down every term the sentence carries"),
            ],
            "boundary_head": "THE PROVISIONAL CLAIM BOUNDARY",
            "boundary_sub": "a pair, and the card carries it too — written now, before any results exist",
            "fields": [
                ("OBJECTIVE", "what the study intends to\ndescribe, predict, or explain"),
                ("UNIT OF ANALYSIS", "the kind of entity the\nanswer makes a claim about"),
                ("OUTCOME", "what you will\nactually record"),
                ("CONDITIONS", "the comparison, setting, or time\nthat gives the outcome meaning"),
                ("KIND", "descriptive or causal,\nstraight from the compass"),
                ("REACH", "for which units the\nanswer must hold"),
            ],
            "boundary": [
                ("HOPE TO DEFEND", "the sentence you\nhope to defend"),
                ("WILL NOT BE ABLE TO DEFEND", "the stronger sentence you already\nknow you will not be able to"),
            ],
            "band": "Yours, never delegated: the choice among candidate wordings  ·  the kind  ·  the reach  ·  both boundary sentences",
            "foot": "A boundary written early is a promise; a boundary written late is an excuse.",
        },
    },
    "book-pt": {
        "mida": {
            "rows": ("O QUE VOCÊ QUER SABER", "COMO VOCÊ VAI DESCOBRIR"),
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
            "miss": "no seu alvo, nunca no\ncadastro: subcobertura",
            "extra": "no cadastro, fora do seu\nalvo: sobrecobertura",
            "dup": "uma unidade, listada duas\nvezes: uma duplicata",
            "foot": "O cadastro não é uma fatia limpa da população acima dele. É aí que uma descrição erra em silêncio.",
        },
        "compass": {
            "axis_kind": ("TIPO", "que tipo de resposta a pergunta quer"),
            "axis_reach": ("ALCANCE", "para quais unidades a resposta precisa valer"),
            "reach": [
                ("DADOS EM MÃOS", "só as unidades que você observou"),
                ("UMA POPULAÇÃO", "um grupo maior de onde você amostra"),
                ("CASOS NÃO VISTOS", "unidades que você ainda não viu"),
            ],
            "kinds": [
                ("DESCRITIVO", "como o mundo é ou\nfoi — você olha e\nregistra"),
                ("CAUSAL", "o que mudaria se\nalguém interviesse"),
            ],
            "cells": [
                ("DESCRIÇÃO", "o que mostram as unidades\nque você de fato observou",
                 "garantido por: medição honesta"),
                ("GENERALIZAÇÃO", "o que mostra o grupo maior,\nalém das unidades que você viu",
                 "garantido por: um desenho amostral"),
                ("PREVISÃO", "o que mostrará um caso que você não viu\n— uma previsão, não uma razão",
                 "garantido por: um teste fora da amostra"),
            ],
            "causal_head": "RACIOCÍNIO CAUSAL",
            "causal_sub": "um tipo, perguntado em três alcances — a única linha que merece a palavra “porque”",
            "causal_cells": [
                "o efeito para as unidades\nque você de fato estudou",
                "o efeito para a população\nque sua amostra representa",
                "o efeito levado a um novo\ncenário ou a um tempo depois",
            ],
            "causal_earned": "garantido por: um substituto crível para o mundo que não aconteceu — o mesmo preço nos três alcances",
            "forbidden": "se seu desenho não consegue isolar a resposta, escreva\n“causal, atualmente não identificada” — nunca descritiva.\nEvidência fraca nunca move uma pergunta de linha.",
            "foot": "Duas perguntas situam qualquer pergunta neste mapa: que tipo de resposta ela quer e para quais unidades essa resposta precisa valer.",
        },
        "declaration": {
            "title": "A DECLARAÇÃO",
            "title_sub": "duas partes, e nenhuma substitui a outra — o contrato do projeto com a evidência",
            "parts": [
                ("1 · A PERGUNTA PRINCIPAL",
                 "a única frase que sua evidência vai responder — classificada por tipo e alcance na lição anterior"),
                ("2 · A FICHA DE CAMPO",
                 "o registro curto que fixa cada termo que a frase carrega"),
            ],
            "boundary_head": "A FRONTEIRA PROVISÓRIA DA ALEGAÇÃO",
            "boundary_sub": "um par, e a ficha também o carrega — escrito agora, antes de qualquer resultado",
            "fields": [
                ("OBJETIVO", "o que o estudo pretende\ndescrever, prever ou explicar"),
                ("UNIDADE DE ANÁLISE", "o tipo de entidade sobre a qual\na resposta faz uma alegação"),
                ("DESFECHO", "o que você vai\nde fato registrar"),
                ("CONDIÇÕES", "a comparação, o cenário ou o tempo\nque dá sentido ao desfecho"),
                ("TIPO", "descritiva ou causal,\ndireto da bússola"),
                ("ALCANCE", "para quais unidades a\nresposta precisa valer"),
            ],
            "boundary": [
                ("ESPERA DEFENDER", "a frase que você\nespera defender"),
                ("NÃO VAI CONSEGUIR DEFENDER", "a frase mais forte que você já\nsabe que não vai conseguir"),
            ],
            "band": "Seu, nunca delegado: a escolha entre as redações candidatas  ·  o tipo  ·  o alcance  ·  as duas frases da fronteira",
            "foot": "Uma fronteira escrita cedo é uma promessa; uma fronteira escrita tarde é uma desculpa.",
        },
    },
    "book-es": {
        "mida": {
            "rows": ("QUÉ QUIERES APRENDER", "CÓMO LO VAS A APRENDER"),
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
            "miss": "en tu objetivo, nunca en el\nmarco: subcobertura",
            "extra": "en el marco, fuera de tu\nobjetivo: sobrecobertura",
            "dup": "una unidad, listada dos\nveces: un duplicado",
            "foot": "El marco no es una rebanada limpia de la población de arriba. Ahí es donde una descripción falla en silencio.",
        },
        "compass": {
            "axis_kind": ("TIPO", "qué tipo de respuesta quiere la pregunta"),
            "axis_reach": ("ALCANCE", "para qué unidades debe valer la respuesta"),
            "reach": [
                ("DATOS A LA MANO", "solo las unidades que observaste"),
                ("UNA POBLACIÓN", "un grupo mayor del que muestreas"),
                ("CASOS NO VISTOS", "unidades que aún no has visto"),
            ],
            "kinds": [
                ("DESCRIPTIVO", "cómo es o fue el\nmundo — miras y\nregistras"),
                ("CAUSAL", "qué cambiaría si\nalguien interviniera"),
            ],
            "cells": [
                ("DESCRIPCIÓN", "lo que muestran las unidades\nque de hecho observaste",
                 "se gana con: medición honesta"),
                ("GENERALIZACIÓN", "lo que muestra el grupo mayor,\nmás allá de las unidades que viste",
                 "se gana con: un diseño muestral"),
                ("PREDICCIÓN", "lo que mostrará un caso que no has visto\n— un pronóstico, no una razón",
                 "se gana con: una prueba fuera de muestra"),
            ],
            "causal_head": "RAZONAMIENTO CAUSAL",
            "causal_sub": "un tipo, preguntado en tres alcances — la única fila que merece la palabra “porque”",
            "causal_cells": [
                "el efecto para las unidades\nque de hecho estudiaste",
                "el efecto para la población\nque tu muestra representa",
                "el efecto llevado a un nuevo\nentorno o a un tiempo posterior",
            ],
            "causal_earned": "se gana con: un sustituto creíble del mundo que no ocurrió — el mismo precio en los tres alcances",
            "forbidden": "si tu diseño no puede aislar la respuesta, escribe\n“causal, actualmente no identificada” — nunca descriptiva.\nLa evidencia débil nunca cambia una pregunta de fila.",
            "foot": "Dos preguntas ubican cualquier pregunta en este mapa: qué tipo de respuesta quiere y para qué unidades debe valer esa respuesta.",
        },
        "declaration": {
            "title": "LA DECLARACIÓN",
            "title_sub": "dos partes, y ninguna sustituye a la otra — el contrato del proyecto con la evidencia",
            "parts": [
                ("1 · LA PREGUNTA PRINCIPAL",
                 "la única frase que tu evidencia va a responder — clasificada por tipo y alcance en la lección anterior"),
                ("2 · LA FICHA DE CAMPO",
                 "el registro breve que fija cada término que la frase lleva"),
            ],
            "boundary_head": "LA FRONTERA PROVISIONAL DE LA AFIRMACIÓN",
            "boundary_sub": "un par, y la ficha también lo lleva — escrito ahora, antes de cualquier resultado",
            "fields": [
                ("OBJETIVO", "qué pretende el estudio\ndescribir, predecir o explicar"),
                ("UNIDAD DE ANÁLISIS", "el tipo de entidad sobre la que\nla respuesta afirma algo"),
                ("RESULTADO", "lo que vas a\nregistrar de hecho"),
                ("CONDICIONES", "la comparación, el entorno o el tiempo\nque da sentido al resultado"),
                ("TIPO", "descriptiva o causal,\ndirecto de la brújula"),
                ("ALCANCE", "para qué unidades debe\nvaler la respuesta"),
            ],
            "boundary": [
                ("ESPERA DEFENDER", "la frase que\nesperas defender"),
                ("NO VA A PODER DEFENDER", "la frase más fuerte que ya\nsabes que no vas a poder"),
            ],
            "band": "Tuyo, nunca delegado: la elección entre las redacciones candidatas  ·  el tipo  ·  el alcance  ·  las dos frases de la frontera",
            "foot": "Una frontera escrita temprano es una promesa; una frontera escrita tarde es una excusa.",
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

    # the target population, and inside it the part you could actually reach
    region(.07, .70, .30, .94, "white", INK, 1.5)
    ax.text(.093, .897, S["target"], ha="left", va="center", fontsize=8.2,
            fontweight="bold", color=INK, zorder=5)
    ax.text(.093, .864, S["target_sub"], ha="left", va="center", fontsize=6.6,
            color=MUTE, zorder=5)

    region(.11, .55, .355, .825, FILL, SOFT, 1.1)
    ax.text(.132, .787, S["accessible"], ha="left", va="center", fontsize=7.6,
            fontweight="bold", color=INK, zorder=5)
    ax.text(.132, .756, S["accessible_sub"], ha="left", va="center",
            fontsize=6.4, color=MUTE, zorder=5)

    # the frame CROSSES the target's boundary: part of what it lists is
    # out of scope entirely, which is what overcoverage means
    region(.37, .93, .40, .70, "none", INK, 1.4, ls="dashed", z=3)
    ax.text(.915, .663, S["frame"], ha="right", va="center", fontsize=7.6,
            fontweight="bold", color=INK, zorder=5)
    ax.text(.915, .632, S["frame_sub"], ha="right", va="center", fontsize=6.4,
            color=MUTE, zorder=5)

    region(.41, .525, .45, .58, INK, INK, 1.0, z=4)
    ax.text(.4675, .515, S["sample"], ha="center", va="center", fontsize=7.4,
            fontweight="bold", color="white", zorder=6)

    # a duplicate is two records for one unit, not an area
    ax.plot([.610, .642], [.545, .545], color=INK, lw=.9, marker="o",
            markersize=7, markerfacecolor=INK, markeredgecolor=INK, zorder=5)
    ax.annotate(S["dup"], xy=(.626, .528), xytext=(.626, .175),
                ha="center", va="center", fontsize=6.8, color=INK,
                linespacing=1.35, zorder=6,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0,
                                mutation_scale=10))

    # the two coverage errors, each pointing at the region that creates it
    ax.annotate(S["miss"], xy=(.185, .47), xytext=(.165, .175),
                ha="center", va="center", fontsize=6.8, color=INK,
                linespacing=1.35, zorder=6,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0,
                                mutation_scale=10))
    ax.annotate(S["extra"], xy=(.845, .47), xytext=(.868, .175),
                ha="center", va="center", fontsize=6.8, color=INK,
                linespacing=1.35, zorder=6,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.0,
                                mutation_scale=10))

    ax.text(.5, .045, S["foot"], ha="center", va="center", fontsize=7.2,
            color=MUTE)

    fig.tight_layout(pad=0.4)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_compass(S: dict, out: Path) -> None:
    """The inquiry compass: kind × reach, the price of each step, and the
    one move the compass forbids.

    Two conventions carry the meaning. Filled boxes are what you classify
    ON — the two kinds and the three reaches. White boxes are the position
    you LAND IN. And the causal row is drawn as ONE band across all three
    reaches, because it is one question kind asked of three unit sets, not
    three new positions.
    """
    fig, ax = plt.subplots(figsize=(10.0, 5.85))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    cxs = (.315, .580, .845)
    cw, grid_l, grid_r = .240, .195, .965
    stub_x, stub_w = .105, .140
    head_y, head_h = .855, .100
    desc_y, desc_h = .660, .205
    caus_y, caus_h = .290, .250
    desc_bot = desc_y - desc_h / 2
    caus_top, caus_bot = caus_y + caus_h / 2, caus_y - caus_h / 2

    def axis_title(cx, pair):
        name, gloss = pair
        ax.text(cx, .966, name, ha="center", va="center",
                fontsize=8.0, fontweight="bold", color=INK)
        ax.text(cx, .936, gloss, ha="center", va="center",
                fontsize=6.6, color=MUTE)

    axis_title(stub_x, S["axis_kind"])
    axis_title((grid_l + grid_r) / 2, S["axis_reach"])

    # reach across the top — filled, because it is an input you classify on
    for cx, (head, sub) in zip(cxs, S["reach"]):
        box(ax, cx, head_y, cw, head_h, FILL, SOFT, lw=1.0, r=.024)
        ax.text(cx, head_y + .020, head, ha="center", va="center",
                fontsize=8.2, fontweight="bold", color=INK)
        ax.text(cx, head_y - .022, sub, ha="center", va="center",
                fontsize=6.6, color=MUTE)

    # kind down the left — filled for the same reason
    for cy, ch, (head, sub) in zip((desc_y, caus_y), (desc_h, caus_h),
                                   S["kinds"]):
        box(ax, stub_x, cy, stub_w, ch, FILL, SOFT, lw=1.0, r=.024)
        ax.text(stub_x, cy + .048, head, ha="center", va="center",
                fontsize=8.2, fontweight="bold", color=INK)
        ax.text(stub_x, cy - .022, sub, ha="center", va="center",
                fontsize=6.5, color=MUTE, linespacing=1.45)

    # the descriptive row: three named positions, each naming what buys it
    for cx, (head, sub, earned) in zip(cxs, S["cells"]):
        box(ax, cx, desc_y, cw, desc_h, "white", INK, lw=1.4, r=.026)
        ax.text(cx, desc_y + .062, head, ha="center", va="center",
                fontsize=8.4, fontweight="bold", color=INK)
        ax.text(cx, desc_y - .008, sub, ha="center", va="center",
                fontsize=6.8, color=MUTE, linespacing=1.35)
        ax.text(cx, desc_y - .074, earned, ha="center", va="center",
                fontsize=6.4, color=INK, style="italic")

    # the causal row: one kind, drawn across all three reaches
    box(ax, (grid_l + grid_r) / 2, caus_y, grid_r - grid_l, caus_h,
        "white", INK, lw=1.4, r=.026)
    ax.text((grid_l + grid_r) / 2, caus_top - .034, S["causal_head"],
            ha="center", va="center", fontsize=8.4, fontweight="bold",
            color=INK)
    ax.text((grid_l + grid_r) / 2, caus_top - .066, S["causal_sub"],
            ha="center", va="center", fontsize=6.8, color=MUTE)
    ax.plot([grid_l + .016, grid_r - .016], [caus_top - .089, caus_top - .089],
            color=SOFT, lw=.8, zorder=3)
    for bx in ((cxs[0] + cxs[1]) / 2, (cxs[1] + cxs[2]) / 2):
        ax.plot([bx, bx], [caus_bot + .038, caus_top - .095],
                color=SOFT, lw=.8, zorder=3)
    for cx, seg in zip(cxs, S["causal_cells"]):
        ax.text(cx, caus_y - .018, seg, ha="center", va="center",
                fontsize=6.9, color=INK, linespacing=1.35)
    ax.text((grid_l + grid_r) / 2, caus_bot + .026, S["causal_earned"],
            ha="center", va="center", fontsize=6.4, color=INK, style="italic")

    # the move the compass forbids, struck out where it would be made
    fx = cxs[0]
    my = (caus_top + desc_bot) / 2
    arrow(ax, fx, caus_top + .008, fx, desc_bot - .008, ls="dashed")
    ax.add_patch(FancyBboxPatch(
        (fx - .018, my - .020), .036, .040,
        boxstyle="round,pad=0,rounding_size=.004",
        facecolor="white", edgecolor="none", zorder=5))
    for dy in (1, -1):
        ax.plot([fx - .011, fx + .011], [my - .015 * dy, my + .015 * dy],
                color=INK, lw=1.5, zorder=6, solid_capstyle="round")
    ax.text(.680, my, S["forbidden"], ha="center", va="center",
            fontsize=6.8, color=INK, linespacing=1.45)

    ax.text(.5, .088, S["foot"], ha="center", va="center", fontsize=7.2,
            color=MUTE)

    fig.tight_layout(pad=0.4)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_declaration(S: dict, out: Path) -> None:
    """The declaration's anatomy: TWO parts, and the boundary lives inside
    the second one.

    The chapter is explicit that a declaration has two parts and that the
    field card is what "names" the objective, the unit, the outcome, the
    conditions, the kind, the reach AND the provisional claim boundary. So
    the boundary is drawn nested inside the card, not standing beside it,
    and it is drawn as a PAIR. The band beneath is the human line: what
    none of this delegates.
    """
    fig, ax = plt.subplots(figsize=(10.0, 6.1))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    ax.text(.5, .965, S["title"], ha="center", va="center",
            fontsize=9.0, fontweight="bold", color=INK)
    ax.text(.5, .936, S["title_sub"], ha="center", va="center",
            fontsize=6.8, color=MUTE)

    # 1 — the sentence itself
    q_head, q_sub = S["parts"][0]
    box(ax, .5, .872, .790, .076, "white", INK, lw=1.4, r=.020)
    ax.text(.5, .891, q_head, ha="center", va="center",
            fontsize=7.8, fontweight="bold", color=INK)
    ax.text(.5, .855, q_sub, ha="center", va="center",
            fontsize=6.6, color=MUTE)
    arrow(ax, .5, .832, .5, .802)

    # 2 — the card that pins every term the sentence carries
    c_head, c_sub = S["parts"][1]
    box(ax, .5, .482, .910, .630, FILL, SOFT, lw=1.1, r=.020)
    ax.text(.5, .766, c_head, ha="center", va="center",
            fontsize=8.0, fontweight="bold", color=INK)
    ax.text(.5, .739, c_sub, ha="center", va="center",
            fontsize=6.6, color=MUTE)
    ax.plot([.075, .925], [.717, .717], color=SOFT, lw=.8, zorder=3)

    fxs, fw = (.215, .500, .785), .255
    for i, (head, sub) in enumerate(S["fields"]):
        cx, cy = fxs[i % 3], (.648 if i < 3 else .528)
        box(ax, cx, cy, fw, .100, "white", INK, lw=1.1, r=.018)
        ax.text(cx, cy + .024, head, ha="center", va="center",
                fontsize=7.2, fontweight="bold", color=INK)
        ax.text(cx, cy - .022, sub, ha="center", va="center",
                fontsize=6.2, color=MUTE, linespacing=1.35)

    # the boundary — inside the card, and a pair
    box(ax, .5, .312, .850, .200, "white", INK, lw=1.3, r=.020)
    ax.text(.5, .385, S["boundary_head"], ha="center", va="center",
            fontsize=7.8, fontweight="bold", color=INK)
    ax.text(.5, .359, S["boundary_sub"], ha="center", va="center",
            fontsize=6.4, color=MUTE)
    ax.plot([.100, .900], [.338, .338], color=SOFT, lw=.8, zorder=3)
    ax.plot([.5, .5], [.228, .331], color=SOFT, lw=.8, zorder=3)
    for cx, (head, sub) in zip((.290, .710), S["boundary"]):
        ax.text(cx, .305, head, ha="center", va="center",
                fontsize=7.2, fontweight="bold", color=INK)
        ax.text(cx, .258, sub, ha="center", va="center",
                fontsize=6.3, color=MUTE, linespacing=1.35)

    # the human line
    box(ax, .5, .100, .910, .054, "white", INK, lw=1.1, r=.018)
    ax.text(.5, .100, S["band"], ha="center", va="center",
            fontsize=7.0, color=INK)

    ax.text(.5, .032, S["foot"], ha="center", va="center", fontsize=7.2,
            color=MUTE, style="italic")

    fig.tight_layout(pad=0.4)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_leadloop(S: dict, out: Path) -> None:
    """The four steps, and the point on them where a lead becomes a source.

    The promotion happens at VERIFICATION, not at the end of the chain: "a
    lead stays a lead until retrieval and verification promote it to a
    source", and documenting comes after. So lead and source are drawn as two
    SPANS over the row, divided between VERIFY and DOCUMENT, rather than as a
    start box and an end box — which would have said, wrongly, that a source
    is what you have only once you have written down where you found it.
    """
    fig, ax = plt.subplots(figsize=(9.6, 4.9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    y, w, gap, x0 = 0.700, 0.210, 0.020, 0.050
    cxs = [x0 + w / 2 + i * (w + gap) for i in range(4)]
    split = (cxs[2] + w / 2 + cxs[3] - w / 2) / 2

    def span(xa, xb, head, sub):
        yb = 0.855
        ax.plot([xa, xb], [yb, yb], color=SOFT, lw=1.0)
        for x in (xa, xb):
            ax.plot([x, x], [yb, yb - 0.028], color=SOFT, lw=1.0)
        ax.text((xa + xb) / 2, yb + 0.075, head, ha="center", va="center",
                fontsize=7.4, color=INK, fontweight="bold")
        ax.text((xa + xb) / 2, yb + 0.028, sub, ha="center", va="center",
                fontsize=6.4, color=MUTE)

    span(x0, split - 0.008, *S["span_lead"])
    span(split + 0.008, x0 + 4 * w + 3 * gap, *S["span_source"])

    for i, (cx, (head, sub)) in enumerate(zip(cxs, S["steps"])):
        box(ax, cx, y, w, 0.155, "white", INK)
        ax.text(cx, y + 0.030, head, ha="center", va="center",
                fontsize=8.0, color=INK, fontweight="bold")
        ax.text(cx, y - 0.036, sub, ha="center", va="center",
                fontsize=6.4, color=MUTE, linespacing=1.5)
        if i:
            arrow(ax, cx - w / 2 - gap, y, cx - w / 2, y)

    vx = cxs[2]
    ax.plot([vx, vx], [y - 0.078, 0.545], color=INK, lw=1.1,
            solid_capstyle="butt", zorder=3)
    ax.text(vx, 0.478, S["checks_head"], ha="center", va="center",
            fontsize=6.4, color=SOFT, fontweight="bold")
    for cx, (q, name, sub) in zip((vx - 0.20, vx + 0.20), S["checks"]):
        arrow(ax, vx, 0.545, cx, 0.415)
        box(ax, cx, 0.368, 0.235, 0.090, "white", SOFT, ls="dashed")
        ax.text(cx, 0.368, q, ha="center", va="center",
                fontsize=7.4, color=INK, style="italic")
        arrow(ax, cx, 0.322, cx, 0.243, color=SOFT)
        ax.text(cx + 0.016, 0.283, S["fail"], ha="left", va="center",
                fontsize=6.2, color=SOFT, style="italic")
        box(ax, cx, 0.160, 0.265, 0.148, FILL, SOFT)
        ax.text(cx, 0.195, name, ha="center", va="center",
                fontsize=7.2, color=INK, fontweight="bold")
        ax.text(cx, 0.128, sub, ha="center", va="center",
                fontsize=6.3, color=MUTE, linespacing=1.5)

    ax.text(0.5, 0.040, S["foot"], ha="center", va="center",
            fontsize=6.6, color=MUTE, style="italic")

    fig.subplots_adjust(left=0.012, right=0.988, top=0.985, bottom=0.015)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_provenance(S: dict, out: Path) -> None:
    """The chain a value travelled, and the two questions you owe it.

    The chapter defines provenance as the origin "and every hand it passed
    through before it reached you", so the chain runs origin-to-you and the
    trace runs back the other way. Only the primary source carries the heavy
    rule: "a value is only as trustworthy as the primary source at the end of
    its chain."
    """
    fig, ax = plt.subplots(figsize=(9.6, 4.8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    y, w, gap = 0.775, 0.200, 0.045
    x0 = 0.032
    cxs = [x0 + w / 2 + i * (w + gap) for i in range(4)]

    ax.text(0.5, 0.955, S["chain_head"], ha="center", va="center",
            fontsize=6.6, color=SOFT, fontweight="bold")

    for i, (cx, (head, sub)) in enumerate(zip(cxs, S["chain"])):
        primary = i == 0
        box(ax, cx, y, w, 0.165, "white" if primary else FILL,
            INK if primary else SOFT, lw=2.0 if primary else 1.1)
        ax.text(cx, y + 0.033, head, ha="center", va="center",
                fontsize=7.6 if primary else 7.2, color=INK, fontweight="bold")
        ax.text(cx, y - 0.038, sub, ha="center", va="center",
                fontsize=6.3, color=MUTE, linespacing=1.5)
        if i:
            arrow(ax, cx - w / 2 - gap, y, cx - w / 2, y, color=SOFT)

    # the trace back, under the chain
    ax.annotate("", xy=(cxs[0], 0.632), xytext=(cxs[-1], 0.632), zorder=4,
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=12,
                                connectionstyle="arc3,rad=-0.14"))
    ax.text(0.5, 0.487, S["back"], ha="center", va="center",
            fontsize=7.2, color=INK, style="italic")

    ax.text(0.5, 0.385, S["asks_head"], ha="center", va="center",
            fontsize=6.6, color=SOFT, fontweight="bold")
    for cx, (head, sub) in zip((0.275, 0.725), S["asks"]):
        box(ax, cx, 0.235, 0.43, 0.185, "white", INK)
        ax.text(cx, 0.283, head, ha="center", va="center",
                fontsize=7.6, color=INK, fontweight="bold")
        ax.text(cx, 0.205, sub, ha="center", va="center",
                fontsize=6.4, color=MUTE, linespacing=1.55)

    ax.text(0.5, 0.055, S["foot"], ha="center", va="center",
            fontsize=6.6, color=MUTE, style="italic")

    fig.subplots_adjust(left=0.012, right=0.988, top=0.985, bottom=0.015)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_codeloop(S: dict, out: Path) -> None:
    """The AI coding loop, and the check that has to close it every time.

    The chapter's loop is "you prompt, you read the output, you interrogate
    it, you refine, and you run it again", so running again returns to
    reading, not to prompting: the feedback arc lands on READ THE OUTPUT.
    The two boxes in ink are the two things the chapter says you own — the
    definition before you delegate, and the per-cycle confirmation.
    """
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    # what you own before any of it runs
    box(ax, 0.5, 0.925, 0.96, 0.10, "white", INK)
    ax.text(0.5, 0.925, S["own_before"], ha="center", va="center",
            fontsize=7.2, color=INK)

    y, w, gap = 0.735, 0.163, 0.030
    x0 = 0.032
    cxs = [x0 + w / 2 + i * (w + gap) for i in range(5)]
    for i, (cx, label) in enumerate(zip(cxs, S["steps"])):
        box(ax, cx, y, w, 0.115, FILL, SOFT)
        ax.text(cx, y, label, ha="center", va="center",
                fontsize=7.4, color=INK, fontweight="bold", linespacing=1.5)
        if i:
            arrow(ax, cx - w / 2 - gap, y, cx - w / 2, y, color=SOFT)
    arrow(ax, cxs[0], 0.875, cxs[0], y + 0.058, color=SOFT)

    # "and you run it again" returns to reading the output — and the return
    # path runs THROUGH the check, because that is the chapter's point: the
    # cycle does not close until you have asked both questions again.
    gx, gy, gw = (cxs[1] + cxs[4]) / 2, 0.495, 0.44
    ax.plot([cxs[4], cxs[4]], [y - 0.058, gy], color=INK, lw=1.2, zorder=3)
    arrow(ax, cxs[4], gy, gx + gw / 2, gy)
    ax.plot([gx - gw / 2, cxs[1]], [gy, gy], color=INK, lw=1.2, zorder=3)
    arrow(ax, cxs[1], gy, cxs[1], y - 0.058)

    ax.text(gx, 0.612, S["gate_head"], ha="center", va="center",
            fontsize=6.6, color=SOFT, fontweight="bold")
    box(ax, gx, gy, gw, 0.105, "white", INK, lw=2.0)
    ax.text(gx, gy, S["gate"], ha="center", va="center",
            fontsize=8.2, color=INK, fontweight="bold")

    ax.text(0.5, 0.265, S["drift"], ha="center", va="center",
            fontsize=6.9, color=MUTE, linespacing=1.6)
    ax.text(0.5, 0.075, S["foot"], ha="center", va="center",
            fontsize=6.6, color=MUTE, style="italic")

    fig.subplots_adjust(left=0.012, right=0.988, top=0.985, bottom=0.015)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_verbgate(S: dict, out: Path) -> None:
    """Three fields kept apart, and the verb they license between them.

    The chapter is emphatic that the kind belongs to the QUESTION and the
    status belongs to the DESIGN, and that fusing them "quietly fuses the two
    fields you just separated" — so the three sit as three separate boxes and
    only the boundary below them is joint. The two verbs are the chapter's
    own example, in its own words: you write one, never the other.
    """
    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    ax.text(0.5, 0.955, S["head"], ha="center", va="center",
            fontsize=6.6, color=SOFT, fontweight="bold")

    y, w, gap = 0.775, 0.30, 0.035
    x0 = 0.025
    cxs = [x0 + w / 2 + i * (w + gap) for i in range(3)]
    for cx, (head, sub, value) in zip(cxs, S["fields"]):
        box(ax, cx, y, w, 0.235, "white", INK)
        ax.text(cx, y + 0.078, head, ha="center", va="center",
                fontsize=7.6, color=INK, fontweight="bold")
        ax.text(cx, y + 0.016, sub, ha="center", va="center",
                fontsize=6.3, color=MUTE, linespacing=1.5)
        ax.plot([cx - w / 2 + 0.03, cx + w / 2 - 0.03], [y - 0.038, y - 0.038],
                color=SOFT, lw=0.8)
        ax.text(cx, y - 0.078, value, ha="center", va="center",
                fontsize=6.8, color=INK, style="italic", linespacing=1.5)
        arrow(ax, cx, y - 0.1175, 0.5, 0.545, color=SOFT)

    box(ax, 0.5, 0.475, 0.62, 0.125, FILL, INK, lw=2.0)
    ax.text(0.5, 0.505, S["boundary"][0], ha="center", va="center",
            fontsize=8.0, color=INK, fontweight="bold")
    ax.text(0.5, 0.448, S["boundary"][1], ha="center", va="center",
            fontsize=6.5, color=MUTE)

    ax.text(0.5, 0.355, S["verb_head"], ha="center", va="center",
            fontsize=6.6, color=SOFT, fontweight="bold")
    for cx, (lead, verb) in zip((0.275, 0.725), S["verbs"]):
        ax.text(cx, 0.268, lead, ha="center", va="center",
                fontsize=6.8, color=SOFT, style="italic")
        ax.text(cx, 0.205, verb, ha="center", va="center",
                fontsize=9.4, color=INK, fontweight="bold")
    ax.plot([0.663, 0.787], [0.203, 0.203], color=INK, lw=1.0)

    ax.text(0.5, 0.065, S["foot"], ha="center", va="center",
            fontsize=6.6, color=MUTE, style="italic")

    fig.subplots_adjust(left=0.012, right=0.988, top=0.985, bottom=0.015)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_capsule(S: dict, out: Path) -> None:
    """The capsule's five parts, and the five ways capsules break.

    The chapter names five parts and, separately, five sins. It does NOT pair
    them one to one, so the sins run as a single band rather than as five
    boxes under five boxes, which would assert a mapping the prose does not
    make.
    """
    fig, ax = plt.subplots(figsize=(9.6, 4.8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    box(ax, 0.5, 0.715, 0.955, 0.50, FILL, INK, lw=1.6)
    ax.text(0.5, 0.918, S["head"], ha="center", va="center",
            fontsize=8.6, color=INK, fontweight="bold")
    ax.text(0.5, 0.862, S["sub"], ha="center", va="center",
            fontsize=6.6, color=MUTE, style="italic")

    w, gap = 0.174, 0.016
    x0 = 0.038
    for i, (head, sub) in enumerate(S["parts"]):
        cx = x0 + w / 2 + i * (w + gap)
        box(ax, cx, 0.665, w, 0.215, "white", SOFT)
        ax.text(cx, 0.715, head, ha="center", va="center",
                fontsize=6.6, color=INK, fontweight="bold")
        ax.text(cx, 0.645, sub, ha="center", va="center",
                fontsize=6.1, color=MUTE, linespacing=1.5)

    ax.text(0.5, 0.375, S["sins_head"], ha="center", va="center",
            fontsize=6.6, color=SOFT, fontweight="bold")
    ax.plot([0.19, 0.81], [0.335, 0.335], color=SOFT, lw=0.8)
    ax.text(0.5, 0.245, S["sins"], ha="center", va="center",
            fontsize=6.5, color=MUTE, linespacing=1.9)

    ax.text(0.5, 0.075, S["foot"], ha="center", va="center",
            fontsize=7.0, color=INK, style="italic")

    fig.subplots_adjust(left=0.012, right=0.988, top=0.985, bottom=0.015)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_uln(S: dict, out: Path) -> None:
    """The three beats of the ULN move, and the spiral it replaces."""
    fig, ax = plt.subplots(figsize=(9.6, 5.0))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    ax.text(0.5, 0.955, S["head"], ha="center", va="center",
            fontsize=6.6, color=SOFT, fontweight="bold")

    y, w, gap = 0.755, 0.295, 0.035
    x0 = 0.028
    for i, (head, sub, ex) in enumerate(S["beats"]):
        cx = x0 + w / 2 + i * (w + gap)
        box(ax, cx, y, w, 0.255, "white", INK)
        ax.text(cx, y + 0.088, head, ha="center", va="center",
                fontsize=8.2, color=INK, fontweight="bold")
        ax.text(cx, y + 0.022, sub, ha="center", va="center",
                fontsize=6.4, color=MUTE, linespacing=1.5)
        ax.plot([cx - w / 2 + 0.03, cx + w / 2 - 0.03], [y - 0.032, y - 0.032],
                color=SOFT, lw=0.8)
        ax.text(cx, y - 0.083, ex, ha="center", va="center",
                fontsize=6.2, color=INK, style="italic", linespacing=1.5)
        if i:
            arrow(ax, cx - w / 2 - gap, y, cx - w / 2, y)

    ax.text(0.5, 0.545, S["prevents_head"], ha="center", va="center",
            fontsize=6.6, color=SOFT, fontweight="bold")
    box(ax, 0.5, 0.455, 0.70, 0.115, FILL, SOFT)
    ax.text(0.5, 0.483, S["prevents"][0], ha="center", va="center",
            fontsize=7.6, color=INK, fontweight="bold")
    ax.text(0.5, 0.428, S["prevents"][1], ha="center", va="center",
            fontsize=6.4, color=MUTE)

    for cx, (label, ex) in zip((0.275, 0.725), S["choose"]):
        ax.text(cx, 0.318, label, ha="center", va="center",
                fontsize=7.0, color=INK, fontweight="bold")
        ax.text(cx, 0.258, ex, ha="center", va="center",
                fontsize=6.5, color=MUTE, style="italic")
    ax.text(0.5, 0.175, S["choose_note"], ha="center", va="center",
            fontsize=6.8, color=MUTE)

    ax.text(0.5, 0.062, S["foot"], ha="center", va="center",
            fontsize=6.6, color=MUTE, style="italic")

    fig.subplots_adjust(left=0.012, right=0.988, top=0.985, bottom=0.015)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


def build_criticalpath(S: dict, out: Path) -> None:
    """What runs together, what runs in order, and the chain you cannot shorten.

    Both halves are the chapter's own examples: its three subtasks with no
    dependency between them, and its worker-critic-you chain of "three steps
    that cannot collapse into fewer". They are drawn as two separate panels
    because the chapter never joins them into one workflow.
    """
    fig, ax = plt.subplots(figsize=(9.6, 4.15))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    # left panel: roles with no dependency
    ax.text(0.245, 0.925, S["head_par"], ha="center", va="center",
            fontsize=6.6, color=SOFT, fontweight="bold")
    ax.text(0.245, 0.868, S["sub_par"], ha="center", va="center",
            fontsize=6.8, color=MUTE, style="italic")
    for i, label in enumerate(S["par"]):
        cy = 0.735 - i * 0.155
        box(ax, 0.245, cy, 0.40, 0.115, FILL, SOFT)
        ax.text(0.245, cy, label, ha="center", va="center",
                fontsize=7.6, color=INK)

    ax.plot([0.495, 0.495], [0.235, 0.955], color=SOFT, lw=0.8, ls=(0, (4, 4)))

    # right panel: the critical path
    ax.text(0.748, 0.925, S["head_seq"], ha="center", va="center",
            fontsize=6.6, color=SOFT, fontweight="bold")
    ax.text(0.748, 0.868, S["sub_seq"], ha="center", va="center",
            fontsize=6.8, color=MUTE, style="italic")
    for i, (head, sub) in enumerate(S["seq"]):
        cy = 0.735 - i * 0.155
        box(ax, 0.748, cy, 0.40, 0.115, "white", INK, lw=1.8)
        ax.text(0.748, cy + 0.022, head, ha="center", va="center",
                fontsize=7.8, color=INK, fontweight="bold")
        ax.text(0.748, cy - 0.028, sub, ha="center", va="center",
                fontsize=6.3, color=MUTE, linespacing=1.45)
        if i:
            arrow(ax, 0.748, cy + 0.0575 + 0.0395, 0.748, cy + 0.0575)
    ax.text(0.748, 0.345, S["seq_note"], ha="center", va="center",
            fontsize=6.8, color=INK, style="italic")

    ax.text(0.5, 0.105, S["foot"], ha="center", va="center",
            fontsize=7.6, color=INK, style="italic")

    fig.subplots_adjust(left=0.012, right=0.988, top=0.985, bottom=0.015)
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)


BUILDERS = (
    ("mida", "mida_map.png", build_mida),
    ("loop", "diagnose_loop.png", build_loop),
    ("groups", "sampling_groups.png", build_groups),
    ("compass", "inquiry_compass.png", build_compass),
    ("declaration", "declaration_anatomy.png", build_declaration),
    ("leadloop", "retrieval_verification_loop.png", build_leadloop),
    ("provenance", "provenance_chain.png", build_provenance),
    ("codeloop", "ai_coding_loop.png", build_codeloop),
    ("verbgate", "claim_boundary_verb.png", build_verbgate),
    ("capsule", "reproducibility_capsule.png", build_capsule),
    ("uln", "uln_move.png", build_uln),
    ("criticalpath", "critical_path.png", build_criticalpath),
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
