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

> **AI is your arm and your research assistant, not your brain.**
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
method · remaining concern · responsible researcher). Primary tool: Google Gemini
in and alongside Colab; reviewer bench: Purdue GenAI Studio; other tools
permitted with disclosure.

## 2. Weekly architecture — 16 weeks, one notebook per week

16 topics, one notebook per week (`nb01`–`nb16`), across **43 meetings = 27
Mon/Wed lectures + 15 in-person Friday studios + 1 async module** (dates in
`planning/CALENDAR_BACKBONE.csv`). Slugs and titles are fixed in
`scripts/notebooks_map.py`; the "research decision" column is the project choice
the student commits to that week.

| Calendar exception | Meeting | Date |
|---|---|---|
| Async module (Thanksgiving replication + red-team) | m37 | Mon Nov 23 |
| No class — Labor Day | — | Mon Sep 7 |
| No class — October break | — | Mon Oct 12 |
| No class — pre-Thanksgiving | — | Wed Nov 18 |
| No class — Thanksgiving | — | Wed/Fri Nov 25 & 27 |
| URC Expo — required poster presentation (not an MWF meeting) | — | Tue Nov 17 |

Since D41 the weekly spine IS the book's Studio arc (D38/D40): each week runs
one Studio sprint (Studios 7 and 10 span two and three weeks; W15 closes
Studios 9 and 11 together), and each course milestone presents a **book
Milestone version** (the bridge column lives in
`planning/PROJECT_MILESTONES.md` and the crosswalk's `book_milestones:`
blocks). Notebook slugs are permanent compatibility ids; nb05–nb16 display
titles and cell content are rebuilt to the studio topics in the D41 content
phase (before launch).

| Wk | Studio sprint (notebook) | Lec | Milestone · due | The week's research decision |
|---|---|---|---|---|
| 1 | S1 Begin the research and govern the work (`nb01`) | 2 | M0 · Fri Aug 28 | What stays human, what may be delegated, and how will every delegation be checked and recorded? |
| 2 | S2 Frame the inquiry (`nb02`) | 2 | M1 · Fri Sep 4 | What exactly am I asking — kind, reach, units, outcome, and claim boundary? |
| 3 | S3 Ground it in verified evidence (`nb03`) | 1 | M2 · Fri Sep 11 | What is genuinely known, what is unresolved, and how must my question change? |
| 4 | S4 Declare and diagnose provisionally (`nb04`) | 2 | M3 · Fri Sep 18 | What is my provisional Contract v0 — MIDA, operationalization, uncertainty, permission status? |
| 5 | S5 Develop the pathway — route hub (`nb05`) | 2 | M4 · Fri Sep 25 | Which route do my question and licence support, what does the mandated contrast rule out, and what can my route never establish? |
| 6 | S6 Govern data and measurement (`nb06`) | 2 | M5 · Fri Oct 2 | How do data reach me, under what permission, and do my measures measure my concepts? |
| 7 | S7 Produce a reproducible first analysis — build (`nb07`) | 2 | M6 · Fri Oct 9 | What code executes my declared analysis, and what first result does it produce with uncertainty? |
| 8 | S7 Verify the first analysis — clean restart (`nb08`) | 1 | M7 · Fri Oct 16 | Does the result survive a clean restart, and does every claim trace to a verified output? |
| 9 | S8 Stress-test and adjudicate (`nb09`) | 2 | M8 · Fri Oct 23 | Which checks were pre-listed, what survived them, and what remains unruled-out? |
| 10 | S9 Write, bound, and disclose — note v0 (`nb10`) | 2 | M9 · Fri Oct 30 | What bounded claim can I write down, with every sentence traced to evidence and disclosure? |
| 11 | S10 Poster adaptation + reproduction gate + lock (`nb11`) | 2 | M10 · Fri Nov 6, 5 PM (terminal) | Which labeled-preliminary claim goes on the poster, and has it passed self-reproduction and the release preflight? |
| 12 | S10 Pitch and defense rehearsal (`nb12`) | 2 | M11 · Fri Nov 13 | How do I compress without inflating, and answer the hardest fair questions? |
| 13 | S10 Public test at the Expo + reflection (`nb13`) | 1 | M12 · Fri Nov 20 | What did public questioning reveal, and what must change in the claim or its defense (Expo Tue Nov 17)? |
| 14 | S11 Async: peer cold run + red-team (`nb14`) | 0 | M13 · Sun Nov 29 (async) | Does a peer's evidence reproduce without author help, and where is it fragile? |
| 15 | S9+S11 Research note v1 + reusable package (`nb15`) | 2 | M14 · Fri Dec 4 | What changed after public criticism and the cold run, and is the revised package reusable? |
| 16 | S12 Special topic: agentic AI, release, and the next cycle (`nb16`) | 2 | M15 · Fri Dec 11 (terminal) | Is the latest package still reproduced, why am I stopping, and what should the next study ask? |

