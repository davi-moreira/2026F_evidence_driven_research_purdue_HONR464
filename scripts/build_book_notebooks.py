#!/usr/bin/env python3
"""build_book_notebooks.py — the book's OWN companion Colab notebooks (D25).

EDR|AI and the course are different artifacts: every book chapter ships its own
companion notebook, so a reader can run the chapter's code and complete the
chapter's "It is your turn" section from the chapter's Colab badge, with no
course involved. This generator parses each edition's chapter .qmd files
(EN book/, PT book-pt/, ES book-es/) and writes one workbook per chapter:

    notebooks/book/chNN_<slug>.ipynb        (English)
    notebooks/book/pt/chNN_<slug>.ipynb     (Português-BR)
    notebooks/book/es/chNN_<slug>.ipynb     (Español)

Each workbook carries: the chapter header + how-to, the research-decision
quote, any runnable code blocks from the chapter body, the full "It is your
turn" section with a work cell per step (D38: AI prompts live INSIDE the
step they serve — prompt-bearing steps also get a response cell), and the
section's grading RUBRIC (D26) — one 0/1/2 row per step plus a standing
craft-and-verification row, derived mechanically from the step text. The
same rubrics are collected into <edition>/_iyt-rubrics.qmd, included in the
For-instructors appendix for grading. Branch/optional lessons close with a
studio-junction note instead of a bare Next link (D38 route graph).

Cell ids are deterministic so regeneration produces clean git diffs. Re-run
after ANY chapter edit (the book-first loop):

    .venv/bin/python scripts/build_book_notebooks.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from book_manifest import (active_lessons, load_architecture,  # noqa: E402
                           require_lock)
SITE = "https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464"

EDITIONS = [
    {
        "code": "en",
        "book_dir": "book",
        "out_sub": "",
        "site_base": f"{SITE}/book",
        "prompts_heading": "Recommended AI prompts",
        "iyt_heading": "It is your turn",
        "lab_headings": ["The Colab laboratory"],
        "chapter_word": "Chapter",
        "book_name": "EDR|AI — Evidence-Driven Research in the Age of AI",
        "header": ("This is the **companion notebook** of [{chapter_word} {n} — "
                   "{title}]({url}) from **{book}**. Authored by "
                   "[Davi Moreira]({home}).\n\n[Open the chapter]({url}) · "
                   "[Book home]({home}) · [Verification Guide]({vg})\n\n"
                   "*AI is your arm and your research assistant, not your brain.*"),
        "howto": ("## How to use this notebook\n\n"
                  "1. Work top to bottom, with the chapter open in another tab.\n"
                  "2. Copy each **AI prompt** into your AI tool, run it, then record "
                  "in the response cell what came back and what you verified.\n"
                  "3. Run the code cells; change something and run again.\n"
                  "4. Finish the **It is your turn** workspace at the end — that is "
                  "this chapter's step of your own research project.\n"
                  "5. Log every AI use in your **AI Research Ledger**: task · tool · "
                  "prompt · output summary · decision · verification method · "
                  "remaining concern · you as the responsible researcher.\n"
                  "6. Your AI can be more than a chatbot: agentic tools can run "
                  "multi-step work for you. Delegating boldly is fine; reviewing, "
                  "curating, and deciding stay yours."),
        "response_cell": ("✍️ **Your run.** Double-click this cell and record: what "
                          "the AI returned (one or two lines), what you verified and "
                          "how, and your ledger row."),
        "code_heading": "## Code from the chapter",
        "code_note": ("The cells below come from the chapter. Run them, then change "
                      "something and run again — the numbers should move the way the "
                      "chapter says they will."),
        "code_from": ("*From the section “{section}”.* **What this cell does:** exactly "
                      "what the chapter walks through in that section; run it and "
                      "compare with the chapter."),
        "code_reading": ("**Reading the output.** The chapter reads this output in the "
                         "same section; check yours against it, then change one input "
                         "and rerun. The numbers should move the way the chapter says "
                         "they will."),
        "step_word": "Step",
        "work_cell": ("✍️ **Your work for step {i}.** Double-click this cell and "
                      "write your answer here."),
        "work_cell_generic": ("✍️ **Your work.** Double-click this cell and complete "
                              "the section above here."),
        "scratch": "# Scratch space — use this cell for any code your steps need.",
        "rubric_heading": "### The standard this section is held to",
        "rubric_intro": ("Use this as a self-check while you work. It is also the bar "
                         "the same work meets later, once your project carries it. "
                         "Each row: **0** missing, **1** attempted but incomplete, "
                         "generic, or unverified, **2** complete, specific to your own "
                         "project, and verified where a check applies. **{total} "
                         "points in all.**"),
        "rubric_header_row": "| # | Criterion | 0–2 |",
        "rubric_standing": ("Craft and verification record: AI use logged in your AI "
                            "Research Ledger, claims stated with their uncertainty, "
                            "and each key claim verified with a named method"),
        "rubric_fallback": "The section above, completed for your own project",
        "appendix_title": '## Grading rubrics — the "It is your turn" sections',
        "appendix_intro": ("One rubric per chapter, derived from the chapter's "
                           "numbered steps. The same rubric appears in the chapter's "
                           "companion notebook, so the standard the reader worked to "
                           "is the standard you apply when the project carries that "
                           "work. The scale, for every rubric: **0** missing · "
                           "**1** attempted · **2** complete, project-specific, and "
                           "verified."),
        "ch_word": "Ch.",
        "closing": ("**Before you leave this notebook:** add today's rows to your AI "
                    "Research Ledger, and verify your key claim with a named method "
                    "from the [Verification Guide]({vg}). AI can review AI — but the "
                    "last decision is human."),
        "next_line": "Next: [{chapter_word} {n} — {title}]({url}).",
        "branch_note": ("That chapter may not be on your route — [Studio {sn}: "
                        "{stitle}]({surl}) is the junction; follow the lesson "
                        "that matches your own project."),
        "last_line": ("This was the last chapter: the **It is your turn** sections "
                      "you worked are your research project. Assemble the portfolio, "
                      "and defend it."),
    },
    {
        "code": "pt",
        "book_dir": "book-pt",
        "out_sub": "pt",
        "site_base": f"{SITE}/book-pt",
        "prompts_heading": "Prompts de IA recomendados",
        "iyt_heading": "Agora é a sua vez",
        "lab_headings": ["O laboratório em Colab", "O laboratório no Colab"],
        "chapter_word": "Capítulo",
        "book_name": "EDR|AI — Pesquisa Orientada por Evidências na Era da IA",
        "header": ("Este é o **notebook companheiro** do [{chapter_word} {n} — "
                   "{title}]({url}) de **{book}**. De autoria de "
                   "[Davi Moreira]({home}).\n\n[Abrir o capítulo]({url}) · "
                   "[Início do livro]({home}) · [Guia de Verificação]({vg})\n\n"
                   "*A IA é o seu braço e a sua assistente de pesquisa, não o seu "
                   "cérebro.*"),
        "howto": ("## Como usar este notebook\n\n"
                  "1. Trabalhe de cima para baixo, com o capítulo aberto em outra "
                  "aba.\n"
                  "2. Copie cada **prompt de IA** para a sua ferramenta de IA, rode, "
                  "e registre na célula de resposta o que voltou e o que você "
                  "verificou.\n"
                  "3. Rode as células de código; mude algo e rode de novo.\n"
                  "4. Termine o espaço de trabalho **Agora é a sua vez** no final — "
                  "ele é a etapa deste capítulo no seu próprio projeto de pesquisa.\n"
                  "5. Registre todo uso de IA no seu **AI Research Ledger**: tarefa · "
                  "ferramenta · prompt · resumo do resultado · decisão · método de "
                  "verificação · preocupação restante · você como pesquisador(a) "
                  "responsável.\n"
                  "6. A sua IA pode ser mais do que um chatbot: ferramentas agênticas "
                  "executam trabalho de várias etapas para você. Delegar com ousadia "
                  "é bom; revisar, fazer a curadoria e decidir continuam com você."),
        "response_cell": ("✍️ **Seu registro.** Clique duas vezes nesta célula e "
                          "anote: o que a IA devolveu (uma ou duas linhas), o que "
                          "você verificou e como, e a sua linha do ledger."),
        "code_heading": "## Código do capítulo",
        "code_note": ("As células abaixo vêm do capítulo. Rode-as, depois mude algo e "
                      "rode de novo — os números devem se mover do jeito que o "
                      "capítulo diz."),
        "code_from": ("*Da seção “{section}”.* **O que esta célula faz:** exatamente o "
                      "que o capítulo percorre nessa seção; rode e compare com o "
                      "capítulo."),
        "code_reading": ("**Lendo o resultado.** O capítulo lê este resultado na mesma "
                         "seção; confira o seu contra o dele, depois mude um valor e "
                         "rode de novo. Os números devem se mover do jeito que o "
                         "capítulo diz."),
        "step_word": "Passo",
        "work_cell": ("✍️ **Seu trabalho no passo {i}.** Clique duas vezes nesta "
                      "célula e escreva a sua resposta aqui."),
        "work_cell_generic": ("✍️ **Seu trabalho.** Clique duas vezes nesta célula e "
                              "complete aqui a seção acima."),
        "scratch": ("# Espaço de rascunho — use esta célula para qualquer código de "
                    "que os passos precisarem."),
        "rubric_heading": "### Como esta seção é avaliada",
        "rubric_intro": ("Cada linha vale **0** (ausente), **1** (tentada, mas "
                         "incompleta, genérica ou não verificada) ou **2** (completa, "
                         "específica do seu próprio projeto e verificada onde couber "
                         "uma checagem). **{total} pontos no total.**"),
        "rubric_header_row": "| # | Critério | 0–2 |",
        "rubric_standing": ("Cuidado e registro de verificação: uso de IA registrado "
                            "no seu AI Research Ledger, alegações declaradas com a "
                            "sua incerteza, e cada alegação-chave verificada com um "
                            "método nomeado"),
        "rubric_fallback": "A seção acima, completada para o seu próprio projeto",
        "appendix_title": ('## Rubricas de avaliação — as seções '
                           '"Agora é a sua vez"'),
        "appendix_intro": ("Uma rubrica por capítulo, derivada dos passos numerados "
                           "do capítulo. A mesma rubrica aparece no notebook "
                           "companheiro do capítulo, então o que você avalia é "
                           "exatamente o que o estudante viu. Pontuação de todas as "
                           "rubricas: **0** ausente · **1** tentada · **2** completa, "
                           "específica do projeto e verificada."),
        "ch_word": "Cap.",
        "closing": ("**Antes de sair deste notebook:** acrescente as linhas de hoje "
                    "ao seu AI Research Ledger, e verifique a sua alegação principal "
                    "com um método nomeado do [Guia de Verificação]({vg}). IA pode "
                    "revisar IA — mas a última decisão é humana."),
        "next_line": "A seguir: [{chapter_word} {n} — {title}]({url}).",
        "last_line": ("Este era o último capítulo: as seções **Agora é a sua vez** "
                      "que você trabalhou são o seu projeto de pesquisa. Monte o "
                      "portfólio, e defenda-o."),
    },
    {
        "code": "es",
        "book_dir": "book-es",
        "out_sub": "es",
        "site_base": f"{SITE}/book-es",
        "prompts_heading": "Prompts de IA recomendados",
        "iyt_heading": "Ahora te toca a ti",
        "lab_headings": ["El laboratorio en Colab"],
        "chapter_word": "Capítulo",
        "book_name": "EDR|AI — Investigación Guiada por la Evidencia en la Era de la IA",
        "header": ("Este es el **cuaderno de acompañamiento** del [{chapter_word} "
                   "{n} — {title}]({url}) de **{book}**. Escrito por "
                   "[Davi Moreira]({home}).\n\n[Abrir el capítulo]({url}) · "
                   "[Inicio del libro]({home}) · [Guía de Verificación]({vg})\n\n"
                   "*La IA es tu brazo y tu asistente de investigación, no tu "
                   "cerebro.*"),
        "howto": ("## Cómo usar este cuaderno\n\n"
                  "1. Trabaja de arriba hacia abajo, con el capítulo abierto en otra "
                  "pestaña.\n"
                  "2. Copia cada **prompt de IA** en tu herramienta de IA, córrelo, y "
                  "registra en la celda de respuesta qué volvió y qué verificaste.\n"
                  "3. Corre las celdas de código; cambia algo y corre de nuevo.\n"
                  "4. Termina el espacio de trabajo **Ahora te toca a ti** del final "
                  "— es el paso de este capítulo en tu propio proyecto de "
                  "investigación.\n"
                  "5. Registra cada uso de IA en tu **AI Research Ledger**: tarea · "
                  "herramienta · prompt · resumen del resultado · decisión · método "
                  "de verificación · preocupación restante · tú como responsable de "
                  "la investigación.\n"
                  "6. Tu IA puede ser más que un chatbot: las herramientas agénticas "
                  "ejecutan trabajo de varios pasos por ti. Delegar con audacia está "
                  "bien; revisar, curar y decidir siguen siendo tuyos."),
        "response_cell": ("✍️ **Tu registro.** Haz doble clic en esta celda y anota: "
                          "qué devolvió la IA (una o dos líneas), qué verificaste y "
                          "cómo, y tu fila del ledger."),
        "code_heading": "## Código del capítulo",
        "code_note": ("Las celdas de abajo vienen del capítulo. Córrelas, luego "
                      "cambia algo y corre de nuevo — los números deben moverse como "
                      "dice el capítulo."),
        "code_from": ("*De la sección “{section}”.* **Qué hace esta celda:** exactamente "
                      "lo que el capítulo recorre en esa sección; córrela y compara "
                      "con el capítulo."),
        "code_reading": ("**Leyendo el resultado.** El capítulo lee este resultado en "
                         "la misma sección; compara el tuyo con el suyo, luego cambia "
                         "un valor y corre de nuevo. Los números deben moverse como "
                         "dice el capítulo."),
        "step_word": "Paso",
        "work_cell": ("✍️ **Tu trabajo en el paso {i}.** Haz doble clic en esta celda "
                      "y escribe tu respuesta aquí."),
        "work_cell_generic": ("✍️ **Tu trabajo.** Haz doble clic en esta celda y "
                              "completa aquí la sección de arriba."),
        "scratch": ("# Espacio de borrador — usa esta celda para cualquier código que "
                    "necesiten los pasos."),
        "rubric_heading": "### Cómo se califica esta sección",
        "rubric_intro": ("Cada fila vale **0** (ausente), **1** (intentada pero "
                         "incompleta, genérica o sin verificar) o **2** (completa, "
                         "específica de tu propio proyecto y verificada donde aplique "
                         "una comprobación). **{total} puntos en total.**"),
        "rubric_header_row": "| # | Criterio | 0–2 |",
        "rubric_standing": ("Cuidado y registro de verificación: uso de IA registrado "
                            "en tu AI Research Ledger, afirmaciones declaradas con su "
                            "incertidumbre, y cada afirmación clave verificada con un "
                            "método nombrado"),
        "rubric_fallback": "La sección de arriba, completada para tu propio proyecto",
        "appendix_title": ('## Rúbricas de calificación — las secciones '
                           '"Ahora te toca a ti"'),
        "appendix_intro": ("Una rúbrica por capítulo, derivada de los pasos numerados "
                           "del capítulo. La misma rúbrica aparece en el cuaderno de "
                           "acompañamiento del capítulo, así que lo que calificas es "
                           "exactamente lo que vio el estudiante. Puntaje de todas "
                           "las rúbricas: **0** ausente · **1** intentada · **2** "
                           "completa, específica del proyecto y verificada."),
        "ch_word": "Cap.",
        "closing": ("**Antes de salir de este cuaderno:** agrega las filas de hoy a "
                    "tu AI Research Ledger, y verifica tu afirmación principal con un "
                    "método nombrado de la [Guía de Verificación]({vg}). La IA puede "
                    "revisar a la IA — pero la última decisión es humana."),
        "next_line": "Siguiente: [{chapter_word} {n} — {title}]({url}).",
        "branch_note": ("Ese capítulo puede no estar en tu ruta — [Estudio {sn}: {stitle}]({surl}) es el cruce; sigue la lección que corresponde a tu proyecto."),
        "last_line": ("Este era el último capítulo: las secciones **Ahora te toca "
                      "a ti** que trabajaste son tu proyecto de investigación. Arma "
                      "el portafolio, y defiéndelo."),
    },
]

FENCE_RE = re.compile(r"^```")
CALLOUT_OPEN_RE = re.compile(r'^:{3,}\s*\{\.callout-[a-z]+(?:\s+title="([^"]*)")?[^}]*\}\s*$')
STEP_RE = re.compile(r"^\d+\.\s")


def parse_front_matter(text: str) -> tuple[str, str]:
    """Return (title, body-after-front-matter)."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    title = ""
    if m:
        tm = re.search(r'^title:\s*"(.*)"\s*$', m.group(1), re.M)
        title = tm.group(1) if tm else ""
        return title, text[m.end():]
    hm = re.search(r"^#\s+(.+?)(?:\s*\{[^}]*\})?\s*$", text, re.M)
    return (hm.group(1) if hm else ""), text


