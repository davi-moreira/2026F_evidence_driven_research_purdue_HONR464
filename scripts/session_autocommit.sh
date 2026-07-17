#!/usr/bin/env bash
# session_autocommit.sh — Claude Code Stop-hook: commit + push at the end of a session/turn.
#
# Wired in .claude/settings.local.json (personal, gitignored) as a "Stop" hook so it
# runs every time a Claude Code turn finishes. The guardrails below make it a no-op on
# ordinary conversational turns, so in practice it only acts after a turn that changed
# tracked files.
#
# Guardrails (the "build it with guardrails" choices):
#   - No-op when there are no changes to tracked files (the common case).
#   - Stages tracked changes only (`git add -u`) — NEVER `git add .`/`-A`, so stray
#     untracked artifacts (notebooks/*.html, *_files/, large CSVs, secrets, gitignored
#     instructor notebooks) are never swept in. New files you still `git add` yourself.
#   - If content files changed (.qmd / .ipynb / _quarto.yml / images), run the Quarto
#     render first and stage docs/ so the published site never goes stale.
#   - Tolerant: a failed render or push logs to stderr but never aborts the session.
#
# Escape hatches:
#   - Disable without editing JSON:  touch .claude/.autocommit-off
#   - Dry run (print actions, change nothing):  AUTOCOMMIT_DRYRUN=1

set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR" 2>/dev/null || exit 0

log() { echo "[session-autocommit] $*" >&2; }

# Off-switch.
if [ -f "$PROJECT_DIR/.claude/.autocommit-off" ]; then
  log "disabled via .claude/.autocommit-off — skipping"
  exit 0
fi

DRY="${AUTOCOMMIT_DRYRUN:-0}"
run() { if [ "$DRY" = "1" ]; then log "DRY: $*"; else eval "$@"; fi; }

# Only operate inside a git work tree.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

# No-op when nothing in tracked files changed (working tree + index both clean).
if git diff --quiet && git diff --cached --quiet; then
  exit 0
fi

QUARTO="/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto"

# Which tracked files changed (working tree + already-staged), excluding rendered output.
changed="$(printf '%s\n%s\n' "$(git diff --name-only)" "$(git diff --cached --name-only)" | sort -u)"
needs_render="$(printf '%s\n' "$changed" | grep -iE '\.qmd$|\.ipynb$|_quarto\.yml$|\.(png|jpe?g|svg|gif)$' | grep -v '^docs/' || true)"

if [ -n "$needs_render" ]; then
  if [ -x "$QUARTO" ]; then
    log "content changed -> quarto render"
    run "\"$QUARTO\" render >&2 2>&1" || log "quarto render failed; committing without a fresh docs/"
  else
    log "content changed but quarto binary not found; committing without a fresh docs/"
  fi
fi

# Stage tracked modifications/deletions only.
run "git add -u"
# Rendering can create NEW files under docs/; stage those (scoped to docs/ only — safe).
if [ -n "$needs_render" ]; then
  run "git add docs >/dev/null 2>&1" || true
fi

# Anything actually staged? (In dry-run, the index is unchanged, so just report and stop.)
if [ "$DRY" = "1" ]; then
  log "DRY: would commit + push the staged tracked changes on branch $(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
  exit 0
fi
if git diff --cached --quiet; then
  exit 0
fi

git commit -m "chore: Session auto commit (Claude Code Stop hook)

Automated commit + push at the end of a Claude Code session/turn.
Tracked changes only; docs/ re-rendered when content changed.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>" >&2 2>&1 || { log "commit failed"; exit 0; }

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
git push origin "$branch" >&2 2>&1 || log "push failed (offline?) — commit is local, will go up next time"
exit 0
