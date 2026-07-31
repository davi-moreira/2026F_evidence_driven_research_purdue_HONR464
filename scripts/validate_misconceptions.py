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
import json
import re
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "planning" / "MISCONCEPTION_MANIFEST.yml"


def load():
    return yaml.safe_load(MANIFEST.read_text())


_TEXT_CACHE: dict[tuple, str] = {}


def read_surface(f: Path) -> str:
    """Text of a surface. Notebooks are JSON, so pull the cell sources out.

    Generated notebooks and rubrics carry the same prose as their canonical
    sources and — unlike `_production_kit/`, which is gitignored — they ARE
    tracked, so they are what a fresh CI checkout can actually read.
    """
    key = (f, f.stat().st_mtime_ns, f.stat().st_size)
    if key in _TEXT_CACHE:
        return _TEXT_CACHE[key]
    raw = f.read_text(errors="ignore")
    if f.suffix != ".ipynb":
        _TEXT_CACHE[key] = raw
        return raw
    try:
        nb = json.loads(raw)
    except json.JSONDecodeError:
        _TEXT_CACHE[key] = raw
        return raw
    out = []
    for cell in nb.get("cells", []):
        src = cell.get("source", "")
        out.append(src if isinstance(src, str) else "".join(src))
    text = "\n".join(out)
    _TEXT_CACHE[key] = text
    return text


def surfaces(spec, defaults) -> tuple[list[Path], list[str]]:
    """Resolve globs to files, and report any REQUIRED glob that matched none.

    Fail-closed: a glob that silently matches zero files is how a gate reports
    "clean" about material it never opened (round-3 finding R3-7).
    """
    groups = spec.get("surfaces") or defaults["surfaces"]
    excl = defaults.get("exclude", [])
    files: list[Path] = []
    empty: list[str] = []
    for entry in groups:
        g = entry["glob"] if isinstance(entry, dict) else entry
        required = entry.get("required", False) if isinstance(entry, dict) else False
        matched = []
        for f in REPO.glob(g):
            if not f.is_file():
                continue
            rel = f.relative_to(REPO).as_posix()
            if any(f.match(e) or re.search(e.replace("**/", ".*").replace("*", "[^/]*"), rel)
                   for e in excl):
                continue
            matched.append(f)
        if required and not matched:
            empty.append(g)
        files.extend(matched)
    return sorted(set(files)), empty


_NORM_CACHE: dict[int, tuple[str, list[int]]] = {}


def _normalize(text: str) -> tuple[str, list[int]]:
    """Collapse whitespace to single spaces; return the text and a char->line map.

    Prose wraps, so a phrase like "specification spread" routinely straddles a
    line break. Matching line-by-line silently misses those — the bug this
    normalization exists to prevent.
    """
    ck = hash(text)
    if ck in _NORM_CACHE:
        return _NORM_CACHE[ck]
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
    res = ("".join(out), lines)
    _NORM_CACHE[ck] = res
    return res


def _allow_spans(norm: str, allow: list[str]) -> list[tuple[int, int]]:
    spans = []
    for a in allow:
        an = " ".join(a.lower().split())
        start = 0
        while (i := norm.find(an, start)) != -1:
            spans.append((i, i + len(an)))
            start = i + 1
    return spans


def scan_file(text: str, phrase: str, allow: list[str]) -> list[int]:
    """Line numbers where `phrase` appears outside an allowed corrective use.

    Works on whitespace-normalized text so wrapped phrases are still caught.
    An allowed corrective use suppresses a hit when it overlaps the same span.
    """
    norm, linemap = _normalize(text)
    needle = " ".join(phrase.lower().split())
    allow_spans = _allow_spans(norm, allow)

    hits, start = [], 0
    while (i := norm.find(needle, start)) != -1:
        span = (i, i + len(needle))
        covered = any(s <= span[0] and span[1] <= e for s, e in allow_spans)
        if not covered:
            hits.append(linemap[i] if i < len(linemap) else 0)
        start = i + 1
    return hits


def scan_pattern(text: str, pattern: str, allow: list[str]) -> list[int]:
    """Same as scan_file but for a regex FAMILY, not a literal phrase.

    Literal phrases only catch the wording that was already fixed. Paraphrase
    is how a misconception actually returns — "eliminates that artifact",
    "returns precisely zero", "if every specification agrees, it is robust".
    These patterns target the CLAIM, so drift is caught too.
    """
    norm, linemap = _normalize(text)
    allow_spans = _allow_spans(norm, allow)
    hits = []
    for m in re.finditer(pattern, norm):
        span = m.span()
        if any(s <= span[0] and span[1] <= e for s, e in allow_spans):
            continue
        hits.append(linemap[m.start()] if m.start() < len(linemap) else 0)
    return hits


