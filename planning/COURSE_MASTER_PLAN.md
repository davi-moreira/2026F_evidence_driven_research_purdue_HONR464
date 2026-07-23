# HONR 46400 — Course Master Plan (Fall 2026, v2)

**Evidence-Driven Research: How to Design, Analyze, Verify, and Defend Empirical
Research** · Purdue Honors College · Mon/Wed/Fri, 50 min · 5 students, 5
individual projects, 5 posters.

This is the source-of-truth narrative for the v2 build. The machine-readable
spine is `course_config.yaml`; the verified date backbone is
`planning/CALENDAR_BACKBONE.csv` (checked by `scripts/validate_calendar.py`);
the notebook registry is `scripts/notebooks_map.py`; the project chain is
`planning/PROJECT_MILESTONES.md`; question-vs-design classification is
`planning/INQUIRY_MAP.md`. On any conflict, dates defer to the calendar backbone
and *intent* defers to this file. The v1 build is preserved at git tag
`v1-compass-build`; the rebuild rationale is `planning/SOURCE_AUDIT_V2.md`.

---

## 1. Mission and central principle

The course teaches honors students — **without assuming a quantitative or
computing background** — to turn curiosity into credible, defensible,
evidence-based insight: find a real gap, scope a research problem, ask an
answerable question, classify it, match it to a design, produce evidence,
verify results, state uncertainty, and defend the whole thing in writing and out
loud. It is not an intro-stats survey, a software course, or a causal-inference
course; it is a course about **selecting, implementing, verifying, and defending
an evidence strategy that fits a question**, low-floor / high-ceiling throughout.

**The central principle governs every meeting, notebook, and deliverable:**

> **AI is your arm and your research assistant — not your brain.**
> AI may propose. The researcher must verify. The evidence must support.

AI is used at high intensity and under tight control. The disciplined workflow
is **Specify → Delegate → Interrogate → Inspect → Verify → Document → Defend**
(SDIIVDD), taught to students in the everyday shorthand **Ask → Verify →
Document**. Seven decisions are **never delegated** (`ai_policy.never_delegate`):
choosing the problem and question; declaring the design and target population;
choosing measures and judging data quality; ethical judgments; deciding which
claims the evidence justifies; owning uncertainty and limitations; and defending
the project publicly. Every deliverable carries an **AI Research Ledger** entry
(task delegated · tool · prompt · output summary · decision · verification
method · remaining concern · responsible student). Primary tool: Google Gemini
in and alongside Colab; reviewer bench: Purdue GenAI Studio; other tools
permitted with disclosure.

## 2. Weekly architecture — 16 weeks, one notebook per week

16 topics, one notebook per week (`nb00`–`nb15`), across **43 meetings = 27
Mon/Wed lectures + 14 in-person Friday studios + 2 async modules** (dates in
`planning/CALENDAR_BACKBONE.csv`). Slugs and titles are fixed in
`scripts/notebooks_map.py`; the "research decision" column is the project choice
the student commits to that week.

| Calendar exception | Meeting | Date |
|---|---|---|
| Async module (instructor traveling) | m17 | Fri Oct 2 |
| Async module (Thanksgiving replication + red-team) | m37 | Mon Nov 23 |
| No class — Labor Day | — | Mon Sep 7 |
| No class — October break | — | Mon Oct 12 |
| No class — pre-Thanksgiving | — | Wed Nov 18 |
| No class — Thanksgiving | — | Wed/Fri Nov 25 & 27 |
| URC Expo — required poster presentation (not an MWF meeting) | — | Tue Nov 17 |

| Wk | Notebook (slug · title) | Lec | Milestone · due | The week's research decision |
|---|---|---|---|---|
| 1 | `nb00` · Research in the age of AI: your arm, your RA — not your brain | 2 | M0 · Fri Aug 28 | What am I curious about, and how will I work with AI? |
| 2 | `nb01` · From curiosity to a research problem: descriptive, predictive, causal | 2 | M1 · Fri Sep 4 | Which questions in my area are answerable, and what is each one's kind and reach? |
| 3 | `nb02` · Research builds on research: verified evidence + real gaps | 1 | M2 · Fri Sep 11 | What is genuinely known, and where is the real gap? |
| 4 | `nb03` · The anatomy of a research design: MIDA + declare → diagnose → redesign | 2 | M3 · Fri Sep 18 | What are my model, inquiry, data strategy, and answer strategy? |
| 5 | `nb04` · Observational descriptive research | 2 | M4 · Fri Sep 25 | Is my question observational-descriptive, and does the design hold? |
| 6 | `nb05` · Observational causal research | 2 | M5 · Fri Oct 2 (async) | Can I identify a causal effect observationally, or must I stay descriptive? |
| 7 | `nb06` · Experimental descriptive research | 2 | M6 · Fri Oct 9 | How will I measure or acquire data — experimentally or not? |
| 8 | `nb07` · Prediction: generalizing to unseen cases | 1 | M7 · Fri Oct 16 | What is my declared analysis protocol, baseline, metric, and honesty check? |
| 9 | `nb08` · Experimental causal research | 2 | M8 · Fri Oct 23 | What does my minimum viable analysis show? |
| 10 | `nb09` · Share the research + attack the analysis | 2 | M9 · Fri Oct 30 | Does my analysis survive robustness checks and red-teaming? |
| 11 | `nb10` · Poster criticism + final poster lock | 2 | M10 · Fri Nov 6, 5 PM (terminal) | What claim, with what boundary, goes on the poster? |
| 12 | `nb11` · Poster delivery: pitches, uncertainty, difficult questions | 2 | M11 · Fri Nov 13 | How do I pitch under uncertainty and field hard questions? |
| 13 | `nb12` · Final conference preparation, presentation + reflection | 1 | M12 · Fri Nov 20 | How did the claim hold up under public criticism at the Expo (Tue Nov 17)? |
| 14 | `nb13` · Async module: replication + red-team of a peer's package | 0 | M13 · Sun Nov 29 (async) | Does a peer's evidence reproduce, and where is it fragile? |
| 15 | `nb14` · From poster to research note | 2 | M14 · Fri Dec 4 | What is the written, reproducible version of my claim? |
| 16 | `nb15` · Managing multiple AI agents + the final defense | 2 | M15 · Fri Dec 11 (terminal) | Can I defend the whole project and my AI collaboration? |

