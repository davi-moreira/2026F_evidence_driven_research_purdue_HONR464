#!/usr/bin/env python3
"""slide_parts.py — the ONE reader that turns EDR|AI source pages into the
structured parts a slide deck is built from.

The book is the source of truth (D20's book-first loop), so no slide text is
ever retyped from a chapter: every verbatim element a deck carries — the
research-decision thesis, the "Do not delegate" rule, the AI failure case, the
worked-example code, the milestone practice — is read out of the chapter here
and rendered by scripts/build_studio_slides.py. When a chapter is edited, the
deck changes on the next build without anyone touching the deck.

Consumers: build_studio_slides.py, validate_slide_sync.py.

What it knows how to read
-------------------------
Chapters (the 40 active lessons) are highly regular: front matter `title:`, a
`.review-pending` banner, a Colab badge, a `> **The research decision.**`
blockquote, then `## Why this decision matters` / `## The concept` /
`## A worked example` / [`## A seeded simulation`] / `## An AI failure case` /
`## It is your turn`, with a `::: {.callout-important title="Do not delegate"}`
inside the last one. Two chapters carry extra `##` sections; nothing here
assumes the canonical set — sections are read as they come.

Studio opener pages carry a `> **What you can defend when you leave.**`
promise, `## Start without a tool`, `## The milestone ahead`, and
`## The lessons in this studio`. Milestone chapters carry `## What you bring`,
`## The practice`, `## A version, not a pass`, `## The four rails, here`, and
`## Where this milestone sits`.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOOK = REPO / "book"
BIB = BOOK / "references.bib"

#: Lines that exist for the book page and never for a slide.
_BADGE = re.compile(r"^\[!\[\]\(https://colab\.research\.google\.com")
_STATION_PTR = re.compile(
    r"<!-- station-pointer:begin -->.*?<!-- station-pointer:end -->",
    re.S)


# --------------------------------------------------------------- blocks
@dataclass
class Block:
    """One parsed body element of a source page."""
    kind: str                       # para | list | code | mermaid | figure
                                    # | quote | callout | table
    text: str = ""
    lang: str = ""                  # code blocks
    items: list[str] = field(default_factory=list)   # list blocks
    src: str = ""                   # figure path, book-relative
    caption: str = ""               # figure caption
    attrs: str = ""                 # figure attributes
    title: str = ""                 # callout title
    classes: str = ""               # callout classes


@dataclass
class Section:
    heading: str
    anchor: str
    blocks: list[Block]
    raw: str = ""                   # the section body as written in the book

    def paragraphs(self) -> list[Block]:
        return [b for b in self.blocks if b.kind == "para"]

    def first(self, kind: str) -> Block | None:
        for b in self.blocks:
            if b.kind == kind:
                return b
        return None

    def all(self, kind: str) -> list[Block]:
        return [b for b in self.blocks if b.kind == kind]


@dataclass
class Page:
    path: Path
    title: str
    lead_quote: str                 # the `> **...**` thesis, label stripped
    lead_label: str                 # the bolded label of that quote
    sections: list[Section]
    digest: str

    def section(self, heading: str) -> Section | None:
        for s in self.sections:
            if s.heading.lower() == heading.lower():
                return s
        return None

    def headings(self) -> list[str]:
        return [s.heading for s in self.sections]


# ------------------------------------------------------------ citations
_BIB_CACHE: dict[str, str] | None = None


def _brace_value(body: str, field: str) -> str:
    r"""A BibTeX field's value with balanced braces.

    A non-greedy `\{(.+?)\}` stops at the FIRST closing brace, which for a
    corporate author written `{{National Academies of Sciences, Engineering,
    and Medicine}}` returns `{National Academies …` — a stray brace that then
    reached the slide. Braces are counted instead.
    """
    m = re.search(rf"{field}\s*=\s*", body)
    if not m:
        return ""
    i = m.end()
    if i >= len(body) or body[i] != "{":
        return body[i:].split(",")[0].strip()
    depth, out = 0, []
    while i < len(body):
        c = body[i]
        if c == "{":
            depth += 1
            if depth == 1:
                i += 1
                continue
        elif c == "}":
            depth -= 1
            if depth == 0:
                break
        out.append(c)
        i += 1
    return "".join(out)


def _split_authors(field: str) -> list[str]:
    """Split a BibTeX author list on ` and ` at brace depth 0 only.

    `{{International Committee of Medical Journal Editors}}` is ONE author,
    and the "and" inside it is part of the name, not a separator.
    """
    parts, depth, cur = [], 0, ""
    i = 0
    while i < len(field):
        c = field[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        if depth == 0 and field[i:i + 5].lower() == " and ":
            parts.append(cur)
            cur = ""
            i += 5
            continue
        cur += c
        i += 1
    if cur.strip():
        parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def _surname(name: str) -> str:
    """The name a reader recognises: a family name, or a corporate name whole."""
    # BibTeX writes an en dash as `--`; a slide is not TeX, so normalize it.
    name = name.replace("---", "\u2014").replace("--", "\u2013").strip()
    if name.startswith("{") and name.endswith("}"):
        return name[1:-1].strip()          # corporate author: never abbreviated
    if "," in name:
        return name.split(",")[0].strip()
    return name.split()[-1] if name.split() else name


def _bib() -> dict[str, str]:
    """citation key -> a short human mark, e.g. 'Zahavy 2026'.

    A key missing from references.bib is deliberately NOT invented: the raw
    `[@key]` survives into the deck so audit_sources.py still sees it.
    """
    global _BIB_CACHE
    if _BIB_CACHE is not None:
        return _BIB_CACHE
    out: dict[str, str] = {}
    if BIB.exists():
        for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", BIB.read_text(), re.S):
            key, body = m.group(1).strip(), m.group(2)
            author = _brace_value(body, "author") or _brace_value(body, "editor")
            yr = re.search(r"year\s*=\s*\{?(\d{4})", body)
            if not (author and yr):
                continue
            names = [_surname(n) for n in _split_authors(author)]
            if not names:
                continue
            if len(names) == 1:
                who = names[0]
            elif len(names) == 2:
                who = f"{names[0]} & {names[1]}"
            else:
                who = f"{names[0]} et al."
            out[key] = f"{who} {yr.group(1)}"
    _BIB_CACHE = out
    return out


def resolve_citations(text: str) -> str:
    """`[@key]`/`[@a; @b]` -> `(Zahavy 2026)`, using the book's own .bib."""
    bib = _bib()

    def one(m: re.Match) -> str:
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        marks = [bib.get(k) for k in keys]
        if not all(marks):
            return m.group(0)          # unknown key: leave it for the audit
        return "(" + "; ".join(marks) + ")"

    text = re.sub(r"\[((?:@[\w:.-]+)(?:\s*;\s*@[\w:.-]+)*)\]", one, text)
    return re.sub(r"(?<!\[)@([\w:.-]{4,})",
                  lambda m: f"({bib[m.group(1)]})" if m.group(1) in bib
                  else m.group(0), text)