def run(verbose: bool = False, check_nums: bool = True) -> list[str]:
    data = load()
    defaults = data["defaults"]
    problems: list[str] = []

    for m in data["misconceptions"]:
        mid = m["id"]
        files, empty = surfaces(m, defaults)
        for g in empty:
            problems.append(
                f"[{mid}] REQUIRED surface matched zero files: {g!r} — the gate "
                f"cannot certify material it never opened")
        allow = m.get("allow", [])
        texts = {f: read_surface(f) for f in files}

        for phrase in m.get("rejects", []):
            for f, text in texts.items():
                for ln in scan_file(text, phrase, allow):
                    problems.append(
                        f"[{mid}] rejected phrase {phrase!r} — "
                        f"{f.relative_to(REPO)}:{ln}")

        for pat in m.get("reject_patterns", []):
            rx, why = pat["pattern"], pat.get("why", "")
            for f, text in texts.items():
                for ln in scan_pattern(text, rx, allow):
                    problems.append(
                        f"[{mid}] rejected CLAIM ({why}) — "
                        f"{f.relative_to(REPO)}:{ln}  [/{rx}/]")

        for phrase in m.get("requires", []):
            needle = " ".join(phrase.lower().split())
            if not any(needle in _normalize(txt)[0] for txt in texts.values()):
                problems.append(
                    f"[{mid}] required correction {phrase!r} appears nowhere "
                    f"on the declared surfaces")

        if verbose:
            print(f"  {mid}: {len(files)} files scanned")

    if check_nums:
        problems.extend(check_numbers(data, verbose=verbose))
    return problems


def check_numbers(data, verbose: bool = False) -> list[str]:
    """Every numeric claim in prose must match the seeded computation.

    Round-3 finding R3-8: the manifest declared numbers and nothing read them,
    so prose could drift away from the figures without failing the build.
    """
    problems: list[str] = []
    specs = data.get("numbers", [])
    if not specs:
        return ["numbers: manifest declares no numerical claims (A5 requires them)"]

    sys.path.insert(0, str(REPO / "scripts"))
    try:
        import build_book_sim_figures as sims
    except Exception as e:                      # pragma: no cover
        return [f"numbers: cannot import the simulation module ({e})"]

    import tempfile
    cache: dict[str, dict] = {}
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        strings = sims.L["book"]
        for spec in specs:
            f = REPO / spec["file"]
            if not f.exists():
                problems.append(f"numbers[{spec['id']}]: missing file {spec['file']}")
                continue
            text, _ = _normalize(read_surface(f))
            for claim in spec["claims"]:
                fn_name, key = claim["source"].split(".", 1)
                if fn_name not in cache:
                    fn = getattr(sims, fn_name, None)
                    if fn is None:
                        problems.append(
                            f"numbers[{spec['id']}]: unknown source function "
                            f"{fn_name!r}")
                        cache[fn_name] = {}
                        continue
                    cache[fn_name] = fn(strings, out)
                stats = cache[fn_name]
                if key not in stats:
                    problems.append(
                        f"numbers[{spec['id']}]: {fn_name} returns no key {key!r} "
                        f"(has: {sorted(stats)})")
                    continue
                computed = float(stats[key])
                needle = " ".join(claim["text"].lower().split())
                if needle not in text:
                    problems.append(
                        f"numbers[{spec['id']}]: prose does not contain "
                        f"{claim['text']!r} — it may have drifted from "
                        f"{fn_name}.{key} = {computed:.4f}")
                    continue
                stated = claim.get("value", _first_number(claim["text"]))
                if stated is None:
                    continue
                tol = float(claim.get("tolerance", 0))
                if abs(stated - computed) > tol:
                    problems.append(
                        f"numbers[{spec['id']}]: prose says {stated} but "
                        f"{fn_name}.{key} computes {computed:.4f} "
                        f"(tolerance {tol})")
                elif verbose:
                    print(f"  numbers[{spec['id']}]: {claim['text']!r} == "
                          f"{computed:.4f} ✓")
    return problems


def _first_number(text: str) -> float | None:
    m = re.search(r"-?\d+(?:\.\d+)?", text.replace(",", ""))
    return float(m.group(0)) if m else None


