# HONR 46400 — Conversation Log

Append-only project history. Never overwrite — always append.

---

## 2026-07-16 — Session 1: Repo bootstrap

**Goal:** Stand up the new course repository for HONR 46400 "Evidence-Driven
Research" (Purdue Honors College, Fall 2026, Mon/Wed/Fri, in person).

**What happened:**
- Seeded the reusable **infrastructure** from
  `2026Summer_predictive_analytics_purdue_MGMT474` via a filtered `rsync` that
  deliberately excluded the quantitative ML **content spine** (the 21 ML
  notebooks, quiz/midterm/homework/handout banks, Kaggle competition, predictive
  final project, `_notebook_lm/`, `lecture_slides/`, `videos/`, `docs/`).
- Pruned quant residue: removed `scripts/audit_cv_first.py`, `scripts/build_nb19.py`,
  `workflow.qmd`, the MGMT ML planning docs, and MGMT-branded image assets; renamed
  `_project_docs/NOTEBOOK_TEMPLATE.md` → `ACTIVITY_TEMPLATE.md` and
  `scripts/qa_format_to_nb09.py` → `scripts/qa_format.py`.
- Created the scaffold: `activities/`, `_research_project/2026Fall/{rubric,template}`,
  `session_guides/`, `brightspace/`, `_worksheets/`, `_handouts/`,
  `_quizzes/2026Fall/`, `_peer_review/`.
- Rewrote the site shell (`_quarto.yml`, `index.qmd`, `syllabus.qmd`,
  `schedule.qmd`, `README.md`) for the research course; preserved the Purdue
  boilerplate (accessibility, CAPS, basic needs, grade challenges, subject-to-change)
  and rewrote the AI Policy around **Ask → Verify → Document**.
- Adapted `CLAUDE.md`: kept Voice/Audience, Commit+Render, MC-parity-as-optional,
  and markdown-hygiene rules; **removed the CV-First / test-set-lock rule** and the
  `RANDOM_SEED`/60-20-20 style constants; **added** the research-integrity rules
  (Evidence-Integrity & Results-Verification, Method-Selection Justification,
  Responsible-AI-Use Documentation, Uncertainty & Limitations in Communication).
- Re-wired the autocommit Stop hook in a fresh minimal `.claude/settings.local.json`.

**Decisions:**
- Content spine format: **light Colab/Jupyter `activities/`** (badges +
  instructor→student generation retained), text/argumentation-first.
- Repo visibility: course repo **public**; a **private `…-tasks` companion** holds
  course-operations tasks (managed via the `course-tasks` skill).

**Open (see `NEW_COURSE_SETUP.md` → Open Decisions & Gap List):** official Purdue
Fall 2026 calendar + URC poster date, class time/room, Brightspace granularity,
assessment weights, Honors grading policy, brand logo. Curriculum (the full
semester plan + activities + milestone content) is designed in the next session.

## 2026-07-17/18 — Full course build (Phases B–F concluded)

Autonomous build session (Fable), continuing the locked Phase A plan. Delivered:
the 44×32 meeting schedule + 7 planning docs; the technical foundation
(notebook template, nbbuild pipeline, validators, hooks, 5 rdss datasets,
translation/ suite); all 20 topic notebooks nb00–nb19 (instructor-first,
executed, stripped, validated, Colab-badged); all 24 milestone docs M00–M23 +
13 project protocols; reconciled syllabus (15/30/20/20/5/10, individual mode);
Phase F audit (all validators + execute-all sweep green). Notable decisions:
canonical constant-effect simulation world (TRUE_ATE = 2.0) shared by
nb04/09/10/11; badges keyed to git-tracked student files; milestone M07 is
two-part (abstract gate Oct 9 / declaration Oct 16); M16 = the URC Expo itself.
See planning/FINAL_REPORT.md. Build state: planning/BUILD_STATUS.md.

---