# ----------------------------------------------------------- link fixing
def to_site_links(text: str, book_url: str, from_dir: str = "") -> str:
    """Rewrite in-book `.qmd` links to published `.html` URLs under `book_url`.

    A deck lives at lecture_slides/<deck>/ and is served from the same site as
    the book, so every relative in-book link has to become absolute or it 404s
    from the deck's directory. `from_dir` is the linking page's own directory,
    book-relative (e.g. "studios"), because `milestone01-x.qmd` written inside
    book/studios/ means book/studios/milestone01-x.html — not book/.
    """
    def one(m: re.Match) -> str:
        label, href = m.group(1), m.group(2)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        base = href.split("#")[0]
        anchor = href[len(base):]
        parts = [p for p in (from_dir.split("/") if from_dir else []) if p]
        for seg in base.split("/"):
            if seg in ("", "."):
                continue
            if seg == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(seg)
        rel = "/".join(parts).replace(".qmd", ".html")
        return f"[{label}]({book_url}/{rel}{anchor})"

    return re.sub(r"\[([^\]]*)\]\(([^)]+)\)", one, text)


def clean(text: str, book_url: str, from_dir: str = "") -> str:
    """Every prose transform a slide needs, in one call."""
    return to_site_links(resolve_citations(text), book_url, from_dir).strip()


# --------------------------------------------------------------- parser
def _fm_title(raw: str) -> str:
    """The page's published title.

    A `title:` in the front matter wins. Failing that, the first `# ` heading
    of the BODY — never of the front matter, which on generated pages opens
    with a `# GENERATED FILE - DO NOT EDIT.` comment that is not a title.
    """
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', raw, re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r"^#\s+(.+?)(?:\s*\{[^}]*\})?\s*$",
                  _strip_front_matter(raw), re.M)
    return m.group(1).strip() if m else ""


def _strip_front_matter(raw: str) -> str:
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            return raw[end + 4:]
    return raw


def _split_callouts(body: str) -> str:
    """Drop the review-pending banner; keep every other fenced div intact."""
    return re.sub(
        r"::: \{\.callout-warning \.review-pending[^}]*\}.*?\n:::\n",
        "", body, flags=re.S)