def self_test() -> int:
    """End-to-end mutation test: route every mutation through the PRODUCTION scan.

    Round-3 finding R3-9: the earlier version wrote a synthetic probe and called
    `scan_file()` directly, so it passed even when the real scan skipped whole
    file classes or ignored every numerical assertion. It was a unit test of the
    matcher wearing a mutation test's name.

    Now each mutation is written into a REAL declared surface, `run()` is called
    exactly as production calls it, and the file is restored afterwards. It also
    verifies the three structural guarantees: a zero-match required glob fails, a
    deleted required correction fails, and drifted prose numbers fail.
    """
    data = load()
    failures: list[str] = []

    baseline = run(check_nums=False)
    if baseline:
        print("✗ self-test cannot run: the tree is not clean to begin with")
        for b in baseline[:8]:
            print("   ", b)
        return 1

    target = REPO / "book/part4-credible-evidence/22-diagnostics-and-negative-tests.qmd"
    original = target.read_text()

    def mutate_and_scan(snippet: str) -> bool:
        """True when the production scan catches the mutation."""
        target.write_text(original + "\n\n" + snippet + "\n")
        try:
            # numbers are exercised separately in guarantee 4; skipping the
            # simulations here keeps ~45 mutations from re-running them all
            return bool(run(check_nums=False))
        finally:
            target.write_text(original)

    # 1. every literal rejected phrase, through the real scan
    for m in data["misconceptions"]:
        for phrase in m.get("rejects", []):
            if not mutate_and_scan(phrase):
                failures.append(f"[{m['id']}] literal NOT caught end-to-end: {phrase!r}")

    # 2. every paraphrase drift, and every benign phrasing that must NOT fire
    for m in data["misconceptions"]:
        for pat in m.get("reject_patterns", []):
            for ex in pat.get("catches", []):
                if not mutate_and_scan(ex):
                    failures.append(f"[{m['id']}] DRIFT not caught end-to-end: {ex!r}")
            for ex in pat.get("permits", []):
                if mutate_and_scan(ex):
                    failures.append(f"[{m['id']}] FALSE POSITIVE end-to-end: {ex!r}")

    # 3. structural guarantee: a required glob matching nothing must FAIL
    mpath = MANIFEST
    manifest_src = mpath.read_text()
    try:
        mpath.write_text(manifest_src.replace(
            '{glob: "notebooks/student/*.ipynb", required: true}',
            '{glob: "notebooks/student/__none__*.ipynb", required: true}'))
        if not any("REQUIRED surface matched zero files" in p for p in run(check_nums=False)):
            failures.append("zero-match required glob did NOT fail the scan")
    finally:
        mpath.write_text(manifest_src)

    # 4. structural guarantee: a drifted prose number must FAIL
    ch14 = REPO / "book/part3-pathways/14-prediction-and-generalization.qmd"
    ch14_src = ch14.read_text()
    try:
        ch14.write_text(ch14_src.replace("0.025 RMSE on average",
                                         "0.030 RMSE on average"))
        if not any("numbers[ch14-optimism]" in p for p in run()):
            failures.append("drifted prose number did NOT fail the scan")
    finally:
        ch14.write_text(ch14_src)

    # 5. structural guarantee: deleting a required correction must FAIL
    ch21 = REPO / "book/part4-credible-evidence/21-robustness-and-sensitivity.qmd"
    ch21_src = ch21.read_text()
    try:
        ch21.write_text(ch21_src.replace("specification\nspread", "REMOVED TERM"))
        if not any("required correction" in p for p in run(check_nums=False)):
            failures.append("deleted required correction did NOT fail the scan")
    finally:
        ch21.write_text(ch21_src)

    if failures:
        print("✗ self-test failed — the gate does not gate:")
        for f in failures:
            print("   ", f)
        return 1

    lit = sum(len(m.get("rejects", [])) for m in data["misconceptions"])
    drift = sum(len(pt.get("catches", []))
                for m in data["misconceptions"] for pt in m.get("reject_patterns", []))
    permit = sum(len(pt.get("permits", []))
                 for m in data["misconceptions"] for pt in m.get("reject_patterns", []))
    print(f"✓ end-to-end mutation test: {lit} literal phrases and {drift} paraphrase "
          f"drifts caught through the production scan, {permit} benign phrasings "
          f"permitted, plus zero-match-glob, drifted-number, and deleted-correction "
          f"guarantees")
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
