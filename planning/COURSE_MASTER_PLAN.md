# HONR 46400 — Course Master Plan (Fall 2026)

**From Curiosity to Defensible Claims** · Purdue Honors College · Mon/Wed/Fri, 50 min · 5 students, 5 individual projects.

This is the source-of-truth narrative for the whole build. The machine-readable
spine is `course_config.yaml`; the verified date backbone is
`scripts/validate_calendar.py` → `planning/CALENDAR_BACKBONE.csv`; the per-meeting
detail is `planning/MEETING_SCHEDULE.{csv,md}`; the project system is
`planning/PROJECT_MILESTONES.md`. Any conflict is resolved in this file's favor for
*intent* and in the calendar script's favor for *dates*.

> **Design guardrails (from the brief).** This is **not** an intro-stats survey, a
> software course, a Bayesian course, a predictive-analytics course, a causal-inference
> course, or a writing seminar. It is a course about **selecting, implementing,
> evaluating, and defending an evidence strategy that matches a research question** —
> taught to honors students **without** a strong quantitative or computing background,
> low-floor / high-ceiling throughout.

---

## 1. The intellectual spine

**Primary:** Blair, Coppock & Humphreys, *Research Design in the Social Sciences:
Declaration, Diagnosis, and Redesign* (Princeton, 2023) — the **MIDA** framework
(**M**odel · **I**nquiry · **D**ata strategy · **A**nswer strategy) and the recurring
**declare → diagnose → redesign** cycle, which functions as the course *operating
system*, not a one-time topic. Source material lives in `_adm/_references/book/`
(declarations, diagnoses, figures, 5 datasets, problem sets, sample syllabi) and the
CRAN **`rdss`** package (MIT).

**Secondary (optional / parallel):** Bergstrom & West, *Calling Bullshit* — used
lightly, "if we have time," to sharpen claim evaluation (visualization distortion,
base rates, prediction-vs-explanation, association-vs-causation). Not in the repo;
sourced from public callingbullshit.org where used. Never a disconnected book club;
never reflexive cynicism — every "bullshit check" ends by asking *what can still be
learned and what evidence would be needed.*

## 2. The four approaches (explicit, recurring, operational)

Every meeting names the approach(es) it emphasizes, the **claim it permits**, and the
**claim it does not permit**. The signature course skill is *classifying a question*
into one (or a justified combination) of:

| Approach | Asks | Permits | Does **not** permit | Deep-dive |
|---|---|---|---|---|
| **Description** | what is observed here? | statements about the data at hand | generalization; causation | `nb06` |
| **Statistical/observational inference** | what generalizes, with how much uncertainty? | population/process estimates + uncertainty | causation from association | `nb10` |
| **Predictive modeling** | can we forecast new cases? | out-of-sample performance vs. a baseline | explanation; causation | `nb12` |
| **Causal reasoning** | what if we intervened? | an effect under a stated identification argument | effects when identification fails | `nb13` |

RDSS covers description, inference, and causal designs richly; **prediction is built
fresher** (scikit-learn: target, baseline, train/test split, metric, leakage,
out-of-sample) because the book barely treats it. `nb02` teaches the classification
skill up front; `nb11` teaches the declare→diagnose→redesign engine that stress-tests
any of the four.

## 3. The operating loop (every notebook, every milestone)

`ASK → DEFINE → CLASSIFY → MATCH → DECLARE → BUILD → DIAGNOSE → REDESIGN → VERIFY →
CLAIM → COMMUNICATE → REVISE.` Recurring notebook moves: **Pause & Predict**,
**Classify the Question**, **Make a Design Choice**, **Run the Study**, **Diagnose**,
**Redesign**, **Verify**, **Defend the Claim**, **Milestone Build/Check/Pitch**,
**Project Transfer**, **Claim Ticket** (exit).

## 4. Course arc — 8 phases across the 44 meetings