## 3. The flipped classroom — the Student Research Lead (SRL) system

From Week 2 onward, **every Mon/Wed lecture is student-led**: 25 leadable
lectures (all Mon/Wed except Week 1's two launch meetings), **slots randomly
assigned at the start of the semester** (no sequential rotation, no seats),
first slot at meeting 4 (`nb02` Lecture 1). Each lecture's **SRL Lead Brief**
is a student-visible section that opens that lecture in its notebook; leads
prepare from about one week ahead and submit a preparation script/notebook two
days ahead. The lead runs a **Socratic investigation, not a summary
presentation** — posing the puzzle, steering the AI investigation, and
prompting peer defense; the instructor formalizes and adjudicates. The brief is
a floor, not a ceiling: creative staging within the fixed frame is expected.
Each meeting type has a **fixed 50-minute architecture** (`srl:` in
`course_config.yaml`; Mon/Wed 4 sections, Friday 5):

| Section | **Monday** | **Wednesday** | **Friday studio** |
|---|---|---|---|
| 1 | Student-led research puzzle · 9 | Student-led retrieval & challenge · 7 | Weekly topic quiz (MC) · 10 |
| 2 | Guided AI research-partner investigation · 22 | Intensive applied AI laboratory · 23 | Research stand-up · 5 |
| 3 | Human verification + instructor formalization · 12 | Peer defense & adversarial questioning · 12 (defense to 38, then SRL synthesis + instructor accuracy lock · D34) | Milestone kickoff + AI-supported work · 30 |
| 4 | Decision and defense · 7 | Transfer to the final project · 8 | Revision, ledger, submission · 5 |
| 5 | — | — | — |

**No new topic content on Fridays.** Every Friday is an in-person studio: a
10-minute multiple-choice quiz on the week's topic (printed; solo; graded),
a stand-up, then the week's milestone is kicked off from its Brightspace brief
and WORKED ON with the student's AI assistant (the weekly peer red-team block
was retired, D30; GenAI Studio reviewer roles still apply at designated
milestones), then revised, ledgered, and submitted at close. The async
meeting is a self-contained module with its own assessable artifact.

## 4. The two conceptual layers (critical — kept exactly)

The course runs on **two distinct classification layers**. Conflating them is the
error the design most guards against.

**Layer 1 — the inquiry compass (RDSS ch. 7): classifies QUESTIONS.** Taught in
Week 2 (`nb02`) and used in every declaration thereafter. Two axes: **kind**
(descriptive — what is/was, no counterfactual; vs causal — what would differ
under an intervention) × **reach** (the data at hand · a population beyond the
data · cases not yet seen). This yields four named positions — **Description**,
**Generalization**, **Prediction**, **Causal reasoning** — each with a claim it
permits and a claim it forbids. Overclaiming is always a **crossing without its
license**; the named violations (silent upgrade, leakage, after-therefore-
because, design mimicry) are drilled by name. Full treatment in
`planning/INQUIRY_MAP.md`.

**Layer 2 — the DeclareDesign design library (RDSS ch. 15–18): organizes
DESIGNS.** Since D41 it powers the **Week 5 route hub** (Studio 5): all five
pathway lessons meet in one week — observational descriptive (ch. 15),
observational causal (ch. 16), experimental descriptive (ch. 17), prediction
(course-authored library entry), experimental causal (ch. 18) — and each
student commits to ONE route (own route-required lesson + one
instructor-assigned contrast; a five-route jigsaw with advocate roles covers
the rest; `hybrid-complex-designs` binds only when the design has stages).
**Prediction is its own answer objective** (generalization to unseen
observations), never forced into the descriptive-vs-causal or
observational-vs-experimental grid. **Experimental assignment does not imply a
causal inquiry**: experimental *descriptive* designs exist (a Week-5 route). A student
moves from Layer 1 to Layer 2 by carrying a classified question into a matched
pathway; the crossing-license and claim-boundary machinery from v1 carries over
intact.

## 5. High-intensity, controlled AI use

Every ordinary notebook (`nb01`–`nb16`) instantiates the SDIIVDD discipline
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
- **Defend Your Decision** — a claim the student can defend, with its boundary.

