#!/usr/bin/env python3
"""validate_book_architecture.py — the Phase-2 identity/crosswalk validator (D35).

Checks the three schema-1.0 manifests against each other, the filesystem, the
meeting schedule, and the milestone briefs. Per D35(7) THE VALIDATOR IS THE
ARBITER: until this passes, nothing generated may consume the crosswalk.

    .venv/bin/python scripts/validate_book_architecture.py
    .venv/bin/python scripts/validate_book_architecture.py --a2

Modes:
  (default)          structural + cross-file + schedule + brief-agreement
                     checks (briefs must equal the crosswalk on BOTH surfaces,
                     both directions — the C1 migration exception is retired);
                     A2 leakage reported as an advisory count (it becomes a
                     hard gate at the Architecture-v1 freeze).
  --a2-advisory      downgrade the A2 scan to advisory (escape hatch).

On success (default mode) writes planning/.crosswalk_lock.json — hashes of the
three manifests + validator version — the machine-readable "verified" flag the
authored files may not carry themselves (C4).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ARCH = REPO / "planning" / "BOOK_ARCHITECTURE.yml"
CW = REPO / "planning" / "COURSE_BOOK_CROSSWALK.yml"
ASSESS = REPO / "planning" / "BOOK_ASSESSMENTS.yml"
LEAK = REPO / "planning" / "BOOK_LEAKAGE_POLICY.yml"
SCHEDULE = REPO / "planning" / "MEETING_SCHEDULE.csv"
BRIEFS = REPO / "_research_project" / "2026Fall"
LOCK = REPO / "planning" / ".crosswalk_lock.json"
VALIDATOR_VERSION = "1.0"

EVENTS = {"introduce", "practice", "checkpoint", "revisit"}
ATS = {"reading-due", "studio", "milestone-submission"}
REQUIREMENTS = {"required", "recommended", "route-required", "optional"}
PURPOSES = {"first-read", "revisit"}


class _DupKeyLoader(yaml.SafeLoader):
    pass


def _no_dup(loader, node, deep=False):
    m = {}
    for k, v in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in m:
            raise yaml.constructor.ConstructorError(
                None, None, f"duplicate key {key!r}", k.start_mark)
        m[key] = loader.construct_object(v, deep=deep)
    return m


_DupKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_dup)


def load(p: Path):
    return yaml.load(p.read_text(), Loader=_DupKeyLoader)


def check_architecture(arch) -> list[str]:
    p: list[str] = []
    if not isinstance(arch.get("schema_version"), str):
        p.append("arch: schema_version must be a string")
    parts = {x["id"]: x for x in arch.get("parts", [])}
    pranks = [x["rank"] for x in arch.get("parts", [])]
    if pranks != sorted(pranks) or len(set(pranks)) != len(pranks):
        p.append("arch: part ranks must be strictly ordered and unique")
    stations = {s["id"]: s for s in arch.get("stations", [])}
    sranks = [s["rank"] for s in arch.get("stations", [])]
    if len(set(sranks)) != len(sranks):
        p.append("arch: station ranks must be unique")
    for s in arch.get("stations", []):
        if not s.get("checkpoints"):
            p.append(f"arch[{s['id']}]: station has no checkpoints")
    routes = set(arch.get("pathways", []))
    genres = set(arch.get("genres", []))
    lessons = arch.get("lessons", [])
    ids = [l["id"] for l in lessons]
    tomb_ids = {t["id"] for t in arch.get("tombstones", [])}
    if len(set(ids)) != len(ids):
        p.append("arch: duplicate lesson ids")
    if set(ids) & tomb_ids:
        p.append(f"arch: tombstoned id reused: {set(ids) & tomb_ids}")
    ranks = [l["rank"] for l in lessons]
    if len(set(ranks)) != len(ranks):
        p.append("arch: duplicate lesson ranks")
    urls = [l["url_path"] for l in lessons]
    if len(set(urls)) != len(urls):
        p.append("arch: duplicate url_path")
    for l in lessons:
        lid = l["id"]
        for field in ("id", "state", "rank", "part", "station", "role",
                      "source", "url_path"):
            if field not in l:
                p.append(f"arch[{lid}]: missing `{field}`")
        if l.get("state") not in ("active", "planned"):
            p.append(f"arch[{lid}]: state must be active|planned")
        if l.get("part") not in parts:
            p.append(f"arch[{lid}]: unknown part {l.get('part')!r}")
        if l.get("station") not in stations:
            p.append(f"arch[{lid}]: unknown station {l.get('station')!r}")
        if l.get("role") not in ("core", "branch", "optional"):
            p.append(f"arch[{lid}]: role must be core|branch|optional")
        if l.get("role") == "branch" and not (l.get("route") or l.get("genre")):
            p.append(f"arch[{lid}]: branch lesson needs a route or genre token")
        if "route" in l and l["route"] not in routes:
            p.append(f"arch[{lid}]: unregistered route {l['route']!r}")
        if "genre" in l and l["genre"] not in genres:
            p.append(f"arch[{lid}]: unregistered genre {l['genre']!r}")
        src = REPO / "book" / l["source"]
        if l.get("state") == "active" and not src.exists():
            p.append(f"arch[{lid}]: active but source missing: {l['source']}")
        if l.get("state") == "planned":
            if not l.get("title_en"):
                p.append(f"arch[{lid}]: planned lesson needs an authored title_en")
            if src.exists():
                p.append(f"arch[{lid}]: planned but source already exists — "
                         f"activate it in the manifest first")
    used_routes = {l.get("route") for l in lessons if l.get("route")}
    if routes - used_routes:
        p.append(f"arch: registered pathway never used: {routes - used_routes}")
    used_stations = {l["station"] for l in lessons}
    if set(stations) - used_stations:
        p.append(f"arch: station with no lessons: {set(stations) - used_stations}")
    # identity epoch (round-8 P1 / A10): every id + url_path released at the
    # epoch must survive unchanged — renames and URL moves fail here, not in
    # review. Tombstoned ids are the only legal exits.
    epoch = arch.get("identity_epoch")
    if not epoch:
        p.append("arch: identity_epoch is unset — A10 has no baseline")
    else:
        import subprocess
        try:
            snap = yaml.safe_load(subprocess.run(
                ["git", "show", f"{epoch}:planning/BOOK_ARCHITECTURE.yml"],
                capture_output=True, text=True, check=True, cwd=REPO).stdout)
            now_urls = {l["id"]: l["url_path"] for l in lessons}
            for el in snap.get("lessons", []):
                eid = el["id"]
                if eid in tomb_ids:
                    continue
                if eid not in now_urls:
                    p.append(f"arch[A10]: epoch lesson {eid!r} vanished — ids "
                             f"are never renamed or deleted, only tombstoned")
                elif el.get("url_path") and now_urls[eid] != el["url_path"]:
                    p.append(f"arch[A10]: {eid} url_path changed from the "
                             f"epoch value — canonical URLs are immutable")
        except subprocess.CalledProcessError:
            p.append(f"arch: identity_epoch {epoch!r} is not a readable commit")
    # editions sanity (D36)
    eds = arch.get("editions", {})
    if "en" not in eds or eds["en"].get("lifecycle") != "current":
        p.append("arch: editions must declare en as current")
    for code, e in eds.items():
        if e.get("lifecycle") == "frozen" and not e.get("snapshot_commit"):
            p.append(f"arch: frozen edition {code} needs snapshot_commit")
    return p


def check_toc(arch) -> list[str]:
    """The EN _quarto.yml chapters block must be byte-identical to what
    scripts/build_book_toc.py renders from the manifest (D38: the TOC is a
    generated projection — twelve studio parts in (studio rank, lesson rank)
    order). Otherwise the TOC is a second, hand-maintained ordering source
    that can silently disagree with identity (Phase-2 critique, step 5)."""
    sys.path.insert(0, str(REPO / "scripts"))
    import build_book_toc
    if (REPO / "book" / "_quarto.yml").read_text() != build_book_toc.render_file():
        return ["toc: book/_quarto.yml disagrees with the manifest — run "
                "scripts/build_book_toc.py"]
    return []


def check_station_specs(arch) -> list[str]:
    """MANIFEST-level: every manifest station needs authored content in
    BOOK_STATIONS.yml (the studio pages are built from it)."""
    p: list[str] = []
    spec_path = REPO / "planning" / "BOOK_STATIONS.yml"
    if not spec_path.exists():
        return ["stations: planning/BOOK_STATIONS.yml is missing"]
    spec = {s["id"]: s for s in yaml.safe_load(spec_path.read_text())["stations"]}
    for st in arch.get("stations", []):
        sid = st["id"]
        if sid not in spec:
            p.append(f"stations[{sid}]: no authored entry in BOOK_STATIONS.yml")
            continue
        for field in ("purpose", "produces", "steps", "rails", "revisit"):
            if not spec[sid].get(field):
                p.append(f"stations[{sid}]: missing authored `{field}`")
    return p


def check_station_pages(arch) -> list[str]:
    """PROJECTION-level: every studio's generated page + workbook exist at
    the D38 paths (book/studios/, notebooks/book/studios/). Generated
    artifacts must not withhold the lock, or the generators that fix them
    could never run (the N2 deadlock)."""
    p: list[str] = []
    for st in arch.get("stations", []):
        sid, n = st["id"], st["rank"]
        page = REPO / "book" / "studios" / f"studio{n:02d}-{sid}.qmd"
        wb = (REPO / "notebooks" / "book" / "studios" /
              f"studio{n:02d}_{sid.replace('-', '_')}.ipynb")
        if not page.exists():
            p.append(f"studios[{sid}]: page missing — run build_station_pages.py")
        if not wb.exists():
            p.append(f"studios[{sid}]: workbook missing — run build_station_pages.py")
    studio_dir = REPO / "book" / "studios"
    extra = ({f.name for f in studio_dir.glob("*.qmd")} if studio_dir.exists()
             else set()) - {
        f"studio{st['rank']:02d}-{st['id']}.qmd" for st in arch.get("stations", [])}
    for e in sorted(extra):
        p.append(f"studios: ORPHAN page not in the manifest: book/studios/{e}")
    legacy = REPO / "book" / "stations"
    if legacy.exists() and any(legacy.glob("*.qmd")):
        p.append("studios: legacy book/stations/*.qmd still present — D38 "
                 "renamed the pages to book/studios/ (aliases cover old URLs)")
    return p


def check_crosswalk(arch, cw) -> list[str]:
    p: list[str] = []
    lessons = {l["id"]: l for l in arch["lessons"]}
    active = {i for i, l in lessons.items() if l["state"] == "active"}
    planned = {i for i, l in lessons.items() if l["state"] == "planned"}
    stations = {s["id"]: {c["id"] for c in s["checkpoints"]}
                for s in arch["stations"]}
    anchors: list[str] = []
    planned_anchors: list[str] = []
    milestones, nbs = [], []
    for r in cw.get("rows", []):
        mi = r.get("milestone", "?")
        milestones.append(mi)
        nbs.append(r.get("nb", "?"))
        for a in r.get("assignments", []):
            lid = a.get("lesson")
            if lid not in active:
                p.append(f"cw[{mi}]: assignment references non-active lesson "
                         f"{lid!r}")
            if a.get("requirement") not in REQUIREMENTS:
                p.append(f"cw[{mi}/{lid}]: bad requirement")
            if a.get("purpose") not in PURPOSES:
                p.append(f"cw[{mi}/{lid}]: bad purpose")
            if a.get("home_anchor"):
                if a.get("purpose") != "first-read":
                    p.append(f"cw[{mi}/{lid}]: a revisit cannot home-anchor")
                anchors.append(lid)
        planned_anchors.extend(r.get("planned_home_anchor", []))
        for e in r.get("station_events", []):
            st = e.get("station")
            if st not in stations:
                p.append(f"cw[{mi}]: unknown station {st!r}")
                continue
            if e.get("event") not in EVENTS:
                p.append(f"cw[{mi}/{st}]: bad event {e.get('event')!r}")
            if e.get("at") not in ATS:
                p.append(f"cw[{mi}/{st}]: bad at {e.get('at')!r}")
            if e.get("event") in ("checkpoint", "revisit"):
                if e.get("checkpoint") not in stations[st]:
                    p.append(f"cw[{mi}/{st}]: unknown checkpoint "
                             f"{e.get('checkpoint')!r}")
        for g in r.get("gates", []):
            for f in ("id", "requires", "before_event", "evidence", "blocking"):
                if f not in g:
                    p.append(f"cw[{mi}]: gate missing `{f}`")
    dup = {a for a in anchors if anchors.count(a) > 1}
    if dup:
        p.append(f"cw: lesson home-anchored more than once: {dup}")
    if set(anchors) != active:
        p.append(f"cw: home anchors do not partition active lessons; "
                 f"missing {active - set(anchors)}, extra {set(anchors) - active}")
    if set(planned_anchors) != planned:
        p.append(f"cw: planned_home_anchor mismatch: {set(planned_anchors) ^ planned}")
    if sorted(milestones) != [f"M{i}" for i in range(16)] and \
            sorted(milestones, key=lambda m: int(m[1:])) != [f"M{i}" for i in range(16)]:
        p.append(f"cw: milestones are not exactly M0..M15")
    if sorted(nbs) != [f"nb{i:02d}" for i in range(1, 17)]:
        p.append("cw: notebooks are not exactly nb01..nb16")
    # every checkpoint reached somewhere (WARNING until Phase 4 per the manifest)
    reached = {(e["station"], e.get("checkpoint"))
               for r in cw.get("rows", []) for e in r.get("station_events", [])
               if e.get("event") == "checkpoint"}
    for st, cps in stations.items():
        for c in cps:
            if (st, c) not in reached:
                print(f"  ⚠ checkpoint never reached in the crosswalk: {st}/{c} "
                      f"(warning until Phase 4)")
    return p


def check_schedule(cw) -> list[str]:
    """Every crosswalk row's nb and milestone must appear in the generated
    schedule (loose token matching until schedule_data grows structured ids)."""
    p: list[str] = []
    rows = list(csv.DictReader(SCHEDULE.open()))
    materials = " || ".join(r["other_material"] for r in rows)
    milestones = " || ".join(r["milestone_developed"] for r in rows)
    for r in cw.get("rows", []):
        if r["nb"] not in materials:
            p.append(f"schedule: {r['nb']} (row {r['milestone']}) never appears "
                     f"in other_material")
        mnum = r["milestone"]
        if not re.search(rf"\b{mnum}\b", milestones):
            p.append(f"schedule: {mnum} never appears in milestone_developed")
    return p


def _brief_anchor_map() -> dict[str, set[int]]:
    """milestone -> chapter numbers named in the brief's Book Anchor section."""
    out: dict[str, set[int]] = {}
    for brief in sorted(BRIEFS.glob("milestone_*.md")):
        m = re.match(r"milestone_(\d+)_", brief.name)
        if not m:
            continue
        mi = f"M{int(m.group(1))}"
        text = brief.read_text()
        # Surface 1: the EDR|AI submission-table row(s). RDSS lines also say
        # "ch. N", so scan only lines mentioning EDR.
        row: set[int] = set()
        for line in text.splitlines():
            if "EDR" in line:
                row.update(int(c) for c in
                           re.findall(r"ch\.?\s*(\d{1,2})", line, re.I))
        # Surface 2: the detailed "- Ch. N — [title](url) · companion" bullet
        # list inside the Book Anchor section (round-8 P1: this list drifted
        # while only the row was checked, handing students contradictory
        # graded requirements).
        bullets = {int(c) for c in
                   re.findall(r"^- Ch\.\s*(\d{1,2})\b", text, re.M)}
        out[mi] = (row, bullets)
    return out


