> **Registry status (2026-07-23).** D1–D11 are legacy seeds from MGMT474: D2/D3/D9
> are DROPPED for HONR 46400, D10 is superseded by D14, the rest survive only where
> restated below or in CLAUDE.md. D12–D16 are the 2026-07-19/20 HONR rulings; parts
> of D12 (sequencing) and D13 (Friday section format) are superseded by **D17**.
> D17–D21 (2026-07-22/23) govern the current v2 build. The full v1 build is
> preserved at git tag `v1-compass-build`.

# Course Design Decisions

This document records design decisions made during course development and the reasoning behind them. Decisions here are **load-bearing** — changing them requires deliberate review, not casual edits. New AI assistants and contributors should read this to understand WHY conventions exist before proposing changes.

---

## Decision 1: Flat Notebook Structure

**Decision:** All 21 notebooks live in `/notebooks/` (flat, not nested by week).

**Rationale:**
- Easier to link/reference (simple URLs).
- Clear sequential numbering (`nb00`–`nb20`).
- Students navigate linearly through days.
- GitHub displays flat lists better than nested directories.

---

## Decision 2: 60/20/20 Split for All Examples

**Decision:** Always use 60% train, 20% validation, 20% test.

**Rationale:**
- Consistency across all 21 notebooks.
- Students learn ONE splitting pattern.
- Sufficient validation data for tuning.
- Realistic test set size for course-scale datasets.

---

## Decision 3: `RANDOM_SEED = 474` Everywhere

**Decision:** All random operations use seed 474 (the course number, QM47400).

**Rationale:**
- Complete reproducibility — students get identical outputs.
- Easier to debug — same results every time.
- Course-specific seed (not the generic `42`).
- Memorable for students.

---

## Decision 4: Google Colab + Gemini (Not Local Jupyter)

**Decision:** Primary platform is Google Colab; AI assistance is Google Gemini.

**Rationale:**
- Zero setup for students (no installation issues).
- Consistent environment (same Python/library versions across all students).
- Built-in GPU access (for the deep-learning day).
- Gemini AI assistance integrated natively.
- Accessible from any device.

**Implication for notebook design:** Code must run in a fresh Colab runtime. No hardcoded local paths. Imports must be standard scientific-Python or pip-installable on first cell.

---

## Decision 5: Exclude Admin Materials from Git

**Decision:** `_adm_stuff/` is in `.gitignore`. Instructor notebooks (`*_instructor*.ipynb`) and `video_guides/` are also gitignored.

**Rationale:**
- Student privacy (contact info, accommodations).
- Sensitive data (grades, evaluations).
- Large files (homework solutions, zip archives).
- Public repo — cannot include private materials.
- Instructor solutions must not leak to students browsing the repo.

---

## Decision 6: Micro-Videos (≤12 min each)

**Decision:** All videos capped at 12 minutes maximum.

**Rationale:**
- Attention-span research suggests 10–15 min is optimal for instructional video.
- Mobile-friendly (students can watch on phone).
- Easy to re-watch specific topics.
- Forces concise, focused content.
- ~6 videos per day = ~1 hour total video, leaving time for hands-on notebook work.

---

## Decision 7: "PAUSE-AND-DO" (Not "Exercise" or "Assignment")

**Decision:** Use "PAUSE-AND-DO" terminology for the 10-minute in-notebook practice blocks.

**Rationale:**
- Clear action signal — pause the video, do this now.
- Distinguishes from graded assignments (which are separate).
- Emphasizes active learning over passive reading.
- 10-minute scope — not homework, not a project.
- Builds an engagement habit across all 21 notebooks.

---

## Decision 8: Instructor-First Notebook Editing Workflow

**Decision:** The instructor notebook (`nbNN_*_instructor.ipynb`) is the source of truth. The student notebook (`nbNN_*_student.ipynb`) is generated from it by copy-then-strip-`INSTRUCTOR SOLUTION`-cells.

