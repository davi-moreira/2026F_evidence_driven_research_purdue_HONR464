#!/usr/bin/env bash
# Convert instructor notebooks to Markdown for NotebookLM ingestion.
#
# Usage:
#   scripts/sync_instructor_md.sh                       # convert all instructor notebooks
#   scripts/sync_instructor_md.sh activities/act09_*.ipynb # convert one (or several)
#
# Output: _notebook_lm/<basename>.md  (+ <basename>_files/ for embedded images)
#
# Wired to fire automatically from a Claude Code PostToolUse hook
# (.claude/settings.json) and can also be invoked manually or by fswatch.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

OUT_DIR="$REPO_ROOT/_notebook_lm"
NBCONVERT="$REPO_ROOT/.venv/bin/jupyter-nbconvert"

mkdir -p "$OUT_DIR"

if [[ ! -x "$NBCONVERT" ]]; then
  echo "sync_instructor_md: $NBCONVERT not found; skipping (no .venv with nbconvert)" >&2
  exit 0
fi

if [[ $# -gt 0 ]]; then
  TARGETS=("$@")
else
  shopt -s nullglob
  TARGETS=(notebooks/instructor/*_instructor.ipynb)
fi

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  echo "sync_instructor_md: no instructor notebooks found"
  exit 0
fi

converted=0
for nb in "${TARGETS[@]}"; do
  # Only act on instructor notebooks; silently skip anything else (lets the
  # hook pass through arbitrary edited paths without erroring).
  case "$(basename "$nb")" in
    *_instructor.ipynb) ;;
    *) continue ;;
  esac
  if [[ ! -f "$nb" ]]; then
    continue
  fi
  echo "→ $nb"
  "$NBCONVERT" --to markdown --output-dir "$OUT_DIR" "$nb" >/dev/null
  converted=$((converted + 1))
done

echo "sync_instructor_md: converted $converted notebook(s) → $OUT_DIR"