**GenAI Studio reviewer bench.** Purdue GenAI Studio supplies custom reviewer
roles at designated milestones (`genai_studio.student_touchpoints`, D41): **M4 Causal
Identification Skeptic** (route declaration), **M7 Prediction & Leakage
Auditor**, **M8 Robustness & Sensitivity Reviewer**, **M10 Poster Critic**
(at the lock), **M13 Reproducibility Auditor**. Gemini remains the
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

## 7. Assessment architecture *(confirmed 2026-07-27)*

From `course_config.yaml assessment:`; sums to 100 and matches `syllabus.qmd`.
Grading rewards correctness, transparency, reproducibility, question-design
alignment, and responsible interpretation — never coding elegance.

| Component | Weight |
|---|---|
| Attendance (iClicker) | 1 |
| Participation (notebook completion + in-class activities + surveys) | 9 |
| Quizzes (weekly Friday MC topic quizzes) | 20 |
| Student Research Lead performance | 20 |
| Final Project Milestones | 20 |
| Final Project | 20 |
| Research artifact (paper/chapter/note) | 10 |

## 8. The course book — EDR|AI: 39 lessons, 12 Studios, 12 Milestone chapters

The course ships its own open text, **EDR|AI — Evidence-Driven Research in the
Age of AI: How to Design, Analyze, Verify, and Defend** (**EDR|AI**), a Quarto
book rendered to `docs/book/` and synchronized with the notebooks by
`validate_book_sync.py`. Since D38 the book's twelve **Studios** are its
navigational parts (39 lessons partitioned 4/2/2/4/6/2/2/4/4/4/2/3), and
since D40 each Studio closes with a generated **Milestone chapter**
("Milestone N: <artifact-first title>") carrying the practice steps, rails,
authored rubric, and workbook badge. The book is presented to students as a
**work in progress**, under development across the semester. **RDSS remains
the theory text**; EDR|AI chapters are the REQUIRED reading and the matching
RDSS chapters are RECOMMENDED (route lessons: own route + one assigned
contrast; hybrid when the design has stages — D41). Course adoption is machine-defined: the
**crosswalk** (`planning/COURSE_BOOK_CROSSWALK.yml`, schema 1.1) maps every
lesson to exactly one home milestone (39-lesson bijection), fires every
studio checkpoint, and carries the D40 naming bridge (course milestones
M0–M15 present book Milestones 1–12 as versions). Studio↔week alignment is
§2's table; per-lesson detail is the generated `planning/BOOK_MAP.md` and
the For Instructors adoption table.

The book is the largest scope item and is sequenced last in the build, gated by
its sync validator. Bergstrom & West, *Calling Bullshit*, is optional/parallel
reading used lightly to sharpen claim evaluation.

## 9. Provenance and change log

Every schedule row and notebook records source · chapter/section/dataset ·
transformation (adapted / translated / extended / newly constructed). Empirical
claims trace to a real, retrievable source; results are verified before reported;
decisions are documented, not just outcomes (`scripts/audit_sources.py`,
`scripts/voice_lint_notebooks.py` enforce this).

- **v3 (2026-08-03, D41)** — Option 2: the studio-first route-selective
  semester. Weekly spine = the book's 12 Studios (D38/D40); W5 route hub
  (own route + one assigned contrast, five-route jigsaw); W6=S6, W7–8=S7
  (build/verify), W9=S8, W10=S9 note v0 before the poster; release
  preflight + author self-reproduction gate before the Nov 6 lock;
  crosswalk schema 1.1 with the book-Milestone naming bridge; milestone
  chain retitled; Synthetic Colleague device (COURSE_REFRAME_OPTIONS.md)
  at standard intensity. Content phase (briefs prose, schedule_data,
  quizzes, SRL briefs, nb05–nb16 rebuild) tracked in D41.
- **v2 (2026-07-23)** — Prompt-architecture rebuild per instructor ruling
  (`SOURCE_AUDIT_V2.md` §3): 16 weekly topics `nb01`–`nb16`; milestones M0–M15;
  Student Research Lead flipped classroom; SDIIVDD AI discipline + AI Research
  Ledger; DeclareDesign design-library pathway weeks (5–9); GenAI Studio reviewer
  bench; peer replication/red-team (M13); research-note genre; 37-chapter course
  book. Calendar moves to 43 meetings (one fewer Wednesday lecture — flagged for
  final syllabus confirmation).
- **v1 (compass build, 2026-07-18 → 07-20)** — 20 notebooks `nb01`–`nb19`,
  milestones M00–M23, Friday-studio + undergraduate-voice redesign (D13–D16).
  Preserved at git tag `v1-compass-build`; strong material (compass definitions,
  crossing-license drills, claim-boundary vocabulary) mined into v2.
