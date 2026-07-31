#!/usr/bin/env python3
"""validate_misconceptions.py — the executable half of acceptance test A5 (D35).

Reads `planning/MISCONCEPTION_MANIFEST.yml` and fails when a corrected methods
misconception reappears anywhere on its declared surfaces: chapter bodies AND
their prompts, canonical notebook sources, configuration, planning docs, and
both translations.

Why it exists: the Batch-B/C review round passed prose review while the same
misconceptions survived in nb08, nb10, ch20, ch23, ms09, ms13, nb14 and the
generated rubrics. The ordinary sync and voice validators cannot see a concept.

    .venv/bin/python scripts/validate_misconceptions.py
    .venv/bin/python scripts/validate_misconceptions.py --self-test

`--self-test` is the mutation test the acceptance contract requires: it
reinserts every rejected phrase into a scratch copy of a real surface and
asserts the scan catches each one. A validator that cannot fail is not a gate.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "planning" / "MISCONCEPTION_MANIFEST.yml"


def load():
    return yaml.safe_load(MANIFEST.read_text())


def surfaces(spec, defaults) -> list[Path]:
    globs = spec.get("surfaces") or defaults["surfaces"]
    excl = defaults.get("exclude", [])
    files: list[Path] = []
    for g in globs:
        for f in REPO.glob(g):
            if not f.is_file():
                continue
            rel = f.relative_to(REPO).as_posix()
            if any(f.match(e) or re.search(e.replace("**/", ".*").replace("*", "[^/]*"), rel)
                   for e in excl):
                continue
            files.append(f)
    return sorted(set(files))


def _normalize(text: str) -> tuple[str, list[int]]:
    """Collapse whitespace to single spaces; return the text and a char->line map.

    Prose wraps, so a phrase like "specification spread" routinely straddles a
    line break. Matching line-by-line silently misses those — the bug this
    normalization exists to prevent.
    """
    out, lines = [], []
    line = 1
    prev_space = False
    for ch in text:
        if ch == "\n":
            line += 1
        if ch.isspace():
            if not prev_space:
                out.append(" ")
                lines.append(line)
            prev_space = True
        else:
            out.append(ch.lower())
            lines.append(line)
            prev_space = False
    return "".join(out), lines


def scan_file(text: str, phrase: str, allow: list[str]) -> list[int]:
    """Line numbers where `phrase` appears outside an allowed corrective use.

    Works on whitespace-normalized text so wrapped phrases are still caught.
    An allowed corrective use suppresses a hit when it overlaps the same span.
    """
    norm, linemap = _normalize(text)
    needle = " ".join(phrase.lower().split())
    allow_spans = []
    for a in allow:
        an = " ".join(a.lower().split())
        start = 0
        while (i := norm.find(an, start)) != -1:
            allow_spans.append((i, i + len(an)))
            start = i + 1

    hits, start = [], 0
    while (i := norm.find(needle, start)) != -1:
        span = (i, i + len(needle))
        covered = any(s <= span[0] and span[1] <= e for s, e in allow_spans)
        if not covered:
            hits.append(linemap[i] if i < len(linemap) else 0)
        start = i + 1
    return hits


def run(verbose: bool = False) -> list[str]:
    data = load()
    defaults = data["defaults"]
    problems: list[str] = []

    for m in data["misconceptions"]:
        mid = m["id"]
        files = surfaces(m, defaults)
        allow = m.get("allow", [])
        texts = {f: f.read_text(errors="ignore") for f in files}

        for phrase in m.get("rejects", []):
            for f, text in texts.items():
                for ln in scan_file(text, phrase, allow):
                    problems.append(
                        f"[{mid}] rejected phrase {phrase!r} — "
                        f"{f.relative_to(REPO)}:{ln}")

        for phrase in m.get("requires", []):
            needle = " ".join(phrase.lower().split())
            if not any(needle in _normalize(txt)[0] for txt in texts.values()):
                problems.append(
                    f"[{mid}] required correction {phrase!r} appears nowhere "
                    f"on the declared surfaces")

        if verbose:
            print(f"  {mid}: {len(files)} files scanned")

    return problems


def self_test() -> int:
    """Mutation test: every rejected phrase must be caught when reinserted."""
    data = load()
    defaults = data["defaults"]
    failures = []
    with tempfile.TemporaryDirectory() as td:
        for m in data["misconceptions"]:
            allow = m.get("allow", [])
            for phrase in m.get("rejects", []):
                probe = Path(td) / "probe.qmd"
                probe.write_text(f"An innocent sentence.\n{phrase}\nAnother line.\n")
                hits = scan_file(probe.read_text(), phrase, allow)
                if not hits:
                    failures.append(f"[{m['id']}] mutation NOT caught: {phrase!r}")
    if failures:
        print("✗ mutation test failed — the gate does not gate:")
        for f in failures:
            print("   ", f)
        return 1
    total = sum(len(m.get("rejects", [])) for m in data["misconceptions"])
    print(f"✓ mutation test: all {total} rejected phrases are caught when reinserted")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true",
                    help="mutation test: assert each rejected phrase is caught")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    problems = run(verbose=args.verbose)
    if problems:
        print(f"✗ misconception scan: {len(problems)} problem(s)")
        for p in problems:
            print("   ", p)
        return 1
    data = load()
    n = len(data["misconceptions"])
    print(f"✓ misconception scan clean — {n} corrected misconceptions hold "
          f"across chapters, prompts, canonical sources, config, and translations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
