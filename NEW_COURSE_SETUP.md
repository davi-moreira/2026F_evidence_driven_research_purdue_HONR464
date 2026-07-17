# HONR 46400 "Evidence-Driven Research" — New-Course Setup Guide

This guide sets up the new course repo at
`/Users/dcordeir/Dropbox/academic/cursos/cursos-davi/evidence_based_research/2026F_evidence_driven_research_purdue_HONR464`,
seeded from the **infrastructure** of
`2026Summer_predictive_analytics_purdue_MGMT474` but with the quantitative
**content spine deliberately left behind**.

> **Key framing.** Unlike the source repo's own `NEW_COURSE_SETUP.md` (which
> assumed "the SAME course, re-paced to a full semester"), HONR 46400 is a
> **different course** that *reuses the machinery* and *replaces the payload*.
> The Quarto site, `.claude` hooks, `scripts/` framework, planning-doc
> templates, instructor→student generation pattern, Brightspace pipeline,
> milestone/peer-eval scaffolding, and the MC-parity gate all transfer. The 21
> ML notebooks, the quiz/midterm/homework/handout banks, the Kaggle competition,
> the predictive final project, ISLP, and the CV-first / test-set-lock rule do
> **not** — they are designed fresh in a later curriculum session.

---

## What transfers (the KEEP / ADAPT / REPLACE map)

| Subsystem | Verdict | What it means for setup |
|---|---|---|
| **Quarto site** (`_quarto.yml`, `index/syllabus/schedule.qmd`, `styles.css`, `docs/`→Pages) | **KEEP shell / REPLACE content** | Site machinery + Purdue palette transfer verbatim; every page body is rewritten. `workflow.qmd` (essay about the ML course) is dropped. |
| **Notebook / activity engine** (`NOTEBOOK_TEMPLATE.md`, instructor→student marker strip, PAUSE-AND-DO, Gemini-prompt+verify, narrative Q&A) | **KEEP pattern / REPLACE payload** | The teaching skeleton + voice transfer; the 21 ML notebooks do **not** seed. New units are lighter, text/argumentation-first. |
| **Assessments** (quiz→D2L-CSV pipeline, midterm case-blueprint framing, `audit_answer_length.py` parity gate) | **KEEP pipeline / REPLACE items** | Quiz machinery + MC-parity gate are domain-agnostic; every item bank is rewritten. Kaggle competition dropped entirely. |
| **Research project spine** (4-milestone cadence, source-of-truth governance, rubric-per-milestone, peer-eval, URC poster) | **ADAPT — highest-value asset** | Maps almost 1:1 to gap→question→sources→method-justification→written report + **oral defense**. Strip `random_state`/test-set ceremony. |
| **Brightspace pipeline** (one MD page per unit, sequential release) | **KEEP structure / REPLACE content** | Re-paced to Fall MWF; multi-video-per-day mapping shrinks for in-person. |
| **Automation** (`make_seed.sh`, `sync_instructor_md.sh`, `session_autocommit.sh`, `voice_check_guides.py`, `analyze_course_eval.py`, `.claude` hook) | **KEEP** | Portable backbone. Prune `audit_cv_first.py` + `build_nb19.py`. Re-wire the autocommit Stop hook by hand (it lives in gitignored local settings). |
| **Operating docs** (`CLAUDE.md`, `DECISIONS.md`, `TROUBLESHOOTING.md`) | **ADAPT** | Keep 2 rules verbatim (Voice, Commit+Render), adapt most, REPLACE the CV-first rule with a research-integrity trio. |
| **Git / GitHub / deploy** (`.gitignore`, Pages model, commit conventions) | **KEEP** | ~90% portable; rename content-dir entries; new remote + Pages branch. |

**Bottom line of the review:** *no subsystem the course needs is missing* — each
has a home in the source. The real work is (a) building **14 fresh
research-methodology artifacts** (see the Gap List at the end) and (b) the
discipline of not letting the ML payload or stale logs ride along in the seed.

