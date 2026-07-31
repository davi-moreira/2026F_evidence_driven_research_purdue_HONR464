#!/usr/bin/env python3
"""validate_misconceptions.py — the executable half of acceptance test A5 (D35).

Reads `planning/MISCONCEPTION_MANIFEST.yml` and fails when a corrected methods
misconception reappears anywhere on its declared surfaces: chapter bodies AND
their prompts, canonical notebook sources, configuration, planning docs, and
both translations.

Why it exists: the Batch-B/C review round passed prose review while the same
misconceptions survived in nb08, nb10, ch20, ch23, ms09, ms13, nb14 and the
generated rubrics. The ordinary sync and voice validators cannot see a concept.

    .venv/bin/python scripts/validate_misconceptions.py              # public surfaces
    .venv/bin/python scripts/validate_misconceptions.py --local      # + canonical sources,
                                                                     #   instructor notebooks,
                                                                     #   staleness check
    .venv/bin/python scripts/validate_misconceptions.py --self-test  # mutation test

HONESTY (round-4 finding G2): the default mode certifies ONLY tracked public
surfaces — what a fresh CI checkout can read. Generated notebooks are not a
substitute for the gitignored canonical sources (an instructor-only solution
can carry a misconception the student copy never shows), so `--local` exists
and is run by `scripts/nbbuild.py` and `scripts/sync_instructor_repo.sh`, the
two points where canonical content actually moves. `--local` additionally
fails when a canonical source is NEWER than its generated student notebook.

`--self-test` is the mutation test the acceptance contract requires. It runs
against an ISOLATED SNAPSHOT of every declared surface (round-4 finding G3: an
earlier version mutated real files and one interrupted run shipped fixture
text into a published chapter). Each mutation must be caught BY ITS OWN
misconception id AT the probe path, and every `allow_reversals:` fixture — an
endorsement built to launder through an `allow:` span — must be caught too.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
_ROOT = REPO                      # parameterized so the self-test can point the
                                  # WHOLE validator at a snapshot (never at the
                                  # real tree)
MANIFEST_REL = Path("planning/MISCONCEPTION_MANIFEST.yml")


def set_root(root: Path) -> None:
    global _ROOT
    _ROOT = root


def manifest_path() -> Path:
    return _ROOT / MANIFEST_REL


class _DupKeyLoader(yaml.SafeLoader):
    """A loader that REFUSES duplicate mapping keys.

    PyYAML silently keeps the last of a duplicated key. That is how a whole
    `reject_patterns:` block vanished from this manifest without a word: two
    blocks under one misconception, the first dropped, the rule it carried
    quietly unenforced while the scan still reported clean (round-4 G1).
    """


def _no_duplicates(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"duplicate key {key!r} — the earlier block would be silently "
                f"discarded", key_node.start_mark)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_DupKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicates)


def check_schema(data) -> list[str]:
    """Structural checks on the manifest itself, before it gates anything.

    A5 requires each defect to carry its estimand, its counterexample, and a
    concept check — a row that only rejects wordings is a phrase filter, not a
    misconception record (round-4 G2).
    """
    problems = []
    ids = [m.get("id") for m in data.get("misconceptions", [])]
    for i in ids:
        if not i:
            problems.append("schema: a misconception has no id")
    dupes = {i for i in ids if ids.count(i) > 1}
    for d in dupes:
        problems.append(f"schema: duplicate misconception id {d!r}")
    for m in data.get("misconceptions", []):
        mid = m.get("id", "?")
        if not (m.get("rejects") or m.get("reject_patterns")):
            problems.append(f"schema[{mid}]: no rejects and no reject_patterns")
        if not m.get("requires"):
            problems.append(f"schema[{mid}]: no `requires` — absence of the error "
                            f"is not presence of the correction")
        for field in ("defect", "estimand", "counterexample", "concept_check"):
            if not m.get(field):
                problems.append(f"schema[{mid}]: missing A5 field `{field}`")
        if m.get("allow") and not m.get("allow_reversals"):
            problems.append(f"schema[{mid}]: has `allow:` but no `allow_reversals:` "
                            f"— an untested allow span is a laundering channel")
        for pt in m.get("reject_patterns", []):
            if not pt.get("catches"):
                problems.append(f"schema[{mid}]: a pattern ships no `catches:` "
                                f"fixtures, so nothing proves it fires")
            if not pt.get("permits"):
                problems.append(f"schema[{mid}]: a pattern ships no `permits:` "
                                f"fixtures, so nothing guards against false failures")
            try:
                re.compile(pt["pattern"])
            except re.error as e:
                problems.append(f"schema[{mid}]: bad regex {pt['pattern']!r} ({e})")
    return problems


def load():
    return yaml.load(manifest_path().read_text(), Loader=_DupKeyLoader)


_TEXT_CACHE: dict[tuple, str] = {}


def read_surface(f: Path) -> str:
    """Text of a surface. Notebooks are JSON, so pull the cell sources out."""
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


def surfaces(spec, defaults, local: bool = False) -> tuple[list[Path], list[str]]:
    """Resolve globs to files, and report any REQUIRED glob that matched none.

    Fail-closed: a glob that silently matches zero files is how a gate reports
    "clean" about material it never opened (round-3 finding R3-7). In --local
    mode, `local_required: true` globs (canonical sources, instructor
    notebooks) are promoted to required.
    """
    groups = spec.get("surfaces") or defaults["surfaces"]
    excl = defaults.get("exclude", [])
    files: list[Path] = []
    empty: list[str] = []
    for entry in groups:
        g = entry["glob"] if isinstance(entry, dict) else entry
        required = entry.get("required", False) if isinstance(entry, dict) else False
        if local and isinstance(entry, dict) and entry.get("local_required"):
            required = True
        matched = []
        for f in _ROOT.glob(g):
            if not f.is_file():
                continue
            rel = f.relative_to(_ROOT).as_posix()
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
    An allowed corrective use suppresses a hit only when it FULLY covers the
    same span — and every `allow:` entry is required (by schema + self-test
    reversals) to contain its refutation, so an endorsement reusing the bare
    quotation no longer matches the allow and still fires (round-4 G3).
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


def check_freshness() -> list[str]:
    """--local only: a canonical source newer than its generated student
    notebook means the tracked artifact is STALE — the public tree shows prose
    the next rebuild will change (round-4 G2's freshness requirement)."""
    problems = []
    src_dir = _ROOT / "_production_kit" / "nb_sources"
    if not src_dir.is_dir():
        return ["local: _production_kit/nb_sources/ missing — canonical sources "
                "cannot be certified from this checkout"]
    for src in sorted(src_dir.glob("*.py")):
        student = _ROOT / "notebooks" / "student" / f"{src.stem}_student.ipynb"
        if not student.exists():
            # v1-era or retired sources carry no tracked counterpart
            continue
        if src.stat().st_mtime > student.stat().st_mtime + 1:
            problems.append(
                f"local: STALE generation — {src.relative_to(_ROOT)} is newer "
                f"than {student.relative_to(_ROOT)}; rerun scripts/nbbuild.py "
                f"{src.stem.split('_')[0]}")
    return problems


def run(verbose: bool = False, check_nums: bool = True,
        local: bool = False) -> list[str]:
    data = load()
    defaults = data["defaults"]
    problems: list[str] = check_schema(data)

    for m in data["misconceptions"]:
        mid = m["id"]
        files, empty = surfaces(m, defaults, local=local)
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
                        f"{f.relative_to(_ROOT)}:{ln}")

        for pat in m.get("reject_patterns", []):
            rx, why = pat["pattern"], pat.get("why", "")
            for f, text in texts.items():
                for ln in scan_pattern(text, rx, allow):
                    problems.append(
                        f"[{mid}] rejected CLAIM ({why}) — "
                        f"{f.relative_to(_ROOT)}:{ln}  [/{rx}/]")

        for phrase in m.get("requires", []):
            needle = " ".join(phrase.lower().split())
            if not any(needle in _normalize(txt)[0] for txt in texts.values()):
                problems.append(
                    f"[{mid}] required correction {phrase!r} appears nowhere "
                    f"on the declared surfaces")

        if verbose:
            print(f"  {mid}: {len(files)} files scanned")

    if local:
        problems.extend(check_freshness())
    if check_nums:
        problems.extend(check_numbers(data, verbose=verbose))
    return problems