**Rationale:**
- Single source of truth — solutions and student version cannot drift.
- Solutions live next to the prompts they answer (easier to maintain).
- Student notebook is generated, never hand-edited; this guarantees the student version is always derivable.
- Allows last-minute solution polish without re-writing the student version separately.

**Implication:** Every cell that should be excluded from the student version MUST contain the literal string `INSTRUCTOR SOLUTION`. The strip script keys on this marker. Unmarked solution cells leak into the student notebook.

---

## Decision 9: CV-First Evaluation, Test-Set Locked Until nb14

**Decision:** From `nb09` onward, all model-performance claims come from cross-validation. The test set (`X_test`, `y_test`) is locked — no model evaluation touches it until `nb14`'s "Opening the Locked Test Set" ceremony.

**Rationale:**
- The test-set-lock ceremony in nb14 is pedagogically central. If the test set is touched 30 times beforehand, the ceremony loses meaning.
- Cross-validation is the professionally honest evaluation method; the course teaches it as the spine.
- Students learn that "I peeked at the test set 30 times before reporting accuracy" is the most common subtle leak in industry.

**Exceptions:**
- `nb14` cell 33 only — the one authorized test-set opening.
- `nb18` Kaggle-submission demo — uses `X_test` to simulate predicting on a held-out CSV (production-pipeline pattern, not model evaluation).

**Implication:** Before every commit in `nb09`–`nb20`, run `scripts/audit_cv_first.py`. The only acceptable hits are the nb14/nb18 exceptions.

---

## Decision 10: Narrative Polish Pattern (nb08 Style)

**Decision:** Every student-notebook markdown cell follows the nb08 narrative style — named business stakeholder in "Why This Matters", flowing prose over bullet lists, inline `"A question that often comes up here"` Q&A blocks, explicit section bridges, warm wrap-ups bridging to the next notebook.

**Rationale:**
- Students read notebooks alone, often late at night. The voice must be encouraging and complete, not skeletal.
- Named stakeholders (HomeValue CFO, MedScreen chief medical officer) make business framing concrete instead of abstract.
- Inline Q&A pre-empts the most common confusions, reducing "I'm stuck and don't know what to ask" moments.
- The `"A question that often comes up here"` phrase is grep-findable for tooling and audits.

**Implication:** New markdown cells longer than ~150 words should be checked against the polish pattern before commit. See `CLAUDE.md` for the polish helper script and the audit checklist.

---

## Decision 11: MC Option-Length Parity in All Assessments

**Decision:** In every multiple-choice question (quizzes, midterm, any future exam), all options must sit in the same length-and-elaboration band: every option ≥ 60% of the question's longest option, and per bank the correct option is strictly longest in ≤ 40% of questions (target ~25%, chance). Distractors carry their own flawed-but-specific rationale at the correct option's elaboration and connector-word density.

**Rationale:**
- In 2026Summer, correct options were authored as full decisions-with-rationale while distractors stayed terse. Two students independently reported (extra-credit program, 2026-06-12) that "always pick the longest option" scored ~100%. Hypothesis tests confirmed it: correct-is-longest in 96% of quiz questions (250 analyzed) and 99.5% of midterm questions (210 analyzed) vs. 25% chance, p < 10⁻¹²³; the midterm's connector-word density showed the same cue.
- Length-balanced, equally-elaborated distractors restore the assessments' validity: the only way to eliminate an option is to recognize the misconception it encodes.

**Exceptions:** none. Numeric/label options satisfy the band by formatting all options in the same shape (e.g., `k = 2` / `k = 100`).

**Implication:** Before importing any quiz/exam CSV to Brightspace, run `python scripts/audit_answer_length.py --file <csv>` — PASS is mandatory. Authoring spec: `scripts/_distractor_rewrite_instructions.md`; per-bank rules embedded in `_quizzes/2026Summer/quiz_generation_plan.md` §4.5 and `_midterm_exam/2026Summer/midterm_generation_plan.md` §5.6. All 48 quiz CSVs and 14 midterm case CSVs were rewritten to this standard on 2026-06-12.

---

## Decision 12: Adopt the RDSS Taxonomy Outright — the Inquiry Compass (2026-07-19)

