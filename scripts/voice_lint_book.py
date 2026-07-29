#!/usr/bin/env python3
"""voice_lint_book.py — the mechanical half of BOOK_VOICE_POLICY (D28).

Flags the machine-detectable AI-tells in the book's prose, per edition:
banned stock phrases, vague upgrade words used as intensifiers, pivot-word
accumulation, and em-dash density. Judgment calls (contrast formulas,
synthetic endings, symmetry) stay human — see
_project_docs/BOOK_VOICE_POLICY.md.

Warnings by default so existing pre-policy chapters can be swept gradually
through the review workflow; `--strict` turns warnings into a failing exit
(use it on files you have just written or revised).

Usage:
    .venv/bin/python scripts/voice_lint_book.py [--strict] [paths...]
    (no paths: lint every .qmd in book/, book-pt/, book-es/)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

PHRASES = {
    "book": [
        "delve", "delving", "it is important to note", "it's important to note",
        "it is worth noting", "sheds light", "shed light on", "at the heart of",
        "underscores the importance", "underscoring the importance", "speaks to",
        "plays a crucial role", "plays an important role", "plays a key role",
        "a testament to", "in today's world", "in today's fast",
        "navigating the", "in the realm of", "the landscape of", "tapestry",
        "game-changer", "unlock the", "harness the", "let's dive", "dive into",
        "in conclusion", "has implications for our understanding",
        "raises broader questions", "in the context of",
    ],
    "book-pt": [
        "é importante notar", "é importante ressaltar", "vale ressaltar",
        "vale destacar", "cabe destacar", "além disso", "ademais",
        "mergulhar em", "mergulhe em", "no cenário atual", "no mundo de hoje",
        "desempenha um papel crucial", "desempenha um papel importante",
        "lançar luz sobre", "em conclusão", "um divisor de águas",
        "destravar o", "no contexto de",
    ],
    "book-es": [
        "es importante notar", "es importante destacar", "cabe destacar",
        "cabe resaltar", "cabe señalar", "además de eso", "sumergirse en",
        "en el mundo actual", "en el panorama actual",
        "desempeña un papel crucial", "desempeña un papel importante",
        "arrojar luz sobre", "en conclusión", "un punto de inflexión",
        "desbloquear el", "en el contexto de",
    ],
}

UPGRADE_WORDS = {
    "book": ["robust", "nuanced", "compelling", "striking", "crucial",
             "pivotal", "vital"],
    "book-pt": ["robusto", "robusta", "crucial", "fundamental", "vital",
                "impactante"],
    "book-es": ["robusto", "robusta", "crucial", "fundamental", "vital",
                "impactante"],
}

PIVOTS = {
    "book": ["however", "indeed", "in fact", "notably", "crucially",
             "moreover", "furthermore"],
    "book-pt": ["no entanto", "de fato", "notavelmente", "crucialmente",
                "além disso", "ademais"],
    "book-es": ["sin embargo", "de hecho", "notablemente", "crucialmente",
                "además"],
}

EMDASH_BUDGET = 20      # per file (chapters are long; the notebooks rule is 1/cell)
PIVOT_BUDGET = 8        # per file
UPGRADE_BUDGET = 4      # per file


def strip_code(text: str) -> str:
    """Remove fenced code blocks and table rows — neither is prose."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return "\n".join(l for l in text.splitlines() if not l.startswith("|"))


def lint(path: Path, edition: str) -> list[str]:
    prose = strip_code(path.read_text()).lower()
    warns = []
    for phrase in PHRASES[edition]:
        n = prose.count(phrase)
        if n:
            warns.append(f"stock phrase “{phrase}” ×{n}")
    up = sum(len(re.findall(rf"\b{re.escape(w)}\b", prose))
             for w in UPGRADE_WORDS[edition])
    if up > UPGRADE_BUDGET:
        warns.append(f"vague upgrade words ×{up} (budget {UPGRADE_BUDGET})")
    piv = sum(len(re.findall(rf"\b{re.escape(w)}\b", prose))
              for w in PIVOTS[edition])
    if piv > PIVOT_BUDGET:
        warns.append(f"pivot words ×{piv} (budget {PIVOT_BUDGET})")
    dashes = prose.count("—")
    if dashes > EMDASH_BUDGET:
        warns.append(f"em dashes ×{dashes} (budget {EMDASH_BUDGET})")
    return warns


def main() -> None:
    strict = "--strict" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--strict"]
    if args:
        targets = []
        for a in args:
            p = Path(a).resolve()
            edition = p.relative_to(REPO).parts[0]
            targets.append((p, edition))
    else:
        targets = [(p, ed) for ed in ("book", "book-pt", "book-es")
                   for p in sorted((REPO / ed).rglob("*.qmd"))
                   if not p.name.startswith("_")]

    flagged = 0
    for path, edition in targets:
        warns = lint(path, edition)
        if warns:
            flagged += 1
            rel = path.relative_to(REPO)
            print(f"⚠️  {rel}")
            for w in warns:
                print(f"    {w}")
    total = len(targets)
    if flagged:
        print(f"{'✗' if strict else '⚠️'} voice lint: {flagged}/{total} files "
              f"flagged (BOOK_VOICE_POLICY.md)")
        if strict:
            sys.exit(1)
    else:
        print(f"✓ voice lint: {total} files clean")


if __name__ == "__main__":
    main()