LINK_RE = re.compile(r"\((?P<path>(?:\.\./)?[\w][\w\-/]*\.qmd)(?P<anchor>#[\w\-]+)?\)")


def resolve_links(text: str, site_base: str, part_dir: str) -> str:
    """Rewrite relative .qmd links to rendered site URLs; strip link attrs."""
    book_root = REPO / site_base.rsplit("/", 1)[-1]

    def sub(m: re.Match) -> str:
        path, anchor = m.group("path"), m.group("anchor") or ""
        if path.startswith("../"):
            path = path[3:]
        elif "/" not in path and not (book_root / path).exists():
            path = f"{part_dir}/{path}"  # sibling chapter in the same part dir
        return f"({site_base}/{path[:-4]}.html{anchor})"

    return LINK_RE.sub(sub, text).replace('{target="_blank"}', "")


def convert_callouts(text: str) -> str:
    """Turn ::: callout divs into markdown blockquotes."""
    out, in_callout = [], False
    for line in text.splitlines():
        m = CALLOUT_OPEN_RE.match(line)
        if m and not in_callout:
            in_callout = True
            title = m.group(1)
            if title:
                out.append(f"> **{title}.**")
                out.append(">")
            continue
        if in_callout and re.match(r"^:{3,}\s*$", line):
            in_callout = False
            continue
        if in_callout:
            out.append(f"> {line}".rstrip())
        else:
            out.append(line)
    return "\n".join(out)


