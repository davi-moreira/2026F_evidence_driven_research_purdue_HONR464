#!/usr/bin/env bash
# check_docs_prune.sh — refuse to publish a pruned or emptied book edition.
#
# WHY THIS EXISTS
# Rendering the SITE project prunes docs/book, docs/book-pt and docs/book-es:
# they are excluded inputs, so Quarto deletes them. They come back only when
# book/, book-pt/ and book-es/ are rendered afterwards. Between those two steps
# there is a window, minutes long, in which the published book editions do not
# exist on disk. Committing in that window takes all three books offline on
# GitHub Pages. It has happened repeatedly, from BOTH the Stop-hook path and the
# manual "build: Render Quarto site" path.
#
# WHAT IT CHECKS
# For each edition whose SOURCE project still exists, are its published pages
# present and non-empty RIGHT NOW? Completeness of the current tree — not
# survival of the paths HEAD happened to have. That distinction matters: a
# rename or restructure preserves the page count and passes, while a prune
# reads zero and blocks.
#
#   check_docs_prune.sh --worktree   what is on disk   (before staging)
#   check_docs_prune.sh --index      what is staged    (before committing)
#
# EXIT CODES
#   0  verified safe
#   1  prune detected — short edition names on stdout
#   3  cannot determine (not a repo, no HEAD, nothing published yet)
#   2  usage error
# Callers must treat anything that is not a clean 0 as "do not publish".
#
# OVERRIDES, for a genuine deletion
#   touch .claude/.allow-docs-prune     honoured for 24h, then ignored
#   AUTOCOMMIT_ALLOW_PRUNE=1            single invocation
#   git commit --no-verify              bypasses the pre-commit wiring
# Retiring an edition outright needs NO override: delete book-es/ and the
# edition stops being protected, because its source project is gone.

set -uo pipefail

EDITIONS="book book-pt book-es"

# Percentage of an edition's published pages that must be present. Sanitised:
# a malformed value must not kill the guard, and must not silently disable it.
FLOOR="${DOCS_PRUNE_FLOOR:-75}"
case "$FLOOR" in ''|*[!0-9]*) FLOOR=75 ;; esac
[ "$FLOOR" -ge 1 ] 2>/dev/null || FLOOR=75

MODE="worktree"
case "${1:-}" in
  ""|--worktree) MODE="worktree" ;;
  --index)       MODE="index" ;;
  *) echo "usage: check_docs_prune.sh [--worktree|--index]" >&2; exit 2 ;;
esac

say() { echo "[docs-prune-guard] $*" >&2; }

root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 3
[ -n "$root" ] || exit 3
cd "$root" 2>/dev/null || exit 3
git rev-parse --verify -q HEAD >/dev/null 2>&1 || exit 3

# ---- documented human overrides ---------------------------------------------
if [ "${AUTOCOMMIT_ALLOW_PRUNE:-0}" = "1" ]; then
  say "override in effect: AUTOCOMMIT_ALLOW_PRUNE=1"
  exit 0
fi
SENTINEL="$root/.claude/.allow-docs-prune"
if [ -f "$SENTINEL" ]; then
  if [ -n "$(find "$SENTINEL" -maxdepth 0 -mmin -1440 2>/dev/null)" ]; then
    say "override in effect: .claude/.allow-docs-prune (expires 24h after its mtime)"
    exit 0
  fi
  say "ignoring .claude/.allow-docs-prune — older than 24h; 'touch' it again to re-arm"
fi

# ---- the check ---------------------------------------------------------------
short=""
checked=0

for bk in $EDITIONS; do
  # No source project -> the edition was retired on purpose. Not our business.
  [ -f "$bk/_quarto.yml" ] || continue

  # How many pages does the published edition have in HEAD? If none, it has
  # never been published and there is nothing to protect.
  total="$(git ls-tree -r --name-only HEAD -- "docs/$bk" 2>/dev/null \
             | grep -c '\.html$' || true)"
  [ "${total:-0}" -gt 0 ] || continue

  # Respect a checkout that git deliberately did not materialise (sparse or
  # skip-worktree); absent files there are not a prune.
  if [ "$MODE" = "worktree" ]; then
    hidden="$(git ls-files -v -- "docs/$bk" 2>/dev/null | grep -c '^[Sh]' || true)"
    if [ "${hidden:-0}" -gt 0 ]; then
      say "skipping docs/$bk — sparse or skip-worktree checkout"
      continue
    fi
  fi

  # Completeness of the CURRENT tree: how many non-empty pages exist now.
  if [ "$MODE" = "worktree" ]; then
    kept="$(find "docs/$bk" -type f -name '*.html' -size +0c 2>/dev/null | wc -l | tr -d ' ')"
  else
    # Staged content, by blob size: a page staged as zero bytes is NOT kept.
    kept="$(git ls-files --stage -z -- "docs/$bk" 2>/dev/null \
              | tr '\0' '\n' \
              | awk '$4 ~ /\.html$/ {print $2}' \
              | git cat-file --batch-check='%(objectsize)' 2>/dev/null \
              | awk '$1 > 0 {n++} END {print n+0}')"
  fi
  kept="${kept:-0}"
  checked=$((checked + 1))

  if [ $((kept * 100)) -lt $((total * FLOOR)) ]; then
    short="$short $bk"
    if [ "$kept" -eq 0 ]; then
      say "docs/$bk: 0 of $total published pages present — this is a prune."
      say "   restore it with:  quarto render $bk/"
    else
      say "docs/$bk: only $kept of $total published pages present (floor ${FLOOR}%)."
      say "   if this is an intended restructure:  touch .claude/.allow-docs-prune"
    fi
  fi
done

[ "$checked" -gt 0 ] || exit 3

if [ -n "$short" ]; then
  echo "${short# }"
  exit 1
fi
exit 0
