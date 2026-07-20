# HONR 46400 Evidence-Driven Research — AI Assistant Guide

This file documents the rules and workflows that change Claude's behavior in this
repository. Reference material lives in linked files — read those when relevant,
not by default.

## Project Mission

**HONR 46400 — SP: Evidence-Driven Research**, a semester-long Honors College
seminar (Fall 2026, meeting **Mon/Wed/Fri, in person**) for Purdue's Honors
College. The course teaches honors students — **without assuming a strong
quantitative or computing background** — to turn curiosity into credible,
evidence-based insight: identify meaningful gaps in a chosen field, translate gaps
into well-scoped research problems, formulate answerable research questions,
classify each question on the **inquiry compass** — its **kind** (descriptive vs
causal, RDSS ch. 7) and its **reach** (the data at hand / a population beyond the
data / cases not yet seen) — justify the classification at a **conceptual** level,
and use computational tools + AI to locate sources, operationalize concepts,
analyze evidence, verify results, and document decisions responsibly. Students
finish able to design and defend a rigorous research approach, interpret findings
with appropriate uncertainty and limitations, and communicate results effectively
in **written AND oral** formats.

- **Instructor:** Professor Davi Moreira
- **Repository:** https://github.com/davi-moreira/2026F_evidence_driven_research_purdue_HONR464
- **Website:** https://davi-moreira.github.io/2026F_evidence_driven_research_purdue_HONR464/
- **Deployment:** Quarto → `docs/` → GitHub Pages

## See Also (Reference Files)

| File | When to read | Status |
|---|---|---|
| `_project_docs/ACTIVITY_TEMPLATE.md` | Creating/restructuring a topic notebook — the full, machine-validated template | ✓ canonical (Fall 2026 build) |
| `_project_docs/DECISIONS.md` | Before proposing changes to conventions (deliverable formats, AI-tool stack, sourcing standards) | ✓ seeded (adapt) |
| `_project_docs/TROUBLESHOOTING.md` | Render fails, Pages stale, git push rejected, leaked solutions | ✓ seeded |
| `_project_docs/COURSE_MATERIAL_WORKFLOW.md` | Producing one unit end-to-end (notebook → session plan → Brightspace page) | ✓ seeded (adapt for MWF/in-person) |
| `planning/COURSE_MASTER_PLAN.md` | Master course plan — source of truth for sequencing (+ `planning/BUILD_STATUS.md` for build state) | ✓ built |
| `planning/MEETING_SCHEDULE.md` | Per-meeting detail (44 × 32 columns; generated from `scripts/schedule_data/`) | ✓ built |
| `CONVERSATION_LOG.md` | Project history and prior decisions | ✓ fresh |
| `scripts/voice_lint_notebooks.py` | Voice gate for student notebooks (also a PostToolUse hook) | ✓ built |
| `scripts/voice_check_guides.py` | Before every session-guide edit | ✓ seeded (repointed) |
| `scripts/audit_answer_length.py` | Before importing any MC quiz CSV (only if MC banks are used) | ✓ seeded (dormant) |
| `scripts/audit_sources.py` | Before shipping any notebook with citations (citation-integrity gate) | ✓ built |
| `scripts/nbbuild.py` | Build one topic notebook end-to-end (source → execute → strip → validate → badge) | ✓ built |

**Canonical notebook reference:** `notebooks/student/nb01_curiosity_to_question_student.ipynb`
— match its formatting exactly. Cell sources live in gitignored
`_production_kit/nb_sources/nbNN_<slug>.py`; edit the source, then rebuild with
`.venv/bin/python scripts/nbbuild.py nbNN`.

---

## 🚨 CRITICAL RULE — Voice and Audience in Student-Facing Content  *(KEEP verbatim)*

The student activity is read **BY students**, not by instructors who then teach it.
Every sentence in a student-facing cell — including AI prompts and "After running,
verify" checklists — must be written **TO the student**, never ABOUT the student and
never TO the instructor.

1. Never write "students" as a third-party noun inside a student-facing cell.
   Rewrite in second person (`you`), neutral imperative, or first person.
2. AI prompts are scripts the student copies into the AI tool — they must sound like
   something a student would actually type.
3. No instructor-voice / facilitation language in student cells. That belongs only
   in `session_guides/NN_session_guide.md` (gitignored).
4. Session guides may reference students in third person in wrapper prose, but NOT
   inside blockquote read-aloud scripts (`> *"..."*`).