## 3. The flipped classroom — the Student Research Lead (SRL) system

From Week 2 onward, **every Mon/Wed lecture is student-led**: 25 leadable
lectures (all Mon/Wed except Week 1's two launch meetings), **5 leads per
student** at n = 5, first slot at meeting 4 (`nb01` Lecture 1). The
lead runs a **Socratic investigation, not a summary presentation** — posing the
puzzle, steering the AI investigation, and prompting peer defense; the instructor
formalizes and adjudicates. Each meeting type has a **fixed 50-minute, 4-section
architecture** (`srl:` in `course_config.yaml`):

| Section | **Monday** | **Wednesday** | **Friday studio** |
|---|---|---|---|
| 1 | Student-led research puzzle · 9 | Student-led retrieval & challenge · 7 | Research stand-up · 6 |
| 2 | Guided AI research-partner investigation · 22 | Intensive applied AI laboratory · 23 | Milestone kickoff + AI-supported sprint · 23 |
| 3 | Human verification + instructor formalization · 12 | Peer defense & adversarial questioning · 12 | Peer & AI red-team review · 12 |
| 4 | Decision and defense · 7 | Transfer to the final project · 8 | Revision, ledger, submission · 9 |

**No new topic content on Fridays.** Every Friday is an in-person studio: a
stand-up, then the week's milestone is kicked off from its Brightspace brief and
worked in an AI-supported sprint, red-teamed by peers and an assigned AI role,
then revised, ledgered, and submitted at close. The two async meetings are
self-contained modules with their own assessable artifact.

## 4. The two conceptual layers (critical — kept exactly)

The course runs on **two distinct classification layers**. Conflating them is the
error the design most guards against.

**Layer 1 — the inquiry compass (RDSS ch. 7): classifies QUESTIONS.** Taught in
Week 2 (`nb01`) and used in every declaration thereafter. Two axes: **kind**
(descriptive — what is/was, no counterfactual; vs causal — what would differ
under an intervention) × **reach** (the data at hand · a population beyond the
data · cases not yet seen). This yields four named positions — **Description**,
**Generalization**, **Prediction**, **Causal reasoning** — each with a claim it
permits and a claim it forbids. Overclaiming is always a **crossing without its
license**; the named violations (silent upgrade, leakage, after-therefore-
because, design mimicry) are drilled by name. Full treatment in
`planning/INQUIRY_MAP.md`.

**Layer 2 — the DeclareDesign design library (RDSS ch. 15–18): organizes
DESIGNS.** It gives Weeks 5–9 their sequence, organizing designs by **inquiry
kind × data strategy**: observational descriptive (Wk 5, `nb04`, ch. 15),
observational causal (Wk 6, `nb05`, ch. 16), experimental descriptive (Wk 7,
`nb06`, ch. 17), experimental causal (Wk 9, `nb08`, ch. 18). **Prediction is its
own answer objective** (generalization to unseen observations) — a
course-authored library entry in the book's declare-diagnose-redesign format
(Wk 8, `nb07`), never forced into the descriptive-vs-causal or
observational-vs-experimental grid. **Experimental assignment does not imply a
causal inquiry**: experimental *descriptive* designs exist (Week 7). A student
moves from Layer 1 to Layer 2 by carrying a classified question into a matched
pathway; the crossing-license and claim-boundary machinery from v1 carries over
intact.

## 5. High-intensity, controlled AI use

Every ordinary notebook (`nb00`–`nb15`) instantiates the SDIIVDD discipline
through a fixed set of moves:

- **AI Research Partner briefing** — how to task the tool for this topic.
- **Initial human commitment** — the student's own answer *before* consulting AI.
- **Gemini prompt sequences**, each followed by an **"After running, verify:"**
  checklist recast as a responsible-AI habit (confirm sources exist, cross-check
  facts, log the decision).
- **Required prompt modification** — the student must change a supplied prompt
  and predict the effect, not just run it.
- **AI-output interrogation** — challenge the response for errors, overreach,
  fabricated citations.
- **AI-code verification** — independently confirm any code the AI produced
  before trusting a result.
- **Competing AI roles** where useful (e.g., proposer vs skeptic).
- **Human-Only Checkpoint** — a decision made with AI set aside.
- **AI Research Ledger entry** — the structured disclosure record.
- **Exit Defense** — a claim the student can defend, with its boundary.

**GenAI Studio reviewer bench.** Purdue GenAI Studio supplies custom reviewer
roles at designated milestones (`genai_studio.student_touchpoints`): **M5 Causal
Identification Skeptic**, **M7 Prediction & Leakage Auditor**, **M9 Poster Critic
+ Robustness Reviewer**, **M13 Reproducibility Auditor**. Gemini remains the
primary in-notebook tool; the reviewer bench is an adversarial second opinion the
student must answer, not obey. Studio capability is implemented only at levels
1–4 (prompted role → custom model → RAG assistant → sequential workflow); a
manual-UI fallback is first-class because student API access is unverified.

## 6. The cumulative Research Project Dossier

Every milestone updates one living artifact, the **Research Project Dossier**,
with **13 components** (`dossier_components`): research charter · evidence and
literature map · MIDA design declaration · data and measurement documentation ·
reproducible Colab notebook · declared analysis protocol · claim–evidence table ·
robustness and diagnostic record · AI Research Ledger · poster and presentation
materials · replication record · research note / chapter · AI-agent management
portfolio. The dossier accumulates across all sixteen milestones; the AI Research
Ledger threads through every one. The full milestone chain — develop → present →
submit → revise cadence, kickoff rules, dossier mapping, and the M10/M15 terminal
locks — lives in `planning/PROJECT_MILESTONES.md`.

## 7. Assessment architecture *(proposal — pending instructor confirmation)*

From `course_config.yaml assessment:`; sums to 100. Grading rewards correctness,
transparency, reproducibility, question-design alignment, and responsible
interpretation — never coding elegance. To be reconciled with `syllabus.qmd`.

| Component | Weight |
|---|---|
| Notebook preparation & engagement | 10 |
| Student Research Lead performance | 15 |
| Milestones M0–M9 | 25 |
| Poster & Expo (M10–M12) | 20 |
| Replication & red-team (M13) | 5 |
| Research note + final chapter (M14–M15) | 15 |
| Claim analyses & concept checks | 10 |

## 8. The course book — 37 chapters, six parts

The course ships its own open text, **Evidence-Driven Research** (EDR), a Quarto
book of **37 chapters in six parts** rendered to `docs/book/` and synchronized
with the notebooks by `validate_book_sync.py`. **RDSS remains the theory text**;
EDR is the course-authored narrative that walks students through the same
material at the honors-undergraduate reading level. Part-to-notebook synchronization:

| Part | EDR chapters | Notebooks |
|---|---|---|
| I — Foundations: research and AI | 1–4 | `nb00` |
| II — From curiosity to a classified question | 5–10 | `nb01`–`nb03` |
| III — Designs I: observational & the compass in practice | 11–16 | `nb04`–`nb08` |
| IV — Designs II: experiments, prediction, robustness | 17–24 | `nb07`–`nb09` + cross-cutting |
| V — Communicating and defending evidence | 25–31 | `nb10`–`nb12` |
| VI — Replication, the research note, managing AI | 32–37 | `nb13`–`nb15` |

The book is the largest scope item and is sequenced last in the build, gated by
its sync validator. Bergstrom & West, *Calling Bullshit*, is optional/parallel
reading used lightly to sharpen claim evaluation.

## 9. Provenance and change log

Every schedule row and notebook records source · chapter/section/dataset ·
transformation (adapted / translated / extended / newly constructed). Empirical
claims trace to a real, retrievable source; results are verified before reported;
decisions are documented, not just outcomes (`scripts/audit_sources.py`,
`scripts/voice_lint_notebooks.py` enforce this).

- **v2 (2026-07-23)** — Prompt-architecture rebuild per instructor ruling
  (`SOURCE_AUDIT_V2.md` §3): 16 weekly topics `nb00`–`nb15`; milestones M0–M15;
  Student Research Lead flipped classroom; SDIIVDD AI discipline + AI Research
  Ledger; DeclareDesign design-library pathway weeks (5–9); GenAI Studio reviewer
  bench; peer replication/red-team (M13); research-note genre; 37-chapter course
  book. Calendar moves to 43 meetings (one fewer Wednesday lecture — flagged for
  final syllabus confirmation).
- **v1 (compass build, 2026-07-18 → 07-20)** — 20 notebooks `nb00`–`nb19`,
  milestones M00–M23, Friday-studio + undergraduate-voice redesign (D13–D16).
  Preserved at git tag `v1-compass-build`; strong material (compass definitions,
  crossing-license drills, claim-boundary vocabulary) mined into v2.
