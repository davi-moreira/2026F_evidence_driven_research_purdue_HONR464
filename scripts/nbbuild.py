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

Usage: .venv/bin/python scripts/nbbuild.py nb00 [nb01 ...] [--no-exec]
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from notebooks_map import NOTEBOOKS, instructor_filename  # noqa: E402

SOURCES = REPO / "_production_kit" / "nb_sources"


def load_cells(n: int):
    slug = NOTEBOOKS[n][0]
    src = SOURCES / f"{slug}.py"
    if not src.exists():
        sys.exit(f"✗ source module missing: {src}")
    spec = importlib.util.spec_from_file_location(slug, src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CELLS


def build_instructor(n: int) -> Path:
    cells = load_cells(n)
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
    out = REPO / "notebooks" / "instructor" / instructor_filename(n)
    nbformat.write(nb, out)
    print(f"✓ built {out.name} ({len(nb.cells)} cells)")
    return out


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
        sys.exit("usage: nbbuild.py nbNN [...]")
    for a in args:
        n = int(a.replace("nb", ""))
        instr = build_instructor(n)
        if do_exec:
            execute(instr)
        subprocess.run([sys.executable, str(REPO / "scripts" / "make_student.py"),
                        str(instr)], check=True)
        subprocess.run([sys.executable, str(REPO / "scripts" / "validate_notebooks.py"),
                        f"nb{n:02d}"], check=True)
    if "--no-badges" not in sys.argv:
        subprocess.run([sys.executable,
                        str(REPO / "scripts" / "update_schedule_badges.py")], check=True)


if __name__ == "__main__":
    main()