def split_sections(body: str) -> list[tuple[str, str]]:
    """Return [(heading, section-text)]; text before first ## gets heading ''."""
    parts: list[tuple[str, str]] = []
    current, buf = "", []
    for line in body.splitlines():
        if line.startswith("## "):
            parts.append((current, "\n".join(buf).strip()))
            current, buf = line[3:].strip(), []
        else:
            buf.append(line)
    parts.append((current, "\n".join(buf).strip()))
    return parts


def first_blockquote(text: str) -> str:
    """The research-decision quote: first run of '>' lines in the chapter."""
    lines, quote, started = text.splitlines(), [], False
    for line in lines:
        if line.startswith(">"):
            started = True
            quote.append(line)
        elif started:
            break
    return "\n".join(quote)


def prompt_chunks(section: str) -> list[tuple[str, bool]]:
    """Split the prompts section into (chunk, has_fence) pieces.

    A new chunk starts at a paragraph opening with '**' outside any fence, so
    each recommended prompt (bold lead + fenced prompt + verify paragraph)
    becomes one chunk and earns its own response cell.
    """
    chunks: list[list[str]] = [[]]
    in_fence = prev_blank = False
    for line in section.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
        if (not in_fence and not FENCE_RE.match(line) and prev_blank
                and (line.startswith("**") or line.startswith(":::"))
                and chunks[-1]):
            chunks.append([])
        chunks[-1].append(line)
        prev_blank = line.strip() == ""
    out = []
    for c in chunks:
        text = "\n".join(c).strip()
        if text:
            out.append((text, "```" in text))
    return out


