# HONR 46400 — Course Master Plan (Fall 2026, v2)

**Evidence-Driven Research: How to Design, Analyze, Verify, and Defend Empirical
Research** · Purdue Honors College · Mon/Wed/Fri, 50 min · 6 students ·
individual projects by default, with instructor-approved group projects allowed.

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
in-person Mon/Wed lectures + 14 in-person Friday studios + 2 asynchronous
online sessions** — 41 meetings in person and 2 online (dates in
`planning/CALENDAR_BACKBONE.csv`; counts in `course_config.yaml calendar:`).
Slugs and titles are fixed in `scripts/notebooks_map.py`; the "research
decision" column is the project choice the student commits to that week.

| Calendar exception | Meeting | Date |
|---|---|---|
| Asynchronous online — post-Expo audience-data capture | m36 | Fri Nov 20 |
| Asynchronous online — Thanksgiving reflection module | m37 | Mon Nov 23 |
| No class — Labor Day | — | Mon Sep 7 |
| No class — October break | — | Mon Oct 12 |
| No class — pre-Thanksgiving | — | Wed Nov 18 |
| No class — Thanksgiving | — | Wed/Fri Nov 25 & 27 |
| URC Expo — required poster presentation (not an MWF meeting) | — | Tue Nov 17 |

Since **D49** the weekly spine IS the book's Studio arc, one Studio per week:
**Monday and Wednesday teach that Studio's lessons together with their "It is
your turn" work, and Friday IS that Studio's milestone.** Studios 1–12 fall on
Weeks 1–12, which puts every fixed date where the book already wants it — the
URC abstract gate (Fri Oct 9) on Studio 7's first result, the terminal poster
lock (Sun Nov 8) on Studio 11's reproduction gate, and Studio 12's release
audit the week *before* the Expo, so the Expo is the release. Weeks 13–16 are
the four date-driven exception weeks; they anchor no new lesson and revisit
what the studios built. Week 1's Monday is the instructor-led orientation, the
one other exception. Course milestone M(n) presents book Milestone (n+1)
through M16 (`planning/COURSE_BOOK_CROSSWALK.yml`). **D54 retired M17**: Week 16
teaches Studio 12 but collects nothing, and its Friday is the course-closing
reflection. **D55**: a milestone is worked at its Friday studio and due the
Sunday after, 11:59 PM.

| Wk | Studio (notebook) | Lec | Milestone · due | The week's research decision |
|---|---|---|---|---|
| 1 | S1 Frame the inquiry (`nb01`) | 2 | M1 · Sun Aug 30 | What am I curious about, what do I already believe, and what evidence would change my mind? |
| 2 | S2 Govern the work (`nb02`) | 2 | M2 · Mon Sep 7 (Labor Day) | How will my tools and I work — and what exactly am I asking, in what kind and reach? |
| 3 | S3 Ground it in verified evidence (`nb03`) | 1 | M3 · Sun Sep 13 | What is genuinely known, what is unresolved, and how must my question change? |
| 4 | S4 Declare and diagnose provisionally (`nb04`) | 2 | M4 · Sun Sep 20 | What is my Contract v0 — MIDA, uncertainty, provisional measures, permission status? |
| 5 | S5 Develop the pathway — route hub (`nb05`) | 2 | M5 · Sun Sep 27 | Which route do my question and licence support, and what can it never establish? |
| 6 | S6 Govern data and measurement (`nb06`) | 2 | M6 · Sun Oct 4 | How did the data reach me, under what permission, and do my measures measure my concepts? |
| 7 | S7 Produce a reproducible first analysis (`nb07`) | 2 | M7 · Tue Oct 13 (October Break) | What does my declared analysis actually produce, with what uncertainty, traceable to which cell? |
| 8 | S8 Stress-test and adjudicate (`nb08`) | 1 | M8 · Sun Oct 18 | Which checks did I pre-list, what survived them, and what remains unruled-out? |
| 9 | S9 Write, bound, and disclose (`nb09`) | 2 | M9 · Sun Oct 25 | What bounded claim can I write down, with every sentence traced to evidence and disclosure? |
| 10 | S10 Adapt and defend (`nb10`) | 2 | M10 · Sun Nov 1 | What does my venue require, and what artifact satisfies it without inflating the claim? |
| 11 | Conference block: poster production + peer review (`nb11`) | 2 | M11 · Wed Nov 4 at class; M12 · Fri Nov 6, 2:30 PM; M13 · Sun Nov 8, 11:59 PM (terminal) | Is the poster traceable to my evidence, and does peer criticism reach me before the lock? |
| 12 | Conference block: presentation preparation (`nb12`) | 2 | M14 · Sun Nov 15 | Can I say this work in thirty seconds, ninety, and two minutes — and take the hard question? |
| 13 | The public test: dress rehearsal + the Expo (`nb13`) | 1 | — (Expo Tue Nov 17) | What does a room of strangers ask that I had not prepared for? |
| 14 | Async reflection: what the public test returned (`nb14`) | 0 | M15 · Sun Nov 29 (async) | Does public questioning change the claim, its boundary, or only how I say it? |
| 15 | S11 Reproduce and package (`nb15`) | 2 | M16 · Sun Dec 6 (the final milestone) | Does my work reproduce from a clean package in a stranger's hands, and what did I accept, rebut, or bound? |
| 16 | S12 Release and direct the next cycle (`nb16`) | 2 | — (Fri Dec 11 is the course-closing reflection, under participation) | Do I release or withhold pending a named repair, and what should the next study ask? |