**Decision:** Retire the four-approach grid (description / statistical inference /
predictive modeling / causal reasoning) as the course's classification scheme and
adopt the book's own taxonomy: every research question is classified by **kind**
(descriptive vs causal inquiry, RDSS ch. 7) and **reach** (the data at hand / a
population beyond the data / cases not yet seen) — branded in course materials as
the **inquiry compass**. The four deep-dive modules survive as named compass
positions: Description (nb06, descriptive · data at hand), **Generalization**
(nb10, descriptive · population — renames "statistical/observational inference"),
Prediction (nb12, descriptive · unseen cases), Causal reasoning (nb13, causal
kind). MIDA + diagnosis remain the cross-cutting machinery.

**Rationale:**
- The old grid stood *beside* the textbook's taxonomy: students read RDSS ch. 7's
  two-family split while the course taught four families, with no student-facing
  reconciliation. Deriving the positions from kind × reach makes the course and
  its book one system.
- The claim-boundary drills survive stronger: every overclaim is now a **compass
  crossing without its license** — sample→population licensed by a sampling data
  strategy (violation: the silent upgrade), observed→unseen licensed by
  prediction-time honesty + held-out diagnosands (violation: leakage),
  descriptive→causal licensed by assignment/identification (violations:
  after-therefore-because, design mimicry). "You buy kind and reach with your
  data strategy, and you prove the purchase with diagnosis."
- Prediction gets an honest textbook home: nb12 authors the design-library entry
  RDSS stops short of — "Observational: predictive" — in the book's own
  declare-diagnose-redesign format (I = target for unseen units; leakage = a
  data-strategy violation; held-out performance = a diagnosand; baseline
  comparison = redesign).
- EDA is taught as the **explore → declare → confirm loop**, not a topic:
  upstream M-calibration (nb04), the named anchor (nb06), the §9.1.3
  whole-procedure rule (nb09), and ch. 22 pivoting/reconciliation (nb17).

**Implication:** `course_config.yaml` now carries `inquiry_framework:` (replacing
`approaches:`); `planning/INQUIRY_MAP.md` (renamed from QUANTITATIVE_APPROACH_MAP)
is canonical; the notebook template block is `## 🧭 Inquiry & Claim Boundary` with
`**Inquiry emphasis:**` (validator updated); the schedule column is `inquiry`
(renamed from `approach`); the student template is
`project/templates/INQUIRY_DECLARATION.md` with kind/reach checkboxes and a
crossing-licenses table; the CLAUDE.md critical rule is "Inquiry-Declaration
Justification". Notebook filenames (e.g., `nb02_four_approaches*`) were kept for
link stability — display titles changed everywhere.

---

## Decision 13: Friday Studios + Phase 1–2 Compression (2026-07-20)

**Decision:** Every Friday is a **studio**: ≈10 min topic recap + ≈10 min
instructor presentation of the next project milestone (from its Brightspace
brief) + ≈30 min supervised milestone/project work with rotating consults. No
new topic content on Fridays. Simultaneously, Phases 1–2 compress from 14
meetings to ~10: P1 = M1–M4 (nb00=1, nb01=2 lectures), P2 = M5–M11 (nb02–nb05
one lecture each), with Phase 2 content ending Wed Sep 16 (week 4). Freed slots
flow to Phase 3 (now M12–M22: nb06=1, nb07/nb09/nb10 two lectures each). nb08
becomes the async Friday-studio module (Oct 2, M05 work day). Every milestone is
kicked off on a Friday; three due dates moved (M00 Aug 26→Aug 28, M03 Sep
16→Sep 18, M05 Oct 7→Oct 2); hard anchors (M07 Oct 9/16, M12 Nov 6, M16 Nov 17,
M22 Dec 7/9, M23 Dec 11) unchanged.

**Rationale:** The prior calendar front-loaded question-formulation and
literature/measurement (32% of the semester) while layering milestone
presentations on top of new Friday content. A fixed weekly rhythm — learn
Mon/Wed, consolidate and build the project Fri — protects project time,
makes milestone expectations explicit, and moves students into the technical
phases (data, answer strategies, diagnosis) a week earlier.