def _crosswalk_chapter_map(arch, cw) -> dict[str, set[int]]:
    """milestone -> DISPLAY chapter numbers implied by home anchors.

    Display numbers are derived from manifest rank among active lessons
    (round-9 N2): the legacy filename prefix is not identity, and a lesson
    without one (every future insertion) would silently vanish from this map.
    """
    sys.path.insert(0, str(REPO / "scripts"))
    from book_manifest import active_lessons
    num = {l["id"]: l["display"] for l in active_lessons(arch)}
    out = {}
    for r in cw.get("rows", []):
        out[r["milestone"]] = {num[a["lesson"]] for a in r.get("assignments", [])
                               if a.get("home_anchor") and a["lesson"] in num}
    return out


def brief_agreement(arch, cw) -> list[str]:
    """Every brief's BOTH surfaces must equal the crosswalk EXACTLY, in both
    directions (round-9 N1: omissions in crosswalk-minus-brief and a full
    pre-migration reversion previously passed). The C1 migration exception is
    RETIRED — migration completed 2026-07-31; there is one legal state."""
    p: list[str] = []
    briefs = _brief_anchor_map()
    cwmap = _crosswalk_chapter_map(arch, cw)
    for mi, expected in cwmap.items():
        if not expected:
            continue
        if mi not in briefs:
            p.append(f"briefs[{mi}]: no brief found for a crosswalk milestone")
            continue
        row, bullets = briefs[mi]
        for name, got in (("submission row", row), ("Book Anchor bullets", bullets)):
            if not got:
                p.append(f"briefs[{mi}]: the {name} surface is MISSING — both "
                         f"student-facing surfaces must state the anchors")
            elif got != expected:
                p.append(f"briefs[{mi}]: {name} lists {sorted(got)} but the "
                         f"crosswalk anchors {sorted(expected)} — the brief "
                         f"is a projection and may not drift")
    if not p:
        print("  ✓ milestone briefs equal the crosswalk on both surfaces")
    return p