## 3. The lecture format — the ten-minute lab meeting *(D74, amended D75)*

From Week 2 onward, **every Mon/Wed lecture opens with a ten-minute lab
meeting**: 25 lectures carry one (all Mon/Wed except Week 1's two launch
meetings), the first at meeting 4 (`nb02` Lecture 1). Since **D75** it is an
**open round with nothing assigned**: the instructor asks the room how the
projects are going, and the room answers — what was decided since last time,
what the evidence looks like, where somebody is stuck. **No student is
designated to present, on any lecture; there is no slot draw, no assigned
question, and nothing is prepared before class by anyone.** Nothing said in the
lab meeting is graded. **The instructor leads from minute 10** and owns
accuracy, the AI tooling, and the clock. Each lecture's **📣 Lab Meeting**
section is a student-visible cell that opens that lecture in its notebook and
states plainly that nobody is assigned and nothing is prepared. The notebook
itself is submitted weekly, under the Lecture Notebooks contract in §7 — the
lead's day-before notebook submission (D66) went with the role, and
`lab_meeting.prep_cadence`, now `none`, is the rule.
Each meeting type has a **fixed 50-minute architecture** (`lab_meeting:` in
`course_config.yaml`; Mon/Wed 4 sections, Friday 3):

| Section | **Monday** | **Wednesday** | **Friday studio** |
|---|---|---|---|
| 1 | Lab meeting: how the projects are going · 10 | Lab meeting: how the projects are going · 10 | Research stand-up · 5 |
| 2 | Guided AI research-partner investigation · 21 | Intensive applied AI laboratory · 20 | Milestone kickoff + AI-supported work · 40 |
| 3 | Human verification + instructor formalization · 12 | Peer defense & adversarial questioning · 12 (defense to 38, then instructor synthesis + accuracy lock · D34) | Revision, ledger, submission · 5 |
| 4 | Decision and defense · 7 | Transfer to the final project · 8 | — |

Both Mon/Wed frames still sum to 50. The lab meeting takes the opener, and the
🧩 Research Puzzle folds into the front of the investigation block, now opened
by the instructor. Section boundaries 3 and 4 are unchanged (31–43 / 43–50
Monday, 30–42 / 42–50 Wednesday), so D22's and D34's later-block rulings stand
untouched, and Friday's 5 / 40 / 5 frame (D58) is unaffected.

**The Student Research Lead (SRL) system is retired for this edition and kept
in full for a future one (D74, Ruling 5).** It ran the same 25 Mon/Wed slots
with a random draw, but the student *led the lecture* — a Socratic
investigation of the day's concept — and was graded on it as a 25% category.
Two design passes found that the fear the format produced was design-caused,
and that its largest source was being graded on teaching unfamiliar
quantitative content to peers. D74 removed that source rather than softening
it, replacing the lead with an ungraded **reporter** who spoke for seven
minutes about their own project and took three minutes of questions.
**Nothing is deleted.** All of `project/srl/` (handbook, rubric,
Socratic question bank, AI integration guide, prep template, peer feedback
form, submission instructions, absent-lead and instructor-intervention
protocols), `scripts/assign_srl_slots.py`, and `scripts/build_srl_packet.py`
stay on disk, exactly as D58 kept the quiz banks. What is retired is the grade
category and the live role, never the material; the per-lecture questions guide
is kept in full and re-owned to the instructor (in the notebooks as
**🔎 Questions to Keep You Thinking**).

