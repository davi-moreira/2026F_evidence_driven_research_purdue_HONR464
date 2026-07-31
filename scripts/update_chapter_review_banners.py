#!/usr/bin/env python3
"""update_chapter_review_banners.py — under-development banners (D26).

While EDR|AI is in its development phase, every chapter that has not yet been
through the instructor's review opens with a warning banner, in all three
editions. The single source of truth is planning/BOOK_REVIEW_STATUS.yml: when
Davi reports a chapter reviewed, flip its `reviewed:` flag there, rerun this
script, and re-render the books — the banner disappears from that chapter in
every edition. Idempotent in both directions (inserts where missing, removes
where reviewed, rewrites nothing else).

Usage: .venv/bin/python scripts/update_chapter_review_banners.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / "planning" / "BOOK_REVIEW_STATUS.yml"

BANNERS = {
    "book": (
        '::: {.callout-warning .review-pending title="Under development"}\n'
        "This chapter is part of a book in active development and has not yet\n"
        "been through the author's review. Content may change as the review\n"
        "advances.\n"
        ":::\n"),
    "book-pt": (
        '::: {.callout-warning .review-pending title="Em desenvolvimento"}\n'
        "Este capítulo faz parte de um livro em desenvolvimento ativo e ainda\n"
        "não passou pela revisão do autor. O conteúdo pode mudar conforme a\n"
        "revisão avança.\n"
        ":::\n"),
    "book-es": (
        '::: {.callout-warning .review-pending title="En desarrollo"}\n'
        "Este capítulo forma parte de un libro en desarrollo activo y todavía\n"
        "no ha pasado por la revisión del autor. El contenido puede cambiar a\n"
        "medida que avanza la revisión.\n"
        ":::\n"),
}

BANNER_RE = re.compile(
    r"::: \{\.callout-warning \.review-pending[^}]*\}\n.*?\n:::\n\n", re.S)
FRONT_RE = re.compile(r"\A(---\n.*?\n---\n\n?)", re.S)


# non-chapter pages that also carry the banner, keyed in the registry
EXTRA_PAGES = [("part1_overview", "part1-research-with-ai/part1-overview.qmd")]


def main() -> None:
    status = yaml.safe_load(REGISTRY.read_text())["lessons"]
    # Pages come from the identity manifest, keyed by IMMUTABLE lesson id —
    # never parsed out of a filename prefix (A10; Phase-2 critique step 2).
    arch = yaml.safe_load((REPO / "planning" / "BOOK_ARCHITECTURE.yml").read_text())
    frozen = {e["root"] for e in arch.get("editions", {}).values()
              if e.get("lifecycle") == "frozen"}
    lesson_pages = [(l["id"], l["source"]) for l in arch["lessons"]
                    if l["state"] == "active"]
    added = removed = kept = 0
    for edition, banner in BANNERS.items():
        write_ok = edition not in frozen        # D36: frozen editions verify only
        pages = [(key, REPO / edition / rel)
                 for key, rel in lesson_pages + EXTRA_PAGES]
        for key, path in pages:
            if key not in status:
                sys.exit(f"✗ {path}: no entry {key} in BOOK_REVIEW_STATUS.yml")
            reviewed = bool(status[key].get("reviewed"))
            text = path.read_text()
            has = BANNER_RE.search(text) is not None
            if reviewed and has:
                if not write_ok:
                    print(f"  ⚠ {edition}/{key}: banner change needed but the "
                          f"edition is FROZEN (D36) — deferred to the "
                          f"translation pass")
                    kept += 1
                    continue
                path.write_text(BANNER_RE.sub("", text, count=1))
                removed += 1
            elif not reviewed and not has:
                if not write_ok:
                    print(f"  ⚠ {edition}/{key}: banner missing but the "
                          f"edition is FROZEN (D36) — deferred")
                    kept += 1
                    continue
                m = FRONT_RE.match(text)
                if not m:
                    sys.exit(f"✗ {path}: no YAML front matter to anchor banner")
                insert_at = m.end()
                body = text[insert_at:].lstrip("\n")
                path.write_text(text[:m.end(1)].rstrip("\n") + "\n\n"
                                + banner + "\n" + body)
                added += 1
            else:
                kept += 1
    reviewed_n = sum(1 for v in status.values() if v.get("reviewed"))
    print(f"✓ review banners: {added} added, {removed} removed, {kept} unchanged "
          f"({reviewed_n}/37 chapters marked reviewed)")


if __name__ == "__main__":
    main()