**Implication:** `scripts/schedule_data/part1–4.py` rewritten; lecture labels
derived via `lecture_labels()` in `scripts/notebooks_map.py`; session guides and
notebooks reference lectures (never meetings or dates).

---

## Decision 14: Undergraduate-Friendly Voice (2026-07-20 — supersedes D10's punctuation habits)

**Decision:** Keep D10's narrative machinery (named-stakeholder "Why This
Matters" openers, "A question that often comes up here" Q&A blocks, prose over
bullets, bridges, warm wrap-ups) but enforce an undergraduate-friendly voice:
em-dashes ≤ 20 per notebook and ≤ 1 per markdown cell; every technical term
introduced as bold term → one-sentence plain definition → concrete example;
sentences ~12–25 words; second person throughout; no fourth-wall meta-references
about how the material was constructed.

**Rationale:** The built notebooks averaged ~2 em-dashes per markdown cell and
introduced compass/RDSS jargon without plain-language onboarding — reading as
AI-generated and taxing for honors students with no quantitative background.
MGMT474's student notebooks (the course's infra ancestor) demonstrate the
target: same pedagogy, restrained punctuation, term-definition-example rhythm.

**Implication:** `scripts/voice_lint_notebooks.py` gains an em-dash budget,
banned meta-phrases, and date-pattern checks; `_project_docs/ACTIVITY_TEMPLATE.md`
§5 rewritten; all 20 notebook sources rewritten and rebuilt.

---

## Decision 15: Material/Schedule Split, Dataset Zip, Password-Gated Instructor Tab (2026-07-20)

**Decision:** The site splits into **Material** (topic-indexed: notebook Colab
badge, dataset zip, readings — generated by `scripts/build_material_page.py`)
and **Schedule** (date-indexed calendar) tabs, QM670-style. All datasets live in
`notebooks/data/` and ship as one bundle `notebooks/data/honr46400_datasets.zip`
(regenerated by `scripts/make_dataset_zip.py`), linked from both pages. A new
**Instructor** tab is client-side encrypted (password `eureka`,
`scripts/protect_instructor_page.py`, wired post-render) and lists Colab badges
pointing at the private repo
`davi-moreira/2026F_evidence_driven_research_purdue_HONR464_instructor`, synced
by `scripts/sync_instructor_repo.sh` from gitignored local material.

**Rationale:** Students need a stable topic-indexed resource catalog separate
from the calendar; a single zip is the offline data path; the instructor needs
the same one-click Colab access to solution notebooks without ever committing
them to the public repo. The page password is a courtesy lock — the private repo
plus GitHub auth is the real protection.

---

## Decision 16: Fabricated Citations Removed Course-Wide (2026-07-20)

**Decision:** The planted-fake-citation teaching device (previously nb00, nb03,
nb08, nb15) is removed entirely. Citation-verification skills are taught with
real, retrievable sources that students locate and confirm. `scripts/audit_sources.py`
now treats the former planted-fake names as a hard blocklist with no disclosure
exemption.