def _parse_blocks(chunk: str) -> list[Block]:
    """One section body -> ordered blocks."""
    blocks: list[Block] = []
    lines = chunk.split("\n")
    i, n = 0, len(lines)
    buf: list[str] = []

    def flush() -> None:
        nonlocal buf
        text = "\n".join(buf).strip()
        buf = []
        if not text:
            return
        # A run of "- " or "1. " lines is a list, not a paragraph.
        ls = [l for l in text.split("\n") if l.strip()]
        if ls and all(re.match(r"^\s*(?:[-*]|\d+\.)\s+", l) for l in ls):
            items, cur = [], ""
            for l in text.split("\n"):
                if re.match(r"^\s*(?:[-*]|\d+\.)\s+", l):
                    if cur:
                        items.append(cur.strip())
                    cur = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", l)
                elif l.strip():
                    cur += " " + l.strip()
            if cur:
                items.append(cur.strip())
            blocks.append(Block(kind="list", items=items, text=text))
        elif text.startswith("|") and "\n|" in text:
            blocks.append(Block(kind="table", text=text))
        else:
            blocks.append(Block(kind="para", text=text))

    while i < n:
        line = lines[i]

        if _BADGE.match(line):
            i += 1
            continue

        # fenced code / mermaid
        m = re.match(r"^```+\s*(\{?[\w.-]*\}?)\s*$", line)
        if m and line.startswith("```"):
            flush()
            fence = re.match(r"^(`{3,})", line).group(1)
            lang = m.group(1).strip("{}")
            body, i = [], i + 1
            while i < n and not lines[i].startswith(fence):
                body.append(lines[i])
                i += 1
            i += 1
            kind = "mermaid" if lang == "mermaid" else "code"
            blocks.append(Block(kind=kind, lang=lang or "text",
                                text="\n".join(body)))
            continue

        # fenced div (callout / column layout)
        if line.startswith(":::") and re.match(r"^:::+\s*\{", line):
            flush()
            opener = re.match(r"^(:+)\s*\{(.*)\}\s*$", line)
            marks = opener.group(1)
            attrs = opener.group(2)
            depth, body, i = 1, [], i + 1
            while i < n and depth:
                if re.match(rf"^{marks}\s*\{{", lines[i]):
                    depth += 1
                elif re.match(rf"^{marks}\s*$", lines[i]):
                    depth -= 1
                    if not depth:
                        break
                body.append(lines[i])
                i += 1
            i += 1
            t = re.search(r'title="([^"]*)"', attrs)
            blocks.append(Block(kind="callout", text="\n".join(body).strip(),
                                title=t.group(1) if t else "",
                                classes=attrs))
            continue

        # standalone figure. The caption and the attribute block routinely
        # wrap across lines in the book sources, so the whole image is read
        # by joining lines until its attributes close.
        if line.lstrip().startswith("!["):
            j, joined = i, ""
            while j < n:
                joined = (joined + " " + lines[j].strip()).strip()
                if re.fullmatch(r"!\[.*?\]\(.+?\)(\{.*\})?", joined, re.S):
                    break
                if not lines[j].strip() or j - i > 12:
                    joined = ""
                    break
                j += 1
            fm = re.fullmatch(r"!\[(.*?)\]\((.+?)\)(\{.*\})?", joined, re.S) \
                if joined else None
            if fm:
                flush()
                blocks.append(Block(kind="figure",
                                    caption=re.sub(r"\s+", " ",
                                                   fm.group(1)).strip(),
                                    src=fm.group(2).strip(),
                                    attrs=fm.group(3) or ""))
                i = j + 1
                continue

        # blockquote run
        if line.startswith(">"):
            flush()
            q: list[str] = []
            while i < n and lines[i].startswith(">"):
                q.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            blocks.append(Block(kind="quote", text="\n".join(q).strip()))
            continue

        if not line.strip():
            flush()
            i += 1
            continue

        buf.append(line)
        i += 1

    flush()
    return blocks