**D75 withdrew the assignment as well — this passage's slot draw is retired in
place.** D74 had carried the D69/D71 draw over unchanged (25 slots, drawn
`4/4/4/4/4/5` at six students) and renamed what it produced, so each lecture had
a reporter instead of a lead. **That is no longer in force.** No reporter is
designated on any lecture, the draw is withdrawn for this edition, no question is
assigned, and nothing is prepared. The reasoning: a designated, dated,
individually-owned slot is still a performance with your name on a calendar, and
an open round needs no draw, no packet, no announcement and no swap rule while
reaching every student every lecture rather than one student every fourth
lecture. Kept on disk and unapplied, alongside the SRL material above:
`scripts/assign_srl_slots.py`, `scripts/build_srl_packet.py`, the drawn roster in
`_adm/roster/`, `planning/SRL_ASSIGNMENT_SCHEDULE.md`, and the
**📣 My Report Plan** cell, which `scripts/nbbuild.py` no longer injects
(`INJECT_REPORT_PLAN = False`) but whose `REPORT_PLAN` constant remains in the
script. Reinstating the reporter model in a future edition costs flipping that
flag and re-running the draw. ⚠ If the Week-1 announcement naming students'
slots was already posted, the withdrawal has to reach them on the course
platform; the repository cannot do that.

**No new topic content on Fridays.** Every Friday is an in-person studio: a
research stand-up, then the week's milestone is kicked off from its Brightspace
brief and WORKED ON with the student's AI assistant (the weekly peer red-team
block was retired, D30; GenAI Studio reviewer roles still apply at designated
milestones), then revised, ledgered, and submitted at close. **D58 retired the
opening 10-minute quiz block for this edition** — no quiz is administered and
nothing is scored on one — and the milestone sprint absorbed those ten minutes,
so the Friday frame is 5 / 40 / 5. The two asynchronous online sessions (Fri
Nov 20 and Mon Nov 23) are self-contained modules with their own assessable
artifacts.

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
roles at designated milestones (`genai_studio.student_touchpoints`, D41): **M5 Causal
Identification Skeptic** (route declaration), **M8 Prediction & Leakage
Auditor**, **M9 Robustness & Sensitivity Reviewer**, **M13 Poster Critic**
(at the lock), **M16 Reproducibility Auditor**. Gemini remains the
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
materials · replication record · research note. The dossier accumulates across
all sixteen milestones; the AI Research Ledger threads through every one. The
full milestone chain — develop → present → submit → revise cadence, kickoff
rules, dossier mapping, and the M13 terminal lock — lives in
`planning/PROJECT_MILESTONES.md`.

## 7. Assessment architecture *(D52, amended D57/D58/D61, and D74, 2026-08-31)*

From `course_config.yaml assessment:`; sums to 100 and matches `syllabus.qmd`.
Grading rewards correctness, transparency, reproducibility, question-design
alignment, and responsible interpretation — never coding elegance.

| Component | Weight |
|---|---|
| Attendance (iClicker) | 1 |
| Participation (studio feedback surveys + profile survey + course reflection + other constructive contributions; one undivided block, D57, amended D58) | 9 |
| IYT Practice (the book's "It is your turn" sections, due on each chapter's reading date; completion, D58, amended D61) | 15 |
| Lecture Notebooks (the weekly `nbNN` worked in class, submitted; completion, D74) | 20 |
| Final Project | 55 |
| **Total** | **100** |

**Lecture Notebooks (20%) is the course's third undivided completion
contract**, with the same mechanics as participation and IYT Practice: one
submission per week per student — the notebook `nbNN` worked in class — due
**11:59 PM on the Sunday that ends the studio week** (Week 16 closes Fri Dec 11,
the last class day); graded on **completion only**, never on whether the answers
came out right and never on anything said in the lab meeting; credit `1.0`
on time, `0.5` within seven days, `0` otherwise; `N = 16` and
`d = ⌈0.10 × 16⌉ = 2`, so `points = 20.0 × (sum of the highest 14 credits) / 14`.
It is **not** participation, and it never carries participation's ±0.9
contribution adjustment — D57's ban stands in its amended form: lecture-notebook
completion may never return **as a participation item**. What the submission
covers is the seven in-class moves and the 📒 AI Research Ledger row for each
lecture; **D75 removed the 📣 My Report Plan cell it used to name as well**, so
the contract names no lab-meeting cell at all. Every number above is D74's,
unchanged. Machine spine:
`course_config.yaml lecture_notebooks:`; dated list: the generated
`planning/LECTURE_NOTEBOOK_SCHEDULE.md`.

