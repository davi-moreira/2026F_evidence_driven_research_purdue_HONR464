#!/usr/bin/env python3
"""build_studio_slides.py — one revealjs deck per EDR|AI studio (D77).

Twelve decks, one per studio, each running that studio's own arc:

    the studio's promise  ->  its lessons, one section each  ->  its milestone

The deck is a GENERATED VIEW OF THE BOOK, never a parallel document. Every
verbatim element — the studio promise, each chapter's research decision, its
"Do not delegate" rule, its AI failure case, its worked-example code and
figures, its "It is your turn" steps, the milestone practice and the four
rails — is read out of the book at build time by scripts/slide_parts.py. Edit
a chapter and rerun this script: the deck changes with it. That is the whole
point, and scripts/validate_slide_sync.py is what keeps the promise honest.

Between the verbatim elements sits the prose the book argues in. Prose does
not fit on a slide unchanged, so each chapter may carry an EDITORIAL OVERLAY
at planning/BOOK_SLIDE_PLANS/<lesson-id>.yml: per book section, the slides to
cut it into, each with a headline and a few short lines. The overlay is
OPTIONAL — a section with no plan falls back to a mechanical rendering of its
paragraphs, so every deck is complete and correct from the first build, and
gets sharper as plans land. A plan records the chapter digest it was written
against; when the chapter moves past it, the plan is STALE and the validator
says which one.

    .venv/bin/python scripts/build_studio_slides.py            # all 12 decks
    .venv/bin/python scripts/build_studio_slides.py 3          # studio 3 only
    .venv/bin/python scripts/build_studio_slides.py --check    # exit 1 if stale

Renders with the site (`lecture_slides/**/*.qmd` is in _quarto.yml's render
list), so a deck is published at
    <site>/lecture_slides/studioNN_<slug>/studioNN_<slug>.html
which is what the Schedule page's Slides column links.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
import textwrap
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import slide_parts as sp                                        # noqa: E402
from book_manifest import active_lessons, load_architecture     # noqa: E402

BOOK = REPO / "book"
OUT_ROOT = REPO / "lecture_slides"
PLANS = REPO / "planning" / "BOOK_SLIDE_PLANS"
SITE = ("https://davi-moreira.github.io/"
        "2026F_evidence_driven_research_purdue_HONR464")
BOOK_URL = f"{SITE}/book"

COURSE = "HONR 46400 · Evidence-Driven Research"
CREED = "AI is your arm and your research assistant, not your brain."
INK = "#1a1a19"

#: Sections whose content the deck renders with a purpose-built slide rather
#: than as prose. Everything else is prose, planned or mechanical.
SPECIAL = {"it is your turn", "an ai failure case"}

#: Words per mechanical prose slide before it is split into lines.
PROSE_WORDS = 58

#: A section with no editorial plan gets at most this many prose slides. The
#: book argues in paragraphs; a slide per paragraph runs a six-chapter studio
#: past 200 slides, which is not a lecture. When a section exceeds the cap its
#: paragraphs are compressed to their lead sentences, and the full prose goes
#: to the speaker notes where the instructor actually needs it.
MAX_FALLBACK = 4


# ------------------------------------------------------------- helpers
def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", text).strip()
    return [s.strip() for s in
            re.split(r"(?<=[.!?])\s+(?=[A-Z“\"(*])", flat) if s.strip()]


def esc_yaml(text: str) -> str:
    return text.replace('"', '\\"')


#: How much a slide can carry at full size before it runs under the footer.
#: Superseded, kept in place. The builder used to COUNT CHARACTERS and stamp
#: a density class the theme sized down — which shrank the type on slides
#: that had room to spare and still let a long code block run past the bottom
#: edge, because a character count cannot know how tall a rendered slide is.
#: `lecture_slides/_theme/fit.html` now measures the real rendered height in
#: the browser and scales only what actually overflows. The function and its
#: thresholds stay so a deck built before the change still renders sanely,
#: and so the mechanism can be reinstated by flipping one constant.
STAMP_DENSITY = False
DENSITY = ((30, ".densest"), (21, ".denser"), (14, ".dense"))
CHARS_PER_LINE = 74


def density(body: str) -> str:
    """The density class a slide's body needs, or '' when it fits."""
    if not STAMP_DENSITY:
        return ""
    lines = 0
    for raw in body.split("\n"):
        line = raw.rstrip()
        if not line or line.startswith(":::"):
            continue
        lines += max(1, -(-len(line) // CHARS_PER_LINE))
    for limit, cls in DENSITY:
        if lines >= limit:
            return cls
    return ""


def menu_attr(label: str) -> str:
    """`data-menu-title="..."`, safe inside a Pandoc heading attribute block.

    The slide menu is how you cross a 122-slide deck mid-class, and by default
    every entry is just the slide's own headline — 122 lines with nothing
    saying which chapter you are in. Every slide therefore carries an explicit
    menu label that names its chapter, and a chapter's divider announces
    itself in capitals so the list reads as a table of contents.

    A straight double quote would close the attribute early and swallow the
    rest of the heading, and several chapter headlines contain one.
    """
    label = " ".join(label.split())
    label = label.replace('\\"', '"')
    # Alternate the replacements so a quoted phrase keeps a real opening and
    # closing mark rather than two closing ones.
    out, opening = [], True
    for ch in label:
        if ch == '"':
            out.append("\u201c" if opening else "\u201d")
            opening = not opening
        else:
            out.append(ch)
    return f'data-menu-title="{"".join(out)}"'


def div(cls: str, body: str, marks: int = 3) -> str:
    """A Pandoc fenced div, with the blank lines Pandoc requires.

    Without a blank line on each side of the fence, a nested run collapses
    into one paragraph and the closing `:::` leaks into the slide as literal
    text. `marks` widens the fence so a div can contain another one.
    """
    fence = ":" * marks
    attrs = " ".join(f".{c}" for c in cls.split())
    return f"{fence} {{{attrs}}}\n\n{body.strip()}\n\n{fence}"


def wrap(text: str, width: int = 78, indent: str = "") -> str:
    """Wrap prose for a readable generated source file, markdown-safe."""
    out = []
    for para in text.split("\n\n"):
        if para.lstrip().startswith(("|", "```", ":::", "<", "!", "-", "*")) \
                or re.match(r"^\s*\d+\.", para):
            out.append(para)
        else:
            out.append(textwrap.fill(para.strip(), width,
                                     initial_indent=indent,
                                     subsequent_indent=indent,
                                     break_long_words=False,
                                     break_on_hyphens=False))
    return "\n\n".join(out)


# ------------------------------------------------------------ the model
def studios() -> list[dict]:
    """Each studio with its lessons, opener page and milestone page."""
    arch = load_architecture()
    by_station: dict[str, list[dict]] = {}
    for lesson in active_lessons():
        by_station.setdefault(lesson["station"], []).append(lesson)

    out = []
    for st in sorted(arch["stations"], key=lambda s: s["rank"]):
        rank, sid = st["rank"], st["id"]
        opener = BOOK / "studios" / f"studio{rank:02d}-{sid}.qmd"
        milestone = BOOK / "studios" / f"milestone{rank:02d}-{sid}.qmd"
        out.append({
            "rank": rank,
            "id": sid,
            "title": st["title"],
            "lessons": sorted(by_station.get(sid, []), key=lambda l: l["rank"]),
            "opener": opener if opener.exists() else None,
            "milestone": milestone if milestone.exists() else None,
            "slug": f"studio{rank:02d}",
            "qmd": OUT_ROOT / f"studio{rank:02d}.qmd",
        })
    return out


def load_plan(lesson_id: str) -> dict:
    p = PLANS / f"{lesson_id}.yml"
    if not p.exists():
        return {}
    data = yaml.safe_load(p.read_text()) or {}
    return data if isinstance(data, dict) else {}


def plan_state(lesson: dict) -> tuple[str, dict]:
    """('none' | 'stale' | 'current', plan)."""
    plan = load_plan(lesson["id"])
    if not plan:
        return "none", {}
    live = sp.digest_of(lesson["source"])
    return ("current" if plan.get("source_sha256") == live else "stale"), plan


# ------------------------------------------------------- slide emitters
class Deck:
    """Accumulates slide markdown for one studio."""

    def __init__(self, studio: dict) -> None:
        self.s = studio
        self.parts: list[str] = []
        self.figs: dict[str, str] = {}       # book-relative src -> figs/<name>
        self.from_dir = ""                   # book dir of the page being quoted
        self.menu_prefix = ""                # names the chapter in the menu

    def add(self, md: str) -> None:
        self.parts.append(md.rstrip() + "\n")

    def quoting(self, source: Path | str) -> None:
        """Name the book page whose prose is being rendered, so its relative
        links resolve from ITS directory."""
        rel = Path(source)
        if rel.is_absolute():
            rel = rel.relative_to(BOOK)
        self.from_dir = str(rel.parent) if str(rel.parent) != "." else ""

    def clean(self, text: str) -> str:
        return sp.clean(text, BOOK_URL, self.from_dir)

    def figure(self, src: str, caption: str = "", width: str = "78%") -> str:
        """Copy a book figure into the shared deck figs/ and return markdown.

        A chapter writes its figures relative to its OWN directory
        (`../images/concepts/mida_map.png` from book/part2-.../), so the path
        is resolved against that directory before the file is located.
        """
        name = Path(src).name
        rel = Path(self.from_dir or ".") / src
        self.figs[str(Path(*rel.parts).as_posix())] = f"figs/{name}"
        cap = self.clean(caption)
        alt = re.sub(r"[\[\]\"]", "", re.sub(r"\*", "", cap))[:150]
        md = (f'![](figs/{name}){{fig-align="center" width="{width}" '
              f'fig-alt="{alt or name}"}}')
        if cap:
            md += "\n\n" + div("figure-caption", wrap(cap))
        return md

    # -- structural slides ------------------------------------------------
    def divider(self, kicker: str, heading: str, line: str = "",
                menu: str = "") -> None:
        attrs = f'background-color="{INK}" .divider {menu_attr(menu or heading)}'
        out = [f'## {heading} {{{attrs}}}', ""]
        if kicker:
            out += [div("kicker", kicker), ""]
        if line:
            out += [div("divider-line", wrap(self.clean(line)))]
        self.add("\n".join(out))

    def slide(self, title: str, body: str, kicker: str = "",
              note: str = "", classes: str = "") -> None:
        classes = " ".join(x for x in (classes, density(body)) if x)
        attrs = " ".join(x for x in
                         (classes, menu_attr(self.menu_prefix + title)) if x)
        out = [f"## {title}" + (f" {{{attrs}}}" if attrs else ""), ""]
        if kicker.strip().lower() == title.strip().lower():
            kicker = ""          # a kicker that repeats the title is noise
        if kicker:
            out += [div("kicker", kicker), ""]
        # The body travels as ONE block. The theme places that block in a
        # fixed rectangle below the title rule and centres it there, and
        # fit.html measures the block to decide whether it has to shrink.
        # Five colons: the widest fence a body can already contain is the
        # four-colon card grid.
        out.append(div("slide-body", body.rstrip(), marks=5))
        if note:
            out += ["", div("notes", wrap(self.clean(note)))]
        self.add("\n".join(out))

    def card(self, title: str, label: str, body: str, cls: str,
             kicker: str = "", note: str = "") -> None:
        text = wrap(self.clean(body))
        # A label that only restates the slide's own title is read twice and
        # says nothing the second time; the card keeps its accent without it.
        if label.strip().lower().strip(".") == title.strip().lower().strip("."):
            inner = div(cls, text)
        else:
            inner = div(cls, f'[{label}]{{.label}}\n\n{text}')
        self.slide(title, inner, kicker=kicker, note=note)

    def grid(self, cls: str, cell_cls: str,
             cells: list[tuple[str, str]]) -> str:
        """A card grid (key terms, the four rails) as properly nested divs."""
        inner = "\n\n".join(
            div(cell_cls, f'[{t}]{{.t}}\n\n[{d}]{{.d}}') for t, d in cells)
        return div(cls, inner, marks=4)


# ------------------------------------------------------ prose rendering
def prose_slides(deck: Deck, lesson_no: int | None, section: sp.Section,
                 plan_section: list | None) -> None:
    """Render one book section, from its plan when there is one."""
    kicker = (f"Chapter {lesson_no} · {section.heading}" if lesson_no
              else section.heading)

    if plan_section:
        for item in plan_section:
            _planned_slide(deck, kicker, section, item)
        return

    # ---- mechanical fallback: the section's own blocks, in order.
    paras = section.paragraphs()
    if len(paras) > MAX_FALLBACK:
        _compressed(deck, kicker, section, paras)
        for block in section.blocks:
            if block.kind in ("para", "list"):
                continue
            _non_prose(deck, kicker, section.heading, block)
        return

    seen_prose = 0
    for block in section.blocks:
        if block.kind == "para":
            head = (section.heading if not seen_prose
                    else f"{section.heading} *(cont.)*")
            _prose_block(deck, kicker, head, block.text)
            seen_prose += 1
        elif block.kind == "list":
            body = "\n".join(f"- {deck.clean(i)}" for i in block.items)
            deck.slide(section.heading if not seen_prose
                       else f"{section.heading} *(cont.)*", body, kicker=kicker)
            seen_prose += 1
        elif block.kind == "figure":
            deck.slide(section.heading, deck.figure(block.src, block.caption),
                       kicker=kicker)
        elif block.kind == "mermaid":
            deck.slide(section.heading,
                       f"```{{mermaid}}\n{block.text}\n```", kicker=kicker)
        elif block.kind == "code":
            deck.slide(section.heading,
                       f"```{block.lang}\n{block.text}\n```",
                       kicker=kicker,
                       note="Run it, change one input, and watch which "
                            "sentence in the chapter stops being true.")
        elif block.kind == "quote":
            deck.card(section.heading, "From the chapter", block.text,
                      "note-card", kicker=kicker)
        elif block.kind == "table":
            deck.slide(section.heading, deck.clean(block.text), kicker=kicker)


def _non_prose(deck: Deck, kicker: str, heading: str, block: sp.Block) -> None:
    """Figures, diagrams and code always get their own slide, plan or none."""
    if block.kind == "figure":
        deck.slide(heading, deck.figure(block.src, block.caption),
                   kicker=kicker)
    elif block.kind == "mermaid":
        deck.slide(heading, f"```{{mermaid}}\n{block.text}\n```", kicker=kicker)
    elif block.kind == "code":
        deck.slide(heading, f"```{block.lang}\n{block.text}\n```", kicker=kicker,
                   note="Run it, change one input, and watch which sentence "
                        "in the chapter stops being true.")
    elif block.kind == "table":
        deck.slide(heading, deck.clean(block.text), kicker=kicker)
    elif block.kind == "quote":
        deck.card(heading, "From the chapter", block.text, "note-card",
                  kicker=kicker)


def _compressed(deck: Deck, kicker: str, section: sp.Section,
                paras: list[sp.Block]) -> None:
    """A long unplanned section as MAX_FALLBACK slides of lead sentences."""
    leads = []
    for b in paras:
        sents = sentences(b.text)
        if sents:
            leads.append((sents[0], b.text))
    per = max(1, -(-len(leads) // MAX_FALLBACK))
    for k in range(0, len(leads), per):
        group = leads[k:k + per]
        body = "\n".join(f"- {deck.clean(lead)}" for lead, _ in group)
        title = section.heading if k == 0 else f"{section.heading} *(cont.)*"
        deck.slide(title, body, kicker=kicker,
                   note="\n\n".join(full for _, full in group))


def _prose_block(deck: Deck, kicker: str, heading: str, text: str) -> None:
    """A book paragraph as one slide: short ones whole, long ones as lines."""
    sents = sentences(text)
    if not sents:
        return
    # The paragraph's own lead is the headline when it is short enough to be
    # one; otherwise the section keeps the title and the lead becomes a line.
    lead = sents[0]
    words = len(re.sub(r"\s+", " ", text).split())
    if words <= PROSE_WORDS:
        deck.slide(heading, wrap(deck.clean(text)), kicker=kicker)
        return
    title = heading
    rest = sents
    if len(lead.split()) <= 14 and not lead.endswith(("?", "!")):
        title = deck.clean(lead).rstrip(".")
        rest = sents[1:]
    chunks = [rest[i:i + 3] for i in range(0, len(rest), 3)] or [[]]
    for k, chunk in enumerate(chunks):
        body = "\n".join(f"- {deck.clean(s)}" for s in chunk)
        deck.slide(title if k == 0 else f"{title} *(cont.)*", body,
                   kicker=kicker, note=text if k == 0 else "")


def _planned_slide(deck: Deck, kicker: str, section: sp.Section,
                   item: dict) -> None:
    title = item.get("title") or section.heading
    layout = item.get("layout", "default")
    note = item.get("note", "")
    body_parts: list[str] = []

    if item.get("lead"):
        body_parts.append(div("lead", wrap(deck.clean(item["lead"]))))

    if layout == "terms" and item.get("terms"):
        cells = [(deck.clean(t["term"]), deck.clean(t["definition"]))
                 for t in item["terms"]]
        body_parts.append(deck.grid(
            "terms two" if len(cells) > 3 else "terms", "term", cells))

    if item.get("bullets"):
        body_parts.append("\n".join(f"- {deck.clean(b)}"
                                    for b in item["bullets"]))

    if item.get("quote"):
        body_parts.append(div("note-card", wrap(deck.clean(item["quote"]))))

    if item.get("table"):
        body_parts.append(deck.clean(item["table"]))

    fig = item.get("figure")
    if fig:
        # The chapter's own block is authoritative for the path: a plan may
        # name the figure by basename or by a differently-rooted path, and
        # only the block knows how the chapter actually writes it.
        block = next((b for b in section.all("figure")
                      if Path(b.src).name == Path(fig).name), None)
        # On a slide, the plan's own lines ARE the caption. Printing the
        # chapter's caption underneath as well says the same thing twice and
        # costs the figure the height it needs to stay legible from the back
        # of a room; the book page keeps its caption either way.
        caption = block.caption if block else ""
        if item.get("bullets") or item.get("lead"):
            caption = ""
        body_parts.append(deck.figure(block.src if block else fig, caption,
                                      item.get("width", "70%")))

    if item.get("mermaid") is not None:
        blocks = section.all("mermaid")
        idx = int(item["mermaid"])
        if idx < len(blocks):
            body_parts.append(f"```{{mermaid}}\n{blocks[idx].text}\n```")

    if item.get("code") is not None:
        blocks = section.all("code")
        idx = int(item["code"])
        if idx < len(blocks):
            body_parts.append(f"```{blocks[idx].lang}\n{blocks[idx].text}\n```")

    cls = ".columns-2" if layout == "two-col" else ""
    deck.slide(title, "\n\n".join(p for p in body_parts if p),
               kicker=kicker, note=note, classes=cls)


# -------------------------------------------------------- chapter block
def chapter_slides(deck: Deck, lesson: dict, n_in_studio: int) -> str:
    """Every slide for one chapter. Returns the plan state for reporting."""
    page = sp.parse(BOOK / lesson["source"])
    deck.quoting(lesson["source"])
    state, plan = plan_state(lesson)
    plan_sections = (plan.get("sections") or {}) if state == "current" else {}
    display = lesson["display"]
    ch_url = f"{BOOK_URL}/{lesson['url_path']}"
    colab = ("https://colab.research.google.com/github/davi-moreira/"
             "2026F_evidence_driven_research_purdue_HONR464/blob/main/"
             f"notebooks/book/{lesson['companion']}")

    # 1. Section divider: the chapter, and what it puts on the table. It also
    #    opens the chapter in the slide menu, and every slide until the next
    #    divider is labelled with the chapter it belongs to.
    deck.divider(f"Lesson {n_in_studio} of this studio · Chapter {display}",
                 page.title, sp.decision_on_table(page),
                 menu=f"CHAPTER {display} — {page.title}")
    deck.menu_prefix = f"Ch {display} · "

    # 2. The research decision, verbatim.
    if page.lead_quote:
        deck.card("The research decision", page.lead_label or
                  "The research decision", page.lead_quote, "decision",
                  kicker=f"Chapter {display}")

    # 3. Key terms, when the chapter defines enough of them to be worth a card.
    terms = sp.key_terms(page, limit=4)
    if len(terms) >= 2:
        cells = [(t, deck.clean(d)) for t, d in terms]
        deck.slide("The words this chapter uses",
                   deck.grid("terms two" if len(cells) >= 2 else "terms",
                             "term", cells),
                   kicker=f"Chapter {display} · Key terms",
                   note="Each term is defined in the chapter on first use; "
                        "these are the definitions as the book gives them.")

    # 4. The argument, section by section.
    for section in page.sections:
        if not section.heading or section.heading.lower() in SPECIAL:
            continue
        prose_slides(deck, display, section,
                     plan_sections.get(section.heading))

    # 5. The AI failure case — the chapter's own, with its accent.
    fail = page.section("An AI failure case")
    if fail:
        paras = fail.paragraphs()
        if paras:
            deck.card("An AI failure case", "Where the tool failed",
                      paras[0].text, "failure",
                      kicker=f"Chapter {display}")
        # The remaining paragraphs say HOW it failed. They get one slide, not
        # one per paragraph: the card above already carries the scene, and a
        # six-chapter studio pays for every extra slide three times over.
        if len(paras) > 1:
            lines = []
            for extra in paras[1:]:
                lines += [s for s in sentences(extra.text)]
            deck.slide("How it failed",
                       "\n".join(f"- {deck.clean(l)}" for l in lines[:5]),
                       kicker=f"Chapter {display} · An AI failure case",
                       note="\n\n".join(b.text for b in paras[1:]))

    # 6. Do not delegate — the calls that stay human.
    dnd = sp.do_not_delegate(page)
    if dnd:
        deck.card("Do not delegate", "This stays yours", dnd.text,
                  "rule-human", kicker=f"Chapter {display}")

    # 7. It is your turn — the steps, and where to work them.
    steps = sp.iyt_steps(page)
    if steps:
        body = "\n".join(f"{i}. {deck.clean(s)}"
                         for i, s in enumerate(steps, 1))
        body += (f'\n\n::: {{.turn}}\n'
                 f'Work it in the [companion notebook]({colab}) with '
                 f'[Chapter {display}]({ch_url}) open beside it. '
                 f'Log every delegation in your AI Research Ledger.\n:::')
        deck.slide("It is your turn", body,
                   kicker=f"Chapter {display} · Your move",
                   note="The chapter's numbered steps, in the book's own "
                        "order. The AI prompts each step carries live in the "
                        "companion notebook.")
    return state


# ----------------------------------------------------------- deck build
def build_deck(studio: dict) -> tuple[str, dict[str, str]]:
    deck = Deck(studio)
    rank, title = studio["rank"], studio["title"]
    states: dict[str, str] = {}

    # ---------------------------------------------------------- opener
    deck.menu_prefix = f"Studio {rank} · "
    if studio["opener"]:
        op = sp.parse(studio["opener"])
        deck.quoting(studio["opener"])
        if op.lead_quote:
            deck.card("What you can defend when you leave",
                      op.lead_label or "The promise of this studio",
                      op.lead_quote, "decision", kicker=f"Studio {rank}")
        start = op.section("Start without a tool")
        if start:
            prose_slides(deck, None, start, None)
        ahead = op.section("The milestone ahead")
        if ahead:
            paras = ahead.paragraphs()
            # The paragraph that names THIS studio's milestone, not the next
            # studio's forward pointer that closes the section.
            here = next((b.text for b in paras
                         if "This studio closes with" in b.text), None)
            if here:
                deck.slide("The milestone ahead", wrap(deck.clean(here)),
                           kicker=f"Studio {rank}",
                           note="\n\n".join(b.text for b in paras
                                             if b.text != here))
            elif paras:
                deck.slide("The milestone ahead",
                           wrap(deck.clean(paras[0].text)),
                           kicker=f"Studio {rank}",
                           note="\n\n".join(b.text for b in paras[1:]))
        lessons_sec = op.section("The lessons in this studio")
        if lessons_sec:
            lists = lessons_sec.all("list")
            if lists:
                body = "\n".join(f"- {deck.clean(i)}" for i in lists[0].items)
                deck.slide("The lessons in this studio", body,
                           kicker=f"Studio {rank} · Road map")

    # --------------------------------------------------------- lessons
    for i, lesson in enumerate(studio["lessons"], 1):
        states[lesson["id"]] = chapter_slides(deck, lesson, i)

    # ------------------------------------------------------- milestone
    ms = studio["milestone"]
    if ms:
        mp = sp.parse(ms)
        deck.quoting(ms)
        deck.divider(f"Studio {rank} closes here", mp.title,
                     "What the lessons handed you becomes one artifact "
                     "you can defend.",
                     menu=f"MILESTONE {rank} — {mp.title}")
        deck.menu_prefix = f"M{rank} · "
        intro = mp.section("")
        if intro:
            for para in intro.paragraphs():
                if para.text.startswith("**What this milestone produces"):
                    deck.card("What this milestone produces",
                              "The artifact", para.text, "decision",
                              kicker=f"Milestone {rank}")
        bring = mp.section("What you bring")
        if bring:
            lists = bring.all("list")
            if lists:
                body = "\n".join(f"- {deck.clean(i)}" for i in lists[0].items)
                deck.slide("What you bring", body,
                           kicker=f"Milestone {rank} · Check before you start")
        practice = mp.section("The practice")
        if practice:
            lists = practice.all("list")
            if lists:
                body = "\n".join(f"{i}. {deck.clean(t)}"
                                 for i, t in enumerate(lists[0].items, 1))
                deck.slide("The practice", body,
                           kicker=f"Milestone {rank} · In the studio")
        rails = mp.section("The four rails, here")
        if rails:
            lists = rails.all("list")
            if lists:
                cells = []
                for item in lists[0].items:
                    m = re.match(r"\*\*(.+?)\*\*\s*(.*)", item, re.S)
                    t = m.group(1).rstrip(".") if m else item[:40]
                    d = m.group(2) if m else ""
                    cells.append((deck.clean(t), deck.clean(d)))
                deck.slide("The four rails, here",
                           deck.grid("rails", "rail", cells),
                           kicker=f"Milestone {rank} · Every studio, "
                                  f"these four")
        version = mp.section("A version, not a pass")
        if version:
            paras = version.paragraphs()
            if paras:
                deck.card("A version, not a pass", "How the record works",
                          paras[0].text, "note-card",
                          kicker=f"Milestone {rank}")

    # ----------------------------------------------------------- close
    ms_url = (f"{BOOK_URL}/studios/milestone{rank:02d}-{studio['id']}.html"
              if ms else "")
    op_url = f"{BOOK_URL}/studios/studio{rank:02d}-{studio['id']}.html"
    links = [f"[Studio {rank} in EDR|AI]({op_url})"]
    if ms_url:
        links.append(f"[Milestone {rank}]({ms_url})")
    links.append(f"[Verification Guide]({BOOK_URL}/verification-guide.html)")
    deck.add(f'''## The one rule {{background-color="{INK}" .divider data-menu-title="THE ONE RULE"}}

::: {{.creed}}
{CREED}
:::

::: {{.divider-line}}
AI can review AI, and a second model is a real auditor of the first. The
last decision is always human.
:::

::: {{.deck-links}}
{" · ".join(links)}
:::
''')

    header = deck_header(studio)
    body = "\n\n".join(deck.parts)
    return header + "\n" + body, deck.figs


def deck_header(studio: dict) -> str:
    rank, title = studio["rank"], studio["title"]
    lesson_ids = " ".join(l["id"] for l in studio["lessons"])
    return f'''---
# GENERATED FILE — DO NOT EDIT.
# Written by scripts/build_studio_slides.py from the EDR|AI book:
#   book/studios/studio{rank:02d}-{studio["id"]}.qmd      (the studio's promise)
#   the studio's chapters                                 (its argument)
#   book/studios/milestone{rank:02d}-{studio["id"]}.qmd   (its milestone)
# Editorial overlay: planning/BOOK_SLIDE_PLANS/<lesson-id>.yml
# Lessons on this deck: {lesson_ids}
# Edit the CHAPTER (or its plan) and rerun the script. Edits made here are
# silently reverted on the next build and fail `--check` in CI.
title: "{COURSE}"
subtitle: "Studio {rank} — {esc_yaml(title)}"
author: "Davi Moreira"
format:
  revealjs:
    theme: [default, _theme/edrai-slides.scss]
    include-in-header: _theme/head.html
    include-after-body: _theme/fit.html
    width: 1600
    height: 900
    margin: 0.07
    center: false
    slide-number: c/t
    show-slide-number: all
    transition: fade
    background-transition: fade
    transition-speed: fast
    incremental: false
    hash: true
    hash-type: number
    history: false
    progress: true
    controls: true
    controls-layout: bottom-right
    touch: true
    preview-links: auto
    link-external-newwindow: true
    logo: _theme/edrai_logo.png
    footer: "EDR|AI · Studio {rank} — {esc_yaml(title)}"
    chalkboard:
      buttons: false
    menu:
      side: left
      width: wide
      numbers: true
    code-line-numbers: false
    highlight-style: github
    fig-align: center
---
'''


# ----------------------------------------------------------------- main
def write_deck(studio: dict, check: bool) -> tuple[bool, dict[str, str]]:
    text, figs = build_deck(studio)
    out_file = studio["qmd"]

    changed = (not out_file.exists()) or out_file.read_text() != text
    if check:
        return changed, figs

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    if changed:
        out_file.write_text(text)

    if figs:
        fig_dir = OUT_ROOT / "figs"
        fig_dir.mkdir(exist_ok=True)
        for src in figs:
            source = (BOOK / src).resolve()
            if source.exists():
                shutil.copy2(source, fig_dir / Path(src).name)
    return changed, figs


def ensure_logo() -> None:
    dst = OUT_ROOT / "_theme" / "edrai_logo.png"
    src = BOOK / "images" / "edrai_logo.png"
    if src.exists() and (not dst.exists() or
                         src.read_bytes() != dst.read_bytes()):
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("studio", nargs="?", type=int,
                    help="build one studio (1-12); default: all")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any deck on disk differs from a fresh "
                         "build, or any plan is stale")
    args = ap.parse_args()

    ensure_logo()
    all_studios = studios()
    targets = [s for s in all_studios
               if args.studio is None or s["rank"] == args.studio]
    if not targets:
        raise SystemExit(f"✗ no studio {args.studio} (1-{len(all_studios)})")

    stale: list[str] = []
    unplanned: list[str] = []
    dirty: list[str] = []

    for st in targets:
        for lesson in st["lessons"]:
            state, _ = plan_state(lesson)
            if state == "stale":
                stale.append(f"{lesson['id']} (studio {st['rank']})")
            elif state == "none":
                unplanned.append(f"{lesson['id']} (studio {st['rank']})")
        changed, _ = write_deck(st, args.check)
        n = len(st["lessons"])
        mark = "≠" if changed else "="
        if changed:
            dirty.append(f"studio{st['rank']:02d}")
        print(f"  {mark} studio{st['rank']:02d} {st['title'][:44]:<46} "
              f"{n} chapter{'s' if n != 1 else ''}")

    if unplanned:
        print(f"\n  ○ {len(unplanned)} chapter(s) with no slide plan "
              f"(mechanical fallback in use)")
    if stale:
        print(f"\n  ⚠ {len(stale)} STALE slide plan(s) — the chapter moved "
              f"past the plan:")
        for s in stale:
            print(f"      {s}")

    if args.check:
        if dirty:
            print(f"\n✗ {len(dirty)} deck(s) stale on disk: "
                  f"{', '.join(dirty)}\n"
                  f"  run: .venv/bin/python scripts/build_studio_slides.py")
            raise SystemExit(1)
        if stale:
            print("\n✗ slide plans stale — revise them against the chapters "
                  "they were written for")
            raise SystemExit(1)
        print("\n✓ every deck matches the book")
        return

    print(f"\n✓ {len(targets)} deck(s) built under lecture_slides/")


if __name__ == "__main__":
    main()