def _anchor(heading: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")


def parse(path: Path) -> Page:
    """Read one EDR|AI source page into its structured parts."""
    raw = path.read_text()
    digest = hashlib.sha256(raw.encode()).hexdigest()
    title = _fm_title(raw)
    body = _strip_front_matter(raw)
    body = _STATION_PTR.sub("", body)
    body = _split_callouts(body)
    # A milestone chapter opens with `# Title {.unnumbered}`, which is its
    # title and not content. Strip ONLY that: a `# ` line further down is a
    # comment inside a code block, and deleting it silently removed the line a
    # speaker note told the instructor to point at.
    head_lines = []
    for line in body.split("\n"):
        head_lines.append(line)
        if line.strip():
            break
    lead = "\n".join(head_lines)
    if re.match(r"^#\s+\S", lead.strip()):
        body = body.replace(lead.strip(), "", 1)

    # The lead thesis quote: the first `> **Label.** ...` run before any `##`.
    lead_label = lead_quote = ""
    head = body.split("\n## ", 1)[0]
    lq = re.search(r"((?:^>.*\n?)+)", head, re.M)
    if lq:
        q = re.sub(r"^>\s?", "", lq.group(1), flags=re.M).strip()
        lm = re.match(r"\*\*(.+?)\*\*\s*(.*)", q, re.S)
        if lm:
            lead_label, lead_quote = lm.group(1).rstrip("."), lm.group(2).strip()
        else:
            lead_quote = q
        head = head.replace(lq.group(1), "")

    sections: list[Section] = []
    intro = head.strip()
    if intro:
        sections.append(Section("", "", _parse_blocks(intro), intro))

    parts = re.split(r"^## +(.+?)\s*$", body, flags=re.M)
    for j in range(1, len(parts), 2):
        h = re.sub(r"\s*\{[^}]*\}\s*$", "", parts[j]).strip()
        sections.append(Section(h, _anchor(h),
                                _parse_blocks(parts[j + 1]), parts[j + 1]))

    return Page(path=path, title=title, lead_quote=lead_quote,
                lead_label=lead_label, sections=sections, digest=digest)


# ------------------------------------------------- chapter conveniences
def decision_on_table(page: Page) -> str:
    """The chapter's one-line stake, from `**The decision on the table: ...**`."""
    s = page.section("Why this decision matters")
    if not s:
        return ""
    for b in s.paragraphs():
        m = re.search(r"\*\*The decision on the table:\s*(.+?)\*\*",
                      b.text, re.S)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip().rstrip(".")
    return ""


def do_not_delegate(page: Page) -> Block | None:
    """The chapter's `Do not delegate` callout, wherever it sits."""
    for s in page.sections:
        for b in s.all("callout"):
            if "do not delegate" in b.title.lower():
                return b
    return None


def s_raw(section: Section) -> str:
    """A section rebuilt as plain text: code fences and callouts dropped.

    Embedded ```text blocks are AI prompts a reader copies into a tool. They
    belong in the companion notebook, never on a slide.
    """
    return "\n\n".join(b.text for b in section.blocks
                        if b.kind in ("para", "list", "quote", "table"))


def iyt_steps(page: Page) -> list[str]:
    """The numbered steps of `It is your turn`, one lead sentence each.

    A step runs across several paragraphs and usually wraps a fenced AI
    prompt, so the steps are read from the section's RAW text: top-level
    `N. ` lines, everything indented under them belonging to that step. The
    prompt itself is notebook material and never reaches a slide.
    """
    s = page.section("It is your turn")
    if not s:
        return []
    body = re.sub(r"```.*?```", "", s.raw, flags=re.S)     # drop prompts
    body = re.sub(r"::: \{.*?\n:::", "", body, flags=re.S)  # drop callouts
    steps: list[str] = []
    for m in re.finditer(r"^(\d+)\.[ \t]+(.+?)(?=^\d+\.[ \t]|\Z)",
                         body, re.M | re.S):
        lead = re.split(r"\n[ \t]*\n", m.group(2).strip())[0]
        lead = re.sub(r"\s+", " ", lead).strip()
        # First sentence only: a slide names the move, the notebook carries it.
        first = re.split(r"(?<=[.!?])\s+(?=[A-Z(])", lead)[0]
        steps.append(first.strip())
    return steps


def key_terms(page: Page, limit: int = 6) -> list[tuple[str, str]]:
    """`**Term**` + its one-sentence definition, from the concept sections.

    The book's D14 rule guarantees the shape: bold term, then a plain-language
    definition in the same sentence. Only that shape is harvested; a bold run
    used for emphasis is skipped.
    """
    terms: list[tuple[str, str]] = []
    seen: set[str] = set()
    for s in page.sections:
        if s.heading.lower() in ("it is your turn", "an ai failure case"):
            continue
        for b in s.paragraphs():
            flat = re.sub(r"\s+", " ", b.text)
            for m in re.finditer(
                    r"\*\*([A-Z][^*]{2,44}?)\*\*[,]?\s+"
                    r"(is|are|means|meaning|refers to|describes|asks)\s+"
                    r"([^.]{15,200}\.)", flat):
                term = m.group(1).strip().rstrip(":,")
                if term.lower() in seen or " " in term and len(term) > 34:
                    continue
                seen.add(term.lower())
                # Drop the copula: the card sets the term on its own line, so
                # "Abduction / is proposing ..." reads as a fragment.
                definition = m.group(3).strip()
                if m.group(2) in ("asks", "describes", "refers to"):
                    definition = f"{m.group(2)} {definition}"
                terms.append((term, definition[0].lower() + definition[1:]
                              if definition else definition))
                if len(terms) >= limit:
                    return terms
    return terms


def digest_of(rel: str) -> str:
    return hashlib.sha256((BOOK / rel).read_bytes()).hexdigest()