**The 25% Student Research Lead category is retired for this edition**, and its
nine-row live rubric is not applied (the rubric file stays on disk — §3). The
20 points above replace it, and the remaining 5 are forced inside the Final
Project, which rises from 50% to 55%.

Final Project is the course's single project-grading category. It uses QM474's
five operative component items without renaming or replacing them, but **D74 is
the seventh documented deviation** from D53's verbatim adoption: Milestone
Deliverables takes the five freed points, so the project-share column no longer
reads 30/20/10/20/20. Because `20 / 55` does not terminate, student-facing
surfaces now print **course** percentages of the final grade: **Milestone
Deliverables 20%**, **Peer Evaluation 10%**, **Peer Review 5%**, **Poster
Presentation at the Purdue Undergraduate Research Conference 10%**, and
**Instructor/TA Evaluation 10%** — 55% in total. `course_config.yaml
final_project_breakdown:` keeps the exact project shares
(36.37 / 18.18 / 9.09 / 18.18 / 18.18, summing to 100.00) as the machine record
only. No component was renamed and no scoring rule inside a component changed.

Individual work is the default; a group project requires instructor approval
before shared work begins. With six students, at most one group of two or
three may be approved. Approvals must preserve at least three active
projects for Peer Review and allow two observers per individual researcher plus
at least one evaluation submission per student. Milestone Deliverables is the
equal-weight mean of M1–M16. Group members receive common scores on shared rubric
rows, while requirements marked individual are scored per member; recorded
milestone scores may differ only on those rows. Peer Evaluation uses actual
confidential ratings: every teammate for a group project, or two assigned project peers for
an individual project. Peer Review remains each student's independent criticism
of every other active project. The conference item combines `70%` M13 poster
quality and `30%` individual M15 live delivery. Instructor/TA Evaluation is the
instructor's evaluation of the M13 final poster submission, judged as research
communication (D54). The syllabus carries only the weights
and the five component descriptions; the "comprehensive set of project
guidelines" it promises is the student-facing
`_research_project/2026Fall/final_project_grading_and_project_modes.md`, its
gradebook implementation is the generated `brightspace/gradebook_spec.md`, and
the full arithmetic and design reconciliation is
`planning/ASSESSMENT_ARCHITECTURE.md`.

## 8. The course book — EDR|AI: 40 lessons, 12 Studios, 12 Milestone chapters

The course ships its own open text, **EDR|AI — Evidence-Driven Research in the
Age of AI: How to Design, Analyze, Verify, and Defend** (**EDR|AI**), a Quarto
book rendered to `docs/book/` and synchronized with the notebooks by
`validate_book_sync.py`. Since D38 the book's twelve **Studios** are its
navigational parts (40 lessons partitioned 1/6/2/4/6/2/2/4/4/4/2/3 after the D45 flip and the D46 declaration lesson), and
since D40 each Studio closes with a generated **Milestone chapter**
("Milestone N: <artifact-first title>") carrying the practice steps, rails,
authored rubric, and workbook badge. The book is presented to students as a
**work in progress**, under development across the semester. **RDSS remains
the theory text**; EDR|AI chapters are the REQUIRED reading and the matching
RDSS chapters are RECOMMENDED (route lessons: own route + one assigned
contrast; hybrid when the design has stages — D41). Course adoption is machine-defined: the
**crosswalk** (`planning/COURSE_BOOK_CROSSWALK.yml`, schema 1.1) maps every
lesson to exactly one home milestone (40-lesson bijection), fires every
studio checkpoint, and carries the D40 naming bridge (course milestones
M1–M16 present book Milestones 1–11 as versions; no course milestone presents Book Milestone 12). Studio↔week alignment is
§2's table; per-lesson detail is the generated `planning/BOOK_MAP.md` and
the For Instructors adoption table.

The book is the largest scope item and is sequenced last in the build, gated by
its sync validator.

## 9. Provenance and change log

Every schedule row and notebook records source · chapter/section/dataset ·
transformation (adapted / translated / extended / newly constructed). Empirical
claims trace to a real, retrievable source; results are verified before reported;
decisions are documented, not just outcomes (`scripts/audit_sources.py`,
`scripts/voice_lint_notebooks.py` enforce this).

