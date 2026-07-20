#!/usr/bin/env python3
"""make_dataset_zip.py — build the single student-facing dataset bundle.

notebooks/data/ is the course's single canonical dataset folder (CLAUDE.md,
Dataset Distribution rule / D15). This script zips every CSV plus the README
into notebooks/data/honr46400_datasets.zip, which the Material and Schedule
pages link as the offline download. Rerun whenever a dataset is added or
changed, then commit the zip.

The archive is deterministic (fixed timestamps, sorted entries) so rebuilding
without a data change produces a byte-identical file and no git churn.

Usage: python3 scripts/make_dataset_zip.py
"""
from __future__ import annotations

import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "notebooks" / "data"
OUT = DATA / "honr46400_datasets.zip"

# Fixed timestamp keeps the archive reproducible run-to-run.
STAMP = (2026, 8, 24, 0, 0, 0)  # first day of class


def main() -> None:
    files = sorted(DATA.glob("*.csv")) + [DATA / "README.md"]
    missing = [f.name for f in files if not f.exists()]
    if missing:
        raise SystemExit(f"✗ missing dataset files: {missing}")

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            info = zipfile.ZipInfo(f"honr46400_datasets/{f.name}", date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, f.read_bytes())

    kb = OUT.stat().st_size / 1024
    print(f"✓ wrote {OUT.relative_to(REPO)} ({len(files)} files, {kb:.0f} KB)")


if __name__ == "__main__":
    main()