```bash
.venv/bin/python scripts/voice_lint_notebooks.py                      # all student notebooks; expect ✓ clean
python3 scripts/voice_check_guides.py session_guides/NN_session_guide.md
```

---

## 🚨 CRITICAL RULE — Undergraduate-Friendly Voice  *(2026-07-20 — supersedes "Narrative Polish Pattern"; see DECISIONS.md D14)*

Notebooks are read by honors undergraduates with **no quantitative background**.
The narrative machinery stays; the prose must read like a person, not a model.

**Keep (the pedagogy):**
1. **"Why This Matters" cells** opened by a named research-world stakeholder
   (thesis advisor, journal reviewer, IRB reviewer, skeptical peer, policy
   stakeholder) whose concern is a direct quote.
2. **Narrative prose over bullet lists** in "Reading the evidence" cells.
3. **Inline Q&A blocks**: `> **A question that often comes up here:** *"<q>"*` +
   one flowing paragraph.
4. **Section bridges** and **warm wrap-ups** with a bridge to the next activity.

**Enforce (the voice — machine-checked by `scripts/voice_lint_notebooks.py`):**
1. **Em-dash budget: ≤ 20 per notebook, ≤ 1 per markdown cell.** Prefer periods,
   commas, and bold lead-ins (`**Why this matters:**`, `**The catch:**`) over
   dash-chained clauses.
2. **Every technical term is introduced as: bold term → one-sentence
   plain-language definition → concrete example** before it is used again.
   Never assume a student knows estimand, sampling frame, held-out, DAG, etc.
3. **Short-to-medium sentences** (roughly 12–25 words). One idea per sentence.
   Second person (`you`) throughout.
4. **No fourth-wall meta-references.** Never tell the reader content was
   "fabricated / planted / invented for this exercise" and never annotate
   Sources sections with asides about the material's construction.
5. **No fabricated citations anywhere** (see Evidence-Integrity rule below):
   citation-verification skills are taught with real, retrievable sources only.

---

## 🚨 CRITICAL RULE — Evidence-Integrity & Results-Verification  *(REPLACES the CV-First rule)*

The course's methodological spine — the analog of what CV-first was to the quant
course. Every empirical claim in any student-facing or deliverable material must be
**traceable and verified**:

1. **Every empirical claim traces to a real, retrievable source.** No fabricated,
   hallucinated, or unverifiable citations. If a claim came from an AI tool, the
   underlying source is independently located and confirmed to exist.
2. **Every result is verified before it is reported** — the deliverable records how
   the output was cross-checked (recomputed, triangulated, or spot-checked).
3. **Decisions are documented, not just outcomes** — which sources, which
   operationalization, which method family, and *why*.
4. **No planted-fake citations, even as a teaching device** (D16, 2026-07-20).
   Citation-verification exercises use real sources the student retrieves and
   confirms. `scripts/audit_sources.py` hard-fails on any known fake name.

```bash
.venv/bin/python scripts/audit_sources.py   # all student notebooks: URL allowlist, verified-citation registry, fake-citation blocklist
```

---

## 🚨 CRITICAL RULE — Inquiry-Declaration Justification  *(REPLACES Method-Selection; taxonomy adopted from RDSS 2026-07-19)*

The course uses the book's taxonomy, not a four-family grid: every research
question is classified by **kind** (descriptive / causal inquiry, RDSS ch. 7) and
**reach** (data at hand / population / unseen cases), giving four named compass
positions — Description (nb06), Generalization (nb10), Prediction (nb12, the
course-authored "Observational: predictive" library entry), Causal reasoning
(nb13) — with MIDA + diagnosis as cross-cutting machinery. Whenever a student
declares a position, the activity or milestone must state, **at a conceptual
level**: (1) why that kind and reach fit the question's words, (2) what crossing
licenses the design holds (sampling → population; prediction-time honesty +
held-out check → unseen; assignment/identification → causal) and hence what the
answer can and cannot establish, and (3) key limitations and sources of
uncertainty. A declaration with no stated justification or limitation is
incomplete. Canonical reference: `planning/INQUIRY_MAP.md`; machine-readable
core: `course_config.yaml` `inquiry_framework:`; student template:
`project/templates/INQUIRY_DECLARATION.md`.

---

## 🚨 CRITICAL RULE — Responsible-AI-Use Documentation  *(NEW — instantiates the mission)*

