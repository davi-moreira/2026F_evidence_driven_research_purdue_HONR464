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
        for field in ("defect", "estimand", "counterexample"):
            if not m.get(field):
                problems.append(f"schema[{mid}]: missing A5 field `{field}`")
        cc = m.get("concept_check")
        if not (isinstance(cc, dict) and cc.get("question") and cc.get("answer")):
            problems.append(f"schema[{mid}]: `concept_check` must carry "
                            f"question AND answer — without the key, a wrong "
                            f"reader is undetectable (A5)")
        anchor = (cc or {}).get("anchor") if isinstance(cc, dict) else None
        if not (isinstance(anchor, dict) and anchor.get("file")
                and anchor.get("locator")):
            problems.append(f"schema[{mid}]: `concept_check.anchor` must be a "
                            f"structured, resolvable {{file, locator}} "
                            f"(round-6 F1)")
        cases = m.get("cases", [])
        kinds = [c.get("kind") for c in cases]
        for need in ("positive", "boundary", "converse"):
            if need not in kinds:
                problems.append(f"schema[{mid}]: no `{need}` case — one vivid "
                                f"counterexample proves a failure CAN happen; "
                                f"only boundary and converse prove WHICH "
                                f"feature causes it (A5)")
        for c in cases:
            if c.get("code"):
                if not c.get("expect"):
                    problems.append(f"schema[{mid}]: a numeric case has no "
                                    f"`expect` assertions")
            elif c.get("fixture"):
                if c.get("verdict") not in ("caught", "permitted"):
                    problems.append(f"schema[{mid}]: a fixture case needs "
                                    f"verdict caught|permitted")
            else:
                problems.append(f"schema[{mid}]: a case has neither `code` "
                                f"nor `fixture`")
        if m.get("allow") and not m.get("allow_reversals"):
            problems.append(f"schema[{mid}]: has `allow:` but no `allow_reversals:` "
                            f"— an untested allow span is a laundering channel")
        for a in m.get("allow", []):
            if not isinstance(a, dict) or not a.get("text") or not a.get("pins"):
                problems.append(
                    f"schema[{mid}]: allow entries must be pinned "
                    f"{{text, pins: [{{file, sha256}}]}} — an unpinned allow "
                    f"suppresses anywhere (round-5 G-B)")
                continue
            for pin in a["pins"]:
                if not (isinstance(pin, dict) and pin.get("file") and pin.get("sha256")):
                    problems.append(f"schema[{mid}]: malformed pin in allow "
                                    f"{a['text'][:40]!r}")
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
    # blank-line join: cells are ALWAYS separate paragraphs, so pin windows
    # never straddle a cell boundary (round-6 F3)
    text = "\n\n".join(out)
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


_PARA_CACHE: dict[int, list[tuple[int, int, str]]] = {}


def _paragraph_index(text: str) -> list[tuple[int, int, str]]:
    """(start_line, end_line, sha256-of-normalized-paragraph) per blank-line
    block. The unit an `allow` pin is scoped to (round-5 G-B)."""
    import hashlib
    ck = hash(text)
    if ck in _PARA_CACHE:
        return _PARA_CACHE[ck]
    out, line = [], 1
    for block in re.split(r"(\n\s*\n)", text):
        if re.fullmatch(r"\n\s*\n", block):
            line += block.count("\n")
            continue
        n = block.count("\n")
        norm = " ".join(block.lower().split())
        if norm:
            out.append((line, line + n,
                        hashlib.sha256(norm.encode()).hexdigest()))
        line += n
    _PARA_CACHE[ck] = out
    return out


def _window_hashes(text: str) -> list[tuple[int, int, str]]:
    """(start_line, end_line, sha256 of the prev+this+next paragraph WINDOW).

    A pin is bound to the window, not the paragraph alone: an endorsement
    added in the paragraph BEFORE or AFTER the quotation changes the window
    hash and invalidates the exception (round-6 F3)."""
    import hashlib
    paras = _paragraph_index(text)
    out = []
    for i, (lo, hi, _sha) in enumerate(paras):
        window = []
        for j in (i - 1, i, i + 1):
            if 0 <= j < len(paras):
                window.append(paras[j][2])
        out.append((lo, hi, hashlib.sha256(" ".join(window).encode()).hexdigest()))
    return out


