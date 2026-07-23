# Troubleshooting

Common issues encountered while developing or deploying HONR 46400 course materials,
with proven solutions. Rewritten 2026-07-23 for the v2 course (DECISIONS.md D17–D21):
the MGMT474-era CV-first / test-set section is gone, and the notebook-build, schedule,
voice, and instructor-page entries reflect this repo's actual pipeline (see
`COURSE_MATERIAL_WORKFLOW.md`).

---

## Issue: Quarto Render Fails

**Symptoms:** Error when running `quarto render`.

**Solutions:**
1. Check `_quarto.yml` syntax (YAML is whitespace-sensitive).
2. Verify all `.qmd` files have valid frontmatter.
3. Check for broken links in `.qmd` files.
4. Try rendering individual files first: `quarto render index.qmd`.
5. Confirm Quarto is installed at the expected path: `/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto --version`.
6. If the failure is in the `post-render` step (`protect_instructor_page.py`), see
   "Instructor Page Shipped Unencrypted" below — the render itself may have produced
   the pages correctly.

---

## Issue: GitHub Pages Not Updating

**Symptoms:** Website shows old content after `git push`.

**Solutions:**
1. **Most common cause: forgot to render and commit `docs/`.** Run `quarto render`, then `git add docs/`, `git commit`, `git push`.
2. Wait 2–5 minutes (first deployment can take longer).
3. Check GitHub Actions: Repository → Actions tab.
4. Verify `docs/` directory exists and contains `index.html`.
5. Hard refresh browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows).
6. Check GitHub Pages settings: Settings → Pages → main branch, `/docs` folder.

---

## Issue: Git Push Rejected

**Symptoms:** `! [rejected] main -> main (fetch first)`.

**Solutions:**
1. Pull first: `git pull origin main`.
2. Resolve any conflicts.
3. Push again: `git push origin main`.

---

## Issue: Notebook Build Fails During Execution

**Symptoms:** `.venv/bin/python scripts/nbbuild.py nbNN` errors while executing the
instructor notebook (an exception raised in a cell aborts the build; the student file
is never generated).

**Cause:** `nbbuild.py` runs the built notebook end-to-end with nbclient before
stripping — any raised error fails the build by design.

**Solutions:**
1. Always invoke with the **repo venv**: `.venv/bin/python scripts/nbbuild.py nbNN`.
   The build uses the `python3` kernel from that venv; running under system Python
   loses the installed libraries (numpy, pandas, matplotlib, scipy, statsmodels,
   scikit-learn, networkx).
2. nbclient executes with **cwd = repo root**, so relative paths in a cell resolve
   from the repo, not from `notebooks/`.
3. For data loads, use `load_course_data()` — it fetches the GitHub raw URL first and
   **falls back to the local `notebooks/data/` copy**, so the build works offline and
   before the file is pushed. Do not hardcode absolute or `/content/` Colab paths.
4. Read the traceback: it names the failing cell. Fix the cell **source** in
   `_production_kit/nb_sources/nbNN_<slug>.py`, never the built `.ipynb`, then rebuild.
5. To iterate on structure without paying the execution cost, `--no-exec` skips the
   run — but a shippable notebook must build cleanly **with** execution.

---

## Issue: Instructor-Solution Cells Leaking to Student Notebook

**Symptoms:** The generated `*_student.ipynb` still shows solution content.

**Cause:** A solution cell did not contain the literal marker `INSTRUCTOR SOLUTION`,
so the strip step in `nbbuild.py` did not remove it. (`validate_notebooks.py` also
fails any student file that still contains the marker.)

**Solutions:**
1. Markdown solution headings must read: `### INSTRUCTOR SOLUTION — Exercise N`.
2. Code solution cells must start with `# INSTRUCTOR SOLUTION` as the first comment.
3. Hidden markdown solutions (e.g., a worked "Reading the evidence") must start with
   `<!-- INSTRUCTOR SOLUTION -->` as the first line.
