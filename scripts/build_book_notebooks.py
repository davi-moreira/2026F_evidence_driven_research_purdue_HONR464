#!/usr/bin/env python3
"""build_book_notebooks.py — the book's OWN companion Colab notebooks (D25).

EDR|AI and the course are different artifacts: every book chapter ships its own
companion notebook, so a reader can run the chapter's code and complete the
chapter's "It is your turn" section from the chapter's Colab badge, with no
course involved. This generator parses each edition's 37 chapter .qmd files
(EN book/, PT book-pt/, ES book-es/) and writes one workbook per chapter:

    notebooks/book/chNN_<slug>.ipynb        (English)
    notebooks/book/pt/chNN_<slug>.ipynb     (Português-BR)
    notebooks/book/es/chNN_<slug>.ipynb     (Español)

Each workbook carries: the chapter header + how-to, the research-decision
quote, any runnable code blocks from the chapter body, the "Recommended AI
prompts" with a response cell per prompt, the "Do not delegate" callout, and
the full "It is your turn" section with a work cell per step.

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
                   "{title}]({url}) from **{book}**. It belongs to the book, not to "
                   "any course: everything you need is this notebook, the chapter, "
                   "and free Colab.\n\n[Open the chapter]({url}) · "
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
                  "remaining concern · you as the responsible researcher."),
        "response_cell": ("✍️ **Your run.** Double-click this cell and record: what "
                          "the AI returned (one or two lines), what you verified and "
                          "how, and your ledger row."),
        "code_heading": "## Code from the chapter",
        "code_note": ("The cells below come from the chapter. Run them, then change "
                      "something and run again — the numbers should move the way the "
                      "chapter says they will."),
        "code_from": "*From the section “{section}”.*",
        "step_word": "Step",
        "work_cell": ("✍️ **Your work for step {i}.** Double-click this cell and "
                      "write your answer here."),
        "work_cell_generic": ("✍️ **Your work.** Double-click this cell and complete "
                              "the section above here."),
        "scratch": "# Scratch space — use this cell for any code your steps need.",
        "closing": ("**Before you leave this notebook:** add today's rows to your AI "
                    "Research Ledger, and verify your key claim with a named method "
                    "from the [Verification Guide]({vg}). AI can review AI — but the "
                    "last decision is human."),
        "next_line": "Next: [{chapter_word} {n} — {title}]({url}).",
        "last_line": ("This was the last chapter: the 37 **It is your turn** sections "
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
                   "{title}]({url}) de **{book}**. Ele pertence ao livro, não a curso "
                   "nenhum: tudo de que você precisa é este notebook, o capítulo e o "
                   "Colab gratuito.\n\n[Abrir o capítulo]({url}) · "
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
                  "responsável."),
        "response_cell": ("✍️ **Seu registro.** Clique duas vezes nesta célula e "
                          "anote: o que a IA devolveu (uma ou duas linhas), o que "
                          "você verificou e como, e a sua linha do ledger."),
        "code_heading": "## Código do capítulo",
        "code_note": ("As células abaixo vêm do capítulo. Rode-as, depois mude algo e "
                      "rode de novo — os números devem se mover do jeito que o "
                      "capítulo diz."),
        "code_from": "*Da seção “{section}”.*",
        "step_word": "Passo",
        "work_cell": ("✍️ **Seu trabalho no passo {i}.** Clique duas vezes nesta "
                      "célula e escreva a sua resposta aqui."),
        "work_cell_generic": ("✍️ **Seu trabalho.** Clique duas vezes nesta célula e "
                              "complete aqui a seção acima."),
        "scratch": ("# Espaço de rascunho — use esta célula para qualquer código de "
                    "que os passos precisarem."),
        "closing": ("**Antes de sair deste notebook:** acrescente as linhas de hoje "
                    "ao seu AI Research Ledger, e verifique a sua alegação principal "
                    "com um método nomeado do [Guia de Verificação]({vg}). IA pode "
                    "revisar IA — mas a última decisão é humana."),
        "next_line": "A seguir: [{chapter_word} {n} — {title}]({url}).",
        "last_line": ("Este era o último capítulo: as 37 seções **Agora é a sua vez** "
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
                   "{n} — {title}]({url}) de **{book}**. Pertenece al libro, no a "
                   "ningún curso: todo lo que necesitas es este cuaderno, el capítulo "
                   "y Colab gratuito.\n\n[Abrir el capítulo]({url}) · "
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
                  "la investigación."),
        "response_cell": ("✍️ **Tu registro.** Haz doble clic en esta celda y anota: "
                          "qué devolvió la IA (una o dos líneas), qué verificaste y "
                          "cómo, y tu fila del ledger."),
        "code_heading": "## Código del capítulo",
        "code_note": ("Las celdas de abajo vienen del capítulo. Córrelas, luego "
                      "cambia algo y corre de nuevo — los números deben moverse como "
                      "dice el capítulo."),
        "code_from": "*De la sección “{section}”.*",
        "step_word": "Paso",
        "work_cell": ("✍️ **Tu trabajo en el paso {i}.** Haz doble clic en esta celda "
                      "y escribe tu respuesta aquí."),
        "work_cell_generic": ("✍️ **Tu trabajo.** Haz doble clic en esta celda y "
                              "completa aquí la sección de arriba."),
        "scratch": ("# Espacio de borrador — usa esta celda para cualquier código que "
                    "necesiten los pasos."),
        "closing": ("**Antes de salir de este cuaderno:** agrega las filas de hoy a "
                    "tu AI Research Ledger, y verifica tu afirmación principal con un "
                    "método nombrado de la [Guía de Verificación]({vg}). La IA puede "
                    "revisar a la IA — pero la última decisión es humana."),
        "next_line": "Siguiente: [{chapter_word} {n} — {title}]({url}).",
        "last_line": ("Este era el último capítulo: las 37 secciones **Ahora te toca "
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


def build_notebook(ed: dict, path: Path, nxt: tuple[str, str] | None) -> dict:
    title, body = parse_front_matter(path.read_text())
    part_dir = path.parent.name
    n = int(path.stem[:2])
    url = f"{ed['site_base']}/{part_dir}/{path.stem}.html"
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

    add_md(f"# {ed['chapter_word']} {n} — {title}\n\n"
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
    else:
        add_md(ed["work_cell_generic"])
    add_code(ed["scratch"])

    closing = ed["closing"].format(vg=vg)
    if nxt:
        nxt_url, nxt_title = nxt
        closing += "\n\n" + ed["next_line"].format(
            chapter_word=ed["chapter_word"], n=n + 1, title=nxt_title, url=nxt_url)
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
    total = 0
    for ed in EDITIONS:
        book_dir = REPO / ed["book_dir"]
        out_dir = REPO / "notebooks" / "book" / ed["out_sub"]
        out_dir.mkdir(parents=True, exist_ok=True)
        files = chapter_files(book_dir)
        if len(files) != 37:
            sys.exit(f"✗ {ed['book_dir']}: found {len(files)} chapters, expected 37")
        for k, path in enumerate(files):
            nxt = None
            if k + 1 < len(files):
                np_ = files[k + 1]
                nxt_title, _ = parse_front_matter(np_.read_text())
                nxt = (f"{ed['site_base']}/{np_.parent.name}/{np_.stem}.html",
                       nxt_title)
            nb = build_notebook(ed, path, nxt)
            slug = f"ch{path.stem[:2]}_{path.stem[3:].replace('-', '_')}"
            out = out_dir / f"{slug}.ipynb"
            out.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n")
            total += 1
        print(f"✓ {ed['book_dir']}: {len(files)} companion notebooks → "
              f"{out_dir.relative_to(REPO)}/")
    print(f"✓ {total} book companion notebooks built")


if __name__ == "__main__":
    main()
