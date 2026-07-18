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