4. Student placeholder cells (`### YOUR ANSWER HERE:` / `# YOUR SOLUTION HERE`) must
   NOT contain `INSTRUCTOR SOLUTION`.
5. Fix the marker in the **cell source** and rebuild — never edit the student `.ipynb`
   by hand: `.venv/bin/python scripts/nbbuild.py nbNN`.

---

## Issue: Voice Lint Fails

**Symptoms:** `voice_lint_notebooks.py` exits non-zero (also fired by the `PostToolUse`
hook whenever a student notebook is written: "voice lint FAILED — fix before committing").

**Cause:** A student-facing cell broke a CLAUDE.md voice rule.

**Solutions:**
1. **"students" as a third-party noun** in a student cell — rewrite in second person
   (`you`), neutral imperative, or first person. `Student's t` (the test name) is the
   only acceptable match. Facilitation/instructor voice belongs only in the session
   guide, never a student cell.
2. **Em-dash budget** exceeded (≤ 1 per markdown cell, ≤ 20 per notebook, D14) —
   replace dash-chained clauses with periods, commas, or bold lead-ins
   (`**Why this matters:**`, `**The catch:**`).
3. **Dates or "Meeting M#"** (D13) — remove them. Position is expressed only as
   lecture labels (`# Lecture 1`, `**Topic NN · N lecture(s)**`); dates live only on
   `schedule.qmd` and in the milestone briefs.
