#!/usr/bin/env bash
# sync_instructor_repo.sh — push instructor material to the PRIVATE repo that
# backs the password-gated Instructor tab (CLAUDE.md, Instructor-First rule).
#
# Syncs notebooks/instructor/, session_guides/, and notebooks/data/ into a
# local clone at _instructor_repo/ (gitignored) and pushes. Run after every
# notebook build (scripts/nbbuild.py) or session-guide regeneration.
#
# Usage: bash scripts/sync_instructor_repo.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PRIVATE_SLUG="davi-moreira/2026F_evidence_driven_research_purdue_HONR464_instructor"
CLONE_DIR="$REPO_ROOT/_instructor_repo"

if [ ! -d "$CLONE_DIR/.git" ]; then
  echo "· cloning $PRIVATE_SLUG into _instructor_repo/"
  gh repo clone "$PRIVATE_SLUG" "$CLONE_DIR"
fi

cd "$CLONE_DIR"
git pull --quiet --rebase 2>/dev/null || true   # empty repo has no upstream yet

mkdir -p notebooks/instructor notebooks/data session_guides
rsync -a --delete "$REPO_ROOT/notebooks/instructor/" notebooks/instructor/
rsync -a --delete "$REPO_ROOT/notebooks/data/"       notebooks/data/
rsync -a --delete "$REPO_ROOT/session_guides/"       session_guides/

cat > README.md <<'EOF'
# HONR 46400 — Instructor Material (PRIVATE)

Solution notebooks (`notebooks/instructor/`), session guides
(`session_guides/`), and course datasets (`notebooks/data/`) for
HONR 46400 Evidence-Driven Research (Fall 2026).

Do not share: instructor notebooks contain solutions. This repo is synced
automatically by `scripts/sync_instructor_repo.sh` in the public course repo —
do not edit here; edits will be overwritten on the next sync.

Open notebooks in Colab via the course site's Instructor tab (requires the
GitHub "Include private repos" authorization in Colab, one time).
EOF

git add -A
if git diff --cached --quiet; then
  echo "✓ instructor repo already up to date"
  exit 0
fi

n_nb=$(ls notebooks/instructor/*.ipynb 2>/dev/null | wc -l | tr -d ' ')
n_sg=$(ls session_guides/*.md 2>/dev/null | wc -l | tr -d ' ')
git commit --quiet -m "sync: ${n_nb} instructor notebooks, ${n_sg} session guides

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push --quiet -u origin HEAD
echo "✓ pushed to $PRIVATE_SLUG (${n_nb} notebooks, ${n_sg} guides)"