def iyt_pieces(section: str) -> tuple[str, list[str]]:
    """Return (intro, [step texts]) from the It-is-your-turn section."""
    lines = section.splitlines()
    intro: list[str] = []
    steps: list[list[str]] = []
    in_fence = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
        if not in_fence and STEP_RE.match(line):
            steps.append([re.sub(STEP_RE, "", line)])
        elif steps:
            steps[-1].append(re.sub(r"^ {2,3}", "", line))
        else:
            intro.append(line)
    return "\n".join(intro).strip(), ["\n".join(s).strip() for s in steps]


def first_sentence(text: str, limit: int = 150) -> str:
    """A rubric criterion from a step: its first sentence, flattened."""
    flat = re.sub(r"\s+", " ", text).strip()
    flat = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", flat)  # links -> their text
    sent = re.split(r"(?<=[.!?])\s", flat)[0].rstrip(".")
    if len(sent) > limit:
        sent = sent[:limit].rsplit(" ", 1)[0] + "…"
    return sent.replace("|", "\\|")


def rubric_table(ed: dict, steps: list[str]) -> str:
    """The chapter's It-is-your-turn rubric (D26): 0/1/2 per step + craft row."""
    rows = ([(f"{ed['step_word']} {i}", first_sentence(s))
             for i, s in enumerate(steps, 1)]
            if steps else [("1", ed["rubric_fallback"])])
    rows.append(("+", ed["rubric_standing"]))
    lines = [ed["rubric_header_row"], "|---|---|---|"]
    lines += [f"| {label} | {crit} | |" for label, crit in rows]
    return (ed["rubric_intro"].format(total=2 * len(rows))
            + "\n\n" + "\n".join(lines))