4. **Fourth-wall meta-references** ("fabricated / planted / invented for this
   exercise") — delete; never annotate the Sources section with construction asides.
5. Fix the **cell source** and rebuild; re-run `.venv/bin/python
   scripts/voice_lint_notebooks.py` until clean.

---

## Issue: `build_meeting_schedule.py` Fails on a Backbone Mismatch

**Symptoms:** `python3 scripts/build_meeting_schedule.py` exits non-zero with a
message like `meeting N: date/day/modality != backbone`, `expected 43 meetings`, or
`backbone has M rows`.

**Cause:** The schedule data in `scripts/schedule_data/partN.py` disagrees with the
verified calendar backbone (`planning/CALENDAR_BACKBONE.csv`). `build_meeting_schedule.py`
validates every row against the backbone and refuses to write on any mismatch — this
gate is deliberate.

**Solutions:**
1. If the **calendar itself** changed (a date, day, or modality moved), the backbone
   is stale. Regenerate it first, then rebuild the schedule:
   ```bash
   python3 scripts/validate_calendar.py --emit-csv   # rewrite planning/CALENDAR_BACKBONE.csv
   python3 scripts/build_meeting_schedule.py
   ```
   `validate_calendar.py` is the single source of truth for the 43-meeting spine
   (41 in-person + 2 async); if it fails, the meeting dates are wrong, not the data.
2. If the **backbone is correct** and a row is wrong, fix that meeting in
   `scripts/schedule_data/partN.py` — the error names the meeting number and field.
   `srl_slot` / `srl_focus` / `cb_reading` may be empty (studios, async, Week 1); all
   other fields are required.
3. Never hand-edit `planning/MEETING_SCHEDULE.{csv,md}` — they are generated.

---

## Issue: Instructor Page Shipped Unencrypted

**Symptoms:** `docs/instructor.html` contains readable instructor content instead of
the password gate, or a diff shows cleartext instructor material staged.

**Cause:** The page was hand-edited or committed without going through `quarto render`,
so the `post-render` step (`protect_instructor_page.py`) never ran. That step AES-GCM
encrypts the page behind the `eureka` gate and is idempotent.

**Solutions:**
1. Re-run the full render so `post-render` fires, then commit the encrypted page:
   ```bash
   /Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto render
   git add docs/instructor.html && git commit -m "build: re-encrypt instructor page"
   ```
2. If the render errors in that step with a crypto import failure, the venv is missing
   the dependency: `.venv/bin/pip install cryptography`, then re-render.
3. Never hand-edit generated pages under `docs/`; edit the generator and re-render.
   The gate is a courtesy lock — the real protection is the private repo the page
   links to (Colab/GitHub require the instructor's login).

---

## Issue: Session-Autocommit Stop Hook Pushed Mid-Work

**Symptoms:** A commit + push happened at the end of a turn before the week's unit was
finished (e.g., a notebook committed before its schedule/guide/brief caught up).

**Cause:** The `Stop` hook `scripts/session_autocommit.sh` (wired in the gitignored
`.claude/settings.local.json`) stages tracked changes and pushes at the end of a turn.
It renders and stages `docs/` when content files changed, so the site never goes stale
— but it also means an interim tree gets published.

**Solutions:**
1. **Keep the working tree coherent at the end of every turn.** Finish the unit's
   Phase A–E (or at least a self-consistent slice) before stopping, so any autocommit
   captures a valid state. The hook stages `git add -u` only (tracked files), never
   `-A`, so untracked artifacts and gitignored instructor material are never swept in.
2. To pause the hook for a work session, use its off-switch (no JSON edit):
   `touch .claude/.autocommit-off` (remove the file to re-enable).
3. To preview without changing anything: `AUTOCOMMIT_DRYRUN=1`.
4. If it pushed an interim state, just continue — the next coherent turn's autocommit
   (or a manual render + commit) supersedes it. Do not force-push to rewrite history.

---

## Issue: Notebook Won't Run in Colab

**Symptoms:** Errors when clicking "Open in Colab".

**Solutions:**
1. Check the Colab badge URL — must match the notebook filename exactly, including the
   `notebooks/student/` path and the `_student.ipynb` suffix (see "Colab Badge Points
   to Wrong File").
2. Verify all imports are standard scientific-Python (numpy, pandas, matplotlib,
   scipy, statsmodels, scikit-learn, networkx) or a first-cell `pip install`.
3. Test in a fresh Colab runtime: Runtime → Disconnect and delete runtime.
4. Data must load via `load_course_data()` (GitHub raw URL first, local fallback),
   never a hardcoded local or `/content/` path.

---

## Issue: Missing Files After Clone

**Symptoms:** Expected files not present after `git clone` of the public repo.

**Solutions:**
1. Check `.gitignore` — many files are excluded by design.
2. Cell sources (`_production_kit/`), instructor notebooks (`notebooks/instructor/`),
   session guides (`session_guides/`), and the local instructor-repo clone
   (`_instructor_repo/`) are gitignored — instructor material lives in the **private**
   repo, reached via `scripts/sync_instructor_repo.sh`.
3. `docs/` should be present — if not, run `quarto render`.

---

## Issue: Dollar Signs Render as Math in the Notebook

**Symptoms:** A markdown cell mentioning `$50,000` shows broken LaTeX or eats
subsequent text; `validate_notebooks.py` flags an unescaped `$<digit>` / `~<digit>`.

**Cause:** Unescaped `$` triggers MathJax; unescaped `~` triggers subscript/strike.

**Solution:** In markdown cells (NOT code cells), always escape: `\$50,000`,
`\~30 sources`. Fix the **cell source** and rebuild.

---

## Issue: Colab Badge Points to Wrong File

**Symptoms:** Clicking the badge opens the instructor notebook (404 on the public
repo) or the wrong topic.

**Cause:** Badge URL was not updated when the notebook was generated/renamed.

**Solution:** Edit the header markdown cell in the **cell source**. The badge URL must be:
```
https://colab.research.google.com/github/davi-moreira/2026F_evidence_driven_research_purdue_HONR464/blob/main/notebooks/student/nbNN_topic_student.ipynb
```
The path must include `notebooks/student/` and end in `_student.ipynb`, never
`_instructor.ipynb`.