def _pinned_suppressor(text: str, allow: list, file_rel: str):
    """Return a predicate: is the hit at (span, line) suppressed?

    Suppression requires ALL of (round-5 G-B, hardened round-6 F3):
      1. the hit span fully inside an occurrence of the allow TEXT;
      2. this file listed in the allow entry's pins;
      3. the WINDOW (previous + containing + next paragraph) hashing to the
         pinned value — any adjacent edit invalidates the exception;
      4. EXACTLY ONE window in the file matching that pin — a duplicated
         copy of the pinned paragraph invalidates it.
    """
    norm, _ = _normalize(text)
    windows = _window_hashes(text)
    entries = []
    for a in allow:
        an = " ".join(a["text"].lower().split())
        shas = {p["sha256"] for p in a["pins"] if p["file"] == file_rel}
        if not shas:
            continue
        spans, start = [], 0
        while (i := norm.find(an, start)) != -1:
            spans.append((i, i + len(an)))
            start = i + 1
        if spans:
            entries.append((spans, shas))

    def suppressed(span: tuple[int, int], line: int) -> bool:
        for spans, shas in entries:
            if not any(s <= span[0] and span[1] <= e for s, e in spans):
                continue
            for lo, hi, wsha in windows:
                if lo <= line <= hi:
                    if wsha in shas and \
                            sum(1 for _, _, w in windows if w == wsha) == 1:
                        return True
                    break
        return False

    return suppressed


def scan_file(text: str, phrase: str, allow: list, file_rel: str = "") -> list[int]:
    """Line numbers where `phrase` appears outside a PINNED corrective use.

    Works on whitespace-normalized text so wrapped phrases are still caught.
    Suppression is pin-scoped: see `_pinned_suppressor`.
    """
    norm, linemap = _normalize(text)
    needle = " ".join(phrase.lower().split())
    suppressed = _pinned_suppressor(text, allow, file_rel)

    hits, start = [], 0
    while (i := norm.find(needle, start)) != -1:
        line = linemap[i] if i < len(linemap) else 0
        if not suppressed((i, i + len(needle)), line):
            hits.append(line)
        start = i + 1
    return hits


def scan_pattern(text: str, pattern: str, allow: list, file_rel: str = "") -> list[int]:
    """Same as scan_file but for a regex FAMILY, not a literal phrase.

    Literal phrases only catch the wording that was already fixed. Paraphrase
    is how a misconception actually returns — "eliminates that artifact",
    "returns precisely zero", "if every specification agrees, it is robust".
    These patterns target the CLAIM, so drift is caught too.
    """
    norm, linemap = _normalize(text)
    suppressed = _pinned_suppressor(text, allow, file_rel)
    hits = []
    for m in re.finditer(pattern, norm):
        line = linemap[m.start()] if m.start() < len(linemap) else 0
        if not suppressed(m.span(), line):
            hits.append(line)
    return hits