def python_blocks(sections, skip_headings) -> list[tuple[str, str]]:
    """(section-heading, code) for every ```python fence outside skipped sections."""
    found = []
    for heading, text in sections:
        if heading in skip_headings:
            continue
        for m in re.finditer(r"```python\n(.*?)\n```", text, re.S):
            found.append((heading, m.group(1)))
    return found


def md_cell(idx: int, source: str) -> dict:
    return {"cell_type": "markdown", "id": f"c{idx:03d}",
            "metadata": {}, "source": source.splitlines(keepends=True)}


def code_cell(idx: int, source: str) -> dict:
    return {"cell_type": "code", "id": f"c{idx:03d}", "metadata": {},
            "execution_count": None, "outputs": [],
            "source": source.splitlines(keepends=True)}


def chapter_files(book_dir: Path) -> list[Path]:
    files = sorted(p for p in book_dir.glob("part*/[0-9][0-9]-*.qmd"))
    return files


def build_notebook(ed: dict, path: Path, nxt: tuple[str, str] | None,
                   rubrics: list | None = None,
                   lesson: dict | None = None,
                   station: dict | None = None) -> dict:
    title, body = parse_front_matter(path.read_text())
    part_dir = path.parent.name
    # Display number and canonical URL come from the MANIFEST (round-9 N2);
    # nothing is parsed out of the filename's numeric prefix.
    n = lesson["display"]
    url = f"{ed['site_base']}/{lesson['url_path']}"
    home = f"{ed['site_base']}/index.html"
    vg = f"{ed['site_base']}/verification-guide.html"

    def prep(text: str) -> str:
        return resolve_links(convert_callouts(text), ed["site_base"], part_dir)

    sections = split_sections(body)
    by_name = dict(sections)
    cells: list[dict] = []
    i = 0

    def add_md(src):
        nonlocal i
        cells.append(md_cell(i, src)); i += 1

    def add_code(src):
        nonlocal i
        cells.append(code_cell(i, src)); i += 1

    add_md(f'<img src="{ed["site_base"]}/images/edrai_logo.png" '
           f'alt="EDR|AI" width="300"/>\n\n'
           f"# {ed['chapter_word']} {n} — {title}\n\n"
           + ed["header"].format(chapter_word=ed["chapter_word"], n=n, title=title,
                                 url=url, home=home, vg=vg, book=ed["book_name"]))
    add_md(ed["howto"])

    quote = first_blockquote(body)
    if quote:
        add_md(prep(quote))

    skip = set(ed["lab_headings"]) | {ed["prompts_heading"], ed["iyt_heading"]}
    code = python_blocks(sections, skip)
    if code:
        add_md(ed["code_heading"] + "\n\n" + ed["code_note"])
        for heading, block in code:
            add_md(ed["code_from"].format(section=heading))
            add_code(block)
            add_md(ed["code_reading"])

    # D38: the standalone prompts section is retired — prompts live inside
    # the IYT steps they serve. (The lookup stays for the frozen PT/ES
    # sources until the translation pass regenerates them.)
    prompts = by_name.get(ed["prompts_heading"], "")
    if prompts:
        add_md(f"## {ed['prompts_heading']}")
        for chunk, has_fence in prompt_chunks(prompts):
            chunk = re.sub(r"^```python\s*$", "```", chunk, flags=re.M)
            add_md(prep(chunk))
            if has_fence:
                add_md(ed["response_cell"])

    iyt = by_name.get(ed["iyt_heading"], "")
    intro, steps = iyt_pieces(iyt)
    add_md(f"## {ed['iyt_heading']}" + (f"\n\n{prep(intro)}" if intro else ""))
    if steps:
        for k, step in enumerate(steps, 1):
            add_md(f"**{ed['step_word']} {k}.** {prep(step)}")
            add_md(ed["work_cell"].format(i=k))
            if "```" in step or "💡" in step:   # the step carries an AI prompt
                add_md(ed["response_cell"])
    else:
        add_md(ed["work_cell_generic"])
    rubric = rubric_table(ed, steps)
    add_md(ed["rubric_heading"] + "\n\n" + rubric)
    if rubrics is not None:
        rubrics.append((n, title, rubric))
    add_code(ed["scratch"])

    closing = ed["closing"].format(vg=vg)
    if nxt:
        nxt_url, nxt_title = nxt
        closing += "\n\n" + ed["next_line"].format(
            chapter_word=ed["chapter_word"], n=n + 1, title=nxt_title, url=nxt_url)
        # D38 route graph: a branch/optional lesson's physical successor may
        # not be on the reader's route — name the studio as the junction.
        if lesson and lesson.get("role") in ("branch", "optional") and station:
            closing += " " + ed["branch_note"].format(
                sn=station["rank"], stitle=station["title"],
                surl=(f"{ed['site_base']}/studios/"
                      f"studio{station['rank']:02d}-{station['id']}.html"))
    else:
        closing += "\n\n" + ed["last_line"]
    add_md(closing)

    return {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    # D36 freeze (round-5 L1): PT/ES are FROZEN until the end-of-project
    # translation pass — generating their companions from frozen sources would
    # still rewrite tracked artifacts, so the generator defaults to EN only.
    # Pass --editions all (or pt/es) ONLY when the freeze is lifted.
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--editions", default="en",
                    choices=["en", "pt", "es", "all"],
                    help="editions to generate (default en — D36 freeze)")
    sel = ap.parse_args().editions
    active = [ed for ed in EDITIONS if sel == "all" or ed["code"] == sel]
    # Identity comes from the validated manifest: active lessons in rank
    # order, with explicit source / url_path / companion paths. Activating a
    # planned lesson changes the count with no code edit (round-9 N2).
    require_lock()
    lessons = active_lessons()
    stations_by_id = {s["id"]: s for s in load_architecture()["stations"]}
    total = 0
    for ed in active:
        book_dir = REPO / ed["book_dir"]
        out_dir = REPO / "notebooks" / "book" / ed["out_sub"]
        out_dir.mkdir(parents=True, exist_ok=True)
        missing = [l["id"] for l in lessons
                   if not (book_dir / l["source"]).exists()]
        if missing:
            sys.exit(f"✗ {ed['book_dir']}: manifest lessons without a source "
                     f"file: {missing}")
        rubrics: list[tuple[int, str, str]] = []
        for k, lesson in enumerate(lessons):
            path = book_dir / lesson["source"]
            nxt = None
            if k + 1 < len(lessons):
                nxt_lesson = lessons[k + 1]
                nxt_path = book_dir / nxt_lesson["source"]
                nxt_title, _ = parse_front_matter(nxt_path.read_text())
                nxt = (f"{ed['site_base']}/{nxt_lesson['url_path']}", nxt_title)
            nb = build_notebook(ed, path, nxt, rubrics, lesson,
                                stations_by_id.get(lesson["station"]))
            out = out_dir / lesson["companion"]
            out.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
            total += 1
        inc = [ed["appendix_title"], "", ed["appendix_intro"], ""]
        for n, title, rubric in rubrics:
            inc += [f"### {ed['ch_word']} {n} — {title}", "", rubric, ""]
        (book_dir / "_iyt-rubrics.qmd").write_text("\n".join(inc))
        print(f"✓ {ed['book_dir']}: {len(lessons)} companion notebooks → "
              f"{out_dir.relative_to(REPO)}/ + _iyt-rubrics.qmd")
    print(f"✓ {total} book companion notebooks built")


if __name__ == "__main__":
    main()