| Phase | Meetings | Dates | Focus | Project outcomes |
|---|---|---|---|---|
| **1 — Curiosity, gaps, answerable questions** | M1–M6 | Aug 24–Sep 4 | How do we know? topic vs gap vs question; classify the approach | Curiosity Map; question pitch; candidate gaps/questions |
| **2 — Literature, model, inquiry, measurement** | M7–M14 | Sep 9–Sep 25 | establish the gap; MIDA Model+Inquiry; operationalization | literature/claim map; question+approach declaration; construct/measurement map |
| **3 — Data & answer strategies** | M15–M22 | Sep 28–Oct 16 | data strategy (sampling/assignment); answer strategy; inference; feasibility/ethics | design declaration; URC abstract; data-access + ethics checkpoint |
| **4 — Pilot, diagnosis, redesign** | M23–M28 | Oct 19–Oct 30 | declare→diagnose→redesign; prediction; causal; verification | executable pilot; approach-specific diagnosis; redesign memo |
| **5 — Poster construction & submission** | M29–M31 | Nov 2–Nov 6 | storyboard → draft → **final poster** (production, not buffer) | approved, submitted poster (**Nov 6 = M31**) |
| **6 — Conference preparation** | M32–M35 | Nov 9–Nov 16 | 1-/3-min delivery; uncertainty & limitations; dress rehearsal | rehearsed presentation; readiness audit |
| **7 — Reflection, feedback, redesign** | M36–M38 | Nov 18–Nov 23 | debrief; feedback→redesign; (async) poster→dossier module | reflection; redesign plan; dossier draft |
| **8 — Reproducibility, brief, Evidence Defense** | M39–M44 | Nov 30–Dec 11 | reproducibility audit; research brief; **Evidence Defense**; synthesis | reproducible dossier; final claim ledger |

**URC Expo — Tue Nov 17** (between M35 and M36): required in-person poster presentation
(not an MWF meeting). Async meetings: **M17 (Oct 2)** and **M38 (Nov 23)** are
self-contained online modules with an assessable artifact each.

## 5. Topic notebooks (one per topic; each absorbs the meetings it needs)

`nbNN_topic_{student,instructor}.ipynb`, flat in `notebooks/`. Student version
committed + Colab-badged on `schedule.qmd`; instructor version gitignored. Every
ordinary notebook carries ≥1 pre-execution prediction, ≥1 runnable activity, ≥1
defended decision, ≥1 practice item, ≥1 interpretation task, ≥1 milestone/project
transfer, and a Claim-Ticket exit. Direct exposition ≤8 min/segment, <15 min/meeting;
≥70% active time.

| NB | Topic | Meetings | Approach emphasis | Milestone developed | Primary provenance |
|---|---|---|---|---|---|
| `nb00` | Launchpad: *How do we know?* course map, Colab, Ask→Verify→Document | M1 | all (framing) | M00 kickoff | brief §3; RDSS ch.1 (concept) |
| `nb01` | Curiosity → gap → problem → **answerable question** | M2–M4 | all (framing) | M00→M01 | RDSS ch.2–3; brief §12 P1 |
| `nb02` | **The four approaches** — classify the question | M5–M6 | all (the skill) | M01 | RDSS ch.4; brief §2 |
| `nb03` | Establishing the gap: source-finding, **citation integrity**, AI hallucination check; claim map | M7–M8 | description/inference | M02 | fresh + AI policy; RDSS ch.6 |
| `nb04` | **Model & Inquiry** (MIDA I): worlds, potential outcomes, estimands; DAG intro | M9–M10 | causal/inference | M03 | RDSS ch.7–9; `declaration_*`; `make_dag_df` |
| `nb05` | **Measurement & operationalization**: concept→construct→indicator | M11–M12 | description/inference | M04 | RDSS ch.8; fresh |
| `nb06` | **Description** (deep dive): distributions, summaries, honest visualization; boundaries | M13–M14 | **description** | M04→M05 | RDSS ch.5,9; `lapop_brazil`, `la_voter_file` |
| `nb07` | **Data strategy** (MIDA II): sampling & assignment; selection; who's missing | M15–M16 | inference/causal | M05 | RDSS ch.9–12; `declaration_2.1/9.1` |
| `nb08` | **Async (Oct 2):** diagnose a misleading claim + answer-strategy preview | M17 | inference | M05 (dev) | brief §12 P3; optional CB case |
| `nb09` | **Answer strategy** (MIDA III): estimators, difference-in-means, regression | M18–M19 | inference/causal | M05→M06 | RDSS ch.13–15; `estimatr`/`lm_robust` |
| `nb10` | **Statistical/observational inference** (deep dive): uncertainty, generalization, assoc≠cause | M20–M22 | **inference** | M06→M07 | RDSS ch.9–15; problem-set 1 |
| `nb11` | **Declare → Diagnose → Redesign** engine: power, bias, coverage; redesign | M23–M24 | all (diagnosis) | M08 | RDSS ch.10–13; `diagnose_design`, `redesign` |
| `nb12` | **Prediction** (deep dive): target, baseline, train/test, metric, leakage | M25–M26 | **prediction** | M08→M09 | fresh scikit-learn; optional CB algorithms |
| `nb13` | **Causal reasoning** (deep dive): counterfactuals, identification, DAGs; DiD/RDD/IV intuition | M27–M28 | **causal** | M09 | RDSS ch.16–19; `declaration_18.1` |
| `nb14` | **Poster storyboard & evidence hierarchy**; honest visualization; claim calibration | M29–M31 | all | M10→M11→M12 | brief §12 P5; RDSS figures; optional CB rebuild-graph |
| `nb15` | **Communicating evidence**: 1-/3-min pitch, uncertainty & limitations, hard questions, rehearsal | M32–M35 | all | M13→M14→M15 | brief §12 P6 |
| `nb16` | **Conference debrief → feedback-to-redesign** | M36–M37 | all | M17→M18 | brief §12 P7 |
| `nb17` | **Async (Nov 23):** Poster-to-Dossier module — robustness/sensitivity, claim ledger, methods/findings | M38 | project-specific | M19 | brief §10 M19 |
| `nb18` | **Reproducibility audit + research brief** | M39–M41 | all | M20→M21 | brief §12 P8; RDSS ch.23 |
| `nb19` | **Evidence Defense + synthesis** of the four approaches; *what is a defensible claim* | M42–M44 | all | M22→M23 | brief §12 P8 |