---

## Prerequisites / environment facts (verified 2026-07-16)

- Target dir **already exists and is empty**: `…/evidence_based_research/2026F_evidence_driven_research_purdue_HONR464/` — seeding into it is safe.
- **`gh` token is expired.** `gh auth status` reports the keyring token invalid for `davi-moreira`. **Run `gh auth refresh -h github.com` before Step 4** or the repo-create will fail.
- Quarto present at `/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto` (v1.9.36).
- Git identity set (Davi Moreira / davi.moreira@gmail.com); GitHub user `davi-moreira`.

---

## Step 0 — Seed strategy (Approach A, recommended)

Run a **one-off `rsync`** (rather than editing the shared `make_seed.sh`) that
carries the whole infra framework in one pass and *subtracts* the known-bad
content — a shorter, more auditable list than enumerating the good files by hand.
The excludes below drop (1) the source's own heavy/private/generated dirs and
(2) the entire quant content spine, so **no ML payload ever arrives** and there
are no "prune the notebooks afterward" steps.

## Step 1 — Create parent + seed

```bash
SRC="/Users/dcordeir/Dropbox/academic/cursos/cursos-davi/predictive_analytics/2026Summer_predictive_analytics_purdue_MGMT474"
DEST="/Users/dcordeir/Dropbox/academic/cursos/cursos-davi/evidence_based_research/2026F_evidence_driven_research_purdue_HONR464"

mkdir -p "$DEST"

# Shared exclude list (used for dry-run and real copy)
EXCL=(
  # vcs / env / cache / generated
  --exclude ".git/" --exclude ".venv/" --exclude "venv/" --exclude "env/"
  --exclude ".quarto/" --exclude "_freeze/" --exclude ".Rproj.user/"
  --exclude ".Rhistory" --exclude "*.Rproj" --exclude ".ipynb_checkpoints/"
  --exclude "__pycache__/" --exclude "*.pyc" --exclude ".DS_Store" --exclude ".scratch/"
  --exclude "docs/" --exclude "*_files/" --exclude "*.html" --exclude "~\$*"
  # heavy media (173GB+) / private / term-specific
  --exclude "videos/" --exclude "lecture_slides/" --exclude "_notebook_lm/"
  --exclude "_adm_stuff/" --exclude "_announcements/" --exclude "_archive/"
  # QUANT CONTENT SPINE — REPLACE, do NOT seed
  --exclude "notebooks/" --exclude "_quizzes/" --exclude "_midterm_exam/"
  --exclude "_homework/" --exclude "_lecture_notes/" --exclude "_handouts/"
  --exclude "_final_project/" --exclude "_course_case_competition/"
  --exclude "brightspace/" --exclude "_production_kit/"
)

# 1a. DRY RUN — inspect what would copy
rsync -a --human-readable --dry-run --itemize-changes "${EXCL[@]}" "$SRC/" "$DEST/"

# 1b. REAL COPY (local only, nothing published)
rsync -a --human-readable "${EXCL[@]}" "$SRC/" "$DEST/"
```

> Note: `_syllabus/` **is** seeded (it holds reusable Purdue/Daniels compliance
> assets). Step 2 prunes its stale term folder + Office lock files.

## Step 2 — Prune seed residue + reset carried-over files + create scaffold dirs

