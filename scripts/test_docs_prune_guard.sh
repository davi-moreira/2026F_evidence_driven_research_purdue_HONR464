#!/usr/bin/env bash
# test_docs_prune_guard.sh — prove the docs-prune guard blocks what it must and
# permits what it must, in a throwaway repo. Touches nothing real: no commits,
# no renders, no network, no Quarto. Runs in about a second.
#
#   bash scripts/test_docs_prune_guard.sh
#
# Each case builds a tiny fixture repo that mimics the real geometry: three book
# source projects (book/, book-pt/, book-es/) and their published output under
# docs/. Then it mutates docs/ the way a prune, a restructure, or a truncated
# render would, and asserts the guard's verdict.

set -uo pipefail

GUARD="$(cd "$(dirname "$0")" && pwd)/check_docs_prune.sh"
[ -r "$GUARD" ] || { echo "cannot find check_docs_prune.sh next to this test"; exit 1; }

pass=0; fail=0
ok()   { pass=$((pass+1)); printf '  \033[32m✓\033[0m %s\n' "$1"; }
bad()  { fail=$((fail+1)); printf '  \033[31m✗\033[0m %s\n' "$1"; }

# Build a fixture: 3 editions, 20 published pages each, all committed.
fixture() {
  local d; d="$(mktemp -d)"
  (
    cd "$d" || exit 1
    git init -q . && git config user.email t@t && git config user.name t
    mkdir -p .claude
    for bk in book book-pt book-es; do
      mkdir -p "$bk" "docs/$bk"
      printf 'project:\n  type: book\n' > "$bk/_quarto.yml"
      for i in $(seq 1 20); do printf '<html>page %s</html>\n' "$i" > "docs/$bk/p$i.html"; done
    done
    mkdir -p docs && echo '<html>site</html>' > docs/index.html
    git add -A >/dev/null && git commit -qm init
  ) || { echo "fixture build failed" >&2; return 1; }
  echo "$d"
}

# assert <label> <expected-rc> <mode> <dir>
assert() {
  local label="$1" want="$2" mode="$3" dir="$4" got
  ( cd "$dir" && bash "$GUARD" "$mode" >/dev/null 2>&1 )
  got=$?
  if [ "$got" = "$want" ]; then ok "$label (rc=$got)"; else bad "$label — wanted rc=$want, got rc=$got"; fi
}

echo "=== BLOCKING cases: the guard must refuse ==="

d=$(fixture); rm -rf "$d/docs/book" "$d/docs/book-pt" "$d/docs/book-es"
assert "full prune of all three editions" 1 --worktree "$d"; rm -rf "$d"

d=$(fixture); rm -rf "$d/docs/book"
assert "site render pruned EN only" 1 --worktree "$d"; rm -rf "$d"

d=$(fixture); rm -rf "$d/docs/book-pt"
assert "one book render failed (PT missing)" 1 --worktree "$d"; rm -rf "$d"

d=$(fixture); for f in "$d"/docs/book/p*.html; do : > "$f"; done
assert "truncated render: pages exist but are zero bytes" 1 --worktree "$d"; rm -rf "$d"

d=$(fixture); ( cd "$d" && rm -rf docs/book && git add -A >/dev/null )
assert "prune already STAGED (index mode)" 1 --index "$d"; rm -rf "$d"

d=$(fixture); ( cd "$d" && for f in docs/book/p*.html; do : > "$f"; done && git add -A >/dev/null )
assert "zero-byte pages STAGED (index mode)" 1 --index "$d"; rm -rf "$d"

d=$(fixture); rm -f "$d"/docs/book/p{1,2,3,4,5,6,7,8,9,10}.html
assert "half the EN pages gone (below 75% floor)" 1 --worktree "$d"; rm -rf "$d"

echo
echo "=== PERMITTED cases: the guard must not get in the way ==="

d=$(fixture)
assert "healthy tree" 0 --worktree "$d"; rm -rf "$d"

d=$(fixture); echo '<html>edited</html>' > "$d/docs/book/p1.html"
assert "ordinary content edit" 0 --worktree "$d"; rm -rf "$d"

d=$(fixture); rm -f "$d"/docs/book/p1.html "$d"/docs/book/p2.html
assert "two pages legitimately retired (18/20 = 90%)" 0 --worktree "$d"; rm -rf "$d"

# The case that killed the first design: a restructure that RENAMES every page.
d=$(fixture); mkdir -p "$d/docs/book/studios"
for i in $(seq 1 20); do mv "$d/docs/book/p$i.html" "$d/docs/book/studios/s$i.html"; done
assert "restructure: all 20 pages renamed, none lost" 0 --worktree "$d"; rm -rf "$d"

d=$(fixture); rm -rf "$d/docs/book-es" "$d/book-es"
assert "edition retired at source (book-es/ deleted too)" 0 --worktree "$d"; rm -rf "$d"

d=$(fixture); rm -rf "$d/docs/book"; touch "$d/.claude/.allow-docs-prune"
assert "prune with a fresh override sentinel" 0 --worktree "$d"; rm -rf "$d"

d=$(fixture); rm -rf "$d/docs/book"
( cd "$d" && AUTOCOMMIT_ALLOW_PRUNE=1 bash "$GUARD" --worktree >/dev/null 2>&1 )
[ $? = 0 ] && ok "prune with AUTOCOMMIT_ALLOW_PRUNE=1 (rc=0)" || bad "AUTOCOMMIT_ALLOW_PRUNE=1 did not override"
rm -rf "$d"

d=$(fixture); rm -rf "$d/docs/book"; touch -t 200001010000 "$d/.claude/.allow-docs-prune"
assert "STALE override (year 2000) must NOT excuse a prune" 1 --worktree "$d"; rm -rf "$d"

echo
echo "=== ROBUSTNESS: a broken guard must never read as 'safe' ==="

d=$(fixture); rm -rf "$d/docs/book"
( cd "$d" && DOCS_PRUNE_FLOOR=abc bash "$GUARD" --worktree >/dev/null 2>&1 )
[ $? = 1 ] && ok "garbage DOCS_PRUNE_FLOOR falls back to 75, still blocks" || bad "malformed floor disabled the guard"
rm -rf "$d"

d=$(fixture); rm -rf "$d/docs/book"
( cd "$d" && DOCS_PRUNE_FLOOR=0 bash "$GUARD" --worktree >/dev/null 2>&1 )
[ $? = 1 ] && ok "DOCS_PRUNE_FLOOR=0 cannot silently disable the guard" || bad "floor=0 disabled the guard"
rm -rf "$d"

d="$(mktemp -d)"; ( cd "$d" && git init -q . )
assert "repo with no HEAD reports 'cannot determine'" 3 --worktree "$d"; rm -rf "$d"

d="$(mktemp -d)"
assert "not a git repo at all reports 'cannot determine'" 3 --worktree "$d"; rm -rf "$d"

d=$(fixture); rm -rf "$d/docs/book" "$d/book"
assert "EN retired at source; PT/ES healthy" 0 --worktree "$d"; rm -rf "$d"

echo
echo "-------------------------------------------"
printf 'passed %d, failed %d\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