## 2026-07-19 — Session: Adopt the RDSS taxonomy (the inquiry compass) + session guides

**Goal:** Replace the four-approach grid with the textbook's own taxonomy end to
end, embed the EDA and prediction improvements that fall out of it, and generate
per-notebook session guides for every MWF meeting.

**What happened:**
- **Taxonomy adopted outright** (Decision 12 in `_project_docs/DECISIONS.md`):
  every question is classified by **kind** (descriptive vs causal, RDSS ch. 7) ×
  **reach** (data at hand / population / unseen cases) — "the inquiry compass."
  Old families map to named positions: description→nb06, statistical inference→
  **generalization** (nb10), predictive modeling→prediction (nb12), causal→nb13.
  Overclaims are **compass crossings without a license** (silent upgrade /
  leakage / after-therefore-because — each licensed by a design element, proven
  by diagnosis).
- **Machine layer:** `course_config.yaml` `approaches:` → `inquiry_framework:`
  (kinds, reaches, positions, crossings, EDA homes); schedule column `approach`
  → `inquiry` (all 44 rows relabeled); `validate_notebooks.py` now requires
  `## 🧭 Inquiry & Claim Boundary` + `**Inquiry emphasis:**`;
  `ACTIVITY_TEMPLATE.md` §2 updated; `notebooks_map.py` titles updated.
- **Planning layer:** `QUANTITATIVE_APPROACH_MAP.md` → **`INQUIRY_MAP.md`**
  (canonical compass reference, rewritten); `COURSE_MASTER_PLAN.md` §2 rewritten
  (+ stale RDSS chapter refs corrected: nb04→ch.6–7, nb07→ch.8, nb09→ch.9,
  nb06→ch.15, etc.); `PROJECT_MILESTONES.md`, assessment/dependency/reading
  maps, milestone briefs (`_research_project/2026Fall/`), poster/conference/
  dossier protocols swept; template `QUANTITATIVE_APPROACH_DECLARATION.md` →
  **`INQUIRY_DECLARATION.md`** (kind/reach checkboxes + crossing-licenses table);
  syllabus/index/schedule qmd updated (meeting titles M5–M6, M20–M22, M44).
- **Notebooks (all 20 rebuilt via nbbuild; validators + voice lint green):**
  nb02 rewritten as the compass skill (kind + reach drills; MIDA figure 2.1
  embedded); nb04 gained **EDA upstream** (explore lapop to calibrate M /
  surface candidate I); nb06 gained the **explore → declare → confirm loop**
  anchor (split-half explore-then-confirm demo); nb09 gained the **§9.1.3
  whole-procedure rule** (spec-shopping false-positive simulation); nb10
  reframed as the **Generalization deep dive** (descriptive inquiries with
  population estimands; silent upgrade = the named reach crossing); nb12
  reframed as the course-authored design-library entry **"Observational:
  predictive"** in declare-diagnose-redesign format (leakage = D-violation;
  held-out metric = diagnosand; baseline = redesign; MIDA figure embedded);
  nb13 relabeled + SATE/PATE reach note; nb17 gained ch. 22 **pivot flags +
  reconciliation** in the claim ledger; nb08/nb19 + all remaining notebooks
  relabeled to compass vocabulary.
- **Session guides built:** new tracked generator
  `scripts/build_session_guides.py` produces `session_guides/NN_session_guide.md`
  per notebook (all 20 guides / 44 meetings) from `MEETING_SCHEDULE.csv`:
  compass cheat sheet, per-meeting run-of-show table, read-alouds
  (voice-checked), hands-on/practice, milestone moment, prep, risks, exit
  ticket. Regenerate after any schedule edit.
- Figures README updated (fig 2.1 now also in nb02/nb12); notebook filenames
  (e.g. `nb02_four_approaches*`) deliberately kept for link stability.

**Decisions:** see Decision 12 (`_project_docs/DECISIONS.md`).