```bash
cd "$DEST"

# 2a. Remove quant-only scripts + the essay page + the wrong-framing setup guide
rm -f scripts/audit_cv_first.py scripts/build_nb19.py
rm -rf scripts/__pycache__
rm -f workflow.qmd                 # 461-line essay about the QM474 ML redesign
rm -f NEW_COURSE_SETUP.md          # replaced by THIS guide (copy this file in)

# 2b. Prune quant planning docs; KEEP + rename the reusable template
rm -f _project_docs/MGMT47400_Online4Week_Plan_2026Summer.md
rm -f _project_docs/claude_course_plan.md
mv _project_docs/NOTEBOOK_TEMPLATE.md _project_docs/ACTIVITY_TEMPLATE.md
#   KEEP (adapt later): COURSE_MATERIAL_WORKFLOW.md, DECISIONS.md,
#   TROUBLESHOOTING.md, COURSE_EVAL_ANALYSIS.md

# 2c. Clean image assets (keep the instructor photo)
find images -name ".DS_Store" -delete
rm -f images/mgmt_474_ai_logo_* images/logo_py*
#   images/davi_moreira_photo.JPG stays; add images/honr_464_logo.png later

# 2d. Prune _syllabus stale term + lock files (KEEP complementary_material/)
rm -rf _syllabus/2026Summer _syllabus/old_files _syllabus/_syllabus_docx 2>/dev/null
find _syllabus -name '~\$*' -delete 2>/dev/null || true

# 2e. Reset the carried-over ML history log to a fresh header (append-only from here)
cat > CONVERSATION_LOG.md <<'EOF'
# HONR 46400 — Conversation Log

Append-only project history. Seeded 2026-07-16 from the MGMT474 infra core;
ML content spine intentionally omitted.
EOF

# 2f. Rename the Q&A helper away from its nb09 lineage (re-key its strings later)
git mv 2>/dev/null scripts/qa_format_to_nb09.py scripts/qa_format.py || mv scripts/qa_format_to_nb09.py scripts/qa_format.py

# 2g. Create the empty scaffold dirs (committed vs gitignored noted)
mkdir -p activities                       # committed: light non-ML student activities
mkdir -p _research_project/2026Fall/rubric _research_project/2026Fall/template   # committed: milestone spine
mkdir -p session_guides                   # gitignored: in-class session plans (was video_guides/)
mkdir -p brightspace                      # gitignored: one LMS page per unit
mkdir -p _worksheets                      # gitignored: light per-unit practice (was _homework/)
mkdir -p _handouts _quizzes/2026Fall _peer_review   # gitignored
touch activities/.gitkeep _research_project/.gitkeep
```

## Step 3 — `git init` + first commit (local, reversible)

Stage **by name** (never `git add -A`) so no private dir, dataset, or temp file
slips in.

```bash
cd "$DEST"
git init
git branch -M main

# Confirm private dirs are ignored BEFORE staging
git check-ignore -v session_guides brightspace _worksheets _quizzes _adm_stuff _syllabus 2>/dev/null

# Update .gitignore content-dir names (see Step 6-I) before this commit, then:
git add _quarto.yml styles.css index.qmd syllabus.qmd schedule.qmd README.md CLAUDE.md LICENSE
git add .gitignore .claude/settings.json CONVERSATION_LOG.md
git add scripts/ _project_docs/ images/
git add activities/.gitkeep _research_project/.gitkeep

git status   # FINAL review — no _adm_stuff/, session_guides/, brightspace/, *_instructor*.ipynb

git commit -m "chore: Seed HONR 46400 Evidence-Driven Research from MGMT474 infra core

Carries the portable infrastructure (Quarto site shell, scripts framework,
.claude hooks, planning-doc templates, .gitignore) and deliberately omits the
quant ML notebook spine and assessment banks, which are replaced with a
research-methodology spine.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

## Step 4 — ⚠️ OUTWARD-FACING / IRREVERSIBLE: create the GitHub remote + push

> **STOP — run only with explicit go-ahead.** This publishes the repo to GitHub.
> Confirm **public vs. private** and the **exact repo name** first (see Open
> Decisions). The `gh` token is currently expired — refresh it first.

```bash
cd "$DEST"
gh auth refresh -h github.com          # token is expired — do this first

# Preferred (adjust --public/--private per decision):
gh repo create 2026F_evidence_driven_research_purdue_HONR464 \
  --public --source=. --remote=origin --push \
  --description "HONR 46400: Evidence-Driven Research — Purdue Honors College, Fall 2026"