**Rationale:** The device required fourth-wall meta-asides ("fabricated for the
verification exercise") that undercut the course's own evidence-integrity spine
and read as AI-generated filler. Verifying real sources exercises the same
skill without shipping fakes in student material.

---

## Decision 17: Prompt-Architecture Rebuild — the v2 Course (2026-07-22, instructor ruling)

**Decision:** The instructor's Fall 2026 master prompt governs the course
architecture. The course is rebuilt as **16 weekly topics (nb00–nb15, one
notebook per week)** over a **43-meeting calendar** (41 in-person + 2 async;
NO class Wed Nov 18, the day after the Expo), with **milestones M0–M15**.
Weeks 5–9 follow the DeclareDesign design library (RDSS ch. 15–18): one week
each for observational descriptive, observational causal, experimental
descriptive, prediction, and experimental causal designs — prediction treated
as its own answer objective, never forced into either grid. The **inquiry
compass (RDSS ch. 7) is retained as the question-classification layer**
(taught Week 2, used in every declaration); the retired four-approach grid
does NOT return. Friday studios adopt the four-section format: stand-up /
milestone kickoff + AI sprint / peer + AI red-team / revise + submit.

**Rationale:** The instructor ruled (2026-07-22) that the new prompt's
architecture must govern and new material be developed. RDSS carries both
layers natively (ch. 7 for questions, ch. 14–19 for designs), so the compass
and the pathway weeks are one system, not competitors.

**Implication:** Supersedes D12's notebook sequencing (compass concepts and
claim-boundary machinery survive) and D13's Friday section format (the
studio-Friday principle — no new topic content on Fridays — survives). All 20
v1 notebooks, 24 v1 milestone briefs, and the 44-meeting schedule are replaced;
v1 is preserved at tag `v1-compass-build` and mined per
`planning/SOURCE_AUDIT_V2.md` §7.

---

## Decision 18: Flipped Classroom — the Student Research Lead System (2026-07-22)

**Decision:** Every Mon/Wed lecture from Week 2 onward is led by a **Student
Research Lead (SRL)** running a Socratic investigation (never a summary
presentation): a concrete puzzle first, prior beliefs elicited, commitment
before AI, directed Gemini use, human-vs-AI comparison, assumption probing,
revision, and a closing defense. 25 lead slots ÷ 5 students = 5 leads each,
assigned by rotation seats A–E in the schedule data. The 50-minute classes use
fixed four-section architectures (Mon 9/22/12/7; Wed 7/23/12/8) enforced by
the session-guide generator. SRL performance is graded on a rubric
(conceptual correctness, Socratic quality, assumption exposure, productive AI
use, AI interrogation, inclusion, time management, connection to research
decisions, handling uncertainty).

**Rationale:** The master prompt's central pedagogy; with a 5-person honors
seminar, frequent leading is feasible and rehearses exactly the skills the
Expo and the final defense assess.

**Implication:** `scripts/schedule_data/` carries `srl_slot` + `srl_focus`
per lecture; the SRL handbook/templates/rubric live in `project/srl/`;
Week 1's two lectures stay instructor-led to model the format.

---

## Decision 19: AI Stack — Gemini Primary, GenAI Studio Reviewer Bench (2026-07-22)

**Decision:** Google Gemini (in/alongside Colab) remains the embedded
in-notebook research assistant; all prompts are REWRITTEN for the v2 material.
**Purdue GenAI Studio** (genai.rcac.purdue.edu) is built out as the course's
reviewer bench: custom role models (base model + system prompt + course
knowledge base), shared via a course group, with required milestone
touchpoints (M5 Causal Identification Skeptic; M7 Prediction & Leakage
Auditor; M9 Poster Critic + Robustness & Sensitivity Reviewer; M13
Reproducibility Auditor) and an OpenAI-compatible-API Colab proof-of-concept
(Colab Secrets, never keys in code; manual-UI fallback is a first-class path).
Materials use the six-level taxonomy (prompted role → custom model → RAG
assistant → sequential multi-role workflow → autonomous agent → multi-agent
orchestration) and implement GenAI Studio only at levels 1–4 — it has NO
native agents and materials never claim otherwise.

**Rationale:** Rewriting 84 working Gemini prompts to a different primary tool
buys nothing; GenAI Studio's verified capabilities (custom models, RAG KBs,
groups, multi-model comparison, OpenAI-compatible API) map exactly onto the
reviewer-role pedagogy and the model-disagreement lessons.

**Implication:** Role specs + KB strategy + PoC live in `genai_studio/`;
student access must be verified by the instructor before the semester (open
item); the SDIIVDD discipline (Specify → Delegate → Interrogate → Inspect →
Verify → Document → Defend) becomes the course's full AI-collaboration loop
with Ask → Verify → Document as its everyday shorthand.

---

## Decision 20: The Course Book — 37 Chapters, Six Parts (2026-07-22)

