#!/usr/bin/env python3
# Stop hook — enforce the standing Commit-AND-Render workflow (CLAUDE.md).
# If the PUBLIC repo has uncommitted tracked changes or unpushed commits when a
# turn ends, remind to render + commit + push. Adapted from QM670's hook suite.
#
# Safety contract:
#   * Advisory ONLY — never commits/pushes by itself.
#   * Reminds at most once per stop (respects stop_hook_active); can never loop.
#   * Fails OPEN (exit 0) on ANY error, so a bug here can never block a session.
#   * `git status --porcelain` respects .gitignore, so instructor notebooks,
#     session guides, _adm/, and local settings never trigger it.
import json
import subprocess
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("stop_hook_active"):
        return 0
    cwd = data.get("cwd") or "."

    def git(*args):
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                              text=True, timeout=10)

    try:
        inside = git("rev-parse", "--is-inside-work-tree")
        if inside.returncode != 0 or inside.stdout.strip() != "true":
            return 0
        dirty = git("status", "--porcelain").stdout.strip()
        unpushed = ""
        if git("rev-parse", "--abbrev-ref", "--symbolic-full-name",
               "@{u}").returncode == 0:
            unpushed = git("log", "--oneline", "@{u}..HEAD").stdout.strip()
    except Exception:
        return 0

    if not dirty and not unpushed:
        return 0

    parts = []
    if dirty:
        parts.append("uncommitted public changes in the working tree")
    if unpushed:
        parts.append("commit(s) not yet pushed to origin")
    reason = (
        "STANDING WORKFLOW (CLAUDE.md → 'Commit AND Render'): there are "
        + " and ".join(parts) + ". Before ending the turn: (1) if any .qmd or "
        "student notebook changed, run quarto render and stage docs/; "
        "(2) commit + push the public course changes — stage files BY NAME, "
        "never instructor notebooks, session_guides/, or _adm/ (sanity-check "
        "`git status` first); (3) share the live course-page link for what "
        "changed. If Davi explicitly asked to hold the commit, say so briefly "
        "and it is fine to stop."
    )
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