```

Manual fallback (create empty repo in the web UI first, then):

```bash
git remote add origin https://github.com/davi-moreira/2026F_evidence_driven_research_purdue_HONR464.git
git push -u origin main
```

## Step 5 — ⚠️ OUTWARD-FACING: enable GitHub Pages + first render + commit `docs/`

> Do Step 6 edits (title/URLs) **before** this render so the first published site
> already carries the correct branding, not stale MGMT474 strings.

1. Browser: **repo → Settings → Pages → Deploy from a branch → `main` / `/docs` → Save.**
2. Render + commit:

```bash
cd "$DEST"
/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto render
git add docs/
git commit -m "build: Initial Quarto render of HONR 46400 site

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
git push origin main
```

## Step 6 — Adapt the seeded infra files

| File | Edit |
|---|---|
| **`CLAUDE.md`** | Replace with the adapted skeleton (Project Mission → HONR 46400, MWF, research mission; new repo/website URLs; See-Also table; **remove the CV-First rule**; drop `RANDOM_SEED`/60-20-20 style rows; keep Voice, Commit+Render, MC-parity-as-optional, markdown-escape; add the research-integrity trio). See companion `CLAUDE.md` skeleton. |
| **`_quarto.yml`** | `title:` → "HONR 46400: Evidence-Driven Research (Fall 2026)"; GitHub `href` → new repo; **comment out the `logo:` line until `images/honr_464_logo.png` exists**; **remove the `workflow.qmd` nav entry** (page deleted). |
| **`index.qmd` + `syllabus.qmd`** | Rewrite the (duplicated in both) Description + Learning Outcomes + Course Materials for research methodology; drop ISLP; meeting line → **Mon/Wed/Fri**; syllabus Assessments table = clearly-marked PROVISIONAL; verify whether the Daniels **GPA-3.3 cap** applies to Honors College (likely remove). Mark "Office: Young Hall 1019" and any dates as **verify/TODO**. |
| **`schedule.qmd`** | Keep the overflow-table CSS harness; replace rows with a placeholder + one example row (real sequence built in the curriculum session); repoint any Colab badge base to the new repo. |
| **`README.md`** | Rewrite course number/title/cadence/URL; drop ISLP/ML topic lines. |
| **`.claude/settings.json`** | KEEP as-is (generic instructor-md sync hook; no-ops with no instructor notebooks). |
| **`.claude/settings.local.json`** | Does NOT seed — **re-add the `session_autocommit.sh` Stop hook by hand** if you want auto render+commit+push. |
| **`.gitignore`** | Keep privacy/media/build blocks + `**/*_instructor*.ipynb`; rename content dirs: `video_guides/`→`session_guides/`, `_homework/`→`_worksheets/`, add `_peer_review/`; keep `_quizzes/ _handouts/ _lecture_notes/ _midterm_exam/ _syllabus/ brightspace/`; `notebooks/data/`→`activities/data/`. |
| **`scripts/audit_answer_length.py`** | Repoint globs `_quizzes/2026Summer` → `_quizzes/2026Fall` (only when MC banks exist). |
| **`scripts/voice_check_guides.py`** | Repoint `video_guides/` → `session_guides/`; drop the `Student's t` whitelist. |

## Step 7 — Bootstrap prompt for the fresh Claude session (in the new repo)

Open Claude Code in `$DEST` and paste:

> Read `CLAUDE.md`, `_project_docs/DECISIONS.md`, `_project_docs/ACTIVITY_TEMPLATE.md`,
> `_project_docs/TROUBLESHOOTING.md`, and `NEW_COURSE_SETUP.md`.
>
> CONTEXT: This repo was seeded from a QUANTITATIVE Predictive Analytics course
> but is now **HONR 46400 "Evidence-Driven Research"** — Purdue Honors College,
> Fall 2026, taught **Mon/Wed/Fri, in person**, over a full semester, for honors
> students **without a strong quantitative or computing background**. The reusable
> INFRASTRUCTURE seeded across; the quant CONTENT spine was deliberately NOT seeded.
>
> DO NOT write curriculum content yet. First, PLAN (for my review): (1) a
> full-semester MWF plan anchored to the official Purdue Fall 2026 calendar + the
> Fall Undergraduate Research Conference poster date, mapping the outcome chain
> gap→question→conceptual method-family choice→locate/appraise sources→
> operationalize→analyze with AI→verify+document→interpret with uncertainty→
> written+oral communication; (2) a lightweight activity/worksheet spine reusing
> the instructor-first + PAUSE-AND-DO + narrative-Q&A conventions; (3) an
> assessment redesign built on the milestone + peer-eval + URC-poster scaffolding,
> ending in a WRITTEN report + ORAL defense (no Kaggle, no ML midterm); (4) the
> research-integrity CLAUDE.md rules. Confirm the plan before building anything.

---

## GAP LIST — 14 fresh artifacts to build (no source analog)

Ordered by how load-bearing they are to the stated outcomes:

1. **Literature-gap identification framework** (gap typology + "reading a field for the gap" worksheet).
2. **Research-question quality rubric** (answerability, scope, specificity, feasibility).
3. **Conceptual method-selection decision aid** — description vs. inference vs. prediction vs. causal (the course's signature skill; *no source analog*).
4. **Operationalization / measurement guidance** (concept → construct → indicator).
5. **Source-finding & citation-integrity guidance** (source location workflow + **fabricated-citation detection** — AI hallucinates cites).
6. **Results-verification & reproducibility checklist** + a fresh content-integrity audit script (fills the retired `audit_cv_first.py` slot).
7. **Responsible-AI-use documentation rubric** (Ask→Verify→Document as an assessed deliverable).
8. **Uncertainty & limitations communication rules** (prose discipline replacing CI machinery).
9. **Oral-presentation deliverable + rubric** (source assesses only a *written* poster; oral defense is entirely new).
10. **Research-ethics / IRB / human-subjects note** (handout + syllabus policy).
11. **Fall Undergraduate Research Conference tie-in** (poster ~Nov 17 — a *stronger* fit for Honors than the summer ML course; make it the M4 capstone).
12. **Participation instrument for in-person MWF** (source was async online — no live-participation mechanism authored).
13. **Fresh full-semester plan + dependency diagram** (`HONR464_Semester_Plan_2026Fall.md`, the source-of-truth every doc syncs to).
14. **New brand assets** (a HONR 46400 logo).

---

## Open decisions to confirm BEFORE the outward-facing steps

1. **Notebook/Colab spine or plain worksheets?** Governs `activities/` holding `.ipynb` + Colab badges + the instructor→student marker-strip mechanic, or plain Quarto/markdown worksheets. *Decide first — everything downstream forks on it.*
2. **Repo name / spelling.** Folder says `evidence_**based**_research` and `HONR**464**`; official title is "Evidence-**Driven** Research", course is HONR **46400** (short code parallels the source's `MGMT474`). Confirm before the irreversible repo-create.
3. **Public or private repo?** Source is public; an Honors research course may warrant private.
4. **Official Purdue Fall 2026 calendar** (first day, Labor Day, October break, Thanksgiving, last class, finals) + the **URC poster date** — anchors the whole milestone schedule.
5. **Class time + room** (MWF known; clock/room not). Any session recorded → governs `session_guides/` vs. video, and whether the camera-language voice audit applies.
6. **Brightspace granularity** — one page per session, per week, or lighter for in-person?
7. **Textbook / readings** — confirm "no single textbook, curated readings"; seed a reading list?
8. **Does the Daniels GPA-3.3 cap apply to Honors?** Needs a definitive answer before the syllabus publishes.
9. **Assessment weights + instruments** (participation %, whether MC quizzes exist → whether `audit_answer_length.py` stays live, oral-defense weight, peer-eval weight).
10. **New brand asset** — will there be a `honr_464_logo.png`, or run logo-less until one exists?