**Decision:** Build the full 37-chapter open-access Quarto book ("Evidence-
Driven Research: How to Design, Analyze, Verify, and Defend Empirical
Research") in `book/`, rendered into `docs/book/` with a site Book tab.
Chapters synchronize with the v2 notebooks + site (Part I ↔ nb00; II ↔
nb01–03; III ↔ nb04–08; IV ↔ nb07–09 + cross-cutting; V ↔ nb10–12; VI ↔
nb13–15), each carrying: the research decision, conceptual explanation, a
STEM worked example, a Colab lab link, recommended AI prompts, a "Do not
delegate" box, an AI failure case, a verification lab, project transfer, and
a defend-your-decision activity. RDSS remains the assigned theory text.

**Rationale:** Instructor ruling (2026-07-22): full book, synchronized with
the new notebooks and site. Building it AFTER the notebooks stabilize keeps
one source of truth; `scripts/validate_book_sync.py` enforces chapter↔notebook
links both ways.

---

## Decision 21: The AI Research Ledger (2026-07-22)

**Decision:** The v1 "AI-use ledger" habit and per-deliverable disclosure
block are unified into ONE structured artifact: the **AI Research Ledger**,
with fixed fields (task delegated · tool used · prompt · output summary ·
decision · verification method · remaining concern · responsible researcher).
Every notebook carries a ledger-entry block; every milestone submission
appends to the student's cumulative ledger inside the Research Project
Dossier. The claim ledger (claims, evidence, verification, boundaries)
remains a DISTINCT instrument: the claim ledger tracks what the research
asserts; the AI Research Ledger tracks what AI did and how it was checked.
Missing ledger entries keep the v1 penalty: the rubric's Craft criterion
scores 0 and the submission is returned.

**Rationale:** One named artifact, taught on day 1 and audited at every
milestone, turns the responsible-AI-use rule from a habit into a graded,
inspectable record — and gives the M13 red-team and M15 portfolio their
primary source.

---

## Decision 22: Week-aligned numbering, quiz-first Fridays, notebook-embedded SRL briefs, confirmed assessment (2026-07-27)

**Decision:** Instructor ruling, seven parts.
1. **Renumbering:** the weekly topic notebooks run `nb01`–`nb16` so the week
   number always equals the notebook number (formerly `nb00`–`nb15`; files,
   registry keys, Topic NN headers, book links, and planning docs all shifted;
   milestones keep M0–M15 and studio notebooks keep ms00–ms15).
2. **SRL assignment:** lead slots are randomly assigned at the start of the
   semester — the seat A–E rotation is retired. No student-facing "five times"
   promise; no five-day SRL-page release.
3. **SRL briefs:** each lecture's SRL guidance is a STUDENT-VISIBLE
   `### 🎤 SRL Lead Brief` cell opening that lecture in its notebook (after
   `# Lecture N`, before the 🧩 Research Puzzle). The old instructor-only "SRL
   page" cells are retired. Briefs must be simple to follow, and must leave
   explicit room for the lead's own staging ("the brief is a floor, not a
   ceiling"). The voice linter allow-lists the exact role name
   "Student Research Lead"/"Student-led" (proper noun, not third-person voice).
   The SRL guide is also a course-book appendix (`book/srl.qmd`).
4. **Friday studios are quiz-first:** 0–10 weekly multiple-choice topic quiz
   (printed, solo, graded) · 10–15 stand-up · 15–32 milestone kickoff +
   AI-supported sprint · 32–42 peer + AI red-team review · 42–50 revise,
   ledger, submit. Quiz masters + keys + D2L banks: `_quizzes/2026Fall/weekly/`
   (gate: `scripts/audit_answer_length.py --file`).
5. **Assessment (confirmed):** Lecture Notebook Completion 10 · Quizzes 20 ·
   SRL performance 20 · Final Project Milestones 20 · Final Project 20 ·
   Research artifact (paper/chapter/note) 10.
6. **Course book:** retitled "Evidence-Driven Research in AI-era: How to
   Design, Analyze, Verify, and Defend"; presented as a work in progress under
   development across the semester.
7. **Site:** course description replaced verbatim (no bold); learning outcomes
   mirror it; the AI-tagline blockquote, async/no-class bullets, midterm/exam
   sentence, revision-policy block, and Milestone Chain section are off the
   home/syllabus pages — the milestone chain and weekly architecture now live
   in nb01 Lecture 1 (dateless; dates stay on Schedule). The tagline drops its
   em dash: "your arm, your RA, not your brain."

**Rationale:** Instructor review of the v2 build (2026-07-27): align numbering
with weeks for student legibility; make the SRL system simpler, public, and
creative; add weekly retrieval practice with a graded quiz; settle grading
weights; de-clutter the public pages while keeping operational detail in the
first notebook, the book appendix, and the schedule.

---

## Decision 23: EDRAI book-first loop, agnostic book, translations, notebook de-cluttering (2026-07-27)

**Decision:** Instructor ruling, second review round.
1. **EDRAI.** The course book's acronym is **EDRAI** (*Evidence-Driven Research
   in AI-era: How to Design, Analyze, Verify, and Defend*). Reading model:
   **EDRAI chapters are the required reading; the matching RDSS chapters are
   recommended** — EDRAI exists to translate RDSS to the econ/STEM/business
   undergraduate audience. Every chapter carries a Reading box naming its RDSS
   companions, and a verification-section callout stating: **AI can review AI,
   but the last decision is always human.** The Book tab opens in a new tab.