def check_freshness() -> list[str]:
    """--local only: the generated student notebook must carry a content-hash
    stamp matching its canonical source. An mtime heuristic was defeatable by
    timestamp restoration or by touching the generated file (round-5 G-D);
    a content hash is not. `scripts/nbbuild.py` writes the stamp on every
    build."""
    import hashlib
    problems = []
    src_dir = _ROOT / "_production_kit" / "nb_sources"
    if not src_dir.is_dir():
        return ["local: _production_kit/nb_sources/ missing — canonical sources "
                "cannot be certified from this checkout"]
    # The ACTIVE stems come from the canonical registry, not from which files
    # happen to exist (round-7 P2: inferring retirement from student-file
    # absence let a deleted artifact escape unreported).
    active_stems: set[str] | None = None
    try:
        sys.path.insert(0, str(REPO / "scripts"))
        import notebooks_map as _nm
        active_stems = {v[0] for v in _nm.NOTEBOOKS.values()} | \
                       {v[0] for v in _nm.MS_NOTEBOOKS.values()}
    except Exception:
        pass                                    # registry unavailable: fall back

    # Iterate the REGISTERED stems, not the files that happen to exist
    # (round-8 P2: looping glob("*.py") let a deleted canonical source
    # vanish silently while its generated artifacts stayed green).
    if active_stems is not None:
        stems = sorted(active_stems)
    else:
        stems = sorted(p.stem for p in src_dir.glob("*.py")
                       if (_ROOT / "notebooks" / "student" /
                           f"{p.stem}_student.ipynb").exists())
    for stem in stems:
        src = src_dir / f"{stem}.py"
        student = _ROOT / "notebooks" / "student" / f"{stem}_student.ipynb"
        instructor = _ROOT / "notebooks" / "instructor" / f"{stem}_instructor.ipynb"
        if not src.exists():
            problems.append(
                f"local: MISSING canonical source {src.relative_to(_ROOT)} "
                f"for registered notebook {stem}")
            continue
        src_hash = hashlib.sha256(src.read_bytes()).hexdigest()
        for artifact in (student, instructor):
            if not artifact.exists():
                problems.append(
                    f"local: MISSING generated artifact "
                    f"{artifact.relative_to(_ROOT)}; rerun scripts/nbbuild.py "
                    f"{src.stem.split('_')[0]}")
                continue
            try:
                meta = json.loads(artifact.read_text()).get("metadata", {})
            except json.JSONDecodeError:
                problems.append(f"local: unreadable notebook "
                                f"{artifact.relative_to(_ROOT)}")
                continue
            stamp = meta.get("edrai_generation", {}).get("src_sha256")
            if stamp is None:
                problems.append(
                    f"local: UNSTAMPED generation — "
                    f"{artifact.relative_to(_ROOT)} carries no source hash; "
                    f"rerun scripts/nbbuild.py {src.stem.split('_')[0]}")
                continue
            if stamp != src_hash:
                problems.append(
                    f"local: STALE generation — {src.relative_to(_ROOT)} "
                    f"changed since {artifact.relative_to(_ROOT)} was built; "
                    f"rerun scripts/nbbuild.py {src.stem.split('_')[0]}")
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
                rel = f.relative_to(_ROOT).as_posix()
                for ln in scan_file(text, phrase, allow, rel):
                    problems.append(
                        f"[{mid}] rejected phrase {phrase!r} — {rel}:{ln}")

        for pat in m.get("reject_patterns", []):
            rx, why = pat["pattern"], pat.get("why", "")
            for f, text in texts.items():
                rel = f.relative_to(_ROOT).as_posix()
                for ln in scan_pattern(text, rx, allow, rel):
                    problems.append(
                        f"[{mid}] rejected CLAIM ({why}) — {rel}:{ln}  [/{rx}/]")

        for phrase in m.get("requires", []):
            needle = " ".join(phrase.lower().split())
            if not any(needle in _normalize(txt)[0] for txt in texts.values()):
                problems.append(
                    f"[{mid}] required correction {phrase!r} appears nowhere "
                    f"on the declared surfaces")

        if verbose:
            print(f"  {mid}: {len(files)} files scanned")

    # anchor resolution (round-6 F1): the concept check must point at a real
    # place a reader is actually asked
    for m in data["misconceptions"]:
        anchor = (m.get("concept_check") or {}).get("anchor")
        if isinstance(anchor, dict) and anchor.get("file"):
            f = _ROOT / anchor["file"]
            if not f.exists():
                problems.append(f"anchor[{m['id']}]: file {anchor['file']!r} "
                                f"does not exist")
            else:
                needle = " ".join(str(anchor.get("locator", "")).lower().split())
                if needle and needle not in _normalize(read_surface(f))[0]:
                    problems.append(f"anchor[{m['id']}]: locator "
                                    f"{anchor['locator']!r} not found in "
                                    f"{anchor['file']}")

    if local:
        problems.extend(check_freshness())
    # the A5 case table ALWAYS runs (round-6 F5): --no-numbers skips only the
    # figure-number evaluator, never the executable misconception record
    problems.extend(check_cases(data, verbose=verbose))
    if check_nums:
        problems.extend(check_numbers(data, verbose=verbose))
    return problems