- **v6 (2026-08-31, D75)** — The lab meeting **loses its reporter**. The
  ten-minute opener stays exactly where D74 put it, but nothing inside it is
  assigned: **no reporter on any lecture, no slot draw** (the D69/D71 assignment
  is withdrawn for this edition), **no assigned question, and no preparation** by
  anyone. The instructor asks the room how the projects are going and the room
  answers; from minute 10 the instructor leads the lesson, as D74 already ruled.
  The injected **📣 My Report Plan** cell is removed from every notebook and the
  cell heading becomes **📣 Lab Meeting**. **No weight, formula, `N` or drop
  count moved** — the frames (Mon 10/21/12/7, Wed 10/20/12/8, Friday 5/40/5), the
  weight table (1 · 9 · 15 · 20 · 55) and the Lecture Notebooks contract
  (N = 16, d = 2, the Sunday rule with its Fri Sep 4 and Fri Dec 11 exceptions)
  are untouched; only that contract's content list changes, since it no longer
  names a lab-meeting cell. Nothing was deleted: the SRL material, both SRL
  scripts, the drawn roster and `nbbuild.py`'s `REPORT_PLAN` constant are all
  kept, unapplied, for a future edition.
- **v5 (2026-08-31, D74)** — The Student Research Lead becomes the **lab
  meeting**: every Mon/Wed lecture from Week 2 opens with ten minutes in which
  one student reports a decision from their own project (7 min) and takes the
  room's questions (3 min), and the **instructor leads from minute 10**. Frames
  retimed to 10 / 21 / 12 / 7 (Mon) and 10 / 20 / 12 / 8 (Wed), both still 50;
  boundaries 3 and 4 and the Friday 5 / 40 / 5 frame untouched. The **25% SRL
  category is retired** and replaced by **Lecture Notebooks 20%**, the third
  undivided completion contract (weekly `nbNN`, Sunday 11:59 PM, completion
  only, N = 16, d = 2); the 5 freed points go to **Milestone Deliverables
  (15 → 20 course points)**, so the **Final Project rises 50% → 55%**. Nothing
  was deleted: every SRL file and script is kept for a future edition, and the
  per-lecture questions guide is kept in full and re-owned to the instructor.
  The D69/D71 draw carries over unchanged and now names reporters *(both the
  reporter and the draw were withdrawn the same day — see v6, D75)*. Also
  corrected here: the calendar prose, which had read 42 in-person meetings and
  one async module rather than **41 in person and 2 asynchronous online
  sessions**.
- **v4 (2026-08-05, D49)** — Realigned to the book's current 40-lesson,
  12-Studio design (D42–D48) and ruled to **one Studio per week**: MW teach
  the studio's lessons with their IYT, Friday is the studio milestone.
  Studios 1–12 → Weeks 1–12 (so M(n) presents book Milestone (n+1));
  Weeks 13–16 are the date-driven exception weeks. Every notebook from
  Week 1 Wednesday to Week 16 rewritten to its new studio.
- **v3 (2026-08-03, D41)** — Option 2: the studio-first route-selective
  semester. Weekly spine = the book's 12 Studios (D38/D40); W5 route hub
  (own route + one assigned contrast, five-route jigsaw); W6=S6, W7–8=S7
  (build/verify), W9=S8, W10=S9 note v0 before the poster; release
  preflight + author self-reproduction gate before the poster lock (Nov 6 at
  the time; the terminal lock is Sun Nov 8, 11:59 PM since D50);
  crosswalk schema 1.1 with the book-Milestone naming bridge; milestone
  chain retitled; Synthetic Colleague device (COURSE_REFRAME_OPTIONS.md)
  at standard intensity. Content phase (briefs prose, schedule_data,
  quizzes, SRL briefs, nb05–nb16 rebuild) tracked in D41.
- **v2 (2026-07-23)** — Prompt-architecture rebuild per instructor ruling
  (`SOURCE_AUDIT_V2.md` §3): 16 weekly topics `nb01`–`nb16`; milestones M1–M17 (M1–M16 since D54);
  Student Research Lead flipped classroom; SDIIVDD AI discipline + AI Research
  Ledger; DeclareDesign design-library pathway weeks (5–9); GenAI Studio reviewer
  bench; peer replication/red-team (M16); research-note genre; 37-chapter course
  book. Calendar moves to 43 meetings (one fewer Wednesday lecture — flagged for
  final syllabus confirmation).
- **v1 (compass build, 2026-07-18 → 07-20)** — 20 notebooks `nb01`–`nb19`,
  milestones M01–M23, Friday-studio + undergraduate-voice redesign (D13–D16).
  Preserved at git tag `v1-compass-build`; strong material (compass definitions,
  crossing-license drills, claim-boundary vocabulary) mined into v2.