2. **The book-first loop.** Going forward: (a) notebook content must reflect
   the book; (b) the instructor manually reviews and updates the book; (c) the
   assistant then articulates and incorporates those reviews across the course
   material (notebooks, guides, site); (d) the book stays
   **institution-agnostic** (usable by instructors/students outside Purdue —
   generic "course platform", "AI reviewer bench", "your research conference"
   phrasing in chapter bodies; Purdue specifics only as parentheticals).
3. **Translations.** EDRAI ships in Brazilian Portuguese (`book-pt/` →
   `docs/book-pt`) and Spanish (`book-es/` → `docs/book-es`). The English
   edition is the source of truth; translations are regenerated from it after
   EN edits. Render all three books on any book change.
4. **Notebook de-cluttering.** The vacuous "all positions (…)" inquiry-emphasis
   tags and the pipe-separated build-provenance metadata lines are retired from
   student-facing cells (validator updated; the end-of-notebook Sources &
   Provenance section stays). The course's opening claim standard is now: "An
   AI tool generated this, the source exists, and I read, confirmed, and
   criticized the underlying argument or technique before using it."
5. **nb01 welcome.** The first notebook opens Lecture 1 with the professor's
   introduction (bio, Palmeiras, Carnaval de Olinda; images in
   `images/professor/`), mirroring the MGMT305 opening-lecture format.
6. **Syllabus de-policying.** The late-policy line and the Poster & Conference
   and Reproducibility policy sections are removed from the syllabus page
   (reproducibility remains enforced through milestones and notebooks).

**Rationale:** Instructor review 2026-07-27 (second round): make the book the
reviewable center of the course with a clear propagation loop, open it to
audiences beyond Purdue (including PT-BR/ES readers), tighten the student
notebooks to content that serves the reader, and raise the claim standard from
"the source exists" to "I read, confirmed, and criticized it."

---

## Decision 24: EDR|AI — the self-contained manual (2026-07-27, third review round)

**Decision:** Instructor ruling.
1. **Title/brand:** the book is **EDR|AI — Evidence-Driven Research in the Age
   of AI** (subtitle: How to Design, Analyze, Verify, and Defend) in all three
   languages; the site tab reads "Book: EDR|AI" and opens in a new tab.
2. **Self-contained manual:** chapter bodies carry NO course furniture
   (milestones, studios, quizzes, rubrics, "this course"). The three closing
   sections (Verification laboratory · Project transfer · Defend your
   decision) are replaced by ONE final **"It is your turn"** section per
   chapter; the 37 sections chain into a complete research project and a draft
   research artifact by the end of the book. Sync-validator element set
   updated accordingly.