def check_numbers(data, verbose: bool = False) -> list[str]:
    """Every numeric claim in prose must match the seeded computation.

    Round-3 finding R3-8: the manifest declared numbers and nothing read them,
    so prose could drift away from the figures without failing the build.
    Round-4 G4: claims now enumerate every numeric component — both endpoints,
    counts, extrema, and the alt-text copies.
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

    cache: dict[str, dict] = {}
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)
        strings = sims.L["book"]
        for spec in specs:
            f = _ROOT / spec["file"]
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


def _snapshot(dst: Path) -> None:
    """Copy every declared surface (plus the manifest) into `dst`, preserving
    relative paths, so the self-test can mutate freely without ever touching
    the real tree."""
    data = yaml.load((REPO / MANIFEST_REL).read_text(), Loader=_DupKeyLoader)
    defaults = data["defaults"]
    todo = {REPO / MANIFEST_REL}
    for entry in defaults["surfaces"]:
        g = entry["glob"] if isinstance(entry, dict) else entry
        todo.update(f for f in REPO.glob(g) if f.is_file())
    for spec in data.get("numbers", []):
        f = REPO / spec["file"]
        if f.exists():
            todo.add(f)
    excl = defaults.get("exclude", [])
    for f in todo:
        rel = f.relative_to(REPO)
        if any(f.match(e) for e in excl):
            continue
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, target)


def self_test() -> int:
    """End-to-end mutation test against an ISOLATED snapshot.

    Round-3 finding R3-9: the earlier version called `scan_file()` directly —
    a unit test of the matcher wearing a mutation test's name. Round-4 G3: the
    next version routed mutations through `run()` but wrote them into REAL
    files; one interrupted run shipped fixture text into published ch22.

    Now: the whole surface set is copied into a temporary snapshot, the
    validator root is pointed there, and every mutation happens on the copy.
    Each mutation must be caught, BY ITS OWN misconception id, AT the probe
    path. Killing this process at any moment leaves the real tree untouched.
    """
    failures: list[str] = []

    with tempfile.TemporaryDirectory(prefix="misconception-selftest-") as td:
        snap = Path(td)
        _snapshot(snap)
        set_root(snap)
        try:
            data = load()

            baseline = run(check_nums=False)
            if baseline:
                print("✗ self-test cannot run: the snapshot is not clean to begin with")
                for b in baseline[:8]:
                    print("   ", b)
                return 1

            probe = snap / "book" / "_selftest_probe.qmd"

            def mutate_and_scan(snippet: str, expect_id: str) -> tuple[bool, bool]:
                """(caught_at_all, caught_by_expected_id_at_probe)."""
                probe.write_text("---\ntitle: probe\n---\n\n" + snippet + "\n")
                try:
                    probs = run(check_nums=False)
                    right = any(f"[{expect_id}]" in p and "_selftest_probe" in p
                                for p in probs)
                    return bool(probs), right
                finally:
                    probe.unlink(missing_ok=True)

            # 1. every literal rejected phrase: caught by ITS id at the probe
            for m in data["misconceptions"]:
                for phrase in m.get("rejects", []):
                    caught, right = mutate_and_scan(phrase, m["id"])
                    if not right:
                        failures.append(
                            f"[{m['id']}] literal not caught by its own rule at "
                            f"the probe: {phrase!r}" if caught else
                            f"[{m['id']}] literal NOT caught end-to-end: {phrase!r}")

            # 2. every paraphrase drift caught; every benign phrasing permitted
            for m in data["misconceptions"]:
                for pat in m.get("reject_patterns", []):
                    for ex in pat.get("catches", []):
                        caught, right = mutate_and_scan(ex, m["id"])
                        if not right:
                            failures.append(
                                f"[{m['id']}] DRIFT not caught by its own rule: {ex!r}"
                                if caught else
                                f"[{m['id']}] DRIFT not caught end-to-end: {ex!r}")
                    for ex in pat.get("permits", []):
                        caught, _ = mutate_and_scan(ex, m["id"])
                        if caught:
                            failures.append(
                                f"[{m['id']}] FALSE POSITIVE end-to-end: {ex!r}")

            # 3. every allow-reversal — an endorsement engineered to hide inside
            # an allow span — MUST still be caught (round-4 G3 laundering)
            for m in data["misconceptions"]:
                for ex in m.get("allow_reversals", []):
                    caught, right = mutate_and_scan(ex, m["id"])
                    if not right:
                        failures.append(
                            f"[{m['id']}] ALLOW-REVERSAL laundered through: {ex!r}")

            # 4. structural guarantee: a required glob matching nothing must FAIL
            mpath = snap / MANIFEST_REL
            manifest_src = mpath.read_text()
            mpath.write_text(manifest_src.replace(
                '{glob: "notebooks/student/*.ipynb", required: true}',
                '{glob: "notebooks/student/__none__*.ipynb", required: true}'))
            if not any("REQUIRED surface matched zero files" in p
                       for p in run(check_nums=False)):
                failures.append("zero-match required glob did NOT fail the scan")
            mpath.write_text(manifest_src)

            # 5. structural guarantee: a drifted prose number must FAIL
            ch14 = snap / "book/part3-pathways/14-prediction-and-generalization.qmd"
            ch14_src = ch14.read_text()
            ch14.write_text(ch14_src.replace("0.025 RMSE on average",
                                             "0.030 RMSE on average"))
            if not any("numbers[ch14-optimism]" in p for p in run()):
                failures.append("drifted prose number did NOT fail the scan")
            ch14.write_text(ch14_src)

            # 6. structural guarantee: deleting a required correction must FAIL
            ch21 = snap / "book/part4-credible-evidence/21-robustness-and-sensitivity.qmd"
            ch21_src = ch21.read_text()
            ch21.write_text(ch21_src.replace("specification\nspread", "REMOVED TERM"))
            if not any("required correction" in p for p in run(check_nums=False)):
                failures.append("deleted required correction did NOT fail the scan")
            ch21.write_text(ch21_src)

            # 7. structural guarantee: a stale canonical source must FAIL --local
            src_dir = snap / "_production_kit" / "nb_sources"
            candidates = sorted(src_dir.glob("*.py")) if src_dir.is_dir() else []
            fresh_pair = next(
                (s for s in candidates
                 if (snap / "notebooks/student" / f"{s.stem}_student.ipynb").exists()),
                None)
            if fresh_pair is not None:
                student = snap / "notebooks/student" / f"{fresh_pair.stem}_student.ipynb"
                import os
                st = student.stat()
                os.utime(fresh_pair, (st.st_atime, st.st_mtime + 3600))
                if not any("STALE generation" in p
                           for p in run(check_nums=False, local=True)):
                    failures.append("stale canonical source did NOT fail --local")
                os.utime(fresh_pair, (st.st_atime, st.st_mtime))
        finally:
            set_root(REPO)
            _TEXT_CACHE.clear()

    if failures:
        print("✗ self-test failed — the gate does not gate:")
        for f in failures:
            print("   ", f)
        return 1

    data = yaml.load((REPO / MANIFEST_REL).read_text(), Loader=_DupKeyLoader)
    lit = sum(len(m.get("rejects", [])) for m in data["misconceptions"])
    drift = sum(len(pt.get("catches", []))
                for m in data["misconceptions"] for pt in m.get("reject_patterns", []))
    permit = sum(len(pt.get("permits", []))
                 for m in data["misconceptions"] for pt in m.get("reject_patterns", []))
    rev = sum(len(m.get("allow_reversals", [])) for m in data["misconceptions"])
    print(f"✓ isolated end-to-end mutation test: {lit} literals and {drift} drifts "
          f"caught by their own rules, {permit} benign phrasings permitted, "
          f"{rev} allow-reversals refused laundering, plus zero-match-glob, "
          f"drifted-number, deleted-correction, and stale-source guarantees "
          f"— no real file was touched")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true",
                    help="mutation test against an isolated snapshot")
    ap.add_argument("--local", action="store_true",
                    help="also require canonical sources + instructor notebooks "
                         "and check generation freshness (run by nbbuild/sync)")
    ap.add_argument("--no-numbers", action="store_true",
                    help="skip the seeded numerical evaluator (fast path for "
                         "notebook builds; chapter edits must run WITH numbers)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    problems = run(verbose=args.verbose, check_nums=not args.no_numbers,
                   local=args.local)
    if problems:
        print(f"✗ misconception scan: {len(problems)} problem(s)")
        for p in problems:
            print("   ", p)
        return 1
    data = load()
    n = len(data["misconceptions"])
    if args.local:
        print(f"✓ misconception scan clean (LOCAL) — {n} corrected misconceptions "
              f"hold across public surfaces AND canonical sources + instructor "
              f"notebooks; generation is fresh")
    else:
        print(f"✓ misconception scan clean — {n} corrected misconceptions hold "
              f"across TRACKED PUBLIC surfaces (canonical sources need --local, "
              f"run by nbbuild and the instructor-repo sync)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