def check_assessments(arch, assess) -> list[str]:
    p: list[str] = []
    ids = {l["id"] for l in arch["lessons"]}
    rank = {l["id"]: l["rank"] for l in arch["lessons"]}
    routes = set(arch["pathways"])
    for cf in assess.get("contract_fields", []):
        f = cf.get("field", "?")
        prog = cf.get("progression", {})
        for stage in ("defined_by", "worked_example_by", "faded_practice_by"):
            v = prog.get(stage)
            if v is None:
                p.append(f"assess[{f}]: missing progression stage `{stage}`")
            elif v not in ids and v != "conditional" and not str(v).startswith("tbd-"):
                p.append(f"assess[{f}]: unknown lesson {v!r} in {stage}")
        d, w = prog.get("defined_by"), prog.get("worked_example_by")
        if d in ids and w in ids and rank[w] < rank[d]:
            p.append(f"assess[{f}]: worked example ({w}) precedes definition ({d})")
        for c in cf.get("conditional", []):
            if c.get("route") not in routes:
                p.append(f"assess[{f}]: unregistered route {c.get('route')!r}")
            if c.get("worked_example_by") not in ids:
                p.append(f"assess[{f}]: unknown lesson in conditional")
    return p


def a2_scan(arch, leak, hard: bool) -> list[str]:
    p: list[str] = []
    rules = [(r["id"], re.compile(r["pattern"], re.I)) for r in leak.get("rules", [])]
    excl = {e["artifact"] for e in leak.get("structural_exclusions", [])}
    hits = []
    for l in arch["lessons"]:
        if l["state"] != "active" or l["id"] in excl:
            continue
        f = REPO / "book" / l["source"]
        text = " ".join(f.read_text(errors="ignore").lower().split())
        for rid, rx in rules:
            for m in rx.finditer(text):
                hits.append((l["id"], rid, m.group(0)))
    if hits:
        msg = (f"A2 leakage: {len(hits)} hit(s) in active EN chapter bodies "
               f"(hard gate at the v1 freeze)")
        if hard:
            p.append(msg)
            for h in hits[:20]:
                p.append(f"  A2 {h[0]}: [{h[1]}] {h[2]!r}")
        else:
            print(f"  ⚠ {msg}")
            agg: dict[tuple, int] = {}
            for lid, rid, _ in hits:
                agg[(lid, rid)] = agg.get((lid, rid), 0) + 1
            for (lid, rid), n in sorted(agg.items()):
                print(f"      {lid}: {rid} ×{n}")
    else:
        print("  ✓ A2 leakage: no hits in active EN chapter bodies")
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a2-advisory", action="store_true",
                    help="downgrade the A2 leakage scan to advisory; it is a "
                         "HARD GATE by default since the Phase-4 de-coursing "
                         "sweep cleared the chapter bodies")
    args = ap.parse_args()

    arch, cw, assess, leak = load(ARCH), load(CW), load(ASSESS), load(LEAK)
    # MANIFEST-level checks certify the manifests themselves; the lock is
    # written on their success. PROJECTION checks (briefs, and elsewhere
    # BOOK_MAP/material) verify generated artifacts are fresh — they fail the
    # run but must not withhold the lock, or the generators that FIX them
    # could never run (deadlock found by the N2 activation fixture).
    manifest_problems = []
    manifest_problems += check_architecture(arch)
    manifest_problems += check_station_specs(arch)
    manifest_problems += check_crosswalk(arch, cw)
    manifest_problems += check_schedule(cw)
    manifest_problems += check_assessments(arch, assess)
    manifest_problems += a2_scan(arch, leak, hard=not args.a2_advisory)

    if manifest_problems:
        print(f"✗ book architecture validation: {len(manifest_problems)} problem(s)")
        for x in manifest_problems:
            print("   ", x)
        LOCK.unlink(missing_ok=True)
        return 1

    # PROJECTION checks: the TOC block and the studio pages are generated
    # artifacts (D38) — stale ones fail the run but never withhold the lock.
    projection_problems = brief_agreement(arch, cw)
    projection_problems += check_toc(arch)
    projection_problems += check_station_pages(arch)

    LOCK.write_text(json.dumps({
        "validator_version": VALIDATOR_VERSION,
        "manifests": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (ARCH, CW, ASSESS, LEAK)},
    }, indent=2) + "\n")
    n_active = sum(1 for l in arch["lessons"] if l["state"] == "active")
    n_planned = sum(1 for l in arch["lessons"] if l["state"] == "planned")
    if projection_problems:
        print(f"✗ generated projections are STALE: {len(projection_problems)} "
              f"problem(s) — manifests are valid (lock written); regenerate")
        for x in projection_problems:
            print("   ", x)
        return 1
    print(f"✓ book architecture consistent — {n_active} active + {n_planned} "
          f"planned lessons, {len(arch['stations'])} stations, home anchors "
          f"partition, schedule + assessments aligned; lock written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
