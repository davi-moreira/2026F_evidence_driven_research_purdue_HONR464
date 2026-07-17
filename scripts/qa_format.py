"""Convert inline-paragraph Q&A blocks to the nb09 blockquote convention.

The nb09 convention is:
    > **A question that often comes up here:** *"<question>"* <answer prose>
(blockquote prefix, bold opener with colon, italic question in double quotes,
single paragraph of flowing prose).

This script rewrites the inline-paragraph form used in earlier drafts:
    A question that often comes up here is *"<question>"* <answer prose>
into the nb09 form, idempotently.

Usage:
    python scripts/qa_format_to_nb09.py notebooks/nb11_decision_trees_student.ipynb [more notebooks...]
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

OPENERS = [
    ("A question that often comes up here is ",   "**A question that often comes up here:** "),
    ("A question that often comes up at this point is ", "**A question that often comes up at this point:** "),
    ("A common follow-up question is ",            "**A common follow-up question:** "),
]


def transform_cell_source(src: str) -> tuple[str, int]:
    """Return (new_src, n_changes). Idempotent — already-formatted blocks are skipped."""
    lines = src.split("\n")
    new_lines: list[str] = []
    n_changes = 0
    for line in lines:
        # Already in the nb09 blockquote form? leave it alone.
        if line.lstrip().startswith("> **A question that often comes up"):
            new_lines.append(line)
            continue
        # Already bolded but not blockquoted? add the blockquote prefix.
        if line.lstrip().startswith("**A question that often comes up"):
            new_lines.append("> " + line.lstrip())
            n_changes += 1
            continue
        # Inline-paragraph form — rewrite to bolded+blockquoted opener.
        matched = False
        for old, new in OPENERS:
            if old in line:
                new_line = line.replace(old, new, 1)
                new_line = "> " + new_line.lstrip()
                new_lines.append(new_line)
                n_changes += 1
                matched = True
                break
        if not matched:
            new_lines.append(line)
    return "\n".join(new_lines), n_changes


def process_notebook(path: Path) -> int:
    nb = json.loads(path.read_text())
    total_changes = 0
    cells_touched: list[int] = []
    for ci, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "markdown":
            continue
        was_list = isinstance(cell["source"], list)
        src = "".join(cell["source"]) if was_list else cell["source"]
        new_src, n_changes = transform_cell_source(src)
        if n_changes > 0:
            cell["source"] = [new_src] if was_list else new_src
            total_changes += n_changes
            cells_touched.append(ci)
    if total_changes > 0:
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    print(f"{path.name}: {total_changes} Q&A block(s) reformatted in cells {cells_touched}")
    return total_changes


def main() -> int:
    paths = [Path(p) for p in sys.argv[1:]]
    if not paths:
        print("usage: python scripts/qa_format_to_nb09.py <notebook> [more...]", file=sys.stderr)
        return 2
    total = 0
    for p in paths:
        total += process_notebook(p)
    print(f"\nTotal reformatted: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
