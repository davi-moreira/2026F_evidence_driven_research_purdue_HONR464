#!/usr/bin/env python3
"""nbbuild.py — build → execute → strip → validate one topic notebook.

Authoring convention: each notebook's cells live in a LOCAL, gitignored source
module `_production_kit/nb_sources/nbNN_<slug>.py` exporting

    CELLS: list[tuple[str, str]]     # ("md" | "code", source)

(the module contains INSTRUCTOR SOLUTION content, hence gitignored — the
committed artifact is the generated student notebook only). This script:

  1. writes notebooks/instructor/nbNN_<slug>_instructor.ipynb (nbformat v4)
  2. executes it end-to-end with nbclient (kernel: repo .venv, cwd: repo root,
     timeout 300s/cell) — any raised error fails the build
  3. generates the student file via scripts/make_student.py logic
  4. runs scripts/validate_notebooks.py on the pair
  5. refreshes schedule.qmd badges (scripts/update_schedule_badges.py)

Milestone studio notebooks build the same way: `nbbuild.py ms04` reads
`_production_kit/nb_sources/ms04_<slug>.py`, writes the ms instructor/student
pair, and validates it with the reduced studio contract. Studio notebooks carry
no schedule badge, so the badge refresh runs only when a topic notebook (nbNN)
was built.

Usage: .venv/bin/python scripts/nbbuild.py nb00 [nb01 ...] [ms04 ...] [--no-exec]
"""
from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from notebooks_map import (  # noqa: E402
    NOTEBOOKS, MS_NOTEBOOKS, instructor_filename, ms_instructor_filename,
)

SOURCES = REPO / "_production_kit" / "nb_sources"


def load_cells(slug: str):
    src = SOURCES / f"{slug}.py"
    if not src.exists():
        sys.exit(f"✗ source module missing: {src}")
    spec = importlib.util.spec_from_file_location(slug, src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CELLS


def _write_instructor(cells, out: Path) -> Path:
    nb = nbformat.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python",
                       "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
        "colab": {"provenance": []},
    }
    for kind, source in cells:
        if kind == "md":
            nb.cells.append(nbformat.v4.new_markdown_cell(source))
        elif kind == "code":
            nb.cells.append(nbformat.v4.new_code_cell(source))
        else:
            sys.exit(f"✗ unknown cell kind {kind!r}")
    nbformat.write(nb, out)
    print(f"✓ built {out.name} ({len(nb.cells)} cells)")
    return out


def build_instructor(n: int) -> Path:
    out = REPO / "notebooks" / "instructor" / instructor_filename(n)
    return _write_instructor(load_cells(NOTEBOOKS[n][0]), out)


def build_ms_instructor(n: int) -> Path:
    out = REPO / "notebooks" / "instructor" / ms_instructor_filename(n)
    return _write_instructor(load_cells(MS_NOTEBOOKS[n][0]), out)


def execute(path: Path) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=300, kernel_name="python3",
                            resources={"metadata": {"path": str(REPO)}})
    client.execute()
    nbformat.write(nb, path)
    n_out = sum(1 for c in nb.cells if c.cell_type == "code" and c.get("outputs"))
    print(f"✓ executed {path.name} — {n_out} code cells produced output")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_exec = "--no-exec" not in sys.argv
    if not args:
        sys.exit("usage: nbbuild.py nbNN|msNN [...]")
    built_topic = False
    for a in args:
        is_ms = a.lower().startswith("ms")
        n = int(re.sub(r"\D", "", a))
        instr = build_ms_instructor(n) if is_ms else build_instructor(n)
        built_topic = built_topic or not is_ms
        if do_exec:
            execute(instr)
        subprocess.run([sys.executable, str(REPO / "scripts" / "make_student.py"),
                        str(instr)], check=True)
        tag = f"ms{n:02d}" if is_ms else f"nb{n:02d}"
        subprocess.run([sys.executable, str(REPO / "scripts" / "validate_notebooks.py"),
                        tag], check=True)
    # Studio (msNN) notebooks carry no schedule badge; refresh only for topics.
    if built_topic and "--no-badges" not in sys.argv:
        subprocess.run([sys.executable,
                        str(REPO / "scripts" / "update_schedule_badges.py")], check=True)


if __name__ == "__main__":
    main()