20 notebooks (nb00–nb19). Each of the four approaches has a dedicated deep-dive
(nb06/nb10/nb12/nb13); nb02 teaches classification; nb11 teaches the diagnosis engine.

## 6. Project-studio cadence (protected in-class development)

- **M1–M11 (Aug 24–Sep 18):** ≥10–15 min project-transfer/milestone work most meetings.
- **M12–M22 (Sep 21–Oct 16):** ≥1 substantial development block/week.
- **M23–M28 (Oct 19–Oct 30):** ≥2 development/analysis blocks/week.
- **M29–M31 (Nov 2–Nov 6):** poster production dominates.
- **M32–M35 (Nov 9–Nov 16):** delivery, peer review, rehearsal dominate.
- **M39–M44 (Nov 30–Dec 11):** revision, reproducibility, brief, Evidence Defense.

Studio format (varied, not mechanical): status/blocker declaration → individual
production with 5-min rotating instructor consultations → cross-disciplinary peer
review → revision → submission check + next-action commitment. With 5 students, every
studio includes short milestone presentations (2-min pitch / 3-min declaration /
5-min walkthrough / storyboard pitch / claim defense).

## 7. Milestone system (markdown deliverables → Brightspace)

Instructions + rubric per milestone in `_research_project/2026Fall/` (MGMT 474
`_final_project` pattern). The brief's M00–M23 are preserved as graded, submittable
milestones with **develop → present → submit → revise** cadence; each has ≥1 prior
in-class development meeting and a presentation/review activity. Full development /
presentation / submission / revision dates: `planning/MILESTONE_PRESENTATION_MAP.md`.
The five students each carry **one individual project** to a required URC poster
(Nov 17) and a reproducible final dossier (Dec 11).

## 8. Assessment architecture (provisional — see ASSESSMENT_ARCHITECTURE.md)

Aligned to the brief's philosophy (no conventional midterm/final exam):

| Component | Weight |
|---|---|
| Daily notebook preparation & engagement | 15% |
| Milestone development, presentations & revisions | 30% |
| URC poster & presentation | 20% |
| Post-conference final research dossier | 20% |
| Evidence Defense & course synthesis | 5% |
| Calling Bullshit claim analyses (optional/light) + concept checks | 10% |

Grading rewards correctness, transparency, reproducibility, approach-alignment, and
responsible interpretation — **not** coding elegance. Reconciled with the current
`syllabus.qmd` provisional weights during Phase B.

## 9. Provenance convention (used everywhere)

Every schedule row and notebook records: **source file · chapter/section/module ·
page/figure/exercise/dataset · transformation** (`adapted` / `translated` /
`extended` / `newly constructed from a source concept`). Empirical claims trace to a
real, retrievable source; results are verified before reported; decisions are
documented, not just outcomes. See `planning/SOURCE_AUDIT.md` §11.