Every deliverable that used an AI tool records, in a short disclosure block: which
tool, for what task (locate sources / operationalize / draft / critique), and how
its output was verified. The verify step is a **graded habit**, not a formality.
Embedded AI prompts carry an **"After running, verify:"** checklist recast as a
responsible-AI habit — confirm cited sources exist, cross-check facts, log the
decision.

---

## 🚨 CRITICAL RULE — Uncertainty & Limitations in Communication  *(NEW)*

Findings are never communicated as certainties. Every written report and oral
defense states the uncertainty around its claims and the limitations of its evidence
and method. A results statement with no uncertainty/limitations framing is a defect
(the "overclaiming certainty" researcher-failure archetype).

---

## 🚨 CRITICAL RULE — Lecture Labels, Never Dates  *(2026-07-20, D13)*

Notebooks and session guides carry **no calendar dates, no day-of-month, no
"Meeting M#" references**. Position is expressed only as explicit lecture labels:

- Notebook header: `**Topic NN · N lecture(s)**` (single-lecture topics say
  `1 lecture`). Multi-lecture notebooks mark internal boundaries with a
  horizontal rule + `*(Lecture i of N starts here.)*`.
- Session guides head each meeting section `## Lecture i of N — <title>`,
  `## Studio Friday — <title>`, or `## Async module — <title>`.
- Labels are **derived mechanically** from `lecture_labels()` in
  `scripts/notebooks_map.py` (computed from `planning/MEETING_SCHEDULE.csv`) —
  never hand-maintained. Dates live ONLY on the public `schedule.qmd` page and
  in milestone briefs (`_research_project/2026Fall/`).

---

## 🚨 CRITICAL RULE — Friday Studio Format  *(2026-07-20, D13)*

**No new topic content on Fridays.** Every Friday session is a studio:
1. **≈10 min** — instructor recaps the week's topic (the compass position, the
   claim boundary, the one thing to remember).
2. **≈10 min** — instructor presents the next final-project milestone from its
   Brightspace brief (generated from `_research_project/2026Fall/milestone_NN_*.md`).
3. **≈30 min** — students work on the milestone and their research project;
   instructor runs rotating consults.

Late-semester performance Fridays (poster production, hot seat, table read,
submission ceremony) keep their character as the work block inside this frame.
Mon/Wed = lectures; the two async meetings are self-contained modules.

---

## 🚨 CRITICAL RULE — Dataset Distribution  *(2026-07-20, D15)*

`notebooks/data/` is the **single canonical dataset folder**. Every dataset the
course uses lives there, and all of them ship in one downloadable bundle,
`notebooks/data/honr46400_datasets.zip`, linked from the Material and Schedule
pages. Whenever a dataset is added or changed:

```bash
.venv/bin/python scripts/make_dataset_zip.py   # regenerate the bundle, then commit it
```

Notebooks keep loading data via `load_course_data()` (GitHub raw URL first,
local fallback); the zip is the student-facing offline copy.

---

## 🚨 CRITICAL WORKFLOW — Instructor-First Notebook Editing  *(hard rule — no exceptions)*

**ANY request to "work on a notebook" means: edit the instructor side first; the
student notebook is only ever a mechanical, answer-stripped copy of it.** Never
edit a `notebooks/student/*.ipynb` directly, and never let the student file
drift from the instructor version.

ALWAYS edit the cell source `_production_kit/nb_sources/nbNN_<slug>.py` (gitignored)
FIRST, then rebuild: `.venv/bin/python scripts/nbbuild.py nbNN` — this regenerates
`notebooks/instructor/nbNN_*_instructor.ipynb`, executes it with nbclient,
generates the student file by stripping every cell containing `INSTRUCTOR
SOLUTION`, runs the template/voice validators, and refreshes the schedule badge.
(Direct edits to an instructor .ipynb without a source rebuild will be lost.)

- Markers (unchanged so audits keep working): `### INSTRUCTOR SOLUTION — Exercise N`,
  `# INSTRUCTOR SOLUTION`, `<!-- INSTRUCTOR SOLUTION -->`.
- Student placeholders: `### YOUR ANSWER HERE:` (text) / `# YOUR SOLUTION HERE`.
- The "solution" is a **model exemplar** (a well-appraised source, a well-scoped
  question, a worked method-justification), not working ML code.
- Only `notebooks/student/*_student.ipynb` is committed; instructor notebooks and
  `_production_kit/` sources are gitignored.
- Schedule badges key off **git-tracked** student files only
  (`scripts/update_schedule_badges.py`) — stage the student notebook before
  regenerating badges when publishing a new topic.
