#!/usr/bin/env bash
#
# make_seed.sh — Seed a NEW course directory from this repo.
#
# Copies the *portable core* (notebooks, AI operating manual, planning docs,
# templates, scripts, instructor materials) and SKIPS everything heavy or
# semester-specific (173 GB of video, slides, rendered docs, grades, venv, .git).
#
# Usage, from anywhere:
#   bash scripts/make_seed.sh /full/path/to/NEW_COURSE_DIR
#
# Example (the 2026 Fall course, one level up in the predictive_analytics root):
#   bash scripts/make_seed.sh \
#     "/Users/dcordeir/Dropbox/academic/cursos/cursos-davi/predictive_analytics/2026F_predictive_analytics__QM474"
#
# It is a DRY-RUN by default. Re-run with --go to actually copy.

set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-}"
GO="${2:-}"

if [[ -z "$DEST" ]]; then
  echo "Usage: bash scripts/make_seed.sh /path/to/NEW_COURSE_DIR [--go]" >&2
  exit 1
fi

RSYNC_FLAGS=(-a --human-readable)
if [[ "$GO" == "--go" ]]; then
  echo ">>> COPYING  $SRC  ->  $DEST"
else
  RSYNC_FLAGS+=(--dry-run --itemize-changes)
  echo ">>> DRY RUN (no files copied). Re-run with '--go' as the 2nd argument to copy."
  echo ">>> Source: $SRC"
  echo ">>> Dest:   $DEST"
fi

mkdir -p "$DEST"

# --- EXCLUDES -------------------------------------------------------------
# Heavy media / generated / private / semester-specific. Edit to taste.
EXCLUDES=(
  # version control + envs + caches (start the new course's git fresh)
  ".git/" ".venv/" "venv/" "env/" ".quarto/" "_freeze/" ".Rproj.user/" ".Rhistory"
  ".ipynb_checkpoints/" "__pycache__/" "*.pyc" ".DS_Store" ".scratch/"
  # huge media — NEVER copy (173 GB + 7 GB + 2.3 GB)
  "videos/" "lecture_slides/" "_notebook_lm/"
  # generated output — regenerate in the new repo, don't carry stale renders
  "docs/"
  # downloaded datasets — re-download / re-link in the new course
  "notebooks/data/"
  # private / semester-specific — grades, announcements, this term's admin
  "_adm_stuff/" "_announcements/"
  # large media bags from one-off render artifacts
  "*_files/" "*.html"
)

ARGS=()
for e in "${EXCLUDES[@]}"; do ARGS+=(--exclude "$e"); done

rsync "${RSYNC_FLAGS[@]}" "${ARGS[@]}" "$SRC/" "$DEST/"

echo
echo ">>> Done."
if [[ "$GO" == "--go" ]]; then
  cat <<EOF

NEXT STEPS (also written in $DEST/NEW_COURSE_SETUP.md):
  1. cd "$DEST"
  2. git init && git add -A && git commit -m "chore: Seed 2026F course from 2026Summer core"
  3. Create the remote repo and push (see NEW_COURSE_SETUP.md, Step 4).
  4. Open Claude Code here and paste the bootstrap prompt from NEW_COURSE_SETUP.md.
EOF
fi
