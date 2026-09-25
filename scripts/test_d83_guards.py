#!/usr/bin/env python3
"""test_d83_guards.py — negative tests for the two D83 course-isolation guards.

Proves, without touching a tracked file, that:

  A. SLIDE OMISSIONS (build_studio_slides.py / validate_slide_sync.py)
     1. a renamed `omit:` heading on a STALE plan makes the builder exit
        nonzero in both modes (build and --check) with every deck byte,
        on disk and in a scratch copy, unchanged;
     2. the validator reports the same defect through the shared helper;
     3. a stale plan whose omitted heading still resolves keeps that
        section off the deck (and the section does reach the deck when the
        omission is removed, so the test can fail).

  B. BOOK_MAP (build_book_map.py)
     4. every explicitly not-adopted lesson renders as "— (book only)";
     5. removing an adopted lesson's home anchor makes render() fail and
        makes --check return 1, even when the projection on disk already
        carries the erroneous marker.

Every mutation is in memory or in a temporary directory; the real plans,
crosswalk, decks and BOOK_MAP are only read.

    .venv/bin/python scripts/test_d83_guards.py      # exit 0 = all pass
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import build_book_map as bbm                                    # noqa: E402
import build_studio_slides as bss                               # noqa: E402
import validate_slide_sync as vss                               # noqa: E402
from book_manifest import not_adopted_ids                       # noqa: E402

LESSON = "observational-causal"
HEADING = "Process tracing: causal inference inside one case"
RENAMED = "Process tracing in one case"
STALE = "0" * 64

passed = failed = 0


def check(ok: bool, label: str) -> None:
    global passed, failed
    if ok:
        passed += 1
        print(f"  ✓ {label}")
    else:
        failed += 1
        print(f"  ✗ {label}")


def digest_tree(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


@contextlib.contextmanager
def patched_plan(mutate):
    """Serve a mutated copy of LESSON's plan to builder and validator."""
    real = bss.load_plan
    plan = mutate(copy.deepcopy(real(LESSON)))

    def fake(lesson_id: str) -> dict:
        return copy.deepcopy(plan) if lesson_id == LESSON else real(lesson_id)

    bss.load_plan = vss.load_plan = fake
    try:
        yield plan
    finally:
        bss.load_plan = vss.load_plan = real


def run_main(fn, argv: list[str]) -> tuple[int, str]:
    old, buf = sys.argv, io.StringIO()
    sys.argv = argv
    code = 0
    try:
        with contextlib.redirect_stdout(buf):
            ret = fn()
            code = ret if isinstance(ret, int) else 0
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 1
    finally:
        sys.argv = old
    return code, buf.getvalue()


def studio_of(lesson_id: str) -> dict:
    return next(s for s in bss.studios()
                if any(l["id"] == lesson_id for l in s["lessons"]))


# --------------------------------------------------------------- A. slides
def test_slides() -> None:
    print("A. slide-plan omissions")
    real_before = digest_tree(REPO / "lecture_slides")

    def renamed(p):
        p["source_sha256"] = STALE
        p["omit"] = [RENAMED if h == HEADING else h for h in p["omit"]]
        return p

    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp) / "lecture_slides"
        shutil.copytree(REPO / "lecture_slides", scratch)
        before = digest_tree(scratch)
        real_out = bss.OUT_ROOT
        bss.OUT_ROOT = scratch               # studios() derives qmd paths
        try:
            with patched_plan(renamed):
                for argv in (["build_studio_slides.py"],
                             ["build_studio_slides.py", "--check"],
                             ["build_studio_slides.py", "5"]):
                    code, out = run_main(bss.main, argv)
                    check(code != 0 and "invalid slide-plan omission" in out,
                          f"builder {' '.join(argv[1:]) or '(write)'} exits "
                          f"{code} on a renamed omission")
                check(digest_tree(scratch) == before,
                      "scratch deck bytes unchanged after the refused builds")

                code, out = run_main(vss.main, ["validate_slide_sync.py"])
                check(code != 0 and f"omit {RENAMED!r} is not an exact" in out,
                      "validator reports the renamed omission")
        finally:
            bss.OUT_ROOT = real_out
    check(digest_tree(REPO / "lecture_slides") == real_before,
          "real lecture_slides/ untouched")

    # A stale plan with a VALID omission still keeps the section off.
    def stale_valid(p):
        p["source_sha256"] = STALE
        return p

    def stale_no_omit(p):
        p["source_sha256"] = STALE
        p.pop("omit", None)
        return p

    marker = HEADING.split(":")[0]           # the heading as a deck kicker
    with patched_plan(stale_valid):
        text, _ = bss.build_deck(studio_of(LESSON))
    check(marker not in text,
          "stale plan with a resolving omission keeps the section off")
    with patched_plan(stale_no_omit):
        text, _ = bss.build_deck(studio_of(LESSON))
    check(marker in text,
          "sensitivity: without the omission the section reaches the deck")


# ------------------------------------------------------------- B. BOOK_MAP
def test_book_map() -> None:
    print("B. BOOK_MAP course mappings")
    fresh = bbm.render()
    n_only = sum(1 for line in fresh.splitlines()
                 if line.endswith("| — (book only) |"))
    check(n_only == len(not_adopted_ids()) and n_only > 0,
          f"{n_only} explicitly not-adopted lesson(s) render as book only")

    cw = yaml.safe_load(bbm.CW.read_text())
    victim = None
    for row in cw["rows"]:
        for a in row.get("assignments", []):
            if a.get("home_anchor") and victim is None:
                victim = a["lesson"]
                a["home_anchor"] = False
    real_cw, real_out = bbm.CW, bbm.OUT
    with tempfile.TemporaryDirectory() as tmp:
        bbm.CW = Path(tmp) / "COURSE_BOOK_CROSSWALK.yml"
        bbm.CW.write_text(yaml.safe_dump(cw, sort_keys=False))
        # the erroneous projection a lenient generator would have written
        wrong = []
        for line in fresh.splitlines():
            cells = line.split(" | ")
            if line.startswith("| ") and len(cells) == 4 and \
                    cells[1].strip() == "1":
                line = " | ".join(cells[:3] + ["— (book only) |"])
            wrong.append(line)
        bbm.OUT = Path(tmp) / "BOOK_MAP.md"
        bbm.OUT.write_text("\n".join(wrong) + "\n")
        try:
            try:
                bbm.render()
                check(False, f"render() fails when {victim} loses its anchor")
            except bbm.MappingError as exc:
                check(victim in str(exc),
                      f"render() fails when {victim} loses its anchor")
            code, out = run_main(bbm.main, ["build_book_map.py", "--check"])
            check(code == 1 and "missing course mapping" in out,
                  "--check returns 1 even with the wrong marker on disk")
        finally:
            bbm.CW, bbm.OUT = real_cw, real_out


def main() -> int:
    test_slides()
    test_book_map()
    print(f"\n{'✓' if not failed else '✗'} {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