- **After building, sync instructor material to the private repo:**
  `scripts/sync_instructor_repo.sh` pushes `notebooks/instructor/`,
  `session_guides/`, and `notebooks/data/` to the private GitHub repo
  `davi-moreira/2026F_evidence_driven_research_purdue_HONR464_instructor`
  (local clone in gitignored `_instructor_repo/`), which backs the
  password-gated Instructor tab. The page gate (password `eureka`) is a
  courtesy lock; the real protection is the private repo + GitHub auth.

---

## 🚨 CRITICAL WORKFLOW — Sync Session Guides and Planning Docs  *(KEEP — repoint)*

Every time an activity is updated: (1) update its session guide
(`session_guides/NN_session_guide.md`, gitignored) and (2) if significant, update
the sequencing rationale in `planning/COURSE_MASTER_PLAN.md` (and the affected
rows in `scripts/schedule_data/` → rebuild `planning/MEETING_SCHEDULE.{csv,md}`).

---

## 🚨 CRITICAL WORKFLOW — Commit AND Render Webpage  *(KEEP verbatim)*

Every content change → `quarto render` → commit `docs/` → push. GitHub Pages serves
`docs/`; skipping the render leaves the site stale (the project's most common
mistake).

```bash
git add <changed .qmd or activity>
git commit -m "feat: ..."
/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto render
git add docs/ && git commit -m "build: Render Quarto site"
git push origin main
```

Site pages: `index` / `syllabus` (hand-edited), `material.qmd` (generated by
`scripts/build_material_page.py`), `schedule.qmd` (generated by
`scripts/update_schedule_badges.py`), `instructor.qmd` (topic table of private-repo
Colab badges). The render's `post-render` step runs
`scripts/protect_instructor_page.py`, which encrypts `docs/instructor.html`
client-side (password `eureka`) — never commit an unencrypted instructor page.
Do not hand-edit generated pages; edit the generator or the schedule data.

---

## 🚨 OPTIONAL RULE — MC Option-Length Parity  *(only if MC quizzes are used)*

If the course uses auto-graded Brightspace MC quizzes: every option ≥ 60% of the
longest option's length; the correct option is strictly longest in ≤ 40% of a
bank's questions; distractors carry equally-elaborated but flawed rationale.

```bash
python3 scripts/audit_answer_length.py --file <path-to-csv>   # PASS required before import
```

If the course assesses only via written/oral deliverables + rubrics, this rule and
its script are dormant but harmless.

---

## Style Guidelines  *(KEEP markdown hygiene; DROP the ML constants)*

| Setting | Value |
|---|---|
| Money in markdown cells | Always escape: `\$50,000` (unescaped `$` triggers LaTeX) |
| Tildes in markdown cells | Always escape: `\~30 sources`, `(\~0.5)` |
| Emoji vocabulary | `✓` success, `⚠️` warning, `📝` exercise, `💡` insight |

> The source course's `RANDOM_SEED = 474` and 60/20/20 split are **dropped**. This
> course uses **`SEED = 464`** (the course number) via `np.random.default_rng(SEED)`
> in every notebook's setup cell; all simulations are deterministic. No seaborn.

## Naming and Commit Conventions  *(KEEP)*

- Student notebooks (committed): `notebooks/student/nbNN_topic_student.ipynb`
- Instructor notebooks (gitignored): `notebooks/instructor/nbNN_topic_instructor.ipynb`
- Cell sources (gitignored, canonical for editing): `_production_kit/nb_sources/nbNN_topic.py`
- Commit messages: `<type>: <subject>` (feat|fix|docs|chore|build|refactor) with a
  trailing `Co-Authored-By:` line. Stage specific files — never `git add .`.

---

**Version:** 4.0 — Course redesign (2026-07-20, DECISIONS.md D13–D16): Friday
studios + Phase 1–2 compression, undergraduate-friendly voice, lecture labels
(never dates), Material/Schedule tab split, single dataset zip, password-gated
Instructor tab backed by the private `_instructor` repo, fabricated citations
removed course-wide. (3.0 = RDSS inquiry compass adopted, 2026-07-19; 2.0 =
Fall 2026 course fully built: planning suite, 20 topic notebooks nb00–nb19,
milestones M00–M23, project protocols, validators. 1.0 = seeded from
2026Summer_predictive_analytics_MGMT474 infra.)
**Maintained by:** Professor Davi Moreira + AI Assistants