def check_cases(data, verbose: bool = False) -> list[str]:
    """Execute the A5 case table (round-5 G-A).

    Every misconception runs its positive, boundary, and converse cases:
    numeric cases execute seeded numpy code and assert declared expectations;
    conceptual cases run their fixtures through the entry's OWN scan rules.
    A green scan with a failing case table means the concept is wrong even
    though no rejected wording is present — exactly what a phrase scanner
    alone cannot see.
    """
    problems: list[str] = []
    try:
        import numpy as np
    except Exception as e:                      # pragma: no cover
        return [f"cases: numpy unavailable ({e})"]

    for m in data["misconceptions"]:
        mid = m["id"]
        allow = m.get("allow", [])
        for c in m.get("cases", []):
            kind = c.get("kind", "?")
            if c.get("code"):
                ns = {"np": np}
                try:
                    exec(c["code"], ns)          # trusted repo-authored code
                except Exception as e:
                    problems.append(f"cases[{mid}/{kind}]: code raised {e!r}")
                    continue
                result = ns.get("result")
                if not isinstance(result, dict):
                    problems.append(f"cases[{mid}/{kind}]: code set no "
                                    f"`result` dict")
                    continue
                for ex in c.get("expect", []):
                    key = ex.get("key")
                    if key not in result:
                        problems.append(f"cases[{mid}/{kind}]: result has no "
                                        f"key {key!r} (has {sorted(result)})")
                        continue
                    got = float(result[key])
                    if "value" in ex:
                        tol = float(ex.get("tolerance", 0))
                        if abs(got - float(ex["value"])) > tol:
                            problems.append(
                                f"cases[{mid}/{kind}]: {key} = {got:.4f}, "
                                f"expected {ex['value']} ± {tol}")
                    if "min" in ex and got < float(ex["min"]):
                        problems.append(
                            f"cases[{mid}/{kind}]: {key} = {got:.4f} < "
                            f"min {ex['min']}")
                    if "max" in ex and got > float(ex["max"]):
                        problems.append(
                            f"cases[{mid}/{kind}]: {key} = {got:.4f} > "
                            f"max {ex['max']}")
            elif c.get("fixture"):
                probe = c["fixture"]
                caught = any(scan_file(probe, ph, allow, "case-fixture")
                             for ph in m.get("rejects", []))
                caught = caught or any(
                    scan_pattern(probe, pt["pattern"], allow, "case-fixture")
                    for pt in m.get("reject_patterns", []))
                want = c.get("verdict") == "caught"
                if caught != want:
                    problems.append(
                        f"cases[{mid}/{kind}]: fixture was "
                        f"{'caught' if caught else 'permitted'}, expected "
                        f"{c.get('verdict')}: {probe[:60]!r}")
            if verbose:
                print(f"  cases[{mid}/{kind}] ✓")
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

            # 6b. structural guarantees on the PIN model (rounds 5-6): the
            # exception must die under (i) an edit inside the quotation's
            # paragraph, (ii) an endorsement in the NEXT paragraph, (iii) an
            # endorsement in the PREVIOUS paragraph, and (iv) a duplicated
            # copy of the pinned paragraph in the same file.
            ch21_src2 = ch21.read_text()
            pin_probes = [
                ("in-paragraph edit",
                 ch21_src2.replace(
                     "quietly claims a precision nobody computed.",
                     "quietly claims a precision nobody computed. "
                     "That warning is overly cautious.")),
                ("next-paragraph endorsement",
                 ch21_src2.replace(
                     "\n\nThen you run one more attack",
                     "\n\nThat warning is overly cautious. Use that quoted "
                     "range as the study uncertainty interval.\n\n"
                     "Then you run one more attack")),
                ("previous-paragraph endorsement",
                 ch21_src2.replace(
                     "eight-to-fifteen range stretched",
                     "Ignore the warning coming next. The eight-to-fifteen "
                     "range stretched")),
            ]
            # (iv) duplicate the whole pinned paragraph at the end of the file
            pinned_para = next(
                (blk for blk in re.split(r"\n\s*\n", ch21_src2)
                 if "the honest range is" in " ".join(blk.lower().split())),
                None)
            if pinned_para is not None:
                pin_probes.append(("same-file duplicate",
                                   ch21_src2 + "\n\n" + pinned_para + "\n"))
            for label, mutated in pin_probes:
                ch21.write_text(mutated)
                if not any("[specification-spread]" in p and "21-robustness" in p
                           for p in run(check_nums=False)):
                    failures.append(f"pin survived laundering probe: {label}")
            ch21.write_text(ch21_src2)

            # 7. structural guarantee: a content-changed canonical source must
            # FAIL --local even with its timestamp untouched (round-5 G-D)
            src_dir = snap / "_production_kit" / "nb_sources"
            candidates = sorted(src_dir.glob("*.py")) if src_dir.is_dir() else []
            fresh_pair = next(
                (s for s in candidates
                 if (snap / "notebooks/student" / f"{s.stem}_student.ipynb").exists()),
                None)
            if fresh_pair is not None:
                import os
                src_bytes = fresh_pair.read_bytes()
                st = fresh_pair.stat()
                fresh_pair.write_bytes(src_bytes + b"\n# drifted content\n")
                os.utime(fresh_pair, (st.st_atime, st.st_mtime))  # mtime restored
                if not any("STALE generation" in p
                           for p in run(check_nums=False, local=True)):
                    failures.append("content-changed canonical source did NOT "
                                    "fail --local (hash check inert)")
                fresh_pair.write_bytes(src_bytes)
            # 7b. structural guarantee: a corrupted INSTRUCTOR stamp must fail
            # --local even while the student copy is valid (round-6 F4)
            instr_nb = next(iter(sorted(
                (snap / "notebooks/instructor").glob("*_instructor.ipynb"))), None)
            if instr_nb is not None:
                instr_src = instr_nb.read_text()
                nbj = json.loads(instr_src)
                nbj.setdefault("metadata", {}).setdefault(
                    "edrai_generation", {})["src_sha256"] = "0" * 64
                instr_nb.write_text(json.dumps(nbj))
                probs7b = run(check_nums=False, local=True)
                if not any("STALE generation" in p and "instructor" in p
                           for p in probs7b):
                    failures.append("corrupted instructor stamp did NOT fail "
                                    "--local")
                instr_nb.write_text(instr_src)

            # 7c. structural guarantee: a broken concept-check anchor must
            # fail — deletion (schema) and a nonexistent locator (round-6 F1)
            manifest_anchor_src = mpath.read_text()
            mpath.write_text(manifest_anchor_src.replace(
                'locator: "counting direction"', 'locator: "phrase that is nowhere"'))
            if not any("anchor[signed-bias]" in p for p in run(check_nums=False)):
                failures.append("nonexistent anchor locator did NOT fail")
            mpath.write_text(manifest_anchor_src.replace(
                'anchor: {file: "book/part2-curiosity-to-design/10-declaring-and-diagnosing-a-research-design.qmd", locator: "counting direction"}',
                'anchor: ""'))
            if not any("concept_check.anchor" in p for p in run(check_nums=False)):
                failures.append("deleted anchor did NOT fail the schema")
            mpath.write_text(manifest_anchor_src)

            # 7d. structural guarantee: a DELETED student artifact of an
            # active notebook must fail --local by name (round-7 P2)
            del_target = snap / "notebooks/student/nb05_observational_descriptive_student.ipynb"
            if del_target.exists():
                del_bytes = del_target.read_bytes()
                del_target.unlink()
                if not any("MISSING generated artifact" in p and "nb05" in p
                           for p in run(check_nums=False, local=True)):
                    failures.append("deleted student artifact did NOT fail "
                                    "--local by name")
                del_target.write_bytes(del_bytes)

            # 8. structural guarantee: a flipped case expectation must FAIL
            # (round-5 G-A: an inert case table is prose wearing a test's name)
            manifest_src2 = mpath.read_text()
            mpath.write_text(manifest_src2.replace(
                "- {key: bias_a, value: 1.993, tolerance: 0.1}",
                "- {key: bias_a, value: 3.5, tolerance: 0.1}"))
            if not any("cases[signed-bias/positive]" in p for p in run()):
                failures.append("flipped case expectation did NOT fail the scan")
            mpath.write_text(manifest_src2)

            # 9. structural guarantee: deleting a required case kind must FAIL
            mpath.write_text(manifest_src2.replace("- kind: converse",
                                                   "- kind: extra", 1))
            if not any("no `converse` case" in p for p in run(check_nums=False)):
                failures.append("deleted converse case did NOT fail the schema")
            mpath.write_text(manifest_src2)
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
    ncases = sum(len(m.get("cases", [])) for m in data["misconceptions"])
    print(f"✓ isolated end-to-end mutation test: {lit} literals and {drift} drifts "
          f"caught by their own rules, {permit} benign phrasings permitted, "
          f"{rev} allow-reversals refused laundering, {ncases} A5 cases "
          f"executable, plus zero-match-glob, drifted-number, "
          f"deleted-correction, pin-invalidation, stale-source, flipped-case, "
          f"and deleted-case guarantees — no real file was touched")
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