3. **Domains:** worked examples come from econ, political science, business,
   and biology, at undergraduate level, in a friendly first-person-researcher
   register (the ch. 2 "run the assay… that part is mine" passage is the
   exemplar).
4. **The AI loop:** the book teaches AI use as a LOOP (prompt → output →
   interrogate → refine → run again; agentic tools run loops autonomously),
   formally introduced in ch. 3 with SDIIVDD as the checklist that governs
   every cycle; chs. 19–20 and 35–36 build on it.
5. **Apparatus:** in-chapter Reading boxes retired; the verification guide is
   now a book APPENDIX (book/verification-guide.qmd, from
   ai_resources/verification_guide.md) and all chapter links point at it; new
   appendices: About the Author; Part I opens with an overview page + mermaid
   diagram of the book's arc; Part I retitled 'Research when AI does
   "everything"'; every book page carries a language switcher (EN · PT-BR ·
   ES) via include-before-body.
6. **nb01:** an explicit ⚙️ Setup section (setup + readiness + AI Research
   Partner) precedes Lecture 1; Lecture 1 is the orientation lecture
   (professor intro with updated title line — Quantitative Methods Department,
   Director of the Daniels Undergraduate Business Honors Program — student
   intros, course at a glance, weekly rhythm + milestone chain, grading,
   materials/logistics, questions), with the SRL Lead Brief and Research
   Puzzle moved after orientation.

**Rationale:** make EDR|AI a book that stands entirely on its own — a manual
any student anywhere can follow to a finished, defensible research artifact —
while the course wraps around it, not the other way round.

## Decision 25: Book/course separation — companion notebooks, For Instructors, book-anchored milestones (2026-07-28, fourth review round)

**Decision:** Instructor ruling. The book and the course are DIFFERENT
artifacts, coupled only through the book-first loop.

1. **The book owns its notebooks:** every chapter has its own companion Colab
   notebook (`notebooks/book/chNN_<slug>.ipynb`, plus `pt/` and `es/`
   editions), generated from the chapter sources by
   `scripts/build_book_notebooks.py` (rerun after any chapter edit). The
   chapter badge opens the companion notebook — a reader runs the chapter's
   code and completes its "It is your turn" section there, with no course.
   Each chapter's "Colab laboratory" section introduces the companion notebook
   first, then names the classroom lab (course notebook nbNN) as
   companion-course material with an inline Colab link.
2. **The course refers to the book:** (a) readings — EDR|AI chapters required,
   RDSS recommended (unchanged); (b) course notebooks derive from the book's
   chapters (lecture structure/dynamics unchanged); (c) every milestone brief
   M0–M15 carries a "Book Anchor — It Is Your Turn" section + submission-table
   row: students complete and submit the anchored chapters' "It is your turn"
   sections (milestone NN anchors the chapters whose primary lab is
   nb(NN+1); the 16 anchors partition all 37 chapters).
3. **For Instructors appendix** (`for-instructors.qmd`, all three editions):
   presents the companion course and makes its material available — the
   two-artifacts model, the weekly SRL/studio architecture, the milestone
   chain, and a table of all 16 course labs with their chapters and Colab
   links.
4. **Front matter:** About the Author moves from the appendices to directly
   AFTER the Preface (unnumbered page); book author is "Davi Moreira" (no
   title); new preface/description blurb — "an open research manual for
   undergraduates who aspire to produce high-quality research with scientific
   impact…" (domains list and "A work in progress" dropped from the blurb; the
   in-preface work-in-progress callout stays).
5. **Validator:** `validate_book_sync.py` now also requires each chapter to
   link its companion notebook, the For-instructors appendix to exist in all
   three editions and link all 16 labs, and PT/ES chapters to link their
   localized companions.

**Rationale:** a reader anywhere can complete the whole manual from the
chapter badges alone, while the course consumes the book (readings, derived
labs, milestone-collected "It is your turn" chains) and the book presents the
course to instructors — separation with an explicit, validated interface.
